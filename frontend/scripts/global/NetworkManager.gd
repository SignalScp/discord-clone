extends Node

## NetworkManager - Handles all network communication
## Singleton autoload for HTTP requests and WebSocket connections

# API Configuration
const API_BASE_URL = "http://localhost:8000"
const WS_BASE_URL = "ws://localhost:8000"

# WebSocket
var websocket: WebSocketPeer = null
var ws_connected: bool = false
var current_channel_id: int = -1
var reconnect_timer: Timer = null
var reconnect_attempts: int = 0
const MAX_RECONNECT_ATTEMPTS = 5

# Signals
signal message_received(message_data: Dictionary)
signal user_joined(user_id: int)
signal user_left(user_id: int)
signal connection_established()
signal connection_lost()
signal connection_error(error: String)


func _ready() -> void:
	"""Initialize network manager."""
	print("[NetworkManager] Initialized")
	
	# Create reconnect timer
	reconnect_timer = Timer.new()
	reconnect_timer.one_shot = true
	reconnect_timer.timeout.connect(_on_reconnect_timeout)
	add_child(reconnect_timer)


func _process(_delta: float) -> void:
	"""Poll WebSocket for incoming messages."""
	if websocket and ws_connected:
		websocket.poll()
		
		var state = websocket.get_ready_state()
		
		if state == WebSocketPeer.STATE_OPEN:
			while websocket.get_available_packet_count():
				var packet = websocket.get_packet()
				var data_string = packet.get_string_from_utf8()
				var json = JSON.new()
				var error = json.parse(data_string)
				
				if error == OK:
					var message_data = json.data
					_handle_websocket_message(message_data)
				else:
					print("[NetworkManager] Failed to parse WebSocket message")
					
		elif state == WebSocketPeer.STATE_CLOSED:
			if ws_connected:
				print("[NetworkManager] WebSocket connection closed")
				ws_connected = false
				connection_lost.emit()
				_attempt_reconnect()


## HTTP Requests

func http_request(method: String, endpoint: String, data: Dictionary = {}, token: String = "") -> Dictionary:
	"""Make HTTP request to backend API.
	
	Args:
		method: HTTP method (GET, POST, PATCH, DELETE)
		endpoint: API endpoint (e.g., '/auth/login')
		data: Request body data
		token: Optional JWT token for authentication
		
	Returns:
		Dictionary with 'success', 'data', and 'error' keys
	"""
	var http = HTTPRequest.new()
	add_child(http)
	
	var url = API_BASE_URL + endpoint
	var headers = ["Content-Type: application/json"]
	
	if token != "":
		headers.append("Authorization: Bearer " + token)
	
	var body = ""
	if not data.is_empty():
		body = JSON.stringify(data)
	
	var http_method = HTTPClient.METHOD_GET
	match method:
		"POST":
			http_method = HTTPClient.METHOD_POST
		"PATCH":
			http_method = HTTPClient.METHOD_PATCH
		"DELETE":
			http_method = HTTPClient.METHOD_DELETE
	
	http.request(url, headers, http_method, body)
	
	# Wait for response
	var response = await http.request_completed
	var result = response[0]
	var response_code = response[1]
	var response_headers = response[2]
	var response_body = response[3]
	
	http.queue_free()
	
	# Parse response
	var response_text = response_body.get_string_from_utf8()
	var json = JSON.new()
	var parse_error = json.parse(response_text)
	
	if result != HTTPRequest.RESULT_SUCCESS:
		return {"success": false, "error": "Network error", "data": {}}
	
	if parse_error != OK:
		return {"success": false, "error": "Parse error", "data": {}}
	
	var response_data = json.data
	
	if response_code >= 200 and response_code < 300:
		return {"success": true, "data": response_data, "error": ""}
	else:
		var error_msg = response_data.get("detail", "Unknown error")
		return {"success": false, "error": error_msg, "data": response_data}


## WebSocket

func connect_websocket(user_id: int, server_id: int, channel_id: int, token: String) -> bool:
	"""Connect to WebSocket for real-time messaging.
	
	Args:
		user_id: Current user ID
		server_id: Server ID
		channel_id: Channel ID
		token: JWT authentication token
		
	Returns:
		True if connection initiated successfully
	"""
	if websocket and ws_connected:
		disconnect_websocket()
	
	websocket = WebSocketPeer.new()
	var url = "%s/ws/%d/%d/%d?token=%s" % [WS_BASE_URL, user_id, server_id, channel_id, token]
	
	print("[NetworkManager] Connecting to WebSocket: ", url)
	
	var error = websocket.connect_to_url(url)
	
	if error != OK:
		print("[NetworkManager] Failed to connect to WebSocket: ", error)
		connection_error.emit("Failed to connect")
		return false
	
	current_channel_id = channel_id
	reconnect_attempts = 0
	
	# Wait for connection
	await get_tree().create_timer(1.0).timeout
	
	if websocket.get_ready_state() == WebSocketPeer.STATE_OPEN:
		ws_connected = true
		print("[NetworkManager] WebSocket connected")
		connection_established.emit()
		return true
	else:
		print("[NetworkManager] WebSocket connection failed")
		return false


func disconnect_websocket() -> void:
	"""Disconnect from WebSocket."""
	if websocket:
		websocket.close()
		ws_connected = false
		websocket = null
		print("[NetworkManager] WebSocket disconnected")


func send_websocket_message(message_data: Dictionary) -> void:
	"""Send message through WebSocket.
	
	Args:
		message_data: Message data to send
	"""
	if not websocket or not ws_connected:
		print("[NetworkManager] Cannot send message: WebSocket not connected")
		return
	
	var json_string = JSON.stringify(message_data)
	var error = websocket.send_text(json_string)
	
	if error != OK:
		print("[NetworkManager] Failed to send WebSocket message: ", error)


func _handle_websocket_message(data: Dictionary) -> void:
	"""Handle incoming WebSocket message.
	
	Args:
		data: Message data received
	"""
	var msg_type = data.get("type", "")
	var msg_data = data.get("data", {})
	
	match msg_type:
		"message":
			message_received.emit(msg_data)
		"user_join":
			user_joined.emit(msg_data.get("user_id", 0))
		"user_leave":
			user_left.emit(msg_data.get("user_id", 0))
		_:
			print("[NetworkManager] Unknown message type: ", msg_type)


func _attempt_reconnect() -> void:
	"""Attempt to reconnect WebSocket."""
	if reconnect_attempts >= MAX_RECONNECT_ATTEMPTS:
		print("[NetworkManager] Max reconnection attempts reached")
		return
	
	reconnect_attempts += 1
	var delay = pow(2, reconnect_attempts - 1)  # Exponential backoff
	print("[NetworkManager] Reconnecting in %d seconds (attempt %d/%d)" % [delay, reconnect_attempts, MAX_RECONNECT_ATTEMPTS])
	
	reconnect_timer.start(delay)


func _on_reconnect_timeout() -> void:
	"""Handle reconnection timeout."""
	print("[NetworkManager] Attempting to reconnect...")
	# Reconnection logic should be handled by the scene that initiated the connection
	connection_error.emit("Connection lost. Please reconnect.")
