"use client";

import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { loginUser, signupUser } from "@/lib/api/services/userServices";
import { useRouter } from "next/navigation";

interface User {
  id: number;
  name: string;
  email: string;
  is_active: boolean;
  role: "admin" | "tenant" | "user";
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
  if (context === undefined) {
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

  // Token management functions
  const saveToken = (token: string, expiresAt: number) => {
    const tokenData: TokenData = { token, expiresAt };
    const tokenDataString = JSON.stringify(tokenData);
    localStorage.setItem("tokenData", tokenDataString);
    setToken(token);
    console.log("AuthContext: Token saved", { token: token.substring(0, 20) + "...", expiresAt });
  };

  const getToken = (): string | null => {
    const tokenDataStr = localStorage.getItem("tokenData");
    if (!tokenDataStr) {
      console.log("AuthContext: No token data found");
      return null;
    }

    try {
      const tokenData: TokenData = JSON.parse(tokenDataStr);
      const now = Date.now();
      const isExpired = now >= tokenData.expiresAt;

      console.log("AuthContext: Token check", {
        now,
        expiresAt: tokenData.expiresAt,
        timeLeft: tokenData.expiresAt - now,
        isExpired
      });

      if (isExpired) {
        console.log("AuthContext: Token expired");
        localStorage.removeItem("tokenData");
        localStorage.removeItem("user");
        return null;
      }
      console.log("AuthContext: Token retrieved successfully");
      return tokenData.token;
    } catch (error) {
      console.error("AuthContext: Error parsing token data:", error);
      localStorage.removeItem("tokenData");
      return null;
    }
  };

  const clearToken = () => {
    localStorage.removeItem("tokenData");
    localStorage.removeItem("user");
    setToken(null);
    setUser(null);
    router.push("/auth/login");
  };

  useEffect(() => {
    // Check if user is logged in on app start
    console.log("AuthContext: Initializing on app start");
    const currentToken = getToken();
    const userData = localStorage.getItem("user");
    if (currentToken && userData) {
      try {
        const parsedUser = JSON.parse(userData);
        setUser(parsedUser);
        setToken(currentToken);
        console.log("AuthContext: User restored from localStorage");
      } catch (error) {
        console.error("AuthContext: Error parsing user data:", error);
        clearToken();
      }
    } else {
      console.log("AuthContext: No valid token or user data found");
    }
    setIsLoading(false);
  }, []);

  // Check token expiration every minute
  useEffect(() => {
    const interval = setInterval(() => {
      const currentToken = getToken();
      if (!currentToken && user) {
        // Token expired but user state still exists, clear everything
        clearToken();
      }
    }, 60000); // Check every minute

    return () => clearInterval(interval);
  }, [user]);

  const redirectToDashboard = (role: "admin" | "tenant" | "user") => {
    if (role === "admin") {
      router.push("/admin/dashboard");
    } else if (role === "tenant") {
      router.push("/tenant");
    } else if (role === "user") {
      router.push("/user");
    }
  };
  const login = async (email: string, password: string) => {
    try {
      setIsLoading(true);
      const response = await loginUser({ email, password });

      if (response.data) {
        const { user: userData, token, expires_at } = response.data;
        console.log("AuthContext: Login successful", {
          userData,
          token: token ? token.substring(0, 20) + "..." : "null",
          expires_at,
        });

        setUser(userData);
        localStorage.setItem("user", JSON.stringify(userData));

        // Save token with expiration (expires_at is already in milliseconds)
        saveToken(token, expires_at);
        redirectToDashboard(userData.role);
      }
    } catch (error) {
      console.error("AuthContext: Login error:", error);
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
    try {
      setIsLoading(true);
      const response = await signupUser({
        name,
        email,
        password,
        is_active: true,
        role,
      });
      if (response.status === 201) {
        router.push("/auth/login");
      } else {
        throw new Error("Signup failed");
      }
    } catch (error) {
      console.error("Signup error:", error);
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
    isAdmin: () => user?.role === "admin",
    isTenant: () => user?.role === "tenant",
    isUser: () => user?.role === "user",
    hasRole: (role) => user?.role === role,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
