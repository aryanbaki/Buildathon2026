import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext.jsx";

const DEFAULT = {
  theme:        "light",
  mockApi:      true,
  apiUrl:       "http://localhost:8000",
  topK:         8,
  confidence:   0.72,
  notifications: true,
  compactMode:  false,
  fontSize:     "medium",
  accentColor:  "#F4A622",
};

function load() {
  try { return { ...DEFAULT, ...JSON.parse(localStorage.getItem("fleet_settings") || "{}") }; }
  catch { return DEFAULT; }
}

function save(s) { localStorage.setItem("fleet_settings", JSON.stringify(s)); }

function Row({ label, sub, children }) {
  return (
    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "16px 0", borderBottom: "1px solid #F0EEE8" }}>
      <div>
        <div style={{ fontSize: 14, fontWeight: 500 }}>{label}</div>
        {sub && <div style={{ fontSize: 12, color: "#9C9890", marginTop: 2 }}>{sub}</div>}
      </div>
      {children}
    </div>
  );
}

function Toggle({ checked, onChange }) {
  return (
    <div onClick={onChange} style={{
      width: 44, height: 24, borderRadius: 12, cursor: "pointer",
      background: checked ? "#F4A622" : "#E4E2D9",
      position: "relative", transition: "background .2s", flexShrink: 0,
    }}>
      <div style={{
        position: "absolute", top: 2, left: checked ? 22 : 2,
        width: 20, height: 20, borderRadius: "50%", background: "#fff",
        transition: "left .2s", boxShadow: "0 1px 4px rgba(0,0,0,.2)",
      }} />
    </div>
  );
}

const SECTIONS = ["General","API & Data","Appearance","Notifications","Account"];
const ACCENTS  = ["#F4A622","#2563EB","#7C3AED","#16A34A","#DC2626","#0891B2"];

