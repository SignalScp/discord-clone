extends VBoxContainer

## UserList - Displays online users in current server

@onready var users_container = $ScrollContainer/UsersContainer
@onready var title_label = $TitleLabel


func _ready() -> void:
	"""Initialize user list."""
	print("[UserList] Ready")
	
	# Connect signals
	DataManager.server_selected.connect(_on_server_selected)
	DataManager.members_updated.connect(_on_members_updated)


func _on_server_selected(server: Dictionary) -> void:
	"""Load members when server is selected.
	
	Args:
		server: Server dictionary
	"""
	var server_id = server.get("id")
	await _load_members(server_id)


func _load_members(server_id: int) -> void:
	"""Load server members.
	
	Args:
		server_id: Server ID
	"""
	var result = await NetworkManager.http_request(
		"GET",
		"/servers/%d/members" % server_id,
		{},
		AuthManager.get_token()
	)
	
	if result.success:
		DataManager.set_members(server_id, result.data)


func _on_members_updated(server_id: int, members: Array) -> void:
	"""Update members display.
	
	Args:
		server_id: Server ID
		members: Array of member dictionaries
	"""
	title_label.text = "Members - %d" % members.size()
	
	# Clear existing
	for child in users_container.get_children():
		child.queue_free()
	
	# Add members
	for member in members:
		var user = member.get("user", {})
		var username = user.get("username", "Unknown")
		var status = user.get("status", "offline")
		
		var label = Label.new()
		label.text = "%s (%s)" % [username, status]
		
		# Color based on status
		if status == "online":
			label.add_theme_color_override("font_color", Color.GREEN)
		elif status == "away":
			label.add_theme_color_override("font_color", Color.YELLOW)
		else:
			label.add_theme_color_override("font_color", Color.GRAY)
		
		users_container.add_child(label)
