const TEAM = [
  { name: "Yesh Salapu",  role: "Frontend Engineer",     avatar: "YS", color: "#1A1A2E", bio: "CS grad, UNT 2026. Built the full React UI, routing, and component system." },
  { name: "Charan",       role: "Database Engineer",      avatar: "CH", color: "#16A34A", bio: "Owns the PostgreSQL schema, OCR ingest pipeline, and synthetic data generation." },
  { name: "Aryan",        role: "RAG & ML Engineer",      avatar: "AR", color: "#F4A622", bio: "Built the ChromaDB vector store, embedding pipeline, and knowledge graph." },
  { name: "Teja",         role: "AI Agent Engineer",      avatar: "TE", color: "#7C3AED", bio: "Designed the query router, SQL agent, document agent, and FastAPI backend." },
];

const STACK = [
  ["Frontend",    "React 18 + Vite + React Router"],
  ["Backend",     "FastAPI + Python 3.12"],
  ["Database",    "PostgreSQL 16 + pgvector"],
  ["AI Extraction","Claude Haiku (Anthropic)"],
  ["AI Routing",  "Claude Sonnet (Anthropic)"],
  ["Web Search",  "Tavily API"],
  ["Vector Store","ChromaDB + sentence-transformers"],
  ["OCR",         "OCRmyPDF + Tesseract"],
  ["Auth",        "JWT + OIDC (Google)"],
  ["Deployment",  "Docker Compose + Railway"],
];

export default function About() {
  return (
    <div style={{ padding: "32px 40px", maxWidth: 900 }}>
      {/* Hero */}
      <div style={{ marginBottom: 36 }}>
        <div style={{ fontSize: 11, fontWeight: 700, color: "#F4A622", letterSpacing: ".12em", textTransform: "uppercase", marginBottom: 6 }}>
          AI Buildathon Dallas 2026
        </div>
        <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 10 }}>About Fleet Document Intelligence</h1>
        <p style={{ fontSize: 15, color: "#6B6965", maxWidth: 600, lineHeight: 1.7 }}>
          Built in 32 hours at AI Buildathon Dallas 2026. Fleet Document Intelligence transforms unstructured trucking paperwork into instant, grounded operational answers — no hallucinations, every answer cites a real source.
        </p>
      </div>

      {/* Problem / Solution */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 36 }}>
        {[
          { label: "The problem", icon: "📦", text: "Trucking carriers run on paper. 50+ documents per week — receipts, registrations, tax forms, inspection reports — all unsearchable. Operators spend hours digging through filing cabinets to answer basic questions." },
          { label: "The solution", icon: "⚡", text: "Ingest every document, link it to the correct truck and driver, and let operators ask anything in plain English. SQL for structured data, RAG for document content, Tavily for live web data — all in one grounded answer." },
        ].map(({ label, icon, text }) => (
          <div key={label} style={{ background: "#fff", border: "1px solid #E4E2D9", borderRadius: 14, padding: "20px 24px" }}>
            <div style={{ fontSize: 24, marginBottom: 10 }}>{icon}</div>
            <div style={{ fontSize: 13, fontWeight: 700, textTransform: "uppercase", letterSpacing: ".06em", color: "#9C9890", marginBottom: 8 }}>{label}</div>
            <p style={{ fontSize: 14, color: "#6B6965", lineHeight: 1.7 }}>{text}</p>
          </div>
        ))}
      </div>

      {/* Team */}
      <div style={{ marginBottom: 36 }}>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>The team</h2>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
          {TEAM.map(({ name, role, avatar, color, bio }) => (
            <div key={name} style={{ background: "#fff", border: "1px solid #E4E2D9", borderRadius: 14, padding: "18px 20px", display: "flex", gap: 14 }}>
              <div style={{
                width: 44, height: 44, borderRadius: "50%", background: color,
                color: "#fff", display: "flex", alignItems: "center", justifyContent: "center",
                fontSize: 14, fontWeight: 700, flexShrink: 0,
              }}>{avatar}</div>
              <div>
                <div style={{ fontSize: 14, fontWeight: 600 }}>{name}</div>
                <div style={{ fontSize: 12, color: "#F4A622", fontWeight: 500, marginBottom: 6 }}>{role}</div>
                <div style={{ fontSize: 13, color: "#6B6965", lineHeight: 1.6 }}>{bio}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Stack */}
      <div>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Tech stack</h2>
        <div style={{ background: "#fff", border: "1px solid #E4E2D9", borderRadius: 14, overflow: "hidden" }}>
          {STACK.map(([layer, tech], i) => (
            <div key={layer} style={{
              display: "flex", justifyContent: "space-between", alignItems: "center",
              padding: "12px 20px", fontSize: 13,
              borderBottom: i < STACK.length - 1 ? "1px solid #E4E2D9" : "none",
            }}>
              <span style={{ color: "#9C9890", fontWeight: 500 }}>{layer}</span>
              <span style={{ fontWeight: 500 }}>{tech}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
