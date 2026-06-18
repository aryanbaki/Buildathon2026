"""
Aryan — embed_documents.py
Chunks document text and embeds into ChromaDB.
Called after Charan's ingestion pipeline writes a Document row.
"""
import re

from sentence_transformers import SentenceTransformer
from backend.rag.vector_store import upsert_document
from backend.config import get_settings

settings = get_settings()
_model = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.embedding_model)
    return _model


def chunk_text(text: str, chunk_size: int = 400, overlap: int = 80) -> list[str]:
    """Split text into overlapping word chunks."""
    words = re.sub(r"\s+", " ", text or "").strip().split()
    if not words:
        return []
    chunks, i = [], 0
    step = max(chunk_size - overlap, 1)
    while i < len(words):
        chunk = " ".join(words[i: i + chunk_size])
        chunks.append(chunk)
        i += step
    return chunks


def embed_and_store(
    doc_id: str,
    raw_text: str,
    truck_id: str | None,
    driver_id: str | None,
    doc_type: str,
    filename: str,
    trailer_id: str | None = None,
    source_path: str | None = None,
    source_page: int | None = None,
    confidence_score: float | None = None,
) -> list[str]:
    """
    Chunk, embed, and upsert document into ChromaDB.
    Returns list of chroma doc IDs created (one per chunk).
    """
    model = get_model()
    chunks = chunk_text(raw_text)
    if not chunks:
        return []

    embeddings = model.encode(chunks).tolist()
    chroma_ids = []
    for idx, chunk in enumerate(chunks):
        chroma_id = f"{doc_id}_chunk_{idx}"
        metadata = {
            "doc_id": doc_id,
            "truck_id": truck_id or "",
            "driver_id": driver_id or "",
            "trailer_id": trailer_id or "",
            "doc_type": doc_type,
            "filename": filename,
            "source_path": source_path or "",
            "source_page": source_page or "",
            "chunk_index": idx,
            "total_chunks": len(chunks),
            "confidence_score": confidence_score or "",
        }
        upsert_document(chroma_id, chunk, metadata, embeddings[idx])
        chroma_ids.append(chroma_id)

    return chroma_ids


def embed_batch(documents: list[dict]) -> dict[str, list[str]]:
    """
    Embed multiple documents. Each dict must have:
    doc_id, raw_text, truck_id, driver_id, doc_type, filename
    Optional: trailer_id, source_path, source_page, confidence_score
    Returns {doc_id: [chroma_ids]}
    """
    results = {}
    for doc in documents:
        ids = embed_and_store(**doc)
        results[doc["doc_id"]] = ids
    return results
