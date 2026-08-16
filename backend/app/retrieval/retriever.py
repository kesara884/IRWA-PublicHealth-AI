"""
Top-K document retriever over the vector store.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from app.config import get_settings
from app.models.retrieval import RetrievalResult, SearchResponse
from app.retrieval.embeddings import (
    create_embedding_service,
    load_embedding_service,
)
from app.retrieval.vector_store import NumpyVectorStore

logger = logging.getLogger(__name__)


class DocumentRetriever:
    def __init__(self) -> None:
        settings = get_settings()
        self.top_k = settings.top_k
        self.store_path = Path(settings.vector_store_path)
        self.store = NumpyVectorStore(settings.vector_store_path)

        if self.store.count > 0:
            self.embedder = load_embedding_service(
                settings.embedding_provider,
                settings.embedding_model,
                self.store_path,
            )
        else:
            self.embedder = create_embedding_service(
                settings.embedding_provider,
                settings.embedding_model,
            )

    @property
    def is_ready(self) -> bool:
        return self.store.count > 0

    @property
    def chunk_count(self) -> int:
        return self.store.count

    def search(
        self,
        query: str,
        top_k: Optional[int] = None,
        disease_filter: Optional[str] = None,
    ) -> SearchResponse:
        k = top_k or self.top_k
        logger.info("Retrieval search: query=%r top_k=%d", query[:120], k)

        query_vec = self.embedder.embed_query(query)
        results: List[RetrievalResult] = self.store.search(
            query_embedding=query_vec,
            top_k=k,
            disease_filter=disease_filter,
        )

        status = "success" if results else "no_results"
        logger.info("Retrieval completed: %d result(s)", len(results))

        return SearchResponse(
            status=status,
            query=query,
            results=results,
            total_results=len(results),
        )


@lru_cache
def get_retriever() -> DocumentRetriever:
    return DocumentRetriever()
