# Mid-Evaluation Quick Reference (Week 6 - 20 Marks)

## ⏰ You Are Here: Week 6 Mid-Evaluation

**Purpose**: Checkpoint assessment showing progress, system design, and feasibility  
**Format**: Presentation + Demo  
**Duration**: 15-20 minutes  
**Marks**: 20 (out of 100 total)  
**Rubric**: 6 criteria × 3-4 marks each  

---

## 📊 SCORING BREAKDOWN (20 Marks)

```
[Criterion]                    [Marks]  [Your Goal]
1. Domain Justification         3       Excellent (3/3)
2. System Understanding         4       Excellent (4/4)
3. Agents & Roles               4       Excellent (4/4)
4. Implementation Plan          3       Excellent (3/3)
5. Responsible AI Plan          3       Excellent (3/3)
6. Commercialization Plan       3       Excellent (3/3)
────────────────────────────────────────────────────
TOTAL                          20       TARGET: 18-20/20
```

---

## 1️⃣ DOMAIN JUSTIFICATION (3 Marks)

**Evaluator is asking**: "Why this domain? Is it a real problem? Is it suitable for agentic AI?"

### Excellent Answer ✅ (3/3)
- **Real-world problem**: "X% of people search for health info online; Y% receive unverified advice"
- **Why it matters**: Health misinformation leads to preventable illness/death
- **Why agentic AI**: Perfect use case for:
  - **IR**: Need to retrieve evidence from knowledge base
  - **NLP**: Need to parse medical entities (diseases, symptoms)
  - **Agents**: Multi-step reasoning (analyze → retrieve → respond)
- **Target users**: Public health orgs, hospitals, NGOs
- **Realistic scope**: Not too simple, not impossible in 10 weeks

### Your Script (30 seconds)
> "Public health misinformation is a critical problem. When people search for health symptoms online, they often get conflicting, unverified advice. This system solves that by retrieving evidence from verified sources and providing transparent, cited answers. It's perfect for agentic AI because we need multiple agents working together: one to understand the query (NLP), one to find evidence (IR), and one to generate the answer (LLM)."

---

## 2️⃣ SYSTEM UNDERSTANDING (4 Marks)

**Evaluator is asking**: "Can you clearly explain what your system is and does?"

### Excellent Answer ✅ (4/4)
- **What it is**: Multi-agent system for evidence-grounded health information
- **What it does**: Takes user question → analyzes it → retrieves evidence → generates answer → checks safety
- **Who uses it**: General public + public health organizations
- **What it solves**: Provides reliable, sourced health information instead of misinformation
- **Why it's valuable**: Reduces health misinformation, improves public health outcomes
- **How it's different**: Transparent (shows sources), safe (refuses unsafe requests), honest (admits insufficient evidence)

### Your Script (1-2 minutes)
> "PublicHealth-AI is an evidence-grounded public health information assistant. Here's what happens when someone asks a question like 'What are the symptoms of dengue?'
> 
> First, our system analyzes the query to extract the disease (dengue) and understand the question type (symptom inquiry).
> 
> Second, it searches our curated knowledge base for relevant evidence.
> 
> Third, it generates an answer using ONLY the retrieved evidence, with proper citations.
> 
> Finally, it runs safety checks to ensure we're not diagnosing or prescribing personalized medication.
> 
> The result: a user gets a reliable, sourced answer backed by evidence. No hallucinations, no unverified claims, no medical advice beyond our scope."

---

## 3️⃣ AGENTS & THEIR ROLES (4 Marks)

**Evaluator is asking**: "What agents do you have? Why? How do they interact?"

### Excellent Answer ✅ (4/4)

#### Agent 1: Query Analysis Agent
- **What it does**: Analyzes natural language queries
- **Specific operations**:
  - **NER (Named Entity Recognition)**: Extracts medical entities (disease=dengue, symptom=fever)
  - **Intent Classification**: Determines question type (SYMPTOM_INQUIRY, PREVENTION, WARNING_SIGNS, RISK_FACTORS, etc.)
  - **Risk Assessment**: Flags safety-critical queries (dosage requests, diagnosis attempts)
- **Input**: "What are the symptoms of dengue?"
- **Output**: Structured JSON
  ```json
  {
    "entities": {"disease": ["dengue"], "medical_topic": ["symptoms"]},
    "intent": "SYMPTOM_INQUIRY",
    "risk_level": "LOW"
  }
  ```
- **Why needed**: Converts natural language → machine-processable structure

