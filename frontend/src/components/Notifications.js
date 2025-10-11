import React, { useState, useEffect } from 'react';
import { CheckCircle, AlertCircle, Info, X } from 'lucide-react';
import './Notifications.css';

const Notifications = ({ notifications, onDismiss }) => {
  return (
    <div className="notifications-container">
      {notifications.map((notification) => (
        <Notification
          key={notification.id}
          notification={notification}
          onDismiss={onDismiss}
        />
      ))}
    </div>
  );
};

const Notification = ({ notification, onDismiss }) => {
  const [isExiting, setIsExiting] = useState(false);

  const handleDismiss = () => {
    setIsExiting(true);
    setTimeout(() => {
      onDismiss && onDismiss(notification.id);
    }, 300);
  };

  useEffect(() => {
    if (notification.autoClose) {
      const timer = setTimeout(() => {
        handleDismiss();
      }, notification.duration || 5000);

      return () => clearTimeout(timer);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [notification]);

  const getIcon = () => {
    switch (notification.type) {
      case 'success':
        return <CheckCircle size={20} />;
      case 'error':
        return <AlertCircle size={20} />;
      case 'info':
      default:
        return <Info size={20} />;
    }
  };

  return (
    <div className={`notification notification-${notification.type} ${isExiting ? 'exiting' : ''}`}>
      <div className="notification-icon">
        {getIcon()}
      </div>
      <div className="notification-content">
        {notification.title && (
          <div className="notification-title">{notification.title}</div>
        )}
        <div className="notification-message">{notification.message}</div>
      </div>
      <button className="notification-close" onClick={handleDismiss}>
        <X size={16} />
      </button>
    </div>
  );
};

export default Notifications;
