import React, { useState } from 'react';
import { Target } from 'lucide-react';

const RescueCoveragePanel = ({ zones, onCoverageCalculated }) => {
  const [selectedZone, setSelectedZone] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [coverageInfo, setCoverageInfo] = useState(null);

  const showCoverage = async () => {
    console.log('Show Coverage clicked!', { selectedZone });
    
    if (!selectedZone) {
      setError('Please select a rescue station');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const zone = zones.find(z => z.id === selectedZone);
      console.log('Zone found:', zone);
      
      const response = await fetch(
        `http://localhost:8000/api/here/rescue-coverage?lat=${zone.coordinates.lat}&lon=${zone.coordinates.lon}`
      );

      const data = await response.json();
      console.log('Coverage response:', data);
      
      if (data.error) {
        setError(data.error);
      } else {
        console.log('Calling onCoverageCalculated with:', data, zone);
        onCoverageCalculated && onCoverageCalculated(data, zone);
        setCoverageInfo({ zone: zone.name, isolines: data.isolines });
        setError('');
      }
    } catch (err) {
      console.error('Coverage calculation error:', err);
      setError('Failed to calculate coverage. Make sure HERE API key is configured.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ background: 'var(--color-card)', padding: 16, borderRadius: 8, marginBottom: 16, border: '1px solid var(--color-panel-border)' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
        <Target size={18} style={{ color: '#10b981' }} />
        <h3 style={{ margin: 0, fontSize: 14, fontWeight: 600, color: 'var(--color-text)' }}>Rescue Coverage</h3>
      </div>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
        <select
          value={selectedZone}
          onChange={e => setSelectedZone(e.target.value)}
          style={{ padding: '6px 8px', borderRadius: 4, border: '1px solid var(--color-panel-border)', background: 'var(--color-bg)', color: 'var(--color-text)', fontSize: 13 }}
        >
          <option value="">Select Rescue Station</option>
          {zones.map(zone => (
            <option key={zone.id} value={zone.id}>{zone.name}</option>
          ))}
        </select>

        <button
          onClick={showCoverage}
          disabled={loading}
          style={{ padding: '8px 12px', borderRadius: 4, border: 'none', background: '#10b981', color: 'white', cursor: loading ? 'not-allowed' : 'pointer', fontSize: 13, fontWeight: 500 }}
        >
          {loading ? 'Calculating...' : 'Show Coverage (5/10/15 min)'}
        </button>

        {error && <div style={{ color: '#ef4444', fontSize: 12 }}>{error}</div>}
        
        {coverageInfo && (
          <div style={{ marginTop: 10, padding: 8, background: 'rgba(16, 185, 129, 0.1)', borderRadius: 4, fontSize: 12 }}>
            <div style={{ color: 'var(--color-text)', marginBottom: 6 }}>
              <strong>Station:</strong> {coverageInfo.zone}
            </div>
            <div style={{ color: 'var(--color-text)', fontSize: 11 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 4, marginBottom: 2 }}>
                <div style={{ width: 12, height: 12, background: '#10b981', borderRadius: 2 }}></div>
                <span>5 min coverage</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 4, marginBottom: 2 }}>
                <div style={{ width: 12, height: 12, background: '#f59e0b', borderRadius: 2 }}></div>
                <span>10 min coverage</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                <div style={{ width: 12, height: 12, background: '#ef4444', borderRadius: 2 }}></div>
                <span>15 min coverage</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RescueCoveragePanel;
