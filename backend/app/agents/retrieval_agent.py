"""
Agent 2 — Medical Document Retrieval Agent

Receives structured query from Agent 1, builds a search query,
performs vector search, and returns evidence with metadata.
"""

from __future__ import annotations

import logging
from typing import List, Optional

from app.config import get_settings
from app.models.query import EntityResult, QueryAnalysisResult, RetrieveAgentRequest, RetrieveAgentResponse
from app.models.retrieval import RetrievalResult
from app.retrieval.retriever import get_retriever

logger = logging.getLogger(__name__)


DISEASE_FILTER_MAP = {
    "dengue": "Dengue",
    "malaria": "Malaria",
    "tuberculosis": "Tuberculosis",
    "influenza": "Influenza",
    "covid-19": "COVID-19",
    "ebola": "Ebola",
    "cholera": "Cholera",
    "typhoid": "Typhoid",
    "general health": "General Health",
}


class MedicalRetrievalAgent:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.retriever = get_retriever()

    def build_search_query(self, analysis: QueryAnalysisResult) -> str:
        """Combine original query with extracted entities for better retrieval."""
        parts: List[str] = [analysis.sanitized_query]

        if analysis.entities.disease:
            parts.append(" ".join(analysis.entities.disease))
        if analysis.entities.medical_topic:
            parts.append(" ".join(analysis.entities.medical_topic))
        if analysis.intent and analysis.intent not in {"GENERAL_HEALTH", "UNSUPPORTED_MEDICAL_REQUEST"}:
            parts.append(analysis.intent.lower().replace("_", " "))

        return " ".join(parts)

    def retrieve(
        self,
        analysis: QueryAnalysisResult,
        top_k: Optional[int] = None,
    ) -> RetrieveAgentResponse:
        logger.info("Agent 2 started: document retrieval")

        if not self.retriever.is_ready:
            logger.error("Vector store is empty")
            return RetrieveAgentResponse(
                status="no_index",
                results=[],
                total_results=0,
                search_query="",
            )

        search_query = self.build_search_query(analysis)
        disease_filter = None
        if len(analysis.entities.disease) == 1:
            raw = analysis.entities.disease[0].lower()
            disease_filter = DISEASE_FILTER_MAP.get(raw, analysis.entities.disease[0].title())

        response = self.retriever.search(
            query=search_query,
            top_k=top_k or self.settings.top_k,
            disease_filter=disease_filter,
        )

        logger.info(
            "Agent 2 completed: %d evidence chunk(s) retrieved",
            response.total_results,
        )

        return RetrieveAgentResponse(
            status=response.status,
            results=response.results,
            total_results=response.total_results,
            search_query=search_query,
        )

    def retrieve_from_request(self, payload: RetrieveAgentRequest) -> RetrieveAgentResponse:
        """Handle HTTP/REST payload from Agent 1."""
        entities = EntityResult(**payload.entities)
        analysis = QueryAnalysisResult(
            original_query=payload.query,
            sanitized_query=payload.query,
            intent=payload.intent,
            entities=entities,
            risk_level=payload.risk_level,
        )
        return self.retrieve(analysis, top_k=payload.top_k)
