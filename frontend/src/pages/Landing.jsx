import { useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";

const SLIDES = [
  { title: "Fleet Document Intelligence", sub: "Ask anything about your fleet in plain English. Every answer grounded in real data.", bg: "#1A1A2E", img: "🚛" },
  { title: "Upload once, query forever", sub: "Maintenance receipts, tax forms, registrations — all searchable instantly.", bg: "#0F2942", img: "📄" },
  { title: "No hallucinations. Ever.", sub: "Every answer cites the exact source document or database row.", bg: "#1A2E1A", img: "⚡" },
];

const NEWS = [
  { date: "Jun 18", tag: "Launch",  title: "Fleet AI debuts at AI Buildathon Dallas 2026", body: "Built in 32 hours by a team of 4 engineers." },
  { date: "Jun 18", tag: "Feature", title: "Tavily web search integration live", body: "Ask about NHTSA recalls, FMCSA rules, and live diesel prices." },
  { date: "Jun 18", tag: "Feature", title: "Google OAuth + 2FA now available", body: "Sign in securely with your Google account." },
  { date: "Jun 18", tag: "Update",  title: "pgvector hybrid retrieval deployed", body: "Vector + full-text + SQL combined for maximum accuracy." },
];

const TAG_COLOR = {
  Launch:  { bg: "#FEF3C7", color: "#92400E" },
  Feature: { bg: "#DBEAFE", color: "#1D4ED8" },
  Update:  { bg: "#DCFCE7", color: "#15803D" },
};

export default function Landing() {
  const { setShowLogin } = useAuth();
  const [slide, setSlide] = useState(0);
  const s = SLIDES[slide];

  function prev() { setSlide((slide - 1 + SLIDES.length) % SLIDES.length); }
  function next() { setSlide((slide + 1) % SLIDES.length); }

  return (
    <div style={{ minHeight: "100vh", background: "#F7F6F3", fontFamily: "Inter,sans-serif" }}>

      {/* Top bar */}
      <div style={{ background: "#1A1A2E", padding: "0 40px", height: 60, display: "flex", alignItems: "center", justifyContent: "space-between", position: "sticky", top: 0, zIndex: 100 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ width: 32, height: 32, background: "#F4A622", borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16 }}>🚛</div>
          <div>
            <div style={{ color: "#fff", fontSize: 14, fontWeight: 600 }}>Fleet AI</div>
            <div style={{ color: "#9898B0", fontSize: 10 }}>Document Intelligence</div>
          </div>
        </div>
        <div style={{ display: "flex", gap: 10 }}>
          <button onClick={() => setShowLogin(true)} style={{ padding: "7px 20px", background: "transparent", color: "#fff", border: "1px solid rgba(255,255,255,.3)", borderRadius: 8, fontSize: 13, fontWeight: 500, cursor: "pointer" }}>
            Login
          </button>
          <button onClick={() => setShowLogin(true)} style={{ padding: "7px 20px", background: "#F4A622", color: "#fff", border: "none", borderRadius: 8, fontSize: 13, fontWeight: 600, cursor: "pointer" }}>
            Register
          </button>
        </div>
      </div>

      {/* Main grid */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 320px", gap: 20, padding: "28px 40px", maxWidth: 1100, margin: "0 auto" }}>

        {/* Left — carousel */}
        <div>
          <div style={{ background: s.bg, borderRadius: 16, padding: "60px 40px", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", position: "relative", minHeight: 380, transition: "background .4s" }}>
            <div style={{ fontSize: 72, marginBottom: 20 }}>{s.img}</div>
            <h1 style={{ color: "#fff", fontSize: 26, fontWeight: 700, textAlign: "center", marginBottom: 12, lineHeight: 1.3 }}>{s.title}</h1>
            <p style={{ color: "rgba(255,255,255,.7)", fontSize: 14, textAlign: "center", maxWidth: 460, lineHeight: 1.7 }}>{s.sub}</p>
            <button onClick={() => setShowLogin(true)} style={{ marginTop: 28, padding: "11px 32px", background: "#F4A622", color: "#fff", border: "none", borderRadius: 10, fontSize: 14, fontWeight: 600, cursor: "pointer" }}>
              Get started →
            </button>
            <button onClick={prev} style={{ position: "absolute", left: 14, top: "50%", transform: "translateY(-50%)", background: "rgba(255,255,255,.15)", border: "none", color: "#fff", borderRadius: "50%", width: 36, height: 36, fontSize: 20, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center" }}>‹</button>
            <button onClick={next} style={{ position: "absolute", right: 14, top: "50%", transform: "translateY(-50%)", background: "rgba(255,255,255,.15)", border: "none", color: "#fff", borderRadius: "50%", width: 36, height: 36, fontSize: 20, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center" }}>›</button>
          </div>

          {/* Dots */}
          <div style={{ display: "flex", justifyContent: "center", gap: 8, marginTop: 14 }}>
            {SLIDES.map((_, i) => (
              <button key={i} onClick={() => setSlide(i)} style={{ width: i === slide ? 24 : 8, height: 8, borderRadius: 99, border: "none", cursor: "pointer", background: i === slide ? "#F4A622" : "#CCC9BC", transition: "all .3s", padding: 0 }} />
            ))}
          </div>

          {/* Scroll down arrow */}
          <div style={{ display: "flex", justifyContent: "center", marginTop: 16 }}>
            <div style={{ color: "#9C9890", fontSize: 22 }}>↓</div>
          </div>

          {/* Feature pills */}
          <div style={{ display: "flex", gap: 8, marginTop: 16, flexWrap: "wrap" }}>
            {["Claude Haiku + Sonnet", "Tavily Web Search", "pgvector RAG", "Google OAuth + 2FA", "PostgreSQL RLS", "Docker + Railway"].map(f => (
              <span key={f} style={{ padding: "5px 12px", background: "#fff", border: "1px solid #E4E2D9", borderRadius: 99, fontSize: 12, color: "#6B6965", fontWeight: 500 }}>{f}</span>
            ))}
          </div>
        </div>

        {/* Right — news */}
        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          <div style={{ background: "#fff", border: "1px solid #E4E2D9", borderRadius: 16, overflow: "hidden" }}>
            <div style={{ padding: "12px 18px", borderBottom: "1px solid #E4E2D9", display: "flex", alignItems: "center", gap: 8 }}>
              <span style={{ fontSize: 15 }}>📰</span>
              <span style={{ fontSize: 14, fontWeight: 600 }}>News</span>
            </div>
            {NEWS.map((n, i) => {
              const tc = TAG_COLOR[n.tag] || TAG_COLOR.Update;
              return (
                <div key={i} style={{ padding: "14px 18px", borderBottom: i < NEWS.length - 1 ? "1px solid #F0EEE8" : "none" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 5 }}>
                    <span style={{ fontSize: 10, fontWeight: 700, padding: "2px 8px", borderRadius: 99, background: tc.bg, color: tc.color }}>{n.tag}</span>
                    <span style={{ fontSize: 11, color: "#9C9890" }}>{n.date}</span>
                  </div>
                  <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 3, lineHeight: 1.4 }}>{n.title}</div>
                  <div style={{ fontSize: 12, color: "#6B6965", lineHeight: 1.5 }}>{n.body}</div>
                </div>
              );
            })}
          </div>

          {/* Stats */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
            {[["32hrs", "built at hackathon"], ["4", "team members"], ["6", "AI features"], ["100%", "grounded answers"]].map(([v, l]) => (
              <div key={l} style={{ background: "#fff", border: "1px solid #E4E2D9", borderRadius: 12, padding: "14px", textAlign: "center" }}>
                <div style={{ fontSize: 20, fontWeight: 700, color: "#1A1A2E" }}>{v}</div>
                <div style={{ fontSize: 11, color: "#9C9890", marginTop: 2 }}>{l}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer */}
      <div style={{ textAlign: "center", padding: "20px 40px", fontSize: 12, color: "#9C9890", borderTop: "1px solid #E4E2D9", marginTop: 10 }}>
        AI Buildathon Dallas 2026 · Yesh · Charan · Aryan · Teja ·{" "}
        <a href="https://github.com/aryanbaki/Buildathon2026" target="_blank" rel="noreferrer" style={{ color: "#F4A622" }}>GitHub ↗</a>
      </div>
    </div>
  );
}
