"""
Rule-based intent classification for public-health queries.
"""

from __future__ import annotations

import re
from typing import Tuple

INTENTS = {
    "SYMPTOMS": [
        r"\bsymptoms?\b",
        r"\bsigns of\b",
        r"\bhow do (?:i|you) know\b",
        r"\bwhat does .+ feel like\b",
    ],
    "WARNING_SIGNS": [
        r"\bwarning signs?\b",
        r"\bsevere (?:symptoms?|signs?)\b",
        r"\bred flags?\b",
        r"\bwhen to (?:see|visit|go to) (?:a )?(?:doctor|hospital|er)\b",
    ],
    "PREVENTION": [
        r"\bprevent(?:ion|ing|ed)?\b",
        r"\bhow (?:can|to) (?:i |we )?(?:avoid|protect|stop)\b",
        r"\bvaccin(?:e|ation|ate)\b",
        r"\breduce (?:the )?risk\b",
    ],
    "TRANSMISSION": [
        r"\btransmi(?:t|ssion|tted)\b",
        r"\bhow (?:is|does) .+ spread\b",
        r"\bcontagious\b",
        r"\bvector\b",
    ],
    "TREATMENT_INFORMATION": [
        r"\btreat(?:ment|ed|ing)?\b",
        r"\bcure\b",
        r"\btherapy\b",
        r"\bmanage(?:ment)?\b",
    ],
    "OUTBREAK_INFORMATION": [
        r"\boutbreak\b",
        r"\bepidemic\b",
        r"\bpandemic\b",
        r"\bsurge\b",
        r"\bcluster\b",
    ],
    "DISEASE_INFORMATION": [
        r"\bwhat is\b",
        r"\btell me about\b",
        r"\binformation about\b",
        r"\bexplain\b",
        r"\boverview\b",
    ],
    "GENERAL_HEALTH": [
        r"\bpublic health\b",
        r"\bhealth tips\b",
        r"\bwellness\b",
        r"\bhealthy habits\b",
    ],
}

UNSUPPORTED_PATTERNS = [
    r"\bdiagnos(?:e|is|ing)\b",
    r"\bwhat (?:do|disease) (?:i|do i) have\b",
    r"\bam i (?:sick|infected)\b",
    r"\b(?:exact|specific) (?:medicine|medication|drug|dosage|dose)\b",
    r"\bhow much (?:medicine|medication|paracetamol|ibuprofen)\b",
    r"\bshould i take\b",
    r"\bprescrib(?:e|ing|ption)\b",
    r"\bwhat pills?\b",
    r"\bmg\b",
    r"\bmilligram\b",
]


def classify_intent(text: str) -> Tuple[str, bool]:
    """
    Return (intent, is_unsupported_request).
    Unsupported requests are flagged separately for risk handling.
    """
    lowered = text.lower()

    for pattern in UNSUPPORTED_PATTERNS:
        if re.search(pattern, lowered):
            return "UNSUPPORTED_MEDICAL_REQUEST", True

    scores = {intent: 0 for intent in INTENTS}
    for intent, patterns in INTENTS.items():
        for pattern in patterns:
            if re.search(pattern, lowered):
                scores[intent] += 1

    best_intent = max(scores, key=scores.get)
    if scores[best_intent] > 0:
        return best_intent, False

    # Default when no pattern matched
    if re.search(r"\b(?:symptom|sign|prevent|transmit|treat|outbreak)\b", lowered):
        return "GENERAL_HEALTH", False

    return "DISEASE_INFORMATION", False
