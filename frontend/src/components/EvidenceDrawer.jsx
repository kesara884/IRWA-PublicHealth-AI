import React, { useState } from "react";

export default function EvidenceDrawer({ retrievalResults, onSelectChunk }) {
  const [filterDisease, setFilterDisease] = useState("ALL");

  if (!retrievalResults || retrievalResults.length === 0) {
    return (
      <div className="evidence-panel empty-panel">
        <h4>📚 Verified Evidence Sources</h4>
        <p className="muted-text">
          No document chunks retrieved for this query. Run a public health question to inspect grounding evidence.
        </p>
      </div>
    );
  }

  const diseases = ["ALL", ...new Set(retrievalResults.map((r) => r.disease || "General"))];
  const filtered =
    filterDisease === "ALL"
      ? retrievalResults
      : retrievalResults.filter((r) => (r.disease || "General") === filterDisease);

  return (
    <div className="evidence-panel">
      <div className="evidence-panel-header">
        <div className="title-area">
          <h4>📚 Verified Source Evidence ({retrievalResults.length})</h4>
          <span className="subtitle">Grounding documents from vector database</span>
        </div>

        {diseases.length > 2 && (
          <div className="disease-filter-tabs">
            {diseases.map((d) => (
              <button
                key={d}
                className={`filter-tab ${filterDisease === d ? "active" : ""}`}
                onClick={() => setFilterDisease(d)}
              >
                {d}
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="evidence-chunks-list">
        {filtered.map((res, idx) => {
          const scorePercent = Math.min(100, Math.round((res.score || 0) * 100));
          return (
            <div
              key={res.chunk_id || idx}
              className="evidence-chunk-card"
              onClick={() => onSelectChunk && onSelectChunk(res)}
            >
              <div className="chunk-card-top">
                <span className="doc-title-badge">📄 {res.title}</span>
                <span className="doc-page-tag">Page {res.page || 1}</span>
              </div>

              <div className="chunk-meta-row">
                <span className="meta-source">Source: <strong>{res.source}</strong></span>
                <span className="meta-disease">Topic: <strong>{res.disease}</strong></span>
              </div>

              <div className="similarity-bar-container">
                <div className="similarity-label">
                  <span>Relevance Score</span>
                  <span>{scorePercent}%</span>
                </div>
                <div className="similarity-track">
                  <div
                    className="similarity-fill"
                    style={{ width: `${scorePercent}%` }}
                  ></div>
                </div>
              </div>

              <p className="chunk-snippet-text">{res.text}</p>

              {res.url && (
                <a
                  href={res.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="source-link"
                  onClick={(e) => e.stopPropagation()}
                >
                  🔗 Source Link
                </a>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
