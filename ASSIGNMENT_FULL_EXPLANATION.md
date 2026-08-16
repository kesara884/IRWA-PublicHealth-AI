# IT 3041 Assignment Brief — Complete Explanation & Your Project Alignment

## 📋 ASSIGNMENT OVERVIEW

**Course**: Information Retrieval and Web Analytics (IT 3041)  
**Assignment**: Design and Implementation of an Agentic AI-Based System  
**Instructor**: Mr. Samadhi Chathuranga Rathnayake  
**Duration**: 10 weeks (Week 1-11)  
**Total Marks**: 100

---

## ⏰ PROJECT TIMELINE

| Week | Activity | Your Status |
|------|----------|-------------|
| Week 1 | Group registration (3-4 students) | ✅ Done |
| Week 2 | Domain selection + Report template released | ✅ Done (Public Health) |
| Week 3 | Assignment officially begins | ✅ In Progress |
| **Week 6** | **Mid Evaluation** ⭐ | 🎯 THIS IS HAPPENING SOON |
| Week 10 | Final Submissions (Video, Report, GitHub) | 📅 Upcoming |
| Week 11 | Viva (Oral Exam) | 📅 Upcoming |

**Your Project**: PublicHealth-AI (Evidence-Grounded Public Health Information Assistant)

---

## 🎯 WHAT YOU MUST BUILD

Your system **MUST** include:

### 1. **Two or More Interacting Intelligent Agents** ✅
Your project has **THREE**:
- ✅ **Query Analysis Agent**: Analyzes user queries (NER, intent, risk classification)
- ✅ **Medical Retrieval Agent**: Searches knowledge base for evidence
- ✅ **Response Agent**: Generates evidence-based answers

### 2. **One or More Large Language Models (LLMs)** ✅
- Configurable LLM (OpenAI or stub for testing)
- Evidence-only response generation
- No hallucinations allowed

### 3. **Natural Language Processing (NLP)** ✅
- Named Entity Recognition (NER): Extract diseases, symptoms, medical topics
- Intent Classification: "SYMPTOM_INQUIRY", "PREVENTION", "WARNING_SIGNS"
- Risk Assessment: Flag high-risk queries (e.g., personal dosage requests)

### 4. **Information Retrieval (IR) Module** ✅
- Vector search using TF-IDF embeddings
- Document chunking and metadata preservation
- Top-K retrieval (default: top-5 chunks)
- Future: Hybrid search with BM25

### 5. **Security Features** ✅
- **Authentication**: JWT tokens + password hashing (bcrypt)
- **Input Sanitization**: PII redaction before LLM processing
- **Encryption**: Environment variables via .env
- **Access Control**: Protected API endpoints

### 6. **Defined Agent Communication Protocol** ✅
- **Protocol**: HTTP/REST + JSON
- **Communication Flow**:
  ```
  Agent 1 (Query Analysis) 
    → POST /api/agents/retrieve 
    → Agent 2 (Retrieval)
  ```
- Agents exchange structured JSON payloads
- Explicit endpoints for each agent operation

### 7. **Responsible AI Practices** ✅
- **Fairness**: Same pipeline for all users
- **Explainability**: Shows entities, intent, risk, evidence, sources
- **Transparency**: Citations match retrieved documents
- **Privacy**: Redacts PII, no logging of sensitive data
- **Ethical Guardrails**: Refuses diagnoses, rejects personalized dosages
- **Honest Uncertainty**: Admits when evidence is insufficient

### 8. **Commercialization Strategy** ✅
- **Target Market**: Public health orgs, hospitals, NGOs, government
- **Pricing Model**: B2B/B2G subscription per organization
- **Deployment**: On-premise or cloud-based
- **Value Prop**: Reliable sourced health information with transparency

---

## 📊 EVALUATION BREAKDOWN (100 Marks Total)

| Component | Marks | When | Your Focus |
|-----------|-------|------|-----------|
| **Mid Evaluation** | 20 | Week 6 | ⭐ **THIS IS NOW** |
| Gen AI Video | 25 | Week 10 | Video presentation |
| Report + GitHub | 35 | Week 10 | Technical documentation |
| Viva | 20 | Week 11 | Oral examination |
| **TOTAL** | **100** | | |

