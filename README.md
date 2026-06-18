# Fleet Document Intelligence
> AI Buildathon Dallas 2026 — Statement 7

**Transform unstructured fleet documents into instant, grounded operational intelligence.**

[![GitHub](https://img.shields.io/badge/GitHub-Buildathon2026-181717?logo=github)](https://github.com/aryanbaki/Buildathon2026)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://python.org)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Claude](https://img.shields.io/badge/Claude-Haiku%20%2B%20Sonnet-D97706?logo=anthropic)](https://anthropic.com)

---

## The problem

Trucking carriers run on paper. An active fleet generates 50+ documents every week — titles, tax forms, fuel records, registration renewals, maintenance receipts. Nothing is searchable. Operators can't answer basic questions without digging through physical files.

## The solution

A system that ingests every fleet document, links each one to the correct truck/driver/trailer, and lets an operator ask any question in plain English — with every answer grounded in a real source document or database row.

---

## Architecture

```
Upload (PDF/IMG/CSV)
        │
        ▼
 Claude Haiku — extraction agent
 (entity linking: truck · driver · date · cost · doc type)
        │
   ┌────┴────┐
   ▼         ▼
PostgreSQL  ChromaDB
(structured) (embeddings)
   │         │
   └────┬────┘
        ▼
 Claude Sonnet — query router
 (classifies: SQL · RAG · hybrid)
        │
        ▼
 Grounded answer + source citations
```

---

## Team

| Person | Role | Owns |
|--------|------|------|
| **Yesh** | Frontend | `frontend/` · `synthetic_data_generator/` |
| **Charan** | DB Pipelines | `ingestion/` · `database/` |
| **Aryan** | RAG + Graph | `rag/` · `graph/` |
| **Teja** | AI Agents | `agents/` · `api/` · `app.py` |

---

## Repo structure

```
fleet-document-intelligence/
├── backend/
│   ├── app.py                          # Teja — FastAPI entrypoint
│   ├── config.py                       # shared config
│   ├── requirements.txt
│   ├── ingestion/
│   │   ├── document_loader.py          # Charan
│   │   ├── ocr_processor.py            # Charan
│   │   ├── metadata_extractor.py       # Charan — Claude Haiku extraction
│   │   └── entity_linker.py            # Charan — links doc to truck/driver
│   ├── database/
│   │   ├── models.py                   # Charan — SQLAlchemy schema
│   │   ├── db.py                       # Charan — session management
│   │   └── seed_data.py               # Charan — 15+ realistic documents
│   ├── graph/
│   │   ├── graph_builder.py            # Aryan
│   │   ├── graph_queries.py            # Aryan
│   │   └── graph_schema.py             # Aryan
│   ├── rag/
│   │   ├── embed_documents.py          # Aryan
│   │   ├── vector_store.py             # Aryan
│   │   ├── retriever.py                # Aryan — query(text, n, truck_id)
│   │   └── answer_generator.py         # Teja
│   ├── agents/
│   │   ├── query_router.py             # Teja — SQL · RAG · hybrid classifier
│   │   ├── sql_agent.py                # Teja
│   │   ├── document_agent.py           # Teja
│   │   └── hybrid_agent.py             # Teja
│   └── api/
│       ├── routes.py                   # Teja — POST /ask, POST /upload
│       └── schemas.py                  # Teja — shared request/response types
├── frontend/
│   └── src/
│       ├── pages/
│       │   ├── Dashboard.jsx           # Yesh
│       │   ├── TruckView.jsx           # Yesh
│       │   └── AskAI.jsx               # Yesh
│       ├── components/
│       │   ├── ChatPanel.jsx           # Yesh
│       │   ├── UploadZone.jsx          # Yesh
│       │   ├── DocumentCard.jsx        # Yesh
│       │   └── GraphView.jsx           # Yesh (uses Aryan's graph data)
│       └── services/
│           └── api.js                  # Yesh — mock + real API calls
└── data/
    └── synthetic_data_generator/
        ├── generate_trucks.py          # Yesh
        ├── generate_drivers.py         # Yesh
        └── generate_documents.py       # Yesh
```

---

## API contract (agreed interfaces — do not change without team sync)

### `POST /ask`
```json
Request:  { "question": "string", "truck_id": "truck_84 | null" }
Response: {
  "answer": "string",
  "query_type": "sql | rag | hybrid",
  "sql_query": "string | null",
  "sources": [
    { "doc_id": "string", "filename": "string", "truck_id": "string",
      "snippet": "string", "score": 0.97 }
  ]
}
```

### `retriever.query()` — Aryan → Teja
```python
def query(text: str, n: int = 5, truck_id: str = None) -> list[dict]:
    # returns: [{"text": str, "doc_id": str, "truck_id": str, "score": float}]
```

---

## Quick start

### Prerequisites
- Python 3.11+
- Node 18+
- Docker Desktop (for Postgres)
- Tesseract OCR (`brew install tesseract` / `apt install tesseract-ocr`) — only needed for PDF/image uploads

### Backend (from repo root)

```bash
git clone https://github.com/aryanbaki/Buildathon2026.git
cd Buildathon2026

python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r backend/requirements.txt

cp .env.example .env
# Edit .env: add ANTHROPIC_API_KEY (optional — demo mode works without it)
# DATABASE_URL defaults to Docker Postgres on port 5433

docker compose up -d
python data/synthetic_data_generator/generate_documents.py
python -m backend.scripts.bootstrap_fleet_data
uvicorn backend.app:app --reload --port 8000
```

Check everything is wired:

```bash
curl http://localhost:8000/health
```

Expected: `"db": true`, `"demo_mode": true` (until you add a real `ANTHROPIC_API_KEY`).

### Frontend
```bash
cd frontend
npm install

# Dev with mock API (no backend needed)
VITE_MOCK_API=true npm run dev

# Dev against real backend
VITE_API_URL=http://localhost:8000 npm run dev
```

### Generate synthetic data only

If you already ran the bootstrap above, skip this. To regenerate docs:

```bash
python data/synthetic_data_generator/generate_documents.py   # → data/raw_documents/
python -m backend.scripts.bootstrap_fleet_data               # → Postgres + Chroma
```

---

## Demo queries to test

```
"How much did truck 84 spend on parts last month?"          → hybrid
"Where's the tax form for truck 84?"                        → rag
"Which trucks have registrations expiring in 30 days?"      → sql
"What does the warranty on truck 85's engine say?"          → rag
"Which truck is most profitable this quarter?"              → sql
"Show me all maintenance records over $500"                 → sql
```

---

## Environment variables

```env
ANTHROPIC_API_KEY=sk-ant-...          # optional for demo; required for full Claude routing
DATABASE_URL=postgresql://fleet_user:fleet_pass@localhost:5433/fleet_docs
CHROMA_PERSIST_PATH=./vector_db/chroma
EXTRACTION_MODEL=claude-haiku-4-5-20251001
ROUTING_MODEL=claude-sonnet-4-6
DEMO_MODE=false                       # auto-on when ANTHROPIC_API_KEY is missing/placeholder
TAVILY_API_KEY=tvly-...               # optional; powers web search queries
CONFIDENCE_THRESHOLD=0.65
```

---

## Built at

**AI Buildathon Dallas 2026** — Irving, TX · June 18–19, 2026

Yesh Salapu · Charan · Aryan · Teja
