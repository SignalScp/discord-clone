# Complete Setup Guide

Step-by-step instructions to get Discord Clone running on your machine.

## Prerequisites

### Required Software

1. **Python 3.10 or higher**
   - Download: https://www.python.org/downloads/
   - Verify: `python --version`

2. **Godot 4.2 or higher**
   - Download: https://godotengine.org/download
   - Extract and run the executable

3. **Git** (optional, for cloning)
   - Download: https://git-scm.com/downloads

---

## Part 1: Backend Setup

### Step 1: Clone or Download Repository

```bash
# Using Git
git clone https://github.com/SignalScp/discord-clone.git
cd discord-clone

# Or download ZIP and extract
```

### Step 2: Navigate to Backend Directory

```bash
cd backend
```

### Step 3: Create Virtual Environment

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**On Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- JWT libraries
- And other dependencies

### Step 5: Configure Environment

**Windows:**
```cmd
copy .env.example .env
```

**Linux/Mac:**
```bash
cp .env.example .env
```

**IMPORTANT:** Open `.env` and change `SECRET_KEY` to a random string:

```env
SECRET_KEY=your-super-secret-random-key-here-change-this
```

Generate a secure key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 6: Start Backend Server

**Using the startup script (recommended):**

**Windows:**
```cmd
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Or manually:**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 7: Verify Backend is Running

Open your browser and visit:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

You should see the API documentation page.

---

## Part 2: Frontend Setup

### Step 1: Open Godot Engine

1. Launch Godot 4.x
2. Click **"Import"** button
3. Click **"Browse"**
4. Navigate to `discord-clone/frontend/`
5. Select `project.godot` file
6. Click **"Import & Edit"**

### Step 2: Configure Backend URL (if needed)

If your backend is not on localhost:8000, edit:

**File:** `scripts/global/NetworkManager.gd`

```gdscript
const API_BASE_URL = "http://localhost:8000"
const WS_BASE_URL = "ws://localhost:8000"
```

Change to your backend URL.

### Step 3: Run the Application

1. Press **F5** or click the **Play** button (▶️) in top-right
2. Login screen should appear

---

## Part 3: First Run

### Create Your First Account

1. Click **"Register"** tab
2. Enter:
   - Username (min 3 characters)
   - Email (valid email format)
   - Password (min 6 characters)
   - Confirm Password (must match)
3. Click **"Create Account"**
4. You'll be automatically logged in

### Create Your First Server

1. Click the **"+"** button in the server list (left sidebar)
2. Enter server name (e.g., "My Server")
3. Optional: Add description
4. Click **"Create"**
5. A default "general" channel is created automatically

### Start Chatting

1. Server should be selected automatically
2. Click on **"# general"** channel
3. Type a message in the input field at bottom
4. Press **Enter** or click **"Send"**
5. Your message appears in the chat!

### Test Real-time Features

**To test real-time messaging:**

1. Open a second instance of the app (export or run in editor again)
2. Register a second user
3. Have the first user invite the second to their server (future feature)
4. Or: Create a server with second user and note the server ID
5. Manually add first user to database (temporary workaround)
6. Both users should see messages in real-time

---

## Troubleshooting

### Backend Issues

#### "Address already in use" Error

**Windows:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -ti:8000 | xargs kill -9
```

#### "Module not found" Error

Make sure virtual environment is activated:
```bash
# Should show (venv) in prompt
pip install -r requirements.txt
```

#### Database Errors

Delete and recreate database:
```bash
rm discord_clone.db
# Restart server (it will recreate the database)
```

### Frontend Issues

#### "Cannot connect to backend"

1. Verify backend is running: http://localhost:8000
2. Check `NetworkManager.gd` has correct URL
3. Check firewall settings
4. Try http://127.0.0.1:8000 instead

#### "Godot version mismatch"

Project requires Godot 4.2+. Update Godot if needed.

#### "Script errors on run"

