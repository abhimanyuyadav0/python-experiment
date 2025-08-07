'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { loginUser, signupUser } from '@/lib/api/services/userServices';

interface User {
  id: number;
  name: string;
  email: string;
  is_active: boolean;
  role: 'admin' | 'tenant' | 'user';
  created_at: string;
  updated_at: string;
}

interface TokenData {
  token: string;
  expiresAt: number;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (name: string, email: string, password: string, role?: 'admin' | 'tenant' | 'user') => Promise<void>;
  logout: () => void;
  isAdmin: () => boolean;
  isTenant: () => boolean;
  isUser: () => boolean;
  hasRole: (role: 'admin' | 'tenant' | 'user') => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Token management functions
  const saveToken = (token: string, expiresAt: number) => {
    const tokenData: TokenData = { token, expiresAt };
    localStorage.setItem('tokenData', JSON.stringify(tokenData));
    setToken(token);
  };

  const getToken = (): string | null => {
    const tokenDataStr = localStorage.getItem('tokenData');
    if (!tokenDataStr) return null;

    try {
      const tokenData: TokenData = JSON.parse(tokenDataStr);
      if (Date.now() > tokenData.expiresAt) {
        // Token expired
        localStorage.removeItem('tokenData');
        localStorage.removeItem('user');
        setToken(null);
        setUser(null);
        return null;
      }
      return tokenData.token;
    } catch (error) {
      console.error('Error parsing token data:', error);
      localStorage.removeItem('tokenData');
      return null;
    }
  };

  const clearToken = () => {
    localStorage.removeItem('tokenData');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
  };

  useEffect(() => {
    // Check if user is logged in on app start
    const currentToken = getToken();
    const userData = localStorage.getItem('user');
    
    if (currentToken && userData) {
      try {
        setUser(JSON.parse(userData));
        setToken(currentToken);
      } catch (error) {
        console.error('Error parsing user data:', error);
        clearToken();
      }
    }
    setIsLoading(false);
  }, []);

  // Check token expiration every minute
  useEffect(() => {
    const interval = setInterval(() => {
      const currentToken = getToken();
      if (!currentToken && user) {
        // Token expired, logout user
        clearToken();
      }
    }, 60000); // Check every minute

    return () => clearInterval(interval);
  }, [user]);

  const login = async (email: string, password: string) => {
    try {
      setIsLoading(true);
      const response = await loginUser({ email, password });
      
      if (response.data) {
        const { user: userData, token, expires_at } = response.data;
        setUser(userData);
        localStorage.setItem('user', JSON.stringify(userData));
        
        // Save token with expiration (convert seconds to milliseconds)
        const expiresAtMs = expires_at * 1000;
        saveToken(token, expiresAtMs);
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (name: string, email: string, password: string, role: 'admin' | 'tenant' | 'user' = 'user') => {
    try {
      setIsLoading(true);
      const response = await signupUser({
        name,
        email,
        password,
        is_active: true,
        role
      });
      
      if (response.data) {
        const userData = response.data;
        setUser(userData);
        localStorage.setItem('user', JSON.stringify(userData));
        
        // Generate a dummy token for signup (in real app, this would come from the backend)
        const dummyToken = `token_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        const expiresAt = Date.now() + (5 * 60 * 1000); // 5 minutes from now
        saveToken(dummyToken, expiresAt);
      }
    } catch (error) {
      console.error('Signup error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    clearToken();
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    token,
    login,
    signup,
    logout,
    isAdmin: () => user?.role === 'admin',
    isTenant: () => user?.role === 'tenant',
    isUser: () => user?.role === 'user',
    hasRole: (role) => user?.role === role,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 