extends Node

## AuthManager - Manages user authentication state
## Singleton autoload for storing auth token and user data

# User data
var current_user: Dictionary = {}
var auth_token: String = ""
var is_authenticated: bool = false

# Signals
signal authentication_changed(authenticated: bool)
signal user_data_updated(user_data: Dictionary)


func _ready() -> void:
	"""Initialize authentication manager."""
	print("[AuthManager] Initialized")


func login(token: String, user_data: Dictionary) -> void:
	"""Set authentication state after successful login.
	
	Args:
		token: JWT authentication token
		user_data: User profile data
	"""
	auth_token = token
	current_user = user_data
	is_authenticated = true
	
	print("[AuthManager] User logged in: ", user_data.get("username", "unknown"))
	authentication_changed.emit(true)
	user_data_updated.emit(user_data)


func logout() -> void:
	"""Clear authentication state."""
	auth_token = ""
	current_user = {}
	is_authenticated = false
	
	print("[AuthManager] User logged out")
	authentication_changed.emit(false)


func get_token() -> String:
	"""Get current authentication token.
	
	Returns:
		JWT token or empty string
	"""
	return auth_token


func get_user() -> Dictionary:
	"""Get current user data.
	
	Returns:
		User profile dictionary
	"""
	return current_user


func get_user_id() -> int:
	"""Get current user ID.
	
	Returns:
		User ID or -1 if not authenticated
	"""
	return current_user.get("id", -1)


func get_username() -> String:
	"""Get current username.
	
	Returns:
		Username or empty string
	"""
	return current_user.get("username", "")


func update_user_data(user_data: Dictionary) -> void:
	"""Update current user data.
	
	Args:
		user_data: Updated user profile data
	"""
	current_user = user_data
	user_data_updated.emit(user_data)
	print("[AuthManager] User data updated")
