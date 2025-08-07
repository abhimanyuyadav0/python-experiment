'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import RoleProtectedRoute from '@/components/RoleProtectedRoute';
import Header from '@/components/header';

export default function TenantLayout({
  children,
}: {
  children: React.ReactNode;
}) {

  return (
    <RoleProtectedRoute requiredRole={['admin', 'tenant']} fallbackPath="/auth/login">
      <div className="min-h-screen bg-gray-100">
        {/* Navigation */}
        <Header role="tenant" />

        {/* Main content */}
        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          {children}
        </main>
      </div>
    </RoleProtectedRoute>
  );
} 