import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach Authorization header if JWT token exists
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("ph_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export async function checkHealth() {
  const resp = await api.get("/health");
  return resp.data;
}

export async function loginUser(usernameOrEmail, password) {
  const resp = await api.post("/api/auth/login", {
    username_or_email: usernameOrEmail,
    password,
  });
  if (resp.data?.access_token) {
    localStorage.setItem("ph_token", resp.data.access_token);
    localStorage.setItem("ph_user", JSON.stringify(resp.data.user));
  }
  return resp.data;
}

export async function registerUser(userData) {
  const resp = await api.post("/api/auth/register", userData);
  if (resp.data?.access_token) {
    localStorage.setItem("ph_token", resp.data.access_token);
    localStorage.setItem("ph_user", JSON.stringify(resp.data.user));
  }
  return resp.data;
}

export async function getMe() {
  const resp = await api.get("/api/auth/me");
  return resp.data;
}

export function logoutUser() {
  localStorage.removeItem("ph_token");
  localStorage.removeItem("ph_user");
}

export function getCurrentUser() {
  const userStr = localStorage.getItem("ph_user");
  if (!userStr) return null;
  try {
    return JSON.parse(userStr);
  } catch {
    return null;
  }
}

export async function processQuery(queryText) {
  const resp = await api.post("/api/query", { query: queryText });
  return resp.data;
}

export default api;
