import { Link, Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

const features = [
  ["Document intake", "Upload PDFs, scans, receipts, forms, and CSVs into one fleet workspace."],
  ["Entity linking", "Connect paperwork to the right truck, driver, trailer, dates, vendors, and costs."],
  ["Grounded answers", "Ask operational questions and get answers tied back to source documents or rows."],
  ["Live context", "Use planned Tavily-backed public lookups for recalls, DOT rules, and fleet context."],
];

const workflow = [
  ["01", "Ingest", "Fleet paperwork is uploaded or generated into the document pipeline."],
  ["02", "Extract", "OCR and metadata extraction pull out truck IDs, dates, costs, and document types."],
  ["03", "Retrieve", "SQL, vector retrieval, and graph context find the right operational evidence."],
  ["04", "Answer", "Operators get concise answers with citations instead of guesses."],
];

export default function Landing() {
  const { user } = useAuth();
  if (user) return <Navigate to="/dashboard" replace />;

  return (
    <div className="public-page">
      <nav className="public-nav">
        <Link to="/" className="brand-lockup" aria-label="FleetMind AI home">
          <span className="brand-mark">FM</span>
          <span>
            <strong>FleetMind AI</strong>
            <small>Document Intelligence</small>
          </span>
        </Link>
        <div className="public-nav-links">
          <Link to="/about">About</Link>
          <a href="#workflow">Workflow</a>
          <Link className="btn btn-ghost" to="/login">Sign in</Link>
        </div>
      </nav>

      <section className="hero-section">
        <div className="hero-copy">
          <span className="eyebrow">AI Buildathon Dallas 2026</span>
          <h1>Turn trucking paperwork into operator-ready intelligence.</h1>
          <p>
            FleetMind AI helps trucking teams organize back-office documents,
            connect them to drivers, trucks, trailers, and loads, and give
            operators a clearer view of what needs attention.
          </p>
          <div className="hero-actions">
            <Link className="btn btn-primary" to="/login">Sign in to dashboard</Link>
            <a className="btn btn-muted" href="#preview">View demo preview</a>
          </div>
        </div>
        <div className="hero-visual" aria-label="Fleet operations dashboard preview">
          <div className="truck-line">
            <span className="truck-cab" />
            <span className="truck-trailer" />
          </div>
          <div className="preview-card preview-main">
            <div>
              <span className="status-dot" />
              Fleet command center
            </div>
            <strong>141</strong>
            <small>demo documents ready for RAG + SQL routing</small>
          </div>
          <div className="preview-grid">
            <div className="preview-card"><b>10</b><span>trucks</span></div>
            <div className="preview-card"><b>4</b><span>trailers</span></div>
            <div className="preview-card"><b>0.65</b><span>confidence floor</span></div>
            <div className="preview-card"><b>RAG</b><span>source citations</span></div>
          </div>
        </div>
      </section>

      <section className="public-band">
        <div className="section-heading">
          <span className="eyebrow">Existing capabilities</span>
          <h2>Built for real fleet back-office work.</h2>
        </div>
        <div className="feature-grid">
          {features.map(([title, text]) => (
            <article className="surface-card lift-card" key={title}>
              <h3>{title}</h3>
              <p>{text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="public-band" id="workflow">
        <div className="section-heading">
          <span className="eyebrow">Workflow</span>
          <h2>From messy files to grounded operator answers.</h2>
        </div>
        <div className="workflow-grid">
          {workflow.map(([step, title, text]) => (
            <article className="workflow-step" key={step}>
              <span>{step}</span>
              <h3>{title}</h3>
              <p>{text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="preview-section" id="preview">
        <div>
          <span className="eyebrow">Dashboard preview</span>
          <h2>One place for questions, documents, and fleet status.</h2>
          <p>
            The protected app keeps the existing dashboard, Ask AI panel,
            upload flow, truck view, API fallback data, and source-based answer
            workflow.
          </p>
          <Link className="btn btn-primary" to="/login">Open FleetMind AI</Link>
        </div>
        <div className="dashboard-preview">
          <div className="mini-topbar" />
          <div className="mini-stat-row">
            <span>Active trucks <b>10</b></span>
            <span>Documents <b>141</b></span>
            <span>Spend MTD <b>$8,240</b></span>
          </div>
          <div className="mini-query">Where is the Form 2290 for truck 84?</div>
          <div className="mini-answer">Answer grounded in form_2290_2025.txt with source match.</div>
        </div>
      </section>

      <footer className="public-footer">
        <span>FleetMind AI</span>
        <span>Built for Statement 7 · AI Buildathon Dallas 2026</span>
        <Link to="/about">Project details</Link>
      </footer>
    </div>
  );
}
