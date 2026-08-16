"""Pydantic models for query analysis, retrieval, LLM response, guardrails, and pipeline response."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.retrieval import RetrievalResult


class EntityResult(BaseModel):
    disease: List[str] = Field(default_factory=list)
    symptom: List[str] = Field(default_factory=list)
    medical_condition: List[str] = Field(default_factory=list)
    medical_topic: List[str] = Field(default_factory=list)
    medication: List[str] = Field(default_factory=list)


class QueryAnalysisResult(BaseModel):
    original_query: str
    sanitized_query: str
    intent: str
    entities: EntityResult
    risk_level: str
    pii_detected: bool = False


class AnalyzeRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)


class RetrieveAgentRequest(BaseModel):
    query: str
    intent: str
    entities: Dict[str, List[str]]
    risk_level: str
    top_k: Optional[int] = None


class RetrieveAgentResponse(BaseModel):
    status: str
    results: List[RetrievalResult]
    total_results: int = 0
    search_query: str = ""


class Citation(BaseModel):
    doc_title: str
    source: str
    page: Optional[int] = None
    snippet: Optional[str] = None
    chunk_id: str


class ResponseAgentResult(BaseModel):
    answer: str
    citations: List[Citation] = Field(default_factory=list)
    model_used: str = "stub"
    raw_llm_output: Optional[str] = None


class ResponsibleAIReport(BaseModel):
    safety_passed: bool = True
    pii_detected: bool = False
    refusal_triggered: bool = False
    citation_validation_passed: bool = True
    warnings: List[str] = Field(default_factory=list)
    disclaimer: str = (
        "This assistant provides general public-health information from verified sources "
        "and is not a substitute for professional medical advice, diagnosis, or treatment."
    )


class AgentPipelineStep(BaseModel):
    step: int
    name: str
    status: str
    detail: Optional[str] = None


class QueryPipelineResponse(BaseModel):
    status: str
    analysis: QueryAnalysisResult
    retrieval: Optional[RetrieveAgentResponse] = None
    response: Optional[ResponseAgentResult] = None
    guardrails_report: Optional[ResponsibleAIReport] = None
    steps: List[AgentPipelineStep] = Field(default_factory=list)
    message: Optional[str] = None
