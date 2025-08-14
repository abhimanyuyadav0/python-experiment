from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

# Import this at the module level to avoid circular imports
from sqlalchemy.orm import Mapped, relationship

class UserRole(str, enum.Enum):
    admin = "admin"
    tenant = "tenant"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    is_active = Column(Integer, default=1, nullable=False) # Using Integer for SQLite compatibility (0=False, 1=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    files = relationship("File", back_populates="user", lazy="dynamic")
