"""Agent API routes — HTTP/REST communication between agents."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from app.agents.query_agent import QueryAnalysisAgent
from app.agents.retrieval_agent import MedicalRetrievalAgent
from app.models.query import (
    AnalyzeRequest,
    QueryAnalysisResult,
    RetrieveAgentRequest,
    RetrieveAgentResponse,
)
from app.security.validation import validate_query

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/agents", tags=["agents"])

_query_agent = QueryAnalysisAgent()
_retrieval_agent = MedicalRetrievalAgent()


@router.post("/analyze", response_model=QueryAnalysisResult)
async def analyze_query(payload: AnalyzeRequest):
    """
    Agent 1 — Query Analysis Agent endpoint.
    Performs PII sanitization, NER, intent, and risk classification.
    """
    query = validate_query(payload.query)
    try:
        return _query_agent.analyze(query)
    except Exception as exc:
        logger.exception("Query analysis failed")
        raise HTTPException(status_code=500, detail=f"Query analysis failed: {exc}") from exc


@router.post("/retrieve", response_model=RetrieveAgentResponse)
async def retrieve_documents(payload: RetrieveAgentRequest):
    """
    Agent 2 — Medical Document Retrieval Agent endpoint.
    Called by Agent 1 over HTTP/REST with structured JSON.
    """
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        return _retrieval_agent.retrieve_from_request(payload)
    except Exception as exc:
        logger.exception("Retrieval agent failed")
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {exc}") from exc
