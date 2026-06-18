"""
Charan — document_loader.py
Handles file ingestion: reads raw bytes → extracts text → returns normalized content.
Supports PDF, images (via OCR), DOCX, TXT, CSV.
"""
import os
from pathlib import Path
from typing import Optional

from backend.ingestion.ocr_processor import ocr_image


def load_document(file_path: str) -> dict:
    """
    Load a document from disk and extract its raw text.

    Returns:
        {
          "filename": str,
          "file_path": str,
          "raw_text": str,
          "file_type": str,
          "size_bytes": int,
          "error": str | None,
        }
    """
    path = Path(file_path)
    result = {
        "filename": path.name,
        "file_path": str(path.resolve()),
        "raw_text": "",
        "file_type": path.suffix.lower().lstrip("."),
        "size_bytes": path.stat().st_size if path.exists() else 0,
        "error": None,
    }

    if not path.exists():
        result["error"] = f"File not found: {file_path}"
        return result

    try:
        ext = path.suffix.lower()
        if ext == ".pdf":
            result["raw_text"] = _extract_pdf(path)
        elif ext in (".jpg", ".jpeg", ".png", ".tiff", ".bmp", ".webp"):
            result["raw_text"] = ocr_image(str(path))
        elif ext == ".docx":
            result["raw_text"] = _extract_docx(path)
        elif ext in (".txt", ".text"):
            result["raw_text"] = path.read_text(encoding="utf-8", errors="replace")
        elif ext == ".csv":
            result["raw_text"] = _extract_csv(path)
        else:
            result["error"] = f"Unsupported file type: {ext}"
    except Exception as e:
        result["error"] = str(e)

    return result


def load_from_bytes(filename: str, content: bytes) -> dict:
    """
    Load document from in-memory bytes (used in API upload endpoint).
    Writes to a temp file, extracts, then cleans up.
    """
    import tempfile
    suffix = Path(filename).suffix
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    try:
        result = load_document(tmp_path)
        result["filename"] = filename
    finally:
        os.unlink(tmp_path)
    return result


def _extract_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
        text = "\n\n".join(pages)
        # If PDF has no extractable text, try OCR on first page image
        if len(text.strip()) < 50:
            return _pdf_ocr_fallback(path)
        return text
    except ImportError:
        raise RuntimeError("pypdf not installed. Run: pip install pypdf")


def _pdf_ocr_fallback(path: Path) -> str:
    """Convert PDF pages to images and OCR them."""
    try:
        from pdf2image import convert_from_path
        import tempfile
        images = convert_from_path(str(path), dpi=200, first_page=1, last_page=3)
        texts = []
        for img in images:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                img.save(tmp.name)
                texts.append(ocr_image(tmp.name))
                os.unlink(tmp.name)
        return "\n\n".join(texts)
    except Exception as e:
        return f"[OCR fallback failed: {e}]"


def _extract_docx(path: Path) -> str:
    try:
        from docx import Document
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except ImportError:
        raise RuntimeError("python-docx not installed. Run: pip install python-docx")


def _extract_csv(path: Path) -> str:
    import csv
    rows = []
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(", ".join(row))
    return "\n".join(rows)
