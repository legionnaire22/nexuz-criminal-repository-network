import React from 'react';

export function AnomalyTicker({ alerts }) {
  return (
    <div className="right-anomaly-box">
      <div className="right-anomaly-head">
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span className="anomaly-pulse-dot"></span>
          <span className="right-anomaly-title">LIVE ANOMALY RADAR</span>
        </div>
        <span className="panel-badge">{alerts.length} Detected</span>
      </div>

      <div className="right-anomaly-list">
        {alerts.map(a => (
          <div 
            key={a.id} 
            className={`right-anomaly-item ${a.severity === 'CRITICAL' ? 'anomaly-critical' : 'anomaly-warn'}`}
            onClick={() => alert(`[${a.id}] ${a.title}\nLayer: ${a.layer}\nSeverity: ${a.severity}\n\n${a.detail}`)}
            title="Click to view full anomaly details"
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
        ))}
      </div>
    </div>
  );
}
