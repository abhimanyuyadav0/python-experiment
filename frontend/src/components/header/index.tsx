import { useAuth } from "@/contexts/AuthContext";
import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import TokenExpirationCountdown from "../TokenExpirationCountdown";

const Header = ({ role }: { role: "admin" | "tenant" | "user" }) => {
  const { user, logout } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const handleLogout = () => {
    logout();
  };

  return (
    <div>
      <div className="sticky top-0 z-10 flex-shrink-0 flex h-16 bg-white shadow">
        {role === "admin" && (
          <div className="flex-1 px-4 flex justify-between">
            <div className="flex-1 flex items-center">
              <h1 className="text-2xl font-semibold text-gray-900">
                Admin Portal
              </h1>
            </div>
            <div className="ml-4 flex items-center md:ml-6 space-x-4">
              <TokenExpirationCountdown />
              <div className="relative">
                <button
                  onClick={handleLogout}
                  className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
                >
                  Sign out
                </button>
              </div>
            </div>
          </div>
        )}
        {role === "tenant" && (
          <div className="flex-1 px-4 flex justify-between">
            <div className="flex-1 flex items-center">
              <Link
                href={`/${role}`}
                className="text-xl font-bold text-green-600"
              >
                Tenant Portal
              </Link>
            </div>
            <div className="ml-4 flex items-center md:ml-6 space-x-4">
              <TokenExpirationCountdown />
              <div className="relative">
                <button
                  onClick={handleLogout}
                  className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
                >
                  Sign out
                </button>
              </div>
            </div>
          </div>
        )}
        {role === "user" && (
          <>
            <div className="flex-1 px-4 flex justify-between">
              <div className="flex-1 flex items-center">
                <Link
                  href={`/${role}`}
                  className="text-xl font-bold text-green-600"
                >
                  User Portal
                </Link>
                <div className="flex">
                  <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                    <Link
                      href={`/${role}`}
                      className="border-green-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                    >
                      Overview
                    </Link>
                    <Link
                      href={`/${role}/users`}
                      className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                    >
                      Users
                    </Link>
                    <Link
                      href={`/${role}/settings`}
                      className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                    >
                      Settings
                    </Link>
                  </div>
                </div>
              </div>
            </div>
            <div className="ml-4 flex items-center md:ml-6 space-x-4">
              <TokenExpirationCountdown />
              <div className="relative">
                <button
                  onClick={handleLogout}
                  className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
                >
                  Sign out
                </button>
              </div>
            </div>
          </>
        )}
      </div>
      <nav className="bg-white shadow-sm">
        {/* Mobile menu */}
        {isMenuOpen && (
          <div className="sm:hidden">
            <div className="pt-2 pb-3 space-y-1">
              <Link
                href={`/${role}`}
                className="bg-green-50 border-green-500 text-green-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
              >
                Overview
              </Link>
              <Link
                href={`/${role}/users`}
                className="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
              >
                Users
              </Link>
              <Link
                href={`/${role}/settings`}
                className="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
              >
                Settings
              </Link>
            </div>
            <div className="pt-4 pb-3 border-t border-gray-200">
              <div className="flex items-center px-4">
                <div className="flex-shrink-0">
                  <div className="h-10 w-10 rounded-full bg-green-600 flex items-center justify-center">
                    <span className="text-white text-sm font-medium">
                      {user?.name?.charAt(0).toUpperCase()}
                    </span>
                  </div>
                </div>
                <div className="ml-3">
                  <div className="text-base font-medium text-gray-800">
                    {user?.name}
                  </div>
                  <div className="text-sm font-medium text-gray-500">
                    {user?.email}
                  </div>
                </div>
              </div>
              <div className="mt-3 space-y-1">
                <button
                  onClick={handleLogout}
                  className="block w-full text-left px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
                >
                  Sign out
                </button>
              </div>
            </div>
          </div>
        )}
      </nav>
    </div>
  );
};

export default Header;
