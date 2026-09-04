import React from 'react';

export function EvidenceBrief({
  nlQuery,
  onQueryChange,
  onExecuteQuery,
  currentCase,
  briefSummary,
  briefFindings,
  onFocusNode
}) {
  const getPlaceholder = () => {
    if (currentCase === 'phantom') return "e.g. how is vikram sinha related to rohit jain...";
    if (currentCase === 'mirage') return "e.g. how is imran khan related to prakash desai...";
    return "e.g. how is arjun mehta related to deepak rao...";
  };

  return (
    <>
      <div className="nl-query-box">
        <input 
          type="text" 
          className="nl-input" 
          placeholder={getPlaceholder()} 
          value={nlQuery}
          onChange={(e) => onQueryChange(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && onExecuteQuery(nlQuery)}
        />
        <button className="btn-nl-run" onClick={() => onExecuteQuery(nlQuery)}>
          <i className="fa-solid fa-magnifying-glass"></i> Ask
        </button>
      </div>

      <div className="evidence-brief-card">
        <div className="evidence-brief-head">
          <span>GROUNDED SUPERVISOR DOSSIER</span>
          <span>CONFIDENCE: 96.0%</span>
        </div>
        <div className="evidence-brief-body">
          {briefSummary}
        </div>

        <div style={{ fontSize: '0.66rem', fontFamily: 'var(--font-mono)', color: 'var(--text-dim)', marginBottom: '6px' }}>
          VERIFIED CITATIONS (CLICK TO LOCATE ON CANVAS):
        </div>
        <div>
          {briefFindings.map((f, idx) => (
            <div key={idx} style={{ marginBottom: '8px', fontSize: '0.7rem', color: '#cbd5e1' }}>
              <div>&bull; {f.text}</div>
              <div style={{ marginTop: '3px' }}>
                {f.nodes.map(n => (
                  <span 
                    key={n} 
                    className="citation-pill"
                    onClick={() => onFocusNode(n)}
                    title="Click to center on canvas"
                  >
                    <i className="fa-solid fa-location-crosshairs"></i> {n}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
