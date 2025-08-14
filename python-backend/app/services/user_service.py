from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import jwt
from jwt import PyJWTError
import hashlib
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import Depends, HTTPException, status, Header
from app.core.database import get_db

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> tuple[str, int]:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # Return token and expiration timestamp in milliseconds
    expire_timestamp_ms = int(expire.timestamp() * 1000)
    return encoded_jwt, expire_timestamp_ms


def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check token type
        if payload.get("type") != token_type:
            return None
            
        # Check expiration
        exp = payload.get("exp")
        if exp is None:
            return None
            
        if datetime.utcnow() > datetime.fromtimestamp(exp):
            return None
            
        return payload
    except PyJWTError:
        return None

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user"""
    try:
        print(f"🔐 create_user: Creating user with data: {user}")
        hashed_password = hash_password(user.password)
        print(f"🔐 create_user: Password hashed successfully")
        
        db_user = User(
            name=user.name,
            email=user.email,
            password=hashed_password,
            role=user.role,
            is_active=user.is_active
        )
        print(f"🔐 create_user: User object created: {db_user}")
        
        db.add(db_user)
        print(f"🔐 create_user: User added to session")
        
        db.commit()
        print(f"🔐 create_user: Changes committed to database")
        
        db.refresh(db_user)
        print(f"🔐 create_user: User refreshed from database: ID={db_user.id}")
        
        return db_user
    except Exception as e:
        print(f"🔐 create_user: Error creating user: {str(e)}")
        db.rollback()
        raise

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all users with pagination"""
    return db.query(User).offset(skip).limit(limit).all()

def get_users_by_role(db: Session, role: UserRole, skip: int = 0, limit: int = 100) -> List[User]:
    """Get users by role with pagination"""
    return db.query(User).filter(User.role == role).offset(skip).limit(limit).all()

def update_user_role(db: Session, user_id: int, new_role: UserRole) -> Optional[User]:
    """Update user role"""
    user = get_user_by_id(db, user_id)
    if user:
        user.role = new_role
        db.commit()
        db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password"""
    try:
        print(f"🔐 authenticate_user: Attempting authentication for email: {email}")
        user = get_user_by_email(db, email)
        if not user:
            print(f"🔐 authenticate_user: User not found for email: {email}")
            return None
        print(f"🔐 authenticate_user: User found - ID: {user.id}, Email: {user.email}, Active: {user.is_active}")
        
        if not verify_password(password, user.password):
            print(f"🔐 authenticate_user: Password verification failed for user: {email}")
            return None
        
        if user.is_active != 1:
            print(f"🔐 authenticate_user: User is not active: {email}, is_active: {user.is_active}")
            return None
        
        print(f"🔐 authenticate_user: Authentication successful for user: {email}")
        return user
    except Exception as e:
        print(f"🔐 authenticate_user: Error during authentication: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def delete_user(db: Session, user_id: int) -> bool:
    """Delete user by ID"""
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)) -> User:
    """Get current authenticated user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    print(f"🔐 get_current_user: Authorization header: {authorization}")
    
    if not authorization:
        print("🔐 get_current_user: No authorization header")
        raise credentials_exception
    
    try:
        # Extract token from Authorization header
        if not authorization.startswith("Bearer "):
            print("🔐 get_current_user: Authorization header doesn't start with 'Bearer '")
            raise credentials_exception
        token = authorization.split(" ")[1]
        print(f"🔐 get_current_user: Extracted token: {token[:20]}...")
        
        # Verify token
        payload = verify_token(token)
        if payload is None:
            print("🔐 get_current_user: Token verification failed")
            raise credentials_exception
        
        print(f"🔐 get_current_user: Token payload: {payload}")
        
        # Get user ID from token
        user_id: int = payload.get("sub")
        if user_id is None:
            print("🔐 get_current_user: No 'sub' field in token payload")
            raise credentials_exception
        
        print(f"🔐 get_current_user: User ID from token: {user_id}")
        
        # Get user from database
        user = get_user_by_id(db, user_id=user_id)
        if user is None:
            print("🔐 get_current_user: User not found in database")
            raise credentials_exception
        
        print(f"🔐 get_current_user: User found: {user.email} (ID: {user.id})")
        return user
    except Exception as e:
        print(f"🔐 get_current_user: Exception: {e}")
        raise credentials_exception
