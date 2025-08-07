"use client";

import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import { jwtDecode } from "jwt-decode";
import { loginUser, signupUser } from "@/lib/api/services/userServices";
import { validateAndCleanToken } from "@/utils/tokenUtils";

interface JWTPayload {
  exp?: number;
  [key: string]: any;
}

interface User {
  id: number;
  name: string;
  email: string;
  is_active: boolean;
  role: "admin" | "tenant" | "user";
  created_at: string;
  updated_at: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (
    name: string,
    email: string,
    password: string,
    role?: "admin" | "tenant" | "user"
  ) => Promise<void>;
  logout: () => void;
  isAdmin: () => boolean;
  isTenant: () => boolean;
  isUser: () => boolean;
  hasRole: (role: "admin" | "tenant" | "user") => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  const saveToStorage = (token: string, userData: User) => {
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(userData));
    setToken(token);
    setUser(userData);
  };

  const clearStorage = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setToken(null);
    setUser(null);
  };

  const getTokenFromStorage = (): string | null => {
    return localStorage.getItem("token");
  };

  const getUserFromStorage = (): User | null => {
    const userStr = localStorage.getItem("user");
    try {
      return userStr ? JSON.parse(userStr) : null;
    } catch (error) {
      console.error("AuthContext: Error parsing user from storage", error);
      return null;
    }
  };

  useEffect(() => {
    const initAuth = () => {
      const storedToken = getTokenFromStorage();
      const { valid } = validateAndCleanToken(storedToken);
      const storedUser = getUserFromStorage();

      if (valid && storedUser) {
        setToken(storedToken);
        setUser(storedUser);
      } else {
        clearStorage();
      }

      setIsLoading(false);
    };

    initAuth();
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      if (!token) return;

      try {
        const decoded: JWTPayload = jwtDecode(token);
        const currentTime = Date.now() / 1000;
        if (decoded.exp && decoded.exp < currentTime) {
          console.warn("Token expired → Logging out");
          logout();
        }
      } catch (error) {
        console.error("Invalid token → Logging out", error);
        logout();
      }
    }, 60_000); // every minute

    return () => clearInterval(interval);
  }, [token]);

  const redirectToDashboard = (role: User["role"]) => {
    const routes = {
      admin: "/admin/dashboard",
      tenant: "/tenant",
      user: "/user",
    };
    router.push(routes[role]);
  };

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const response = await loginUser({ email, password });
      const { user: userData, token } = response.data;

      saveToStorage(token, userData);

      redirectToDashboard(userData.role);
    } catch (error) {
      console.error("Login failed:", error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (
    name: string,
    email: string,
    password: string,
    role: "admin" | "tenant" | "user" = "user"
  ) => {
    setIsLoading(true);
    try {
      const response = await signupUser({
        name,
        email,
        password,
        role,
        is_active: true,
      });

      if (response.status === 201) {
        router.push("/auth/login");
      } else {
        throw new Error("Signup failed");
      }
    } catch (error) {
      console.error("Signup failed:", error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    clearStorage();
    router.push("/auth/login");
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    token,
    login,
    signup,
    logout,
    isAdmin: () => user?.role === "admin",
    isTenant: () => user?.role === "tenant",
    isUser: () => user?.role === "user",
    hasRole: (role) => user?.role === role,
  };

  return (
    <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
  );
};
