from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import jwt
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

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES or 5  # fallback to 5 minutes
        expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    
    current_time = datetime.utcnow()
    
    to_encode.update({
        "exp": expire,
        "iat": current_time,
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    expire_timestamp_ms = int(expire.timestamp() * 1000)
    print(f"🔐 create_access_token: Token created with expiration: {expire_timestamp_ms}")
    return encoded_jwt, expire_timestamp_ms

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload if valid"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"🔐 verify_token: Token verified successfully, payload: {payload}")
        return payload
    except jwt.ExpiredSignatureError:
        print("🔐 verify_token: Token expired")
        return None
    except jwt.JWTError as e:
        print(f"🔐 verify_token: JWT error: {e}")
        return None

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user"""
    hashed_password = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

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
        
        # Get user email from token
        email: str = payload.get("sub")
        if email is None:
            print("🔐 get_current_user: No 'sub' field in token payload")
            raise credentials_exception
        
        print(f"🔐 get_current_user: User email from token: {email}")
        
        # Get user from database
        user = get_user_by_email(db, email=email)
        if user is None:
            print("🔐 get_current_user: User not found in database")
            raise credentials_exception
        
        print(f"🔐 get_current_user: User found: {user.email}")
        return user
    except Exception as e:
        print(f"🔐 get_current_user: Exception: {e}")
        raise credentials_exception
