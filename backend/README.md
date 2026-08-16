# PublicHealth-AI Backend

## Quick start

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 1. Ingest sample documents (Phase 3)

```bash
python scripts/ingest_documents.py --reset
```

Expected: **34 chunks** indexed into `data/vector_store/`.

### 2. Run API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Health: http://127.0.0.1:8000/health  
- Retrieval status: http://127.0.0.1:8000/api/retrieval/status  
- Search: `POST /api/retrieval/search` with `{"query": "..."}`  
- Docs: http://127.0.0.1:8000/docs  

## Embedding providers

| Provider | Env value | Notes |
|----------|-----------|-------|
| TF-IDF (default) | `EMBEDDING_PROVIDER=tfidf` | Works on Python 3.13 |
| Sentence Transformers | `EMBEDDING_PROVIDER=sentence_transformers` | Requires Python 3.10–3.12 + torch |

## Sample data

Documents in `data/sample_documents/` are **clearly labeled sample excerpts** for development only. Replace with official WHO/CDC PDFs for production.
