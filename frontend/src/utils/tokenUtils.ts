// lib/auth/tokenUtils.ts
import { jwtDecode } from "jwt-decode";

interface JWTPayload {
  exp?: number;
  [key: string]: any;
}

/**
 * Validates the given token.
 * Returns:
 *   - { valid: true, decoded } if token is valid and not expired.
 *   - { valid: false } if token is invalid or expired (and clears storage+cookies).
 */
export const validateAndCleanToken = (
  token: string | null
): { valid: boolean; decoded?: JWTPayload } => {
  if (!token) {
    clearAuthStorage();
    return { valid: false };
  }

  try {
    const decoded: JWTPayload = jwtDecode(token);
    const now = Date.now() / 1000;

    if (decoded.exp && decoded.exp < now) {
      clearAuthStorage();
      return { valid: false };
    }

    return { valid: true, decoded };
  } catch (err) {
    console.error("validateAndCleanToken → invalid token, clearing auth data");
    clearAuthStorage();
    return { valid: false };
  }
};

export const clearAuthStorage = () => {
  localStorage.removeItem("loggedUser");
  localStorage.removeItem("token");
  document.cookie = "token=; path=/; max-age=0";
};
