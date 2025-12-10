# Discord Clone - Backend

FastAPI backend server with WebSocket support for real-time messaging.

## Installation

### 1. Create Virtual Environment

```bash
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

**Important**: Change `SECRET_KEY` to a secure random string in production!

Generate a secure key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Run Server

```bash
# Development mode (auto-reload)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the run script:
chmod +x run.sh
./run.sh
```

Server will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── dependencies.py      # Shared dependencies
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   ├── users.py         # User routes
│   │   ├── servers.py       # Server routes
│   │   ├── channels.py      # Channel routes
│   │   └── messages.py      # Message routes
│   ├── websocket/
│   │   ├── __init__.py
│   │   └── manager.py       # WebSocket connection manager
│   └── utils/
│       ├── __init__.py
│       ├── security.py      # JWT and password hashing
│       └── helpers.py       # Helper functions
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_messages.py
├── requirements.txt
├── .env.example
└── run.sh
```

## API Endpoints

### Authentication

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=john_doe&password=SecurePass123!
```

Returns:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Users

#### Get Current User
```http
GET /users/me
Authorization: Bearer <token>
```

### Servers

#### Create Server
```http
POST /servers
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "My Server",
  "description": "A cool server"
}
```

#### Get User Servers
```http
GET /servers
Authorization: Bearer <token>
```

### Channels

#### Create Channel
```http
POST /servers/{server_id}/channels
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "general",
  "description": "General chat"
}
```

### Messages

#### Send Message
```http
POST /channels/{channel_id}/messages
Authorization: Bearer <token>
Content-Type: application/json

{
  "content": "Hello, world!"
}
```

#### Get Message History
```http
GET /channels/{channel_id}/messages?skip=0&limit=50
Authorization: Bearer <token>
```

### WebSocket

#### Connect to Channel
```javascript
ws://localhost:8000/ws/{user_id}/{server_id}/{channel_id}?token=<jwt_token>
```

Message format:
```json
{
  "type": "message",
  "data": {
    "id": 1,
    "content": "Hello!",
    "user": {
      "id": 1,
      "username": "john_doe"
    },
    "created_at": "2024-01-01T12:00:00"
  }
}
```

## Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_auth.py
```

### Run with Coverage
```bash
pytest --cov=app tests/
```

## Database

### Schema Overview

- **User**: User accounts with authentication
- **Server**: Discord-like servers
- **ServerMember**: Server membership and roles
- **Channel**: Text channels within servers
- **Message**: Chat messages in channels

### Reset Database

```bash
rm discord_clone.db
# Restart server to recreate
```

## Development

### Code Style

- Follow PEP 8
- Use type hints
- Document all functions with docstrings
- Maximum line length: 100 characters

### Adding New Endpoints

1. Create/update model in `models.py`
2. Create Pydantic schema in `schemas.py`
3. Implement route in appropriate file under `routes/`
4. Register route in `main.py`
5. Add tests in `tests/`

## Production Deployment

### Security Checklist

- [ ] Change SECRET_KEY to random value
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Set proper CORS origins
- [ ] Use environment-specific .env file
- [ ] Enable rate limiting
- [ ] Set up logging
- [ ] Configure firewall rules

### Example with PostgreSQL

```env
DATABASE_URL=postgresql://user:password@localhost/discord_clone
```

### Running with Gunicorn

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
# Kill process
kill -9 <PID>
```

### Database Locked
```bash
# Stop all running instances
# Delete database file
rm discord_clone.db
# Restart server
```

### WebSocket Connection Failed
- Check firewall settings
- Verify CORS configuration
- Ensure valid JWT token
- Check server logs for errors

## License

MIT License