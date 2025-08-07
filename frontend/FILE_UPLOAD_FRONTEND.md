# Frontend File Upload Implementation

## Overview

The frontend file upload functionality has been implemented in the admin create-data page with a proper service layer following the existing patterns in the application.

## Features

### ✅ **File Upload Service**
- **Location**: `src/lib/api/services/fileServices/index.ts`
- **Features**:
  - Upload files with proper authentication
  - Get user files with optional type filtering
  - Download files with proper blob handling
  - Delete files with confirmation
  - TypeScript interfaces for type safety

### ✅ **Enhanced UI Components**
- **File Upload Button**: Triggers file selection dialog
- **File Type Validation**: Supports multiple file types
- **Progress Indicators**: Loading states for upload and file listing
- **File Management Modal**: View, download, and delete files
- **Responsive Design**: Works on different screen sizes

### ✅ **Supported File Types**
- **Documents**: PDF, DOC, DOCX, TXT
- **Images**: JPG, JPEG, PNG, GIF
- **Videos**: MP4
- **Audio**: MP3
- **Archives**: ZIP

## Implementation Details

### File Service (`fileServices/index.ts`)

```typescript
// Upload a file
export const uploadFile = (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  
  return axoisInstance.post<FileUploadResponse>("/api/v1/files/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

// Get user files
export const getUserFiles = (fileType?: string) => {
  const params = fileType ? { file_type: fileType } : {};
  return axoisInstance.get<FileListResponse>("/api/v1/files/", { params });
};

// Download file
export const downloadFile = (fileId: number) => {
  return axoisInstance.get(`/api/v1/files/${fileId}/download`, {
    responseType: "blob",
  });
};

// Delete file
export const deleteFile = (fileId: number) => {
  return axoisInstance.delete(`/api/v1/files/${fileId}`);
};
```

### Page Integration (`create-data/page.tsx`)

#### State Management
```typescript
const [uploadedFiles, setUploadedFiles] = useState<FileResponse[]>([]);
const [isUploading, setIsUploading] = useState(false);
const [isLoadingFiles, setIsLoadingFiles] = useState(false);
const [uploadStatus, setUploadStatus] = useState<string>("");
const [showUploadModal, setShowUploadModal] = useState(false);
```

#### File Upload Handler
```typescript
const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
  const file = event.target.files?.[0];
  if (!file) return;

  // Validate file type and size
  // Upload using service
  // Update UI state
  // Show success/error messages
};
```

#### File Management Functions
```typescript
// List user files
const listUploadedFiles = async () => {
  const response = await getUserFiles();
  setUploadedFiles(response.data.files);
};

// Download file
const downloadFile = async (fileId: number, filename: string) => {
  const response = await downloadFileService(fileId);
  // Create blob and trigger download
};

// Delete file
const deleteFile = async (fileId: number) => {
  await deleteFileService(fileId);
  // Update local state
};
```

## UI Components

### File Upload Button
- Triggers hidden file input
- Shows loading state during upload
- Displays upload status messages

### File Management Modal
- Lists all uploaded files
- Shows file metadata (name, type, size, upload date)
- Download and delete actions for each file
- Responsive design with proper spacing

### File Display
```typescript
{uploadedFiles.map((file) => (
  <div key={file.id} className="border border-gray-200 rounded-lg p-3">
    <div className="flex justify-between items-start">
      <div className="flex-1">
        <h4 className="font-medium text-gray-900">
          {file.original_filename}
        </h4>
        <p className="text-sm text-gray-500">
          Type: {file.file_type} • Size: {formatFileSize(file.file_size)}
        </p>
        <p className="text-sm text-gray-500">
          Uploaded: {new Date(file.created_at).toLocaleDateString()}
        </p>
      </div>
      <div className="flex gap-2 ml-4">
        <button onClick={() => downloadFile(file.id, file.original_filename)}>
          <Download className="w-3 h-3" /> Download
        </button>
        <button onClick={() => deleteFile(file.id)}>
          <Trash2 className="w-3 h-3" /> Delete
        </button>
      </div>
    </div>
  </div>
))}
```

## Error Handling

### Upload Errors
- File type validation
- File size limits (10MB)
- Network error handling
- Authentication error handling

### Service Errors
- Proper error messages from API
- User-friendly error display
- Graceful fallbacks

## Security Features

1. **Authentication**: All requests include JWT token
2. **File Validation**: Client-side file type and size validation
3. **User Isolation**: Users can only access their own files
4. **Secure Downloads**: Files downloaded through authenticated endpoints

## Usage

1. **Upload File**:
   - Click "Upload File" button
   - Select file from dialog
   - File is uploaded and added to list

2. **View Files**:
   - Click "View Uploaded Files" button
   - Modal shows all user files
   - Files are automatically loaded on page load

3. **Download File**:
   - Click download button in file list
   - File is downloaded with original filename

4. **Delete File**:
   - Click delete button in file list
   - Confirmation dialog appears
   - File is removed from server and list

## Integration with Backend

The frontend integrates seamlessly with the Python backend file upload API:

- **Upload Endpoint**: `POST /api/v1/files/upload`
- **List Files**: `GET /api/v1/files/`
- **Download File**: `GET /api/v1/files/{id}/download`
- **Delete File**: `DELETE /api/v1/files/{id}`

All endpoints require authentication and return proper error responses that are handled by the frontend service layer.
