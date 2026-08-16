import React, { useState } from "react";
import EvidenceDrawer from "../components/EvidenceDrawer.jsx";
import PipelineVisualizer from "../components/PipelineVisualizer.jsx";
import SafetyAlerts from "../components/SafetyAlerts.jsx";
import { processQuery } from "../services/api.js";

const PRESET_QUERIES = [
  {
    label: "🦟 Dengue Symptoms",
    query: "What are the main symptoms of dengue fever?",
    desc: "Evidence-grounded retrieval + citations",
  },
  {
    label: "🛡️ Dengue Prevention",
    query: "What preventive measures can reduce dengue transmission?",
    desc: "Prevention intent classification",
  },
  {
    label: "🦟 Malaria Transmission",
    query: "How is malaria transmitted to humans?",
    desc: "Transmission intent & WHO evidence",
  },
  {
    label: "⛔ Dosage Refusal Test",
    query: "What is the exact dosage of paracetamol for a 5-year-old child?",
    desc: "High risk refusal (Responsible AI)",
  },
  {
    label: "🔒 PII Redaction Test",
    query: "My name is John Doe, phone 555-0199, what are dengue symptoms?",
    desc: "Sanitizes PII before query processing",
  },
  {
    label: "❓ Out-of-KB Test",
    query: "What are the latest treatments for rare disease X123?",
    desc: "Graceful 'insufficient evidence' fallback",
  },
];

