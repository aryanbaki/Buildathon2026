import { useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";

const MOCK_USERS = {
  "yeshsalapu2@gmail.com": { name: "Yesh Salapu", avatar: "YS", role: "fleet_admin" },
  "demo@fleetai.com":      { name: "Fleet Demo",  avatar: "FD", role: "dispatcher" },
};

const VALID_CODE = "248613";

export default function LoginModal() {
  const { login } = useAuth();
  const [step, setStep]       = useState("email");   // email | password | twofa
  const [email, setEmail]     = useState("");
  const [password, setPass]   = useState("");
  const [code, setCode]       = useState("");
  const [error, setError]     = useState("");
  const [loading, setLoading] = useState(false);

  async function handleEmail(e) {
    e.preventDefault();
    setError("");
    if (!email.includes("@")) { setError("Enter a valid email."); return; }
    setLoading(true);
    await new Promise(r => setTimeout(r, 800));
    setLoading(false);
    setStep("password");
  }

  async function handlePassword(e) {
    e.preventDefault();
    setError("");
    if (password.length < 6) { setError("Password must be at least 6 characters."); return; }
    setLoading(true);
    await new Promise(r => setTimeout(r, 1000));
    setLoading(false);
    setStep("twofa");
  }

  async function handleTwoFA(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    await new Promise(r => setTimeout(r, 700));
    setLoading(false);
    if (code !== VALID_CODE) { setError("Incorrect code. Try 248613 for demo."); return; }
    const profile = MOCK_USERS[email] || { name: email.split("@")[0], avatar: email[0].toUpperCase(), role: "dispatcher" };
    login({ email, ...profile });
  }

  function handleGoogle() {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      login({ email: "google@fleetai.com", name: "Google User", avatar: "G", role: "fleet_admin" });
    }, 1400);
  }

  return (
    <div style={{
      position: "fixed", inset: 0, background: "rgba(0,0,0,.55)",
      display: "flex", alignItems: "center", justifyContent: "center",
      zIndex: 1000, padding: 20,
    }}>
      <div style={{
        background: "#fff", borderRadius: 16, width: "100%", maxWidth: 400,
        boxShadow: "0 24px 60px rgba(0,0,0,.2)", overflow: "hidden",
      }}>
        {/* Header */}
        <div style={{ background: "#1A1A2E", padding: "28px 32px 24px", textAlign: "center" }}>
          <div style={{ fontSize: 28, marginBottom: 8 }}>🚛</div>
          <div style={{ color: "#fff", fontSize: 18, fontWeight: 600 }}>Fleet Document Intelligence</div>
          <div style={{ color: "#9898B0", fontSize: 13, marginTop: 4 }}>Sign in to your account</div>
        </div>

        <div style={{ padding: "28px 32px" }}>
          {/* Step indicators */}
          <div style={{ display: "flex", gap: 6, marginBottom: 24 }}>
            {["email","password","twofa"].map((s, i) => (
              <div key={s} style={{
                flex: 1, height: 3, borderRadius: 99,
                background: ["email","password","twofa"].indexOf(step) >= i ? "#F4A622" : "#E4E2D9",
                transition: "background .3s",
              }} />
            ))}
          </div>

          {/* Step: Email */}
          {step === "email" && (
            <form onSubmit={handleEmail}>
              <div style={{ marginBottom: 16 }}>
                <label style={labelStyle}>Email address</label>
                <input
                  type="email" value={email}
                  onChange={e => setEmail(e.target.value)}
                  placeholder="you@company.com"
                  autoFocus style={inputStyle}
                />
              </div>
              {error && <div style={errorStyle}>{error}</div>}
              <button type="submit" disabled={loading} style={btnPrimary}>
                {loading ? "Checking…" : "Continue →"}
              </button>

              <div style={{ display: "flex", alignItems: "center", gap: 10, margin: "20px 0" }}>
                <div style={{ flex: 1, height: 1, background: "#E4E2D9" }} />
                <span style={{ fontSize: 12, color: "#9C9890" }}>or</span>
                <div style={{ flex: 1, height: 1, background: "#E4E2D9" }} />
              </div>

              <button type="button" onClick={handleGoogle} disabled={loading} style={btnGoogle}>
                <GoogleIcon /> Sign in with Google
              </button>
            </form>
          )}

          {/* Step: Password */}
          {step === "password" && (
            <form onSubmit={handlePassword}>
              <div style={{ marginBottom: 6, fontSize: 13, color: "#6B6965" }}>
                Signing in as <strong style={{ color: "#1C1C1E" }}>{email}</strong>
              </div>
              <button type="button" onClick={() => setStep("email")} style={backBtn}>← Change email</button>
              <div style={{ marginBottom: 16, marginTop: 16 }}>
                <label style={labelStyle}>Password</label>
                <input
                  type="password" value={password}
                  onChange={e => setPass(e.target.value)}
                  placeholder="Enter your password"
                  autoFocus style={inputStyle}
                />
              </div>
              {error && <div style={errorStyle}>{error}</div>}
              <button type="submit" disabled={loading} style={btnPrimary}>
                {loading ? "Verifying…" : "Sign in →"}
              </button>
            </form>
          )}

          {/* Step: 2FA */}
          {step === "twofa" && (
            <form onSubmit={handleTwoFA}>
              <div style={{ textAlign: "center", marginBottom: 20 }}>
                <div style={{ fontSize: 32, marginBottom: 8 }}>🔐</div>
                <div style={{ fontSize: 15, fontWeight: 600, marginBottom: 4 }}>Two-step verification</div>
                <div style={{ fontSize: 13, color: "#6B6965" }}>
                  Enter the 6-digit code sent to your authenticator app or SMS.
                </div>
              </div>
              <div style={{ marginBottom: 16 }}>
                <label style={labelStyle}>Verification code</label>
                <input
                  type="text" value={code}
                  onChange={e => setCode(e.target.value.replace(/\D/g,"").slice(0,6))}
                  placeholder="000000"
                  autoFocus maxLength={6}
                  style={{ ...inputStyle, fontSize: 24, textAlign: "center", letterSpacing: 8, fontWeight: 600 }}
                />
                <div style={{ fontSize: 11, color: "#9C9890", marginTop: 6, textAlign: "center" }}>
                  Demo code: <strong>248613</strong>
                </div>
              </div>
              {error && <div style={errorStyle}>{error}</div>}
              <button type="submit" disabled={loading || code.length < 6} style={btnPrimary}>
                {loading ? "Verifying…" : "Verify & Sign in"}
              </button>
              <button type="button" onClick={() => setStep("password")} style={{ ...backBtn, marginTop: 12 }}>
                ← Back
              </button>
            </form>
          )}
        </div>

        <div style={{ padding: "0 32px 20px", textAlign: "center", fontSize: 11, color: "#9C9890" }}>
          AI Buildathon Dallas 2026 · Secure fleet document access
        </div>
      </div>
    </div>
  );
}

function GoogleIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 48 48" style={{ flexShrink: 0 }}>
      <path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9 3.2l6.7-6.7C35.8 2.5 30.2 0 24 0 14.6 0 6.6 5.5 2.5 13.5l7.8 6C12.3 13.2 17.7 9.5 24 9.5z"/>
      <path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.9 7.2l7.7 6C43.6 37.5 46.5 31.5 46.5 24.5z"/>
      <path fill="#FBBC05" d="M10.3 28.6A14.9 14.9 0 0 1 9.5 24c0-1.6.3-3.1.8-4.6l-7.8-6A24 24 0 0 0 0 24c0 3.9.9 7.5 2.5 10.7l7.8-6.1z"/>
      <path fill="#34A853" d="M24 48c6.2 0 11.4-2 15.2-5.5l-7.7-6c-2 1.4-4.6 2.2-7.5 2.2-6.3 0-11.7-3.7-13.7-9l-7.8 6C6.6 42.5 14.6 48 24 48z"/>
    </svg>
  );
}

const labelStyle = { display: "block", fontSize: 12, fontWeight: 600, color: "#6B6965", marginBottom: 6, textTransform: "uppercase", letterSpacing: ".05em" };
const inputStyle = { width: "100%", padding: "10px 14px", fontSize: 15, border: "1px solid #E4E2D9", borderRadius: 8, outline: "none", background: "#FAFAFA" };
const errorStyle = { fontSize: 12, color: "#DC2626", background: "#FEE2E2", border: "1px solid #FECACA", borderRadius: 8, padding: "8px 12px", marginBottom: 12 };
const btnPrimary = { width: "100%", padding: "11px", background: "#F4A622", color: "#fff", border: "none", borderRadius: 8, fontSize: 14, fontWeight: 600, cursor: "pointer" };
const btnGoogle  = { width: "100%", padding: "10px", background: "#fff", color: "#1C1C1E", border: "1px solid #E4E2D9", borderRadius: 8, fontSize: 14, fontWeight: 500, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", gap: 10 };
const backBtn    = { background: "none", border: "none", fontSize: 12, color: "#9C9890", cursor: "pointer", padding: 0 };
