import React, { useRef, useState } from "react";
import Modal from "../modal";
import Button from "../button";
import { PlusIcon } from "lucide-react";
import { toast } from "react-toastify";
import { FileResponse, uploadFile } from "@/lib/api/services/fileServices";
import { AxiosResponse } from "axios";

interface UploadFileProps {
  label: string;
  name: string;
  type: string;
  placeholder: string;
  value: FileResponse | null;
  onChange: (file: FileResponse) => void;
}

const UploadFile = ({
  label,
  name,
  type,
  placeholder,
  value,
  onChange,
}: UploadFileProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileSelect = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    console.log("CreateDataPage: File selected:", {
      name: file.name,
      type: file.type,
      size: file.size,
    });

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
      return;
    }

    // Validate file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      return;
    }

    setIsUploading(true);

    try {
      toast.info("Starting file upload");
      const response: AxiosResponse<{ data: FileResponse }> = await uploadFile(
        file
      );
      alert(response.data.data);
      onChange(response.data.data);
      setIsOpen(false);
      toast.success("Upload successful!");
    } catch (error: any) {
      toast.error("Upload error:", error);
    } finally {
      setIsUploading(false);
    }
  };
  const handleModal = () => {
    setIsOpen(!isOpen);
  };
  return (
    <div>
      <Button variant="outline" size="sm" onClick={handleModal}>
        <PlusIcon />
        {label}
      </Button>
      <Modal isOpen={isOpen} onClose={handleModal}>
        <div>
          <h1>Upload File</h1>
        </div>
        <div>
          <input
            type="file"
            accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png,.gif,.mp4,.mp3,.zip"
            onChange={handleFileSelect}
          />
        </div>
      </Modal>
    </div>
  );
};

export default UploadFile;
