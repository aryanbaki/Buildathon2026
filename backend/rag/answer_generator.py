"""
Teja — answer_generator.py
Final answer synthesis using Claude Sonnet.
Takes structured data or retrieved chunks → plain English answer.
"""
import anthropic
from backend.config import get_settings

settings = get_settings()
client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

SYSTEM = """You are a fleet operations assistant. Answer the operator's question concisely
and accurately using ONLY the data provided. Never invent figures or details.
If data is missing, say so. Be direct — operators need fast, clear answers."""


def generate_sql_answer(question: str, sql: str, rows: list[dict]) -> str:
    if not rows:
        return (
            "No records found matching that query in the fleet database. "
            "I won't guess — upload the relevant documents or try a different time range."
        )
    prompt = f"""Question: {question}

SQL used: {sql}

Data returned ({len(rows)} rows):
{_format_rows(rows)}

Answer the question in 1-3 sentences using this data."""
    return _call(prompt)


def generate_rag_answer(question: str, chunks: list[dict]) -> str:
    context = "\n\n---\n\n".join(
        f"[{c['filename']} | truck {c['truck_id']}]\n{c['text']}" for c in chunks
    )
    prompt = f"""Question: {question}

Relevant document excerpts:
{context}

Answer based only on the excerpts above. Cite the filename when referencing specific content."""
    return _call(prompt)


def generate_hybrid_answer(question: str, sql_answer: str, rag_chunks: list[dict], sql_rows: list[dict]) -> str:
    context = "\n\n".join(
        f"[{c['filename']}]: {c['snippet']}" for c in rag_chunks[:3]
    )
    prompt = f"""Question: {question}

Structured data summary: {sql_answer}

Supporting document excerpts:
{context}

Combine both sources into one clear, grounded answer. Do not repeat information."""
    return _call(prompt)


def _call(prompt: str) -> str:
    try:
        msg = client.messages.create(
            model=settings.routing_model,
            max_tokens=600,
            system=SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text.strip()
    except Exception as e:
        return f"Answer generation failed: {e}"


def _format_rows(rows: list[dict]) -> str:
    if not rows:
        return "(empty)"
    keys = list(rows[0].keys())
    lines = [" | ".join(keys)]
    for row in rows[:10]:
        lines.append(" | ".join(str(row.get(k, "")) for k in keys))
    return "\n".join(lines)