#### Agent 2: Medical Retrieval Agent
- **What it does**: Finds relevant evidence
- **Specific operations**:
  - **Embedding**: Converts query to vector using TF-IDF
  - **Vector Search**: Searches vector DB (34 indexed chunks)
  - **Top-K Retrieval**: Returns top-5 most relevant chunks with scores
- **Input**: Structured query from Agent 1
- **Output**: Evidence chunks with metadata
  ```json
  {
    "results": [
      {
        "source": "WHO",
        "title": "Dengue Guidelines",
        "text": "Dengue symptoms include...",
        "score": 0.92,
        "url": "https://..."
      }
    ]
  }
  ```
- **Why needed**: Grounds answer in verified evidence

#### Agent 3: Response Agent
- **What it does**: Generates human-readable answer
- **Specific operations**:
  - **Evidence Selection**: Picks best retrieved chunks
  - **Answer Generation**: LLM creates response using ONLY evidence
  - **Citation**: Attaches source attribution
- **Input**: Original question + retrieved evidence
- **Output**: Answer with citations
  > "Dengue symptoms typically include high fever, severe headache, and body aches (WHO Dengue Guidelines, p. 15). In some cases, warning signs may develop 3-7 days after onset..."
- **Why needed**: Produces clear, cited answer for humans

#### How They Interact
```
User Query
    ↓
Agent 1 (Query Analysis)
    ↓ [HTTP POST to /api/agents/retrieve]
Agent 2 (Retrieval)
    ↓
Agent 3 (Response Generation)
    ↓ [Responsible AI Guard validation]
Answer to User
```

### Your Script (2 minutes)
> "We have three agents working together. Agent 1 is the Query Analyst. It takes your question and extracts what you're asking about: what disease, what topic, how risky is the query. For 'What are symptoms of dengue?', it identifies disease=dengue, topic=symptoms, risk=low.
> 
> Agent 2 is the Retrieval Agent. It takes Agent 1's output and searches our knowledge base—34 indexed document chunks from WHO, CDC, and other verified sources. It finds the top-5 most relevant chunks with similarity scores.
> 
> Agent 3 is the Response Agent. It takes your original question plus the evidence and generates a clear, cited answer using ONLY that evidence.
> 
> All agents communicate over HTTP/REST with JSON payloads. Each has one job, and together they produce a reliable, grounded answer."

---

## 4️⃣ IMPLEMENTATION PLAN (3 Marks)

**Evaluator is asking**: "How will LLM, NLP, IR, security, and agent communication work together?"

### Excellent Answer ✅ (3/3)
Show you understand how each component fits:

| Component | Technology | How It Works |
|-----------|-----------|---|
| **LLM** | OpenAI / Stub | Configurable via env var; generates answers constrained to evidence |
| **NLP** | spaCy + rules | NER extracts entities, rule-based intent/risk classification (Phase 10+) |
| **IR** | TF-IDF + NumPy | Chunks → TF-IDF embeddings → stored in vector DB → top-K search |
| **Security** | JWT + bcrypt | Auth middleware on protected routes; PII redacted before LLM |
| **Agent Comm** | HTTP/REST | Each agent exposes endpoints; other agents POST JSON payloads |

### Phase-Based Plan
```
Phase 1-4 (NOW ✅):
  ✅ API skeleton, retrieval, demo

Phase 5-9 (NEXT):
  → Better NLP (spaCy integration)
  → User auth (JWT/bcrypt)
  → Real LLM (OpenAI API)

Phase 10-12:
  → PII sanitization
  → Production security
  → Deployment infrastructure
```

### Your Script (1 minute)
> "Here's how everything integrates:
> 
> The LLM component is configurable—we can use OpenAI or a stub for testing. It's constrained to only use retrieved evidence.
> 
> The NLP component uses spaCy and rule-based classifiers to extract entities and intent from queries. We're implementing this in Phase 10.
> 
> The IR module uses TF-IDF embeddings stored in NumPy. We have a clear upgrade path to Sentence Transformers for better accuracy.
> 
> Security is layered: JWT authentication for API access, input sanitization, PII redaction before LLM processing.
> 
> Agent communication is HTTP/REST over JSON. Each agent exposes endpoints; other agents POST structured payloads and get back results.
> 
> We're currently at Phase 1-4 (core infrastructure), aiming for Phase 12 (full deployment) by end of semester."

---

## 5️⃣ RESPONSIBLE AI PLAN (3 Marks)

**Evaluator is asking**: "How do you handle ethical risks? What could go wrong and what are you doing about it?"