---

## 🎤 MID-EVALUATION (20 Marks) — WEEK 6

This is what you're doing **NOW**. You must present/demonstrate:

### 1. **Domain Justification** (3 Marks)
**What they're looking for**: Why did you choose public health?

**Your answer**:
- ❌ Problem: Public seeks unverified health info online
- ✅ Suitability: Perfect for IR (retrieval grounding) + NLP (NER for diseases) + Agentic AI
- ✅ Real-world impact: Reduces health misinformation
- ✅ Target users: Public health orgs, hospitals, NGOs

### 2. **System Understanding** (4 Marks)
**What they're looking for**: Can you clearly explain your system?

**Your answer**:
- ✅ What it is: Multi-agent system for evidence-grounded health info
- ✅ Problem it solves: Unverified, unsafe health advice
- ✅ Target users: Public + public health organizations
- ✅ How it works: Query → Analysis → Retrieval → Evidence Response → Safety Check
- ✅ Why it matters: Transparent, cited, refuses unsafe requests

### 3. **Agents and Their Roles** (4 Marks)
**What they're looking for**: Clear agent definitions and interactions

**Your answer**:
- ✅ **Agent 1 - Query Analysis**:
  - Input: User question
  - Process: NER (extract medical entities), Intent (classify question type), Risk (assess safety level)
  - Output: Structured JSON
  - Why needed: Converts natural language to machine-processable format

- ✅ **Agent 2 - Medical Retrieval**:
  - Input: Structured query
  - Process: Embed query using TF-IDF, search vector DB, get top-5 chunks
  - Output: Evidence with metadata and scores
  - Why needed: Finds factual ground truth in knowledge base

- ✅ **Agent 3 - Response Generation**:
  - Input: User question + retrieved evidence
  - Process: LLM generates answer using ONLY evidence
  - Output: Answer with citations
  - Why needed: Produces human-readable, grounded response

- ✅ **How they interact**: Agent 1 → Agent 2 (over HTTP/REST) → Agent 3 → Responsible AI Guard

### 4. **Implementation Plan** (3 Marks)
**What they're looking for**: How will everything work together?

**Your answer**:
- ✅ **LLM Integration**: Configured via env var; generates constrained responses
- ✅ **NLP Components**: spaCy for NER (Phase 10+), rule-based intent/risk
- ✅ **IR Module**: TF-IDF embeddings → NumPy vector store → top-K retrieval
- ✅ **Security**: JWT auth, PII redaction, encrypted config
- ✅ **Agent Communication**: HTTP/REST endpoints with JSON payloads
- ✅ **Timeline**: Phases 1-12 mapped out (currently at Phase 1-4)

### 5. **Responsible AI Plan** (3 Marks)
**What they're looking for**: How do you handle ethical risks?

**Your answer**:
- ✅ **Fairness**: Same logic for all queries, no demographic bias
- ✅ **Transparency**: Shows entities, intent, risk, evidence, sources
- ✅ **Explainability**: Citations justify answers; score explains relevance
- ✅ **Privacy**: Redacts PII, never logs sensitive data
- ✅ **Honesty**: Admits insufficient evidence; refuses unsafe requests
- ✅ **Specific safety checks**:
  - Diagnosis refusal: "I'm not a clinician"
  - Dosage refusal: "Consult healthcare professional"
  - Citation validation: Ensure claims match evidence
  - No hallucinations: Evidence-only generation

### 6. **Commercialization Plan** (3 Marks)
**What they're looking for**: Who would pay for this? How much?

**Your answer**:
- ✅ **Target Market**: 
  - Public health ministries
  - Hospital networks
  - NGOs (WHO, Red Cross, etc.)
  - Government health agencies
  
- ✅ **Value Proposition**:
  - Reduces health misinformation
  - Transparent, auditable responses
  - Customizable knowledge base (local diseases, languages)
  - HIPAA-compliant architecture
  
