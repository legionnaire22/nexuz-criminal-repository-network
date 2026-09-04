import React from 'react';

export function AgentDebate({
  debateTopic,
  consensusScore,
  debates,
  onTopicChange
}) {
  return (
    <>
      {/* Live Consensus & Topic Status Bar */}
      <div className="debate-showdown-bar">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.62rem', color: 'var(--text-dim)' }}>
            DISPUTE TOPIC:
          </span>
          <select 
            className="debate-topic-select" 
            value={debateTopic}
            onChange={(e) => onTopicChange(e.target.value)}
          >
            <option value="alias">Alias Merging vs False Accusation</option>
            <option value="role">Structural Hub vs Unwitting Conduit</option>
          </select>
        </div>

        <div className="debate-trigger-row" style={{ justifyContent: 'space-between' }}>
          <div className="consensus-meter-wrap" style={{ width: '100%' }}>
            <span>Consensus:</span>
            <div className="consensus-bar-track" style={{ flex: 1 }}>
              <div className="consensus-bar-fill" style={{ width: `${consensusScore}%` }}></div>
            </div>
            <span style={{ color: consensusScore > 80 ? 'var(--emerald-radar)' : consensusScore > 50 ? 'var(--amber-warn)' : '#94a3b8', fontWeight: 'bold' }}>
              {consensusScore}%
            </span>
          </div>
        </div>
      </div>

      {/* Streaming Agent Speeches or Idle State */}
      {debates.length === 0 ? (
        <div className="debate-empty-state">
          <div className="radar-idle-ring">
            <i className="fa-solid fa-users-viewfinder" style={{ fontSize: '1.4rem', color: '#64748b' }}></i>
          </div>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.72rem', color: '#94a3b8', marginTop: '12px' }}>
            AGENT CONSENSUS PIPELINE IDLE
          </div>
          <p style={{ fontSize: '0.65rem', color: 'var(--text-dim)', textAlign: 'center', maxWidth: '260px', marginTop: '6px', lineHeight: '1.4' }}>
            Click <strong>"Run AI Investigation"</strong> in the graph toolbar or <strong>"Run Debate"</strong> above to stream agent deliberation.
          </p>
        </div>
      ) : (
        debates.map((d, i) => (
          <div key={i} className={`debate-item debate-${d.color}`}>
            <div className="debate-agent-title">
              <span style={{ 
                color: d.color === 'extractor' ? 'var(--cyan-bright)' : 
                       d.color === 'resolver' ? 'var(--amber-warn)' : 
                       d.color === 'analyst' ? 'var(--crimson-target)' : 'var(--purple-supervisor)' 
              }}>
                AGENT: {d.agent.toUpperCase()}
              </span>
              <span style={{ color: 'var(--text-dim)' }}>{d.time}</span>
            </div>
            <div className="debate-text">{d.text}</div>
          </div>
        ))
      )}
    </>
  );
}