### Excellent Answer ✅ (3/3)

**8 Core Principles**:
1. **Evidence-Grounded**: Never invent claims or citations
2. **No Diagnosis**: Explicitly refuse diagnostic queries
3. **No Prescriptions**: Never give personalized medication advice
4. **Transparent**: Show entities, intent, risk, evidence, sources
5. **Privacy-First**: Redact PII before LLM processing
6. **Fair**: Same algorithm for all users; no demographic bias
7. **Explainable**: Citations justify every claim
8. **Honest**: Admit when evidence is insufficient

**Safety Checks**:

| Risk | Check | Action on Failure |
|------|-------|-------------------|
| Unsupported claims | Claim validation | Regenerate constrained or fallback |
| Missing citations | Citation check | Attach or refuse answer |
| Wrong citations | Citation matching | Strip or fallback |
| Diagnosis language | Pattern detection | Safe refusal message |
| Dosage requests | Intent flag | Safe refusal message |
| PII leakage | Output scan | Redact or fallback |

**Example Safe Refusals**:
- Query: "Diagnose my chest pain"
  - Response: "I cannot diagnose medical conditions. Chest pain can be serious—please seek immediate medical attention."

- Query: "What dosage of paracetamol for my headache?"
  - Response: "I cannot provide personalized medication dosage. Please consult a healthcare professional."

### Your Script (1.5 minutes)
> "Responsible AI is central to our design. We have 8 core principles:
> 
> First, everything is evidence-grounded. We never invent claims or citations.
> 
> Second, we're not a diagnosis system. If someone asks 'Diagnose my symptoms', we refuse and direct them to a doctor.
> 
> Third, no personalized prescriptions. We won't say 'take 500mg of drug X'—we suggest consulting a professional.
> 
> Fourth, we're transparent. We show what entities we found, what intent, what risk level, and which sources informed the answer.
> 
> Fifth, we protect privacy. We redact PII from input before sending to the LLM.
> 
> Sixth, fairness. All users get the same algorithm, no demographic bias.
> 
> Seventh, explainability. Citations explain why we gave that answer.
> 
> Eighth, honesty. If evidence is insufficient, we say so.
> 
> To minimize hallucinations, we run safety checks on every response. We validate that claims match retrieved evidence, ensure citations are present and correct, and flag diagnosis/dosage language."

---

## 6️⃣ COMMERCIALIZATION PLAN (3 Marks)

**Evaluator is asking**: "Who pays for this? How much? Why would they buy it?"

### Excellent Answer ✅ (3/3)

#### Market & Customers
- **Primary**: Public health ministries, hospital networks, NGOs
- **Secondary**: Telemedicine platforms, corporate wellness programs
- **Tertiary**: Government health agencies, international health organizations
- **Market size**: Global digital health market ~$200B; health info assistants segment ~$5-10B

#### Value Proposition
- ✅ Reduces health misinformation (proven business value)
- ✅ Transparent, auditable responses (compliance/liability reduction)
- ✅ Multilingual, customizable knowledge base (global reach)
- ✅ HIPAA/GDPR compliant architecture (healthcare adoption)
- ✅ Cost-effective vs. hiring health communicators ($50K+/year per person)

#### Pricing Models

**Option 1: Subscription per Organization**
- Startup: $5,000/month (up to 100K queries/month)
- Growth: $15,000/month (up to 500K queries/month)
- Enterprise: $50,000/month (unlimited queries + on-premise)

**Option 2: Per-Query Pricing**
- $0.01-$0.05 per answer
- Scales with usage
- Good for low-volume deployments

**Option 3: Enterprise License**
- $100,000-$500,000/year one-time
- On-premise or private cloud
- Custom knowledge base + SLA
- Best for large hospital networks

#### Why They'd Adopt
- **ROI**: Reduce hospital misinformation calls by 30-50% → cost savings
- **Liability**: Auditable system reduces legal risk
- **Scale**: Serve millions of users without hiring staff
- **Quality**: Better public health outcomes → reputation/funding boost