- ✅ **Pricing Model** (Examples):
  - Subscription: $5,000-$50,000/month per organization (tiered by size)
  - Per-query pricing: $0.01-$0.05 per answer
  - Enterprise license: $100,000+/year with on-premise deployment
  
- ✅ **Why they'd adopt**:
  - Reduces liability (grounded in evidence)
  - Improves public health messaging
  - Cost-effective vs. hiring health communicators
  - Scalable to millions of users

---

## 📽️ MID-EVALUATION PRESENTATION FORMAT

**Duration**: 15-20 minutes  
**Components**:

1. **Opening** (30 sec)
   - Project title, team names, course
   - Hook: "Health misinformation kills. Our system prevents it."

2. **Problem Statement** (1 min)
   - Show statistics: % of people seeking health info online
   - Show problem: conflicting advice, no sources, unsafe recommendations
   - Why it matters: lives affected

3. **Solution Overview** (1 min)
   - Multi-agent system diagram
   - How it solves the problem
   - Key differentiator: retrieval-grounded, transparent, refuses unsafe requests

4. **System Architecture** (2 min)
   - Show Mermaid diagram
   - Walk through data flow: User → Frontend → API → Agents → Response → User
   - Highlight agent communication protocol (HTTP/REST)

5. **Agent Roles** (2 min)
   - Agent 1: Query Analysis (NER, intent, risk)
   - Agent 2: Retrieval (vector search)
   - Agent 3: Response (LLM evidence-only)
   - Show example JSON payloads

6. **Demo** (3-4 min) ⭐ **MOST IMPORTANT**
   - Live query: "What are symptoms of dengue?"
   - Show each agent's output
   - Show retrieved evidence with sources
   - Show final answer with citations
   - Show safe refusal for: "What's the dosage of paracetamol?"

7. **Responsible AI** (1.5 min)
   - List 8 principles
   - Show safety checks
   - Explain how you minimize hallucinations

8. **Commercialization** (1 min)
   - Market size
   - Pricing strategy
   - Examples of target customers

9. **Roadmap & Challenges** (1 min)
   - What's done (Phases 1-4)
   - What's next (Phases 5-12)
   - Any blockers

10. **Q&A** (2-3 min)
    - Be ready for technical questions
    - Have statistics ready
    - Know your differentiators

---

## ✅ MID-EVALUATION CHECKLIST

Before your presentation, verify:

- [ ] Can you explain the domain choice in 30 seconds?
- [ ] Can you describe your system in 1-2 minutes?
- [ ] Can you explain what each agent does and how they communicate?
- [ ] Do you have a realistic implementation plan covering LLM + NLP + IR + Security + Agent comm?
- [ ] Can you list 5+ Responsible AI risks and your mitigations?
- [ ] Can you pitch your commercialization (market + pricing) convincingly?
- [ ] Can you run a live demo showing all 3 agents in action?
- [ ] Have you practiced your presentation to 15-20 minutes?
- [ ] Do you have speaker notes/script prepared?
- [ ] Does your team know their individual parts?

---

## 🔴 COMMON MID-EVAL MISTAKES TO AVOID

1. ❌ **Vague agent explanations**: "The agent does stuff" → ✅ Specify: NER extracts disease, intent classifies question type, risk flags unsafe queries
2. ❌ **No demo**: Talking theory only → ✅ Show live API call with output
3. ❌ **Weak Responsible AI**: Generic privacy talk → ✅ Specific: "We refuse diagnosis queries; cite all claims"
4. ❌ **Unrealistic implementation plan**: "We'll use GPT-4 + FAISS + spaCy in 2 weeks" → ✅ Realistic: "Phase-based rollout; MVP is TF-IDF + stub LLM"
5. ❌ **No commercialization**: "Uh, hospitals?" → ✅ Specific market, pricing per org, deployment strategy
6. ❌ **Wrong domain**: Picked something too simple/complex for the time → ✅ Public health is perfect: real-world problem + perfect for IR/NLP/agents

---

## 📄 YOUR PRESENTATION OUTLINE

### Slide 1: Title
- PublicHealth-AI
- Team members
- IT 3041

