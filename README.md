# PublicHealth-AI

**Evidence-Grounded Public Health Information & Disease Advisory Assistant**

Course: Information Retrieval and Web Analytics (IT 3041)  
Project type: Agentic AI-Based System Development  
Domain: Public Health

> This system provides **general public-health information** retrieved from verified sources.  
> It is **not** a medical diagnosis system and does **not** prescribe medication.

---

## 1. Project overview

PublicHealth-AI is a multi-agent prototype that:

1. Analyses a user query (NER, intent, risk)
2. Retrieves evidence from a public-health knowledge base (vector/RAG)
3. Generates an evidence-grounded answer with citations
4. Runs Responsible AI / safety checks before returning the answer

Agents communicate over **HTTP/REST + JSON**.

---

## 2. Problem statement

The public often seeks health information online, but answers may be unverified, incomplete, or unsafe. This project demonstrates an **agentic IR + NLP + LLM** pipeline that grounds responses in a curated public-health corpus and refuses unsupported or high-risk medical requests (e.g. personalised dosage).

---

## 3. Architecture (high level)

See [docs/architecture.md](docs/architecture.md) for the Mermaid diagram and component details.

```
User → React Frontend → FastAPI Backend
         → Query Analysis Agent (NER / Intent / Risk)
         → Medical Retrieval Agent (embeddings + vector search)
         → Response Agent (LLM, evidence-only)
         → Responsible AI Guard → User
```

---

## 4. Agent descriptions

| Agent | Role |
|-------|------|
| **Query Analysis Agent** | Sanitize input, Medical NER, intent + risk classification, structured JSON |
| **Medical Document Retrieval Agent** | Embed query, top-K vector search, return evidence + metadata |
| **Evidence-Based Response Agent** | LLM answer using **only** retrieved evidence + citations |

---

## 5. Technology stack

| Layer | Choice |
|-------|--------|
| Frontend | React, Vite, Axios, CSS |
| Backend | Python, FastAPI, Uvicorn, Pydantic |
| Auth (later) | JWT, bcrypt/passlib |
| NLP (later) | spaCy + rule-based medical NER |
| IR (later) | Sentence Transformers + FAISS (or Chroma) |
| LLM | Configurable via `LLM_PROVIDER` (OpenAI or stub) |

---

## 6. Installation

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Frontend

```bash
cd frontend
npm install
```

---

## 7. Environment variables

Copy `backend/.env.example` → `backend/.env`. Important keys:

| Variable | Purpose |
|----------|---------|
| `JWT_SECRET_KEY` | JWT signing secret |
| `LLM_PROVIDER` | `stub` or `openai` |
| `OPENAI_API_KEY` | Required only if provider is `openai` |
| `TOP_K` | Retrieval result count (default 5) |
| `CORS_ORIGINS` | Allowed frontend origins |

**Never commit `.env` or API keys.**

---

## 8. How to run the backend

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Health: http://127.0.0.1:8000/health  
- Docs: http://127.0.0.1:8000/docs  

---

## 9. How to run the frontend

```bash
cd frontend
npm run dev
```

Open http://localhost:5173

---

## 10. How to ingest documents

From `backend/` (after activating the virtual environment):

```bash
python scripts/ingest_documents.py --reset
```

This loads sample documents from `data/sample_documents/`, chunks them, generates TF-IDF embeddings, and indexes **34 chunks** into `data/vector_store/`.

To add official PDFs later, place them in `data/raw/` or update `documents_manifest.json`, then re-run ingestion.

**Note:** On Python 3.13, we use **TF-IDF + NumPy** (Chroma/FAISS/sentence-transformers require Python 3.10–3.12 or extra build tools). Set `EMBEDDING_PROVIDER=sentence_transformers` when those packages are available.

## 10b. Test retrieval (Phase 5)

```bash
# API (with server running)
curl -X POST http://127.0.0.1:8000/api/retrieval/search \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the symptoms of dengue?"}'

curl http://127.0.0.1:8000/api/retrieval/status
```

---

## 11. How agents communicate

Agent 1 calls Agent 2 via **HTTP REST + JSON** (e.g. `POST /api/agents/retrieve`).  
Details: [docs/agent-flow.md](docs/agent-flow.md) (outline in Phase 1; endpoints implemented in Phases 6–7).

---

## 12. Responsible AI

- Evidence-only generation; no invented citations  
- Refusal of diagnosis / personalised dosage  
- PII sanitisation before LLM calls  
- Safety validation layer  

See [docs/responsible-ai.md](docs/responsible-ai.md).

---

## 13. Security

- JWT authentication (Phase 11)  
- Password hashing (bcrypt) — never plain text  
- Input validation + PII redaction  
- Secrets via environment variables  

---

## 14. Test cases

Planned demo queries (Phases 13–14):

1. Symptoms of dengue → evidence + citations  
2. Dengue prevention → PREVENTION intent  
3. Malaria transmission → TRANSMISSION  
4. Exact medicine/dosage → HIGH / UNSUPPORTED + safe refusal  
5. Out-of-KB question → explicit “insufficient verified evidence”  

---

## 15. Team members

| Member | Role (suggested) |
|--------|------------------|
| *Member 1* | Backend / Agents / IR |
| *Member 2* | NLP / Responsible AI / Docs |
| *Member 3* | Frontend / Auth / Demo flow |

*Replace with your group’s real names before submission.*

---

## Current status

| Phase | Status |
|-------|--------|
| 1 — Structure + health + frontend shell | **Done** |
| 2 — Backend health + retrieval status | **Done** |
| 3 — Document ingestion pipeline | **Done** (34 sample chunks) |
| 4 — Vector store + retriever | **Done** (NumPy + TF-IDF) |
| 5 — Test retrieval API | **Done** (`POST /api/retrieval/search`) |
| 6 — Query Analysis Agent | **Done** (NER, intent, risk) |
| 7 — Agent HTTP communication | **Done** (`/api/agents/*`, `/api/query`) |
| 8 — Response Agent (LLM) | Next |

**Next:** Phase 8 — Evidence-Based Response Agent (LLM/RAG answer generation).
