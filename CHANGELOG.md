# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-10

### Added

#### Backend
- Complete FastAPI backend with REST API
- JWT-based authentication system
- User registration and login
- Server management (CRUD operations)
- Channel management
- Real-time messaging via WebSocket
- Message history with pagination (50 per page)
- SQLAlchemy ORM with SQLite/PostgreSQL support
- Pydantic schema validation
- Password hashing with bcrypt
- CORS configuration
- Comprehensive API documentation
- Unit and integration tests
- Windows (run.bat) and Linux/Mac (run.sh) launchers

#### Frontend
- Godot 4.2 desktop application
- Login and registration UI
- Server list sidebar
- Channel list
- Real-time chat interface
- User list with online status
- WebSocket client with auto-reconnect
- HTTP client for REST API
- Global state management (AuthManager, DataManager, NetworkManager)
- Message caching
- Clean, Discord-inspired UI

#### Documentation
- Complete README with quickstart guide
- API reference (docs/API.md)
- Architecture documentation (docs/ARCHITECTURE.md)
- Setup guide (docs/SETUP.md)
- Contributing guidelines (CONTRIBUTING.md)
- MIT License

#### DevOps
- GitHub Actions workflow for backend tests
- Automated testing setup
- .gitignore for Python and Godot

### Technical Details

**Backend Stack:**
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- Pydantic 2.5.0
- PyJWT 3.3.0
- Uvicorn 0.24.0

**Frontend Stack:**
- Godot 4.2
- GDScript
- WebSocket support
- HTTP client

**Database Schema:**
- User table (authentication)
- Server table (guilds)
- ServerMember table (membership)
- Channel table (text channels)
- Message table (chat messages)

### Security
- Bcrypt password hashing
- JWT token authentication
- Token expiration (24 hours)
- Input validation
- SQL injection prevention

### Performance
- Message pagination (50 per page)
- Local caching on frontend
- WebSocket for real-time updates
- Database indexing

---

## [Unreleased]

### Planned Features
- Direct messages between users
- File and image uploads
- Voice channels
- User avatars
- Server invite system
- Advanced permissions
- Message reactions
- Typing indicators
- User profiles
- Message search
- Mobile app support

### Known Issues
- Server invites not implemented (manual server joining)
- No file upload support
- WebSocket may fail after max reconnect attempts
- Message history limited to 50 messages per load

---

## Version History

- **1.0.0** (2024-12-10) - Initial release
  - Full-featured Discord clone
  - Backend + Frontend complete
  - Production-ready code
  - Comprehensive documentation
