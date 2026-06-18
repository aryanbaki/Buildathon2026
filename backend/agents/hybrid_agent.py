"""
Teja — hybrid_agent.py
Runs both SQL and RAG in parallel, then merges into one grounded answer.
"""
from backend.agents.sql_agent import run as run_sql
from backend.agents.document_agent import run as run_rag
from backend.rag.answer_generator import generate_hybrid_answer
from backend.agents.grounding import NO_HYBRID_ANSWER, has_confident_sources


def run(question: str, truck_id: str = None, trailer_id: str = None) -> dict:
    sql_result = run_sql(question, truck_id)
    rag_result = run_rag(question, truck_id, trailer_id)

    sql_rows = sql_result.get("raw_rows", [])
    rag_sources = rag_result.get("sources", [])
    sql_has_data = bool(sql_rows)
    rag_has_data = has_confident_sources(rag_sources)

    if not sql_has_data and not rag_has_data:
        return {
            "answer": NO_HYBRID_ANSWER,
            "query_type": "hybrid",
            "sql_query": sql_result.get("sql_query"),
            "sources": [],
        }

    if not sql_has_data:
        return {
            "answer": rag_result["answer"],
            "query_type": "hybrid",
            "sql_query": sql_result.get("sql_query"),
            "sources": rag_sources,
        }

    if not rag_has_data:
        return {
            "answer": sql_result["answer"],
            "query_type": "hybrid",
            "sql_query": sql_result.get("sql_query"),
            "sources": [],
        }

    answer = generate_hybrid_answer(
        question=question,
        sql_answer=sql_result.get("answer", ""),
        rag_chunks=rag_sources,
        sql_rows=sql_rows,
    )

    return {
        "answer": answer,
        "query_type": "hybrid",
        "sql_query": sql_result.get("sql_query"),
        "sources": rag_sources,
    }
