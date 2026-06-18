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

A system that ingests every fleet document, links each one to the correct truck, driver, and trailer, and lets an operator ask any question in plain English — with every answer grounded in a real source document or database row.

---

## Architecture

```mermaid
flowchart LR
    A[Upload PDF, image, or CSV] --> B[Claude Haiku extraction]
    B --> C[Entity linking: truck, driver, trailer, date, cost, doc type]
    C --> D[(PostgreSQL structured records)]
    C --> E[(ChromaDB document embeddings)]
    C --> F[Knowledge graph relationships]
    D --> G[Claude Sonnet query router]
    E --> G
    F --> G
    G --> H[SQL, RAG, or hybrid answer]
    H --> I[Grounded answer plus source citations]
```

The graph module is intentional, not extra scope. It builds a lightweight knowledge graph across trucks, drivers, trailers, vendors, documents, and expenses so the system can answer relationship questions such as which trailer was tied to Truck 84 during a maintenance event or which driver was associated with an expiring registration.

---

## Team

| Person | Role | Owns |
|--------|------|------|
| **Yesh** | Frontend | `frontend/` · `synthetic_data_generator/` |
| **Charan** | DB Pipelines | `ingestion/` · `database/` |
| **Aryan** | RAG + Graph | `rag/` · `graph/` |
| **Teja** | AI Agents | `agents/` · `api/` · `app.py` |

Aryan's branch focuses on the RAG/retrieval contract: retrieve the right source documents, preserve citations, support truck/driver/trailer filters, expose graph relationships, and return "I don't know based on the uploaded documents" when the evidence is missing.

---

## Repo structure

```text
fleet-document-intelligence/
├── backend/
│   ├── app.py                          # Teja — FastAPI entrypoint
│   ├── config.py                       # shared config
│   ├── requirements.txt
│   ├── ingestion/
│   │   ├── document_loader.py          # Charan
│   │   ├── ocr_processor.py            # Charan
│   │   ├── metadata_extractor.py       # Charan — Claude Haiku extraction
│   │   └── entity_linker.py            # Charan — links doc to truck/driver/trailer
│   ├── database/
│   │   ├── models.py                   # Charan — SQLAlchemy schema
│   │   ├── db.py                       # Charan — session management
│   │   └── seed_data.py                # Charan — realistic fleet seed data
│   ├── graph/
│   │   ├── graph_builder.py            # Aryan — relationship graph export
│   │   ├── graph_queries.py            # Aryan — graph retrieval helpers
│   │   └── graph_schema.py             # Aryan — graph node/edge types
│   ├── rag/
│   │   ├── embed_documents.py          # Aryan — chunking + embeddings
│   │   ├── vector_store.py             # Aryan — ChromaDB collection helpers
│   │   ├── retriever.py                # Aryan — query(text, n, truck_id)
│   │   └── answer_generator.py         # Teja — final answer synthesis
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
        ├── generate_trailers.py        # Yesh
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

### `retriever.query()` — Aryan -> Teja

```python
def query(text: str, n: int = 5, truck_id: str = None) -> list[dict]:
    # returns: [{
    #   "text": str,
    #   "doc_id": str,
    #   "truck_id": str,
    #   "driver_id": str,
    #   "trailer_id": str,
    #   "filename": str,
    #   "doc_type": str,
    #   "source_page": int | None,
    #   "score": float
    # }]