1. Check all scripts are in correct locations
2. Verify autoload paths in Project Settings
3. Close and reopen Godot

#### WebSocket Connection Failed

1. Check JWT token is valid (re-login)
2. Verify WebSocket URL in NetworkManager
3. Check browser console for errors
4. Ensure backend WebSocket endpoint is running

### General Issues

#### "No servers showing"

1. Create a server first (+ button)
2. Check browser console for API errors
3. Verify authentication token

#### "Messages not appearing"

1. Check WebSocket connection status
2. Verify channel is selected
3. Check backend logs for errors
4. Try refreshing (close and reopen app)

---

## Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Manual Testing Checklist

- [ ] User registration works
- [ ] User login works
- [ ] Server creation works
- [ ] Channel creation works
- [ ] Message sending works
- [ ] Message history loads
- [ ] Real-time updates work
- [ ] User list shows online status
- [ ] Logout works

---

## Production Deployment

### Backend

#### Using Docker (recommended)

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t discord-clone-backend .
docker run -p 8000:8000 discord-clone-backend
```

#### Using Gunicorn

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Environment Variables for Production

```env
SECRET_KEY=<VERY-SECURE-RANDOM-KEY>
DATABASE_URL=postgresql://user:password@localhost/discord_clone
ENVIRONMENT=production
ALLOWED_ORIGINS=https://yourdomain.com
```

### Frontend

1. Open Godot
2. Go to **Project → Export**
3. Add export preset:
   - Windows Desktop
   - Linux/X11
   - macOS
4. Configure export settings
5. Click **Export Project**
6. Distribute the executable

---

## Performance Tuning

### Backend

1. **Use PostgreSQL instead of SQLite**
   ```env
   DATABASE_URL=postgresql://user:pass@localhost/dbname
   ```

2. **Enable connection pooling**
   ```python
   engine = create_engine(
       settings.DATABASE_URL,
       pool_size=20,
       max_overflow=40
   )
   ```

3. **Add Redis for caching**
   ```bash
   pip install redis
   ```

### Frontend

1. **Reduce message history limit**
   ```gdscript
   # Load only 20 messages initially
   var result = await NetworkManager.http_request(
       "GET",
       "/messages/channels/%d/messages?limit=20" % channel_id,
       {},
       AuthManager.get_token()
   )
   ```

2. **Implement message pagination**
   - Load more on scroll up
   - Keep only recent messages in memory

---

## Security Checklist

### For Production

- [ ] Change SECRET_KEY to random value
- [ ] Use HTTPS (not HTTP)
- [ ] Enable CORS only for your domain
- [ ] Use PostgreSQL (not SQLite)
- [ ] Set up rate limiting
- [ ] Enable logging
- [ ] Regular backups
- [ ] Monitor for suspicious activity
- [ ] Keep dependencies updated
- [ ] Use environment variables (not hardcoded)

---

## Getting Help

### Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Godot Docs**: https://docs.godotengine.org/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/

### Common Commands Reference

**Backend:**
```bash
# Start server
python -m uvicorn app.main:app --reload

# Run tests
pytest tests/

# Check code style
black app/
flake8 app/
```

**Database:**
```bash
# Reset database
rm discord_clone.db

# Backup database
cp discord_clone.db discord_clone.db.backup
```

---

## Next Steps

1. **Customize the UI**
   - Edit Godot scenes
   - Add custom themes
   - Create custom icons

2. **Add Features**
   - Direct messages
   - File uploads
   - Voice channels
   - User profiles
   - Server invites

3. **Improve Performance**
   - Add caching
   - Optimize database queries
   - Implement lazy loading

4. **Deploy to Production**
   - Set up cloud hosting
   - Configure domain
   - Enable HTTPS
   - Set up monitoring

---

## Success!

You now have a fully functional Discord clone running locally! 🎉

For questions or issues, check the documentation or open an issue on GitHub.
