"""
Teja — hybrid_agent.py
Runs both SQL and RAG in parallel, then merges into one grounded answer.
"""
from backend.agents.sql_agent import run as run_sql
from backend.agents.document_agent import run as run_rag
from backend.rag.answer_generator import generate_hybrid_answer


def run(question: str, truck_id: str = None) -> dict:
    sql_result = run_sql(question, truck_id)
    rag_result = run_rag(question, truck_id)

    answer = generate_hybrid_answer(
        question=question,
        sql_answer=sql_result.get("answer", ""),
        rag_chunks=rag_result.get("sources", []),
        sql_rows=sql_result.get("raw_rows", []),
    )

    return {
        "answer": answer,
        "query_type": "hybrid",
        "sql_query": sql_result.get("sql_query"),
        "sources": rag_result.get("sources", []),
    }
