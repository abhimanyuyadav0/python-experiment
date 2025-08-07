# File Upload API Documentation

## Overview

The File Upload API provides secure, user-specific file storage with automatic file type categorization. Files are organized by user and file type in the following structure:

```
uploads/
├── user/
│   ├── {user_id}/
│   │   ├── image/
│   │   ├── document/
│   │   ├── video/
│   │   ├── audio/
│   │   ├── archive/
│   │   └── other/
```

## Features

- **User-specific storage**: Each user's files are completely isolated
- **Automatic file type detection**: Files are categorized based on extension and MIME type
- **Secure file naming**: Unique filenames prevent conflicts
- **Authentication required**: All operations require valid JWT token
- **File metadata storage**: Complete file information stored in database

## Supported File Types

| Category | Extensions | MIME Types |
|----------|------------|------------|
| **Image** | .jpg, .jpeg, .png, .gif, .bmp, .webp, .svg | image/* |
| **Document** | .pdf, .doc, .docx, .txt, .rtf, .odt | application/pdf, application/msword |
| **Video** | .mp4, .avi, .mov, .wmv, .flv, .webm | video/* |
| **Audio** | .mp3, .wav, .flac, .aac, .ogg | audio/* |
| **Archive** | .zip, .rar, .7z, .tar, .gz | application/zip |
| **Other** | All other file types | - |

## API Endpoints

### 1. Upload File

**POST** `/api/v1/files/upload`

Upload a file for the authenticated user.

**Headers:**
```
Authorization: Bearer {jwt_token}
Content-Type: multipart/form-data
```

**Request Body:**
```
file: [binary file data]
```

**Response:**
```json
{
  "message": "File uploaded successfully",
  "file": {
    "id": 1,
    "filename": "uuid-filename.ext",
    "original_filename": "my-document.pdf",
    "file_type": "document",
    "file_extension": ".pdf",
    "file_size": 1024000,
    "file_path": "user/1/document/uuid-filename.pdf",
    "mime_type": "application/pdf",
    "user_id": 1,
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": null,
    "url": "/api/v1/files/1/download"
  }
}
```

### 2. Get User Files

**GET** `/api/v1/files/`

Get all files for the authenticated user.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Query Parameters:**
- `file_type` (optional): Filter by file type (image, document, video, audio, archive, other)

**Response:**
```json
{
  "files": [
    {
      "id": 1,
      "filename": "uuid-filename.pdf",
      "original_filename": "my-document.pdf",
      "file_type": "document",
      "file_extension": ".pdf",
      "file_size": 1024000,
      "file_path": "user/1/document/uuid-filename.pdf",
      "mime_type": "application/pdf",
      "user_id": 1,
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": null,
      "url": "/api/v1/files/1/download"
    }
  ],
  "total": 1
}
```

### 3. Get File Information

**GET** `/api/v1/files/{file_id}`

Get detailed information about a specific file.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response:**
```json
{
  "id": 1,
  "filename": "uuid-filename.pdf",
  "original_filename": "my-document.pdf",
  "file_type": "document",
  "file_extension": ".pdf",
  "file_size": 1024000,
  "file_path": "user/1/document/uuid-filename.pdf",
  "mime_type": "application/pdf",
  "user_id": 1,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": null,
  "url": "/api/v1/files/1/download"
}
```

### 4. Download File

**GET** `/api/v1/files/{file_id}/download`

Download a file owned by the authenticated user.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response:**
- File content with appropriate headers
- Original filename preserved
- Correct MIME type set

### 5. Delete File

**DELETE** `/api/v1/files/{file_id}`

Delete a file owned by the authenticated user.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response:**
```json
{
  "message": "File deleted successfully"
}
```

### 6. Get Files by Type

**GET** `/api/v1/files/types/{file_type}`

Get all files of a specific type for the authenticated user.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response:**
```json
{
  "files": [...],
  "total": 5
}
```

## Usage Examples

### Python Example

```python
import requests

# Login to get token
login_data = {
    "username": "user@example.com",
    "password": "user123"
}
response = requests.post("http://localhost:8000/api/v1/users/login", data=login_data)
token = response.json()["access_token"]

# Upload file
headers = {"Authorization": f"Bearer {token}"}
with open("document.pdf", "rb") as f:
    files = {"file": ("document.pdf", f, "application/pdf")}
    response = requests.post(
        "http://localhost:8000/api/v1/files/upload",
        headers=headers,
        files=files
    )

if response.status_code == 200:
    file_info = response.json()["file"]
    print(f"File uploaded: {file_info['original_filename']}")
    print(f"Access URL: {file_info['url']}")
```

### cURL Example

```bash
# Login
curl -X POST "http://localhost:8000/api/v1/users/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=user123"

# Upload file (replace TOKEN with actual token)
curl -X POST "http://localhost:8000/api/v1/files/upload" \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@document.pdf"

# Get user files
curl -X GET "http://localhost:8000/api/v1/files/" \
  -H "Authorization: Bearer TOKEN"

# Download file
curl -X GET "http://localhost:8000/api/v1/files/1/download" \
  -H "Authorization: Bearer TOKEN" \
  -o downloaded_file.pdf
```

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 404 Not Found
```json
{
  "detail": "File not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Upload failed: [error message]"
}
```

## Security Features

1. **Authentication Required**: All endpoints require valid JWT token
2. **User Isolation**: Users can only access their own files
3. **Secure File Naming**: UUID-based filenames prevent conflicts
4. **File Type Validation**: Automatic categorization and validation
5. **Path Traversal Protection**: Secure file path handling

## Database Schema

The `files` table stores file metadata:

```sql
CREATE TABLE files (
    id INTEGER PRIMARY KEY,
    filename VARCHAR NOT NULL,
    original_filename VARCHAR NOT NULL,
    file_type VARCHAR NOT NULL,
    file_extension VARCHAR NOT NULL,
    file_size INTEGER NOT NULL,
    file_path VARCHAR NOT NULL,
    mime_type VARCHAR NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Testing

Run the test script to verify the API:

```bash
cd python-backend
python test_file_upload.py
```

This will:
1. Login as a test user
2. Upload a test file
3. Retrieve file information
4. List user files
5. Clean up test files
