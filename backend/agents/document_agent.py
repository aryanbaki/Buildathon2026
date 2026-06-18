"""
Teja — document_agent.py
Answers questions using RAG — retrieves relevant document chunks from ChromaDB
and generates a grounded, citation-backed answer.
"""
from backend.rag.retriever import query as rag_query, query_with_filters, normalize_truck_id
from backend.rag.answer_generator import generate_rag_answer
from backend.agents.grounding import (
    NO_DOCUMENT_ANSWER,
    filter_confident_sources,
    has_confident_sources,
)


def run(question: str, truck_id: str = None, trailer_id: str = None) -> dict:
    truck_id = normalize_truck_id(truck_id)
    if trailer_id:
        chunks = query_with_filters(question, n=5, truck_id=truck_id, trailer_id=trailer_id)
    else:
        chunks = rag_query(question, n=5, truck_id=truck_id)

    if not chunks or not has_confident_sources(chunks):
        return {
            "answer": NO_DOCUMENT_ANSWER,
            "query_type": "rag",
            "sql_query": None,
            "sources": [],
        }

    confident_chunks = filter_confident_sources(chunks)
    answer = generate_rag_answer(question, confident_chunks)

    sources = [
        {
            "doc_id": c["doc_id"],
            "filename": c["filename"],
            "truck_id": c["truck_id"],
            "trailer_id": c.get("trailer_id") or None,
            "snippet": c["text"][:200] + ("…" if len(c["text"]) > 200 else ""),
            "score": c["score"],
        }
        for c in confident_chunks
    ]

    return {
        "answer": answer,
        "query_type": "rag",
        "sql_query": None,
        "sources": sources,
    }
