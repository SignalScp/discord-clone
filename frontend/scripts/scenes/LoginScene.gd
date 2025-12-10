extends Control

## LoginScene - User authentication interface
## Handles login and registration

# UI Nodes
@onready var tab_container = $MarginContainer/VBoxContainer/TabContainer
@onready var status_label = $MarginContainer/VBoxContainer/StatusLabel

# Login tab
@onready var login_username = $MarginContainer/VBoxContainer/TabContainer/Login/VBoxContainer/UsernameInput
@onready var login_password = $MarginContainer/VBoxContainer/TabContainer/Login/VBoxContainer/PasswordInput
@onready var login_button = $MarginContainer/VBoxContainer/TabContainer/Login/VBoxContainer/LoginButton

# Register tab
@onready var register_username = $MarginContainer/VBoxContainer/TabContainer/Register/VBoxContainer/UsernameInput
@onready var register_email = $MarginContainer/VBoxContainer/TabContainer/Register/VBoxContainer/EmailInput
@onready var register_password = $MarginContainer/VBoxContainer/TabContainer/Register/VBoxContainer/PasswordInput
@onready var register_confirm = $MarginContainer/VBoxContainer/TabContainer/Register/VBoxContainer/ConfirmPasswordInput
@onready var register_button = $MarginContainer/VBoxContainer/TabContainer/Register/VBoxContainer/RegisterButton

var is_loading: bool = false


func _ready() -> void:
	"""Initialize login scene."""
	print("[LoginScene] Ready")
	
	# Connect signals
	login_button.pressed.connect(_on_login_pressed)
	register_button.pressed.connect(_on_register_pressed)
	
	# Enable enter key for login
	login_password.text_submitted.connect(_on_login_password_submitted)
	register_confirm.text_submitted.connect(_on_register_password_submitted)


func _on_login_pressed() -> void:
	"""Handle login button press."""
	if is_loading:
		return
	
	var username = login_username.text.strip_edges()
	var password = login_password.text
	
	# Validate inputs
	if username.is_empty() or password.is_empty():
		show_status("Please fill in all fields", false)
		return
	
	is_loading = true
	login_button.disabled = true
	show_status("Logging in...", true)
	
	# Prepare login data (OAuth2 format)
	var form_data = "username=%s&password=%s" % [username.uri_encode(), password.uri_encode()]
	
	# Make request
	var http = HTTPRequest.new()
	add_child(http)
	
	var url = NetworkManager.API_BASE_URL + "/auth/login"
	var headers = ["Content-Type: application/x-www-form-urlencoded"]
	
	http.request(url, headers, HTTPClient.METHOD_POST, form_data)
	var response = await http.request_completed
	
	var result = response[0]
	var response_code = response[1]
	var response_body = response[3]
	
	http.queue_free()
	
	is_loading = false
	login_button.disabled = false
	
	# Parse response
	var response_text = response_body.get_string_from_utf8()
	var json = JSON.new()
	var parse_error = json.parse(response_text)
	
	if result != HTTPRequest.RESULT_SUCCESS or parse_error != OK:
		show_status("Network error. Please try again.", false)
		return
	
	var data = json.data
	
	if response_code == 200:
		var token = data.get("access_token", "")
		
		# Get user data
		await _fetch_user_data(token)
	else:
		var error_msg = data.get("detail", "Login failed")
		show_status(error_msg, false)


func _on_register_pressed() -> void:
	"""Handle register button press."""
	if is_loading:
		return
	
	var username = register_username.text.strip_edges()
	var email = register_email.text.strip_edges()
	var password = register_password.text
	var confirm = register_confirm.text
	
	# Validate inputs
	if username.is_empty() or email.is_empty() or password.is_empty():
		show_status("Please fill in all fields", false)
		return
	
	if username.length() < 3:
		show_status("Username must be at least 3 characters", false)
		return
	
	if password.length() < 6:
		show_status("Password must be at least 6 characters", false)
		return
	
	if password != confirm:
		show_status("Passwords do not match", false)
		return
	
	if not email.contains("@"):
		show_status("Invalid email address", false)
		return
	
	is_loading = true
	register_button.disabled = true
	show_status("Creating account...", true)
	
	# Make request
	var register_data = {
		"username": username,
		"email": email,
		"password": password
	}
	
	var result = await NetworkManager.http_request("POST", "/auth/register", register_data)
	
	is_loading = false
	register_button.disabled = false
	
	if result.success:
		show_status("Account created! Logging in...", true)
		
		# Auto-login after registration
		await get_tree().create_timer(1.0).timeout
		login_username.text = username
		login_password.text = password
		tab_container.current_tab = 0
		_on_login_pressed()
	else:
		show_status(result.error, false)


func _fetch_user_data(token: String) -> void:
	"""Fetch user data after login.
	
	Args:
		token: JWT authentication token
	"""
	show_status("Fetching user data...", true)
	
	var result = await NetworkManager.http_request("GET", "/users/me", {}, token)
	
	if result.success:
		var user_data = result.data
		
		# Update auth manager
		AuthManager.login(token, user_data)
		
		show_status("Login successful!", true)
		await get_tree().create_timer(0.5).timeout
		
		# Switch to main scene
		get_tree().change_scene_to_file("res://scenes/main/MainScene.tscn")
	else:
		show_status("Failed to fetch user data: " + result.error, false)


func _on_login_password_submitted(_text: String) -> void:
	"""Handle enter key in login password field."""
	_on_login_pressed()


func _on_register_password_submitted(_text: String) -> void:
	"""Handle enter key in register confirm password field."""
	_on_register_pressed()


func show_status(message: String, is_success: bool) -> void:
	"""Show status message.
	
	Args:
		message: Status message to display
		is_success: Whether this is a success message (green) or error (red)
	"""
	status_label.text = message
	
	if is_success:
		status_label.add_theme_color_override("font_color", Color.GREEN)
	else:
		status_label.add_theme_color_override("font_color", Color.RED)
	
	status_label.visible = true
