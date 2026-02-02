import axios from "axios";

/**
 * Central Axios instance for DeepTrace frontend
 * Used by cryptoService, stegoService, watermarkService, etc.
 */
const api = axios.create({
  baseURL: "http://127.0.0.1:5000/api", // Flask backend
  timeout: 30000,
  headers: {
    "Accept": "application/json"
  }
});

export default api;