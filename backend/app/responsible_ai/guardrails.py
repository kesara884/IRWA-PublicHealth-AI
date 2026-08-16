"""
Phase 9: Responsible AI Guardrails & Safety Enforcement.
Handles safety checks, unsafe query refusal, citation verification, and compliance metadata.
"""

import logging
import re
from typing import List, Optional

from app.models.query import (
    Citation,
    QueryAnalysisResult,
    ResponseAgentResult,
    ResponsibleAIReport,
)
from app.models.retrieval import RetrievalResult
from app.security.pii_sanitizer import sanitize_pii

logger = logging.getLogger(__name__)

# Refusal keywords and unsafe patterns
UNSAFE_PATTERNS = [
    re.compile(r"\b(?:give me|what is the|how much)\s+(?:dosage|dose|mg|milligram|tablets)\b", re.IGNORECASE),
    re.compile(r"\b(?:prescribe|medicate|cure me|diagnose me)\b", re.IGNORECASE),
    re.compile(r"\bdo i have\s+(?:dengue|malaria|covid|cancer|flu|hiv)\b", re.IGNORECASE),
    re.compile(r"\b(?:suicide|self-harm|kill myself)\b", re.IGNORECASE),
]

DISCLAIMER_TEXT = (
    "This system provides general public-health information from verified sources "
    "and does not provide personalized medical diagnosis, prescription advice, or clinical care."
)


class ResponsibleAIGuard:
    """Responsible AI Enforcement Agent for safety, grounding, and citation compliance."""

    def evaluate_request(self, original_query: str, analysis: QueryAnalysisResult) -> ResponsibleAIReport:
        """Evaluate initial request for safety, risk, and PII presence."""
        warnings: List[str] = []

        # Check PII
        pii_res = sanitize_pii(original_query)
        if pii_res.pii_detected:
            warnings.append(f"PII detected and redacted ({pii_res.redaction_count} item(s)).")

        # Check UNSAFE / HIGH RISK queries
        refusal_triggered = False
        if analysis.intent == "UNSUPPORTED_MEDICAL_REQUEST" or analysis.risk_level == "HIGH":
            refusal_triggered = True
            warnings.append("Request flagged as HIGH risk or UNSUPPORTED medical request (diagnosis/dosage).")

        for pattern in UNSAFE_PATTERNS:
            if pattern.search(original_query):
                refusal_triggered = True
                if "dosage" in pattern.pattern or "dose" in pattern.pattern:
                    warnings.append("Personalized dosage advice requested — blocked for patient safety.")
                break

        return ResponsibleAIReport(
            safety_passed=not refusal_triggered,
            pii_detected=pii_res.pii_detected,
            refusal_triggered=refusal_triggered,
            citation_validation_passed=True,
            warnings=warnings,
            disclaimer=DISCLAIMER_TEXT,
        )

    def validate_response(
        self,
        response_result: ResponseAgentResult,
        retrieval_results: List[RetrievalResult],
        report: ResponsibleAIReport,
    ) -> ResponsibleAIReport:
        """Validate LLM response citations against retrieved document context."""
        retrieved_titles = set()
        for res in retrieval_results:
            title_val = getattr(res, "title", "")
            if title_val:
                retrieved_titles.add(title_val.strip().lower())

        invalid_citations = []
        for cite in response_result.citations:
            title_clean = cite.doc_title.strip().lower()
            if title_clean and title_clean not in retrieved_titles and not any(t in title_clean for t in retrieved_titles):
                invalid_citations.append(cite.doc_title)

        if invalid_citations:
            report.citation_validation_passed = False
            report.warnings.append(f"Unverified citation(s) detected: {', '.join(invalid_citations)}")

        if not response_result.answer.endswith(DISCLAIMER_TEXT):
            response_result.answer = f"{response_result.answer.strip()}\n\n---\n*Disclaimer: {DISCLAIMER_TEXT}*"

        return report
