# Commercialization Concept — PublicHealth-AI

**Status:** Mid-evaluation concept only. Prices below are **proposed examples**, not market quotes.

## Product

B2B / B2G **evidence-grounded public health Q&A** over an organization-approved document corpus (WHO, CDC, ministry guidelines, internal SOPs).

## Target users

- Public health organizations  
- Hospitals and clinic networks  
- NGOs working on community health  
- Government health departments  
- Research / academic public-health units  

## Value proposition

- Faster access to **cited** guideline content for staff and call-centre agents  
- Transparent IR trail (evidence + sources) for audit and training  
- Configurable refusal of diagnosis/dosage-style requests (Responsible AI)  
- Deployable with organization-controlled documents (no fabricated sources)

## Business model

| Model | Description |
|-------|-------------|
| Subscription (SaaS) | Per-seat or per-org monthly access to hosted assistant |
| Enterprise license | Annual license + support for on-prem / private cloud |
| Government / private deployment | Custom corpus ingestion + SLA |

## Proposed example pricing (illustrative only)

| Tier | Proposed example | Includes (example) |
|------|------------------|--------------------|
| Pilot | ~$200–500 / month | Single department, sample corpus size, email support |
| Organization | ~$1,500–4,000 / month | Multi-user, custom document ingest, SSO-ready roadmap |
| Enterprise / Gov | Custom quote | On-prem, dedicated corpus, audit logs, training |

**Label:** These figures are **proposed examples for the assignment**, not actual market prices.

## Deployment ideas

1. **Cloud SaaS** — managed FastAPI + vector store; org uploads approved PDFs  
2. **Private VPC** — same stack inside customer cloud  
3. **On-prem** — air-gapped ministry/hospital networks with local LLM option later  

## Go-to-market (simple)

1. Pilot with a university / NGO health desk  
2. Expand corpus to ministry guidelines  
3. Sell seats to clinic networks and public-health call centres  

## Risks & ethics (commercial)

- Must never market as diagnostic software without appropriate regulation  
- Clear disclaimers and human escalation paths  
- Data protection agreements for any logged queries  
