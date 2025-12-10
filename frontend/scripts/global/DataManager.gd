extends Node

## DataManager - Manages cached data and state
## Singleton autoload for storing servers, channels, and messages

# Cached data
var servers: Array = []
var current_server_id: int = -1
var current_server: Dictionary = {}

var channels: Array = []
var current_channel_id: int = -1
var current_channel: Dictionary = {}

var messages: Dictionary = {}  # {channel_id: [messages]}
var server_members: Dictionary = {}  # {server_id: [members]}

# Signals
signal servers_updated(servers_list: Array)
signal server_selected(server: Dictionary)
signal channels_updated(channels_list: Array)
signal channel_selected(channel: Dictionary)
signal messages_updated(channel_id: int, messages_list: Array)
signal message_added(channel_id: int, message: Dictionary)
signal members_updated(server_id: int, members_list: Array)


func _ready() -> void:
	"""Initialize data manager."""
	print("[DataManager] Initialized")


## Servers

func set_servers(servers_list: Array) -> void:
	"""Update servers list.
	
	Args:
		servers_list: Array of server dictionaries
	"""
	servers = servers_list
	servers_updated.emit(servers_list)
	print("[DataManager] Servers updated: ", servers.size())


func add_server(server: Dictionary) -> void:
	"""Add new server to list.
	
	Args:
		server: Server dictionary
	"""
	servers.append(server)
	servers_updated.emit(servers)
	print("[DataManager] Server added: ", server.get("name", "unknown"))


func select_server(server_id: int) -> void:
	"""Select a server.
	
	Args:
		server_id: Server ID to select
	"""
	current_server_id = server_id
	
	# Find server in list
	for server in servers:
		if server.get("id") == server_id:
			current_server = server
			server_selected.emit(server)
			print("[DataManager] Server selected: ", server.get("name", "unknown"))
			return


## Channels

func set_channels(channels_list: Array) -> void:
	"""Update channels list.
	
	Args:
		channels_list: Array of channel dictionaries
	"""
	channels = channels_list
	channels_updated.emit(channels_list)
	print("[DataManager] Channels updated: ", channels.size())


func add_channel(channel: Dictionary) -> void:
	"""Add new channel to list.
	
	Args:
		channel: Channel dictionary
	"""
	channels.append(channel)
	channels_updated.emit(channels)
	print("[DataManager] Channel added: ", channel.get("name", "unknown"))


func select_channel(channel_id: int) -> void:
	"""Select a channel.
	
	Args:
		channel_id: Channel ID to select
	"""
	current_channel_id = channel_id
	
	# Find channel in list
	for channel in channels:
		if channel.get("id") == channel_id:
			current_channel = channel
			channel_selected.emit(channel)
			print("[DataManager] Channel selected: ", channel.get("name", "unknown"))
			return


## Messages

func set_messages(channel_id: int, messages_list: Array) -> void:
	"""Set messages for a channel.
	
	Args:
		channel_id: Channel ID
		messages_list: Array of message dictionaries
	"""
	messages[channel_id] = messages_list
	messages_updated.emit(channel_id, messages_list)
	print("[DataManager] Messages loaded for channel %d: %d messages" % [channel_id, messages_list.size()])


func add_message(channel_id: int, message: Dictionary) -> void:
	"""Add new message to channel.
	
	Args:
		channel_id: Channel ID
		message: Message dictionary
	"""
	if not messages.has(channel_id):
		messages[channel_id] = []
	
	messages[channel_id].append(message)
	message_added.emit(channel_id, message)
	

func get_messages(channel_id: int) -> Array:
	"""Get messages for a channel.
	
	Args:
		channel_id: Channel ID
		
	Returns:
		Array of message dictionaries
	"""
	return messages.get(channel_id, [])


## Members

func set_members(server_id: int, members_list: Array) -> void:
	"""Set members for a server.
	
	Args:
		server_id: Server ID
		members_list: Array of member dictionaries
	"""
	server_members[server_id] = members_list
	members_updated.emit(server_id, members_list)
	print("[DataManager] Members loaded for server %d: %d members" % [server_id, members_list.size()])


func get_members(server_id: int) -> Array:
	"""Get members for a server.
	
	Args:
		server_id: Server ID
		
	Returns:
		Array of member dictionaries
	"""
	return server_members.get(server_id, [])


func clear_all() -> void:
	"""Clear all cached data."""
	servers.clear()
	channels.clear()
	messages.clear()
	server_members.clear()
	current_server_id = -1
	current_channel_id = -1
	current_server = {}
	current_channel = {}
	print("[DataManager] All data cleared")
