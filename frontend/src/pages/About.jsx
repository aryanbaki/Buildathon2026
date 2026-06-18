import React from "react";
import { Link } from "react-router-dom";

const TEAM = [
  ["Yesh Salapu", "Frontend Engineer", "React UI, routing, dashboard surfaces, and component polish."],
  ["Charan", "Database Engineer", "PostgreSQL schema, OCR ingestion pipeline, upload storage, and seed data."],
  ["Aryan", "RAG & Graph Engineer", "ChromaDB retrieval, metadata filters, trailer-aware RAG, and knowledge graph helpers."],
  ["Teja", "AI Agent Engineer", "Query routing, SQL/document/hybrid agents, FastAPI API layer, and demo bootstrap."],
];

const STACK = [
  ["Frontend", "React 18, Vite, React Router"],
  ["Backend", "FastAPI, Python, Docker Compose"],
  ["Database", "PostgreSQL, SQLAlchemy"],
  ["Retrieval", "ChromaDB, sentence-transformers, metadata filters"],
  ["Documents", "Tesseract OCR, PDF/image/text loaders, synthetic messy fleet docs"],
  ["Reasoning", "Claude Haiku extraction, Claude Sonnet routing, grounded fallback demo agents"],
  ["External context", "Tavily for planned recall, DOT/FMCSA, and diesel-price lookups"],
];

const cards = [
  ["Problem", "Trucking teams manage high-volume paperwork across receipts, registrations, inspections, tax forms, titles, and maintenance records."],
  ["Solution", "FleetMind AI links documents to trucks, drivers, trailers, dates, costs, and source snippets so operators can ask questions in plain English."],
  ["Impact", "Fleet operators, dispatchers, managers, and accounting teams can find the right evidence faster without guessing or digging through files."],
];

export default function About() {
  return (
    <div className="public-page about-public">
      <nav className="public-nav">
        <Link to="/" className="brand-lockup">
          <span className="brand-mark">FM</span>
          <span>
            <strong>FleetMind AI</strong>
            <small>Project overview</small>
          </span>
        </Link>
        <div className="public-nav-links">
          <Link to="/">Home</Link>
          <Link className="btn btn-ghost" to="/login">Sign in</Link>
        </div>
      </nav>

      <main className="about-shell">
        <section className="page-hero public-hero-narrow">
          <div>
            <span className="eyebrow">AI Buildathon Dallas 2026</span>
            <h1>Fleet document intelligence for messy trucking operations.</h1>
            <p>
              FleetMind AI is a buildathon MVP for Statement 7: turn unstructured
              fleet paperwork into searchable, grounded operational intelligence.
            </p>
          </div>
        </section>

        <section className="feature-grid">
          {cards.map(([title, text]) => (
            <article className="surface-card lift-card" key={title}>
              <h3>{title}</h3>
              <p>{text}</p>
            </article>
          ))}
        </section>

        <section className="public-band compact-band">
          <div className="section-heading">
            <span className="eyebrow">Who it helps</span>
            <h2>Operators, dispatchers, fleet managers, and accounting teams.</h2>
          </div>
          <p className="wide-copy">
            The app is designed for people who need quick answers about drivers,
            trucks, trailers, loads, invoices, PODs, bills of lading, maintenance,
            tax forms, registrations, and document expirations.
          </p>
        </section>

        <section className="public-band compact-band">
          <div className="section-heading">
            <span className="eyebrow">Team ownership</span>
            <h2>Clear workstreams across frontend, ingestion, RAG, and agents.</h2>
          </div>
          <div className="team-grid">
            {TEAM.map(([name, role, work]) => (
              <article className="team-card" key={name}>
                <span>{name.split(" ").map((part) => part[0]).join("").slice(0, 2)}</span>
                <div>
                  <h3>{name}</h3>
                  <strong>{role}</strong>
                  <p>{work}</p>
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="public-band compact-band">
          <div className="section-heading">
            <span className="eyebrow">Tech stack</span>
            <h2>The MVP combines structured data, document retrieval, and graph context.</h2>
          </div>
          <div className="stack-list">
            {STACK.map(([layer, tech]) => (
              <div key={layer}>
                <span>{layer}</span>
                <strong>{tech}</strong>
              </div>
            ))}
          </div>
        </section>

        <section className="builder-card">
          <div>
            <span className="eyebrow">About the builder</span>
            <h2>Placeholder builder note</h2>
            <p>
              Replace this with your personal buildathon story, role, and what
              you want judges to know about your RAG/retrieval work.
            </p>
          </div>
          <Link className="btn btn-primary" to="/login">Enter the demo</Link>
        </section>
      </main>
    </div>
  );
}
