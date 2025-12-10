# Complete Setup Guide

Step-by-step guide to get Discord Clone running on your machine.

## Prerequisites

### Required Software

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Godot 4.2+** - [Download](https://godotengine.org/download)
- **Git** - [Download](https://git-scm.com/downloads)

### Verify Installation

```bash
python --version  # Should show 3.10 or higher
git --version
```

## Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/SignalScp/discord-clone.git
cd discord-clone
```

### Step 2: Backend Setup

#### On Windows

```bash
cd backend
run.bat
```

The script will:
1. Create virtual environment
2. Install dependencies
3. Create .env file from example
4. Start the server

#### On Linux/Mac

```bash
cd backend
chmod +x run.sh
./run.sh
```

#### Manual Setup (Alternative)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Generate secure secret key
python -c "import secrets; print(secrets.token_hex(32))"
# Copy output and paste into .env as SECRET_KEY

# Start server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Verify Backend is Running

Open browser and visit:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

You should see the interactive API documentation.

### Step 3: Frontend Setup

1. **Download Godot**
   - Visit https://godotengine.org/download
   - Download Godot 4.2 or newer
   - Extract and run

2. **Import Project**
   - Open Godot
   - Click "Import"
   - Navigate to `discord-clone/frontend/`
   - Select `project.godot`
   - Click "Import & Edit"

3. **Configure Backend URL**
   - In Godot, open `scripts/global/NetworkManager.gd`
   - Verify URLs:
     ```gdscript
     const API_BASE_URL = "http://localhost:8000"
     const WS_BASE_URL = "ws://localhost:8000"
     ```

4. **Run Frontend**
   - Press **F5** or click the Play button
   - Login screen should appear

## First Time Usage

### 1. Create Account

1. Click "Register" tab
2. Enter:
   - Username (min 3 characters)
   - Email address
   - Password (min 6 characters)
   - Confirm password
3. Click "Create Account"
4. You'll be automatically logged in

### 2. Create Your First Server

1. Click the **+** button in the left sidebar (server list)
2. Enter server name (e.g., "My Server")
3. Optionally add description
4. Click "Create"
5. A default "general" channel will be created

### 3. Start Chatting

1. Select your server from the left sidebar
2. Select "general" channel
3. Type a message in the input field
4. Press Enter or click "Send"

### 4. Invite Friends (Multi-User Testing)

1. Open another Godot instance or export as executable
2. Register a different account
3. Both users need to join the same server (manual for now)
4. Select the same channel
5. Messages will appear in real-time!

## Configuration

### Backend Configuration (.env)

```env
# Security - CHANGE THIS IN PRODUCTION!
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Database
DATABASE_URL=sqlite:///./discord_clone.db

# Server
HOST=0.0.0.0
PORT=8000

# CORS
ALLOWED_ORIGINS=http://localhost:*,http://127.0.0.1:*

# Environment
ENVIRONMENT=development
```

### Using PostgreSQL (Production)

1. Install PostgreSQL
2. Create database:
   ```sql
   CREATE DATABASE discord_clone;
   ```
3. Update `.env`:
   ```env
   DATABASE_URL=postgresql://username:password@localhost/discord_clone
   ```
4. Install additional dependency:
   ```bash
   pip install psycopg2-binary
   ```

## Testing

### Backend Tests

```bash
cd backend
pytest

# With coverage
pytest --cov=app tests/

# Verbose output
pytest -v
```

### Manual Testing

1. **Test Registration**
   - Try valid registration
   - Try duplicate username
   - Try invalid email

2. **Test Login**
   - Try correct credentials
   - Try wrong password
   - Try non-existent user

3. **Test Messaging**
   - Send messages
   - Open two clients
   - Verify real-time delivery

4. **Test WebSocket**
   - Disconnect network
   - Verify reconnection
   - Check error messages

## Troubleshooting

### Backend Issues

#### "Port 8000 already in use"

**Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

**Linux/Mac:**
```bash
lsof -i :8000
kill -9 <PID>
```

#### "Module not found"

```bash
# Ensure virtual environment is activated
pip install -r requirements.txt
```

#### "Database is locked"

```bash
# Stop all running instances
# Delete database
rm discord_clone.db
# Restart server (database will be recreated)
```

### Frontend Issues

#### "Cannot connect to backend"

1. Verify backend is running: http://localhost:8000
2. Check `NetworkManager.gd` configuration
3. Check firewall settings
4. Try http://127.0.0.1:8000 instead

#### "WebSocket connection failed"

1. Check browser console (if web export)
2. Verify JWT token is valid
3. Check backend logs
4. Ensure WebSocket endpoint is accessible

#### "Godot won't import project"

1. Ensure Godot 4.2+
2. Delete `.godot` folder and re-import
3. Check file permissions

### Common Errors

#### "401 Unauthorized"
- Token expired (login again)
- Invalid token
- Missing Authorization header

#### "403 Forbidden"
- Not a member of server/channel
- Insufficient permissions

#### "404 Not Found"
- Server/channel/message doesn't exist
- Incorrect ID

## Development

### Running in Development Mode

**Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
- Just press F5 in Godot editor

### Hot Reload

- **Backend**: Automatically reloads on file changes (with `--reload` flag)
- **Frontend**: Press F5 in Godot to reload

### Debugging

**Backend:**
```python
import pdb; pdb.set_trace()  # Add breakpoint
```

**Frontend:**
- Use Godot's built-in debugger (F6)
- Check Output panel for `print()` statements
- Use `push_warning()` and `push_error()` for debugging

### Code Style

**Backend (Python):**
- Follow PEP 8
- Use type hints
- Document all functions
- Max line length: 100

**Frontend (GDScript):**
- Follow Godot style guide
- Use type hints
- Document public functions
- Use tabs for indentation

## Production Deployment

### Backend Deployment

1. **Update .env for production:**
   ```env
   ENVIRONMENT=production
   SECRET_KEY=<very-long-random-string>
   DATABASE_URL=postgresql://...
   ALLOWED_ORIGINS=https://yourdomain.com
   ```

2. **Use production server:**
   ```bash
   pip install gunicorn
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

3. **Set up reverse proxy (Nginx):**
   ```nginx
   server {
       listen 80;
       server_name api.yourdomain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /ws/ {
           proxy_pass http://localhost:8000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
       }
   }
   ```

### Frontend Export

1. **Configure export preset:**
   - Project → Export
   - Add preset for your platform
   - Configure settings

2. **Export:**
   - Click "Export Project"
   - Choose location
   - Click "Save"

3. **Distribute:**
   - Share executable with users
   - No installation required

## Next Steps

### Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://www.sqlalchemy.org/
- **Godot**: https://docs.godotengine.org/
- **WebSockets**: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API

### Feature Ideas

- Direct messages
- File uploads
- Voice channels
- User avatars
- Server invites
- Roles and permissions
- Message reactions
- Message editing/deletion
- User presence (typing indicator)
- Server settings

## Support

For issues and questions:
- Check existing documentation
- Review API docs: http://localhost:8000/docs
- Open issue on GitHub

## License

MIT License - See LICENSE file for details
