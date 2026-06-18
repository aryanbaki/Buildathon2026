"""
Charan - pipeline.py
End-to-end document ingestion for the DB pipelines workstream.

Flow:
1. Store uploaded files or load existing files from disk.
2. Extract document text.
3. Extract structured metadata.
4. Link metadata to truck, driver, and trailer rows.
5. Store the document and any structured records in PostgreSQL.
"""
from collections.abc import Callable
from datetime import date
from uuid import uuid4

from sqlalchemy.orm import Session

from backend.database.models import DocType, Document, FuelRecord, MaintenanceRecord
from backend.ingestion.document_loader import load_document
from backend.ingestion.entity_linker import link_entities
from backend.ingestion.storage import save_upload_file

MetadataExtractor = Callable[[str], dict]


def ingest_document(
    file_path: str,
    db: Session,
    metadata_extractor: MetadataExtractor | None = None,
    truck_id_override: str | None = None,
) -> Document:
    """
    Ingest a document from disk and persist the extracted data.

    The caller owns the database transaction. This function flushes so the
    returned Document has an ID available for downstream RAG/vector indexing.
    """
    loaded = load_document(file_path)
    return ingest_loaded_document(
        loaded,
        db,
        metadata_extractor=metadata_extractor,
        truck_id_override=truck_id_override,
    )


def ingest_document_bytes(
    filename: str,
    content: bytes,
    db: Session,
    metadata_extractor: MetadataExtractor | None = None,
    truck_id_override: str | None = None,
    upload_dir: str | None = None,
) -> Document:
    """
    Persist an uploaded document, then ingest it through the same disk pipeline.

    Storing the original upload first gives operators an auditable source file
    path for every database row.
    """
    stored_path = save_upload_file(filename, content, upload_dir=upload_dir)
    return ingest_document(
        str(stored_path),
        db,
        metadata_extractor=metadata_extractor,
        truck_id_override=truck_id_override,
    )


def ingest_loaded_document(
    loaded: dict,
    db: Session,
    metadata_extractor: MetadataExtractor | None = None,
    truck_id_override: str | None = None,
) -> Document:
    """
    Persist a loaded document dict from document_loader.py.

    Expected loaded keys: filename, file_path, raw_text, file_type, size_bytes,
    and error. Raises ValueError if the loader could not read the document.
    """
    if loaded.get("error"):
        raise ValueError(f"Document load failed: {loaded['error']}")

    raw_text = loaded.get("raw_text") or ""
    extractor = metadata_extractor or _default_metadata_extractor
    metadata = extractor(raw_text)
    linked = link_entities(metadata, db)

    if not linked.get("truck_id") and truck_id_override:
        linked["truck_id"] = truck_id_override

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


def _default_metadata_extractor(raw_text: str) -> dict:
    """Lazy-load Claude extraction so callers can inject another parser."""
    from backend.ingestion.metadata_extractor import extract_metadata

    return extract_metadata(raw_text)


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