```

---

## Aryan's RAG and graph retrieval phase

The RAG layer is responsible for turning messy fleet documents into searchable, citation-ready evidence.

* `embed_documents.py` chunks extracted document text, attaches metadata, embeds each chunk, and stores it in ChromaDB.
* `vector_store.py` manages the Chroma collection and keeps metadata filterable by truck, driver, trailer, document type, filename, and source page.
* `retriever.py` performs semantic search, applies optional fleet filters, enforces a confidence floor, and returns source-ready chunks.
* `graph_builder.py` exports a truck/driver/trailer/document/vendor graph for relationship retrieval.
* `graph_queries.py` provides graph helpers for truck, trailer, vendor, and document relationship questions.

---

## Seed data scope

The MVP should seed at least 40-50 documents so the demo matches the real fleet workload of 50+ documents per week. The seeded dataset should cover 8-10 document types, including:

* maintenance receipts
* repair invoices
* fuel logs
* fuel receipts
* registrations
* trailer registrations
* titles
* tax forms
* inspection reports
* insurance documents

These documents should be distributed across multiple trucks, drivers, trailers, vendors, dates, and document states so the dashboard and Ask AI workflow feel like a real weekly operations queue instead of a small sample set.

---

## Realistic document messiness

The synthetic document generator should create messy fleet paperwork, not only clean structured PDFs. `generate_documents.py` should include:

* OCR-style typos such as `TRK-084`, `Truck #84`, `Truck84`, and `T-84` referring to the same truck.
* Inconsistent trailer IDs such as `TRL-204`, `Trailer 204`, and `204-T`.
* Mixed date formats such as `06/18/2026`, `June 18, 2026`, and `2026-06-18`.
* Missing or partial fields, especially vendor names, VIN fragments, driver names, and totals.
* Scanned receipt artifacts such as faint totals, duplicated lines, crooked table text, and handwritten-style notes.
* Multi-page PDFs with tables, line items, and page-level citations.

This is important because the system is being judged on whether it can handle realistic trucking documents, including noisy scans and inconsistent fleet naming.

---

## How we prevent hallucinations

The assistant should only answer from retrieved documents or structured database records. If the needed evidence is not found, it returns a clear "I don't know based on the uploaded documents" response instead of guessing.

* Answers include citations with document name, page, and relevant snippet whenever possible.
* Low-confidence retrieval results are treated as missing evidence, not as permission to infer.
* Structured fields such as `truck_id`, `driver_id`, and `trailer_id` must come from extracted metadata or linked records before they appear in an answer.

---

## Quick start

### Prerequisites

* Python 3.11+
* Node 18+
* PostgreSQL 15+
* Tesseract OCR (`brew install tesseract` / `apt install tesseract-ocr`)

### Backend

```bash
git clone https://github.com/aryanbaki/Buildathon2026.git
cd Buildathon2026/backend

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Add ANTHROPIC_API_KEY and DATABASE_URL to .env

python -m database.db        # creates tables
python -m database.seed_data # seeds fleet documents

uvicorn app:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install

# Dev with mock API (no backend needed)
VITE_MOCK_API=true npm run dev

# Dev against real backend
VITE_API_URL=http://localhost:8000 npm run dev
```

### Generate synthetic data

```bash
cd data/synthetic_data_generator
python generate_trucks.py
python generate_drivers.py
python generate_trailers.py
python generate_documents.py   # creates PDFs in data/raw_documents/
```

---

## Demo queries to test

```text
"How much did truck 84 spend on parts last month?"          -> hybrid
"Where's the tax form for truck 84?"                        -> rag
"Which trailers linked to truck 84 have expiring docs?"     -> hybrid
"Which trucks have registrations expiring in 30 days?"      -> sql
"What does the warranty on truck 85's engine say?"          -> rag
"Which truck is most profitable this quarter?"              -> sql
"Show me all maintenance records over $500"                 -> sql
```

---

## Environment variables

```env
ANTHROPIC_API_KEY=sk-ant-...
DATABASE_URL=postgresql://fleet_user:fleet_pass@localhost:5432/fleet_docs
CHROMA_PERSIST_PATH=./vector_db/chroma
EXTRACTION_MODEL=claude-haiku-4-5-20251001
ROUTING_MODEL=claude-sonnet-4-6
```

---

## Built at

**AI Buildathon Dallas 2026** — Irving, TX · June 18–19, 2026

Yesh Salapu · Charan · Aryan · Teja
