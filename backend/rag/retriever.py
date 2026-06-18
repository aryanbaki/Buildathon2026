"""
Aryan — retriever.py
THE handoff interface. Teja calls query() directly — do not change the signature.

Contract:
    query(text, n, truck_id) -> list[{text, doc_id, truck_id, driver_id, trailer_id,
                                      score, filename, doc_type, source_page}]
"""
from sentence_transformers import SentenceTransformer
from backend.rag.vector_store import build_where_filter, get_collection
from backend.config import get_settings

settings = get_settings()
_model = None
DEFAULT_MIN_SCORE = 0.2


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
            text, doc_id, truck_id, driver_id, trailer_id, score, filename,
            doc_type, chunk_index, source_page
    """
    return query_with_filters(text=text, n=n, truck_id=truck_id)


def query_with_filters(
    text: str,
    n: int = 5,
    truck_id: str | None = None,
    driver_id: str | None = None,
    trailer_id: str | None = None,
    doc_type: str | None = None,
    min_score: float = DEFAULT_MIN_SCORE,
) -> list[dict]:
    """Semantic search with optional fleet metadata filters."""
    if not text or not text.strip():
        return []

    truck_id = normalize_truck_id(truck_id)
    driver_id = normalize_entity_id(driver_id, "driver")
    trailer_id = normalize_entity_id(trailer_id, "trailer")

    col = get_collection()
    count = col.count()
    if count == 0:
        return []

    model = _get_model()
    embedding = model.encode(text).tolist()
    where_filter = build_where_filter(
        truck_id=truck_id,
        driver_id=driver_id,
        trailer_id=trailer_id,
        doc_type=doc_type,
    )

    query_kwargs = {
        "query_embeddings": [embedding],
        "n_results": min(max(n, 1), count),
        "include": ["documents", "metadatas", "distances"],
    }
    if where_filter:
        query_kwargs["where"] = where_filter

    results = col.query(**query_kwargs)

    output = []
    if not results["ids"] or not results["ids"][0]:
        return output

    for i, chroma_id in enumerate(results["ids"][0]):
        meta = results["metadatas"][0][i]
        distance = results["distances"][0][i]
        score = max(0.0, round(1 - distance, 4))   # cosine distance -> similarity
        if score < min_score:
            continue

        output.append({
            "text": results["documents"][0][i],
            "doc_id": meta.get("doc_id", ""),
            "truck_id": meta.get("truck_id", ""),
            "driver_id": meta.get("driver_id", ""),
            "trailer_id": meta.get("trailer_id", ""),
            "filename": meta.get("filename", ""),
            "doc_type": meta.get("doc_type", ""),
            "source_path": meta.get("source_path", ""),
            "source_page": _to_optional_int(meta.get("source_page")),
            "chunk_index": int(meta.get("chunk_index", 0)),
            "chroma_id": chroma_id,
            "score": score,
        })

    return sorted(output, key=lambda x: x["score"], reverse=True)


def _to_optional_int(value):
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def normalize_truck_id(value: str | None) -> str | None:
    """Accept common truck ID formats while storing one canonical form."""
    if not value:
        return None
    cleaned = str(value).strip().lower().replace("-", "_").replace("#", "")
    if cleaned.startswith("truck_"):
        return cleaned
    if cleaned.startswith("trk_"):
        return f"truck_{cleaned.split('_', 1)[1].lstrip('0') or '0'}"
    if cleaned.startswith("t_"):
        return f"truck_{cleaned.split('_', 1)[1].lstrip('0') or '0'}"
    if cleaned.isdigit():
        return f"truck_{cleaned.lstrip('0') or '0'}"
    return cleaned


def normalize_entity_id(value: str | None, prefix: str) -> str | None:
    """Normalize simple driver/trailer IDs without changing unknown IDs."""
    if not value:
        return None
    cleaned = str(value).strip().lower().replace("-", "_").replace("#", "")
    if cleaned.startswith(f"{prefix}_"):
        return cleaned
    if prefix == "trailer" and cleaned.startswith("trl_"):
        return f"trailer_{cleaned.split('_', 1)[1].lstrip('0') or '0'}"
    return cleaned
