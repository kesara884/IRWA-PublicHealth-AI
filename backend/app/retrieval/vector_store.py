"""
Persistent vector store using NumPy + JSON metadata.

Designed for Python 3.13 compatibility when Chroma/FAISS wheels are unavailable.
Supports the same retrieval interface; can be swapped for FAISS/Chroma later.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import List, Optional

import numpy as np

from app.models.retrieval import DocumentChunk, RetrievalResult

logger = logging.getLogger(__name__)

EMBEDDINGS_FILE = "embeddings.npy"
METADATA_FILE = "metadata.json"
TEXTS_FILE = "texts.json"
INDEX_VERSION = "1.0"


class NumpyVectorStore:
    def __init__(self, persist_path: str) -> None:
        self.persist_path = Path(persist_path)
        self.persist_path.mkdir(parents=True, exist_ok=True)
        self._embeddings: Optional[np.ndarray] = None
        self._metadatas: List[dict] = []
        self._texts: List[str] = []
        self._ids: List[str] = []
        self._load_if_exists()

    def _load_if_exists(self) -> None:
        emb_path = self.persist_path / EMBEDDINGS_FILE
        meta_path = self.persist_path / METADATA_FILE
        texts_path = self.persist_path / TEXTS_FILE

        if not (emb_path.exists() and meta_path.exists() and texts_path.exists()):
            return

        self._embeddings = np.load(emb_path)
        payload = json.loads(meta_path.read_text(encoding="utf-8"))
        self._ids = payload["ids"]
        self._metadatas = payload["metadatas"]
        self._texts = json.loads(texts_path.read_text(encoding="utf-8"))
        logger.info("Loaded vector index with %d chunks from %s", len(self._ids), self.persist_path)

    @property
    def count(self) -> int:
        return len(self._ids)

    def reset(self) -> None:
        logger.warning("Resetting vector store at %s", self.persist_path)
        for name in (EMBEDDINGS_FILE, METADATA_FILE, TEXTS_FILE):
            path = self.persist_path / name
            if path.exists():
                path.unlink()
        tfidf = self.persist_path / "tfidf_vectorizer.pkl"
        if tfidf.exists():
            tfidf.unlink()
        self._embeddings = None
        self._metadatas = []
        self._texts = []
        self._ids = []

    def add_chunks(self, chunks: List[DocumentChunk], embeddings: np.ndarray) -> None:
        if len(chunks) != embeddings.shape[0]:
            raise ValueError("chunks and embeddings length mismatch")

        self._ids = [c.chunk_id for c in chunks]
        self._texts = [c.text for c in chunks]
        self._metadatas = [
            {
                "document_id": c.metadata.document_id,
                "source": c.metadata.source,
                "title": c.metadata.title,
                "page": c.metadata.page,
                "year": c.metadata.year,
                "disease": c.metadata.disease,
                "url": c.metadata.url,
                "chunk_index": c.metadata.chunk_index,
                "is_sample_data": c.metadata.is_sample_data,
                "file_name": c.metadata.file_name or "",
            }
            for c in chunks
        ]
        self._embeddings = embeddings.astype(np.float32)
        self._persist()
        logger.info("Indexed %d chunks in NumPy store at %s", len(self._ids), self.persist_path)

    def _persist(self) -> None:
        np.save(self.persist_path / EMBEDDINGS_FILE, self._embeddings)
        (self.persist_path / METADATA_FILE).write_text(
            json.dumps({"version": INDEX_VERSION, "ids": self._ids, "metadatas": self._metadatas}, indent=2),
            encoding="utf-8",
        )
        (self.persist_path / TEXTS_FILE).write_text(json.dumps(self._texts, indent=2), encoding="utf-8")

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
        disease_filter: Optional[str] = None,
    ) -> List[RetrievalResult]:
        if self.count == 0 or self._embeddings is None:
            logger.warning("Vector store is empty — run ingest_documents.py first")
            return []

        from app.retrieval.embeddings import cosine_scores

        scores = cosine_scores(query_embedding, self._embeddings)

        ranked_indices = np.argsort(scores)[::-1]
        results: List[RetrievalResult] = []

        for idx in ranked_indices:
            meta = self._metadatas[idx]
            if disease_filter and meta.get("disease", "").lower() != disease_filter.lower():
                continue

            score = round(float(scores[idx]), 4)
            if score <= 0:
                continue

            results.append(
                RetrievalResult(
                    chunk_id=self._ids[idx],
                    source=meta.get("source", "Unknown"),
                    title=meta.get("title", "Unknown"),
                    page=int(meta.get("page", 1)),
                    score=score,
                    text=self._texts[idx],
                    url=meta.get("url", ""),
                    document_id=meta.get("document_id", ""),
                    disease=meta.get("disease", ""),
                )
            )
            if len(results) >= top_k:
                break

        return results


# Alias for future FAISS/Chroma swap — same interface
VectorStore = NumpyVectorStore
