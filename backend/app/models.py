"""SQLAlchemy database models."""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum
from .database import Base


class UserStatus(str, enum.Enum):
    """User online status enumeration."""
    ONLINE = "online"
    OFFLINE = "offline"
    AWAY = "away"
    DND = "dnd"  # Do Not Disturb


class MemberRole(str, enum.Enum):
    """Server member role enumeration."""
    OWNER = "owner"
    ADMIN = "admin"
    MODERATOR = "moderator"
    MEMBER = "member"


class User(Base):
    """User account model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.OFFLINE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    owned_servers = relationship("Server", back_populates="owner", cascade="all, delete-orphan")
    server_memberships = relationship("ServerMember", back_populates="user", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class Server(Base):
    """Server model (like Discord guild)."""
    __tablename__ = "servers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="owned_servers")
    members = relationship("ServerMember", back_populates="server", cascade="all, delete-orphan")
    channels = relationship("Channel", back_populates="server", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Server(id={self.id}, name='{self.name}')>"


class ServerMember(Base):
    """Server membership model."""
    __tablename__ = "server_members"
    
    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(Integer, ForeignKey("servers.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(Enum(MemberRole), default=MemberRole.MEMBER, nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    server = relationship("Server", back_populates="members")
    user = relationship("User", back_populates="server_memberships")
    
    def __repr__(self):
        return f"<ServerMember(server_id={self.server_id}, user_id={self.user_id}, role={self.role})>"


class Channel(Base):
    """Channel model (text channels within servers)."""
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(Integer, ForeignKey("servers.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    server = relationship("Server", back_populates="channels")
    messages = relationship("Message", back_populates="channel", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Channel(id={self.id}, name='{self.name}', server_id={self.server_id})>"


class Message(Base):
    """Message model."""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_edited = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    channel = relationship("Channel", back_populates="messages")
    user = relationship("User", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, user_id={self.user_id}, channel_id={self.channel_id})>"
