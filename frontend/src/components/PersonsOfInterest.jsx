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
          <i className="fa-solid fa-user-secret" style={{ color: 'var(--amber-warn)' }}></i>
          PERSONS OF INTEREST
        </div>
        <span className="panel-badge">
          {isAnalyzed ? `${suspects.length} Targets • 26 False Positives Rejected` : `${suspects.length} Candidates`}
        </span>
      </div>

      <div className="suspects-scroll">
        {suspects.map(s => {
          const isSelected = selectedSuspect?.id === s.id;
          return (
            <div
              key={s.id}
              className={`suspect-card ${
                isSelected ? 'selected' : ''
              } ${isAnalyzed ? (s.isSuspect ? 'marked-suspect' : s.score < 0.1 ? 'marked-innocent' : '') : ''}`}
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
                      background: !isAnalyzed 
                        ? '#64748b' 
                        : s.score >= 0.85
                          ? 'var(--crimson-target)'
                          : s.score >= 0.5
                            ? 'var(--amber-warn)'
                            : 'var(--emerald-radar)'
                    }}
                  />
                  <span className="suspect-identity">{s.name}</span>
                </div>
                {/* Score badge only on selected */}
                {isSelected && (
                  isAnalyzed ? (
                    <span className={`suspect-score-badge ${
                      s.score >= 0.85 ? 'score-critical' : s.score >= 0.5 ? 'score-warning' : 'score-cleared'
                    }`}>
                      {(s.score * 100).toFixed(0)}% THREAT
                    </span>
                  ) : (
                    <span className="suspect-score-badge score-pending">
                      PENDING SCAN
                    </span>
                  )
                )}
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
        })}
      </div>
    </section>
  );
}
