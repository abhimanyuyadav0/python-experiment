from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.file import FileType

class FileResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_type: FileType
    file_extension: str
    file_size: int
    file_path: str
    mime_type: str
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    url: str

    class Config:
        from_attributes = True

class FileUploadResponse(BaseModel):
    message: str
    file: FileResponse

class FileListResponse(BaseModel):
    files: List[FileResponse]
    total: int
