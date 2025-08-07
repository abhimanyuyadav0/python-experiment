import axois from "axios";

const axoisInstance = axois.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

axoisInstance.interceptors.request.use(
  (config) => {
    const tokenDataStr = typeof window !== "undefined" ? localStorage.getItem("tokenData") : null;
    if (tokenDataStr) {
      try {
        const tokenData = JSON.parse(tokenDataStr);
        const now = Date.now();
        console.log("Axios interceptor: Token check", {
          now,
          expiresAt: tokenData.expiresAt,
          timeLeft: tokenData.expiresAt - now,
          isExpired: false
        });
        
        if (now >= tokenData.expiresAt) {
          config.headers.Authorization = `Bearer ${tokenData.token}`;
          console.log("Axios interceptor: Added Authorization header");
        } else {
          console.log("Axios interceptor: Token expired, not adding header");
        }
      } catch (error) {
        console.error('Error parsing token data:', error);
      }
    } else {
      console.log("Axios interceptor: No token data found");
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default axoisInstance;
