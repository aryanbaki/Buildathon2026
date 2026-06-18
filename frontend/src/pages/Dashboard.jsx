import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getFleetStats, getTrucks } from "../services/api.js";
import UploadZone from "../components/UploadZone.jsx";

function StatCard({ label, value, sub, accent }) {
  return (
    <div style={{ background: "#fff", border: "1px solid #E4E2D9", borderRadius: 14, padding: "20px 24px", borderTop: `3px solid ${accent || "#E4E2D9"}` }}>
      <div style={{ fontSize: 11, color: "#9C9890", fontWeight: 600, marginBottom: 8, textTransform: "uppercase", letterSpacing: ".05em" }}>{label}</div>
      <div style={{ fontSize: 28, fontWeight: 600, lineHeight: 1 }}>{value}</div>
      {sub && <div style={{ fontSize: 12, color: "#9C9890", marginTop: 6 }}>{sub}</div>}
    </div>
  );
}

const QUERIES = [
  { q: "How much did truck 84 spend on maintenance last month?", tag: "sql" },
  { q: "Which registrations are expiring in 30 days?",          tag: "sql" },
  { q: "Where is the Form 2290 for truck 84?",                  tag: "rag" },
  { q: "What did the last DOT inspection say about truck 86?",  tag: "rag" },
  { q: "Are there active recalls on our 2019 Freightliner?",    tag: "web" },
  { q: "What documents do I need to renew plates for truck 85?",tag: "hybrid" },
];

const TAG = {
  sql:    { bg: "#DBEAFE", color: "#1D4ED8" },
  rag:    { bg: "#EDE9FE", color: "#6D28D9" },
  hybrid: { bg: "#FEF3C7", color: "#92400E" },
  web:    { bg: "#DCFCE7", color: "#15803D" },
};

// Replace VIDEO_ID with your actual YouTube video ID once you have it
const VIDEO_ID = "dQw4w9WgXcQ";

const HOW_IT_WORKS = [
  { icon: "📤", step: "1", title: "Upload documents", desc: "Drop any fleet document — PDFs, photos, receipts, forms. OCR extracts the text automatically." },
  { icon: "🔗", step: "2", title: "Auto-linked", desc: "Claude Haiku extracts truck IDs, dates, and costs and links each document to the right truck and driver." },
  { icon: "💬", step: "3", title: "Ask anything", desc: "Type a plain English question. The query router sends it to SQL, RAG, or web search — whichever fits." },
  { icon: "📎", step: "4", title: "Grounded answers", desc: "Every answer cites the exact source document or database row. No hallucinations, ever." },
];

