"""
Teja — grounding.py
Shared helpers to prevent hallucinated answers when retrieval or SQL returns nothing useful.
"""
from backend.config import get_settings

settings = get_settings()

NO_DOCUMENT_ANSWER = (
    "I couldn't find a document in the fleet records that answers this. "
    "Try uploading the relevant document first."
)

NO_HYBRID_ANSWER = (
    "I couldn't find enough fleet data to answer this reliably. "
    "The database and document search both came up short — try uploading "
    "the relevant files or rephrasing your question."
)


def confidence_threshold() -> float:
    return settings.confidence_threshold


def has_confident_sources(sources: list[dict], threshold: float | None = None) -> bool:
    """True when at least one source meets the similarity threshold."""
    if not sources:
        return False
    cutoff = threshold if threshold is not None else confidence_threshold()
    return max(s.get("score", 0) for s in sources) >= cutoff


def filter_confident_sources(sources: list[dict], threshold: float | None = None) -> list[dict]:
    cutoff = threshold if threshold is not None else confidence_threshold()
    return [s for s in sources if s.get("score", 0) >= cutoff]
