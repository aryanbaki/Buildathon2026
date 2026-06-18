"""
Aryan — embed_documents.py
Chunks document text and embeds into ChromaDB.
Called after Charan's ingestion pipeline writes a Document row.
"""
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
    words = text.split()
    if not words:
        return []
    chunks, i = [], 0
    while i < len(words):
        chunk = " ".join(words[i: i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


def embed_and_store(
    doc_id: str,
    raw_text: str,
    truck_id: str | None,
    driver_id: str | None,
    doc_type: str,
    filename: str,
) -> list[str]:
    """
    Chunk, embed, and upsert document into ChromaDB.
    Returns list of chroma doc IDs created (one per chunk).
    """
    model = get_model()
    chunks = chunk_text(raw_text)
    if not chunks:
        return []

    chroma_ids = []
    for idx, chunk in enumerate(chunks):
        chroma_id = f"{doc_id}_chunk_{idx}"
        embedding = model.encode(chunk).tolist()
        metadata = {
            "doc_id": doc_id,
            "truck_id": truck_id or "",
            "driver_id": driver_id or "",
            "doc_type": doc_type,
            "filename": filename,
            "chunk_index": idx,
            "total_chunks": len(chunks),
        }
        upsert_document(chroma_id, chunk, metadata, embedding)
        chroma_ids.append(chroma_id)

    return chroma_ids


def embed_batch(documents: list[dict]) -> dict[str, list[str]]:
    """
    Embed multiple documents. Each dict must have:
    doc_id, raw_text, truck_id, driver_id, doc_type, filename
    Returns {doc_id: [chroma_ids]}
    """
    results = {}
    for doc in documents:
        ids = embed_and_store(**doc)
        results[doc["doc_id"]] = ids
    return results
