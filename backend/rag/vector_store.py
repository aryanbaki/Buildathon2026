"""
Aryan — vector_store.py
ChromaDB collection management. Single source of truth for the vector store.
"""
from typing import Any

import chromadb
from chromadb.config import Settings as ChromaSettings
from backend.config import get_settings

settings = get_settings()
_client = None
_collection = None


def get_client() -> chromadb.Client:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path=settings.chroma_persist_path,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
    return _client


def get_collection():
    global _collection
    if _collection is None:
        _collection = get_client().get_or_create_collection(
            name=settings.chroma_collection_name,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def normalize_metadata(metadata: dict[str, Any]) -> dict[str, str | int | float | bool]:
    """Keep Chroma metadata filterable and JSON-safe."""
    normalized = {}
    for key, value in metadata.items():
        if value is None:
            continue
        if isinstance(value, (str, int, float, bool)):
            normalized[key] = value
        else:
            normalized[key] = str(value)
    return normalized


def build_where_filter(**filters: str | int | float | bool | None) -> dict | None:
    """Build a Chroma where clause from non-empty metadata filters."""
    clauses = []
    for key, value in filters.items():
        if value is None or value == "":
            continue
        clauses.append({key: {"$eq": value}})

    if not clauses:
        return None
    if len(clauses) == 1:
        return clauses[0]
    return {"$and": clauses}


def upsert_document(doc_id: str, text: str, metadata: dict, embedding: list[float] = None):
    """Add or update a document chunk in the vector store."""
    col = get_collection()
    kwargs = dict(
        ids=[doc_id],
        documents=[text],
        metadatas=[normalize_metadata(metadata)],
    )
    if embedding:
        kwargs["embeddings"] = [embedding]
    col.upsert(**kwargs)


def delete_document(doc_id: str):
    get_collection().delete(ids=[doc_id])


def collection_count() -> int:
    return get_collection().count()
