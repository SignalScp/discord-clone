# Discord Clone - Frontend

Godot 4.x frontend for Discord Clone with real-time messaging.

## Requirements

- Godot 4.2 or higher
- Backend server running (see backend/README.md)

## Installation

1. Download and install [Godot 4.x](https://godotengine.org/download)
2. Open Godot
3. Click "Import"
4. Navigate to this directory and select `project.godot`
5. Click "Import & Edit"

## Configuration

### Backend Connection

Edit `scripts/global/NetworkManager.gd` to configure backend URL:

```gdscript
const API_BASE_URL = "http://localhost:8000"
const WS_BASE_URL = "ws://localhost:8000"
```

## Running

1. Ensure backend server is running
2. In Godot editor, press **F5** or click the Play button
3. The login screen will appear

## Project Structure

```
frontend/
├── scenes/
│   ├── login/
│   │   └── LoginScene.tscn       # Login/Register screen
│   └── main/
│       ├── MainScene.tscn        # Main application window
│       ├── ChatUI.tscn           # Chat interface
│       ├── ServerList.tscn       # Server sidebar
│       ├── ChannelList.tscn      # Channel list
│       └── UserList.tscn         # Online users list
├── scripts/
│   ├── global/
│   │   ├── NetworkManager.gd     # HTTP/WebSocket client
│   │   ├── AuthManager.gd        # Authentication state
│   │   └── DataManager.gd        # Data caching
│   ├── scenes/
│   │   ├── LoginScene.gd
│   │   ├── MainScene.gd
│   │   ├── ChatUI.gd
│   │   ├── ServerList.gd
│   │   ├── ChannelList.gd
│   │   └── UserList.gd
│   └── utils/
│       └── APIClient.gd          # API wrapper
└── assets/
    ├── icons/
    ├── fonts/
    └── themes/
```

## Features

- ✅ User authentication (login/register)
- ✅ Server list with navigation
- ✅ Channel browsing
- ✅ Real-time messaging via WebSocket
- ✅ Message history loading
- ✅ Online user list
- ✅ Auto-reconnect on connection loss
- ✅ Message caching

## Usage

### First Time Setup

1. Click "Register" on login screen
2. Enter username, email, and password
3. Click "Create Account"
4. You'll be logged in automatically

### Creating a Server

1. Click the "+" button in server list (left sidebar)
2. Enter server name and optional description
3. A default "general" channel will be created

### Chatting

1. Select a server from the left sidebar
2. Select a channel from the channel list
3. Type your message in the input field at the bottom
4. Press Enter or click Send

### Creating Channels

1. Select a server
2. Click "+" next to "Channels"
3. Enter channel name
4. Start chatting!

## Keyboard Shortcuts

- **Enter** - Send message
- **Esc** - Close dialogs
- **Ctrl+Q** - Quit application

## Troubleshooting

### Can't connect to backend

1. Verify backend is running (`http://localhost:8000/health`)
2. Check `NetworkManager.gd` configuration
3. Ensure no firewall blocking connections

### WebSocket connection fails

1. Check browser console for errors
2. Verify JWT token is valid
3. Ensure backend WebSocket endpoint is accessible

### Messages not appearing

1. Check WebSocket connection status
2. Verify you're in the correct channel
3. Check backend logs for errors

## Development

### Adding New Features

1. Create scene in `scenes/` directory
2. Create corresponding script in `scripts/scenes/`
3. Update `MainScene.tscn` to include new feature
4. Test thoroughly

### Debugging

- Use Godot's built-in debugger (F6)
- Check Output panel for print statements
- Enable debug mode in `NetworkManager.gd`

## Building Executable

1. Go to Project → Export
2. Add export preset for your platform
3. Configure export settings
4. Click "Export Project"

## License

MIT License
