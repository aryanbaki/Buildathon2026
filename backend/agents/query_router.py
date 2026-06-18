"""
Teja — query_router.py
Uses Claude Sonnet to classify the user's question into sql | rag | hybrid,
then delegates to the correct agent. Returns a unified response dict.

This is the core of the system — every /ask request goes through here.
"""
import anthropic
from backend.config import get_settings

settings = get_settings()
client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

ROUTER_PROMPT = """You are a query router for a fleet document intelligence system.

The system has two data sources:
1. PostgreSQL database — structured data: trucks, drivers, maintenance costs, fuel records, registration dates, document metadata
2. ChromaDB vector store — full text of fleet documents: maintenance receipts, fuel receipts, registration PDFs, tax forms, inspection reports

Classify the user's question into ONE of:
- "sql"    — answer requires only structured data (costs, dates, counts, comparisons)
- "rag"    — answer requires reading document content (warranty text, form details, specific document lookup)
- "hybrid" — answer requires BOTH structured data AND document content

Examples:
- "How much did truck 84 spend on maintenance last month?" → sql
- "What does the warranty on truck 85's engine say?" → rag
- "Where is the tax form for truck 84?" → rag
- "Which trucks have expiring registrations and what did each cost to register?" → hybrid
- "Which truck is most profitable this quarter?" → sql
- "What did the last inspection report say about truck 86?" → rag
- "Show me all maintenance records over $500 and what parts were replaced" → hybrid

Respond with ONLY a JSON object:
{"type": "sql" | "rag" | "hybrid", "reason": "one sentence explanation"}"""


def route(question: str, truck_id: str = None) -> dict:
    """
    Route a question to the right agent.

    Returns the full response dict:
    {
      "answer": str,
      "query_type": "sql" | "rag" | "hybrid",
      "sql_query": str | None,
      "sources": list[dict],
    }
    """
    import json, re

    # Step 1: Classify
    try:
        msg = client.messages.create(
            model=settings.routing_model,
            max_tokens=200,
            messages=[{
                "role": "user",
                "content": f"{ROUTER_PROMPT}\n\nQuestion: {question}",
            }],
        )
        raw = msg.content[0].text.strip()
        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        classification = json.loads(raw)
        query_type = classification.get("type", "hybrid")
    except Exception:
        query_type = "hybrid"   # safe fallback

    # Step 2: Delegate
    from backend.agents.sql_agent import run as run_sql
    from backend.agents.document_agent import run as run_rag
    from backend.agents.hybrid_agent import run as run_hybrid

    if query_type == "sql":
        return run_sql(question, truck_id)
    elif query_type == "rag":
        return run_rag(question, truck_id)
    else:
        return run_hybrid(question, truck_id)
