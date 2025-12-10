# Complete Setup Guide

Step-by-step instructions to get Discord Clone running on your machine.

## System Requirements

### Minimum Requirements
- OS: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- RAM: 4GB
- Disk Space: 500MB
- Python: 3.10 or higher
- Godot: 4.2 or higher

### Recommended
- RAM: 8GB+
- Python 3.11+
- Godot 4.2+

## Prerequisites Installation

### Python Installation

**Windows:**
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer
3. Check "Add Python to PATH"
4. Verify: `python --version`

**macOS:**
```bash
brew install python@3.11
```

**Linux:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

### Godot Installation

1. Download Godot 4.2+ from [godotengine.org](https://godotengine.org/download)
2. Extract the archive
3. Run the Godot executable
4. (Optional) Add to PATH for command-line access

## Backend Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/SignalScp/discord-clone.git
cd discord-clone
```

### Step 2: Backend Installation

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` file:

```env
# IMPORTANT: Change this in production!
SECRET_KEY=your-super-secret-key-here-change-this

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Database (SQLite for development)
DATABASE_URL=sqlite:///./discord_clone.db

# Server
HOST=0.0.0.0
PORT=8000

# CORS (allow all for development)
ALLOWED_ORIGINS=http://localhost:*,http://127.0.0.1:*

ENVIRONMENT=development
```

**Generate Secure Secret Key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 4: Run Backend

**Windows:**
```bash
run.bat
```

**macOS/Linux:**
```bash
chmod +x run.sh
./run.sh
```

**Or manually:**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 5: Verify Backend

Open browser:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

You should see the interactive API documentation.

## Frontend Setup

### Step 1: Open Project in Godot

1. Launch Godot
2. Click "Import"
3. Click "Browse"
4. Navigate to `discord-clone/frontend/`
5. Select `project.godot`
6. Click "Import & Edit"

### Step 2: Configure Backend URL

If your backend is not on `localhost:8000`, edit:

`frontend/scripts/global/NetworkManager.gd`

```gdscript
const API_BASE_URL = "http://localhost:8000"
const WS_BASE_URL = "ws://localhost:8000"
```

### Step 3: Run Frontend

In Godot editor:
- Press **F5** (Run Project)
- Or click the Play button (▶️) in top-right corner

The login screen should appear.

## First Time Usage

### 1. Register an Account

1. Click "Register" tab
2. Enter:
   - Username (min 3 characters)
   - Email (valid email format)
   - Password (min 6 characters)
   - Confirm Password
3. Click "Create Account"
4. You'll be automatically logged in

### 2. Create Your First Server

1. Click the "+" button in the server list (left sidebar)
2. Enter server name (e.g., "My First Server")
3. Enter description (optional)
4. Click "Create"
5. A default "general" channel is created automatically

### 3. Start Chatting

1. The "general" channel is selected automatically
2. Type a message in the input field at the bottom
3. Press **Enter** or click "Send"
4. Your message appears in the chat!

### 4. Invite Friends

Currently, you need to:
1. Have friend register an account
2. Share your server ID (visible in URL/API)
3. Use API to add members (feature coming soon in UI)

## Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
pytest tests/
```

### Manual Testing

1. Open multiple frontend instances
2. Register different users
3. Add them to the same server
4. Send messages between users
5. Verify real-time updates

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

**Database errors:**
```bash
# Delete and recreate database
rm discord_clone.db
# Restart backend - tables will be recreated
```

**Import errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend Issues

**Can't connect to backend:**
1. Verify backend is running: http://localhost:8000/health
2. Check `NetworkManager.gd` URLs
3. Check firewall settings
4. Try 127.0.0.1 instead of localhost

**WebSocket connection failed:**
1. Check backend logs for errors
2. Verify JWT token is valid (try re-login)
3. Check WebSocket URL in NetworkManager
4. Ensure backend WebSocket endpoint is accessible

**Godot import errors:**
1. Ensure Godot 4.2+ is installed
2. Delete `.godot/` folder and re-import
3. Check all script paths are correct

**Scenes not loading:**
1. Verify all .tscn files exist
2. Check script references in scenes
3. Re-import project in Godot

### Common Errors

**401 Unauthorized:**
- Token expired - log in again
- Invalid credentials

**403 Forbidden:**
- User not a member of server
- Insufficient permissions

**404 Not Found:**
- Invalid server/channel ID
- Resource deleted

**500 Internal Server Error:**
- Check backend logs
- Database connection issue
- Bug in backend code

## Production Deployment

### Backend Production

1. **Use PostgreSQL:**

```env
DATABASE_URL=postgresql://user:password@localhost/discord_clone
```

2. **Update Environment:**

```env
ENVIRONMENT=production
SECRET_KEY=<generated-secret-key>
ALLOWED_ORIGINS=https://yourdomain.com
```

3. **Run with Gunicorn:**

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

4. **Setup NGINX:**

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

5. **Setup SSL with Let's Encrypt:**

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.yourdomain.com
```

### Frontend Production

1. **Update NetworkManager URLs:**

```gdscript
const API_BASE_URL = "https://api.yourdomain.com"
const WS_BASE_URL = "wss://api.yourdomain.com"
```

2. **Export Project:**

In Godot:
- Project → Export
- Add export template for your platform
- Configure settings
- Export

3. **Distribute:**
- Windows: .exe file
- macOS: .app bundle  
- Linux: executable binary

## Performance Optimization

### Backend

1. **Enable connection pooling** (PostgreSQL)
2. **Use Redis for caching**
3. **Enable Gzip compression**
4. **Set up CDN for static assets**
5. **Implement rate limiting**

### Frontend

1. **Optimize assets** (compress images)
2. **Lazy load message history**
3. **Implement message pagination**
4. **Cache server/channel data**

## Monitoring

### Backend Logs

```bash
# View logs in real-time
tail -f backend.log

# Search for errors
grep ERROR backend.log
```

### Health Checks

```bash
# Check API health
curl http://localhost:8000/health

# Check database connection
curl http://localhost:8000/health/db
```

## Backup

### Database Backup

**SQLite:**
```bash
cp discord_clone.db discord_clone_backup_$(date +%Y%m%d).db
```

**PostgreSQL:**
```bash
pg_dump discord_clone > backup_$(date +%Y%m%d).sql
```

### Restore

**SQLite:**
```bash
cp discord_clone_backup_20240101.db discord_clone.db
```

**PostgreSQL:**
```bash
psql discord_clone < backup_20240101.sql
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/SignalScp/discord-clone/issues
- Documentation: `/docs` folder
- API Docs: http://localhost:8000/docs

## Next Steps

- [API Documentation](API.md)
- [Architecture Guide](ARCHITECTURE.md)
- [Contributing Guidelines](../README.md)

## Security Checklist

- [ ] Changed SECRET_KEY from default
- [ ] Using HTTPS in production
- [ ] Configured CORS properly
- [ ] Set up firewall rules
- [ ] Using PostgreSQL in production
- [ ] Enabled rate limiting
- [ ] Set up monitoring
- [ ] Regular backups configured
- [ ] SSL certificates configured
- [ ] Strong password policy enforced

## License

MIT License - See LICENSE file for details
