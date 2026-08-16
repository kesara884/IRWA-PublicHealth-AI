# Mid-Evaluation Presentation Support — PublicHealth-AI

Suggested slide outline for Week 6 Mid Evaluation (IT 3041).

---

## Slide 1 — Project title + team

**PublicHealth-AI**  
Evidence-Grounded Public Health Information & Disease Advisory Assistant  

Course: Information Retrieval and Web Analytics (IT 3041)  
Team: *[Member 1], [Member 2], [Member 3]*

---

## Slide 2 — Problem

- Public seeks health information online; quality varies  
- Risk of unverified advice, missing sources, unsafe personalisation  
- Need for **retrieval-grounded**, transparent, multi-agent assistance  

---

## Slide 3 — Proposed solution

- Multi-agent system: Query Analysis → Document Retrieval → Evidence-based Response  
- NLP (NER, intent, risk) + IR/RAG + configurable LLM  
- Responsible AI guardrails + authentication  
- Positioning: **information assistant**, not diagnosis AI  

---

## Slide 4 — System architecture

Show Mermaid diagram from `docs/architecture.md`:

User → React → FastAPI → Agents → Vector DB → LLM → RAI Guard → User  

Include: Auth, PII sanitization, HTTP/REST agent communication, source attribution.

---

## Slide 5 — Agent roles

| Agent | Job |
|-------|-----|
| Query Analysis | NER, intent, risk → JSON |
| Medical Retrieval | Embed + top-K vector search |
| Response | LLM answer from evidence only |

---

## Slide 6 — Agent communication protocol

- Protocol: **HTTP/REST + JSON**  
- Example: `POST /api/agents/retrieve`  
- Agent 1 sends structured query; Agent 2 returns evidence list  

---

## Slide 7 — IR / RAG pipeline

Document → extract → clean → chunk → metadata → embed → vector DB → top-K retrieve → cite  

---

## Slide 8 — Working demo

Live run:

1. “What are the symptoms of dengue?” → evidence + citations  
2. Show demo Steps 1–7 in UI  
3. Optional: dosage question → safe refusal  

*(Demo depth depends on implementation phase at presentation time.)*

---

## Slide 9 — Responsible AI

- No diagnosis / no personalised dosage  
- Citations must match retrieved evidence  
- PII redaction  
- Explicit insufficient-evidence behaviour  
- We minimize hallucinations; we do **not** claim zero  

---

## Slide 10 — Commercialization

- Target: public health orgs, hospitals, NGOs, government  
- Model: B2B/B2G subscription or enterprise/on-prem  
- Example pricing labeled as **proposed examples only**  
- See `docs/commercialization.md`  

---

## Evaluation checklist (assignment)

1. System architecture — yes (`docs/architecture.md`)  
2. Agent roles and communication flow — yes (`docs/agent-flow.md`)  
3. Progress demonstration — Phase 1: structure + health; full agent demo in later phases  
4. Responsible AI compliance check — policy + later guard code  
5. Brief commercialization concept — yes (`docs/commercialization.md`)  
