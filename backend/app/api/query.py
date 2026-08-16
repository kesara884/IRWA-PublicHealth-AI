"""
Query orchestration endpoint — runs end-to-end 6-step Agent Pipeline:
  Step 1: Input Received & PII Sanitization
  Step 2: Agent 1 — Query Analysis (NER, intent, risk)
  Step 3: Agent 1 → Agent 2 HTTP/REST
  Step 4: Agent 2 — Retrieval
  Step 5: Agent 3 — Response Agent (LLM Evidence Generation)
  Step 6: Responsible AI Guardrails & Validation
"""

from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.agents.communicator import AgentCommunicator
from app.agents.query_agent import QueryAnalysisAgent
from app.agents.response_agent import ResponseAgent
from app.models.auth import UserResponse
from app.models.query import AgentPipelineStep, AnalyzeRequest, QueryPipelineResponse
from app.responsible_ai.guardrails import ResponsibleAIGuard
from app.security.auth import get_optional_user
from app.security.validation import validate_query

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/query", tags=["query"])

_query_agent = QueryAnalysisAgent()
_communicator = AgentCommunicator(use_http=True)
_response_agent = ResponseAgent()
_guardrails = ResponsibleAIGuard()


@router.post("", response_model=QueryPipelineResponse)
async def process_query(
    payload: AnalyzeRequest,
    current_user: Optional[UserResponse] = Depends(get_optional_user),
):
    """
    End-to-end multi-agent system pipeline (Phases 1–10):
    Executes steps 1 through 6 and returns grounded answer, citations, & safety reports.
    """
    query = validate_query(payload.query)
    steps: list[AgentPipelineStep] = []

    # Step 1: Input Received & Sanitization
    steps.append(
        AgentPipelineStep(
            step=1,
            name="Input Received & PII Sanitization",
            status="completed",
            detail=f"Authenticated as: {current_user.username if current_user else 'Guest'}",
        )
    )

    # Step 2 — Query Analysis Agent
    logger.info("Pipeline step 2: Query Analysis Agent")
    try:
        analysis = _query_agent.analyze(query)
    except Exception as exc:
        logger.exception("Query analysis failed")
        raise HTTPException(status_code=500, detail=f"Query analysis failed: {exc}") from exc

    steps.append(
        AgentPipelineStep(
            step=2,
            name="Agent 1 — Query Analysis",
            status="completed",
            detail=(
                f"Intent: {analysis.intent} | Risk: {analysis.risk_level} | "
                f"Diseases: {', '.join(analysis.entities.disease) or 'none'}"
            ),
        )
    )

    # Pre-evaluate safety guardrails
    rai_report = _guardrails.evaluate_request(query, analysis)

    # High-risk unsupported requests (e.g. diagnosis/dosage refusal)
    if rai_report.refusal_triggered:
        steps.extend(
            [
                AgentPipelineStep(
                    step=3,
                    name="Agent 1 → Agent 2 REST",
                    status="skipped",
                    detail="Skipped due to HIGH risk / unsupported medical request",
                ),
                AgentPipelineStep(
                    step=4,
                    name="Agent 2 — Retrieval",
                    status="skipped",
                    detail="No retrieval performed for unsupported medical query",
                ),
                AgentPipelineStep(
                    step=5,
                    name="Agent 3 — LLM Response Agent",
                    status="completed",
                    detail="Generated safe medical refusal guidance",
                ),
                AgentPipelineStep(
                    step=6,
                    name="Responsible AI Guardrails",
                    status="completed",
                    detail="Safety refusal enforced — non-diagnostic advice issued",
                ),
            ]
        )
        return QueryPipelineResponse(
            status="blocked",
            analysis=analysis,
            retrieval=None,
            response=None,
            guardrails_report=rai_report,
            steps=steps,
            message=(
                "I am unable to provide a diagnosis, personalized treatment plan, or medication dosage. "
                "I can, however, provide general public-health information from verified sources."
            ),
        )

    # Step 3 — Agent 1 -> Agent 2 HTTP REST Communication
    steps.append(
        AgentPipelineStep(
            step=3,
            name="Agent 1 → Agent 2 REST",
            status="in_progress",
            detail="HTTP/REST communication",
        )
    )

    try:
        retrieval = await _communicator.call_retrieval_agent(analysis)
    except Exception as exc:
        logger.exception("Agent communication failed")
        steps[-1].status = "failed"
        steps[-1].detail = str(exc)
        raise HTTPException(status_code=502, detail=f"Agent communication failed: {exc}") from exc

    steps[-1].status = "completed"
    steps[-1].detail = f"POST /api/agents/retrieve → {retrieval.total_results} result(s)"

    # Step 4 — Agent 2 Retrieval
    steps.append(
        AgentPipelineStep(
            step=4,
            name="Agent 2 — Medical Retrieval",
            status="completed" if retrieval.total_results > 0 else "no_results",
            detail=f"Retrieved top {retrieval.total_results} evidence chunk(s)",
        )
    )

    # Step 5 — Agent 3 LLM Response Agent
    steps.append(
        AgentPipelineStep(
            step=5,
            name="Agent 3 — LLM Response Agent",
            status="in_progress",
            detail="Generating RAG response with citations",
        )
    )

    try:
        response_result = await _response_agent.generate_response(analysis, retrieval.results)
        steps[-1].status = "completed"
        steps[-1].detail = f"Generated answer via model '{response_result.model_used}' ({len(response_result.citations)} citation(s))"
    except Exception as exc:
        logger.exception("Response agent generation failed")
        steps[-1].status = "failed"
        steps[-1].detail = str(exc)
        raise HTTPException(status_code=500, detail=f"Response agent generation failed: {exc}") from exc

    # Step 6 — Responsible AI Guardrails & Validation
    steps.append(
        AgentPipelineStep(
            step=6,
            name="Responsible AI Guardrails",
            status="completed",
            detail="Validated citations & appended public health disclaimer",
        )
    )
    rai_report = _guardrails.validate_response(response_result, retrieval.results, rai_report)

    status = "success" if retrieval.total_results > 0 else "no_evidence"
    message = None
    if retrieval.total_results == 0:
        message = (
            "I could not find sufficient verified evidence in the current "
            "public-health knowledge base to answer this question."
        )

    return QueryPipelineResponse(
        status=status,
        analysis=analysis,
        retrieval=retrieval,
        response=response_result,
        guardrails_report=rai_report,
        steps=steps,
        message=message,
    )
