"""
Application configuration via environment variables.
Secrets must never be hardcoded — use .env (see .env.example).
"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central settings loaded from environment / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_name: str = "PublicHealth-AI"
    app_env: str = "development"
    debug: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # CORS — comma-separated origins in env
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # JWT (used from Phase 11)
    jwt_secret_key: str = "change-me-to-a-long-random-secret"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    # LLM (used from Phase 8)
    llm_provider: str = "stub"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str = "https://api.openai.com/v1"

    # Retrieval (Phase 4+)
    top_k: int = 5
    embedding_provider: str = "tfidf"  # tfidf | sentence_transformers
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    vector_store_path: str = "./data/vector_store"
    sample_documents_path: str = "./data/sample_documents"
    processed_data_path: str = "./data/processed"
    chunk_size: int = 500
    chunk_overlap: int = 100

    # Agent HTTP base URL
    agent_api_base_url: str = "http://127.0.0.1:8000"

    @property
    def cors_origin_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton for FastAPI dependency injection."""
    return Settings()
