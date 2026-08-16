"""
Basic PII detection and redaction before NLP / LLM processing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(
    r"(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{2,4}\)?[\s-]?)?\d{3,4}[\s-]?\d{3,4}\b"
)
NIC_RE = re.compile(r"\b\d{9,12}[vVxX]?\b")
NAME_INTRO_RE = re.compile(
    r"\b(?:my name is|i am|i'm)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})",
    re.IGNORECASE,
)
ADDRESS_HINT_RE = re.compile(
    r"\b\d{1,5}\s+[A-Za-z]+\s+(?:street|st|road|rd|lane|ln|avenue|ave)\b",
    re.IGNORECASE,
)

REDACTED = "[REDACTED]"


@dataclass
class SanitizeResult:
    sanitized_text: str
    pii_detected: bool
    redaction_count: int


def sanitize_pii(text: str) -> SanitizeResult:
    """Detect and redact common PII patterns."""
    redaction_count = 0
    sanitized = text

    for pattern in (EMAIL_RE, PHONE_RE, NIC_RE, ADDRESS_HINT_RE):
        sanitized, n = pattern.subn(REDACTED, sanitized)
        redaction_count += n

    def _name_replacer(match: re.Match) -> str:
        return match.group(0).replace(match.group(1), REDACTED)

    sanitized, n = NAME_INTRO_RE.subn(_name_replacer, sanitized)
    redaction_count += n

    return SanitizeResult(
        sanitized_text=sanitized,
        pii_detected=redaction_count > 0,
        redaction_count=redaction_count,
    )
