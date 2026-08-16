"""
Risk classification for public-health queries.

HIGH risk: diagnosis requests, personalized dosage, prescribing language.
MEDIUM: treatment questions without explicit dosage.
LOW: general information, symptoms, prevention, transmission.
"""

from __future__ import annotations

import re
from typing import Tuple

HIGH_RISK_PATTERNS = [
    r"\bdiagnos(?:e|is|ing)\b",
    r"\bwhat (?:do|disease) (?:i|do i) have\b",
    r"\bam i (?:sick|infected|positive)\b",
    r"\b(?:exact|specific) (?:medicine|medication|drug|dosage|dose)\b",
    r"\bhow much (?:medicine|medication|paracetamol|ibuprofen|aspirin)\b",
    r"\bshould i take\b",
    r"\bprescrib(?:e|ing|ption)\b",
    r"\bwhat pills? (?:should|can) i take\b",
    r"\b\d+\s*mg\b",
    r"\bmilligram\b",
]

MEDIUM_RISK_PATTERNS = [
    r"\btreat(?:ment|ed|ing)?\b",
    r"\bmedicine\b",
    r"\bmedication\b",
    r"\bdrug\b",
    r"\bantibiotic\b",
    r"\bantiviral\b",
    r"\bcure\b",
]


def classify_risk(text: str, intent: str, is_unsupported: bool) -> str:
  """Return LOW | MEDIUM | HIGH."""
  if is_unsupported or intent == "UNSUPPORTED_MEDICAL_REQUEST":
      return "HIGH"

  lowered = text.lower()

  for pattern in HIGH_RISK_PATTERNS:
      if re.search(pattern, lowered):
          return "HIGH"

  if intent in {"TREATMENT_INFORMATION"}:
      return "MEDIUM"

  for pattern in MEDIUM_RISK_PATTERNS:
      if re.search(pattern, lowered):
          return "MEDIUM"

  return "LOW"


def risk_explanation(risk_level: str, intent: str) -> str:
    if risk_level == "HIGH":
        return (
            "Query requests diagnosis or personalized medication guidance. "
            "System will not provide dosage or diagnosis."
        )
    if risk_level == "MEDIUM":
        return "Query relates to treatment; response must stay general and evidence-based."
    return "General public-health information request."
