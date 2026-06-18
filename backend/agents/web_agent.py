"""
Teja — web_agent.py
Answers external fleet-context questions via Tavily (recalls, DOT regs, fuel prices).
Only used when the question is clearly about public/regulatory data, not fleet documents.
"""
import re
import anthropic
from backend.config import get_settings
from backend.agents.web_search_agent import (
    lookup_dot_regulation,
    lookup_fuel_prices,
    lookup_recall,
    search_fleet_context,
)

settings = get_settings()
client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

_RECALL_RE = re.compile(r"\brecall\b", re.I)
_DOT_RE = re.compile(r"\b(dot|fmcsa|regulation|compliance|hours.?of.?service|hos)\b", re.I)
_FUEL_PRICE_RE = re.compile(r"\b(diesel|fuel)\s+(price|cost)\b|\bfuel prices?\b", re.I)
_MAKE_MODEL_YEAR = re.compile(
    r"(?P<make>Freightliner|Kenworth|Peterbilt|Volvo|Mack)\s+(?P<model>\w+).*?(?P<year>20\d{2})",
    re.I,
)


def _search_for_question(question: str) -> list[dict]:
    if not settings.tavily_api_key:
        return []

    match = _MAKE_MODEL_YEAR.search(question)
    if _RECALL_RE.search(question) and match:
        return lookup_recall(match.group("make"), match.group("model"), int(match.group("year")))

    if _DOT_RE.search(question):
        return lookup_dot_regulation(question)

    if _FUEL_PRICE_RE.search(question):
        region = "Texas" if "texas" in question.lower() else "United States"
        return lookup_fuel_prices(region)

    return search_fleet_context(question)


def _synthesize(question: str, results: list[dict]) -> str:
    if not results:
        return (
            "I couldn't find current public information for that question. "
            "Set TAVILY_API_KEY or try a fleet-document question instead."
        )

    context = "\n\n".join(
        f"[{r.get('title', 'Source')}]({r.get('url', '')})\n{r.get('content', '')[:400]}"
        for r in results[:3]
    )
    try:
        msg = client.messages.create(
            model=settings.routing_model,
            max_tokens=500,
            system="Answer using ONLY the web search snippets provided. Cite source titles. Do not invent fleet-specific data.",
            messages=[{
                "role": "user",
                "content": f"Question: {question}\n\nWeb results:\n{context}",
            }],
        )
        return msg.content[0].text.strip()
    except Exception as e:
        return f"Web answer synthesis failed: {e}"


def run(question: str, truck_id: str = None, trailer_id: str = None) -> dict:
    results = _search_for_question(question)
    answer = _synthesize(question, results)

    sources = [
        {
            "doc_id": r.get("url", "") or f"web_{i}",
            "filename": r.get("title", "Web result"),
            "truck_id": truck_id or "",
            "trailer_id": trailer_id,
            "snippet": r.get("content", "")[:200],
            "score": float(r.get("score", 0.5)),
        }
        for i, r in enumerate(results[:3])
    ]

    return {
        "answer": answer,
        "query_type": "web",
        "sql_query": None,
        "sources": sources,
    }
