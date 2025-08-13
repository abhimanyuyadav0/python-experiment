"use client";

import { Download, Trash2, RefreshCcw } from "lucide-react";
import React, { useState } from "react";
import {
  uploadFile,
  getUserFiles,
  deleteFile as deleteFileService,
  downloadFile as downloadFileService,
} from "@/lib/api/services/fileServices";
import { toast } from "react-toastify";
import { useQuery } from "@tanstack/react-query";
import UploadFile from "@/components/uploadFile";

const CreateDataPage = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string>("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadedFileDetails, setUploadedFileDetails] = useState<any>(null);

  // Format file size
  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  const {
    data: uploadedFiles,
    isFetching: isLoadingFiles,
    refetch: refetchFiles,
  } = useQuery({
    queryKey: ["files"],
    queryFn: () => getUserFiles(),
  });

  const downloadFile = async (fileId: number, filename: string) => {
    try {
      const response = await downloadFileService(fileId);

      // Create blob and download
      const blob = new Blob([response.data], {
        type: response.headers["content-type"],
      });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error: any) {
      toast.error("Error downloading file:", error);
    }
  };

  const deleteFile = async (fileId: number) => {
    if (!confirm("Are you sure you want to delete this file?")) return;

    try {
      await deleteFileService(fileId);

      // Remove from uploaded files list
      refetchFiles();
    } catch (error: any) {
      toast.error("Error deleting file:", error);
    }
  };

  const handleUpload = async (file: File) => {
    setIsUploading(true);
    setUploadStatus(`Uploading ${file.name}...`);
    try {
      const response = await uploadFile(file);
      setUploadStatus("Upload successful!");
      toast.success("File uploaded successfully!");
      refetchFiles();
      return response.data; // Return the upload response data
    } catch (error: any) {
      toast.error(
        "Upload failed: " + (error.response?.data?.detail || error.message)
      );
      setUploadStatus(
        `Upload failed: ${error.response?.data?.detail || "Upload failed"}`
      );
      throw error; // Re-throw to let the component handle the error
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">
          Medical Report Data Generator
        </h1>
        <button onClick={() => refetchFiles()} disabled={isLoadingFiles}>
          <RefreshCcw
            className={`w-5 h-5 ${isLoadingFiles ? "animate-spin" : ""}`}
          />
        </button>
      </div>

      <div className="flex flex-wrap gap-4 mb-8">
        <UploadFile
          label="Upload File"
          name="file"
          type="file"
          placeholder="Upload File"
          value={selectedFile}
          onChange={(file) => setSelectedFile(file)}
          onUpload={(file) => handleUpload(file)}
          onUploadSuccess={(fileDetails) => {
            setUploadedFileDetails(fileDetails);
          }}
          isUploading={isUploading}
        />
      </div>

      {/* Upload Status */}
      {uploadStatus && (
        <div
          className={`mb-4 p-3 rounded-lg ${
            uploadStatus.includes("successful")
              ? "bg-green-100 text-green-800 border border-green-200"
              : uploadStatus.includes("failed")
              ? "bg-red-100 text-red-800 border border-red-200"
              : "bg-blue-100 text-blue-800 border border-blue-200"
          }`}
        >
          {uploadStatus}
        </div>
      )}

      {/* Uploaded File Details */}
      {uploadedFileDetails && (
        <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">
            Last Uploaded File Details:
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium text-blue-700">File Name:</span>
              <span className="ml-2 text-blue-900">
                {uploadedFileDetails.original_filename}
              </span>
            </div>
            <div>
              <span className="font-medium text-blue-700">File Type:</span>
              <span className="ml-2 text-blue-900">
                {uploadedFileDetails.file_type}
              </span>
            </div>
            <div>
              <span className="font-medium text-blue-700">File Size:</span>
              <span className="ml-2 text-blue-900">
                {formatFileSize(uploadedFileDetails.file_size)}
              </span>
            </div>
            <div>
              <span className="font-medium text-blue-700">File ID:</span>
              <span className="ml-2 text-blue-900">
                {uploadedFileDetails.id}
              </span>
            </div>
            {uploadedFileDetails.url && (
              <div className="md:col-span-2">
                <span className="font-medium text-blue-700">File URL:</span>
                <span className="ml-2 text-blue-900 break-all">
                  {uploadedFileDetails.url}
                </span>
              </div>
            )}
          </div>
        </div>
      )}
      <div className="mt-3">
        {uploadedFiles?.data.files.length === 0 ? (
          <p className="text-gray-500 text-center py-4">
            No files uploaded yet.
          </p>
        ) : (
          <div className="space-y-3">
            {uploadedFiles?.data.files.map((file) => (
              <div
                key={file.id}
                className="border border-gray-200 rounded-lg p-3"
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900">
                      {file.original_filename}
                    </h4>
                    <p className="text-sm text-gray-500">
                      Type: {file.file_type} • Size:{" "}
                      {formatFileSize(file.file_size)}
                    </p>
                    <p className="text-sm text-gray-500">
                      Uploaded: {new Date(file.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="flex gap-2 ml-4">
                    <button
                      onClick={() =>
                        downloadFile(file.id, file.original_filename)
                      }
                      className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm flex items-center gap-1"
                    >
                      <Download className="w-3 h-3" />
                      Download
                    </button>
                    <button
                      onClick={() => deleteFile(file.id)}
                      className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm flex items-center gap-1"
                    >
                      <Trash2 className="w-3 h-3" />
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default CreateDataPage;
