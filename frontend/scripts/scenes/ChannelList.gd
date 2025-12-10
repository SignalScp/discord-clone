extends VBoxContainer

## ChannelList - Displays channels for selected server

@onready var channels_container = $ScrollContainer/ChannelsContainer
@onready var server_name_label = $ServerNameLabel


func _ready() -> void:
	"""Initialize channel list."""
	print("[ChannelList] Ready")
	
	# Connect signals
	DataManager.server_selected.connect(_on_server_selected)
	DataManager.channels_updated.connect(_on_channels_updated)


func _on_server_selected(server: Dictionary) -> void:
	"""Update UI when server is selected.
	
	Args:
		server: Server dictionary
	"""
	server_name_label.text = server.get("name", "Unknown Server")


func _on_channels_updated(channels: Array) -> void:
	"""Update channel list UI.
	
	Args:
		channels: Array of channel dictionaries
	"""
	# Clear existing
	for child in channels_container.get_children():
		child.queue_free()
	
	# Create button for each channel
	for channel in channels:
		var button = Button.new()
		button.text = "# " + channel.get("name", "unknown")
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.pressed.connect(_on_channel_selected.bind(channel.get("id")))
		channels_container.add_child(button)


func _on_channel_selected(channel_id: int) -> void:
	"""Handle channel selection.
	
	Args:
		channel_id: Selected channel ID
	"""
	print("[ChannelList] Channel selected: ", channel_id)
	DataManager.select_channel(channel_id)
