"use client";

import React from "react";
import { XIcon } from "lucide-react";

interface ModalProps {
  title?: string;
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
  showCloseIcon?: boolean;
  size?: "sm" | "md" | "lg" | "xl"; // optional sizing
}

const sizeClasses = {
  sm: "max-w-sm",
  md: "max-w-md",
  lg: "max-w-lg",
  xl: "max-w-2xl",
};

const Modal: React.FC<ModalProps> = ({
  title,
  isOpen,
  onClose,
  children,
  showCloseIcon = true,
  size = "md",
}) => {
  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40"
      style={{ backgroundColor: isOpen ? "rgba(0, 0, 0, 0.4)" : "transparent" }}
    >
      <div
        className={`bg-white p-6 rounded-lg shadow-lg w-full ${sizeClasses[size]}`}
      >
        {(title || showCloseIcon) && (
          <div className="flex justify-between items-center mb-4">
            {title && <h2 className="text-lg font-semibold">{title}</h2>}
            {showCloseIcon && (
              <button
                onClick={onClose}
                className="text-gray-500 cursor-pointer hover:text-gray-700"
              >
                <XIcon className="w-5 h-5" />
              </button>
            )}
          </div>
        )}
        <div>{children}</div>
      </div>
    </div>
  );
};

export default Modal;
