"""
Charan - storage.py
Persistent file storage helpers for uploaded fleet documents.

The ingestion pipeline stores original uploads before extraction so database
rows point to durable files instead of temporary paths.
"""
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
import re

from backend.config import get_settings

_SAFE_NAME_PATTERN = re.compile(r"[^A-Za-z0-9._-]+")


def save_upload_file(
    filename: str,
    content: bytes,
    upload_dir: str | None = None,
) -> Path:
    """
    Save uploaded bytes into the configured raw-document directory.

    Files are grouped by UTC date and prefixed with a UUID to avoid collisions.
    Returns the absolute path to the stored file.
    """
    if not filename or not filename.strip():
        filename = "upload.bin"

    settings = get_settings()
    base_dir = Path(upload_dir or settings.upload_dir)
    today = datetime.now(timezone.utc).strftime("%Y/%m/%d")
    target_dir = base_dir / today
    target_dir.mkdir(parents=True, exist_ok=True)

    safe_name = _safe_filename(filename)
    target_path = target_dir / f"{uuid4().hex}_{safe_name}"
    target_path.write_bytes(content)
    return target_path.resolve()


def _safe_filename(filename: str) -> str:
    name = Path(filename).name.strip().replace(" ", "_")
    name = _SAFE_NAME_PATTERN.sub("_", name)
    return name or "upload.bin"
