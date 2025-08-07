import React from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  className?: string;
  variant?: "primary" | "secondary" | "outline" | "ghost" | "link";
  size?: "xs" | "sm" | "md" | "lg";
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  type?: "button" | "submit" | "reset";
  icon?: React.ReactNode;
}

const Button = ({ children, ...props }: ButtonProps) => {
  const {
    className,
    variant = "primary",
    size = "sm",
    disabled,
    loading,
    onClick,
    type,
    icon,
    ...rest
  } = props;
  const getVariant = () => {
    switch (variant) {
      case "primary":
        return "bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white";
      case "secondary":
        return "bg-gray-200 text-gray-800";
      case "outline":
        return "bg-transparent border border-primary text-primary";
      case "ghost":
        return "bg-transparent text-primary";
      case "link":
        return "bg-transparent text-primary";
      default:
        return "bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white";
    }
  };
  const getSize = () => {
    switch (size) {
      case "xs":
        return "text-xs py-1 px-2";
      case "sm":
        return "text-sm py-1 px-2";
      case "md":
        return "text-md py-1 px-3";
      case "lg":
        return "text-md py-2 px-4";
      default:
          return "text-xs py-1 px-2";
    }
  };
  return (
    <button
      {...rest}
      className={` ${getVariant()} ${getSize()} rounded-md flex items-center gap-2 ${
        disabled ? "opacity-50 cursor-not-allowed" : ""
      } ${loading ? "opacity-50 cursor-not-allowed" : ""} ${className}`}
    >
      {children}
    </button>
  );
};

export default Button;
