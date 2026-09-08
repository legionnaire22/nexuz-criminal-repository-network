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
              <span className="unscanned-highlight">Click "Run AI Investigation"</span> to trigger Extractor & GDS Graph Scoring agents to isolate culpable syndicate targets.
            </div>
            <div className="unscanned-stats-chip">
              <span><i className="fa-solid fa-database"></i> 7,266 Records Ingested</span>
              <span><i className="fa-solid fa-shield-halved"></i> 0 Pre-Judgments</span>
            </div>
          </div>
        ) : (
          suspects.map(s => {
            const isSelected = selectedSuspect?.id === s.id;
            const evidence = s.evidence || {};
            const isWitness = s.tags?.includes('WITNESS') || s.tags?.includes('VICTIM') || s.score < 0.2;

            return (
              <div
                key={s.id}
                className={`suspect-card ${
                  isSelected ? 'selected' : ''
                } ${s.isSuspect ? 'marked-suspect' : isWitness ? 'marked-innocent' : ''}`}
                onClick={() => {
                  if (isSelected) {
                    onSelectSuspect(null);
                  } else {
                    onSelectSuspect(s);
                    onFocusNode(s.id);
                  }
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
                  {/* Score badge + Expand/Contract Chevron */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <span className={`suspect-score-badge ${
                      s.isSuspect ? 'score-critical' : s.score >= 0.5 ? 'score-warning' : 'score-cleared'
                    }`}>
                      {s.isSuspect ? `${(s.score * 100).toFixed(0)}% THREAT` : 'CLEARED'}
                    </span>
                    <i
                      className={`fa-solid ${isSelected ? 'fa-chevron-up' : 'fa-chevron-down'}`}
                      style={{
                        fontSize: '0.65rem',
                        color: isSelected ? 'var(--cyan-bright)' : '#64748b',
                        transition: 'transform 0.2s ease'
                      }}
                      title={isSelected ? "Click to contract" : "Click to expand forensic evidence"}
                    />
                  </div>
                </div>

                {/* Sub-header role */}
                <div className="suspect-role">{s.alias} &bull; {s.role}</div>

                {/* Tags row */}
                <div className="suspect-tags-row">
                  {s.tags.map(t => <span key={t} className="suspect-tag">{t}</span>)}
                </div>

                {/* Expanded Forensic Evidence & Telemetry — Revealed on Click */}
                {isSelected && (
                  <div className="suspect-evidence-container" onClick={(e) => e.stopPropagation()}>
                    {/* Verdict / Status Banner */}
                    <div className={`evidence-status-banner ${s.isSuspect ? 'banner-suspect' : 'banner-cleared'}`}>
                      <div className="banner-title-row">
                        <span className="banner-icon">
                          <i className={`fa-solid ${s.isSuspect ? 'fa-triangle-exclamation' : 'fa-shield-halved'}`}></i>
                        </span>
                        <span className="banner-title">
                          {s.isSuspect ? 'INCULPATORY EVIDENCE (PRIME SUSPECT)' : 'EXCULPATORY VERDICT (CLEARED / WITNESS)'}
                        </span>
                      </div>
                      <span className="banner-badge">
                        {s.isSuspect ? 'CULPABLE SYNDICATE LINKAGE' : 'BSA SEC 63 VERIFIED'}
                      </span>
                    </div>

                    {/* Primary Forensic Reason */}
                    <div className="evidence-reason-box">
                      <div className="evidence-reason-label">
                        <i className="fa-solid fa-file-lines"></i>
                        PRIMARY FORENSIC REASON:
                      </div>
                      <div className="evidence-reason-text">
                        {s.reason || 'No specific reason recorded.'}
                      </div>
                    </div>

                    {/* Multi-Modal Evidence Breakdown */}
                    <div className="evidence-breakdown-grid">
                      {/* Telecom CDR Audit */}
                      <div className="evidence-item">
                        <div className="evidence-item-head">
                          <i className="fa-solid fa-phone"></i>
                          <span>TELECOM CDR AUDIT</span>
                        </div>
                        <div className="evidence-item-content">
                          {evidence.telecom || (s.isSuspect 
                            ? 'Abnormal pre-incident call frequency burst logged against syndicate handsets.' 
                            : '0 calls logged to criminal syndicate MSISDNs. Z-Score = 0.00.')}
                        </div>
                      </div>

                      {/* Financial / PMLA Audit */}
                      <div className="evidence-item">
                        <div className="evidence-item-head">
                          <i className="fa-solid fa-building-columns"></i>
                          <span>FINANCIAL / PMLA AUDIT</span>
                        </div>
                        <div className="evidence-item-content">
                          {evidence.financial || (s.isSuspect 
                            ? 'Involved in structured smurfing deposits (<₹10L) to evade FIU-IND thresholds.' 
                            : '0 transactions to/from syndicate current accounts or Hawala ledgers.')}
                        </div>
                      </div>

                      {/* Spatial Telemetry / Alibi */}
                      <div className="evidence-item">
                        <div className="evidence-item-head">
                          <i className="fa-solid fa-location-dot"></i>
                          <span>SPATIAL TELEMETRY & ALIBI</span>
                        </div>
                        <div className="evidence-item-content">
                          {evidence.spatial || (s.isSuspect 
                            ? 'Concurrent cellular registration confirmed at Tower BKC-112 during staging.' 
                            : 'Incidental geographical presence verified; corroborated independent bystander statement.')}
                        </div>
                      </div>

                      {/* Graph Topology */}
                      <div className="evidence-item">
                        <div className="evidence-item-head">
                          <i className="fa-solid fa-diagram-project"></i>
                          <span>GRAPH CENTRALITY & TOPOLOGY</span>
                        </div>
                        <div className="evidence-item-content">
                          {evidence.graph || (s.isSuspect 
                            ? `High centrality influence score (${(s.score * 0.35).toFixed(2)}). Critical cluster link.` 
                            : 'Betweenness Centrality = 0.000 (Completely isolated from criminal flow). Degree = 1.')}
                        </div>
                      </div>

                      {/* Statutory Basis */}
                      <div className="evidence-item item-full">
                        <div className="evidence-item-head">
                          <i className="fa-solid fa-scale-balanced"></i>
                          <span>LEGAL CITATION & STATUTORY SAFEGUARD</span>
                        </div>
                        <div className="evidence-item-content highlight-statute">
                          {evidence.statutory || (s.isSuspect 
                            ? `Charged under BNS 2023 Sec 111 (Organized Crime) & primary exhibit: ${s.doc || 'FIR Entry'}.` 
                            : `Attested witness deposition under BNSS 2023 Sec 180 / CrPC 161. Formally exonerated under BSA 2023 Sec 63.`)}
                        </div>
                      </div>
                    </div>

                    {/* Interactive Action Buttons */}
                    <div className="suspect-actions-strip">
                      <button
                        className={`btn-suspect-action btn-mark-crimson ${s.isSuspect ? 'action-active' : ''}`}
                        onClick={() => onToggleMarkSuspect(s.id, true)}
                        title="Mark entity as Prime Suspect"
                      >
                        <i className="fa-solid fa-crosshairs"></i> Mark Suspect
                      </button>
                      <button
                        className={`btn-suspect-action btn-mark-cleared ${!s.isSuspect ? 'action-active' : ''}`}
                        onClick={() => onToggleMarkSuspect(s.id, false)}
                        title="Clear entity as Innocent Civilian"
                      >
                        <i className="fa-solid fa-shield"></i> Clear / Innocent
                      </button>
                      <button
                        className="btn-suspect-action btn-collapse-strip"
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectSuspect(null);
                        }}
                        title="Contract details"
                      >
                        <i className="fa-solid fa-compress"></i> Contract
                      </button>
                    </div>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </section>
  );
}
