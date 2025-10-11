import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, Polygon, useMap } from 'react-leaflet';
import L from 'leaflet';
import { Home, Droplets, Users, AlertTriangle } from 'lucide-react';
import 'leaflet/dist/leaflet.css';
import './DisasterMap.css';

// Decode HERE Flexible Polyline format
const decodePolyline = (encoded) => {
  const coords = [];
  let index = 0;
  
  // Decode header (first value is version and precision)
  const decodeUnsignedValue = () => {
    let result = 0;
    let shift = 0;
    let b;
    do {
      b = encoded.charCodeAt(index++) - 63;
      result |= (b & 0x1f) << shift;
      shift += 5;
    } while (b >= 0x20);
    return result;
  };
  
  const decodeSignedValue = () => {
    const value = decodeUnsignedValue();
    return (value & 1) ? ~(value >> 1) : (value >> 1);
  };
  
  // Read header
  const header = decodeUnsignedValue();
  const precision = header & 15;
  const thirdDim = (header >> 4) & 7;
  const thirdDimPrecision = (header >> 7) & 15;
  // HERE uses precision value to indicate 10^5, not the actual exponent
  const factor = 100000;
  
  let lat = 0;
  let lng = 0;
  let z = 0;
  
  while (index < encoded.length) {
    lat += decodeSignedValue();
    lng += decodeSignedValue();
    
    if (thirdDim) {
      z += decodeSignedValue();
    }
    
    coords.push([lat / factor, lng / factor]);
  }
  
  return coords;
};

// Fix Leaflet default marker icon issue
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

// Component to handle map updates
function MapUpdater({ center, zoom }) {
  const map = useMap();
  
  useEffect(() => {
    if (center) {
      map.setView(center, zoom, { animate: true, duration: 1 });
    }
  }, [center, zoom, map]);
  
  return null;
}

