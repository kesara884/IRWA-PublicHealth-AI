"""
Text embedding services for the retrieval pipeline.

Primary (Python 3.13 compatible): TF-IDF via scikit-learn.
Optional upgrade: Sentence Transformers when torch/ST are available (Python 3.10–3.12).
"""

from __future__ import annotations

import logging
import pickle
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

VECTORIZER_FILENAME = "tfidf_vectorizer.pkl"


class BaseEmbeddingService(ABC):
    @abstractmethod
    def fit_embed(self, texts: List[str]) -> np.ndarray:
        """Fit on corpus (if needed) and return document embeddings."""

    @abstractmethod
    def embed_query(self, query: str) -> np.ndarray:
        """Embed a single query using the fitted model."""

    @abstractmethod
    def save(self, directory: Path) -> None:
        ...

    @classmethod
    @abstractmethod
    def load(cls, directory: Path, model_name: str) -> "BaseEmbeddingService":
        ...


class TfidfEmbeddingService(BaseEmbeddingService):
    """Lightweight IR embeddings — works on Python 3.13 without PyTorch."""

    def __init__(self, model_name: str = "tfidf") -> None:
        self.model_name = model_name
        self._vectorizer: Optional[TfidfVectorizer] = None

    def fit_embed(self, texts: List[str]) -> np.ndarray:
        logger.info("Fitting TF-IDF vectorizer on %d documents", len(texts))
        self._vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            max_features=8000,
        )
        matrix = self._vectorizer.fit_transform(texts)
        return matrix.toarray().astype(np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        if self._vectorizer is None:
            raise RuntimeError("TF-IDF vectorizer not fitted. Run ingestion first.")
        vec = self._vectorizer.transform([query]).toarray().astype(np.float32)
        return vec[0]

    def save(self, directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / VECTORIZER_FILENAME
        with path.open("wb") as f:
            pickle.dump(self._vectorizer, f)
        logger.info("Saved TF-IDF vectorizer to %s", path)

    @classmethod
    def load(cls, directory: Path, model_name: str) -> "TfidfEmbeddingService":
        path = directory / VECTORIZER_FILENAME
        if not path.exists():
            raise FileNotFoundError(f"TF-IDF vectorizer not found: {path}")
        service = cls(model_name=model_name)
        with path.open("rb") as f:
            service._vectorizer = pickle.load(f)
        return service


class SentenceTransformerEmbeddingService(BaseEmbeddingService):
    """Dense embeddings when sentence-transformers + torch are installed."""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self._model = None

    def _load_model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            logger.info("Loading Sentence Transformer: %s", self.model_name)
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def fit_embed(self, texts: List[str]) -> np.ndarray:
        model = self._load_model()
        vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        return np.asarray(vectors, dtype=np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        model = self._load_model()
        vec = model.encode([query], normalize_embeddings=True, show_progress_bar=False)[0]
        return np.asarray(vec, dtype=np.float32)

    def save(self, directory: Path) -> None:
        # ST models are loaded by name from HuggingFace cache; nothing to persist locally.
        directory.mkdir(parents=True, exist_ok=True)
        marker = directory / "embedding_provider.txt"
        marker.write_text(f"sentence_transformers:{self.model_name}", encoding="utf-8")

    @classmethod
    def load(cls, directory: Path, model_name: str) -> "SentenceTransformerEmbeddingService":
        return cls(model_name=model_name)


def create_embedding_service(provider: str, model_name: str) -> BaseEmbeddingService:
    provider = provider.lower().strip()
    if provider == "sentence_transformers":
        try:
            import sentence_transformers  # noqa: F401

            return SentenceTransformerEmbeddingService(model_name=model_name)
        except ImportError:
            logger.warning(
                "sentence-transformers unavailable — falling back to TF-IDF. "
                "Use Python 3.10–3.12 with torch for dense embeddings."
            )
    return TfidfEmbeddingService(model_name="tfidf")


def load_embedding_service(provider: str, model_name: str, store_path: Path) -> BaseEmbeddingService:
    provider = provider.lower().strip()
    vectorizer_path = store_path / VECTORIZER_FILENAME
    if vectorizer_path.exists():
        return TfidfEmbeddingService.load(store_path, model_name)
    if provider == "sentence_transformers":
        return SentenceTransformerEmbeddingService.load(store_path, model_name)
    raise FileNotFoundError(
        f"No embedding artifacts in {store_path}. Run: python scripts/ingest_documents.py"
    )


def cosine_scores(query_vec: np.ndarray, doc_matrix: np.ndarray) -> np.ndarray:
    """Compute cosine similarity between one query vector and all document vectors."""
    q = query_vec.reshape(1, -1)
    return cosine_similarity(q, doc_matrix).flatten()
