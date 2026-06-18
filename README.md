# Buildathon2026

# Fleet Document Intelligence System 🚛📄

An AI-powered document intelligence platform for trucking fleets that transforms scattered paperwork into a searchable, structured knowledge system.

## Problem

Trucking carriers generate dozens of documents every week:

* Vehicle titles
* Registration renewals
* Tax forms
* Fuel receipts
* Maintenance invoices
* Insurance documents
* Driver certifications

These records often live in filing cabinets, glove boxes, shared drives, and email threads. Finding a specific document or answering operational questions can take hours.

Examples:

* Which trucks are most profitable?
* How much was spent on repairs last month?
* Where is the title for Truck 84?
* What documents are required to renew this plate?
* Which maintenance expenses are associated with a specific trailer?

## Solution

Fleet Document Intelligence automatically ingests fleet documents, extracts key information, links documents to trucks, drivers, and trailers, and enables natural-language search across the entire fleet.

The system combines:

* OCR for scanned documents
* Entity extraction
* Knowledge graph relationships
* SQL analytics
* Vector search (RAG)
* AI-powered question answering

This allows operators to ask questions in plain English and receive grounded, source-backed answers.

---

## Key Features

### Document Ingestion

Upload PDFs, images, receipts, tax forms, and maintenance records.

### OCR & Metadata Extraction

Automatically extract:

* Truck IDs
* VIN numbers
* Driver names
* Trailer numbers
* Dates
* Costs
* Vendors

### Entity Linking

Documents are connected to:

* Trucks
* Drivers
* Trailers

Creating a unified fleet knowledge base.

### Hybrid Search

Supports:

* Database queries
* Document retrieval
* Combined SQL + document reasoning

### Knowledge Graph

Visualize relationships between:

* Vehicles
* Drivers
* Trailers
* Documents
* Expenses

### AI Fleet Assistant

Ask questions such as:

> Which truck had the highest maintenance costs last quarter?

> Show me all tax documents associated with Truck 84.

> Why is Truck 12 less profitable than Truck 18?

---

## Project Architecture

```text
Documents
    ↓
OCR Processing
    ↓
Metadata Extraction
    ↓
Entity Linking
    ↓
Database + Knowledge Graph + Vector Store
    ↓
Query Router
    ↓
AI Assistant
```

---

## Folder Structure

```text
fleet-document-intelligence/
│
├── backend/
│   ├── ingestion/
│   ├── database/
│   ├── graph/
│   ├── rag/
│   ├── agents/
│   └── api/
│
├── frontend/
│   ├── pages/
│   ├── components/
│   └── services/
│
├── data/
│   ├── raw_documents/
│   ├── processed/
│   └── synthetic_data_generator/
│
├── vector_db/
├── knowledge_graph/
└── docs/
```

---

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite / PostgreSQL

### AI & NLP

* OpenAI API
* LangChain
* ChromaDB
* Tesseract OCR

### Knowledge Graph

* NetworkX
* PyVis

### Frontend

* React
* Vite
* Tailwind CSS

### Storage

* Local Storage
* PostgreSQL
* ChromaDB

---

## Database Entities

### Trucks

Stores:

* VIN
* Plate Number
* Make
* Model
* Year

### Drivers

Stores:

* Name
* License Number
* Contact Information

### Trailers

Stores:

* Trailer Details
* Registrations
* Inspections

### Documents

Stores:

* File Metadata
* Document Type
* Linked Entities

### Expenses

Stores:

* Fuel Costs
* Maintenance Costs
* Registration Fees
* Insurance Payments

---

## Sample Questions

### Document Retrieval

> Where is the title for Truck 84?

### Analytics Query

> How much did I spend on repairs last month?

### Hybrid Query

> Why is Truck 84 less profitable than Truck 86?

### Compliance Query

> Which registrations expire within 30 days?

---

## Synthetic Data

The project includes realistic trucking documents such as:

* Vehicle Titles
* Registrations
* Maintenance Invoices
* Fuel Receipts
* Tax Documents
* Driver Certifications
* Trailer Records

Synthetic data is intentionally noisy to simulate real-world fleet operations.

---

## Future Enhancements

* Automated renewal reminders
* Fleet profitability dashboards
* Multi-fleet support
* Driver performance analytics
* Predictive maintenance alerts
* Compliance monitoring
* Cloud deployment

---

## Impact

Fleet Document Intelligence reduces the time spent searching for paperwork, improves operational visibility, and enables trucking operators to make data-driven decisions using natural language.

Instead of digging through filing cabinets and email threads, fleet managers can simply ask:

> "Show me everything related to Truck 84."

and receive an immediate, evidence-backed answer.

---

## Team Goal

Build a reliable AI system that transforms unstructured fleet documents into actionable operational intelligence while ensuring every answer is grounded in real data and source documents.
