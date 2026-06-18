## Folder Structure

```text
fleet-document-intelligence/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   │
│   ├── ingestion/
│   │   ├── document_loader.py
│   │   ├── ocr_processor.py
│   │   ├── metadata_extractor.py
│   │   └── entity_linker.py
│   │
│   ├── database/
│   │   ├── models.py
│   │   ├── db.py
│   │   └── seed_data.py
│   │
│   ├── graph/
│   │   ├── graph_builder.py
│   │   ├── graph_queries.py
│   │   └── graph_schema.py
│   │
│   ├── rag/
│   │   ├── embed_documents.py
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   └── answer_generator.py
│   │
│   ├── agents/
│   │   ├── query_router.py
│   │   ├── sql_agent.py
│   │   ├── document_agent.py
│   │   └── hybrid_agent.py
│   │
│   └── api/
│       ├── routes.py
│       └── schemas.py
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── TruckView.jsx
│   │   │   └── AskAI.jsx
│   │   │
│   │   ├── components/
│   │   │   ├── UploadZone.jsx
│   │   │   ├── GraphView.jsx
│   │   │   ├── ChatPanel.jsx
│   │   │   └── DocumentCard.jsx
│   │   │
│   │   └── services/
│   │       └── api.js
│   │
│   └── package.json
│
├── data/
│   ├── raw_documents/
│   │   ├── truck_84/
│   │   │   ├── registration.pdf
│   │   │   ├── title.pdf
│   │   │   ├── maintenance_jan.pdf
│   │   │   └── fuel_receipt_01.jpg
│   │   │
│   │   ├── truck_85/
│   │   └── truck_86/
│   │
│   ├── processed/
│   │   ├── extracted_text/
│   │   ├── metadata/
│   │   └── embeddings/
│   │
│   └── synthetic_data_generator/
│       ├── generate_trucks.py
│       ├── generate_drivers.py
│       └── generate_documents.py
│
├── vector_db/
│   └── chroma/
│
├── knowledge_graph/
│   └── graph.json
│
└── docs/
    ├── architecture.md
    ├── schema.md
    └── demo_queries.md
```

### Folder Purpose

* **backend/**: Contains the Flask/FastAPI backend, database models, ingestion pipeline, RAG logic, graph logic, agents, and API routes.
* **frontend/**: Contains the React dashboard, truck views, upload interface, AI chat panel, graph view, and API service calls.
* **data/**: Stores raw synthetic trucking documents, processed text, extracted metadata, embeddings, and data generation scripts.
* **vector_db/**: Stores the local Chroma vector database used for document retrieval.
* **knowledge_graph/**: Stores graph data linking trucks, drivers, trailers, vendors, documents, and expenses.
* **docs/**: Contains architecture notes, database schema documentation, and demo questions for testing the system.

### Main System Flow

1. Documents are uploaded or generated inside `data/raw_documents/`.
2. The backend ingestion pipeline reads documents using `document_loader.py`.
3. OCR is handled by `ocr_processor.py`.
4. Important fields are extracted using `metadata_extractor.py`.
5. Documents are linked to trucks, drivers, trailers, and vendors using `entity_linker.py`.
6. Structured records are stored in the database.
7. Document text is embedded and stored in the vector database.
8. The knowledge graph connects related entities.
9. The AI agent routes user questions to SQL, document retrieval, or hybrid reasoning.
10. The frontend displays the dashboard, documents, graph relationships, and AI answers with evidence.
