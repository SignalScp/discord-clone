"""Tests for authentication endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import User

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
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


def test_register_user():
    """Test user registration."""
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_register_duplicate_username():
    """Test registration with duplicate username."""
    # First registration
    client.post(
        "/auth/register",
        json={
            "username": "duplicate",
            "email": "user1@example.com",
            "password": "testpass123"
        }
    )
    
    # Try to register with same username
    response = client.post(
        "/auth/register",
        json={
            "username": "duplicate",
            "email": "user2@example.com",
            "password": "testpass123"
        }
    )
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_login():
    """Test user login."""
    # Register user first
    client.post(
        "/auth/register",
        json={
            "username": "logintest",
            "email": "login@example.com",
            "password": "testpass123"
        }
    )
    
    # Login
    response = client.post(
        "/auth/login",
        data={
            "username": "logintest",
            "password": "testpass123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    response = client.post(
        "/auth/login",
        data={
            "username": "nonexistent",
            "password": "wrongpass"
        }
    )
    
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()
