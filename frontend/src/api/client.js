import axios from "axios";

// Points at the backend built earlier (uvicorn main:app --reload runs on 8000 by default).
// Override via a .env file if your backend runs somewhere else - see .env.example.
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const apiClient = axios.create({
  baseURL: BASE_URL,
});

// Attach the JWT to every request automatically, once the user is logged in.
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
