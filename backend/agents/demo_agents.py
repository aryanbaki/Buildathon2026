"""
Demo agents — no Claude required.
Auto-used when ANTHROPIC_API_KEY is missing/invalid so the hackathon demo still runs.
"""
import re
from typing import Optional, Tuple
from sqlalchemy import text

from backend.database.db import get_db
from backend.rag.retriever import query as rag_query, query_with_filters, normalize_truck_id
from backend.agents.grounding import (
    NO_DOCUMENT_ANSWER,
    NO_HYBRID_ANSWER,
    filter_confident_sources,
    has_confident_sources,
)
from backend.agents.web_search_agent import search_fleet_context

_SQL_HINT = re.compile(
    r"\b(how much|how many|which truck|most profitable|expiring|count|spend|over \$|records?|total)\b",
    re.I,
)
_RAG_HINT = re.compile(
    r"\b(where|warranty|tax form|inspection|what does|what did|show me the|find the)\b",
    re.I,
)
_WEB_HINT = re.compile(
    r"\b(recall|nhtsa|fmcsa|dot regulation|diesel price|fuel price)\b",
    re.I,
)


def route(question: str, truck_id: str = None, trailer_id: str = None) -> dict:
    q = question.strip()
    truck_id = normalize_truck_id(truck_id)

    if _WEB_HINT.search(q):
        from backend.auth_status import tavily_configured
        if tavily_configured():
            return _run_web(q, truck_id, trailer_id)

    if _RAG_HINT.search(q) and not _SQL_HINT.search(q):
        return _run_rag(q, truck_id, trailer_id)

    if _SQL_HINT.search(q) and not _RAG_HINT.search(q):
        return _run_sql(q, truck_id)

    if _SQL_HINT.search(q) and _RAG_HINT.search(q):
        return _run_hybrid(q, truck_id, trailer_id)

    # Default: try RAG first, then SQL
    rag = _run_rag(q, truck_id, trailer_id)
    if rag.get("sources"):
        return rag
    return _run_sql(q, truck_id)


def _run_web(question: str, truck_id: str = None, trailer_id: str = None) -> dict:
    results = search_fleet_context(question, max_results=3)
    if not results:
        return {
            "answer": "No web results found for that question.",
            "query_type": "web",
            "sql_query": None,
            "sources": [],
            "demo_mode": True,
        }
    lines = [f"Based on public sources (demo mode, no Claude synthesis):"]
    sources = []
    for i, r in enumerate(results[:3]):
        title = r.get("title", "Source")
        snippet = (r.get("content") or "")[:200]
        lines.append(f"- {title}: {snippet}")
        sources.append({
            "doc_id": r.get("url") or f"web_{i}",
            "filename": title,
            "truck_id": truck_id or "",
            "trailer_id": trailer_id,
            "snippet": snippet,
            "score": float(r.get("score", 0.5)),
        })
    return {
        "answer": "\n".join(lines),
        "query_type": "web",
        "sql_query": None,
        "sources": sources,
        "demo_mode": True,
    }


def _run_sql(question: str, truck_id: str = None) -> dict:
    sql, label = _pick_sql(question, truck_id)
    if not sql:
        return {
            "answer": "Demo mode: couldn't map that question to SQL. Add a valid ANTHROPIC_API_KEY for full NL→SQL.",
            "query_type": "sql",
            "sql_query": None,
            "sources": [],
            "demo_mode": True,
        }

    try:
        with get_db() as db:
            result = db.execute(text(sql))
            rows = [dict(zip(result.keys(), row)) for row in result.fetchall()]
    except Exception as exc:
        return {
            "answer": f"SQL execution failed: {exc}",
            "query_type": "sql",
            "sql_query": sql,
            "sources": [],
            "demo_mode": True,
        }

    answer = _format_sql_answer(label, rows)
    return {
        "answer": answer,
        "query_type": "sql",
        "sql_query": sql,
        "sources": [],
        "raw_rows": rows[:20],
        "demo_mode": True,
    }


