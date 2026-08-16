# Mid-Evaluation Presentation Guide — PublicHealth-AI

## Quick Reference Summary

### Project at a Glance
- **Name**: PublicHealth-AI
- **Type**: Evidence-Grounded Public Health Information & Disease Advisory Assistant
- **Course**: IT 3041 (Information Retrieval and Web Analytics)
- **Status**: Phase 1-4 Complete (Mid-Evaluation Checkpoint)

---

## The Problem (30 seconds)
When people search for health information online:
- ❌ Answers are often unverified or incomplete
- ❌ Sources are unreliable or missing
- ❌ Personalized medical advice (e.g., "I have a headache, what drug should I take?") is unsafe
- **Need**: A system that grounds answers in trusted sources with proper citations

---

## The Solution (30 seconds)
PublicHealth-AI is a **multi-agent system** that:
1. **Understands** your question (NLP: identifies diseases, medical topics, risk level)
2. **Retrieves** relevant evidence from curated public health sources (IR/RAG)
3. **Answers** using ONLY that evidence with proper citations
4. **Checks** safety (refuses diagnoses, rejects dosage questions, protects privacy)

---

## Architecture (1 minute)

```
USER → FRONTEND (React)
     ↓
API GATEWAY (FastAPI)
     ↓
QUERY ANALYSIS AGENT → Extract entities, classify intent, assess risk
     ↓
RETRIEVAL AGENT → Vector search in knowledge base → Top-5 evidence chunks
     ↓
RESPONSE AGENT → Generate answer from evidence only
     ↓
RESPONSIBLE AI GUARD → Validate safety & citations
     ↓
USER → Answer + Evidence + Sources
```

**Three Core Agents**:
1. **Query Analysis**: NER (Named Entity Recognition), Intent Classification, Risk Assessment
2. **Retrieval**: Vector search (TF-IDF embeddings) with top-K retrieval
3. **Response**: Evidence-only LLM answer generation

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18 + Vite 6 |
| **Backend** | Python 3.13 + FastAPI + Uvicorn |
| **NLP** | spaCy + rule-based (Phase 10+) |
| **IR/RAG** | TF-IDF + NumPy vector store (upgradeable to Sentence Transformers) |
| **LLM** | Configurable (OpenAI or stub for testing) |
| **Auth** | JWT + bcrypt (Phase 10+) |
| **Communication** | HTTP/REST + JSON |

---

## What's Implemented (Phase 1-4)

✅ **Frontend**
- React shell with health check connectivity
- Authentication UI (Login/Register)
- Query input and response display
- Step visualization (shows what agents did)

✅ **Backend**
- FastAPI with CORS, health checks, structured logging
- Config management via pydantic-settings
- 3 API endpoints: `/api/agents/analyze`, `/api/agents/retrieve`, `/api/query`
- `/health` endpoint shows retrieval readiness

✅ **Data & Retrieval**
- 6 labeled sample documents (dengue, malaria, TB, influenza, COVID-19, prevention)
- 34 chunks indexed into vector store
- Document metadata: source, title, page, year, disease, URL
- TF-IDF embeddings with NumPy persistence
- Script: `ingest_documents.py` for automatic indexing

✅ **Responsible AI**
- Policy defined (see `docs/responsible-ai.md`)
- Enforcement code to come (Phase 10)
- Plans for: citation validation, diagnosis refusal, dosage refusal, PII redaction

---

## Demo Walkthrough (2-3 minutes)

### Scenario: "What are the symptoms of dengue?"

**Step 1: Frontend**
- User types query and submits

**Step 2: Query Analysis**
- System identifies entities: disease=["dengue"], topic=["symptoms"]
- Intent: "SYMPTOM_INQUIRY"
- Risk Level: "LOW"
- Shows JSON output in UI

**Step 3: Retrieval**
- Query is embedded using TF-IDF
- Vector search finds top-5 most similar chunks
- Results include: source, score, text, metadata, URL

**Step 4: Response Generation**
- LLM generates answer using ONLY retrieved evidence
- Includes citations: "(Source: WHO Dengue Guidelines, p.15)"

**Step 5: Safety Check**
- Responsible AI Guard validates:
  - ✅ No unsupported claims
  - ✅ Citations present and match evidence
  - ✅ No diagnosis language
  - Shows answer to user

**Optional Refusal Demo**:
- Ask: "What dosage of paracetamol should I take?"
- System: "I cannot provide personalized medication dosage. Please consult a healthcare professional."

---

## Responsible AI Highlights

### 8 Core Principles
1. **Evidence-Grounded**: Never invent facts or citations
2. **No Diagnosis**: Not a clinical decision-support tool
3. **No Prescriptions**: Refuses personalized dosages
4. **Transparent**: Shows reasoning (entities, intent, risk, sources)
5. **Privacy-First**: Redacts PII before processing
6. **Fair**: Same pipeline for all users
7. **Explainable**: Citations justify answers
8. **Honest**: Admits when evidence is insufficient

### Safety Checks
| Risk | Action |
|------|--------|
| Unsupported claims | Regenerate with constraints or fallback |
| Missing/wrong citations | Attach or refuse answer |
| Diagnosis language | Safe refusal message |
| Dosage requests | Safe refusal message |
| PII in output | Redact or fallback |

