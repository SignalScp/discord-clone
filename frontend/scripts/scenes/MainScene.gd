extends Control

## MainScene - Main application interface
## Manages the overall UI and coordinates between components

@onready var server_list = $HBoxContainer/ServerList
@onready var channel_list = $HBoxContainer/MiddlePanel/ChannelList
@onready var chat_ui = $HBoxContainer/MiddlePanel/ChatUI
@onready var user_list = $HBoxContainer/UserList


func _ready() -> void:
	"""Initialize main scene."""
	print("[MainScene] Ready")
	
	# Check authentication
	if not AuthManager.is_authenticated:
		print("[MainScene] Not authenticated, returning to login")
		get_tree().change_scene_to_file("res://scenes/login/LoginScene.tscn")
		return
	
	print("[MainScene] User: ", AuthManager.get_username())
	
	# Load user's servers
	await _load_servers()


func _load_servers() -> void:
	"""Load user's servers from backend."""
	print("[MainScene] Loading servers...")
	
	var result = await NetworkManager.http_request("GET", "/servers", {}, AuthManager.get_token())
	
	if result.success:
		var servers = result.data
		DataManager.set_servers(servers)
		print("[MainScene] Loaded %d servers" % servers.size())
		
		# Auto-select first server if available
		if servers.size() > 0:
			DataManager.select_server(servers[0].get("id"))
	else:
		print("[MainScene] Failed to load servers: ", result.error)
