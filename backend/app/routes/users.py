"""User routes for profile management."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from ..database import get_db
from ..models import User, UserStatus
from ..schemas import UserResponse, UserUpdate
from ..dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current authenticated user's profile.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User profile data
    """
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user by ID.
    
    Args:
        user_id: User ID to retrieve
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        User profile data
        
    Raises:
        HTTPException: If user not found
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update current user's profile.
    
    Args:
        user_update: User update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated user profile
        
    Raises:
        HTTPException: If username or email already taken
    """
    # Update username if provided
    if user_update.username:
        existing_user = db.query(User).filter(
            User.username == user_update.username,
            User.id != current_user.id
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        current_user.username = user_update.username
    
    # Update email if provided
    if user_update.email:
        existing_email = db.query(User).filter(
            User.email == user_update.email,
            User.id != current_user.id
        ).first()
        
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken"
            )
        
        current_user.email = user_update.email
    
    # Update status if provided
    if user_update.status:
        current_user.status = user_update.status
    
    db.commit()
    db.refresh(current_user)
    
    logger.info(f"User profile updated: {current_user.username} (ID: {current_user.id})")
    
    return current_user


@router.patch("/me/status", response_model=UserResponse)
async def update_user_status(
    new_status: UserStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user's online status.
    
    Args:
        new_status: New user status
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated user profile
    """
    current_user.status = new_status
    db.commit()
    db.refresh(current_user)
    
    logger.info(f"User status updated: {current_user.username} -> {new_status}")
    
    return current_user
