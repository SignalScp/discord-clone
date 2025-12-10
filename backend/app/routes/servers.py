"""Server routes for server management."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from ..database import get_db
from ..models import User, Server, ServerMember, MemberRole, Channel
from ..schemas import ServerCreate, ServerResponse, ServerUpdate, ChannelCreate, ChannelResponse, ServerMemberResponse
from ..dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("", response_model=ServerResponse, status_code=status.HTTP_201_CREATED)
async def create_server(
    server_data: ServerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new server.
    
    Args:
        server_data: Server creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created server object
    """
    # Create server
    new_server = Server(
        name=server_data.name,
        description=server_data.description,
        owner_id=current_user.id
    )
    
    db.add(new_server)
    db.commit()
    db.refresh(new_server)
    
    # Add owner as member with OWNER role
    owner_member = ServerMember(
        server_id=new_server.id,
        user_id=current_user.id,
        role=MemberRole.OWNER
    )
    
    db.add(owner_member)
    
    # Create default "general" channel
    general_channel = Channel(
        server_id=new_server.id,
        name="general",
        description="General discussion channel"
    )
    
    db.add(general_channel)
    db.commit()
    
    logger.info(f"Server created: {new_server.name} (ID: {new_server.id}) by user {current_user.username}")
    
    return new_server


@router.get("", response_model=List[ServerResponse])
async def get_user_servers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all servers the current user is a member of.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of servers
    """
    # Get all server memberships for current user
    memberships = db.query(ServerMember).filter(
        ServerMember.user_id == current_user.id
    ).all()
    
    # Get servers from memberships
    server_ids = [m.server_id for m in memberships]
    servers = db.query(Server).filter(Server.id.in_(server_ids)).all()
    
    return servers


@router.get("/{server_id}", response_model=ServerResponse)
async def get_server(
    server_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get server details by ID.
    
    Args:
        server_id: Server ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Server details
        
    Raises:
        HTTPException: If server not found or user not a member
    """
    server = db.query(Server).filter(Server.id == server_id).first()
    
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Server not found"
        )
    
    # Check if user is a member
    membership = db.query(ServerMember).filter(
        ServerMember.server_id == server_id,
        ServerMember.user_id == current_user.id
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this server"
        )
    
    return server


@router.patch("/{server_id}", response_model=ServerResponse)
async def update_server(
    server_id: int,
    server_update: ServerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update server details.
    
    Args:
        server_id: Server ID
        server_update: Server update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated server
        
    Raises:
        HTTPException: If not authorized or server not found
    """
    server = db.query(Server).filter(Server.id == server_id).first()
    
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Server not found"
        )
    
    # Check if user is owner or admin
    membership = db.query(ServerMember).filter(
        ServerMember.server_id == server_id,
        ServerMember.user_id == current_user.id
    ).first()
    
    if not membership or membership.role not in [MemberRole.OWNER, MemberRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this server"
        )
    
    # Update server fields
    if server_update.name:
        server.name = server_update.name
    if server_update.description is not None:
        server.description = server_update.description
    
    db.commit()
    db.refresh(server)
    
    logger.info(f"Server updated: {server.name} (ID: {server.id})")
    
    return server


@router.delete("/{server_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_server(
    server_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a server (owner only).
    
    Args:
        server_id: Server ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If not owner or server not found
    """
    server = db.query(Server).filter(Server.id == server_id).first()
    
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Server not found"
        )
    
    # Only owner can delete server
    if server.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the server owner can delete this server"
        )
    
    db.delete(server)
    db.commit()
    
    logger.info(f"Server deleted: {server.name} (ID: {server.id})")


@router.get("/{server_id}/members", response_model=List[ServerMemberResponse])
async def get_server_members(
    server_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all members of a server.
    
    Args:
        server_id: Server ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of server members
        
    Raises:
        HTTPException: If user not a member
    """
    # Check if user is a member
    membership = db.query(ServerMember).filter(
        ServerMember.server_id == server_id,
        ServerMember.user_id == current_user.id
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this server"
        )
    
    # Get all members
    members = db.query(ServerMember).filter(
        ServerMember.server_id == server_id
    ).all()
    
    return members


@router.post("/{server_id}/channels", response_model=ChannelResponse, status_code=status.HTTP_201_CREATED)
async def create_channel(
    server_id: int,
    channel_data: ChannelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new channel in a server.
    
    Args:
        server_id: Server ID
        channel_data: Channel creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created channel
        
    Raises:
        HTTPException: If not authorized or server not found
    """
    # Check if server exists
    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Server not found"
        )
    
    # Check if user has permission (owner, admin, or moderator)
    membership = db.query(ServerMember).filter(
        ServerMember.server_id == server_id,
        ServerMember.user_id == current_user.id
    ).first()
    
    if not membership or membership.role == MemberRole.MEMBER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create channels"
        )
    
    # Create channel
    new_channel = Channel(
        server_id=server_id,
        name=channel_data.name,
        description=channel_data.description
    )
    
    db.add(new_channel)
    db.commit()
    db.refresh(new_channel)
    
    logger.info(f"Channel created: {new_channel.name} (ID: {new_channel.id}) in server {server_id}")
    
    return new_channel


@router.get("/{server_id}/channels", response_model=List[ChannelResponse])
async def get_server_channels(
    server_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all channels in a server.
    
    Args:
        server_id: Server ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of channels
        
    Raises:
        HTTPException: If user not a member
    """
    # Check if user is a member
    membership = db.query(ServerMember).filter(
        ServerMember.server_id == server_id,
        ServerMember.user_id == current_user.id
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this server"
        )
    
    # Get all channels
    channels = db.query(Channel).filter(Channel.server_id == server_id).all()
    
    return channels