### Slide 2: Problem
- "Public seeks health info online → misinformation → health risks"
- Stats: X% of people Google symptoms, Y% get conflicting advice
- Why it matters: Lives affected, unnecessary anxiety

### Slide 3: Solution
- Multi-agent system with NLP + IR + LLM
- Retrieval-grounded: answers backed by evidence
- Transparent: shows sources and reasoning
- Safe: refuses unsafe requests

### Slide 4: Architecture
- Show Mermaid diagram
- User → Frontend → Backend → Agents → Response → User

### Slide 5: Agent Roles
- Query Analysis Agent: NER, intent, risk
- Retrieval Agent: Vector search
- Response Agent: Evidence-based answer

### Slide 6: Communication Protocol
- HTTP/REST + JSON
- Example: Agent 1 POSTs to /api/agents/retrieve → Agent 2

### Slide 7: IR/RAG Pipeline
- Chunk documents → Create embeddings → Store in vector DB → Retrieve top-5 → Generate answer with citations

### Slide 8: Live Demo
- Show http://localhost:8000/docs
- Make API call
- Show output

### Slide 9: Responsible AI
- 8 principles + safety checks
- Examples: Diagnosis refusal, dosage refusal, citation validation

### Slide 10: Commercialization
- Market: Public health orgs
- Pricing: $5K-$50K/month
- Why they'd adopt: Reduce misinformation, improve messaging

### Slide 11: Roadmap
- Phase 1-4 done ✅
- Phase 5-12: NLP, security, LLM, deployment

### Slide 12: Q&A
- Be ready for technical questions
- Know your differentiators

---

## 🎬 LIVE DEMO SCRIPT

**Scenario**: User asks "What are the symptoms of dengue?"

**Step 1** (30 sec):
- Go to http://localhost:8000/docs
- Find `/api/query/analyze` endpoint
- Say: "First, we analyze the query for medical entities and intent"

**Step 2** (30 sec):
- Make request with query: "What are the symptoms of dengue?"
- Show output JSON:
  ```json
  {
    "entities": {"disease": ["dengue"]},
    "intent": "SYMPTOM_INQUIRY",
    "risk_level": "LOW"
  }
  ```
- Say: "Agent 1 identified dengue as the disease and this is a symptom inquiry (low risk)"

**Step 3** (1 min):
- Find `/api/retrieval/search` endpoint
- Make request: `{"query": "dengue symptoms"}`
- Show results: top-5 chunks with scores and sources
- Say: "Agent 2 searched our knowledge base and found 5 relevant sources"

**Step 4** (30 sec):
- Find `/api/query` endpoint (full pipeline)
- Make request: `{"query": "What are the symptoms of dengue?"}`
- Show final answer with citations
- Say: "Agent 3 generated an answer using ONLY the retrieved evidence"

**Step 5 - Refusal Demo** (30 sec):
- Make request: "What dosage of paracetamol should I take?"
- Show safe refusal message
- Say: "Our safety checks prevent us from giving personalized medical advice"

**Total Demo Time**: ~4 minutes

---

## 🎓 WHAT EVALUATORS WILL MARK YOU ON

### Mid-Evaluation Marking Rubric (20 Marks Total)

| Criterion | Excellent | Good | Satisfactory | Poor | Your Goal |
|-----------|-----------|------|--------------|------|-----------|
| **Domain Choice** (3 marks) | Strong justification, real-world impact | Clear, good understanding | Basic justification, weakly explained | Cannot justify | **Aim for Excellent** |
| **System Understanding** (4 marks) | Clearly explains what it is, why needed, value | Good explanation, minor gaps | General understanding, some unclear | Cannot explain | **Aim for Excellent** |
| **Agents & Roles** (4 marks) | Clearly identifies agents, explains roles, interactions | Clear with minor gaps | Basic identification only | Poorly defined | **Aim for Excellent** |
| **Implementation Plan** (3 marks) | Clear, realistic, shows understanding of all components | Good plan, most important parts | Basic plan, several unclear | Unrealistic | **Aim for Good/Excellent** |
| **Responsible AI** (3 marks) | Identifies all risks, provides realistic solutions | Major concerns addressed | Basic awareness only | Little understanding | **Aim for Excellent** |
| **Commercialization** (3 marks) | Clear market, pricing, deployment, convincing ROI | Reasonable concept | Basic idea, lacks depth | Unclear/unrealistic | **Aim for Good/Excellent** |

