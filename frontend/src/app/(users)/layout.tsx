'use client';

import { useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import RoleProtectedRoute from '@/components/RoleProtectedRoute';
import Header from '@/components/header';

export default function UserLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isAuthenticated, logout } = useAuth();

  useEffect(() => {
    if (!isAuthenticated) {
      logout();
    }
  }, [isAuthenticated]);

  return (
    <RoleProtectedRoute requiredRole={['admin', 'tenant', 'user']} fallbackPath="/user">
      <div className="min-h-screen bg-gray-100">
        {/* Navigation */}
        <Header role="user" />

        {/* Main content */}
        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          {children}
        </main>
      </div>
    </RoleProtectedRoute>
  );
} 