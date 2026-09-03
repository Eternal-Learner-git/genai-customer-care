import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <header className="border-b border-teal-100 bg-white">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <Link to="/" className="font-display text-xl text-teal-700">
          Care Desk
        </Link>

        {user && (
          <nav className="flex items-center gap-6 text-sm">
            <Link to="/" className="text-ink/70 hover:text-teal-600">
              My complaints
            </Link>
            {user.role === "admin" && (
              <Link to="/admin" className="text-ink/70 hover:text-teal-600">
                Admin dashboard
              </Link>
            )}
            <span className="text-ink/40">|</span>
            <span className="text-ink/60">{user.name}</span>
            <button
              onClick={handleLogout}
              className="rounded-md border border-teal-200 px-3 py-1.5 text-teal-700 hover:bg-teal-50"
            >
              Log out
            </button>
          </nav>
        )}
      </div>
    </header>
  );
}
