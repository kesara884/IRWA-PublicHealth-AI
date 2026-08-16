# ChatGPT Prompt for Mid-Evaluation Presentation

Copy and paste the entire section below into ChatGPT to generate your mid-evaluation presentation script and talking points.

---

## PROMPT FOR CHATGPT

```
You are helping me prepare for a mid-evaluation presentation for my university course (IT 3041: Information Retrieval and Web Analytics). 

PROJECT OVERVIEW:
- Project Name: PublicHealth-AI
- Type: Agentic AI-Based System Development  
- Domain: Public Health Information Assistant
- Status: Phase 1-4 complete (mid-evaluation checkpoint)

PROBLEM STATEMENT:
The public often seeks health information online, but answers may be:
- Unverified or incomplete
- From unreliable sources
- Unsafe (e.g., suggesting personalized dosages)
- Lacking proper citations

PROPOSED SOLUTION:
A multi-agent system that:
1. Analyzes user queries using NLP (Named Entity Recognition, Intent Classification, Risk Assessment)
2. Retrieves evidence from a curated public-health knowledge base using vector search (RAG)
3. Generates evidence-grounded answers with proper citations
4. Runs Responsible AI safety checks before returning answers

KEY TECHNOLOGY STACK:
- Frontend: React + Vite
- Backend: Python + FastAPI + Uvicorn
- NLP: spaCy (for future phases)
- IR/RAG: TF-IDF embeddings + NumPy vector store (with upgrade path to Sentence Transformers)
- LLM: Configurable (OpenAI or stub)
- Authentication: JWT + bcrypt (Phase 10+)
- Database: Vector store + metadata

SYSTEM ARCHITECTURE:
```
User → React Frontend → FastAPI Backend
  ↓
  Query Analysis Agent (NER, Intent, Risk)
  ↓
  Medical Retrieval Agent (Vector Search)
  ↓
  Response Agent (LLM - Evidence Only)
  ↓
  Responsible AI Guard (Safety Checks)
  ↓
  User (Answer + Citations)
```

THREE CORE AGENTS:
1. Query Analysis Agent: Sanitizes input, extracts medical entities, classifies intent, assesses risk level → returns structured JSON
2. Medical Retrieval Agent: Embeds the query, performs top-K vector search (default: top-5), returns evidence chunks with metadata and sources
3. Response Agent: Generates answers using ONLY retrieved evidence, includes proper citations

AGENT COMMUNICATION:
- Protocol: HTTP/REST + JSON
- Agents communicate through FastAPI endpoints
- Example: `/api/agents/analyze`, `/api/agents/retrieve`, `/api/query`

IMPLEMENTED FEATURES (Phase 1-4):
✅ Project repository structure following assignment guidelines
✅ FastAPI health check endpoint
✅ Configuration management via pydantic-settings
✅ React frontend shell with health connectivity
✅ Document ingestion pipeline (6 labeled sample documents)
✅ Vector store with TF-IDF embeddings
✅ Retrieval endpoint: POST /api/retrieval/search
✅ Demo step visualization in UI
✅ Environment variable management via .env

INFORMATION RETRIEVAL / RAG PIPELINE:
Document → Extract → Clean → Chunk → Metadata Assignment → Embed → Vector DB → Top-K Retrieve → Cite

VECTOR STORE:
- 34 sample document chunks indexed
- Each chunk retains: document_id, source, title, page, year, disease, URL
- Default TOP_K=5 for retrieval
- TF-IDF embedding (Python 3.13 compatible)
- Future: Hybrid search with BM25

RESPONSIBLE AI PRINCIPLES:
1. Evidence-grounded answers only (no hallucinations/invented citations)
2. NOT a diagnosis system
3. NOT a prescription system (refuses personalized dosages)
4. Transparent: shows intent, entities, risk level, evidence, sources
5. User-data protection: PII redacted before LLM
6. Honest uncertainty: explicitly states when evidence is insufficient

RESPONSIBLE AI SAFETY CHECKS:
- Validates against unsupported medical claims
- Ensures citations match retrieved evidence
- Refuses diagnosis language
- Refuses personalized medication dosage
- Detects PII leakage in output
- Safe fallback messages for unsafe queries

COMMERCIALIZATION TARGET:
- Market: Public health organizations, hospitals, NGOs, government agencies
- Model: B2B/B2G subscription or enterprise/on-prem deployment
- Value proposition: Reliable, sourced health information with transparency

DEMO SCENARIO (for presentation):
1. User asks: "What are the symptoms of dengue?"
2. System displays:
   - Query analysis results (entities, intent, risk level)
   - Retrieved evidence with sources
   - Generated answer with citations
   - Demo steps visualization
3. Optional: Show safe refusal for dangerous query (e.g., asking for drug dosage)

DEPLOYMENT STATUS:
- Backend: Running on localhost:8000 with auto-reload
- Frontend: Running on localhost:5173
- API Documentation: http://localhost:8000/docs (Swagger UI)
- Health Check: http://localhost:8000/health

NOW, PLEASE GENERATE FOR ME:

1. **A 10-slide presentation outline** with:
   - Slide titles
   - Key talking points for each slide
   - Estimated speaking time per slide (2-3 minutes each)
   - Suggested visuals/diagrams to show

2. **Speaker notes** for each slide that I can read from:
   - Clear, natural language
   - Engaging and informative
   - Includes statistics or context where relevant
   - Transitions between slides

3. **Technical demo script** showing:
   - Step-by-step what to show on screen
   - What to say during the demo
   - How to handle potential issues
   - Alternative quick demo if full system isn't available

4. **Possible Q&A responses** for common questions:
   - How is this different from existing health chatbots?
   - What about privacy and PII?
   - Can this replace doctor consultations?
   - How do you handle hallucinations?
   - What's the business model?
   - What's next in the roadmap?

5. **Key metrics/statistics to mention** that show progress and legitimacy

Format the output in markdown with clear sections, bullet points where appropriate, and bold for emphasis. Make it easy to reference during the presentation.
```

---

## HOW TO USE THIS PROMPT:

1. **Copy the entire "PROMPT FOR CHATGPT" section** (from the triple backticks)
2. **Paste it into ChatGPT** (https://chat.openai.com)
3. **ChatGPT will generate**:
   - Complete 10-slide presentation outline
   - Speaker notes for delivery
   - Technical demo walkthrough
   - Q&A preparation
   - Metrics to emphasize

4. **Optional follow-ups you can ask ChatGPT**:
   - "Make the presentation more technical for a technical audience"
   - "Add more emphasis on the Responsible AI aspects"
   - "Create a condensed 5-minute version for quick pitch"
   - "Generate presentation slides in JSON format I can use with presentation software"
   - "Make the demo script more interactive with audience engagement"

---

## ADDITIONAL RESOURCES FOR YOUR PRESENTATION:

- **Architecture Diagram**: Located in `docs/architecture.md` (shows Mermaid diagram)
- **Agent Flow**: Details in `docs/agent-flow.md`
- **Responsible AI Policy**: In `docs/responsible-ai.md`
- **Commercialization Plan**: In `docs/commercialization.md`
- **Live API Docs**: Running at http://localhost:8000/docs

---

## TIPS FOR DELIVERY:

1. **Start with the problem** - Make it relatable (everyone searches for health info online)
2. **Show the solution visually** - Use the architecture diagram
3. **Demonstrate live** - Run the API and show responses
4. **Emphasize safety** - Highlight Responsible AI safeguards
5. **End with vision** - Talk about commercialization and real-world impact
6. **Be humble** - Mention this is Phase 1-4; acknowledge what's still to come