---

## Deployment Status

🚀 **Currently Running**:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Health Check**: http://localhost:8000/health

**Quick Start**:
```bash
# Backend
cd backend
.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm run dev
```

---

## Commercialization Vision

**Target Market**:
- Public health organizations
- Hospitals and clinics
- NGOs and government agencies
- Global health initiatives

**Business Model**:
- B2B/B2G subscription
- Enterprise/on-prem deployment
- White-label customization

**Value Proposition**:
- ✅ Reliable sourced information
- ✅ Reduced health misinformation
- ✅ Transparent & explainable answers
- ✅ HIPAA-ready privacy architecture

---

## Roadmap (What's Next)

**Phase 5-9**: 
- Implement spaCy NER for better entity extraction
- Add authentication (JWT/bcrypt)
- Upgrade to Sentence Transformers
- Implement Responsible AI safety checks

**Phase 10-11**:
- PII sanitization
- Real LLM integration (OpenAI/Cohere)
- User-session management
- Full security audit

**Phase 12+**:
- Multi-language support
- Integration with healthcare systems
- Mobile app
- Production deployment

---

## Common Q&A Responses

### Q: How is this different from WebMD, healthline, or existing health chatbots?

**A**: 
- WebMD is a passive knowledge base; we actively synthesize answers from verified sources
- Health chatbots often hallucinate or mix information; we explicitly show sources
- We refuse to diagnose or prescribe—we provide general information only
- Transparent: you see which documents informed the answer

### Q: What about privacy and patient data?

**A**:
- No patient data stored (general info only)
- PII (email, phone, address) is redacted before processing
- JWT authentication for access control
- Never logs passwords, API keys, or sensitive data
- Designed to be HIPAA-compliant when deployed in healthcare settings

### Q: Can this replace a doctor?

**A**:
- No. This is explicitly NOT a diagnosis or prescription tool
- We position it as an "information assistant," not a clinical tool
- For personal health decisions, users are encouraged to consult healthcare professionals
- We refuse personalized dosage and diagnosis queries

### Q: How do you handle hallucinations?

**A**:
- We don't claim zero hallucinations, but we minimize them through:
  - Retrieval-grounding: answers only use retrieved evidence
  - Citation validation: every claim must map to a source
  - Evidence thresholds: refuse to answer if TOP-5 results are low-confidence
  - Responsible AI checks: flag unsupported claims
- If we can't ground an answer, we tell the user

### Q: What's the business model?

**A**:
- B2B/B2G licensing to health organizations
- Subscription per organization (not per user)
- On-premise deployment for privacy-sensitive clients
- White-label customization available

### Q: What happens if someone asks an unsafe question?

**A**:
- Example: "What dosage of paracetamol should I take?"
- System: "I cannot provide personalized medication dosage. Please consult a healthcare professional. Here's general information about paracetamol..."
- Example: "Can you diagnose why I have chest pain?"
- System: "I can't diagnose medical conditions. Chest pain can be serious—please seek immediate medical attention."

---

## Presentation Slide Order

1. **Title Slide** — Project name, team, course
2. **Problem** — Why health info online is unreliable
3. **Solution** — Multi-agent system overview
4. **Architecture** — System diagram + components
5. **Agent Roles** — Query Analysis, Retrieval, Response
6. **Communication Protocol** — HTTP/REST + JSON
7. **IR/RAG Pipeline** — How documents flow through system
8. **Live Demo** — Walk through a query end-to-end
9. **Responsible AI** — Principles & safety checks
10. **Commercialization & Roadmap** — Vision & next steps

---

## Tips for Delivery

1. **Open with a relatable problem**: "How many of you have Googled a health symptom and gotten conflicting advice?"
2. **Use the architecture diagram**: Make it visual, don't just talk about it
3. **Show live demo**: Have browser open to http://localhost:8000/docs and make a test API call
4. **Emphasize safety**: Responsible AI is your differentiator
5. **Tell a story**: Take them through user journey, not just tech details
6. **Handle uncertainty well**: "This is Phase 1-4; Phase 5-12 includes X, Y, Z"
7. **Practice refusal scenarios**: Show what happens with unsafe queries
8. **End strong**: Vision of reducing health misinformation globally

---

## Files to Reference

- `docs/mid-evaluation.md` — Official slide outline
- `docs/architecture.md` — Detailed architecture + Mermaid diagram
- `docs/agent-flow.md` — Agent communication protocol
- `docs/responsible-ai.md` — Safety principles & checks
- `docs/commercialization.md` — Market analysis & pricing
- `backend/README.md` — Backend setup instructions
- `frontend/README.md` — Frontend setup (if exists)

---

## Presentation Timing

- **Title + Problem**: 2 min
- **Solution + Architecture**: 3 min
- **Agents + Protocol**: 2 min
- **IR/RAG**: 1 min
- **Live Demo**: 3-4 min
- **Responsible AI**: 2 min
- **Commercialization + Q&A**: 2-3 min
- **Total**: ~15-18 minutes (leaves 2-5 min for questions)

