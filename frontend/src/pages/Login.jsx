import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { loginUser } from "../services/api.js";

export default function Login() {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await loginUser(identifier, password);
      navigate("/dashboard");
      window.location.reload();
    } catch (err) {
      setError(err.response?.data?.detail || "Invalid login credentials.");
    } finally {
      setLoading(false);
    }
  };

  const prefill = (userType) => {
    if (userType === "admin") {
      setIdentifier("admin");
      setPassword("admin123");
    } else {
      setIdentifier("user");
      setPassword("user123");
    }
  };

  return (
    <main className="auth-page-container">
      <div className="auth-card">
        <div className="auth-card-header">
          <h2>🔐 Account Sign In</h2>
          <p>PublicHealth-AI Multi-Agent Access</p>
        </div>

        {error && <div className="auth-error-banner">{error}</div>}

        <form onSubmit={handleLogin} className="auth-form">
          <div className="form-group">
            <label>Username or Email</label>
            <input
              type="text"
              required
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              placeholder="e.g. user or researcher@publichealth.ai"
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>

          <button type="submit" className="btn-auth-primary" disabled={loading}>
            {loading ? "Authenticating…" : "Sign In"}
          </button>
        </form>

        <div className="demo-accounts-box">
          <span className="demo-title">Quick Demo Login:</span>
          <div className="demo-btn-group">
            <button className="btn-demo" onClick={() => prefill("user")}>
              👤 Demo User (user / user123)
            </button>
            <button className="btn-demo" onClick={() => prefill("admin")}>
              🔑 Admin User (admin / admin123)
            </button>
          </div>
        </div>

        <div className="auth-card-footer">
          <span>Don't have an account? </span>
          <Link to="/register">Create one here</Link>
        </div>
      </div>
    </main>
  );
}
