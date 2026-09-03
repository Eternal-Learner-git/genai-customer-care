import React, { createContext, useContext, useState, useEffect } from "react";
import apiClient from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // On first load, if a token is already saved, try to fetch the current user
  // so a page refresh doesn't log the person out.
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setLoading(false);
      return;
    }
    apiClient
      .get("/me")
      .then((res) => setUser(res.data))
      .catch(() => {
        localStorage.removeItem("access_token");
      })
      .finally(() => setLoading(false));
  }, []);

  async function login(email, password) {
    // The backend's /token endpoint expects OAuth2 form data, not JSON -
    // this is a FastAPI/OAuth2PasswordRequestForm convention (username = email here).
    const form = new URLSearchParams();
    form.append("username", email);
    form.append("password", password);

    const res = await apiClient.post("/token", form, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    localStorage.setItem("access_token", res.data.access_token);
    const meRes = await apiClient.get("/me");
    setUser(meRes.data);
    return meRes.data;
  }

  async function register(name, email, password) {
    await apiClient.post("/register", { name, email, password });
    // Registering doesn't log the user in automatically on the backend,
    // so we chain straight into login for a smoother experience.
    return login(email, password);
  }

  function logout() {
    localStorage.removeItem("access_token");
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
