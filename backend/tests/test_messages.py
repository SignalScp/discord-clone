"""Tests for message endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_messages.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def get_auth_token():
    """Helper to get authentication token."""
    # Register and login
    client.post(
        "/auth/register",
        json={
            "username": "msgtest",
            "email": "msgtest@example.com",
            "password": "testpass123"
        }
    )
    
    response = client.post(
        "/auth/login",
        data={
            "username": "msgtest",
            "password": "testpass123"
        }
    )
    
    return response.json()["access_token"]


def test_send_message():
    """Test sending a message."""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create server and channel first
    server_response = client.post(
        "/servers",
        json={"name": "Test Server", "description": "Test"},
        headers=headers
    )
    server_id = server_response.json()["id"]
    
    # Get default general channel
    channels_response = client.get(f"/servers/{server_id}/channels", headers=headers)
    channel_id = channels_response.json()[0]["id"]
    
    # Send message
    response = client.post(
        f"/messages/channels/{channel_id}/messages",
        json={"content": "Hello, world!"},
        headers=headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "Hello, world!"
    assert "id" in data


def test_get_messages():
    """Test retrieving message history."""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create server
    server_response = client.post(
        "/servers",
        json={"name": "Test Server 2", "description": "Test"},
        headers=headers
    )
    server_id = server_response.json()["id"]
    
    # Get channel
    channels_response = client.get(f"/servers/{server_id}/channels", headers=headers)
    channel_id = channels_response.json()[0]["id"]
    
    # Send multiple messages
    for i in range(5):
        client.post(
            f"/messages/channels/{channel_id}/messages",
            json={"content": f"Message {i}"},
            headers=headers
        )
    
    # Get messages
    response = client.get(
        f"/messages/channels/{channel_id}/messages?limit=10",
        headers=headers
    )
    
    assert response.status_code == 200
    messages = response.json()
    assert len(messages) == 5
