from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FastAPIFile
from fastapi.responses import FileResponse as FastAPIFileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.file_service import FileService
from app.services.user_service import get_current_user
from app.models.user import User
from app.schemas.file import FileResponse, FileUploadResponse, FileListResponse

router = APIRouter()

@router.get("/test-auth")
async def test_file_auth(current_user: User = Depends(get_current_user)):
    """Test authentication for file endpoints"""
    print(f"🔐 test_file_auth: User authenticated - ID: {current_user.id}, Email: {current_user.email}")
    return {
        "message": "Authentication successful",
        "user_id": current_user.id,
        "user_email": current_user.email,
        "user_role": current_user.role
    }

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a file for the authenticated user.
    Files are stored in user-specific directories: user/{user_id}/{file_type}/
    """
    print(f"📁 upload_file: User ID: {current_user.id}")
    print(f"📁 upload_file: File: {file.filename}, Type: {file.content_type}, Size: {file.size}")
    print(f"📁 upload_file: User email: {current_user.email}, Role: {current_user.role}")
    
    file_service = FileService(db)
    
    try:
        uploaded_file = await file_service.upload_file(file, current_user.id)
        print(f"📁 upload_file: File uploaded successfully, ID: {uploaded_file.id}")
        
        # Create FileResponse with URL
        file_response = FileResponse(
            id=uploaded_file.id,
            filename=uploaded_file.filename,
            original_filename=uploaded_file.original_filename,
            file_type=uploaded_file.file_type,
            file_extension=uploaded_file.file_extension,
            file_size=uploaded_file.file_size,
            file_path=uploaded_file.file_path,
            mime_type=uploaded_file.mime_type,
            user_id=uploaded_file.user_id,
            created_at=uploaded_file.created_at,
            updated_at=uploaded_file.updated_at,
            url=f"/api/v1/files/{uploaded_file.id}/download"
        )
        
        return FileUploadResponse(
            message="File uploaded successfully",
            file=file_response
        )
    except Exception as e:
        print(f"📁 upload_file: Error: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/", response_model=FileListResponse)
async def get_user_files(
    file_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all files for the authenticated user, optionally filtered by file type.
    File types: image, document, video, audio, archive, other
    """
    print(f"📁 get_user_files: User ID: {current_user.id}, File type filter: {file_type}")
    print(f"📁 get_user_files: User email: {current_user.email}, Role: {current_user.role}")
    
    file_service = FileService(db)
    files = file_service.get_user_files(current_user.id, file_type)
    
    print(f"📁 get_user_files: Found {len(files)} files")
    
    # Convert File objects to FileResponse with URLs
    file_responses = []
    for file in files:
        file_response = FileResponse(
            id=file.id,
            filename=file.filename,
            original_filename=file.original_filename,
            file_type=file.file_type,
            file_extension=file.file_extension,
            file_size=file.file_size,
            file_path=file.file_path,
            mime_type=file.mime_type,
            user_id=file.user_id,
            created_at=file.created_at,
            updated_at=file.updated_at,
            url=f"/api/v1/files/{file.id}/download"
        )
        file_responses.append(file_response)
    
    return FileListResponse(
        files=file_responses,
        total=len(file_responses)
    )

@router.get("/{file_id}", response_model=FileResponse)
async def get_file_info(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get information about a specific file owned by the authenticated user.
    """
    file_service = FileService(db)
    file = file_service.get_file_by_id(file_id, current_user.id)
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        id=file.id,
        filename=file.filename,
        original_filename=file.original_filename,
        file_type=file.file_type,
        file_extension=file.file_extension,
        file_size=file.file_size,
        file_path=file.file_path,
        mime_type=file.mime_type,
        user_id=file.user_id,
        created_at=file.created_at,
        updated_at=file.updated_at,
        url=f"/api/v1/files/{file.id}/download"
    )

@router.get("/{file_id}/download")
async def download_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Download a file owned by the authenticated user.
    """
    file_service = FileService(db)
    file_path = file_service.get_file_path(file_id, current_user.id)
    
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")
    
    file = file_service.get_file_by_id(file_id, current_user.id)
    
    return FastAPIFileResponse(
        path=file_path,
        filename=file.original_filename,
        media_type=file.mime_type
    )

@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a file owned by the authenticated user.
    """
    file_service = FileService(db)
    success = file_service.delete_file(file_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {"message": "File deleted successfully"}

@router.get("/types/{file_type}", response_model=FileListResponse)
async def get_files_by_type(
    file_type: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all files of a specific type for the authenticated user.
    """
    file_service = FileService(db)
    files = file_service.get_user_files(current_user.id, file_type)
    
    # Convert File objects to FileResponse with URLs
    file_responses = []
    for file in files:
        file_response = FileResponse(
            id=file.id,
            filename=file.filename,
            original_filename=file.original_filename,
            file_type=file.file_type,
            file_extension=file.file_extension,
            file_size=file.file_size,
            file_path=file.file_path,
            mime_type=file.mime_type,
            user_id=file.user_id,
            created_at=file.created_at,
            updated_at=file.updated_at,
            url=f"/api/v1/files/{file.id}/download"
        )
        file_responses.append(file_response)
    
    return FileListResponse(
        files=file_responses,
        total=len(file_responses)
    )
