"""
Teja — api/routes.py
All API endpoints. POST /ask is the main demo route.
"""
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.api.schemas import (
    AskRequest, AskResponse, UploadResponse,
    TruckResponse, DocumentResponse, FleetStatsResponse
)
from backend.agents.query_router import route
from backend.database.db import get_db_dep
from backend.database.models import Document, Truck

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    """Main AI query endpoint — routes to SQL, RAG, or hybrid agent."""
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    result = route(req.question, req.truck_id)
    return AskResponse(**result)


@router.post("/upload", response_model=UploadResponse)
async def upload(
    file: UploadFile = File(...),
    truck_id: str = Form(...),
    db: Session = Depends(get_db_dep),
):
    """Ingest a fleet document through Charan's DB pipeline, then embed it."""
    from backend.ingestion.pipeline import ingest_document_bytes
    from backend.rag.embed_documents import embed_and_store

    content = await file.read()

    try:
        doc = ingest_document_bytes(
            filename=file.filename,
            content=content,
            db=db,
            truck_id_override=truck_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    doc_type = doc.doc_type.value if doc.doc_type else "other"
    chroma_ids = embed_and_store(
        doc_id=doc.id,
        raw_text=doc.raw_text or "",
        truck_id=doc.truck_id,
        driver_id=doc.driver_id,
        doc_type=doc_type,
        filename=doc.filename,
        trailer_id=doc.trailer_id,
        source_path=doc.file_path,
        confidence_score=doc.confidence_score,
    )
    doc.chroma_doc_id = chroma_ids[0] if chroma_ids else None

    return UploadResponse(
        doc_id=doc.id,
        filename=doc.filename,
        truck_id=doc.truck_id,
        doc_type=doc_type,
        confidence_score=doc.confidence_score or 0.0,
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
