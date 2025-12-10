extends VBoxContainer

## ChatUI - Chat interface with messages and input

@onready var channel_name_label = $ChannelHeader/ChannelNameLabel
@onready var messages_container = $MessagesScroll/MessagesContainer
@onready var message_input = $InputPanel/MessageInput
@onready var send_button = $InputPanel/SendButton

var is_loading: bool = false
var is_connected: bool = false


func _ready() -> void:
	"""Initialize chat UI."""
	print("[ChatUI] Ready")
	
	# Connect signals
	DataManager.channel_selected.connect(_on_channel_selected)
	DataManager.messages_updated.connect(_on_messages_updated)
	DataManager.message_added.connect(_on_message_added)
	
	NetworkManager.message_received.connect(_on_websocket_message)
	NetworkManager.connection_established.connect(_on_ws_connected)
	NetworkManager.connection_lost.connect(_on_ws_disconnected)
	
	send_button.pressed.connect(_on_send_pressed)
	message_input.text_submitted.connect(_on_message_submitted)


func _on_channel_selected(channel: Dictionary) -> void:
	"""Handle channel selection.
	
	Args:
		channel: Channel dictionary
	"""
	var channel_id = channel.get("id")
	channel_name_label.text = "# " + channel.get("name", "unknown")
	
	print("[ChatUI] Loading channel: ", channel_id)
	
	# Disconnect from previous channel
	if is_connected:
		NetworkManager.disconnect_websocket()
		is_connected = false
	
	# Load message history
	await _load_messages(channel_id)
	
	# Connect to WebSocket
	await _connect_websocket(channel_id)


func _load_messages(channel_id: int) -> void:
	"""Load message history for channel.
	
	Args:
		channel_id: Channel ID
	"""
	var result = await NetworkManager.http_request(
		"GET",
		"/messages/channels/%d/messages?limit=50" % channel_id,
		{},
		AuthManager.get_token()
	)
	
	if result.success:
		DataManager.set_messages(channel_id, result.data)
		print("[ChatUI] Loaded %d messages" % result.data.size())


func _connect_websocket(channel_id: int) -> void:
	"""Connect to WebSocket for real-time updates.
	
	Args:
		channel_id: Channel ID
	"""
	var user_id = AuthManager.get_user_id()
	var server_id = DataManager.current_server_id
	var token = AuthManager.get_token()
	
	var success = await NetworkManager.connect_websocket(user_id, server_id, channel_id, token)
	
	if success:
		is_connected = true
		print("[ChatUI] WebSocket connected")


func _on_messages_updated(channel_id: int, messages: Array) -> void:
	"""Update messages display.
	
	Args:
		channel_id: Channel ID
		messages: Array of message dictionaries
	"""
	# Clear existing
	for child in messages_container.get_children():
		child.queue_free()
	
	# Add messages
	for message in messages:
		_add_message_to_ui(message)


func _on_message_added(channel_id: int, message: Dictionary) -> void:
	"""Add new message to display.
	
	Args:
		channel_id: Channel ID
		message: Message dictionary
	"""
	if channel_id == DataManager.current_channel_id:
		_add_message_to_ui(message)


func _add_message_to_ui(message: Dictionary) -> void:
	"""Add message to UI.
	
	Args:
		message: Message dictionary
	"""
	var user = message.get("user", {})
	var username = user.get("username", "Unknown")
	var content = message.get("content", "")
	
	var label = Label.new()
	label.text = "[%s]: %s" % [username, content]
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	messages_container.add_child(label)


func _on_send_pressed() -> void:
	"""Handle send button press."""
	var content = message_input.text.strip_edges()
	
	if content.is_empty():
		return
	
	if is_loading:
		return
	
	is_loading = true
	send_button.disabled = true
	
	# Send via HTTP
	var channel_id = DataManager.current_channel_id
	var result = await NetworkManager.http_request(
		"POST",
		"/messages/channels/%d/messages" % channel_id,
		{"content": content},
		AuthManager.get_token()
	)
	
	is_loading = false
	send_button.disabled = false
	
	if result.success:
		message_input.text = ""
		var message = result.data
		# Message will be added via WebSocket
	else:
		print("[ChatUI] Failed to send message: ", result.error)


func _on_message_submitted(_text: String) -> void:
	"""Handle enter key in message input."""
	_on_send_pressed()


func _on_websocket_message(message_data: Dictionary) -> void:
	"""Handle incoming WebSocket message.
	
	Args:
		message_data: Message data
	"""
	var channel_id = DataManager.current_channel_id
	DataManager.add_message(channel_id, message_data)


func _on_ws_connected() -> void:
	"""Handle WebSocket connection."""
	print("[ChatUI] WebSocket connected")


func _on_ws_disconnected() -> void:
	"""Handle WebSocket disconnection."""
	print("[ChatUI] WebSocket disconnected")
	is_connected = false
