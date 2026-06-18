"""
Charan - pipeline.py
End-to-end document ingestion for the DB pipelines workstream.

Flow:
1. Load document text from disk or uploaded bytes.
2. Extract structured metadata.
3. Link metadata to truck, driver, and trailer rows.
4. Store the document and any structured records in PostgreSQL.
"""
from datetime import date
from uuid import uuid4

from sqlalchemy.orm import Session

from backend.database.models import DocType, Document, FuelRecord, MaintenanceRecord
from backend.ingestion.document_loader import load_document, load_from_bytes
from backend.ingestion.entity_linker import link_entities
from backend.ingestion.metadata_extractor import extract_metadata


def ingest_document(file_path: str, db: Session) -> Document:
    """
    Ingest a document from disk and persist the extracted data.

    The caller owns the database transaction. This function flushes so the
    returned Document has an ID available for downstream RAG/vector indexing.
    """
    loaded = load_document(file_path)
    return ingest_loaded_document(loaded, db)


def ingest_document_bytes(filename: str, content: bytes, db: Session) -> Document:
    """
    Ingest an uploaded document from in-memory bytes.

    Useful for the API upload route because it avoids duplicating pipeline
    logic outside Charan's ingestion layer.
    """
    loaded = load_from_bytes(filename, content)
    return ingest_loaded_document(loaded, db)


def ingest_loaded_document(loaded: dict, db: Session) -> Document:
    """
    Persist a loaded document dict from document_loader.py.

    Expected loaded keys: filename, file_path, raw_text, file_type, size_bytes,
    and error. Raises ValueError if the loader could not read the document.
    """
    if loaded.get("error"):
        raise ValueError(f"Document load failed: {loaded['error']}")

    raw_text = loaded.get("raw_text") or ""
    metadata = extract_metadata(raw_text)
    linked = link_entities(metadata, db)

    document = Document(
        id=f"doc_{uuid4().hex}",
        truck_id=linked.get("truck_id"),
        driver_id=linked.get("driver_id"),
        trailer_id=linked.get("trailer_id"),
        doc_type=_parse_doc_type(metadata.get("doc_type")),
        filename=loaded.get("filename") or "unknown",
        file_path=loaded.get("file_path"),
        raw_text=raw_text,
        extracted_metadata=metadata,
        doc_date=_parse_date(metadata.get("doc_date")),
        expiry_date=_parse_date(metadata.get("expiry_date")),
        amount=_parse_float(metadata.get("amount")),
        vendor=metadata.get("vendor"),
        notes=metadata.get("notes"),
        confidence_score=_parse_float(metadata.get("confidence")),
        is_verified=False,
    )

    db.add(document)
    db.flush()

    _create_structured_record(document, metadata, db)
    db.flush()

    return document


def _create_structured_record(document: Document, metadata: dict, db: Session) -> None:
    """Create typed SQL rows that make finance/maintenance questions easy."""
    if not document.truck_id:
        return

    if document.doc_type == DocType.MAINTENANCE:
        db.add(MaintenanceRecord(
            truck_id=document.truck_id,
            document_id=document.id,
            service_date=document.doc_date,
            service_type=metadata.get("service_type"),
            vendor=document.vendor,
            parts_cost=_parse_float(metadata.get("parts_cost")) or 0.0,
            labor_cost=_parse_float(metadata.get("labor_cost")) or 0.0,
            total_cost=document.amount or 0.0,
            odometer_at_service=_parse_int(metadata.get("odometer")),
            description=metadata.get("notes"),
        ))
        return

    if document.doc_type == DocType.FUEL_RECEIPT:
        db.add(FuelRecord(
            truck_id=document.truck_id,
            document_id=document.id,
            fill_date=document.doc_date,
            gallons=_parse_float(metadata.get("gallons")),
            price_per_gallon=_parse_float(metadata.get("price_per_gallon")),
            total_cost=document.amount,
            location=document.vendor,
            odometer=_parse_int(metadata.get("odometer")),
        ))


def _parse_doc_type(value: str | None) -> DocType:
    if not value:
        return DocType.OTHER
    try:
        return DocType(value)
    except ValueError:
        return DocType.OTHER


def _parse_date(value: str | date | None) -> date | None:
    if isinstance(value, date):
        return value
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _parse_float(value) -> float | None:
    if value is None:
        return None
    try:
        return round(float(value), 2)
    except (TypeError, ValueError):
        return None


def _parse_int(value) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
