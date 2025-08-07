from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import jwt
import hashlib
from datetime import datetime, timedelta
from typing import List, Optional

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
    print(f"🔐 Token Debug: ACCESS_TOKEN_EXPIRE_MINUTES = {ACCESS_TOKEN_EXPIRE_MINUTES}")
    print(f"🔐 Token Debug: Current time (UTC) = {current_time}")
    print(f"🔐 Token Debug: Expire time (UTC) = {expire}")
    print(f"🔐 Token Debug: Current timestamp (seconds) = {current_time.timestamp()}")
    print(f"🔐 Token Debug: Current timestamp (ms) = {int(current_time.timestamp() * 1000)}")
    print(f"🔐 Token Debug: Expire timestamp (seconds) = {expire.timestamp()}")
    print(f"🔐 Token Debug: Expire timestamp (ms) = {int(expire.timestamp() * 1000)}")
    print(f"🔐 Token Debug: Time difference (ms) = {int(expire.timestamp() * 1000) - int(current_time.timestamp() * 1000)}")
    
    to_encode.update({
        "exp": expire,
        "iat": current_time,
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    expire_timestamp_ms = int(expire.timestamp() * 1000)
    return encoded_jwt, expire_timestamp_ms

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload if valid"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
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
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    if not user.is_active:
        return None
    return user

def delete_user(db: Session, user_id: int) -> bool:
    """Delete user by ID"""
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
