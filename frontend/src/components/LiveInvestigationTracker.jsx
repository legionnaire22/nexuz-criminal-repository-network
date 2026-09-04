import React from 'react';

export function LiveInvestigationTracker({
  currentPhase,
  hypothesisStatus,
  formationProgress,
  processingRate,
  isRunning,
  isAnalyzed
}) {
  const steps = [
    { num: 1, label: "Ingest & Probe", desc: "Noise Filtering" },
    { num: 2, label: "Anomaly Lock", desc: "Heuristic Rules" },
    { num: 3, label: "GNN Scoring", desc: "Syndicate Emergence" },
    { num: 4, label: "Consensus", desc: "Multi-Agent Deliberation" }
  ];

  const getPhaseBadge = () => {
    if (isRunning) {
      if (currentPhase === 1) return { text: "PHASE 1: PROBING SIGNALS", cls: "phase-badge-probe" };
      if (currentPhase === 2) return { text: "PHASE 2: ANOMALY MATCHING", cls: "phase-badge-anomaly" };
      if (currentPhase === 3) return { text: "PHASE 3: GNN RISK SCORING", cls: "phase-badge-gnn" };
      if (currentPhase === 4) return { text: "PHASE 4: AGENT CONSENSUS", cls: "phase-badge-consensus" };
      return { text: "INVESTIGATING...", cls: "phase-badge-probe" };
    }
    if (isAnalyzed) {
      return { text: "INVESTIGATION COMPLETE", cls: "phase-badge-complete" };
    }
    return { text: "STANDBY • RAW INGESTION", cls: "phase-badge-standby" };
  };

  const badge = getPhaseBadge();

  return (
    <section className="tactical-panel live-tracker-panel">
      <div className="panel-head">
        <div className="panel-head-title">
          <div className={`tracker-radar-dot ${isRunning ? 'active' : ''}`}></div>
          INVESTIGATION PIPELINE
        </div>
        <span className={`phase-status-pill ${badge.cls}`}>
          {badge.text}
        </span>
      </div>

      <div className="tracker-body">
        {/* Step Progression Grid */}
        <div className="tracker-steps-grid">
          {steps.map((s) => {
            const isCompleted = isAnalyzed || (isRunning && currentPhase > s.num);
            const isActive = isRunning && currentPhase === s.num;
            return (
              <div 
                key={s.num} 
                className={`tracker-step-item ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}
              >
                <div className="step-num-bubble">
                  {isCompleted ? <i className="fa-solid fa-check"></i> : s.num}
                </div>
                <div className="step-labels">
                  <span className="step-title">{s.label}</span>
                  <span className="step-desc">{s.desc}</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Progress Bar */}
        <div className="tracker-progress-wrap">
          <div className="tracker-progress-track">
            <div 
              className="tracker-progress-fill" 
              style={{ width: `${isAnalyzed ? 100 : formationProgress}%` }}
            ></div>
          </div>
          <div className="tracker-telemetry-row">
            <span>
              <i className="fa-solid fa-bolt" style={{ color: 'var(--cyan-bright)' }}></i>
              {isRunning ? `${processingRate.toLocaleString()} ev/s` : '7,266 Signals Mapped'}
            </span>
            <span style={{ color: isAnalyzed ? 'var(--emerald-radar)' : 'var(--cyan-bright)' }}>
              {isAnalyzed ? '100% Corroborated' : `${formationProgress}% Complete`}
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}
