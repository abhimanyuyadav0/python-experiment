from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.user import UserRole
from app.schemas.user import UserCreate, UserResponse, UserLogin, TokenData
from app.services.user_service import (
    create_user, get_user_by_id, get_user_by_email, get_users, get_users_by_role,
    update_user_role, authenticate_user, create_access_token, delete_user
)

router = APIRouter()

@router.post("/authenticate", response_model=TokenData)
def authenticate_user_endpoint(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return token"""
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    token, expires_at = create_access_token(data={"sub": user.email})
    print("token, expires_at", token, expires_at)
    return TokenData(
        user=user,
        token=token,
        expires_at=expires_at
    )

@router.get("/role/{role}", response_model=List[UserResponse])
def get_users_by_role_endpoint(
    role: UserRole,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """Get users by role with pagination"""
    users = get_users_by_role(db, role, skip=skip, limit=limit)
    return users

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if user with email already exists
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    return create_user(db=db, user=user)

@router.get("/", response_model=List[UserResponse])
def get_all_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """Get all users with pagination"""
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.patch("/{user_id}/role", response_model=UserResponse)
def update_user_role_endpoint(
    user_id: int,
    role: UserRole = Query(..., description="New role for the user"),
    db: Session = Depends(get_db)
):
    """Update user role (admin only)"""
    user = update_user_role(db, user_id, role)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    """Delete user by ID"""
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
