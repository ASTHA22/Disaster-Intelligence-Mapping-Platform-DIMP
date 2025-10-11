import React from 'react';
import { AlertTriangle, Activity } from 'lucide-react';
import './Header.css';

const Header = ({ statistics }) => {
  return (
    <header className="header">
      <div className="header-left">
        <AlertTriangle className="logo-icon" size={32} />
        <div className="header-title">
          <h1>DIMP</h1>
          <p>Disaster Intelligence Mapping Platform</p>
        </div>
      </div>
      
      <div className="header-stats">
        <div className="stat-item">
          <Activity size={18} />
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span className="stat-label">Active Operations</span>
            <span className="stat-value">{statistics.rescue_operations_active || 0}</span>
          </div>
        </div>
        
        <div className="stat-separator"></div>
        
        <div className="stat-item">
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span className="stat-label">Affected Area</span>
            <span className="stat-value">{statistics.total_affected_area_km2 || 0} km²</span>
          </div>
        </div>
        
        <div className="stat-separator"></div>
        
        <div className="stat-item critical">
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span className="stat-label">Displaced</span>
            <span className="stat-value">{statistics.displaced_population?.toLocaleString() || 0}</span>
          </div>
        </div>
      </div>
      
      <div className="header-right">
        <div className="status-indicator">
          <span className="status-dot"></span>
          <span>Live</span>
        </div>
        <div className="last-update">
          Last updated: {new Date().toLocaleTimeString()}
        </div>
      </div>
    </header>
  );
};

export default Header;
