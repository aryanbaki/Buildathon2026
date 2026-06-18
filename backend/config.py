from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Anthropic
    anthropic_api_key: str = ""

    # PostgreSQL
    database_url: str = "postgresql://fleet_user:fleet_pass@localhost:5433/fleet_docs"

    # ChromaDB
    chroma_persist_path: str = "./vector_db/chroma"
    chroma_collection_name: str = "fleet_documents"

    # Models
    extraction_model: str = "claude-haiku-4-5-20251001"
    routing_model: str = "claude-sonnet-4-6"
    embedding_model: str = "all-MiniLM-L6-v2"

    # External search
    tavily_api_key: str = ""

    # RAG grounding — reject low-confidence retrievals to avoid hallucinations
    confidence_threshold: float = 0.65

    # App
    app_name: str = "Fleet Document Intelligence"
    debug: bool = False
    demo_mode: bool = False
    upload_dir: str = "./data/raw_documents"
    processed_dir: str = "./data/processed"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