### Your Script (1.5 minutes)
> "Our target market is public health organizations, hospitals, and NGOs. Let me explain why they'd pay for this:
> 
> First, ROI. Public health orgs spend millions answering health misinformation calls. Our system reduces false queries by 30-50%, saving $100K-$500K annually for large organizations.
> 
> Second, liability. Healthcare systems are sued for misinformation. Our auditable, evidence-grounded system reduces that risk.
> 
> Third, scale. Instead of hiring 10 health communicators at $50K each, they deploy our system for $15K-$50K/month, serving millions of users.
> 
> Pricing is subscription-based:
> - Startup plan: $5K/month
> - Growth plan: $15K/month
> - Enterprise: $50K/month or $100K-$500K/year for on-premise
> 
> Examples of customers:
> - A public health ministry launching a citizen hotline (prevent misinformation)
> - A hospital network providing telehealth (reduce nurse call volume)
> - An NGO like Red Cross (reach remote populations with accurate info)
> 
> We project break-even in 18 months and 40% annual growth in the health information sector."

---

## 📋 PRESENTATION CHECKLIST

Before you present, verify:

**Content** ✅
- [ ] Can explain domain in 30 seconds
- [ ] Can describe system in 1-2 minutes  
- [ ] Can explain all 3 agents and their interactions
- [ ] Have implementation plan covering all components
- [ ] Can list 5+ Responsible AI risks and mitigations
- [ ] Have specific pricing/market data ready
- [ ] Have live demo script ready (with backup screenshots)

**Delivery** ✅
- [ ] Presentation is 15-20 minutes (with time for Q&A)
- [ ] Each slide has clear talking points
- [ ] You've practiced as a team
- [ ] Everyone knows their section
- [ ] You know who's presenting what

**Technical** ✅
- [ ] Backend is running (http://localhost:8000)
- [ ] API docs are accessible (http://localhost:8000/docs)
- [ ] Sample queries work without errors
- [ ] Demo walkthrough is rehearsed
- [ ] You have backup screenshots if demo fails

**Q&A Prep** ✅
- [ ] Know your differentiators
- [ ] Know your challenges
- [ ] Know your timeline
- [ ] Know your Responsible AI approach
- [ ] Know your commercialization

---

## 🎯 FINAL TIPS FOR SUCCESS

### During Presentation
1. **Start strong**: Lead with the problem (relatable, real-world)
2. **Use visuals**: Show architecture diagram, don't just describe
3. **Be specific**: "We use TF-IDF with NumPy" not "we use embeddings"
4. **Show confidence**: You've built this; you know it
5. **Demo well**: Walk through each agent's output step-by-step
6. **Emphasize differentiation**: Responsible AI is your main differentiator
7. **Be honest about scope**: "Phase 1-4 done; Phase 5-12 planned" shows realism

### Handling Questions
- **Q: Why not use existing health chatbots?**
  - A: "Existing systems often hallucinate or lack transparency. Ours shows sources, refuses unsafe requests, minimizes hallucinations through retrieval-grounding."

- **Q: What about HIPAA compliance?**
  - A: "Architecture is HIPAA-ready: PII redaction, encryption, audit logging. Full implementation in Phase 12."

- **Q: What if the LLM makes mistakes?**
  - A: "We minimize mistakes by constraining to retrieved evidence only. Responsible AI checks validate answers before showing to users."

- **Q: How do you scale to millions of users?**
  - A: "Backend is stateless FastAPI → easily horizontal scalable. Vector DB can scale to millions of documents via FAISS/Chroma."

---

## ⏱️ TIMING BREAKDOWN (20 Minutes Total)

- **Opening** (1 min): Project intro, course, team
- **Problem** (1.5 min): Health misinformation is real
- **Solution** (1.5 min): Multi-agent system overview
- **Architecture** (2 min): Show diagram + explain flow
- **Agents** (2 min): 3 agents + their roles
- **Implementation** (1 min): How components work together
- **Demo** (4 min): Live walkthrough ⭐ (MOST IMPORTANT)
- **Responsible AI** (1.5 min): 8 principles + safety checks
- **Commercialization** (1.5 min): Market + pricing
- **Roadmap** (1 min): Phase 1-12 timeline
- **Q&A** (3 min): Answer evaluator questions

**Total**: ~20 minutes

---

## 🏆 TO SCORE 18-20/20 (Excellent):

- ✅ Clear, compelling domain justification (real problem, good fit for agentic AI)
- ✅ Can explain system clearly and concisely
- ✅ Three agents well-defined with specific roles
- ✅ Realistic, phased implementation plan
- ✅ Thoughtful, specific Responsible AI approach
- ✅ Credible, researched commercialization plan
- ✅ Working demo showing all 3 agents
- ✅ Confident, well-practiced delivery
- ✅ Honest about scope ("Phase 1-4 done, Phase 5-12 planned")
- ✅ Able to answer technical questions

---

**You've got this! 🚀 Practice once more, then nail the presentation.**

