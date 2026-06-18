import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getFleetStats, getTrucks } from "../services/api.js";
import UploadZone from "../components/UploadZone.jsx";

function StatCard({ label, value, sub, tone = "green" }) {
  return (
    <article className={`stat-card tone-${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
      {sub && <small>{sub}</small>}
    </article>
  );
}

const QUERIES = [
  { q: "How much did truck 84 spend on maintenance last month?", tag: "sql" },
  { q: "Which registrations are expiring in 30 days?", tag: "sql" },
  { q: "Where is the Form 2290 for truck 84?", tag: "rag" },
  { q: "What did the last DOT inspection say about truck 86?", tag: "rag" },
  { q: "Are there active recalls on our 2019 Freightliner?", tag: "web" },
  { q: "What documents do I need to renew plates for truck 85?", tag: "hybrid" },
];

const HOW_IT_WORKS = [
  ["01", "Upload", "PDFs, scans, receipts, forms, and CSVs enter the same fleet intake."],
  ["02", "Link", "Metadata connects each document to trucks, drivers, trailers, dates, and costs."],
  ["03", "Route", "Questions move through SQL, RAG, hybrid, or Tavily-backed web paths."],
  ["04", "Cite", "Answers stay grounded in database rows and source document snippets."],
];

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [trucks, setTrucks] = useState([]);
  const [tab, setTab] = useState("ask");
  const [showVideo, setShowVideo] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    getFleetStats().then(setStats);
    getTrucks().then(setTrucks);
  }, []);

  return (
    <div className="page-wrap dashboard-page">
      <header className="page-hero">
        <div>
          <span className="eyebrow">FleetMind AI command center</span>
          <h1>Fleet document intelligence</h1>
          <p>
            Ask fleet questions, upload documents, monitor expiring records, and
            jump into truck-specific context without leaving the operator view.
          </p>
        </div>
        <button className="btn btn-muted" onClick={() => setShowVideo(true)}>View workflow</button>
      </header>

      {showVideo && (
        <div className="modal-backdrop" onClick={() => setShowVideo(false)}>
          <div className="modal-card" onClick={(event) => event.stopPropagation()}>
            <div className="modal-header">
              <strong>How FleetMind AI works</strong>
              <button onClick={() => setShowVideo(false)}>x</button>
            </div>
            <div className="workflow-grid modal-workflow">
              {HOW_IT_WORKS.map(([step, title, text]) => (
                <article className="workflow-step" key={step}>
                  <span>{step}</span>
                  <h3>{title}</h3>
                  <p>{text}</p>
                </article>
              ))}
            </div>
          </div>
        </div>
      )}

      {stats ? (
        <section className="stats-grid">
          <StatCard label="Active trucks" value={stats.total_trucks} tone="green" />
          <StatCard label="Documents ingested" value={stats.total_documents} tone="steel" />
          <StatCard label="Spend MTD" value={`$${(stats.total_spend_mtd || 0).toLocaleString()}`} tone="amber" />
          <StatCard label="Expiring soon" value={stats.expiring_soon} sub="next 30 days" tone={stats.expiring_soon > 0 ? "red" : "green"} />
        </section>
      ) : (
        <section className="stats-grid">
          {[0, 1, 2, 3].map((item) => <div className="stat-card loading-card" key={item} />)}
        </section>
      )}

      <section className="workflow-strip">
        {HOW_IT_WORKS.map(([step, title, text]) => (
          <button className="workflow-pill" key={step} onClick={() => setShowVideo(true)}>
            <span>{step}</span>
            <strong>{title}</strong>
            <small>{text}</small>
          </button>
        ))}
      </section>

      <section className="dashboard-grid">
        <article className="surface-panel">
          <div className="panel-tabs">
            <button className={tab === "ask" ? "active" : ""} onClick={() => setTab("ask")}>Ask AI</button>
            <button className={tab === "upload" ? "active" : ""} onClick={() => setTab("upload")}>Upload documents</button>
          </div>
          <div className="panel-body">
            {tab === "ask" && (
              <div className="query-list">
                {QUERIES.map(({ q, tag }) => (
                  <button key={q} onClick={() => navigate("/ask", { state: { question: q } })}>
                    <span>{q}</span>
                    <b>{tag}</b>
                  </button>
                ))}
              </div>
            )}
            {tab === "upload" && <UploadZone trucks={trucks} onUploadComplete={() => getFleetStats().then(setStats)} />}
          </div>
        </article>

        <article className="surface-panel">
          <div className="panel-title">
            <span>Fleet roster</span>
            <small>{trucks.length || 0} units loaded</small>
          </div>
          <div className="truck-list">
            {trucks.map((truck) => (
              <button key={truck.id} onClick={() => navigate(`/trucks/${truck.id}`)}>
                <span>
                  <strong>Truck {truck.unit_number}</strong>
                  <small>{truck.year} {truck.make} {truck.model}</small>
                </span>
                <b className={truck.status === "active" ? "status-active" : "status-idle"}>{truck.status}</b>
              </button>
            ))}
            {!trucks.length && <div className="empty-state">No trucks loaded yet. Run the demo bootstrap or use mock fallback data.</div>}
          </div>
        </article>
      </section>
    </div>
  );
}
