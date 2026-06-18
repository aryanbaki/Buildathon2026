"""
Aryan — vector_store.py
ChromaDB collection management. Single source of truth for the vector store.
"""
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


def upsert_document(doc_id: str, text: str, metadata: dict, embedding: list[float] = None):
    """Add or update a document chunk in the vector store."""
    col = get_collection()
    kwargs = dict(
        ids=[doc_id],
        documents=[text],
        metadatas=[{k: str(v) for k, v in metadata.items() if v is not None}],
    )
    if embedding:
        kwargs["embeddings"] = [embedding]
    col.upsert(**kwargs)


def delete_document(doc_id: str):
    get_collection().delete(ids=[doc_id])


def collection_count() -> int:
    return get_collection().count()
