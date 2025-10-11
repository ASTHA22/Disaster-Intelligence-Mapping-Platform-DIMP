import React, { useState } from 'react';
import { Navigation, MapPin } from 'lucide-react';

const RoutePanel = ({ zones, onRouteCalculated }) => {
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [routeInfo, setRouteInfo] = useState(null);

  const calculateRoute = async () => {
    console.log('Calculate Route clicked!', { origin, destination });
    
    if (!origin || !destination) {
      setError('Please select both origin and destination');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const originZone = zones.find(z => z.id === origin);
      const destZone = zones.find(z => z.id === destination);
      
      console.log('Zones found:', { originZone, destZone });

      const response = await fetch('http://localhost:8000/api/here/route', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          origin_lat: originZone.coordinates.lat,
          origin_lon: originZone.coordinates.lon,
          destination_lat: destZone.coordinates.lat,
          destination_lon: destZone.coordinates.lon
        })
      });

      const data = await response.json();
      console.log('Route response:', data);
      
      if (data.error || data.detail) {
        setError(data.error || data.detail || 'Route calculation failed');
      } else {
        // Create simple route from origin to destination for visualization
        const simpleRoute = {
          ...data,
          coordinates: [
            [originZone.coordinates.lat, originZone.coordinates.lon],
            [destZone.coordinates.lat, destZone.coordinates.lon]
          ]
        };
        console.log('Calling onRouteCalculated with simple route');
        onRouteCalculated && onRouteCalculated(simpleRoute);
        setRouteInfo(data);
        setError('');
      }
    } catch (err) {
      console.error('Route calculation error:', err);
      setError('Failed to calculate route. Make sure HERE API key is configured.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ background: 'var(--color-card)', padding: 16, borderRadius: 8, marginBottom: 16, border: '1px solid var(--color-panel-border)' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
        <Navigation size={18} style={{ color: '#3b82f6' }} />
        <h3 style={{ margin: 0, fontSize: 14, fontWeight: 600, color: 'var(--color-text)' }}>Evacuation Route</h3>
      </div>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
        <select
          value={origin}
          onChange={e => setOrigin(e.target.value)}
          style={{ padding: '6px 8px', borderRadius: 4, border: '1px solid var(--color-panel-border)', background: 'var(--color-bg)', color: 'var(--color-text)', fontSize: 13 }}
        >
          <option value="">Select Origin (Disaster Zone)</option>
          {zones.map(zone => (
            <option key={zone.id} value={zone.id}>{zone.name} - {zone.severity}</option>
          ))}
        </select>

        <select
          value={destination}
          onChange={e => setDestination(e.target.value)}
          style={{ padding: '6px 8px', borderRadius: 4, border: '1px solid var(--color-panel-border)', background: 'var(--color-bg)', color: 'var(--color-text)', fontSize: 13 }}
        >
          <option value="">Select Destination (Shelter)</option>
          {zones.map(zone => (
            <option key={zone.id} value={zone.id}>{zone.name}</option>
          ))}
        </select>

        <button
          onClick={calculateRoute}
          disabled={loading}
          style={{ padding: '8px 12px', borderRadius: 4, border: 'none', background: '#3b82f6', color: 'white', cursor: loading ? 'not-allowed' : 'pointer', fontSize: 13, fontWeight: 500 }}
        >
          {loading ? 'Calculating...' : 'Calculate Route'}
        </button>

        {error && <div style={{ color: '#ef4444', fontSize: 12 }}>{error}</div>}
        
        {routeInfo && (
          <div style={{ marginTop: 10, padding: 8, background: 'rgba(59, 130, 246, 0.1)', borderRadius: 4, fontSize: 12 }}>
            <div style={{ color: 'var(--color-text)', marginBottom: 4 }}>
              <strong>Distance:</strong> {routeInfo.distance_km} km
            </div>
            <div style={{ color: 'var(--color-text)' }}>
              <strong>Duration:</strong> {routeInfo.duration_minutes} min
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RoutePanel;
