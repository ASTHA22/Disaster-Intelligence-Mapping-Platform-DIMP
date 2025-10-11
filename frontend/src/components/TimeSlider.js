import React from 'react';
import { Clock, Play, Pause, RotateCcw } from 'lucide-react';
import './TimeSlider.css';

const TimeSlider = ({ currentTime, onTimeChange, isPlaying, onPlayPause, onReset }) => {
  // Generate time options (last 24 hours)
  const generateTimeOptions = () => {
    const options = [];
    const now = new Date();
    
    for (let i = 24; i >= 0; i--) {
      const time = new Date(now - i * 60 * 60 * 1000);
      options.push({
        value: i,
        label: time.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        fullLabel: time.toLocaleString('en-US', { 
          month: 'short', 
          day: 'numeric', 
          hour: '2-digit', 
          minute: '2-digit' 
        })
      });
    }
    
    return options;
  };

  const timeOptions = generateTimeOptions();
  const currentOption = timeOptions[currentTime] || timeOptions[timeOptions.length - 1];

  return (
    <div className="time-slider-container">
      <div className="time-slider-header">
        <Clock size={18} />
        <span className="time-slider-title">Disaster Timeline</span>
        <span className="current-time">{currentOption.fullLabel}</span>
      </div>

      <div className="time-slider-controls">
        <button 
          className="time-control-btn"
          onClick={onPlayPause}
          title={isPlaying ? "Pause" : "Play"}
        >
          {isPlaying ? <Pause size={16} /> : <Play size={16} />}
        </button>

        <div className="slider-wrapper">
          <input
            type="range"
            min="0"
            max={timeOptions.length - 1}
            value={currentTime}
            onChange={(e) => onTimeChange(parseInt(e.target.value))}
            className="time-slider"
          />
          <div className="slider-labels">
            <span>24h ago</span>
            <span>Now</span>
          </div>
        </div>

        <button 
          className="time-control-btn"
          onClick={onReset}
          title="Reset to current time"
        >
          <RotateCcw size={16} />
        </button>
      </div>

      <div className="time-markers">
        {[0, 6, 12, 18, 24].map(hour => (
          <div 
            key={hour} 
            className={`time-marker ${currentTime === hour ? 'active' : ''}`}
            onClick={() => onTimeChange(hour)}
          >
            <div className="marker-dot"></div>
            <span className="marker-label">{hour === 0 ? '24h' : `${24-hour}h`}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TimeSlider;
