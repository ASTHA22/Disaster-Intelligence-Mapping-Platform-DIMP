import React, { useState, useEffect } from 'react';
import './App.css';
import DisasterMapLeaflet from './components/DisasterMapLeaflet';
import Dashboard from './components/Dashboard';
import PrioritizationPanel from './components/PrioritizationPanel';
import AlertPanel from './components/AlertPanel';
import RoutePanel from './components/RoutePanel';
import RescueCoveragePanel from './components/RescueCoveragePanel';
import ImageComparisonPanel from './components/ImageComparisonPanel';
import SocialFeed from './components/SocialFeed';
import Header from './components/Header';
import { Sun, Moon } from 'lucide-react';
import TimeSlider from './components/TimeSlider';
import SearchBar from './components/SearchBar';
import Notifications from './components/Notifications';
import { fetchDisasterData } from './services/api';

function App() {
  const [theme, setTheme] = useState('dark');
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);
  const toggleTheme = () => setTheme(theme === 'dark' ? 'light' : 'dark');
  const [disasterData, setDisasterData] = useState({
    zones: [],
    floodAreas: [],
    infrastructure: [],
    displacement: [],
    alerts: [],
    socialFeed: [],
    statistics: {}
  });
  
  const [selectedLayer, setSelectedLayer] = useState({
    zones: true,
    floods: true,
    infrastructure: true,
    displacement: true
  });
  
  const [currentTime, setCurrentTime] = useState(24); // 24 = now, 0 = 24h ago
  const [isPlaying, setIsPlaying] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [selectedZone, setSelectedZone] = useState(null);
  const [liveStatus, setLiveStatus] = useState(false);
  const [loading, setLoading] = useState(true);
  const [routeData, setRouteData] = useState(null);
  const [coverageData, setCoverageData] = useState(null);

  useEffect(() => {
    const poll = async () => {
      await loadData();
      setLiveStatus(true);
      setTimeout(() => setLiveStatus(false), 1000);
    };
    poll();
    const interval = setInterval(poll, 30000); // Poll every 30 seconds instead of 10
    return () => clearInterval(interval);
  }, []);

  // Time slider playback
  useEffect(() => {
    let timer;
    if (isPlaying && currentTime < 24) {
      timer = setTimeout(() => {
        setCurrentTime(prev => Math.min(prev + 1, 24));
      }, 1000);
    } else if (isPlaying && currentTime >= 24) {
      setIsPlaying(false);
    }
    return () => {
      if (timer) {
        clearTimeout(timer);
      }
    };
  }, [isPlaying, currentTime]);

  const loadData = async () => {
    try {
      const data = await fetchDisasterData();
      // Merge new data with existing state to preserve user interactions
      setDisasterData(prevData => ({
        ...prevData,
        ...data,
        // Preserve any existing data that shouldn't be overwritten
      }));
      setLoading(false);
    } catch (error) {
      console.error('Error loading disaster data:', error);
      // Don't clear data on error, just stop loading indicator
      setLoading(false);
      // Keep existing data intact
    }
  };

  const toggleLayer = (layer) => {
    setSelectedLayer(prev => ({
      ...prev,
      [layer]: !prev[layer]
    }));
  };

  const handleTimeChange = (time) => {
    setCurrentTime(time);
    setIsPlaying(false);
  };

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  const handleReset = () => {
    setCurrentTime(24);
    setIsPlaying(false);
  };

  const handleExport = async (format) => {
    try {
      addNotification({
        type: 'info',
        message: `Generating ${format.toUpperCase()} report...`,
        autoClose: true,
        duration: 2000
      });

      const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/api/export/${format}`);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `disaster_report_${Date.now()}.${format}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      addNotification({
        type: 'success',
        title: 'Export Successful',
        message: `${format.toUpperCase()} report downloaded successfully!`,
        autoClose: true,
        duration: 3000
      });
    } catch (error) {
      console.error(`Export failed:`, error);
      addNotification({
        type: 'error',
        title: 'Export Failed',
        message: `Failed to export ${format.toUpperCase()}. Please try again.`,
        autoClose: true,
        duration: 5000
      });
    }
  };

  const addNotification = (notification) => {
    const id = Date.now();
    setNotifications(prev => [...prev, { ...notification, id }]);
  };

  const dismissNotification = (id) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  const handleLocationSelect = (zone) => {
    setSelectedZone(zone);
    addNotification({
      type: 'info',
      message: `Viewing ${zone.name} - ${zone.severity} severity`,
      autoClose: true,
      duration: 3000
    });
  };

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Loading Disaster Intelligence Platform...</p>
      </div>
    );
  }

  return (
    <div className="App">
      <div style={{ position: 'relative', width: '100%' }}>
        <Header statistics={disasterData.statistics} />
        <button
          onClick={toggleTheme}
          className="theme-toggle-btn"
          title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
        >
          {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
        </button>
      </div>
      
      <Notifications 
        notifications={notifications}
        onDismiss={dismissNotification}
      />

      <div className="main-container">
        <div className="left-panel">
          <SearchBar 
            zones={disasterData.zones}
            onLocationSelect={handleLocationSelect}
          />
          <TimeSlider
            currentTime={currentTime}
            onTimeChange={handleTimeChange}
            isPlaying={isPlaying}
            onPlayPause={handlePlayPause}
            onReset={handleReset}
          />
          <PrioritizationPanel zones={disasterData.zones} />
          <RoutePanel 
            zones={disasterData.zones}
            onRouteCalculated={(route) => setRouteData(route)}
          />
          <RescueCoveragePanel 
            zones={disasterData.zones}
            onCoverageCalculated={(coverage, zone) => setCoverageData({ coverage, zone })}
          />
          <ImageComparisonPanel />
          <Dashboard 
            statistics={disasterData.statistics}
            selectedLayer={selectedLayer}
            toggleLayer={toggleLayer}
            onExport={handleExport}
          />
          <AlertPanel alerts={disasterData.alerts} />
        </div>
        
        <div className="map-container">
          <DisasterMapLeaflet 
            zones={disasterData.zones}
            floodAreas={disasterData.floodAreas}
            infrastructure={disasterData.infrastructure}
            displacement={disasterData.displacement}
            selectedLayer={selectedLayer}
            selectedZone={selectedZone}
            routeData={routeData}
            coverageData={coverageData}
          />
        </div>
        
        <div className="right-panel">
          <SocialFeed posts={disasterData.socialFeed} />
        </div>
      </div>
    </div>
  );
}

export default App;
