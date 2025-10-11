import React, { useState } from 'react';
import { AlertTriangle } from 'lucide-react';
import './PrioritizationPanel.css';

const PrioritizationPanel = ({ zones }) => {
  const [confirmations, setConfirmations] = useState({});
  const [showAll, setShowAll] = useState(false);
  if (!zones || zones.length === 0) return null;
  const severityOrder = { critical: 1, high: 2, medium: 3, low: 4 };
  const sorted = [...zones].sort((a, b) => {
    // Feedback priority: zones with responder feedback '4' (critical) move to top
    const aFeedback = confirmations[a.id];
    const bFeedback = confirmations[b.id];
    if (aFeedback === '4' && bFeedback !== '4') return -1;
    if (bFeedback === '4' && aFeedback !== '4') return 1;
    // Then by severity
    if (severityOrder[a.severity] !== severityOrder[b.severity]) {
      return severityOrder[a.severity] - severityOrder[b.severity];
    }
    // Then by original damage score
    return b.damage_score - a.damage_score;
  });
  const handleConfirm = (zoneId, value) => {
    setConfirmations(prev => ({ ...prev, [zoneId]: value }));
  };
  const displayList = showAll ? sorted : sorted.slice(0, 5);

  return (
    <div className="prioritization-panel">
      <div className="prioritization-header">
        <AlertTriangle size={18} style={{ color: '#ef4444' }} />
        <h3>Damage Prioritization</h3>
      </div>
      <div style={{ marginBottom: 8, fontSize: 12, color: '#64748b', display: 'flex', gap: 16, flexWrap: 'wrap' }}>
        <span style={{ fontWeight: 500 }}>Responder Feedback:</span>
        <span>1=Mild</span>
        <span>2=Moderate</span>
        <span>3=Severe</span>
        <span>4=Critical</span>
      </div>
      <ol className="priority-list">
        {displayList.map((zone, idx) => (
          <li key={zone.id} className={`priority-item priority-${zone.severity}`} style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap' }}>
            <span className="priority-rank">#{idx + 1}</span>
            <span className="priority-name">{zone.name}</span>
            <span className="priority-severity">{zone.severity}</span>
            <select
              value={confirmations[zone.id] || ''}
              onChange={e => handleConfirm(zone.id, e.target.value)}
              style={{ marginLeft: 'auto', width: 60, fontSize: 13, borderRadius: 4, padding: '2px 4px', background: '#fff', border: '1px solid #cbd5e1' }}
            >
              <option value="">FB</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
            </select>
          </li>
        ))}
      </ol>
      {sorted.length > 5 && (
        <button
          onClick={() => setShowAll(v => !v)}
          style={{ margin: '10px auto 0 auto', display: 'block', fontSize: 13, borderRadius: 4, padding: '4px 14px', background: '#3b82f6', color: 'white', border: 'none', cursor: 'pointer' }}
        >
          {showAll ? 'Show Top 5 Only' : `Show All (${sorted.length})`}
        </button>
      )}
    </div>
  );
}

export default PrioritizationPanel;
