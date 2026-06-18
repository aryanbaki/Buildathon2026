"""
Bootstrap fleet demo data end-to-end (no Databricks required).

1. Ensure DB tables exist and fleet entities are seeded
2. Ingest synthetic documents from data/raw_documents/
3. Embed all documents into ChromaDB

Usage (from repo root):
    python data/synthetic_data_generator/generate_documents.py
    python -m backend.scripts.bootstrap_fleet_data
"""
from pathlib import Path
from typing import Optional

from backend.database.db import get_db, init_db
from backend.database.models import Document, MaintenanceRecord, FuelRecord
from backend.database.seed_data import seed_entities
from backend.ingestion.batch_ingest import discover_documents
from backend.ingestion.synthetic_metadata import extract_synthetic_metadata
from backend.rag.embed_documents import embed_and_store

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DOCS_DIR = REPO_ROOT / "data" / "raw_documents"


def _metadata_extractor(raw_text: str) -> dict:
    # Pipeline only passes raw text; filename hints are embedded in content headers.
    return extract_synthetic_metadata(raw_text)


def _truck_override_for_path(path: Path) -> Optional[str]:
    for part in path.parts:
        if part.startswith("truck_"):
            return part
    return None


def ingest_and_embed_all(raw_dir: Optional[Path] = None) -> dict:
    raw_dir = raw_dir or RAW_DOCS_DIR
    summary = {
        "raw_dir": str(raw_dir),
        "ingest": {},
        "embedded_docs": 0,
        "chroma_chunks": 0,
        "errors": [],
    }

    if not raw_dir.exists():
        raise FileNotFoundError(
            f"No documents found at {raw_dir}. "
            "Run: python data/synthetic_data_generator/generate_documents.py"
        )

    with get_db() as db:
        for path in discover_documents(raw_dir):
            truck_override = _truck_override_for_path(path)
            try:
                from backend.ingestion.pipeline import ingest_document

                doc = ingest_document(
                    str(path),
                    db,
                    metadata_extractor=_metadata_extractor,
                    truck_id_override=truck_override,
                )
                chroma_ids = embed_and_store(
                    doc_id=doc.id,
                    raw_text=doc.raw_text or "",
                    truck_id=doc.truck_id,
                    driver_id=doc.driver_id,
                    trailer_id=doc.trailer_id,
                    doc_type=doc.doc_type.value if doc.doc_type else "other",
                    filename=doc.filename,
                    source_path=doc.file_path,
                    confidence_score=doc.confidence_score,
                )
                doc.chroma_doc_id = chroma_ids[0] if chroma_ids else None
                summary["embedded_docs"] += 1
                summary["chroma_chunks"] += len(chroma_ids)
            except Exception as exc:
                db.rollback()
                summary["errors"].append({"file": str(path), "error": str(exc)})

    return summary


def _clear_document_tables(db) -> None:
    db.query(MaintenanceRecord).delete()
    db.query(FuelRecord).delete()
    db.query(Document).delete()
    db.flush()


def bootstrap(reseed: bool = True, raw_dir: Optional[Path] = None) -> dict:
    init_db()
    with get_db() as db:
        if reseed:
            _clear_document_tables(db)
            seed_entities(db)

    result = ingest_and_embed_all(raw_dir=raw_dir)

    with get_db() as db:
        result["postgres_documents"] = db.query(Document).count()

    return result


def main():
    print("Bootstrapping fleet data...")
    print(f"  Raw docs dir: {RAW_DOCS_DIR}")
    result = bootstrap()
    print(f"  Postgres documents: {result['postgres_documents']}")
    print(f"  Embedded docs: {result['embedded_docs']}")
    print(f"  Chroma chunks: {result['chroma_chunks']}")
    if result["errors"]:
        print(f"  Errors: {len(result['errors'])}")
        for err in result["errors"][:5]:
            print(f"    - {err['file']}: {err['error']}")
    else:
        print("  No ingestion errors.")
    print("Done.")


if __name__ == "__main__":
    main()
