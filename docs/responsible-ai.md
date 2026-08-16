# Responsible AI — PublicHealth-AI

**Status:** Policy and design for Phase 1. Enforcement code lands in Phase 10.

## Principles

1. **Evidence-grounded answers only** — no invented medical facts or citations.
2. **No diagnosis** — the system is not a clinician.
3. **No personalised medication dosage** — refuse and redirect to professional care.
4. **Transparency** — show intent, entities, risk, evidence, and sources in the UI.
5. **User-data protection** — redact PII before LLM calls; do not log passwords/tokens/PII.
6. **Fairness** — same pipeline for all users; avoid demographic assumptions in prompts.
7. **Explainability** — citations and retrieval scores support why an answer was given.
8. **Honest uncertainty** — if evidence is insufficient, say so explicitly.

## Safety checks (planned)

| Check | Action on failure |
|-------|-------------------|
| Unsupported claims | Fallback / regenerate constrained |
| Missing citations when evidence exists | Attach or fail safe |
| Citations not in retrieved set | Strip / fallback |
| Diagnosis language | Safe refusal |
| Personalised dosage | Safe refusal |
| Unsafe medical instructions | Safe refusal |
| PII leakage in output | Redact / fallback |

### Example safe fallback

> I’m unable to provide a diagnosis or personalized medication dosage. I can provide general public-health information from verified sources.

### Insufficient evidence message

> I could not find sufficient verified evidence in the current public-health knowledge base to answer this question.

## What we do **not** claim

- We do **not** claim zero hallucinations.
- We **minimize** unsupported content via retrieval grounding + validation.

## Medical safety positioning

| Correct framing | Incorrect framing |
|-----------------|-------------------|
| Evidence-Grounded Public Health Information Assistant | AI Doctor |
| General information from verified sources | Medical Diagnosis AI |
| Seek professional care for personal decisions | AI that prescribes medicine |