const DisasterMapLeaflet = ({ zones, floodAreas, infrastructure, displacement, selectedLayer, selectedZone, routeData, coverageData }) => {
  const [center, setCenter] = useState([19.0760, 72.8777]); // Mumbai
  const [zoom, setZoom] = useState(11);
  const [theme, setTheme] = useState('dark');
  const [mapStyle, setMapStyle] = useState('standard'); // 'standard', 'satellite', 'drone'


  // Detect theme changes
  useEffect(() => {
    const observer = new MutationObserver(() => {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
      setTheme(currentTheme);
    });
    
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['data-theme']
    });
    
    // Set initial theme
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    setTheme(currentTheme);
    
    return () => observer.disconnect();
  }, []);

  // Update map when zone is selected
  useEffect(() => {
    if (selectedZone && selectedZone.coordinates) {
      setCenter([selectedZone.coordinates.lat, selectedZone.coordinates.lon]);
      setZoom(13);
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
      severe: '#dc2626',
      major: '#ea580c',
      moderate: '#f59e0b',
      minor: '#fbbf24'
    };
    return colors[damageLevel] || '#64748b';
  };

  // Create custom icons
  const createCustomIcon = (color, IconComponent) => {
    return L.divIcon({
      className: 'custom-marker',
      html: `<div style="background-color: ${color}; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 2px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
          ${IconComponent === 'alert' ? '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line>' : ''}
          ${IconComponent === 'droplet' ? '<path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>' : ''}
          ${IconComponent === 'home' ? '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline>' : ''}
          ${IconComponent === 'users' ? '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path>' : ''}
        </svg>
      </div>`,
      iconSize: [32, 32],
      iconAnchor: [16, 16],
      popupAnchor: [0, -16]
    });
  };

  return (
    <div className="disaster-map" style={{ height: '100%', width: '100%', padding: '16px' }}>
      <div style={{ display: 'flex', gap: 8, marginBottom: 10, alignItems: 'center' }}>
        <span style={{ fontWeight: 600, fontSize: 14 }}>Map Style:</span>
        <button onClick={() => setMapStyle('standard')} style={{ background: mapStyle==='standard' ? '#3b82f6' : '#e5e7eb', color: mapStyle==='standard' ? 'white' : '#1e293b', border: 'none', borderRadius: 6, padding: '4px 12px', cursor: 'pointer' }}>Standard</button>
        <button onClick={() => setMapStyle('satellite')} style={{ background: mapStyle==='satellite' ? '#3b82f6' : '#e5e7eb', color: mapStyle==='satellite' ? 'white' : '#1e293b', border: 'none', borderRadius: 6, padding: '4px 12px', cursor: 'pointer' }}>Satellite</button>
        <button onClick={() => setMapStyle('drone')} style={{ background: mapStyle==='drone' ? '#3b82f6' : '#e5e7eb', color: mapStyle==='drone' ? 'white' : '#1e293b', border: 'none', borderRadius: 6, padding: '4px 12px', cursor: 'pointer' }}>Drone</button>
      </div>
      <MapContainer
        center={center}
        zoom={zoom}
        style={{ height: 'calc(100% - 50px)', width: '100%', borderRadius: '8px' }}
        zoomControl={true}
      >
        {/* Map Tiles - switches based on mapStyle */}
        {mapStyle === 'satellite' ? (
          <TileLayer
            attribution='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
            url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
            maxZoom={19}
          />
        ) : (
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
            url={theme === 'dark'
              ? "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
              : "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
            }
            subdomains="abcd"
            maxZoom={20}
          />
        )}
        {/* Drone overlay simulation */}
        {mapStyle === 'drone' && (
          <TileLayer
            url="https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png"
            opacity={0.4}
            attribution="&copy; Stadia Maps"
          />
        )}

        <MapUpdater center={center} zoom={zoom} />

        {/* Disaster Zones */}
        {selectedLayer.zones && zones.filter(zone => zone.coordinates).map(zone => (
          <Marker
            key={zone.id}
            position={[zone.coordinates.lat, zone.coordinates.lon]}
            icon={createCustomIcon(getSeverityColor(zone.severity), 'alert')}
          >
            <Popup>
              <div style={{ color: '#1e293b' }}>
                <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', fontWeight: 'bold' }}>{zone.name}</h3>
                <p style={{ margin: '4px 0', fontSize: '12px' }}>
                  <strong>Severity:</strong> <span style={{ color: getSeverityColor(zone.severity), textTransform: 'uppercase' }}>{zone.severity}</span>
                </p>
                <p style={{ margin: '4px 0', fontSize: '12px' }}>
                  <strong>Damage:</strong> {(zone.damage_score * 100).toFixed(0)}%
                </p>
                <p style={{ margin: '4px 0', fontSize: '12px' }}>
                  <strong>Area:</strong> {zone.affected_area_km2} km²
                </p>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Flood Areas */}
        {selectedLayer.floods && floodAreas.filter(flood => flood.coordinates).map(flood => (
          <Marker
            key={flood.id}
            position={[flood.coordinates.lat, flood.coordinates.lon]}
            icon={createCustomIcon('#3b82f6', 'droplet')}
          >
            <Popup>
              <div style={{ color: '#1e293b' }}>
                <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', fontWeight: 'bold' }}>{flood.location}</h3>
                <p style={{ margin: '4px 0', fontSize: '12px' }}>
                  <strong>Water Level:</strong> {flood.water_level_m}m
                </p>
                <p style={{ margin: '4px 0', fontSize: '12px' }}>
                  <strong>Status:</strong> {flood.status}
                </p>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Infrastructure Damage */}
        {selectedLayer.infrastructure && infrastructure.filter(infra => infra.coordinates).map(infra => (
          <Marker
            key={infra.id}
            position={[infra.coordinates.lat, infra.coordinates.lon]}
            icon={createCustomIcon(getDamageColor(infra.damage_level), 'home')}
          >
            <Popup>
              <div style={{ color: '#1e293b' }}>
                <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', fontWeight: 'bold' }}>{infra.type}</h3>
                <p style={{ margin: '4px 0', fontSize: '12px' }}>
                  <strong>Location:</strong> {infra.location}
                </p>
                <p style={{ margin: '4px 0', fontSize: '12px' }}>
                  <strong>Damage:</strong> {infra.damage_level}
                </p>
                <p style={{ margin: '4px 0', fontSize: '12px' }}>
                  <strong>Status:</strong> {infra.status}
                </p>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Displacement Zones */}
        {selectedLayer.displacement && displacement.filter(disp => disp.coordinates).map(disp => (
          <Marker
            key={disp.id}
            position={[disp.coordinates.lat, disp.coordinates.lon]}
            icon={createCustomIcon('#a855f7', 'users')}
          >
            <Popup>
              <div style={{ color: '#1e293b' }}>
                <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', fontWeight: 'bold' }}>{disp.area}</h3>
                <p style={{ margin: '4px 0', fontSize: '12px' }}>
                  <strong>Displaced:</strong> {disp.displaced_count.toLocaleString()} people
                </p>
                <p style={{ margin: '4px 0', fontSize: '12px' }}>
                  <strong>Shelter Capacity:</strong> {disp.shelter_capacity.toLocaleString()}
                </p>
                <p style={{ margin: '4px 0', fontSize: '12px' }}>
                  <strong>Status:</strong> {disp.status}
                </p>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Route and Coverage Visualization */}
        <>
          {routeData && routeData.coordinates && routeData.coordinates.length >= 2 && (
            <Polyline
              positions={routeData.coordinates}
              color="#3b82f6"
              weight={4}
              opacity={0.8}
            />
          )}
          {/* Rescue Coverage Visualization */}
          {coverageData && coverageData.coverage && coverageData.coverage.isolines &&
            coverageData.coverage.isolines.map((isoline, idx) => {
              try {
                if (!isoline.polygons || !isoline.polygons[0]) {
                  return null;
                }
                // Backend returns polygons as array of coordinates in [lng, lat]
                const coords = isoline.polygons[0];

                // Validate ranges (lng, lat) then convert to Leaflet's [lat, lng]
                const positions = coords
                  .filter(coord =>
                    Array.isArray(coord) &&
                    coord.length === 2 &&
                    Math.abs(coord[0]) <= 180 && // lng
                    Math.abs(coord[1]) <= 90     // lat
                  )
                  .map(coord => [coord[1], coord[0]]); // [lat, lng]

                if (positions.length < 3) {
                  console.log('Not enough valid positions after [lng,lat] -> [lat,lng] conversion for isoline', idx);
                  return null;
                }
                return (
                  <Polygon
                    key={idx}
                    positions={positions}
                    color={idx === 0 ? '#10b981' : idx === 1 ? '#f59e0b' : '#ef4444'}
                    fillColor={idx === 0 ? '#10b981' : idx === 1 ? '#f59e0b' : '#ef4444'}
                    fillOpacity={0.4}
                    weight={3}
                  />
                );
              } catch (e) {
                console.error('Polygon render error:', e);
                return null;
              }
            })}

          {/* Add a marker at the coverage origin */}
          {coverageData && coverageData.coverage && coverageData.coverage.origin && coverageData.coverage.origin.location && (
            <Marker
              position={[coverageData.coverage.origin.location.lat, coverageData.coverage.origin.location.lng]}
              icon={L.icon({
                iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
              })}
            >
              <Popup>Rescue Station</Popup>
            </Marker>
          )}
        </>
      {/* End overlays fragment */}
    </MapContainer>
  </div>
);
}

export default DisasterMapLeaflet;