**Key to Scoring High**:
- Specificity: "We use TF-IDF with NumPy" ✅ not "We use embeddings" ❌
- Justification: "This domain is good for IR because..." ✅
- Demo: Show working system ✅
- Honesty: "Phase 1-4 done, Phase 5-12 planned" ✅

---

## 📚 DELIVERABLES SUMMARY

### Week 6 - Mid Evaluation (20 marks)
- ✅ Presentation (system, agents, demo, RAI, commercialization)

### Week 10 - Final Submissions (60 marks total)
- **Gen AI Video** (25 marks): 3-5 min explanation using Synthesia, HeyGen, etc.
- **Report** (30 marks): Technical documentation (see template in Week 2)
- **GitHub Repo** (5 marks): Well-organized code with README

### Week 11 - Viva (20 marks)
- Oral examination on technical depth, individual contribution, RAI, commercialization

---

## 🚀 NEXT STEPS FOR SUCCESS

1. **This Week**:
   - [ ] Review this guide
   - [ ] Practice presentation with your team (15-20 min)
   - [ ] Prepare demo script
   - [ ] Test live API calls

2. **Before Presentation**:
   - [ ] Prepare speaker notes
   - [ ] Rehearse Q&A responses
   - [ ] Ensure demo works (have backup screenshots)
   - [ ] Check that all 3 agents can be shown
   - [ ] Verify commercialization strategy is believable

3. **During Presentation**:
   - [ ] Open with engaging problem statement
   - [ ] Use architecture diagram effectively
   - [ ] Show live demo (or pre-recorded fallback)
   - [ ] Emphasize Responsible AI as differentiator
   - [ ] End with vision and roadmap

4. **After Mid-Eval**:
   - [ ] Get feedback from evaluators
   - [ ] Start video production for Week 10
   - [ ] Write technical report
   - [ ] Finalize GitHub repo

---

## 💡 QUICK ANSWERS TO LIKELY QUESTIONS

**Q: Why public health?**
- A: Real-world problem (health misinformation), perfect for IR (retrieval grounding) + NLP (medical entities) + agents (multi-step reasoning)

**Q: How do you ensure citations are correct?**
- A: Every answer is generated from top-K retrieved chunks; claims must map to source documents

**Q: What about hallucinations?**
- A: We don't claim zero; we minimize via retrieval-grounding + citation validation + safety checks

**Q: Why three agents?**
- A: Separation of concerns: Query analysis (NLP) → Retrieval (IR) → Response (LLM). Each agent has one job, communicated via HTTP/REST

**Q: How will this make money?**
- A: B2B/B2G subscription to public health orgs ($5K-$50K/month) who need reliable, auditable health messaging

**Q: What's next?**
- A: Phases 5-12 include: Better NLP (spaCy), real LLM (OpenAI), security (JWT), production deployment

---

## 🎯 FINAL SUCCESS CHECKLIST

✅ **Problem**: Clearly articulated (health misinformation is a real problem)  
✅ **Solution**: Multi-agent system that's specific and believable  
✅ **Agents**: 3 clearly defined agents with explicit roles  
✅ **Communication**: HTTP/REST + JSON protocol between agents  
✅ **Tech Stack**: LLM + NLP + IR + Security mentioned and explained  
✅ **Demo**: Live or pre-recorded system in action  
✅ **Responsible AI**: 8+ principles + specific safety checks  
✅ **Commercialization**: Real market, realistic pricing, clear deployment  
✅ **Timeline**: Realistic phases (you're at 1-4, aiming for 12)  
✅ **Presentation**: 15-20 minutes, practiced, with Q&A prep

---

**You've got this! 🚀 Your PublicHealth-AI project hits every requirement perfectly.**

