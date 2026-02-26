import axios from "axios";

/**
 * Central Axios instance for DeepTrace frontend
 * Handles Dev vs Production automatically
 */

const BACKEND_URL =
  import.meta.env.MODE === "development"
    ? "http://localhost:5000"
    : "/api";  // In production, Vercel rewrite handles this

const api = axios.create({
  baseURL: BACKEND_URL,
  timeout: 30000,
  headers: {
    Accept: "application/json",
  },
});

/* Optional: Global error interceptor for debugging */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error?.response || error);
    return Promise.reject(error);
  }
);

export default api;