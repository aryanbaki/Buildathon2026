"""
Charan - batch_ingest.py
Batch ingestion utilities for loading a folder of fleet documents.

This is used for backfilling filing-cabinet style document dumps into the
same DB pipeline that powers API uploads.
"""
from pathlib import Path

from sqlalchemy.orm import Session

from backend.ingestion.pipeline import ingest_document, MetadataExtractor

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
    ".tiff",
    ".bmp",
    ".webp",
    ".docx",
    ".txt",
    ".text",
    ".csv",
}


def discover_documents(root_dir: str | Path) -> list[Path]:
    """Return supported document files under a folder, sorted for repeatability."""
    root = Path(root_dir)
    if not root.exists():
        raise FileNotFoundError(f"Document folder not found: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Expected a folder: {root}")

    files = [
        path for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return sorted(files)


def ingest_folder(
    root_dir: str | Path,
    db: Session,
    metadata_extractor: MetadataExtractor | None = None,
    truck_id_override: str | None = None,
) -> dict:
    """
    Ingest every supported document in a folder.

    Returns a summary with successful document IDs and per-file errors so one
    bad scan does not stop the whole backfill. The caller still controls the
    final commit for successfully inserted rows.
    """
    summary = {
        "root_dir": str(Path(root_dir)),
        "attempted": 0,
        "inserted": [],
        "errors": [],
    }

    for path in discover_documents(root_dir):
        summary["attempted"] += 1
        try:
            with db.begin_nested():
                doc = ingest_document(
                    str(path),
                    db,
                    metadata_extractor=metadata_extractor,
                    truck_id_override=truck_id_override,
                )
                summary["inserted"].append({
                    "doc_id": doc.id,
                    "filename": doc.filename,
                    "truck_id": doc.truck_id,
                    "doc_type": doc.doc_type.value if doc.doc_type else "other",
                })
        except Exception as exc:
            summary["errors"].append({
                "file_path": str(path),
                "error": str(exc),
            })

    return summary
