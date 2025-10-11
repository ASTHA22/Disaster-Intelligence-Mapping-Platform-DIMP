import React from 'react';
import { Bell, AlertTriangle, AlertCircle, Info } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import './AlertPanel.css';

const AlertPanel = ({ alerts }) => {
  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical':
        return <AlertTriangle size={18} />;
      case 'high':
        return <AlertCircle size={18} />;
      default:
        return <Info size={18} />;
    }
  };

  const getSeverityClass = (severity) => {
    return `alert-item severity-${severity}`;
  };

  return (
    <div className="alert-panel">
      <div className="alert-header">
        <Bell size={20} />
        <h3>Active Alerts</h3>
        <span className="alert-count">{alerts.length}</span>
      </div>

      <div className="alert-list">
        {alerts.slice(0, 8).map(alert => (
          <div key={alert.id} className={getSeverityClass(alert.severity)}>
            <div className="alert-icon">
              {getSeverityIcon(alert.severity)}
            </div>
            <div className="alert-content">
              <div className="alert-title">{alert.type}</div>
              <div className="alert-location">{alert.location}</div>
              <div className="alert-description">{alert.description}</div>
              <div className="alert-meta">
                <span className="alert-time">
                  {formatDistanceToNow(new Date(alert.timestamp), { addSuffix: true })}
                </span>
                <span className="alert-status">{alert.status}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AlertPanel;
