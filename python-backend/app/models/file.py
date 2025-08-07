from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class FileType(str, enum.Enum):
    IMAGE = "image"
    DOCUMENT = "document"
    VIDEO = "video"
    AUDIO = "audio"
    ARCHIVE = "archive"
    OTHER = "other"

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)  # Stored filename
    original_filename = Column(String, nullable=False)  # Original user filename
    file_type = Column(Enum(FileType), nullable=False)
    file_extension = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)  # Size in bytes
    file_path = Column(String, nullable=False)  # Relative path from uploads directory
    mime_type = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    user = relationship("User", back_populates="files")
