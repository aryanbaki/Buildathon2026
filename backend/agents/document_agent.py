"""
Teja — document_agent.py
Answers questions using RAG — retrieves relevant document chunks from ChromaDB
and generates a grounded, citation-backed answer.
"""
from backend.rag.retriever import query as rag_query
from backend.rag.answer_generator import generate_rag_answer


def run(question: str, truck_id: str = None) -> dict:
    chunks = rag_query(question, n=5, truck_id=truck_id)

    if not chunks:
        return {
            "answer": "No relevant documents found for this question. Try uploading the relevant files first.",
            "query_type": "rag",
            "sql_query": None,
            "sources": [],
        }

    answer = generate_rag_answer(question, chunks)

    sources = [
        {
            "doc_id": c["doc_id"],
            "filename": c["filename"],
            "truck_id": c["truck_id"],
            "snippet": c["text"][:200] + ("…" if len(c["text"]) > 200 else ""),
            "score": c["score"],
        }
        for c in chunks
    ]

    return {
        "answer": answer,
        "query_type": "rag",
        "sql_query": None,
        "sources": sources,
    }