def _run_rag(question: str, truck_id: str = None, trailer_id: str = None) -> dict:
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
            "demo_mode": True,
        }

    confident = filter_confident_sources(chunks)
    top = confident[0]
    answer = (
        f"From {top['filename']} (truck {top['truck_id']}, score {top['score']}): "
        f"{top['text'][:400].strip()}{'…' if len(top['text']) > 400 else ''}"
    )
    sources = [
        {
            "doc_id": c["doc_id"],
            "filename": c["filename"],
            "truck_id": c["truck_id"],
            "trailer_id": c.get("trailer_id") or None,
            "snippet": c["text"][:200] + ("…" if len(c["text"]) > 200 else ""),
            "score": c["score"],
        }
        for c in confident[:3]
    ]
    return {
        "answer": answer,
        "query_type": "rag",
        "sql_query": None,
        "sources": sources,
        "demo_mode": True,
    }


def _run_hybrid(question: str, truck_id: str = None, trailer_id: str = None) -> dict:
    sql_result = _run_sql(question, truck_id)
    rag_result = _run_rag(question, truck_id, trailer_id)
    sql_rows = sql_result.get("raw_rows", [])
    rag_sources = rag_result.get("sources", [])

    if not sql_rows and not rag_sources:
        return {
            "answer": NO_HYBRID_ANSWER,
            "query_type": "hybrid",
            "sql_query": sql_result.get("sql_query"),
            "sources": [],
            "demo_mode": True,
        }

    parts = []
    if sql_rows:
        parts.append(sql_result["answer"])
    if rag_sources:
        parts.append(rag_result["answer"])

    return {
        "answer": " ".join(parts),
        "query_type": "hybrid",
        "sql_query": sql_result.get("sql_query"),
        "sources": rag_sources,
        "demo_mode": True,
    }


def _pick_sql(question: str, truck_id: Optional[str]) -> Tuple[Optional[str], str]:
    q = question.lower()
    unit_match = re.search(r"truck\s*#?\s*(\d+)", q)
    unit = unit_match.group(1) if unit_match else None
    tid = truck_id or (f"truck_{unit}" if unit else None)

    if "profitable" in q or "profit" in q:
        return _SQL_PROFITABILITY, "most profitable truck this quarter"

    if "expiring" in q and "registration" in q:
        return _SQL_EXPIRING_REGS, "trucks with expiring registrations"

    if "maintenance" in q and ("500" in q or "over" in q):
        return _SQL_MAINT_OVER_500, "maintenance over $500"

    if tid and ("parts" in q or "maintenance" in q or "spend" in q):
        return _SQL_TRUCK_MAINT_MTD.format(truck_id=tid), f"maintenance spend for {tid}"

    if "how many" in q and "truck" in q:
        return _SQL_ACTIVE_TRUCKS, "active truck count"

    if tid and ("fuel" in q or "diesel" in q):
        return _SQL_TRUCK_FUEL_QTR.format(truck_id=tid), f"fuel costs for {tid}"

    if tid:
        return _SQL_TRUCK_DOCS.format(truck_id=tid), f"documents for {tid}"

    return _SQL_FLEET_SUMMARY, "fleet summary"


def _format_sql_answer(label: str, rows: list[dict]) -> str:
    if not rows:
        return f"No records found for {label}."
    if len(rows) == 1 and len(rows[0]) <= 3:
        parts = [f"{k}: {v}" for k, v in rows[0].items()]
        return f"{label.title()} — " + ", ".join(parts)
    lines = [f"{label.title()} — {len(rows)} result(s):"]
    for row in rows[:5]:
        lines.append(" · " + ", ".join(f"{k}={v}" for k, v in row.items()))
    return "\n".join(lines)


_SQL_ACTIVE_TRUCKS = """
SELECT COUNT(*) AS active_trucks FROM trucks WHERE status = 'active';
"""

