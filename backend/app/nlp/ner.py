"""
Medical Named Entity Recognition.

Uses a rule-based lexicon (primary) with optional spaCy enhancement when installed.
"""

from __future__ import annotations

import logging
import re
from typing import Dict, List, Set

from app.models.query import EntityResult

logger = logging.getLogger(__name__)

# Curated lexicons for prototype — extend with spaCy/medspaCy in production
DISEASES: Dict[str, str] = {
    "dengue": "dengue",
    "dengue fever": "dengue",
    "malaria": "malaria",
    "tuberculosis": "tuberculosis",
    "tb": "tuberculosis",
    "influenza": "influenza",
    "flu": "influenza",
    "covid": "covid-19",
    "covid-19": "covid-19",
    "coronavirus": "covid-19",
    "ebola": "ebola",
    "cholera": "cholera",
    "typhoid": "typhoid",
}

SYMPTOMS: Dict[str, str] = {
    "fever": "fever",
    "headache": "headache",
    "cough": "cough",
    "rash": "rash",
    "vomiting": "vomiting",
    "nausea": "nausea",
    "fatigue": "fatigue",
    "chills": "chills",
    "body ache": "body ache",
    "body aches": "body ache",
    "muscle pain": "muscle pain",
    "joint pain": "joint pain",
    "shortness of breath": "shortness of breath",
    "chest pain": "chest pain",
    "night sweats": "night sweats",
    "loss of taste": "loss of taste",
    "loss of smell": "loss of smell",
}

MEDICAL_TOPICS: Dict[str, str] = {
    "symptoms": "symptoms",
    "symptom": "symptoms",
    "warning signs": "warning signs",
    "warning sign": "warning signs",
    "prevention": "prevention",
    "prevent": "prevention",
    "transmission": "transmission",
    "transmit": "transmission",
    "transmitted": "transmission",
    "spread": "transmission",
    "treatment": "treatment",
    "treat": "treatment",
    "outbreak": "outbreak",
    "vaccine": "vaccination",
    "vaccination": "vaccination",
    "immunization": "vaccination",
    "hygiene": "hygiene",
    "handwashing": "hand hygiene",
}

MEDICATIONS: Dict[str, str] = {
    "paracetamol": "paracetamol",
    "acetaminophen": "paracetamol",
    "ibuprofen": "ibuprofen",
    "aspirin": "aspirin",
    "antibiotic": "antibiotic",
    "antibiotics": "antibiotic",
    "antiviral": "antiviral",
    "artemisinin": "artemisinin",
}

CONDITIONS: Dict[str, str] = {
    "hemorrhagic fever": "hemorrhagic fever",
    "respiratory illness": "respiratory illness",
    "infection": "infection",
}


def _find_lexicon_matches(text: str, lexicon: Dict[str, str]) -> List[str]:
    lowered = text.lower()
    found: Set[str] = set()
    # Longest phrases first to avoid partial overlaps
    for phrase in sorted(lexicon.keys(), key=len, reverse=True):
        if re.search(rf"\b{re.escape(phrase)}\b", lowered):
            found.add(lexicon[phrase])
    return sorted(found)


def _try_spacy_entities(text: str) -> EntityResult:
    """Optional spaCy pass — returns empty result if spaCy is unavailable."""
    try:
        import spacy  # noqa: F401
    except ImportError:
        return EntityResult()

    try:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        diseases: Set[str] = set()
        conditions: Set[str] = set()
        for ent in doc.ents:
            if ent.label_ in {"DISEASE", "CONDITION"}:
                diseases.add(ent.text.lower())
            elif ent.label_ in {"PRODUCT"}:
                pass  # medications handled by lexicon
        return EntityResult(
            disease=sorted(diseases),
            medical_condition=sorted(conditions),
        )
    except Exception as exc:
        logger.debug("spaCy NER unavailable: %s", exc)
        return EntityResult()


def extract_entities(text: str) -> EntityResult:
    """
    Extract medical entities from user text.
    Rule-based layer is always used; spaCy augments when available.
    """
    rule_result = EntityResult(
        disease=_find_lexicon_matches(text, DISEASES),
        symptom=_find_lexicon_matches(text, SYMPTOMS),
        medical_condition=_find_lexicon_matches(text, CONDITIONS),
        medical_topic=_find_lexicon_matches(text, MEDICAL_TOPICS),
        medication=_find_lexicon_matches(text, MEDICATIONS),
    )

    spacy_result = _try_spacy_entities(text)

    return EntityResult(
        disease=sorted(set(rule_result.disease + spacy_result.disease)),
        symptom=sorted(set(rule_result.symptom + spacy_result.symptom)),
        medical_condition=sorted(
            set(rule_result.medical_condition + spacy_result.medical_condition)
        ),
        medical_topic=rule_result.medical_topic,
        medication=rule_result.medication,
    )
