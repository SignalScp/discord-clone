extends VBoxContainer

## ServerList - Displays and manages server list

var server_button_scene = preload("res://scenes/ui_components/ServerButton.tscn")

@onready var servers_container = $ScrollContainer/ServersContainer
@onready var add_button = $AddServerButton


func _ready() -> void:
	"""Initialize server list."""
	print("[ServerList] Ready")
	
	# Connect signals
	DataManager.servers_updated.connect(_on_servers_updated)
	add_button.pressed.connect(_on_add_server_pressed)


func _on_servers_updated(servers: Array) -> void:
	"""Update server list UI.
	
	Args:
		servers: Array of server dictionaries
	"""
	# Clear existing buttons
	for child in servers_container.get_children():
		child.queue_free()
	
	# Create button for each server
	for server in servers:
		var button = Button.new()
		button.text = server.get("name", "Unknown")[0]  # First letter
		button.custom_minimum_size = Vector2(60, 60)
		button.pressed.connect(_on_server_selected.bind(server.get("id")))
		servers_container.add_child(button)


func _on_server_selected(server_id: int) -> void:
	"""Handle server selection.
	
	Args:
		server_id: Selected server ID
	"""
	print("[ServerList] Server selected: ", server_id)
	DataManager.select_server(server_id)
	
	# Load channels for this server
	await _load_channels(server_id)


func _load_channels(server_id: int) -> void:
	"""Load channels for selected server.
	
	Args:
		server_id: Server ID
	"""
	var result = await NetworkManager.http_request(
		"GET",
		"/servers/%d/channels" % server_id,
		{},
		AuthManager.get_token()
	)
	
	if result.success:
		DataManager.set_channels(result.data)
		
		# Auto-select first channel
		if result.data.size() > 0:
			DataManager.select_channel(result.data[0].get("id"))


func _on_add_server_pressed() -> void:
	"""Handle add server button press."""
	print("[ServerList] Add server pressed")
	# TODO: Show create server dialog