_SQL_EXPIRING_REGS = """
SELECT t.unit_number, d.filename, d.expiry_date, d.amount
FROM documents d
JOIN trucks t ON t.id = d.truck_id
WHERE d.doc_type = 'REGISTRATION'
  AND d.expiry_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days'
ORDER BY d.expiry_date;
"""

_SQL_MAINT_OVER_500 = """
SELECT t.unit_number, m.service_date, m.service_type, m.vendor, m.total_cost
FROM maintenance_records m
JOIN trucks t ON t.id = m.truck_id
WHERE m.total_cost > 500
ORDER BY m.total_cost DESC
LIMIT 10;
"""

_SQL_TRUCK_MAINT_MTD = """
SELECT COALESCE(SUM(m.total_cost), 0) AS maintenance_spend_mtd
FROM maintenance_records m
WHERE m.truck_id = '{truck_id}'
  AND EXTRACT(MONTH FROM m.service_date) = EXTRACT(MONTH FROM CURRENT_DATE)
  AND EXTRACT(YEAR FROM m.service_date) = EXTRACT(YEAR FROM CURRENT_DATE);
"""

_SQL_TRUCK_FUEL_QTR = """
SELECT COALESCE(SUM(f.total_cost), 0) AS fuel_spend_qtr
FROM fuel_records f
WHERE f.truck_id = '{truck_id}'
  AND EXTRACT(QUARTER FROM f.fill_date) = EXTRACT(QUARTER FROM CURRENT_DATE)
  AND EXTRACT(YEAR FROM f.fill_date) = EXTRACT(YEAR FROM CURRENT_DATE);
"""

_SQL_TRUCK_DOCS = """
SELECT filename, doc_type, doc_date, amount, vendor
FROM documents
WHERE truck_id = '{truck_id}'
ORDER BY doc_date DESC NULLS LAST
LIMIT 8;
"""

_SQL_FLEET_SUMMARY = """
SELECT
  (SELECT COUNT(*) FROM trucks WHERE status = 'active') AS active_trucks,
  (SELECT COUNT(*) FROM documents) AS total_documents,
  (SELECT COALESCE(SUM(total_cost), 0) FROM maintenance_records
    WHERE EXTRACT(MONTH FROM service_date) = EXTRACT(MONTH FROM CURRENT_DATE)) AS maint_spend_mtd;
"""

_SQL_PROFITABILITY = """
WITH costs AS (
  SELECT t.id AS truck_id, t.unit_number,
    COALESCE((SELECT SUM(total_cost) FROM maintenance_records m
              WHERE m.truck_id = t.id
                AND EXTRACT(QUARTER FROM m.service_date) = EXTRACT(QUARTER FROM CURRENT_DATE)
                AND EXTRACT(YEAR FROM m.service_date) = EXTRACT(YEAR FROM CURRENT_DATE)), 0)
  + COALESCE((SELECT SUM(total_cost) FROM fuel_records f
              WHERE f.truck_id = t.id
                AND EXTRACT(QUARTER FROM f.fill_date) = EXTRACT(QUARTER FROM CURRENT_DATE)
                AND EXTRACT(YEAR FROM f.fill_date) = EXTRACT(YEAR FROM CURRENT_DATE)), 0) AS operating_cost
  FROM trucks t WHERE t.status = 'active'
),
revenue AS (
  SELECT truck_id, COALESCE(SUM(amount), 0) AS trip_revenue
  FROM documents
  WHERE amount IS NOT NULL
    AND EXTRACT(QUARTER FROM doc_date) = EXTRACT(QUARTER FROM CURRENT_DATE)
    AND EXTRACT(YEAR FROM doc_date) = EXTRACT(YEAR FROM CURRENT_DATE)
  GROUP BY truck_id
)
SELECT c.unit_number,
       COALESCE(r.trip_revenue, 0) AS revenue,
       c.operating_cost,
       COALESCE(r.trip_revenue, 0) - c.operating_cost AS net_profit
FROM costs c
LEFT JOIN revenue r ON r.truck_id = c.truck_id
ORDER BY net_profit DESC
LIMIT 5;
"""
