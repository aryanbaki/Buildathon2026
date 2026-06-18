import { useState, useEffect } from "react";
import { getFleetStats, getTrucks } from "../services/api";
import ChatPanel from "../components/ChatPanel";
import UploadZone from "../components/UploadZone";

function StatCard({ label, value, sub, color }) {
  return (
    <div style={{
      background: "var(--color-background-secondary,#f5f5f3)",
      borderRadius: 8, padding: "1rem", flex: 1,
    }}>
      <div style={{ fontSize: 13, color: "var(--color-text-secondary)", marginBottom: 4 }}>{label}</div>
      <div style={{ fontSize: 24, fontWeight: 500, color: color || "var(--color-text-primary)" }}>{value}</div>
      {sub && <div style={{ fontSize: 12, color: "var(--color-text-secondary)", marginTop: 2 }}>{sub}</div>}
    </div>
  );
}

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [trucks, setTrucks] = useState([]);
  const [tab, setTab] = useState("ask"); // ask | upload

  useEffect(() => {
    getFleetStats().then(setStats);
    getTrucks().then(setTrucks);
  }, []);

  return (
    <div style={{ maxWidth: 960, margin: "0 auto", padding: "24px 20px" }}>
      {/* Header */}
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: 22, fontWeight: 500, margin: 0 }}>Fleet Document Intelligence</h1>
        <p style={{ fontSize: 14, color: "var(--color-text-secondary)", margin: "4px 0 0" }}>
          Ask anything about your fleet — every answer grounded in real documents.
        </p>
      </div>

      {/* Stat cards */}
      {stats && (
        <div style={{ display: "flex", gap: 12, marginBottom: 24 }}>
          <StatCard label="Active trucks" value={stats.total_trucks} />
          <StatCard label="Documents ingested" value={stats.total_documents} />
          <StatCard label="Spend MTD" value={`$${stats.total_spend_mtd.toLocaleString()}`} />
          <StatCard
            label="Expiring soon"
            value={stats.expiring_soon}
            sub="registrations / insurance"
            color={stats.expiring_soon > 0 ? "#A32D2D" : undefined}
          />
        </div>
      )}

      {/* Main panel */}
      <div style={{
        background: "var(--color-background-primary,#fff)",
        border: "0.5px solid var(--color-border-tertiary,#e0dfd8)",
        borderRadius: 12, overflow: "hidden",
      }}>
        {/* Tabs */}
        <div style={{ display: "flex", borderBottom: "0.5px solid var(--color-border-tertiary,#e0dfd8)" }}>
          {["ask", "upload"].map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              style={{
                padding: "12px 20px", fontSize: 14, border: "none", background: "none",
                cursor: "pointer", fontWeight: tab === t ? 500 : 400,
                color: tab === t ? "var(--color-text-primary)" : "var(--color-text-secondary)",
                borderBottom: tab === t ? "2px solid #534AB7" : "2px solid transparent",
              }}
            >
              {t === "ask" ? "Ask AI" : "Upload Documents"}
            </button>
          ))}
        </div>

        <div style={{ padding: 20 }}>
          {tab === "ask" && <ChatPanel />}
          {tab === "upload" && <UploadZone trucks={trucks} onUploadComplete={() => getFleetStats().then(setStats)} />}
        </div>
      </div>
    </div>
  );
}