export default function Dashboard() {
  const [stats, setStats]   = useState(null);
  const [trucks, setTrucks] = useState([]);
  const [tab, setTab]       = useState("ask");
  const [showVideo, setShowVideo] = useState(false);
  const navigate = useNavigate();

  useEffect(() => { getFleetStats().then(setStats); getTrucks().then(setTrucks); }, []);

  return (
    <div style={{ padding: "32px 40px", maxWidth: 1100 }}>
      {/* Header */}
      <div style={{ marginBottom: 28 }}>
        <div style={{ fontSize: 11, fontWeight: 700, color: "#F4A622", letterSpacing: ".12em", textTransform: "uppercase", marginBottom: 6 }}>
          AI Buildathon Dallas 2026
        </div>
        <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 16 }}>
          <div>
            <h1 style={{ fontSize: 26, fontWeight: 600, marginBottom: 6 }}>Fleet Document Intelligence</h1>
            <p style={{ fontSize: 14, color: "#6B6965", maxWidth: 520 }}>
              Ask anything about your fleet in plain English. Every answer is grounded in a real document or database record.
            </p>
          </div>
          <button onClick={() => setShowVideo(true)} style={{
            display: "flex", alignItems: "center", gap: 8, padding: "10px 18px",
            background: "#1A1A2E", color: "#fff", border: "none",
            borderRadius: 10, fontSize: 13, fontWeight: 600, cursor: "pointer", flexShrink: 0,
          }}>
            ▶ How it works
          </button>
        </div>
      </div>

      {/* Video modal */}
      {showVideo && (
        <div onClick={() => setShowVideo(false)} style={{
          position: "fixed", inset: 0, background: "rgba(0,0,0,.7)",
          display: "flex", alignItems: "center", justifyContent: "center",
          zIndex: 999, padding: 24,
        }}>
          <div onClick={e => e.stopPropagation()} style={{ background: "#fff", borderRadius: 16, overflow: "hidden", width: "100%", maxWidth: 800 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "14px 20px", borderBottom: "1px solid #E4E2D9" }}>
              <div style={{ fontSize: 15, fontWeight: 600 }}>How Fleet AI works</div>
              <button onClick={() => setShowVideo(false)} style={{ background: "none", border: "none", fontSize: 20, cursor: "pointer", color: "#9C9890" }}>✕</button>
            </div>
            {/* YouTube embed — replace VIDEO_ID with your real video */}
            <div style={{ position: "relative", paddingBottom: "56.25%", background: "#000" }}>
              <iframe
                src={`https://www.youtube.com/embed/${VIDEO_ID}?autoplay=1`}
                title="How Fleet AI works"
                allow="autoplay; fullscreen"
                style={{ position: "absolute", inset: 0, width: "100%", height: "100%", border: "none" }}
              />
            </div>
            {/* Steps below video */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 0 }}>
              {HOW_IT_WORKS.map(({ icon, step, title, desc }, i) => (
                <div key={step} style={{
                  padding: "16px 18px", borderTop: "1px solid #E4E2D9",
                  borderRight: i < 3 ? "1px solid #E4E2D9" : "none",
                }}>
                  <div style={{ fontSize: 20, marginBottom: 6 }}>{icon}</div>
                  <div style={{ fontSize: 11, fontWeight: 700, color: "#F4A622", marginBottom: 4 }}>STEP {step}</div>
                  <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 4 }}>{title}</div>
                  <div style={{ fontSize: 12, color: "#6B6965", lineHeight: 1.5 }}>{desc}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Stat cards */}
      {stats && (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 14, marginBottom: 24 }}>
          <StatCard label="Active trucks"      value={stats.total_trucks}    accent="#F4A622" />
          <StatCard label="Documents ingested" value={stats.total_documents} accent="#2563EB" />
          <StatCard label="Spend MTD"          value={`$${(stats.total_spend_mtd||0).toLocaleString()}`} accent="#7C3AED" />
          <StatCard label="Expiring soon"      value={stats.expiring_soon}   accent={stats.expiring_soon > 0 ? "#DC2626" : "#16A34A"} sub="next 30 days" />
        </div>
      )}

      {/* How it works strip (always visible, compact) */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 12, marginBottom: 24 }}>
        {HOW_IT_WORKS.map(({ icon, step, title }) => (
          <div key={step} onClick={() => setShowVideo(true)} style={{
            background: "#fff", border: "1px solid #E4E2D9", borderRadius: 10,
            padding: "12px 16px", display: "flex", alignItems: "center", gap: 10,
            cursor: "pointer", transition: "border-color .15s",
          }}
          onMouseEnter={e => e.currentTarget.style.borderColor = "#F4A622"}
          onMouseLeave={e => e.currentTarget.style.borderColor = "#E4E2D9"}
          >
            <span style={{ fontSize: 18 }}>{icon}</span>
            <div>
              <div style={{ fontSize: 10, fontWeight: 700, color: "#F4A622" }}>STEP {step}</div>
              <div style={{ fontSize: 12, fontWeight: 600 }}>{title}</div>
            </div>
          </div>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18 }}>
        {/* Left */}
        <div style={{ background: "#fff", border: "1px solid #E4E2D9", borderRadius: 14, overflow: "hidden" }}>
          <div style={{ display: "flex", borderBottom: "1px solid #E4E2D9" }}>
            {["ask","upload"].map(t => (
              <button key={t} onClick={() => setTab(t)} style={{
                padding: "12px 20px", fontSize: 13, border: "none", background: "none",
                cursor: "pointer", fontWeight: tab === t ? 600 : 400,
                color: tab === t ? "#1C1C1E" : "#6B6965",
                borderBottom: tab === t ? "2px solid #F4A622" : "2px solid transparent",
              }}>{t === "ask" ? "Try asking" : "Upload docs"}</button>
            ))}
          </div>
          <div style={{ padding: 20 }}>
            {tab === "ask" && (
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {QUERIES.map(({ q, tag }) => (
                  <button key={q} onClick={() => navigate("/ask", { state: { question: q } })} style={{
                    display: "flex", alignItems: "center", justifyContent: "space-between",
                    gap: 10, padding: "10px 14px",
                    background: "#F7F6F3", border: "1px solid #E4E2D9",
                    borderRadius: 10, textAlign: "left", fontSize: 13, cursor: "pointer",
                  }}
                  onMouseEnter={e => e.currentTarget.style.borderColor = "#F4A622"}
                  onMouseLeave={e => e.currentTarget.style.borderColor = "#E4E2D9"}
                  >
                    <span>{q}</span>
                    <span style={{ fontSize: 10, fontWeight: 700, padding: "2px 8px", borderRadius: 99, flexShrink: 0, ...TAG[tag] }}>{tag}</span>
                  </button>
                ))}
              </div>
            )}
            {tab === "upload" && <UploadZone trucks={trucks} onUploadComplete={() => getFleetStats().then(setStats)} />}
          </div>
        </div>

        {/* Right — fleet roster */}
        <div style={{ background: "#fff", border: "1px solid #E4E2D9", borderRadius: 14, padding: 20 }}>
          <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 16 }}>Fleet roster</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {trucks.map(t => (
              <button key={t.id} onClick={() => navigate(`/trucks/${t.id}`)} style={{
                display: "flex", alignItems: "center", justifyContent: "space-between",
                padding: "12px 16px", background: "#F7F6F3",
                border: "1px solid #E4E2D9", borderRadius: 10, cursor: "pointer",
              }}
              onMouseEnter={e => e.currentTarget.style.borderColor = "#F4A622"}
              onMouseLeave={e => e.currentTarget.style.borderColor = "#E4E2D9"}
              >
                <div style={{ textAlign: "left" }}>
                  <div style={{ fontSize: 13, fontWeight: 600 }}>Truck {t.unit_number}</div>
                  <div style={{ fontSize: 12, color: "#6B6965" }}>{t.year} {t.make} {t.model}</div>
                </div>
                <span style={{
                  fontSize: 11, fontWeight: 600, padding: "3px 10px", borderRadius: 99,
                  background: t.status === "active" ? "#DCFCE7" : "#FEE2E2",
                  color: t.status === "active" ? "#16A34A" : "#DC2626",
                }}>{t.status}</span>
              </button>
            ))}
            {!trucks.length && (
              <div style={{ fontSize: 13, color: "#6B6965", padding: "20px 0", textAlign: "center" }}>
                No trucks — run seed_data.py first
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
