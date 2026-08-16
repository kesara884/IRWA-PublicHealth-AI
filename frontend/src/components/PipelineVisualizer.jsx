import React from "react";

export default function PipelineVisualizer({ steps, analysis, responseModel }) {
  if (!steps || steps.length === 0) return null;

  const getStepIcon = (stepNum, status) => {
    if (status === "skipped") return "⏭️";
    if (status === "failed") return "❌";
    if (status === "blocked") return "🚫";
    if (status === "no_results") return "⚠️";
    switch (stepNum) {
      case 1:
        return "📥";
      case 2:
        return "🔍";
      case 3:
        return "🌐";
      case 4:
        return "📚";
      case 5:
        return "🤖";
      case 6:
        return "🛡️";
      default:
        return "⚙️";
    }
  };

  return (
    <div className="pipeline-card">
      <div className="pipeline-header">
        <h3 className="pipeline-title">
          <span className="icon">⛓️</span> Agent Execution Pipeline & Protocol Flow
        </h3>
        <span className="pipeline-badge">{steps.length} Steps Executed</span>
      </div>

      <div className="pipeline-steps-grid">
        {steps.map((s) => (
          <div
            key={s.step}
            className={`step-box step-status-${s.status} ${
              s.status === "in_progress" ? "step-pulse" : ""
            }`}
          >
            <div className="step-top">
              <span className="step-number">Step {s.step}</span>
              <span className={`status-pill pill-${s.status}`}>{s.status}</span>
            </div>
            <div className="step-main">
              <span className="step-icon">{getStepIcon(s.step, s.status)}</span>
              <span className="step-name">{s.name}</span>
            </div>
            {s.detail && <p className="step-detail">{s.detail}</p>}
          </div>
        ))}
      </div>

      {analysis && (
        <div className="pipeline-analysis-bar">
          <div className="analysis-item">
            <span className="label">Detected Intent:</span>
            <span className="val intent-tag">{analysis.intent}</span>
          </div>
          <div className="analysis-item">
            <span className="label">Risk Level:</span>
            <span className={`val risk-tag risk-${analysis.risk_level.toLowerCase()}`}>
              {analysis.risk_level}
            </span>
          </div>
          <div className="analysis-item">
            <span className="label">Medical NER Entities:</span>
            <span className="val entity-tag">
              {analysis.entities.disease.length > 0
                ? analysis.entities.disease.join(", ")
                : "General Health"}
            </span>
          </div>
          <div className="analysis-item">
            <span className="label">PII Status:</span>
            <span className={`val pii-tag ${analysis.pii_detected ? "pii-alert" : "pii-clean"}`}>
              {analysis.pii_detected ? "REDACTED" : "CLEAN"}
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
