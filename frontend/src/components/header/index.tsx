import { useAuth } from "@/contexts/AuthContext";
import React, { useState } from "react";
import Link from "next/link";
import TokenExpirationCountdown from "../TokenExpirationCountdown";

const Header = ({ role }: { role: "admin" | "tenant" | "user" }) => {
  const { user, logout } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
  };

  const userIcon = (
    <div className="ml-3 relative">
      <button
        onClick={() => setIsMenuOpen(!isMenuOpen)}
        className="max-w-xs bg-white flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
      >
        <span className="sr-only">Open user menu</span>
        <div className="h-8 w-8 rounded-full bg-green-600 flex items-center justify-center">
          <span className="text-white text-sm font-medium">
            {user?.name?.charAt(0).toUpperCase()}
          </span>
        </div>
      </button>
      {isMenuOpen && (
        <div className="sm:hidden absolute right-0 mt-2 w-48 bg-white shadow-lg rounded-md py-2 z-50">
          <Link
            href={`/${role}`}
            className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            Overview
          </Link>
          <Link
            href={`/${role}/users`}
            className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            Users
          </Link>
          <Link
            href={`/${role}/settings`}
            className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            Settings
          </Link>
          <button
            onClick={handleLogout}
            className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            Sign out
          </button>
        </div>
      )}
    </div>
  );

  const roleTitleMap = {
    admin: "Admin Portal",
    tenant: "Tenant Portal",
    user: "User Portal",
  };

  return (
    <div className="sticky top-0 z-10 flex-shrink-0 flex h-16 bg-white shadow">
      <div className="flex-1 px-4 flex justify-between items-center">
        <div className="flex items-center space-x-6">
          {role !== "admin" ? (
            <Link href={`/${role}`} className="text-xl font-bold text-green-600">
              {roleTitleMap[role]}
            </Link>
          ) : (
            <h1 className="text-2xl font-semibold text-gray-900">
              {roleTitleMap[role]}
            </h1>
          )}

          {role === "user" && (
            <div className="hidden sm:flex space-x-6">
              <Link
                href={`/${role}`}
                className="border-green-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              >
                Overview
              </Link>
              <Link
                href={`/${role}/users`}
                className="text-gray-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 text-sm font-medium"
              >
                Users
              </Link>
              <Link
                href={`/${role}/settings`}
                className="text-gray-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 text-sm font-medium"
              >
                Settings
              </Link>
            </div>
          )}
        </div>

        <div className="flex items-center space-x-4">
          <TokenExpirationCountdown />
          <button
            onClick={handleLogout}
            className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
          >
            Sign out
          </button>
          {userIcon}
        </div>
      </div>
    </div>
  );
};

export default Header;
