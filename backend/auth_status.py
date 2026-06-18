"""Credential helpers — know what's configured before calling external APIs."""
from functools import lru_cache

from backend.config import get_settings


def is_placeholder_key(value: str) -> bool:
    cleaned = (value or "").strip().lower()
    if not cleaned:
        return True
    placeholders = ("your-key", "changeme", "test-key", "sk-ant-...", "xxx")
    return any(p in cleaned for p in placeholders)


def anthropic_configured() -> bool:
    key = get_settings().anthropic_api_key
    return bool(key) and key.startswith("sk-ant-") and not is_placeholder_key(key)


def tavily_configured() -> bool:
    key = get_settings().tavily_api_key
    return bool(key) and not is_placeholder_key(key)


def use_demo_mode() -> bool:
    """Use rule-based agents when Claude isn't configured (buildathon fallback)."""
    settings = get_settings()
    if settings.demo_mode:
        return True
    return not anthropic_configured()


@lru_cache(maxsize=1)
def verify_anthropic_key() -> dict:
    """Lightweight live check — cached for the process lifetime."""
    if not anthropic_configured():
        return {"ok": False, "reason": "ANTHROPIC_API_KEY missing or placeholder in .env"}

    from anthropic import Anthropic

    settings = get_settings()
    client = Anthropic(api_key=settings.anthropic_api_key)
    try:
        client.messages.create(
            model=settings.routing_model,
            max_tokens=8,
            messages=[{"role": "user", "content": "ping"}],
        )
        return {"ok": True}
    except Exception as exc:
        name = type(exc).__name__
        message = str(exc)
        if "authentication" in message.lower() or name == "AuthenticationError":
            return {"ok": False, "reason": "ANTHROPIC_API_KEY rejected (invalid x-api-key)"}
        return {"ok": False, "reason": f"{name}: {message[:120]}"}
