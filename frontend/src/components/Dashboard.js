import React from 'react';
import { Layers, Home, Droplets, Users, AlertCircle, Download, FileText, FileJson, FileSpreadsheet } from 'lucide-react';
import './Dashboard.css';

const Dashboard = ({ statistics, selectedLayer, toggleLayer, onExport }) => {
  const layers = [
    { id: 'zones', label: 'Disaster Zones', icon: AlertCircle, color: '#ef4444' },
    { id: 'floods', label: 'Flood Areas', icon: Droplets, color: '#3b82f6' },
    { id: 'infrastructure', label: 'Infrastructure', icon: Home, color: '#f59e0b' },
    { id: 'displacement', label: 'Displacement', icon: Users, color: '#8b5cf6' },
  ];

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <Layers size={20} />
        <h2>Control Panel</h2>
      </div>

      <div className="statistics-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{ backgroundColor: '#7f1d1d' }}>
            <Home size={24} />
          </div>
          <div className="stat-content">
            <p className="stat-title">Damaged Buildings</p>
            <p className="stat-number">{statistics.damaged_buildings?.toLocaleString() || 0}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ backgroundColor: '#1e3a8a' }}>
            <Droplets size={24} />
          </div>
          <div className="stat-content">
            <p className="stat-title">Flooded Zones</p>
            <p className="stat-number">{statistics.flooded_zones || 0}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ backgroundColor: '#581c87' }}>
            <Users size={24} />
          </div>
          <div className="stat-content">
            <p className="stat-title">Displaced People</p>
            <p className="stat-number">{statistics.displaced_population?.toLocaleString() || 0}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ backgroundColor: '#065f46' }}>
            <AlertCircle size={24} />
          </div>
          <div className="stat-content">
            <p className="stat-title">Emergency Shelters</p>
            <p className="stat-number">{statistics.emergency_shelters || 0}</p>
          </div>
        </div>
      </div>

      <div className="layer-controls">
        <h3>Map Layers</h3>
        {layers.map(layer => (
          <div key={layer.id} className="layer-toggle">
            <input
              type="checkbox"
              id={layer.id}
              checked={selectedLayer[layer.id]}
              onChange={() => toggleLayer(layer.id)}
            />
            <label htmlFor={layer.id}>
              <layer.icon size={18} style={{ color: layer.color }} />
              <span>{layer.label}</span>
            </label>
          </div>
        ))}
      </div>

      <div className="export-section">
        <h3>
          <Download size={18} />
          Export Data
        </h3>
        <div className="export-buttons">
          <button 
            className="export-btn pdf"
            onClick={() => onExport && onExport('pdf')}
            title="Export as PDF Report"
          >
            <FileText size={16} />
            <span>PDF Report</span>
          </button>
          <button 
            className="export-btn json"
            onClick={() => onExport && onExport('json')}
            title="Export as JSON"
          >
            <FileJson size={16} />
            <span>JSON</span>
          </button>
          <button 
            className="export-btn csv"
            onClick={() => onExport && onExport('csv')}
            title="Export as CSV"
          >
            <FileSpreadsheet size={16} />
            <span>CSV</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
