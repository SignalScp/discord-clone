"""Channel routes for channel management."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from ..database import get_db
from ..models import User, Channel, ServerMember
from ..schemas import ChannelResponse, ChannelUpdate
from ..dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{channel_id}", response_model=ChannelResponse)
async def get_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get channel details by ID.
    
    Args:
        channel_id: Channel ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Channel details
        
    Raises:
        HTTPException: If channel not found or user not authorized
    """
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
    
    return channel


@router.patch("/{channel_id}", response_model=ChannelResponse)
async def update_channel(
    channel_id: int,
    channel_update: ChannelUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update channel details.
    
    Args:
        channel_id: Channel ID
        channel_update: Channel update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated channel
        
    Raises:
        HTTPException: If not authorized or channel not found
    """
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    # Check if user has permission (not just a regular member)
    membership = db.query(ServerMember).filter(
        ServerMember.server_id == channel.server_id,
        ServerMember.user_id == current_user.id
    ).first()
    
    if not membership or membership.role == "member":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this channel"
        )
    
    # Update channel fields
    if channel_update.name:
        channel.name = channel_update.name
    if channel_update.description is not None:
        channel.description = channel_update.description
    
    db.commit()
    db.refresh(channel)
    
    logger.info(f"Channel updated: {channel.name} (ID: {channel.id})")
    
    return channel


@router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a channel.
    
    Args:
        channel_id: Channel ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If not authorized or channel not found
    """
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    # Check if user has permission
    membership = db.query(ServerMember).filter(
        ServerMember.server_id == channel.server_id,
        ServerMember.user_id == current_user.id
    ).first()
    
    if not membership or membership.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this channel"
        )
    
    db.delete(channel)
    db.commit()
    
    logger.info(f"Channel deleted: {channel.name} (ID: {channel.id})")
