import axois from "axios";
import { refreshToken as refreshTokenApi } from "./services/userServices";

const axoisInstance = axois.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
  headers: {
    "centent-Type": "application/json",
  },
});

axoisInstance.interceptors.request.use(
  (config) => {
    const tokenDataStr = typeof window !== "undefined" ? localStorage.getItem("tokenData") : null;
    if (tokenDataStr) {
      try {
        const tokenData = JSON.parse(tokenDataStr);
        if (Date.now() <= tokenData.expiresAt) {
          config.headers.Authorization = `Bearer ${tokenData.token}`;
        }
      } catch (error) {
        console.error('Error parsing token data:', error);
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

let isRefreshing = false;
let failedQueue: any[] = [];

function processQueue(error: any, token: string | null = null) {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
}

axoisInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise(function (resolve, reject) {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers["Authorization"] = "Bearer " + token;
            return axoisInstance(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }
      originalRequest._retry = true;
      isRefreshing = true;
      // Token expired, redirect to login
      localStorage.removeItem("tokenData");
      localStorage.removeItem("user");
      window.location.href = "/auth/login";
      return Promise.reject(error);
    }
    return Promise.reject(error);
  }
);

export default axoisInstance;
