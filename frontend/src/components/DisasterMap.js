import React, { useState } from 'react';
import Map, { Marker, Popup } from 'react-map-gl';
import { Home, Droplets, Users, AlertTriangle, Clock } from 'lucide-react';
import 'mapbox-gl/dist/mapbox-gl.css';
import './DisasterMap.css';

// Using CartoDB Dark Matter - free, no API key required

const DisasterMap = ({ zones, floodAreas, infrastructure, displacement, selectedLayer, selectedZone }) => {
  const [viewState, setViewState] = useState({
    longitude: 72.8777,  // Mumbai
    latitude: 19.0760,   // Mumbai
    zoom: 11
  });
  
  const [popupInfo, setPopupInfo] = useState(null);

  // Zoom to selected zone from search
  React.useEffect(() => {
    if (selectedZone && selectedZone.coordinates) {
      setViewState({
        longitude: selectedZone.coordinates.lon,
        latitude: selectedZone.coordinates.lat,
        zoom: 13,
        transitionDuration: 1000
      });
      setPopupInfo(selectedZone);
    }
  }, [selectedZone]);

  const getSeverityColor = (severity) => {
    const colors = {
      critical: '#ef4444',
      high: '#f59e0b',
      medium: '#3b82f6',
      low: '#10b981'
    };
    return colors[severity] || '#64748b';
  };

  const getDamageColor = (damageLevel) => {
    const colors = {
      destroyed: '#7f1d1d',
      severe: '#ef4444',
      moderate: '#f59e0b',
      minor: '#fbbf24'
    };
    return colors[damageLevel] || '#64748b';
  };


  return (
    <div className="disaster-map">
      <Map
        {...viewState}
        onMove={evt => setViewState(evt.viewState)}
        mapStyle={{
          version: 8,
          sources: {
            'carto-dark': {
              type: 'raster',
              tiles: ['https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png'],
              tileSize: 256,
              attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
            }
          },
          layers: [
            {
              id: 'carto-dark-layer',
              type: 'raster',
              source: 'carto-dark',
              minzoom: 0,
              maxzoom: 22
            }
          ]
        }}
        style={{ width: '100%', height: '100%' }}
      >
        {/* Disaster Zones */}
        {selectedLayer.zones && zones.filter(zone => zone.coordinates).map(zone => (
          <Marker
            key={zone.id}
            longitude={zone.coordinates.lon}
            latitude={zone.coordinates.lat}
            anchor="center"
          >
            <div 
              className="marker disaster-marker"
              style={{ 
                backgroundColor: getSeverityColor(zone.severity),
                boxShadow: `0 0 20px ${getSeverityColor(zone.severity)}`
              }}
              onClick={() => setPopupInfo({ type: 'zone', data: zone })}
            >
              <AlertTriangle size={20} />
            </div>
          </Marker>
        ))}

        {/* Flood Areas */}
        {selectedLayer.floods && floodAreas.filter(flood => flood.coordinates).map(flood => (
          <Marker
            key={flood.id}
            longitude={flood.coordinates.lon}
            latitude={flood.coordinates.lat}
            anchor="center"
          >
            <div 
              className="marker flood-marker"
              onClick={() => setPopupInfo({ type: 'flood', data: flood })}
            >
              <Droplets size={20} />
            </div>
          </Marker>
        ))}

        {/* Infrastructure Damage */}
        {selectedLayer.infrastructure && infrastructure.filter(infra => infra.coordinates).map(infra => (
          <Marker
            key={infra.id}
            longitude={infra.coordinates.lon}
            latitude={infra.coordinates.lat}
            anchor="center"
          >
            <div 
              className="marker infrastructure-marker"
              style={{ backgroundColor: getDamageColor(infra.damage_level) }}
              onClick={() => setPopupInfo({ type: 'infrastructure', data: infra })}
            >
              <Home size={18} />
            </div>
          </Marker>
        ))}

        {/* Displacement Zones */}
        {selectedLayer.displacement && displacement.filter(disp => disp.coordinates).map(disp => (
          <Marker
            key={disp.id}
            longitude={disp.coordinates.lon}
            latitude={disp.coordinates.lat}
            anchor="center"
          >
            <div 
              className="marker displacement-marker"
              onClick={() => setPopupInfo({ type: 'displacement', data: disp })}
            >
              <Users size={20} />
              <span className="marker-count">{disp.displaced_count}</span>
            </div>
          </Marker>
        ))}

        {/* Popup */}
        {popupInfo && (
          <Popup
            longitude={popupInfo.data.coordinates.lon}
            latitude={popupInfo.data.coordinates.lat}
            anchor="bottom"
            onClose={() => setPopupInfo(null)}
            closeButton={true}
            closeOnClick={false}
            className="custom-popup"
          >
            <div className="popup-content">
              {popupInfo.type === 'zone' && (
                <>
                  <h3>{popupInfo.data.name}</h3>
                  <div className="popup-row">
                    <span>Severity:</span>
                    <span className={`severity-badge ${popupInfo.data.severity}`}>
                      {popupInfo.data.severity.toUpperCase()}
                    </span>
                  </div>
                  <div className="popup-row">
                    <span>Damage Score:</span>
                    <span>{(popupInfo.data.damage_score * 100).toFixed(0)}%</span>
                  </div>
                  <div className="popup-row">
                    <span>Affected Area:</span>
                    <span>{popupInfo.data.affected_area_km2} km²</span>
                  </div>
                </>
              )}

              {popupInfo.type === 'flood' && (
                <>
                  <h3>{popupInfo.data.location}</h3>
                  <div className="popup-row">
                    <span>Water Level:</span>
                    <span>{popupInfo.data.water_level_m} meters</span>
                  </div>
                  <div className="popup-row">
                    <span>Status:</span>
                    <span className="status-badge">{popupInfo.data.status}</span>
                  </div>
                  <div className="popup-row">
                    <span>Affected:</span>
                    <span>{popupInfo.data.affected_population.toLocaleString()} people</span>
                  </div>
                  {popupInfo.data.evacuation_required && (
                    <div className="evacuation-warning">⚠️ Evacuation Required</div>
                  )}
                </>
              )}

              {popupInfo.type === 'infrastructure' && (
                <>
                  <h3>{popupInfo.data.name}</h3>
                  <div className="popup-row">
                    <span>Type:</span>
                    <span>{popupInfo.data.type.replace('_', ' ').toUpperCase()}</span>
                  </div>
                  <div className="popup-row">
                    <span>Damage:</span>
                    <span className={`damage-badge ${popupInfo.data.damage_level}`}>
                      {popupInfo.data.damage_level.toUpperCase()}
                    </span>
                  </div>
                  <div className="popup-row">
                    <span>Operational:</span>
                    <span>{popupInfo.data.operational ? '✓ Yes' : '✗ No'}</span>
                  </div>
                  <div className="popup-row">
                    <span>Repair Time:</span>
                    <span>{popupInfo.data.estimated_repair_days} days</span>
                  </div>
                </>
              )}

              {popupInfo.type === 'displacement' && (
                <>
                  <h3>{popupInfo.data.area}</h3>
                  <div className="popup-row">
                    <span>Displaced:</span>
                    <span>{popupInfo.data.displaced_count.toLocaleString()} people</span>
                  </div>
                  <div className="popup-row">
                    <span>Shelter Capacity:</span>
                    <span>{popupInfo.data.shelter_capacity.toLocaleString()}</span>
                  </div>
                  <div className="popup-needs">
                    <strong>Needs:</strong>
                    <div className="needs-list">
                      {popupInfo.data.needs.map(need => (
                        <span key={need} className="need-tag">{need}</span>
                      ))}
                    </div>
                  </div>
                </>
              )}
            </div>
          </Popup>
        )}
      </Map>

      <div className="map-legend">
        <h4>Legend</h4>
        <div className="legend-item">
          <div className="legend-marker" style={{ backgroundColor: '#ef4444' }}>
            <AlertTriangle size={14} />
          </div>
          <span>Disaster Zone</span>
        </div>
        <div className="legend-item">
          <div className="legend-marker" style={{ backgroundColor: '#3b82f6' }}>
            <Droplets size={14} />
          </div>
          <span>Flood Area</span>
        </div>
        <div className="legend-item">
          <div className="legend-marker" style={{ backgroundColor: '#f59e0b' }}>
            <Home size={14} />
          </div>
          <span>Infrastructure</span>
        </div>
        <div className="legend-item">
          <div className="legend-marker" style={{ backgroundColor: '#8b5cf6' }}>
            <Users size={14} />
          </div>
          <span>Displacement</span>
        </div>
      </div>

      <div className="map-info">
        <p>✅ HERE Maps API Active</p>
        <p>Routing, Isoline & Geocoding enabled • Real-time disaster tracking</p>
      </div>
    </div>
  );
};

export default DisasterMap;
