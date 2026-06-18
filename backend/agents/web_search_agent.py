from tavily import TavilyClient
from backend.config import get_settings

settings = get_settings()


def get_client() -> TavilyClient:
    if not settings.tavily_api_key:
        raise RuntimeError("TAVILY_API_KEY not set in .env")
    return TavilyClient(api_key=settings.tavily_api_key)


def search_fleet_context(query: str, max_results: int = 3) -> list[dict]:
    client = get_client()
    try:
        response = client.search(
            query=query,
            search_depth="basic",
            max_results=max_results,
            include_domains=[
                "fmcsa.dot.gov", "nhtsa.gov", "eia.gov",
                "trucking.org", "overdriveonline.com", "fleetowner.com",
            ],
        )
        return [
            {"title": r.get("title",""), "url": r.get("url",""),
             "content": r.get("content","")[:500], "score": r.get("score",0.0)}
            for r in response.get("results", [])
        ]
    except Exception as e:
        return [{"title": "Search failed", "url": "", "content": str(e), "score": 0.0}]


def lookup_recall(make: str, model: str, year: int) -> list[dict]:
    return search_fleet_context(f"NHTSA recall {year} {make} {model} commercial truck")


def lookup_dot_regulation(topic: str) -> list[dict]:
    return search_fleet_context(f"FMCSA DOT regulation {topic} trucking compliance 2025 2026")


def lookup_fuel_prices(region: str = "Texas") -> list[dict]:
    return search_fleet_context(f"current diesel fuel price {region} 2026")
