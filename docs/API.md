# API Documentation

Complete API reference for Discord Clone backend.

## Base URL

```
http://localhost:8000
```

## Authentication

All endpoints except `/auth/register` and `/auth/login` require authentication via JWT Bearer token.

### Headers

```http
Authorization: Bearer <your_jwt_token>
```

---

## Authentication Endpoints

### Register User

Create a new user account.

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "status": "offline",
  "created_at": "2024-01-01T12:00:00"
}
```

**Errors:**
- `400` - Username or email already registered

---

### Login

Login and receive JWT token.

**Endpoint:** `POST /auth/login`

**Request Body:** (application/x-www-form-urlencoded)
```
username=john_doe&password=SecurePass123!
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors:**
- `401` - Invalid credentials

---

## User Endpoints

### Get Current User

Get authenticated user's profile.

**Endpoint:** `GET /users/me`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "status": "online",
  "created_at": "2024-01-01T12:00:00"
}
```

---

### Get User by ID

**Endpoint:** `GET /users/{user_id}`

**Response:** `200 OK`
```json
{
  "id": 2,
  "username": "jane_doe",
  "email": "jane@example.com",
  "status": "online",
  "created_at": "2024-01-01T13:00:00"
}
```

**Errors:**
- `404` - User not found

---

### Update User Profile

**Endpoint:** `PATCH /users/me`

**Request Body:**
```json
{
  "username": "new_username",
  "status": "away"
}
```

**Response:** `200 OK` - Updated user object

---

## Server Endpoints

### Create Server

**Endpoint:** `POST /servers`

**Request Body:**
```json
{
  "name": "My Awesome Server",
  "description": "A place for friends"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "My Awesome Server",
  "description": "A place for friends",
  "owner_id": 1,
  "created_at": "2024-01-01T12:00:00"
}
```

---

### Get User's Servers

**Endpoint:** `GET /servers`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Server 1",
    "description": "First server",
    "owner_id": 1,
    "created_at": "2024-01-01T12:00:00"
  }
]
```

---

### Get Server Details

**Endpoint:** `GET /servers/{server_id}`

**Response:** `200 OK` - Server object

**Errors:**
- `404` - Server not found
- `403` - Not a member of this server

---

### Update Server

**Endpoint:** `PATCH /servers/{server_id}`

**Request Body:**
```json
{
  "name": "Updated Name",
  "description": "Updated description"
}
```

**Response:** `200 OK` - Updated server object

**Errors:**
- `403` - Not authorized (must be owner or admin)

---

### Delete Server

**Endpoint:** `DELETE /servers/{server_id}`

**Response:** `204 No Content`

**Errors:**
- `403` - Only owner can delete

---

### Get Server Members

**Endpoint:** `GET /servers/{server_id}/members`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "server_id": 1,
    "user_id": 1,
    "role": "owner",
    "joined_at": "2024-01-01T12:00:00",
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "status": "online",
      "created_at": "2024-01-01T12:00:00"
    }
  }
]
```

---

## Channel Endpoints

### Create Channel

**Endpoint:** `POST /servers/{server_id}/channels`

**Request Body:**
```json
{
  "name": "random",
  "description": "Random chat"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "server_id": 1,
  "name": "random",
  "description": "Random chat",
  "created_at": "2024-01-01T12:00:00"
}
```

---

### Get Server Channels

**Endpoint:** `GET /servers/{server_id}/channels`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "server_id": 1,
    "name": "general",
    "description": "General chat",
    "created_at": "2024-01-01T12:00:00"
  }
]
```

---

### Get Channel

**Endpoint:** `GET /channels/{channel_id}`

**Response:** `200 OK` - Channel object

---

### Update Channel

**Endpoint:** `PATCH /channels/{channel_id}`

**Request Body:**
```json
{
  "name": "new-name",
  "description": "Updated description"
}
```

**Response:** `200 OK` - Updated channel object

---

### Delete Channel

**Endpoint:** `DELETE /channels/{channel_id}`

**Response:** `204 No Content`

---

## Message Endpoints

### Send Message

**Endpoint:** `POST /messages/channels/{channel_id}/messages`

**Request Body:**
```json
{
  "content": "Hello, everyone!"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "channel_id": 1,
  "user_id": 1,
  "content": "Hello, everyone!",
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:00",
  "is_edited": false,
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "status": "online",
    "created_at": "2024-01-01T12:00:00"
  }
}
```

---

### Get Message History

**Endpoint:** `GET /messages/channels/{channel_id}/messages`

**Query Parameters:**
- `skip` (int, default: 0) - Number of messages to skip
- `limit` (int, default: 50, max: 100) - Max messages to return

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "channel_id": 1,
    "user_id": 1,
    "content": "First message",
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00",
    "is_edited": false,
    "user": {...}
  }
]
```

---

### Update Message

**Endpoint:** `PATCH /messages/messages/{message_id}`

**Request Body:**
```json
{
  "content": "Updated message content"
}
```

**Response:** `200 OK` - Updated message (is_edited: true)

---

### Delete Message

**Endpoint:** `DELETE /messages/messages/{message_id}`

**Response:** `204 No Content`

---

## WebSocket

### Connect to Channel

**Endpoint:** `ws://localhost:8000/ws/{user_id}/{server_id}/{channel_id}?token=<jwt_token>`

**Authentication:** Pass JWT token as query parameter

### Message Format

**Incoming messages:**
```json
{
  "type": "message",
  "data": {
    "id": 1,
    "content": "Hello!",
    "user_id": 1,
    "username": "john_doe",
    "created_at": "2024-01-01T12:00:00"
  }
}
```

**User join:**
```json
{
  "type": "user_join",
  "data": {
    "user_id": 2,
    "channel_id": 1
  }
}
```

**User leave:**
```json
{
  "type": "user_leave",
  "data": {
    "user_id": 2,
    "channel_id": 1
  }
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message description"
}
```

### Common Status Codes

- `200` - Success
- `201` - Created
- `204` - No Content (successful deletion)
- `400` - Bad Request (validation error)
- `401` - Unauthorized (authentication required)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `500` - Internal Server Error
