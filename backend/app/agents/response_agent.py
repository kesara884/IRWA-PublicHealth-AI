"""
Phase 8: Evidence-Based Response Agent.
Generates RAG responses with strict citation metadata using OpenAI LLM or deterministic fallback stub.
"""

import logging
import re
from typing import List, Optional

import httpx

from app.config import get_settings
from app.models.query import (
    Citation,
    QueryAnalysisResult,
    ResponseAgentResult,
)
from app.models.retrieval import RetrievalResult

logger = logging.getLogger(__name__)


class ResponseAgent:
    """Agent responsible for synthesizing evidence-grounded answers with citations."""

    def __init__(self):
        self.settings = get_settings()

    async def generate_response(
        self,
        analysis: QueryAnalysisResult,
        retrieval_results: List[RetrievalResult],
    ) -> ResponseAgentResult:
        """
        Generate an evidence-grounded response for the given query and retrieved documents.
        """
        if not retrieval_results:
            return ResponseAgentResult(
                answer=(
                    "I could not find sufficient verified evidence in the current "
                    "public-health knowledge base to answer this question."
                ),
                citations=[],
                model_used="stub",
                raw_llm_output=None,
            )

        citations: List[Citation] = []
        for idx, res in enumerate(retrieval_results, 1):
            text_str = getattr(res, "text", "") or getattr(res, "chunk_text", "")
            title_str = getattr(res, "title", f"Document {idx}")
            source_str = getattr(res, "source", "Public Health KB")
            page_num = getattr(res, "page", 1)
            chunk_id = getattr(res, "chunk_id", f"chunk_{idx}")

            citations.append(
                Citation(
                    doc_title=title_str,
                    source=source_str,
                    page=page_num,
                    snippet=text_str[:180] + "..." if len(text_str) > 180 else text_str,
                    chunk_id=chunk_id,
                )
            )

        provider = self.settings.llm_provider.lower()
        api_key = self.settings.openai_api_key

        if provider == "openai" and api_key and not api_key.startswith("your-"):
            try:
                llm_response = await self._call_openai(analysis.sanitized_query, retrieval_results)
                if llm_response:
                    return ResponseAgentResult(
                        answer=llm_response,
                        citations=citations,
                        model_used=f"openai/{self.settings.openai_model}",
                        raw_llm_output=llm_response,
                    )
            except Exception as exc:
                logger.warning("OpenAI API call failed, falling back to stub: %s", exc)

        # Fallback / Stub Mode Generation
        stub_answer = self._generate_stub_response(analysis, retrieval_results, citations)
        return ResponseAgentResult(
            answer=stub_answer,
            citations=citations,
            model_used="evidence-synthesizer-stub",
            raw_llm_output=stub_answer,
        )

    async def _call_openai(
        self, query: str, retrieval_results: List[RetrievalResult]
    ) -> Optional[str]:
        """Call OpenAI Chat Completions API with evidence grounding prompt."""
        evidence_text = ""
        for i, res in enumerate(retrieval_results, 1):
            title = getattr(res, "title", "Document")
            source = getattr(res, "source", "Unknown")
            page = getattr(res, "page", 1)
            text_str = getattr(res, "text", "")
            evidence_text += (
                f"\n[Source {i}: {title} ({source}), Page {page}]\n{text_str}\n"
            )

        system_prompt = (
            "You are an Evidence-Grounded Public Health Advisory Assistant. "
            "Your task is to answer the user's health question strictly using the provided source documents. "
            "RULES:\n"
            "1. Answer ONLY using the facts present in the provided source documents.\n"
            "2. Cite your sources inline using [Doc: <title>, Source: <source>, Page: <page>].\n"
            "3. If the sources do not contain enough information, state clearly that information is limited.\n"
            "4. Do NOT provide personal medical diagnoses or prescription drug dosages."
        )

        user_prompt = f"User Question: {query}\n\nRetrieved Evidence:\n{evidence_text}"

        headers = {
            "Authorization": f"Bearer {self.settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.settings.openai_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
            "max_tokens": 500,
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                f"{self.settings.openai_base_url}/chat/completions",
                json=payload,
                headers=headers,
            )
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                logger.error("OpenAI API returned error %s: %s", resp.status_code, resp.text)
                return None

    def _generate_stub_response(
        self,
        analysis: QueryAnalysisResult,
        retrieval_results: List[RetrievalResult],
        citations: List[Citation],
    ) -> str:
        """Generate a structured, evidence-grounded answer synthesized from top chunks."""
        top_chunks = retrieval_results[:3]
        summaries = []
        for i, chunk in enumerate(top_chunks):
            chunk_text = getattr(chunk, "text", "")
            clean_snippet = chunk_text.strip().replace("\n", " ")
            meta = citations[i]
            cite_tag = f"[Doc: {meta.doc_title}, Page: {meta.page or 1}]"
            summaries.append(f"{clean_snippet} {cite_tag}")

        disease_name = analysis.entities.disease[0] if analysis.entities.disease else "the inquired public health topic"
        joined_evidence = "\n\n".join([f"• {s}" for s in summaries])

        answer = (
            f"Based on verified public-health evidence regarding **{disease_name}**, "
            f"here are key information highlights:\n\n"
            f"{joined_evidence}\n\n"
            f"For further detailed guidance, please refer to official public health resources "
            f"such as the World Health Organization (WHO) or Ministry of Health guidelines."
        )

        return answer
