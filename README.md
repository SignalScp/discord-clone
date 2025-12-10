# Discord Clone

A full-featured Discord clone application with real-time messaging capabilities, built with Godot 4.x for the frontend and FastAPI for the backend.

## Features

- 🔐 **Complete Authentication System** - User registration and login with JWT tokens
- 💬 **Real-time Messaging** - WebSocket-based instant message delivery
- 🖥️ **Server Management** - Create and manage multiple servers
- 📺 **Channel System** - Organize conversations with text channels
- 👥 **User Presence** - Real-time online/offline status tracking
- 📜 **Message History** - Paginated message loading (50 messages per page)
- 🎨 **Modern UI** - Clean, responsive interface built with Godot
- 🔄 **Auto-Reconnect** - Automatic WebSocket reconnection on connection loss

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **python-socketio** - WebSocket support
- **PyJWT** - JWT token authentication
- **bcrypt** - Password hashing
- **Uvicorn** - ASGI server

### Frontend
- **Godot 4.x** - Open-source game engine
- **GDScript** - Godot's scripting language
- **WebSocket** - Real-time communication
- **HTTP Client** - RESTful API integration

## Project Structure

```
discord-clone/
├── backend/           # FastAPI backend server
│   ├── app/
│   │   ├── routes/    # API endpoints
│   │   ├── websocket/ # WebSocket manager
│   │   └── utils/     # Helper functions
│   └── tests/         # Backend tests
├── frontend/          # Godot frontend
│   ├── scenes/        # UI scenes
│   ├── scripts/       # GDScript files
│   └── assets/        # Images, fonts, themes
└── docs/              # Documentation
```

## Quick Start

### Prerequisites

- Python 3.10+
- Godot 4.x
- Git

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from example:
```bash
cp .env.example .env
```

5. Run the server:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Open Godot 4.x
2. Click "Import"
3. Navigate to `frontend/project.godot`
4. Click "Import & Edit"
5. Press F5 to run the project

## Configuration

### Backend (.env)

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./discord_clone.db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### Frontend (NetworkManager.gd)

```gdscript
const API_BASE_URL = "http://localhost:8000"
const WS_BASE_URL = "ws://localhost:8000"
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and receive JWT token

### Users
- `GET /users/me` - Get current user info
- `GET /users/{user_id}` - Get user by ID

### Servers
- `POST /servers` - Create new server
- `GET /servers` - Get user's servers
- `GET /servers/{server_id}` - Get server details

### Channels
- `POST /servers/{server_id}/channels` - Create channel
- `GET /servers/{server_id}/channels` - Get server channels

### Messages
- `POST /channels/{channel_id}/messages` - Send message
- `GET /channels/{channel_id}/messages` - Get message history
- `WS /ws/{user_id}/{server_id}/{channel_id}` - WebSocket connection

## Usage

1. **Register an Account**
   - Launch the frontend
   - Click "Register" on the login screen
   - Enter username, email, and password

2. **Create a Server**
   - Click the "+" button in the server list
   - Enter server name and description

3. **Create Channels**
   - Select a server
   - Click "+" in the channel list
   - Enter channel name

4. **Start Chatting**
   - Select a channel
   - Type your message in the input field
   - Press Enter or click Send

## Development

### Running Tests

```bash
cd backend
pytest tests/
```

### Database Migrations

The database is automatically created on first run. To reset:

```bash
rm discord_clone.db
```

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

## API Documentation

See [docs/API.md](docs/API.md) for complete API reference.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Inspired by Discord
- Built with Godot and FastAPI
- Created as a learning project for full-stack development

## Support

For issues and questions, please open an issue on GitHub.

---

**Note**: This is an educational project and not affiliated with Discord Inc.