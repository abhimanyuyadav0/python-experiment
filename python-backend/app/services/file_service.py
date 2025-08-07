import os
import uuid
import mimetypes
from pathlib import Path
from typing import List, Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.file import File, FileType

class FileService:
    def __init__(self, db: Session):
        self.db = db
        self.uploads_dir = Path("uploads")
        self.uploads_dir.mkdir(exist_ok=True)
        print(f"🔧 FileService: Uploads directory: {self.uploads_dir.absolute()}")
        print(f"🔧 FileService: Directory exists: {self.uploads_dir.exists()}")
        print(f"🔧 FileService: Directory writable: {os.access(self.uploads_dir, os.W_OK)}")

    def _get_file_type(self, filename: str, mime_type: str) -> FileType:
        """Determine file type based on extension and MIME type."""
        extension = Path(filename).suffix.lower()
        
        # Image files
        if extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'] or 'image/' in mime_type:
            return FileType.IMAGE
        
        # Document files
        elif extension in ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'] or 'application/pdf' in mime_type or 'application/msword' in mime_type:
            return FileType.DOCUMENT
        
        # Video files
        elif extension in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm'] or 'video/' in mime_type:
            return FileType.VIDEO
        
        # Audio files
        elif extension in ['.mp3', '.wav', '.flac', '.aac', '.ogg'] or 'audio/' in mime_type:
            return FileType.AUDIO
        
        # Archive files
        elif extension in ['.zip', '.rar', '.7z', '.tar', '.gz'] or 'application/zip' in mime_type:
            return FileType.ARCHIVE
        
        else:
            return FileType.OTHER

    def _create_user_directory(self, user_id: int, file_type: FileType) -> Path:
        """Create user-specific directory structure."""
        user_dir = self.uploads_dir / "user" / str(user_id) / file_type.value
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir

    def _generate_unique_filename(self, original_filename: str) -> str:
        """Generate a unique filename to prevent conflicts."""
        extension = Path(original_filename).suffix
        unique_id = str(uuid.uuid4())
        return f"{unique_id}{extension}"

    async def upload_file(self, file: UploadFile, user_id: int) -> File:
        """Upload a file and store metadata in database."""
        print(f"🔧 FileService.upload_file: Starting upload for user {user_id}")
        
        # Read file content
        content = await file.read()
        file_size = len(content)
        print(f"🔧 FileService.upload_file: File size: {file_size} bytes")
        
        # Determine file type
        file_type = self._get_file_type(file.filename, file.content_type or "")
        print(f"🔧 FileService.upload_file: File type: {file_type}")
        
        # Create user directory
        user_dir = self._create_user_directory(user_id, file_type)
        print(f"🔧 FileService.upload_file: User directory: {user_dir}")
        
        # Generate unique filename
        stored_filename = self._generate_unique_filename(file.filename)
        file_path = user_dir / stored_filename
        print(f"🔧 FileService.upload_file: File path: {file_path}")
        
        # Save file to disk
        with open(file_path, "wb") as f:
            f.write(content)
        print(f"🔧 FileService.upload_file: File saved to disk")
        
        # Create relative path for database
        relative_path = str(file_path.relative_to(self.uploads_dir))
        print(f"🔧 FileService.upload_file: Relative path: {relative_path}")
        
        # Create database record
        db_file = File(
            filename=stored_filename,
            original_filename=file.filename,
            file_type=file_type,
            file_extension=Path(file.filename).suffix.lower(),
            file_size=file_size,
            file_path=relative_path,
            mime_type=file.content_type or "application/octet-stream",
            user_id=user_id
        )
        
        self.db.add(db_file)
        self.db.commit()
        self.db.refresh(db_file)
        print(f"🔧 FileService.upload_file: Database record created, ID: {db_file.id}")
        
        return db_file

    def get_user_files(self, user_id: int, file_type: Optional[str] = None) -> List[File]:
        """Get all files for a user, optionally filtered by type."""
        print(f"🔧 FileService.get_user_files: user_id={user_id}, file_type={file_type}")
        
        query = self.db.query(File).filter(File.user_id == user_id)
        
        if file_type:
            query = query.filter(File.file_type == file_type)
        
        files = query.order_by(File.created_at.desc()).all()
        print(f"🔧 FileService.get_user_files: Found {len(files)} files")
        
        return files

    def get_file_by_id(self, file_id: int, user_id: int) -> Optional[File]:
        """Get a specific file by ID, ensuring it belongs to the user."""
        return self.db.query(File).filter(
            File.id == file_id,
            File.user_id == user_id
        ).first()

    def get_file_path(self, file_id: int, user_id: int) -> Optional[str]:
        """Get the full file path for a file."""
        file = self.get_file_by_id(file_id, user_id)
        if not file:
            return None
        
        full_path = self.uploads_dir / file.file_path
        return str(full_path) if full_path.exists() else None

    def delete_file(self, file_id: int, user_id: int) -> bool:
        """Delete a file from storage and database."""
        file = self.get_file_by_id(file_id, user_id)
        if not file:
            return False
        
        # Delete from storage
        full_path = self.uploads_dir / file.file_path
        if full_path.exists():
            full_path.unlink()
        
        # Delete from database
        self.db.delete(file)
        self.db.commit()
        
        return True
