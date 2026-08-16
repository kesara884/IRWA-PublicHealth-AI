"""Retrieval API routes for Phase 4/5 testing (independent of agents)."""

import logging

from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.models.retrieval import SearchRequest, SearchResponse
from app.retrieval.retriever import get_retriever

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/retrieval", tags=["retrieval"])


@router.get("/status")
async def retrieval_status():
    """Check whether the vector store is populated and ready."""
    settings = get_settings()
    retriever = get_retriever()
    return {
        "status": "ready" if retriever.is_ready else "empty",
        "chunk_count": retriever.chunk_count,
        "vector_store_path": settings.vector_store_path,
        "embedding_provider": settings.embedding_provider,
        "embedding_model": settings.embedding_model,
        "top_k_default": settings.top_k,
        "message": (
            "Vector store is ready for retrieval."
            if retriever.is_ready
            else "Vector store is empty. Run: python scripts/ingest_documents.py"
        ),
    }


@router.post("/search", response_model=SearchResponse)
async def search_documents(payload: SearchRequest):
    """
    Test retrieval independently (Phase 5).
    Returns top-K evidence chunks with source metadata and scores.
    """
    query = payload.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    retriever = get_retriever()
    if not retriever.is_ready:
        raise HTTPException(
            status_code=503,
            detail="Vector store is empty. Run scripts/ingest_documents.py first.",
        )

    try:
        return retriever.search(query=query, top_k=payload.top_k)
    except Exception as exc:
        logger.exception("Retrieval failed")
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {exc}") from exc
