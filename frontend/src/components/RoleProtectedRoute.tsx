'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';

interface RoleProtectedRouteProps {
  children: React.ReactNode;
  requiredRole: 'admin' | 'tenant' | 'user' | ('admin' | 'tenant' | 'user')[];
  fallbackPath?: string;
}

export default function RoleProtectedRoute({ 
  children, 
  requiredRole, 
  fallbackPath = '/dashboard' 
}: RoleProtectedRouteProps) {
  const { isAuthenticated, isLoading, hasRole, isAdmin, isTenant, isUser } = useAuth();
  const router = useRouter();

  const hasRequiredRole = () => {
    if (Array.isArray(requiredRole)) {
      return requiredRole.some(role => hasRole(role));
    }
    return hasRole(requiredRole);
  };

  useEffect(() => {
    if (!isLoading && (!isAuthenticated || !hasRequiredRole())) {
      router.push(fallbackPath);
    }
  }, [isAuthenticated, isLoading, hasRequiredRole, requiredRole, router, fallbackPath]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (!isAuthenticated || !hasRequiredRole()) {
    return null;
  }

  return <>{children}</>;
} 