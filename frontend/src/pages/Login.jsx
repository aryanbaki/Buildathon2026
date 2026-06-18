import { Link, Navigate, useNavigate } from "react-router-dom";
import { useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";

const VALID_CODE = "248613";

export default function Login() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const [step, setStep] = useState("email");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  if (user) return <Navigate to="/dashboard" replace />;

  async function pause(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  async function handleEmail(event) {
    event.preventDefault();
    setError("");
    if (!email.includes("@")) {
      setError("Enter a valid fleet email.");
      return;
    }
    setLoading(true);
    await pause(350);
    setLoading(false);
    setStep("password");
  }

  async function handlePassword(event) {
    event.preventDefault();
    setError("");
    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }
    setLoading(true);
    await pause(350);
    setLoading(false);
    setStep("twofa");
  }

  async function handleCode(event) {
    event.preventDefault();
    setError("");
    setLoading(true);
    await pause(300);
    setLoading(false);
    if (code !== VALID_CODE) {
      setError("Wrong code. Demo code: 248613");
      return;
    }
    login({
      email,
      name: email.split("@")[0] || "Fleet Operator",
      avatar: (email[0] || "F").toUpperCase(),
      role: "fleet_admin",
    });
    navigate("/dashboard", { replace: true });
  }

  function demoLogin() {
    login({ email: "demo@fleetmind.ai", name: "Demo Operator", avatar: "D", role: "fleet_admin" });
    navigate("/dashboard", { replace: true });
  }

  return (
    <div className="auth-page">
      <Link to="/" className="brand-lockup auth-brand">
        <span className="brand-mark">FM</span>
        <span>
          <strong>FleetMind AI</strong>
          <small>Operator access</small>
        </span>
      </Link>

      <section className="auth-shell">
        <div className="auth-story">
          <span className="eyebrow">Protected command center</span>
          <h1>Sign in to review fleet documents, questions, and truck context.</h1>
          <p>
            Demo authentication keeps the buildathon flow fast while preserving
            the protected dashboard experience.
          </p>
          <div className="auth-metrics">
            <span><b>SQL</b> structured fleet records</span>
            <span><b>RAG</b> cited document answers</span>
            <span><b>Graph</b> truck-driver-trailer links</span>
          </div>
        </div>

        <div className="auth-card">
          <div className="step-bars" aria-hidden="true">
            {["email", "password", "twofa"].map((name, index) => (
              <span key={name} className={["email", "password", "twofa"].indexOf(step) >= index ? "active" : ""} />
            ))}
          </div>

          {step === "email" && (
            <form onSubmit={handleEmail}>
              <h2>Welcome back</h2>
              <p>Use the demo path or continue with an email.</p>
              <label>Email address</label>
              <input value={email} onChange={(e) => setEmail(e.target.value)} autoFocus type="email" placeholder="operator@fleet.com" />
              {error && <div className="form-error">{error}</div>}
              <button className="btn btn-primary auth-submit" disabled={loading}>{loading ? "Checking..." : "Continue"}</button>
              <button className="btn btn-muted auth-submit" type="button" onClick={demoLogin}>Use demo access</button>
            </form>
          )}

          {step === "password" && (
            <form onSubmit={handlePassword}>
              <h2>Verify password</h2>
              <p>Signing in as <strong>{email}</strong></p>
              <label>Password</label>
              <input value={password} onChange={(e) => setPassword(e.target.value)} autoFocus type="password" placeholder="Enter password" />
              {error && <div className="form-error">{error}</div>}
              <button className="btn btn-primary auth-submit" disabled={loading}>{loading ? "Verifying..." : "Sign in"}</button>
              <button className="link-button" type="button" onClick={() => setStep("email")}>Change email</button>
            </form>
          )}

          {step === "twofa" && (
            <form onSubmit={handleCode}>
              <h2>Two-step verification</h2>
              <p>Enter the buildathon demo code.</p>
              <label>Verification code</label>
              <input className="code-input" value={code} onChange={(e) => setCode(e.target.value.replace(/\D/g, "").slice(0, 6))} autoFocus inputMode="numeric" placeholder="248613" />
              <small>Demo code: 248613</small>
              {error && <div className="form-error">{error}</div>}
              <button className="btn btn-primary auth-submit" disabled={loading || code.length < 6}>{loading ? "Verifying..." : "Open dashboard"}</button>
              <button className="link-button" type="button" onClick={() => setStep("password")}>Back</button>
            </form>
          )}
        </div>
      </section>
    </div>
  );
}
