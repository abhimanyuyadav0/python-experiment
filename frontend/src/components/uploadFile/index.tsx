import React, { useRef, useState } from "react";
import Modal from "../modal";
import Button from "../button";
import { PlusIcon, Upload, File, CheckCircle, XCircle } from "lucide-react";
import { toast } from "react-toastify";

interface UploadFileProps {
  label: string;
  name: string;
  type: string;
  placeholder: string;
  value: File | null;
  onChange: (file: File | null) => void;
  onUpload?: (file: File) => Promise<any>; // Changed to return upload response
  onUploadSuccess?: (fileDetails: any) => void; // New prop for upload success callback
  isUploading?: boolean;
}

const UploadFile = ({
  label,
  name,
  type,
  placeholder,
  value,
  onChange,
  onUpload,
  onUploadSuccess,
  isUploading = false,
}: UploadFileProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<string>("");
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [isUploadingInModal, setIsUploadingInModal] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate file type (allow common file types)
    const allowedTypes = [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "text/plain",
      "image/jpeg",
      "image/jpg",
      "image/png",
      "image/gif",
      "video/mp4",
      "audio/mpeg",
      "application/zip",
    ];

    if (!allowedTypes.includes(file.type)) {
      toast.error("File type not supported");
      return;
    }

    // Validate file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      toast.error("File size too large (max 10MB)");
      return;
    }

    // Update the parent component's state
    onChange(file);

    // If onUpload is provided, handle the upload
    if (onUpload) {
      setIsUploadingInModal(true);
      setUploadProgress(`Uploading ${file.name}...`);

      try {
        const result = await onUpload(file);
        setUploadResult(result);
        setUploadProgress("Upload successful!");
        toast.success("File uploaded successfully!");

        // Call the success callback with file details
        if (onUploadSuccess && result) {
          onUploadSuccess(result.file);
        }

        // Keep modal open for a moment to show success, then close
        setTimeout(() => {
          setIsOpen(false);
          setUploadResult(null);
          setUploadProgress("");
        }, 2000);
      } catch (error: any) {
        setUploadProgress("Upload failed!");
        toast.error(
          "Upload failed: " + (error.response?.data?.detail || error.message)
        );

        // Keep modal open for a moment to show error, then close
        setTimeout(() => {
          setIsOpen(false);
          setUploadResult(null);
          setUploadProgress("");
        }, 2000);
      } finally {
        setIsUploadingInModal(false);
      }
    } else {
      setIsOpen(false);
      toast.success("File selected successfully!");
    }
  };

  const handleModal = () => {
    setIsOpen(!isOpen);
  };

  const handleButtonClick = () => {
    setIsOpen(true); // Open modal instead of triggering file input directly
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  return (
    <div>
      <Button
        variant="outline"
        size="sm"
        onClick={handleButtonClick}
        disabled={isUploading}
      >
        {isUploading ? (
          <>
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-current"></div>
            Uploading...
          </>
        ) : (
          <>
            <Upload className="w-4 h-4" />
            {value ? value.name : label}
          </>
        )}
      </Button>

      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png,.gif,.mp4,.mp3,.zip"
        onChange={handleFileSelect}
        style={{ display: "none" }}
      />

      <Modal isOpen={isOpen} onClose={handleModal}>
        <div className="p-6">
          <h2 className="text-xl font-semibold mb-4">Upload File</h2>

          <div
            className="space-y-4"
            onClick={() => fileInputRef.current?.click()}
          >
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <Upload className="w-8 h-8 mx-auto mb-2 text-gray-400" />
              <p className="text-gray-600 mb-2">Click to select a file</p>
              <p className="text-sm text-gray-500">
                Supported formats: PDF, DOC, DOCX, TXT, JPG, PNG, GIF, MP4, MP3,
                ZIP
              </p>
              <p className="text-sm text-gray-500">Max size: 10MB</p>
            </div>
            <input
              type="file"
              name={name}
              accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png,.gif,.mp4,.mp3,.zip"
              onChange={handleFileSelect}
              className="w-full"
            />
          </div>
          {value && !isUploadingInModal && !uploadResult && (
            <div className="space-y-4">
              <div className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center space-x-3">
                  <File className="w-8 h-8 text-blue-500" />
                  <div className="flex-1">
                    <h3 className="font-medium text-gray-900">{value.name}</h3>
                    <p className="text-sm text-gray-500">
                      {value.type} • {formatFileSize(value.size)}
                    </p>
                  </div>
                </div>
              </div>
              <Button
                onClick={() => fileInputRef.current?.click()}
                className="w-full"
                disabled={isUploadingInModal}
              >
                {isUploadingInModal ? "Uploading..." : "Upload File"}
              </Button>
            </div>
          )}

          {isUploadingInModal && (
            <div className="space-y-4">
              <div className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center space-x-3">
                  <File className="w-8 h-8 text-blue-500" />
                  <div className="flex-1">
                    <h3 className="font-medium text-gray-900">{value?.name}</h3>
                    <p className="text-sm text-gray-500">
                      {value?.type} • {value ? formatFileSize(value.size) : ""}
                    </p>
                  </div>
                </div>
              </div>
              <div className="text-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2"></div>
                <p className="text-gray-600">{uploadProgress}</p>
              </div>
            </div>
          )}

          {uploadResult && (
            <div className="space-y-4">
              <div className="border border-green-200 rounded-lg p-4 bg-green-50">
                <div className="flex items-center space-x-3">
                  <CheckCircle className="w-8 h-8 text-green-500" />
                  <div className="flex-1">
                    <h3 className="font-medium text-green-900">
                      Upload Successful!
                    </h3>
                    <p className="text-sm text-green-600">{uploadProgress}</p>
                  </div>
                </div>
              </div>

              <div className="border border-gray-200 rounded-lg p-4">
                <h4 className="font-medium text-gray-900 mb-2">
                  File Details:
                </h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">File Name:</span>
                    <span className="text-gray-900">
                      {uploadResult.original_filename || value?.name}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">File Type:</span>
                    <span className="text-gray-900">
                      {uploadResult.file_type || value?.type}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">File Size:</span>
                    <span className="text-gray-900">
                      {uploadResult.file_size
                        ? formatFileSize(uploadResult.file_size)
                        : value
                        ? formatFileSize(value.size)
                        : ""}
                    </span>
                  </div>
                  {uploadResult.url && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">File URL:</span>
                      <span className="text-gray-900 text-xs truncate max-w-32">
                        {uploadResult.url}
                      </span>
                    </div>
                  )}
                  {uploadResult.id && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">File ID:</span>
                      <span className="text-gray-900">{uploadResult.id}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </Modal>
    </div>
  );
};

export default UploadFile;
