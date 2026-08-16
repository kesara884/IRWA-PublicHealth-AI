"""
Agent 1 — Query Analysis Agent

Responsibilities:
  1. Receive user natural-language query
  2. Sanitize input (PII redaction)
  3. Medical NER
  4. Intent classification
  5. Risk classification
  6. Return structured JSON for Agent 2
"""

from __future__ import annotations

import logging

from app.models.query import QueryAnalysisResult
from app.nlp.intent import classify_intent
from app.nlp.ner import extract_entities
from app.nlp.risk import classify_risk
from app.security.pii_sanitizer import sanitize_pii

logger = logging.getLogger(__name__)


class QueryAnalysisAgent:
    def analyze(self, query: str) -> QueryAnalysisResult:
        logger.info("Agent 1 started: query analysis")
        original = query.strip()

        sanitize = sanitize_pii(original)
        if sanitize.pii_detected:
            logger.info("PII redacted: %d pattern(s)", sanitize.redaction_count)

        intent, is_unsupported = classify_intent(sanitize.sanitized_text)
        entities = extract_entities(sanitize.sanitized_text)
        risk_level = classify_risk(sanitize.sanitized_text, intent, is_unsupported)

        logger.info(
            "Agent 1 completed: intent=%s risk=%s diseases=%s",
            intent,
            risk_level,
            entities.disease,
        )

        return QueryAnalysisResult(
            original_query=original,
            sanitized_query=sanitize.sanitized_text,
            intent=intent,
            entities=entities,
            risk_level=risk_level,
            pii_detected=sanitize.pii_detected,
        )
