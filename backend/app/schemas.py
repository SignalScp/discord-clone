"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from .models import UserStatus, MemberRole


# ============ User Schemas ============

class UserBase(BaseModel):
    """Base user schema."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=6, max_length=100)


class UserUpdate(BaseModel):
    """Schema for user updates."""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    status: Optional[UserStatus] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    status: UserStatus
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserResponse):
    """Schema for user in database (includes password hash)."""
    password_hash: str


# ============ Authentication Schemas ============

class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data contained in JWT token."""
    user_id: Optional[int] = None
    username: Optional[str] = None


# ============ Server Schemas ============

class ServerBase(BaseModel):
    """Base server schema."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class ServerCreate(ServerBase):
    """Schema for server creation."""
    pass


class ServerUpdate(BaseModel):
    """Schema for server updates."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class ServerResponse(ServerBase):
    """Schema for server response."""
    id: int
    owner_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============ Server Member Schemas ============

class ServerMemberResponse(BaseModel):
    """Schema for server member response."""
    id: int
    server_id: int
    user_id: int
    role: MemberRole
    joined_at: datetime
    user: UserResponse
    
    model_config = ConfigDict(from_attributes=True)


# ============ Channel Schemas ============

class ChannelBase(BaseModel):
    """Base channel schema."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class ChannelCreate(ChannelBase):
    """Schema for channel creation."""
    pass


class ChannelUpdate(BaseModel):
    """Schema for channel updates."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class ChannelResponse(ChannelBase):
    """Schema for channel response."""
    id: int
    server_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============ Message Schemas ============

class MessageBase(BaseModel):
    """Base message schema."""
    content: str = Field(..., min_length=1, max_length=2000)


class MessageCreate(MessageBase):
    """Schema for message creation."""
    pass


class MessageUpdate(BaseModel):
    """Schema for message updates."""
    content: str = Field(..., min_length=1, max_length=2000)


class MessageResponse(MessageBase):
    """Schema for message response."""
    id: int
    channel_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    is_edited: bool
    user: UserResponse
    
    model_config = ConfigDict(from_attributes=True)


# ============ WebSocket Schemas ============

class WebSocketMessage(BaseModel):
    """Schema for WebSocket messages."""
    type: str  # 'message', 'user_join', 'user_leave', 'typing'
    data: dict
