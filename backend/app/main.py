"""
PublicHealth-AI FastAPI application entrypoint.

Phases 1-10 complete: health check, CORS, auth, agents, retrieval,
LLM response, and Responsible AI guardrails.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.agents import router as agents_router
from app.api.auth import router as auth_router
from app.api.query import router as query_router
from app.api.retrieval import router as retrieval_router
from app.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("publichealth_ai")

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=(
        "Evidence-Grounded Public Health Information & Disease Advisory Assistant. "
        "Provides general public-health information from verified sources — "
        "not a diagnosis or prescription system."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(retrieval_router)
app.include_router(agents_router)
app.include_router(query_router)
app.include_router(auth_router)


@app.on_event("startup")
async def on_startup() -> None:
    logger.info(
        "Starting %s (env=%s, llm_provider=%s)",
        settings.app_name,
        settings.app_env,
        settings.llm_provider,
    )


@app.get("/health", tags=["system"])
async def health_check():
    """
    Liveness/readiness probe for demos and deployment checks.
    """
    retrieval_ready = False
    chunk_count = 0
    try:
        from app.retrieval.retriever import get_retriever

        retriever = get_retriever()
        retrieval_ready = retriever.is_ready
        chunk_count = retriever.chunk_count
    except Exception:
        pass

    return {
        "status": "ok",
        "service": settings.app_name,
        "version": "0.1.0",
        "environment": settings.app_env,
        "retrieval": {
            "ready": retrieval_ready,
            "chunk_count": chunk_count,
        },
        "message": (
            "Evidence-grounded public health assistant API is running. "
            "This system does not diagnose or prescribe."
        ),
    }


@app.get("/", tags=["system"])
async def root():
    """Root redirect helper for browsers hitting the API base URL."""
    return {
        "service": settings.app_name,
        "docs": "/docs",
        "health": "/health",
    }
