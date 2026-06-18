"""
Aryan — retriever.py
THE handoff interface. Teja calls query() directly — do not change the signature.

Contract:
    query(text, n, truck_id) -> list[{text, doc_id, truck_id, score, filename, doc_type}]
"""
from sentence_transformers import SentenceTransformer
from backend.rag.vector_store import get_collection
from backend.config import get_settings

settings = get_settings()
_model = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.embedding_model)
    return _model


def query(text: str, n: int = 5, truck_id: str = None) -> list[dict]:
    """
    Semantic search over fleet documents.

    Args:
        text:     Natural language query
        n:        Max results to return
        truck_id: Optional filter to a specific truck (e.g. "truck_84")

    Returns:
        List of dicts with keys:
            text, doc_id, truck_id, score, filename, doc_type, chunk_index
    """
    model = _get_model()
    embedding = model.encode(text).tolist()

    where_filter = None
    if truck_id:
        where_filter = {"truck_id": {"$eq": truck_id}}

    col = get_collection()
    results = col.query(
        query_embeddings=[embedding],
        n_results=min(n, col.count() or 1),
        where=where_filter,
        include=["documents", "metadatas", "distances"],
    )

    output = []
    if not results["ids"] or not results["ids"][0]:
        return output

    for i, chroma_id in enumerate(results["ids"][0]):
        meta = results["metadatas"][0][i]
        distance = results["distances"][0][i]
        score = round(1 - distance, 4)   # cosine distance → similarity

        output.append({
            "text": results["documents"][0][i],
            "doc_id": meta.get("doc_id", ""),
            "truck_id": meta.get("truck_id", ""),
            "filename": meta.get("filename", ""),
            "doc_type": meta.get("doc_type", ""),
            "chunk_index": int(meta.get("chunk_index", 0)),
            "score": score,
        })

    return sorted(output, key=lambda x: x["score"], reverse=True)
