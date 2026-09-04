import React from 'react';
import { CASE_METADATA } from '../data/cases';

export function Header({
  currentCase,
  onSwitchCase,
  queryLatency,
  isAnalyzed,
  onOpenReviewModal,
  onOpenCourtModal
}) {
  const meta = CASE_METADATA[currentCase] || {};
  const fpCount = meta.fpRejected || 26;

  return (
    <header className="command-header">
      <div className="brand-cluster">
        <div className="brand-logo-badge">
          <i className="fa-solid fa-shield-halved"></i> NEXUS
        </div>
        <div className="brand-meta">
          <span className="brand-title">Criminal Network Analysis</span>
          <span className="brand-sub">NEXUS v2.0 &bull; SIH 2026</span>
        </div>
      </div>

      {/* Live Telemetry Cluster: Query Latency + FP Pruned + Zero False Accusations */}
      <div className="telemetry-cluster">
        <div className="telemetry-item">
          <span className="telemetry-label">Supervisor Query</span>
          <span className="telemetry-num" style={{ color: 'var(--amber-warn)' }}>{queryLatency} ms</span>
        </div>

        <div className="telemetry-item">
          <span className="telemetry-label">False Positives Rejected</span>
          <span className="telemetry-num" style={{ color: 'var(--emerald-radar)' }}>
            {isAnalyzed ? `${fpCount} REJECTED` : 'SCANNING NOISE'}
          </span>
        </div>

        <div className="telemetry-item">
          <span className="telemetry-label">False Accusations</span>
          <span className="telemetry-num" style={{ color: 'var(--cyan-bright)' }}>0 (BSA SEC 63)</span>
        </div>
      </div>

      {/* Case Selector & Quick Actions */}
      <div className="header-actions">
        <select
          className="case-selector-btn"
          value={currentCase}
          onChange={(e) => onSwitchCase(e.target.value)}
        >
          <option value="sandstorm">Operation Sandstorm (Narcotics)</option>
          <option value="phantom">Operation Phantom (Hawala Bridge)</option>
          <option value="mirage">Operation Mirage (SIM-Swap Fraud)</option>
        </select>

        <button
          className="btn-tactical-header"
          style={{ background: 'rgba(168, 85, 247, 0.22)', borderColor: 'var(--purple-supervisor)', color: '#d8b4fe' }}
          onClick={onOpenReviewModal}
          title="Open Section 63 BNSS Human-in-the-Loop Review Queue"
        >
          <i className="fa-solid fa-users-gear"></i> HITL Review Queue
        </button>

        <button
          className="btn-tactical-header btn-court-dossier"
          onClick={onOpenCourtModal}
          title="Export Court-Admissible Intelligence Dossier under BNSS Sec 63/65B"
        >
          <i className="fa-solid fa-gavel"></i> Court Dossier
        </button>
      </div>
    </header>
  );
}
