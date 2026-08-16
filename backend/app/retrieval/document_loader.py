"""
Load public-health documents, clean text, chunk, and attach metadata.

Supports .txt, .md, and .pdf (via pypdf). Sample documents are clearly flagged.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Iterator, List, Optional

from app.models.retrieval import ChunkMetadata, DocumentChunk

logger = logging.getLogger(__name__)

WHITESPACE_RE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """Normalize whitespace and strip control characters."""
    text = text.replace("\x00", " ")
    text = WHITESPACE_RE.sub(" ", text)
    return text.strip()


def extract_pdf_text(path: Path) -> str:
    """Extract text from a PDF using pypdf."""
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("pypdf is required for PDF ingestion. Install with: pip install pypdf") from exc

    reader = PdfReader(str(path))
    pages: List[str] = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text.strip():
            pages.append(page_text)
    return "\n\n".join(pages)


def load_file_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8")
    if suffix == ".pdf":
        return extract_pdf_text(path)
    raise ValueError(f"Unsupported file type: {suffix}")


def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> List[str]:
    """
    Split text into overlapping character-based chunks.
    Tries to break on sentence boundaries when possible.
    """
    text = clean_text(text)
    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            # Prefer breaking at sentence or paragraph boundary
            boundary = max(
                text.rfind(". ", start, end),
                text.rfind("\n", start, end),
                text.rfind("; ", start, end),
            )
            if boundary > start + chunk_size // 2:
                end = boundary + 1

        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)

        if end >= len(text):
            break
        start = max(end - chunk_overlap, start + 1)

    return chunks


def load_manifest(manifest_path: Path) -> List[dict]:
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    return data.get("documents", [])


def iter_document_chunks(
    source_dir: Path,
    manifest_path: Path,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> Iterator[DocumentChunk]:
    """Yield chunks for every document listed in the manifest."""
    entries = load_manifest(manifest_path)

    for entry in entries:
        file_name = entry["file_name"]
        file_path = source_dir / file_name
        if not file_path.exists():
            logger.warning("Skipping missing file: %s", file_path)
            continue

        logger.info("Loading document: %s", file_name)
        raw_text = load_file_text(file_path)
        pieces = chunk_text(raw_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        doc_id = entry["document_id"]
        for idx, piece in enumerate(pieces):
            meta = ChunkMetadata(
                document_id=doc_id,
                source=entry["source"],
                title=entry["title"],
                page=entry.get("page", 1) + idx,  # approximate page for text samples
                year=entry.get("year", 2024),
                disease=entry["disease"],
                url=entry["url"],
                chunk_index=idx,
                is_sample_data=entry.get("is_sample_data", True),
                file_name=file_name,
            )
            chunk_id = f"{doc_id}_chunk_{idx:03d}"
            yield DocumentChunk(chunk_id=chunk_id, text=piece, metadata=meta)


def save_processed_chunks(chunks: List[DocumentChunk], output_path: Path) -> None:
    """Persist processed chunks as JSON for inspection/debugging."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [
        {
            "chunk_id": c.chunk_id,
            "text": c.text,
            "metadata": c.metadata.model_dump(),
        }
        for c in chunks
    ]
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    logger.info("Saved %d processed chunks to %s", len(chunks), output_path)
