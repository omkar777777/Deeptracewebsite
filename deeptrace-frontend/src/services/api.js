import axios from "axios";

/**
 * Central Axios instance for DeepTrace frontend
 * Used by cryptoService, stegoService, watermarkService, etc.
 */

const BACKEND_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000/api";

const api = axios.create({
  baseURL: BACKEND_URL,
  timeout: 30000,
  headers: {
    "Accept": "application/json"
  }
});

/* Optional: Global error interceptor for debugging */
api.interceptors.response.use(
  response => response,
  error => {
    console.error("API Error:", error?.response || error);
    return Promise.reject(error);
  }
);

export default api;