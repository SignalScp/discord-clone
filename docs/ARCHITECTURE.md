# Architecture Documentation

## System Overview

Discord Clone is a full-stack application consisting of:

1. **Backend** - FastAPI REST API with WebSocket support
2. **Frontend** - Godot 4.x desktop application
3. **Database** - SQLite (development) / PostgreSQL (production)

## Architecture Diagram

```
┌───────────────────────────────┐
│   Godot Frontend (Client)     │
│                                │
│  ┌────────────────────────┐  │
│  │  NetworkManager       │  │
│  │  - HTTP Client        │  │
│  │  - WebSocket Client   │  │
│  └────────────────────────┘  │
│  ┌────────────────────────┐  │
│  │  AuthManager          │  │
│  │  - Token Storage      │  │
│  │  - User State         │  │
│  └────────────────────────┘  │
│  ┌────────────────────────┐  │
│  │  DataManager          │  │
│  │  - Local Cache        │  │
│  │  - State Management   │  │
│  └────────────────────────┘  │
└───────────────────────────────┘
           │ HTTP/WebSocket
           │
┌──────────┴────────────────────┐
│   FastAPI Backend (Server)    │
│                                │
│  ┌────────────────────────┐  │
│  │  REST API Routes      │  │
│  │  - Auth               │  │
│  │  - Users              │  │
│  │  - Servers            │  │
│  │  - Channels           │  │
│  │  - Messages           │  │
│  └────────────────────────┘  │
│  ┌────────────────────────┐  │
│  │  WebSocket Manager    │  │
│  │  - Connections        │  │
│  │  - Broadcasting       │  │
│  └────────────────────────┘  │
│  ┌────────────────────────┐  │
│  │  SQLAlchemy ORM       │  │
│  └────────────────────────┘  │
└────────────────┬───────────────┘
                │
         ┌──────┴──────┐
         │   Database   │
         │  (SQLite)   │
         └─────────────┘
```

## Backend Architecture

### Layer Structure

1. **API Layer** (`routes/`)
   - Handles HTTP requests
   - Input validation via Pydantic
   - JWT authentication
   - Response formatting

2. **Business Logic Layer** (`models.py`, `schemas.py`)
   - Data models (SQLAlchemy)
   - Validation schemas (Pydantic)
   - Business rules

3. **Data Access Layer** (`database.py`)
   - Database connection
   - Session management
   - Transaction handling

4. **WebSocket Layer** (`websocket/`)
   - Real-time communication
   - Connection management
   - Message broadcasting

5. **Utility Layer** (`utils/`)
   - Security (JWT, hashing)
   - Helper functions
   - Shared utilities

### Database Schema

```sql
User
- id: INTEGER PRIMARY KEY
- username: STRING UNIQUE
- email: STRING UNIQUE
- password_hash: STRING
- status: ENUM (online/offline/away/dnd)
- created_at: DATETIME
- updated_at: DATETIME

Server
- id: INTEGER PRIMARY KEY
- name: STRING
- description: TEXT
- owner_id: INTEGER FK -> User
- created_at: DATETIME

ServerMember
- id: INTEGER PRIMARY KEY
- server_id: INTEGER FK -> Server
- user_id: INTEGER FK -> User
- role: ENUM (owner/admin/moderator/member)
- joined_at: DATETIME

Channel
- id: INTEGER PRIMARY KEY
- server_id: INTEGER FK -> Server
- name: STRING
- description: TEXT
- created_at: DATETIME

Message
- id: INTEGER PRIMARY KEY
- channel_id: INTEGER FK -> Channel
- user_id: INTEGER FK -> User
- content: TEXT
- is_edited: BOOLEAN
- created_at: DATETIME
- updated_at: DATETIME
```

## Frontend Architecture

### Component Structure

1. **Global Singletons** (Autoloaded)
   - `NetworkManager` - HTTP/WebSocket client
   - `AuthManager` - Authentication state
   - `DataManager` - Data cache and state

2. **Scenes**
   - `LoginScene` - Authentication UI
   - `MainScene` - Main application window
   - `ServerList` - Server sidebar
   - `ChannelList` - Channel list
   - `ChatUI` - Chat interface
   - `UserList` - Member list

### Data Flow

```
User Action
    ↓
UI Scene
    ↓
NetworkManager (HTTP Request)
    ↓
Backend API
    ↓
Response
    ↓
DataManager (Cache Update)
    ↓
Signal Emission
    ↓
UI Update
```

### Real-time Messaging Flow

```
User types message
    ↓
ChatUI sends HTTP POST
    ↓
Backend saves to database
    ↓
Backend broadcasts via WebSocket
    ↓
NetworkManager receives
    ↓
DataManager adds to cache
    ↓
ChatUI displays message
```

## Security

### Authentication Flow

1. User submits credentials
2. Backend validates password (bcrypt)
3. Backend generates JWT token
4. Token sent to client
5. Client includes token in all requests
6. Backend validates token on each request

### JWT Token Structure

```json
{
  "sub": 123,  // user_id
  "username": "john_doe",
  "exp": 1234567890  // expiration timestamp
}
```

### Security Measures

- Password hashing with bcrypt
- JWT token authentication
- CORS configuration
- Input validation (Pydantic)
- SQL injection prevention (SQLAlchemy ORM)
- XSS prevention (output encoding)

## Performance Optimizations

1. **Caching**
   - Frontend caches servers, channels, messages
   - Reduces API calls

2. **Pagination**
   - Message history limited to 50 per request
   - Lazy loading on scroll

3. **WebSocket**
   - Real-time updates without polling
   - Reduced server load

4. **Database Indexing**
   - Indexes on foreign keys
   - Username and email indexes

## Scalability Considerations

### Current Limitations

- Single server instance
- SQLite database (file-based)
- In-memory WebSocket connections

### Future Improvements

1. **Database**
   - Migrate to PostgreSQL
   - Connection pooling
   - Read replicas

2. **WebSocket**
   - Redis for pub/sub
   - Horizontal scaling
   - Load balancing

3. **Caching**
   - Redis for session storage
   - CDN for static assets

4. **Monitoring**
   - Prometheus metrics
   - Grafana dashboards
   - Error tracking (Sentry)

## Deployment

### Development

```bash
# Backend
cd backend
python -m uvicorn app.main:app --reload

# Frontend
# Open in Godot and press F5
```

### Production

```bash
# Backend with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend
# Export as executable from Godot
```

## Testing Strategy

1. **Unit Tests**
   - Test individual functions
   - Mock dependencies

2. **Integration Tests**
   - Test API endpoints
   - Test database operations

3. **End-to-End Tests**
   - Test complete user flows
   - Automated UI testing

## Error Handling

### Backend

- HTTP status codes (400, 401, 403, 404, 500)
- Detailed error messages
- Logging with timestamps

### Frontend

- Connection error handling
- Auto-reconnect logic
- User-friendly error messages
- Graceful degradation
