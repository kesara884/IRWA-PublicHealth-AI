"""
Agent HTTP/REST communication layer.

Agent 1 calls Agent 2 over HTTP when use_http=True (demo mode).
Falls back to in-process calls when HTTP fails or in tests.
"""

from __future__ import annotations

import logging
from typing import Optional

import httpx

from app.agents.retrieval_agent import MedicalRetrievalAgent
from app.config import get_settings
from app.models.query import QueryAnalysisResult, RetrieveAgentRequest, RetrieveAgentResponse

logger = logging.getLogger(__name__)


class AgentCommunicator:
    def __init__(self, use_http: bool = True) -> None:
        self.settings = get_settings()
        self.use_http = use_http
        self._local_agent = MedicalRetrievalAgent()

    async def call_retrieval_agent(
        self,
        analysis: QueryAnalysisResult,
        top_k: Optional[int] = None,
    ) -> RetrieveAgentResponse:
        if self.use_http:
            try:
                return await self._http_retrieve(analysis, top_k)
            except Exception as exc:
                logger.warning("HTTP agent call failed, using in-process fallback: %s", exc)

        return self._local_agent.retrieve(analysis, top_k=top_k)

    async def _http_retrieve(
        self,
        analysis: QueryAnalysisResult,
        top_k: Optional[int] = None,
    ) -> RetrieveAgentResponse:
        payload = RetrieveAgentRequest(
            query=analysis.sanitized_query,
            intent=analysis.intent,
            entities=analysis.entities.model_dump(),
            risk_level=analysis.risk_level,
            top_k=top_k,
        )

        url = f"{self.settings.agent_api_base_url.rstrip('/')}/api/agents/retrieve"
        logger.info("Agent 1 → Agent 2 HTTP POST %s", url)

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload.model_dump())
            response.raise_for_status()
            data = response.json()

        logger.info("Agent 2 HTTP response: status=%s results=%d", data.get("status"), data.get("total_results", 0))
        return RetrieveAgentResponse(**data)
