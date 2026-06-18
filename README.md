# Buildathon2026
## Folder Structure
text
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
│   │
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