export default function Dashboard() {
  const [queryInput, setQueryInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState("response");

  const handleSubmit = async (e, customQuery) => {
    if (e) e.preventDefault();
    const q = customQuery || queryInput;
    if (!q || !q.trim()) return;

    setLoading(true);
    setError(null);
    if (customQuery) setQueryInput(customQuery);

    try {
      const data = await processQuery(q);
      setResult(data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || err.message || "Query processing failed");
    } finally {
      setLoading(false);
    }
  };

  const renderFormattedAnswer = (text) => {
    if (!text) return null;

    // Highlight citation tags like [Doc: Title, Page: 1]
    const citationRegex = /\[Doc:\s*([^,\]]+),\s*Page:\s*(\d+)\]/g;
    const parts = [];
    let lastIndex = 0;
    let match;

    while ((match = citationRegex.exec(text)) !== null) {
      if (match.index > lastIndex) {
        parts.push(text.substring(lastIndex, match.index));
      }
      const title = match[1];
      const page = match[2];
      parts.push(
        <span key={match.index} className="inline-citation-badge" title={`Source Document: ${title}`}>
          🔖 {title} (p. {page})
        </span>
      );
      lastIndex = citationRegex.lastIndex;
    }

    if (lastIndex < text.length) {
      parts.push(text.substring(lastIndex));
    }

    return parts;
  };

  return (
    <main className="dashboard-layout">
      {/* Sidebar: Presets & Info */}
      <aside className="dashboard-sidebar">
        <div className="sidebar-section">
          <h3>⚡ Demo Evaluation Queries</h3>
          <p className="sidebar-sub">Click a preset test query to trigger the multi-agent pipeline:</p>
          <div className="preset-buttons-list">
            {PRESET_QUERIES.map((p, idx) => (
              <button
                key={idx}
                className="preset-btn"
                onClick={() => handleSubmit(null, p.query)}
                disabled={loading}
              >
                <div className="preset-label">{p.label}</div>
                <div className="preset-desc">{p.desc}</div>
              </button>
            ))}
          </div>
        </div>

        <div className="sidebar-section system-info-box">
          <h4>💡 System Capabilities</h4>
          <ul>
            <li>✨ <strong>Agent 1:</strong> Medical NER & Risk Analysis</li>
            <li>🌐 <strong>Agent REST:</strong> HTTP Inter-Agent Protocol</li>
            <li>📚 <strong>Agent 2:</strong> Vector Store Retrieval</li>
            <li>🤖 <strong>Agent 3:</strong> LLM Evidence Synthesis</li>
            <li>🛡️ <strong>Guardrails:</strong> PII Redaction & Refusal Logic</li>
          </ul>
        </div>
      </aside>

      {/* Main Content Area */}
      <section className="dashboard-main">
        <div className="query-input-card">
          <h2>Evidence-Grounded Public Health Assistant</h2>
          <p className="lead-text">
            Ask any public health question regarding disease symptoms, prevention, or transmission.
          </p>

          <form onSubmit={(e) => handleSubmit(e, null)} className="query-form">
            <div className="input-group">
              <input
                type="text"
                className="query-input"
                placeholder="e.g. What are the symptoms of dengue fever?"
                value={queryInput}
                onChange={(e) => setQueryInput(e.target.value)}
                disabled={loading}
              />
              <button type="submit" className="btn-submit" disabled={loading || !queryInput.trim()}>
                {loading ? <span className="spinner">⏳ Processing…</span> : <span>Search 🔍</span>}
              </button>
            </div>
          </form>

          {error && <div className="error-banner">❌ {error}</div>}
        </div>

        {/* Results Container */}
        {result && (
          <div className="results-container">
            {/* Navigation Tabs for Result Views */}
            <div className="result-nav-tabs">
              <button
                className={`nav-tab ${activeTab === "response" ? "active" : ""}`}
                onClick={() => setActiveTab("response")}
              >
                💬 Grounded Answer
              </button>
              <button
                className={`nav-tab ${activeTab === "pipeline" ? "active" : ""}`}
                onClick={() => setActiveTab("pipeline")}
              >
                ⛓️ Agent Flow ({result.steps?.length || 0})
              </button>
              <button
                className={`nav-tab ${activeTab === "evidence" ? "active" : ""}`}
                onClick={() => setActiveTab("evidence")}
              >
                📚 Source Evidence ({result.retrieval?.total_results || 0})
              </button>
              <button
                className={`nav-tab ${activeTab === "safety" ? "active" : ""}`}
                onClick={() => setActiveTab("safety")}
              >
                🛡️ Responsible AI Status
              </button>
            </div>

            {/* TAB 1: Grounded Answer View */}
            {activeTab === "response" && (
              <div className="tab-pane response-pane">
                {result.status === "blocked" ? (
                  <div className="refusal-card">
                    <div className="refusal-icon">🚫</div>
                    <h3>Medical Advisory & Refusal</h3>
                    <p className="refusal-msg">{result.message}</p>
                    <div className="refusal-note">
                      <strong>Responsible AI Rule:</strong> The assistant refuses personalized medical
                      diagnoses or dosage prescriptions to prioritize user health and safety.
                    </div>
                  </div>
                ) : (
                  <div className="response-card">
                    <div className="response-header">
                      <h3>💡 Evidence-Grounded Answer</h3>
                      {result.response?.model_used && (
                        <span className="model-tag">Model: {result.response.model_used}</span>
                      )}
                    </div>

                    <div className="response-body">
                      {result.response?.answer ? (
                        <div className="formatted-text">
                          {renderFormattedAnswer(result.response.answer)}
                        </div>
                      ) : (
                        <p className="no-ans-text">{result.message || "No answer generated."}</p>
                      )}
                    </div>

                    {result.response?.citations && result.response.citations.length > 0 && (
                      <div className="citations-footer">
                        <h4>📌 Grounding Sources & Citations ({result.response.citations.length})</h4>
                        <div className="citations-grid">
                          {result.response.citations.map((c, i) => (
                            <div key={i} className="citation-item">
                              <span className="cite-num">[{i + 1}]</span>
                              <div className="cite-details">
                                <span className="cite-title">{c.doc_title}</span>
                                <span className="cite-meta">
                                  {c.source} | Page {c.page || 1}
                                </span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* Compact Pipeline Summary underneath response */}
                <PipelineVisualizer
                  steps={result.steps}
                  analysis={result.analysis}
                  responseModel={result.response?.model_used}
                />
              </div>
            )}

            {/* TAB 2: Agent Flow Visualizer */}
            {activeTab === "pipeline" && (
              <div className="tab-pane">
                <PipelineVisualizer
                  steps={result.steps}
                  analysis={result.analysis}
                  responseModel={result.response?.model_used}
                />
              </div>
            )}

            {/* TAB 3: Evidence Drawer */}
            {activeTab === "evidence" && (
              <div className="tab-pane">
                <EvidenceDrawer retrievalResults={result.retrieval?.results} />
              </div>
            )}

            {/* TAB 4: Responsible AI */}
            {activeTab === "safety" && (
              <div className="tab-pane">
                <SafetyAlerts report={result.guardrails_report} analysis={result.analysis} />
              </div>
            )}
          </div>
        )}
      </section>
    </main>
  );
}
