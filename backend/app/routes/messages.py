"""Message routes for sending and retrieving messages."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
import logging

from ..database import get_db
from ..models import User, Message, Channel, ServerMember
from ..schemas import MessageCreate, MessageResponse, MessageUpdate
from ..dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/channels/{channel_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    channel_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send a message to a channel.
    
    Args:
        channel_id: Channel ID
        message_data: Message content
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created message
        
    Raises:
        HTTPException: If channel not found or user not authorized
    """
    # Check if channel exists
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    # Check if user is a member of the server
    membership = db.query(ServerMember).filter(
        ServerMember.server_id == channel.server_id,
        ServerMember.user_id == current_user.id
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this channel"
        )
    
    # Create message
    new_message = Message(
        channel_id=channel_id,
        user_id=current_user.id,
        content=message_data.content,
        is_edited=False
    )
    
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    logger.info(f"Message sent by {current_user.username} in channel {channel_id}")
    
    return new_message


@router.get("/channels/{channel_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    channel_id: int,
    skip: int = Query(0, ge=0, description="Number of messages to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of messages to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get message history for a channel.
    
    Args:
        channel_id: Channel ID
        skip: Number of messages to skip (for pagination)
        limit: Maximum number of messages to return (max 100)
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of messages (newest first)
        
    Raises:
        HTTPException: If channel not found or user not authorized
    """
    # Check if channel exists
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    # Check if user is a member of the server
    membership = db.query(ServerMember).filter(
        ServerMember.server_id == channel.server_id,
        ServerMember.user_id == current_user.id
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this channel"
        )
    
    # Get messages (newest first)
    messages = db.query(Message).filter(
        Message.channel_id == channel_id
    ).order_by(Message.created_at.desc()).offset(skip).limit(limit).all()
    
    # Reverse to show oldest first in the returned list
    messages.reverse()
    
    return messages


@router.get("/messages/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific message by ID.
    
    Args:
        message_id: Message ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Message details
        
    Raises:
        HTTPException: If message not found or user not authorized
    """
    message = db.query(Message).filter(Message.id == message_id).first()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Check if user has access to the channel
    channel = db.query(Channel).filter(Channel.id == message.channel_id).first()
    membership = db.query(ServerMember).filter(
        ServerMember.server_id == channel.server_id,
        ServerMember.user_id == current_user.id
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this message"
        )
    
    return message


@router.patch("/messages/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: int,
    message_update: MessageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update (edit) a message.
    
    Args:
        message_id: Message ID
        message_update: Updated message content
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated message
        
    Raises:
        HTTPException: If not authorized or message not found
    """
    message = db.query(Message).filter(Message.id == message_id).first()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Only message author can edit
    if message.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own messages"
        )
    
    # Update message
    message.content = message_update.content
    message.is_edited = True
    
    db.commit()
    db.refresh(message)
    
    logger.info(f"Message {message_id} edited by user {current_user.username}")
    
    return message


@router.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a message.
    
    Args:
        message_id: Message ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If not authorized or message not found
    """
    message = db.query(Message).filter(Message.id == message_id).first()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Only message author or server admin/owner can delete
    if message.user_id != current_user.id:
        # Check if user is admin/owner
        channel = db.query(Channel).filter(Channel.id == message.channel_id).first()
        membership = db.query(ServerMember).filter(
            ServerMember.server_id == channel.server_id,
            ServerMember.user_id == current_user.id
        ).first()
        
        if not membership or membership.role not in ["owner", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this message"
            )
    
    db.delete(message)
    db.commit()
    
    logger.info(f"Message {message_id} deleted")
