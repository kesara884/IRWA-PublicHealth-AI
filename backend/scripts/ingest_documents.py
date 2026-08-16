#!/usr/bin/env python3
"""
Ingest public-health documents into the vector store.

Pipeline:
  Document → text extraction → cleaning → chunking → metadata → embeddings → vector DB

Usage (from backend/):
  python scripts/ingest_documents.py
  python scripts/ingest_documents.py --reset
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.config import get_settings
from app.retrieval.document_loader import iter_document_chunks, save_processed_chunks
from app.retrieval.embeddings import create_embedding_service
from app.retrieval.vector_store import NumpyVectorStore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("ingest_documents")


def ingest(source_dir: Path, manifest_path: Path, reset: bool = False) -> None:
    settings = get_settings()

    logger.info("Starting ingestion from %s", source_dir)
    chunks = list(
        iter_document_chunks(
            source_dir=source_dir,
            manifest_path=manifest_path,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
    )

    if not chunks:
        logger.error("No chunks produced — check manifest and source files")
        sys.exit(1)

    processed_path = Path(settings.processed_data_path) / "chunks.json"
    save_processed_chunks(chunks, processed_path)

    embedder = create_embedding_service(settings.embedding_provider, settings.embedding_model)
    texts = [c.text for c in chunks]
    logger.info("Generating embeddings for %d chunks (provider=%s)...", len(texts), settings.embedding_provider)
    embeddings = embedder.fit_embed(texts)

    store = NumpyVectorStore(settings.vector_store_path)
    if reset:
        store.reset()

    store.add_chunks(chunks, embeddings)
    embedder.save(Path(settings.vector_store_path))

    logger.info("Ingestion complete")
    logger.info("  Documents source : %s", source_dir)
    logger.info("  Chunks indexed   : %d", len(chunks))
    logger.info("  Vector store     : %s", settings.vector_store_path)
    logger.info("  Embedding provider: %s", settings.embedding_provider)
    logger.info("  Processed output : %s", processed_path)


def main() -> None:
    settings = get_settings()
    parser = argparse.ArgumentParser(description="Ingest public-health documents")
    parser.add_argument("--source", type=Path, default=Path(settings.sample_documents_path))
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--reset", action="store_true", help="Clear vector store before ingest")
    args = parser.parse_args()

    source_dir = args.source.resolve()
    manifest_path = (args.manifest or source_dir / "documents_manifest.json").resolve()

    if not source_dir.exists():
        logger.error("Source directory not found: %s", source_dir)
        sys.exit(1)

    ingest(source_dir=source_dir, manifest_path=manifest_path, reset=args.reset)


if __name__ == "__main__":
    main()
