import React from 'react';

export function AnomalyTicker({ alerts }) {
  return (
    <div className="right-anomaly-box">
      <div className="right-anomaly-head">
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span className={`anomaly-pulse-dot ${alerts.length > 0 ? 'active' : ''}`}></span>
          <span className="right-anomaly-title">LIVE ANOMALY RADAR</span>
        </div>
        <span className={`panel-badge ${alerts.length > 0 ? 'badge-detected' : ''}`}>
          {alerts.length > 0 ? `${alerts.length} Detected` : 'Standby'}
        </span>
      </div>

      <div className="right-anomaly-list">
        {alerts.length === 0 ? (
          <div className="anomaly-standby-placeholder">
            <div className="radar-sweep-icon">
              <i className="fa-solid fa-radar fa-spin"></i>
            </div>
            <div className="standby-title">RADAR IN STANDBY</div>
            <div className="standby-desc">
              Multi-layer anomaly detectors are idling.
              <br />
              <span style={{ color: 'var(--cyan-bright)' }}>Click "Run AI Investigation"</span> to detect Smurfing, CDR Bursts & Hawala Bridges.
            </div>
          </div>
        ) : (
          alerts.map((a, idx) => (
            <div 
              key={a.id} 
              className={`right-anomaly-item ${a.severity === 'CRITICAL' ? 'anomaly-critical' : 'anomaly-warn'} anomaly-slide-in`}
              style={{ animationDelay: `${idx * 0.1}s` }}
              title="Click to view full anomaly forensics"
            >
              <div className="anomaly-item-top">
                <span className="anomaly-code">[{a.id}]</span>
                <span className={`anomaly-sev-tag ${a.severity === 'CRITICAL' ? 'sev-crit' : 'sev-high'}`}>
                  {a.severity}
                </span>
              </div>
              <div className="anomaly-item-title">{a.title}</div>
              <div className="anomaly-item-detail">{a.detail}</div>
              <div className="anomaly-item-layer">
                <i className="fa-solid fa-layer-group"></i> {a.layer}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
