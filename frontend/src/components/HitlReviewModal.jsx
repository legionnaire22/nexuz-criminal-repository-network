import React from 'react';

export function HitlReviewModal({
  reviewItems,
  reviewStatusMsg,
  onApplyDecision,
  onClose
}) {
  return (
    <div className="court-modal-overlay" onClick={onClose}>
      <div className="court-dossier-sheet" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '820px' }}>
        <div className="court-dossier-head" style={{ borderBottom: '1px solid rgba(168, 85, 247, 0.3)' }}>
          <div>
            <div className="court-title-main" style={{ color: '#d8b4fe' }}>
              <i className="fa-solid fa-scale-balanced"></i> HUMAN-IN-THE-LOOP RESOLVER QUEUE (BNSS COMPLIANT)
            </div>
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.68rem', color: 'var(--text-dim)' }}>
              AMBIGUOUS ENTITY MERGES AWAITING LEAD INVESTIGATOR RATIFICATION &bull; ACTIVE SQLITE AUDIT QUEUE
            </span>
          </div>
          <button 
            style={{ background: 'transparent', border: 'none', color: '#fff', fontSize: '1.2rem', cursor: 'pointer' }}
            onClick={onClose}
          >
            <i className="fa-solid fa-xmark"></i>
          </button>
        </div>

        <div className="court-dossier-body">
          {reviewStatusMsg && (
            <div style={{ 
              padding: '8px 12px', 
              marginBottom: '12px', 
              borderRadius: '4px', 
              background: 'rgba(0, 255, 136, 0.15)', 
              border: '1px solid var(--emerald-radar)', 
              color: 'var(--emerald-radar)', 
              fontFamily: 'var(--font-mono)', 
              fontSize: '0.75rem' 
            }}>
              {reviewStatusMsg}
            </div>
          )}

          <table className="evidence-table">
            <thead>
              <tr>
                <th>Merge ID</th>
                <th>Candidate Entity 1</th>
                <th>Candidate Entity 2</th>
                <th>Score</th>
                <th>Corroboration Signals</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {reviewItems.map(item => (
                <tr key={item.merge_id}>
                  <td style={{ fontFamily: 'var(--font-mono)', color: 'var(--cyan-bright)' }}>{item.merge_id}</td>
                  <td><strong>{item.entity_1?.name}</strong> <span style={{ fontSize: '0.65rem', color: 'var(--text-dim)' }}>({item.entity_1?.doc})</span></td>
                  <td><strong>{item.entity_2?.name}</strong> <span style={{ fontSize: '0.65rem', color: 'var(--text-dim)' }}>({item.entity_2?.doc})</span></td>
                  <td>
                    <span style={{ fontWeight: 'bold', color: item.similarity_score >= 0.85 ? 'var(--emerald-radar)' : 'var(--amber-warn)' }}>
                      {(item.similarity_score * 100).toFixed(0)}%
                    </span>
                  </td>
                  <td style={{ fontSize: '0.72rem', color: '#cbd5e1' }}>{item.match_reason}</td>
                  <td>
                    {item.status === 'APPROVED' ? (
                      <span style={{ color: 'var(--emerald-radar)', fontWeight: 'bold', fontSize: '0.75rem' }}><i className="fa-solid fa-check"></i> APPROVED</span>
                    ) : item.status === 'REJECTED' ? (
                      <span style={{ color: 'var(--crimson-target)', fontWeight: 'bold', fontSize: '0.75rem' }}><i className="fa-solid fa-xmark"></i> REJECTED</span>
                    ) : (
                      <div style={{ display: 'flex', gap: '6px' }}>
                        <button 
                          style={{ padding: '4px 8px', background: 'rgba(0, 255, 136, 0.2)', border: '1px solid var(--emerald-radar)', color: '#fff', borderRadius: '4px', cursor: 'pointer', fontSize: '0.7rem' }}
                          onClick={() => onApplyDecision(item.merge_id, 'APPROVED')}
                        >
                          Approve
                        </button>
                        <button 
                          style={{ padding: '4px 8px', background: 'rgba(255, 42, 85, 0.2)', border: '1px solid var(--crimson-target)', color: '#fff', borderRadius: '4px', cursor: 'pointer', fontSize: '0.7rem' }}
                          onClick={() => onApplyDecision(item.merge_id, 'REJECTED')}
                        >
                          Reject
                        </button>
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
