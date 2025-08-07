import axoisInstance from "../../axois";

export interface FileResponse {
  id: number;
  filename: string;
  original_filename: string;
  file_type: "image" | "document" | "video" | "audio" | "archive" | "other";
  file_extension: string;
  file_size: number;
  file_path: string;
  mime_type: string;
  user_id: number;
  created_at: string;
  updated_at: string | null;
  url: string;
}

export interface FileUploadResponse {
  message: string;
  file: FileResponse;
}

export interface FileListResponse {
  files: FileResponse[];
  total: number;
}

// Upload a file
export const uploadFile = (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  
  console.log("fileServices: Uploading file:", {
    name: file.name,
    type: file.type,
    size: file.size
  });
  
  return axoisInstance.post<FileUploadResponse>("/api/v1/files/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

// Get all files for the current user
export const getUserFiles = (fileType?: string) => {
  const params = fileType ? { file_type: fileType } : {};
  console.log("getUserFiles: Making request with params:", params);
  return axoisInstance.get<FileListResponse>("/api/v1/files/", { params });
};

// Get file information by ID
export const getFileInfo = (fileId: number) => {
  return axoisInstance.get<FileResponse>(`/api/v1/files/${fileId}`);
};

// Download a file
export const downloadFile = (fileId: number) => {
  return axoisInstance.get(`/api/v1/files/${fileId}/download`, {
    responseType: "blob",
  });
};

// Delete a file
export const deleteFile = (fileId: number) => {
  return axoisInstance.delete(`/api/v1/files/${fileId}`);
};

// Get files by type
export const getFilesByType = (fileType: string) => {
  return axoisInstance.get<FileListResponse>(`/api/v1/files/types/${fileType}`);
};

// Test authentication
export const testFileAuth = () => {
  console.log("fileServices: Testing file authentication");
  return axoisInstance.get("/api/v1/files/test-auth");
};
