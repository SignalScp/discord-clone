# Discord Clone

<div align="center">

![Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Godot](https://img.shields.io/badge/godot-4.2+-blue.svg)

A full-featured Discord clone with real-time messaging, built with **FastAPI** and **Godot**.

[Features](#features) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Screenshots](#screenshots) • [Contributing](#contributing)

</div>

---

## 🚀 Features

### ✅ Implemented

- **🔐 Complete Authentication System**
  - User registration with validation
  - JWT-based login
  - Secure password hashing (bcrypt)
  - Token-based session management

- **💬 Real-time Messaging**
  - WebSocket-based instant delivery
  - Message history with pagination (50 per page)
  - Message editing and deletion
  - Auto-reconnect on connection loss

- **🖥️ Server Management**
  - Create and manage multiple servers
  - Server roles (Owner, Admin, Moderator, Member)
  - Automatic "general" channel creation
  - Server member management

- **📺 Channel System**
  - Multiple text channels per server
  - Channel creation and management
  - Permission-based access control

- **👥 User Presence**
  - Real-time online/offline status
  - User list with status indicators
  - Member count display

- **🎨 Modern UI**
  - Clean, responsive interface
  - Discord-inspired design
  - Dark theme
  - Smooth animations

### 🚧 Potential Extensions

- Direct messages between users
- File and image uploads
- Voice channels
- User avatars and profiles
- Server invites with invite codes
- Advanced permissions system
- Message reactions and emojis
- Typing indicators
- Message search
- User mentions and notifications

---

## 💻 Tech Stack

### Backend

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - SQL toolkit and ORM
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation
- **[python-socketio](https://python-socketio.readthedocs.io/)** - WebSocket support
- **[PyJWT](https://pyjwt.readthedocs.io/)** - JWT authentication
- **[Passlib](https://passlib.readthedocs.io/)** - Password hashing
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI server

### Frontend

- **[Godot 4.2](https://godotengine.org/)** - Open-source game engine
- **GDScript** - Godot's scripting language
- **WebSocket** - Real-time communication
- **HTTPRequest** - REST API integration

### Database

- **SQLite** (Development)
- **PostgreSQL** (Production-ready)

---

## 📁 Project Structure

```
discord-clone/
├── backend/              # FastAPI backend server
│   ├── app/
│   │   ├── routes/       # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── servers.py
│   │   │   ├── channels.py
│   │   │   └── messages.py
│   │   ├── websocket/   # WebSocket manager
│   │   ├── utils/       # Security, helpers
│   │   ├── main.py      # Application entry
│   │   ├── models.py    # Database models
│   │   └── schemas.py   # Pydantic schemas
│   ├── tests/           # Unit & integration tests
│   ├── run.bat          # Windows launcher
│   ├── run.sh           # Linux/Mac launcher
│   └── requirements.txt # Python dependencies
│
├── frontend/            # Godot frontend
│   ├── scenes/          # UI scenes
│   │   ├── login/
│   │   └── main/
│   ├── scripts/         # GDScript files
│   │   ├── global/      # Singletons (NetworkManager, etc.)
│   │   └── scenes/      # Scene scripts
│   └── project.godot   # Godot project config
│
├── docs/                # Documentation
│   ├── API.md           # API reference
│   ├── ARCHITECTURE.md  # System architecture
│   └── SETUP.md         # Setup guide
│
├── README.md            # This file
├── LICENSE              # MIT License
└── CONTRIBUTING.md      # Contribution guidelines
```

---

## ⚡ Quick Start

### Prerequisites

- Python 3.10+
- Godot 4.2+
- Git

### 1. Clone Repository

```bash
git clone https://github.com/SignalScp/discord-clone.git
cd discord-clone
```

### 2. Start Backend

**Windows:**
```bash
cd backend
run.bat
```

**Linux/Mac:**
```bash
cd backend
chmod +x run.sh
./run.sh
```

Backend will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### 3. Start Frontend

1. Open Godot 4.2+
2. Click "Import"
3. Select `frontend/project.godot`
4. Click "Import & Edit"
5. Press **F5** to run

### 4. Create Account & Start Chatting!

1. Click "Register" and create an account
2. Click "+" to create a server
3. Start messaging in the "general" channel

🎉 **That's it! You're ready to go!**

For detailed setup instructions, see [docs/SETUP.md](docs/SETUP.md).

---

## 📚 Documentation

- **[Complete Setup Guide](docs/SETUP.md)** - Detailed installation and configuration
- **[API Reference](docs/API.md)** - Complete API documentation with examples
- **[Architecture](docs/ARCHITECTURE.md)** - System design and architecture
- **[Contributing](CONTRIBUTING.md)** - How to contribute to this project

### Quick Links

- **Backend README**: [backend/README.md](backend/README.md)
- **Frontend README**: [frontend/README.md](frontend/README.md)
- **API Docs** (when running): http://localhost:8000/docs

---

## 📸 Screenshots

### Login Screen
![Login Screen](https://via.placeholder.com/800x500/2c2f33/ffffff?text=Login+Screen)

*Clean authentication interface with login and registration tabs*

### Main Interface
![Main Interface](https://via.placeholder.com/800x500/2c2f33/ffffff?text=Main+Interface)

*Discord-inspired layout with server list, channels, chat, and member list*

### Real-time Messaging
![Chat](https://via.placeholder.com/800x500/2c2f33/ffffff?text=Real-time+Chat)

*Instant message delivery via WebSocket*

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest                      # Run all tests
pytest -v                   # Verbose output
pytest --cov=app tests/     # With coverage
```

### Manual Testing

1. **Single User Testing**
   - Register and login
   - Create server and channels
   - Send messages

2. **Multi-User Testing**
   - Open two Godot instances
   - Register different accounts
   - Join same server
   - Test real-time messaging

---

## 🔧 Configuration

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

---

## 🚀 Deployment

### Backend (Production)

```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend (Export)

1. Project → Export
2. Add export preset for your platform
3. Export as executable

See [docs/SETUP.md](docs/SETUP.md) for detailed deployment instructions.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development setup and coding standards.

---

## 🐛 Known Issues

- Server invites not yet implemented (users must manually join same server)
- No file upload support yet
- Message pagination only loads newest 50 messages
- WebSocket reconnection may fail after multiple attempts

---

## 🗣️ Roadmap

- [ ] Direct messages
- [ ] File/image uploads
- [ ] User avatars
- [ ] Server invite system
- [ ] Voice channels
- [ ] Advanced permissions
- [ ] Message reactions
- [ ] Typing indicators
- [ ] User profiles
- [ ] Message search
- [ ] Mobile app (Godot export)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by [Discord](https://discord.com/)
- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Godot Engine](https://godotengine.org/)
- Created as a full-stack learning project

---

## 📞 Support

For questions, issues, or feature requests:

- 🐛 [Open an Issue](https://github.com/SignalScp/discord-clone/issues)
- 📚 [Read the Docs](docs/)
- 💬 [Discussions](https://github.com/SignalScp/discord-clone/discussions)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

<div align="center">

**Made with ❤️ by SignalScp**

[View on GitHub](https://github.com/SignalScp/discord-clone)

</div>
