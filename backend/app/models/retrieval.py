"""Pydantic models for document chunks and retrieval results."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ChunkMetadata(BaseModel):
    document_id: str
    source: str
    title: str
    page: int = 1
    year: int = 2024
    disease: str
    url: str
    chunk_index: int = 0
    is_sample_data: bool = True
    file_name: Optional[str] = None


class DocumentChunk(BaseModel):
    chunk_id: str
    text: str
    metadata: ChunkMetadata


class RetrievalResult(BaseModel):
    source: str
    title: str
    page: int
    score: float
    text: str
    url: str
    document_id: str
    disease: str
    chunk_id: str


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    top_k: Optional[int] = Field(default=None, ge=1, le=20)


class SearchResponse(BaseModel):
    status: str
    query: str
    results: List[RetrievalResult]
    total_results: int


class IngestSummary(BaseModel):
    documents_processed: int
    chunks_created: int
    vector_store_path: str
    embedding_model: str
