"""
Teja — api/routes.py
All API endpoints. POST /ask is the main demo route.
"""
import uuid
from datetime import date
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.api.schemas import (
    AskRequest, AskResponse, UploadResponse,
    TruckResponse, DocumentResponse, FleetStatsResponse
)
from backend.agents.query_router import route
from backend.database.db import get_db_dep
from backend.database.models import Document, Truck, DocType

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    """Main AI query endpoint — routes to SQL, RAG, or hybrid agent."""
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    result = route(req.question, req.truck_id, req.trailer_id)
    return AskResponse(**result)


@router.post("/upload", response_model=UploadResponse)
async def upload(
    file: UploadFile = File(...),
    truck_id: str = Form(...),
    db: Session = Depends(get_db_dep),
):
    """Ingest a fleet document: extract → link → embed."""
    from backend.ingestion.document_loader import load_from_bytes
    from backend.ingestion.metadata_extractor import extract_metadata
    from backend.ingestion.entity_linker import link_entities
    from backend.rag.embed_documents import embed_and_store

    content = await file.read()
    loaded = load_from_bytes(file.filename, content)

    if loaded.get("error"):
        raise HTTPException(status_code=422, detail=loaded["error"])

    meta = extract_metadata(loaded["raw_text"])
    entities = link_entities(meta, db)

    # Override truck_id from form if Claude didn't find it
    if not entities["truck_id"] and truck_id:
        entities["truck_id"] = truck_id

    doc_id = str(uuid.uuid4())
    doc_type_str = meta.get("doc_type", "other")
    try:
        doc_type = DocType(doc_type_str)
    except ValueError:
        doc_type = DocType.OTHER

    doc = Document(
        id=doc_id,
        truck_id=entities["truck_id"],
        driver_id=entities["driver_id"],
        trailer_id=entities["trailer_id"],
        doc_type=doc_type,
        filename=file.filename,
        file_path=loaded["file_path"],
        raw_text=loaded["raw_text"],
        extracted_metadata=meta,
        doc_date=meta.get("doc_date"),
        expiry_date=meta.get("expiry_date"),
        amount=meta.get("amount"),
        vendor=meta.get("vendor"),
        confidence_score=meta.get("confidence", 0.0),
    )
    db.add(doc)
    db.flush()

    chroma_ids = embed_and_store(
        doc_id=doc_id,
        raw_text=loaded["raw_text"],
        truck_id=entities["truck_id"],
        driver_id=entities["driver_id"],
        trailer_id=entities["trailer_id"],
        doc_type=doc_type_str,
        filename=file.filename,
        source_path=loaded.get("file_path"),
        confidence_score=meta.get("confidence"),
    )
    doc.chroma_doc_id = chroma_ids[0] if chroma_ids else None

    return UploadResponse(
        doc_id=doc_id,
        filename=file.filename,
        truck_id=entities["truck_id"],
        doc_type=doc_type_str,
        confidence_score=meta.get("confidence", 0.0),
        message=f"Ingested {len(chroma_ids)} chunks into vector store.",
    )


@router.get("/trucks", response_model=list[TruckResponse])
def get_trucks(db: Session = Depends(get_db_dep)):
    trucks = db.query(Truck).filter(Truck.status != "sold").all()
    return [TruckResponse(
        id=t.id, unit_number=t.unit_number, make=t.make,
        model=t.model, year=t.year, status=t.status
    ) for t in trucks]


@router.get("/trucks/{truck_id}/documents", response_model=list[DocumentResponse])
def get_truck_documents(truck_id: str, db: Session = Depends(get_db_dep)):
    docs = db.query(Document).filter(Document.truck_id == truck_id).all()
    return [DocumentResponse(
        id=d.id, filename=d.filename,
        doc_type=d.doc_type.value if d.doc_type else "other",
        doc_date=str(d.doc_date) if d.doc_date else None,
        expiry_date=str(d.expiry_date) if d.expiry_date else None,
        amount=d.amount, vendor=d.vendor,
        confidence_score=d.confidence_score,
    ) for d in docs]


@router.get("/stats", response_model=FleetStatsResponse)
def get_stats(db: Session = Depends(get_db_dep)):
    total_trucks = db.query(Truck).filter(Truck.status == "active").count()
    total_docs = db.query(Document).count()

    mtd = db.execute(text("""
        SELECT COALESCE(SUM(total_cost), 0) FROM maintenance_records
        WHERE EXTRACT(MONTH FROM service_date) = EXTRACT(MONTH FROM CURRENT_DATE)
          AND EXTRACT(YEAR FROM service_date) = EXTRACT(YEAR FROM CURRENT_DATE)
    """)).scalar()

    expiring = db.execute(text("""
        SELECT COUNT(*) FROM documents
        WHERE expiry_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days'
    """)).scalar()

    return FleetStatsResponse(
        total_trucks=total_trucks,
        total_documents=total_docs,
        total_spend_mtd=float(mtd or 0),
        expiring_soon=int(expiring or 0),
    )
