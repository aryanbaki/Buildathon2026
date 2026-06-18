"""
Teja — query_router.py
Uses Claude Sonnet to classify the user's question into sql | rag | hybrid | web,
then delegates to the correct agent. Returns a unified response dict.

Falls back to demo_agents when ANTHROPIC_API_KEY is missing/invalid.
"""
import re
import anthropic
from backend.config import get_settings
from backend.auth_status import use_demo_mode, verify_anthropic_key

settings = get_settings()
client = anthropic.Anthropic(api_key=settings.anthropic_api_key) if settings.anthropic_api_key else None

_WEB_HINT = re.compile(
    r"\b(recall|nhtsa|fmcsa|dot regulation|diesel price|fuel price|compliance rule)\b",
    re.I,
)

ROUTER_PROMPT = """You are a query router for a fleet document intelligence system.

The system has three data sources:
1. PostgreSQL database — structured data: trucks, drivers, trailers, maintenance costs, fuel records, registration dates, document metadata
2. ChromaDB vector store — full text of fleet documents: maintenance receipts, fuel receipts, registration PDFs, tax forms, inspection reports
3. Tavily web search — public data only: NHTSA recalls, FMCSA/DOT regulations, regional diesel prices (NOT fleet-specific docs)

Classify the user's question into ONE of:
- "sql"    — answer requires only structured data (costs, dates, counts, comparisons, profitability)
- "rag"    — answer requires reading fleet document content (warranty text, form details, specific document lookup)
- "hybrid" — answer requires BOTH structured data AND fleet document content
- "web"    — answer requires public/regulatory/live market data (recalls, DOT rules, diesel prices)

Examples:
- "How much did truck 84 spend on maintenance last month?" → sql
- "What does the warranty on truck 85's engine say?" → rag
- "Where is the tax form for truck 84?" → rag
- "Which trucks have expiring registrations and what did each cost to register?" → hybrid
- "Which truck is most profitable this quarter?" → sql
- "What did the last inspection report say about truck 86?" → rag
- "Show me all maintenance records over $500 and what parts were replaced" → hybrid
- "Any NHTSA recall on the 2019 Freightliner Cascadia?" → web
- "Current diesel price in Texas?" → web
- "FMCSA hours of service rules for property carriers?" → web

Respond with ONLY a JSON object:
{"type": "sql" | "rag" | "hybrid" | "web", "reason": "one sentence explanation"}"""


def route(question: str, truck_id: str = None, trailer_id: str = None) -> dict:
    """
    Route a question to the right agent.

    Returns the full response dict:
    {
      "answer": str,
      "query_type": "sql" | "rag" | "hybrid" | "web",
      "sql_query": str | None,
      "sources": list[dict],
    }
    """
    if use_demo_mode():
        from backend.agents import demo_agents
        return demo_agents.route(question, truck_id, trailer_id)

    import json

    # Fast path for obvious external lookups
    if _WEB_HINT.search(question) and settings.tavily_api_key:
        from backend.agents.web_agent import run as run_web
        return run_web(question, truck_id, trailer_id)

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
    from backend.agents.web_agent import run as run_web

    if query_type == "sql":
        return run_sql(question, truck_id)
    elif query_type == "rag":
        return run_rag(question, truck_id, trailer_id)
    elif query_type == "web":
        return run_web(question, truck_id, trailer_id)
    else:
        return run_hybrid(question, truck_id, trailer_id)