export default function Settings() {
  const [settings, set] = useState(load);
  const [section, setSec] = useState("General");
  const [saved, setSaved] = useState(false);
  const { user, logout }  = useAuth();

  function update(k, v) { set(s => { const n = {...s,[k]:v}; save(n); return n; }); }

  function handleSave() { save(settings); setSaved(true); setTimeout(() => setSaved(false), 2000); }

  return (
    <div style={{ padding: "32px 40px", maxWidth: 900 }}>
      <div style={{ marginBottom: 28 }}>
        <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 6 }}>Settings</h1>
        <p style={{ fontSize: 14, color: "#6B6965" }}>Manage your Fleet AI preferences.</p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "200px 1fr", gap: 20 }}>
        {/* Sidebar nav */}
        <div style={{ background: "#fff", border: "1px solid #E4E2D9", borderRadius: 14, padding: "10px 8px", alignSelf: "start" }}>
          {SECTIONS.map(s => (
            <button key={s} onClick={() => setSec(s)} style={{
              display: "block", width: "100%", textAlign: "left",
              padding: "9px 12px", borderRadius: 8, fontSize: 13, fontWeight: section === s ? 600 : 400,
              background: section === s ? "#FEF9EC" : "transparent",
              color: section === s ? "#C4841A" : "#6B6965",
              border: "none", cursor: "pointer", marginBottom: 2,
            }}>{s}</button>
          ))}
        </div>

        {/* Content */}
        <div style={{ background: "#fff", border: "1px solid #E4E2D9", borderRadius: 14, padding: "8px 28px 24px" }}>

          {section === "General" && (
            <>
              <Row label="Mock API mode" sub="Use simulated data — no backend required">
                <Toggle checked={settings.mockApi} onChange={() => update("mockApi", !settings.mockApi)} />
              </Row>
              <Row label="Compact mode" sub="Reduce spacing for dense layouts">
                <Toggle checked={settings.compactMode} onChange={() => update("compactMode", !settings.compactMode)} />
              </Row>
              <Row label="Results per query" sub={`Currently showing top ${settings.topK} results`}>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <input type="range" min={3} max={20} step={1} value={settings.topK}
                    onChange={e => update("topK", +e.target.value)} style={{ width: 100 }} />
                  <span style={{ fontSize: 13, fontWeight: 600, minWidth: 20 }}>{settings.topK}</span>
                </div>
              </Row>
              <Row label="Min confidence threshold" sub="Answers below this go to human review">
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <input type="range" min={0.5} max={0.95} step={0.01} value={settings.confidence}
                    onChange={e => update("confidence", +e.target.value)} style={{ width: 100 }} />
                  <span style={{ fontSize: 13, fontWeight: 600, minWidth: 30 }}>{(settings.confidence*100).toFixed(0)}%</span>
                </div>
              </Row>
            </>
          )}

          {section === "API & Data" && (
            <>
              <Row label="Backend API URL" sub="FastAPI endpoint for live data">
                <input value={settings.apiUrl} onChange={e => update("apiUrl", e.target.value)}
                  style={{ padding: "7px 10px", fontSize: 13, border: "1px solid #E4E2D9", borderRadius: 8, width: 240 }} />
              </Row>
              <Row label="Mock API" sub="Override with simulated responses">
                <Toggle checked={settings.mockApi} onChange={() => update("mockApi", !settings.mockApi)} />
              </Row>
              <div style={{ marginTop: 16, padding: "14px 16px", background: "#F7F6F3", borderRadius: 10, fontSize: 13, color: "#6B6965" }}>
                <strong style={{ color: "#1C1C1E" }}>Environment variables needed:</strong><br />
                <code style={{ fontSize: 12, fontFamily: "monospace" }}>VITE_API_URL={settings.apiUrl}</code><br />
                <code style={{ fontSize: 12, fontFamily: "monospace" }}>VITE_MOCK_API={settings.mockApi.toString()}</code>
              </div>
            </>
          )}

          {section === "Appearance" && (
            <>
              <Row label="Font size" sub="Adjust text size across the app">
                <select value={settings.fontSize} onChange={e => update("fontSize", e.target.value)}
                  style={{ padding: "7px 10px", fontSize: 13, border: "1px solid #E4E2D9", borderRadius: 8 }}>
                  <option value="small">Small</option>
                  <option value="medium">Medium</option>
                  <option value="large">Large</option>
                </select>
              </Row>
              <Row label="Accent color" sub="Primary action color">
                <div style={{ display: "flex", gap: 8 }}>
                  {ACCENTS.map(c => (
                    <div key={c} onClick={() => update("accentColor", c)} style={{
                      width: 26, height: 26, borderRadius: "50%", background: c, cursor: "pointer",
                      outline: settings.accentColor === c ? `2px solid ${c}` : "none",
                      outlineOffset: 2,
                    }} />
                  ))}
                </div>
              </Row>
              <Row label="Theme" sub="Light / Dark mode (dark mode coming soon)">
                <select value={settings.theme} onChange={e => update("theme", e.target.value)}
                  style={{ padding: "7px 10px", fontSize: 13, border: "1px solid #E4E2D9", borderRadius: 8 }}>
                  <option value="light">Light</option>
                  <option value="dark">Dark (coming soon)</option>
                </select>
              </Row>
            </>
          )}

          {section === "Notifications" && (
            <>
              <Row label="Enable notifications" sub="System alerts and updates">
                <Toggle checked={settings.notifications} onChange={() => update("notifications", !settings.notifications)} />
              </Row>
              <Row label="Expiry alerts" sub="Notify when docs expire within 30 days">
                <Toggle checked={true} onChange={() => {}} />
              </Row>
              <Row label="Low confidence alerts" sub="Flag answers that need human review">
                <Toggle checked={true} onChange={() => {}} />
              </Row>
            </>
          )}

          {section === "Account" && (
            <>
              {user && (
                <div style={{ display: "flex", alignItems: "center", gap: 14, padding: "20px 0", borderBottom: "1px solid #F0EEE8", marginBottom: 8 }}>
                  <div style={{ width: 48, height: 48, borderRadius: "50%", background: "#1A1A2E", color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16, fontWeight: 700 }}>
                    {user.avatar || user.name?.[0]}
                  </div>
                  <div>
                    <div style={{ fontSize: 15, fontWeight: 600 }}>{user.name}</div>
                    <div style={{ fontSize: 13, color: "#9C9890" }}>{user.email}</div>
                    <div style={{ fontSize: 11, background: "#FEF9EC", color: "#C4841A", padding: "2px 8px", borderRadius: 99, marginTop: 4, display: "inline-block", fontWeight: 600 }}>
                      {user.role?.replace("_"," ")}
                    </div>
                  </div>
                </div>
              )}
              <Row label="Two-step verification" sub="Google Authenticator or SMS">
                <span style={{ fontSize: 12, fontWeight: 600, padding: "3px 10px", borderRadius: 99, background: "#DCFCE7", color: "#15803D" }}>Active</span>
              </Row>
              <div style={{ paddingTop: 20 }}>
                <button onClick={logout} style={{ padding: "9px 20px", background: "#FEE2E2", color: "#B91C1C", border: "1px solid #FECACA", borderRadius: 8, fontSize: 13, fontWeight: 600, cursor: "pointer" }}>
                  Sign out
                </button>
              </div>
            </>
          )}

          <div style={{ marginTop: 24, display: "flex", justifyContent: "flex-end" }}>
            <button onClick={handleSave} style={{ padding: "9px 24px", background: saved ? "#16A34A" : "#1A1A2E", color: "#fff", border: "none", borderRadius: 8, fontSize: 13, fontWeight: 600, cursor: "pointer", transition: "background .3s" }}>
              {saved ? "✓ Saved" : "Save settings"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
