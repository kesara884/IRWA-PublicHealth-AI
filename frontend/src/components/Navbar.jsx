import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { checkHealth, getCurrentUser, logoutUser } from "../services/api";

export default function Navbar() {
  const [user, setUser] = useState(getCurrentUser());
  const [backendStatus, setBackendStatus] = useState("checking");
  const navigate = useNavigate();

  useEffect(() => {
    let mounted = true;
    checkHealth()
      .then((data) => {
        if (mounted) setBackendStatus(data.status === "ok" ? "online" : "degraded");
      })
      .catch(() => {
        if (mounted) setBackendStatus("offline");
      });

    return () => {
      mounted = false;
    };
  }, []);

  const handleLogout = () => {
    logoutUser();
    setUser(null);
    navigate("/login");
  };

  return (
    <header className="navbar-container">
      <div className="navbar-left">
        <Link to="/" className="navbar-brand">
          <span className="brand-logo">🛡️</span>
          <span className="brand-title">PublicHealth-AI</span>
          <span className="brand-badge">Multi-Agent RAG</span>
        </Link>
      </div>

      <div className="navbar-center">
        <div className={`status-indicator status-${backendStatus}`}>
          <span className="status-dot"></span>
          <span className="status-label">
            Backend: {backendStatus === "online" ? "Connected (Port 8000)" : backendStatus}
          </span>
        </div>
      </div>

      <div className="navbar-right">
        {user ? (
          <div className="user-profile-badge">
            <div className="user-avatar">{user.username.charAt(0).toUpperCase()}</div>
            <div className="user-info">
              <span className="user-name">{user.full_name || user.username}</span>
              <span className="user-role-tag">{user.role}</span>
            </div>
            <button className="btn-logout" onClick={handleLogout} title="Sign Out">
              Logout
            </button>
          </div>
        ) : (
          <div className="auth-nav-buttons">
            <Link to="/login" className="btn-nav btn-secondary">
              Login
            </Link>
            <Link to="/register" className="btn-nav btn-primary">
              Register
            </Link>
          </div>
        )}
      </div>
    </header>
  );
}
