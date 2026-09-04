import React from 'react';

export function PersonsOfInterest({
  suspects,
  selectedSuspect,
  onSelectSuspect,
  onToggleMarkSuspect,
  onFocusNode,
  isAnalyzed = false
}) {
  return (
    <section className="tactical-panel">
      <div className="panel-head">
        <div className="panel-head-title">
          <i className="fa-solid fa-user-secret" style={{ color: isAnalyzed ? 'var(--amber-warn)' : '#64748b' }}></i>
          PERSONS OF INTEREST
        </div>
        <span className="panel-badge">
          {isAnalyzed ? `${suspects.filter(s => s.isSuspect).length} Targets Isolated` : 'Awaiting Pipeline Scan'}
        </span>
      </div>

      <div className="suspects-scroll">
        {!isAnalyzed ? (
          <div className="unscanned-persons-placeholder">
            <div className="unscanned-icon-wrap">
              <i className="fa-solid fa-satellite-dish"></i>
            </div>
            <div className="unscanned-title">RAW UNCLASSIFIED INGESTION</div>
            <div className="unscanned-desc">
              Incoming CDR, FIR & Banking transactions are currently unclassified. 
              <br />
              <span className="unscanned-highlight">Click "Run AI Investigation"</span> to trigger Extractor & GNN Scoring agents to isolate culpable syndicate targets.
            </div>
            <div className="unscanned-stats-chip">
              <span><i className="fa-solid fa-database"></i> 7,266 Records Ingested</span>
              <span><i className="fa-solid fa-shield-halved"></i> 0 Pre-Judgments</span>
            </div>
          </div>
        ) : (
          suspects.map(s => {
            const isSelected = selectedSuspect?.id === s.id;
            return (
              <div
                key={s.id}
                className={`suspect-card ${
                  isSelected ? 'selected' : ''
                } ${s.isSuspect ? 'marked-suspect' : s.score < 0.1 ? 'marked-innocent' : ''}`}
                onClick={() => {
                  onSelectSuspect(s);
                  onFocusNode(s.id);
                }}
              >
                {/* Always visible: threat dot + name */}
                <div className="suspect-row-top">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '7px' }}>
                    <span
                      className="suspect-threat-dot"
                      style={{
                        background: s.isSuspect
                          ? 'var(--crimson-target)'
                          : s.score >= 0.5
                            ? 'var(--amber-warn)'
                            : 'var(--emerald-radar)'
                      }}
                    />
                    <span className="suspect-identity">{s.name}</span>
                  </div>
                  {/* Score badge */}
                  <span className={`suspect-score-badge ${
                    s.isSuspect ? 'score-critical' : s.score >= 0.5 ? 'score-warning' : 'score-cleared'
                  }`}>
                    {s.isSuspect ? `${(s.score * 100).toFixed(0)}% THREAT` : 'CLEARED'}
                  </span>
                </div>

                {/* Expanded details — only when selected */}
                {isSelected && (
                  <>
                    <div className="suspect-role">{s.alias} &bull; {s.role}</div>

                    <div className="suspect-tags-row">
                      {s.tags.map(t => <span key={t} className="suspect-tag">{t}</span>)}
                    </div>

                    <div className="suspect-actions-strip" onClick={(e) => e.stopPropagation()}>
                      <button
                        className="btn-suspect-action btn-mark-crimson"
                        onClick={() => onToggleMarkSuspect(s.id, true)}
                        title="Mark entity as Prime Suspect"
                      >
                        <i className="fa-solid fa-crosshairs"></i> Mark Suspect
                      </button>
                      <button
                        className="btn-suspect-action btn-mark-cleared"
                        onClick={() => onToggleMarkSuspect(s.id, false)}
                        title="Clear entity as Innocent Civilian"
                      >
                        <i className="fa-solid fa-shield"></i> Clear / Innocent
                      </button>
                    </div>
                  </>
                )}
              </div>
            );
          })
        )}
      </div>
    </section>
  );
}
