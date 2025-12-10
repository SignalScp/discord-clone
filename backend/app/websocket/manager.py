"""WebSocket connection manager for real-time messaging."""

from fastapi import WebSocket
from typing import Dict, List, Set
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for real-time messaging."""
    
    def __init__(self):
        """Initialize connection manager."""
        # Store active connections: {channel_id: {user_id: websocket}}
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}
        # Track user presence: {user_id: set of channel_ids}
        self.user_channels: Dict[int, Set[int]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int, server_id: int, channel_id: int):
        """Accept and register a new WebSocket connection.
        
        Args:
            websocket: WebSocket connection
            user_id: User ID
            server_id: Server ID
            channel_id: Channel ID
        """
        await websocket.accept()
        
        # Initialize channel connections if not exists
        if channel_id not in self.active_connections:
            self.active_connections[channel_id] = {}
        
        # Add connection
        self.active_connections[channel_id][user_id] = websocket
        
        # Track user channels
        if user_id not in self.user_channels:
            self.user_channels[user_id] = set()
        self.user_channels[user_id].add(channel_id)
        
        logger.info(f"User {user_id} connected to channel {channel_id}")
        logger.info(f"Active connections in channel {channel_id}: {len(self.active_connections[channel_id])}")
    
    def disconnect(self, websocket: WebSocket, user_id: int, server_id: int, channel_id: int):
        """Remove a WebSocket connection.
        
        Args:
            websocket: WebSocket connection
            user_id: User ID
            server_id: Server ID
            channel_id: Channel ID
        """
        # Remove from active connections
        if channel_id in self.active_connections:
            if user_id in self.active_connections[channel_id]:
                del self.active_connections[channel_id][user_id]
            
            # Clean up empty channel
            if not self.active_connections[channel_id]:
                del self.active_connections[channel_id]
        
        # Remove from user channels tracking
        if user_id in self.user_channels:
            self.user_channels[user_id].discard(channel_id)
            
            # Clean up empty user tracking
            if not self.user_channels[user_id]:
                del self.user_channels[user_id]
        
        logger.info(f"User {user_id} disconnected from channel {channel_id}")
    
    async def send_personal_message(self, message: dict, user_id: int, channel_id: int):
        """Send a message to a specific user in a channel.
        
        Args:
            message: Message data to send
            user_id: Target user ID
            channel_id: Channel ID
        """
        if channel_id in self.active_connections:
            if user_id in self.active_connections[channel_id]:
                websocket = self.active_connections[channel_id][user_id]
                try:
                    await websocket.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending message to user {user_id}: {e}")
    
    async def broadcast(self, message: dict, channel_id: int, exclude_user: int = None):
        """Broadcast a message to all users in a channel.
        
        Args:
            message: Message data to broadcast
            channel_id: Channel ID
            exclude_user: Optional user ID to exclude from broadcast
        """
        if channel_id not in self.active_connections:
            return
        
        disconnected_users = []
        
        for user_id, websocket in self.active_connections[channel_id].items():
            # Skip excluded user
            if exclude_user and user_id == exclude_user:
                continue
            
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to user {user_id}: {e}")
                disconnected_users.append(user_id)
        
        # Clean up disconnected users
        for user_id in disconnected_users:
            if user_id in self.active_connections[channel_id]:
                del self.active_connections[channel_id][user_id]
    
    def get_channel_users(self, channel_id: int) -> List[int]:
        """Get list of users currently connected to a channel.
        
        Args:
            channel_id: Channel ID
            
        Returns:
            List of user IDs
        """
        if channel_id in self.active_connections:
            return list(self.active_connections[channel_id].keys())
        return []
    
    def is_user_online(self, user_id: int) -> bool:
        """Check if a user is online (connected to any channel).
        
        Args:
            user_id: User ID
            
        Returns:
            True if user is online, False otherwise
        """
        return user_id in self.user_channels and len(self.user_channels[user_id]) > 0
    
    def get_user_channels(self, user_id: int) -> Set[int]:
        """Get all channels a user is currently connected to.
        
        Args:
            user_id: User ID
            
        Returns:
            Set of channel IDs
        """
        return self.user_channels.get(user_id, set())
