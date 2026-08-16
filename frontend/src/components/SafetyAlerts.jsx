import React from "react";

export default function SafetyAlerts({ report, analysis }) {
  if (!report && !analysis) return null;

  return (
    <div className="safety-alerts-card">
      <div className="safety-card-header">
        <h4>🛡️ Responsible AI Guardrails & Compliance</h4>
        <span className={`safety-status-badge ${report?.safety_passed ? "pass" : "alert"}`}>
          {report?.safety_passed ? "Safety Approved" : "Refusal Triggered"}
        </span>
      </div>

      <div className="safety-grid">
        <div className="safety-stat-box">
          <span className="stat-label">PII Redaction</span>
          <span className={`stat-value ${analysis?.pii_detected ? "warn" : "good"}`}>
            {analysis?.pii_detected ? "⚠️ PII Masked" : "✅ Clean Input"}
          </span>
        </div>

        <div className="safety-stat-box">
          <span className="stat-label">Citation Grounding</span>
          <span
            className={`stat-value ${
              report?.citation_validation_passed !== false ? "good" : "warn"
            }`}
          >
            {report?.citation_validation_passed !== false ? "✅ 100% Grounded" : "⚠️ Check Citations"}
          </span>
        </div>

        <div className="safety-stat-box">
          <span className="stat-label">Risk Rating</span>
          <span
            className={`stat-value risk-${(analysis?.risk_level || "low").toLowerCase()}`}
          >
            {analysis?.risk_level || "LOW"}
          </span>
        </div>

        <div className="safety-stat-box">
          <span className="stat-label">Refusal Logic</span>
          <span className={`stat-value ${report?.refusal_triggered ? "warn" : "good"}`}>
            {report?.refusal_triggered ? "⛔ Refused (Unsafe)" : "✅ Clear to Respond"}
          </span>
        </div>
      </div>

      {report?.warnings && report.warnings.length > 0 && (
        <div className="safety-warnings-box">
          <h5>Compliance Log & Warnings:</h5>
          <ul>
            {report.warnings.map((w, idx) => (
              <li key={idx}>⚠️ {w}</li>
            ))}
          </ul>
        </div>
      )}

      {report?.disclaimer && (
        <div className="disclaimer-callout">
          <span className="icon">⚕️</span>
          <p className="disclaimer-text">{report.disclaimer}</p>
        </div>
      )}
    </div>
  );
}
