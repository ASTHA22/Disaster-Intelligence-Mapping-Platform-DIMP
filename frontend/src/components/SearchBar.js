import React, { useState } from 'react';
import { Search, MapPin, X } from 'lucide-react';
import './SearchBar.css';

const SearchBar = ({ zones, onLocationSelect }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  
  // Debug: Log zones when component receives them
  React.useEffect(() => {
    console.log('SearchBar received zones:', zones?.length || 0, 'zones');
  }, [zones]);

  const handleSearch = (value) => {
    setQuery(value);
    
    if (value.length < 2) {
      setResults([]);
      setIsOpen(false);
      return;
    }

    // Search through zones - check multiple fields
    const filtered = (zones || []).filter(zone => {
      if (!zone) return false;
      const searchStr = value.toLowerCase();
      
      // Search in name, type, id, location, area, or region fields
      return (
        (zone.name && zone.name.toLowerCase().includes(searchStr)) ||
        (zone.type && zone.type.toLowerCase().includes(searchStr)) ||
        (zone.id && zone.id.toLowerCase().includes(searchStr)) ||
        (zone.location && zone.location.toLowerCase().includes(searchStr)) ||
        (zone.area && zone.area.toLowerCase().includes(searchStr)) ||
        (zone.region && zone.region.toLowerCase().includes(searchStr))
      );
    });

    console.log('Search query:', value);
    console.log('Search results:', filtered.length, 'found');
    console.log('Sample result:', filtered[0]);
    setResults(filtered);
    setIsOpen(filtered.length > 0);
  };

  const handleSelect = (zone) => {
    setQuery(zone.name || zone.location || zone.id);
    setIsOpen(false);
    onLocationSelect && onLocationSelect(zone);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && results.length > 0) {
      // Select first result on Enter
      handleSelect(results[0]);
    }
  };

  const handleClear = () => {
    setQuery('');
    setResults([]);
    setIsOpen(false);
  };

  return (
    <div className="search-bar-container">
      <div className="search-bar">
        <Search size={20} className="search-icon" />
        <input
          type="text"
          placeholder="Search disasters (type: fire, earthquake, Bandra, etc)..."
          value={query}
          onChange={(e) => handleSearch(e.target.value)}
          onKeyPress={handleKeyPress}
          onFocus={() => results.length > 0 && setIsOpen(true)}
          className="search-input"
        />
        {query && (
          <button onClick={handleClear} className="clear-btn">
            <X size={18} />
          </button>
        )}
      </div>

      {isOpen && results.length > 0 && (
        <div className="search-results">
          {results.map((zone) => (
            <div
              key={zone.id}
              className="search-result-item"
              onClick={() => handleSelect(zone)}
            >
              <MapPin size={16} className="result-icon" />
              <div className="result-content">
                <div className="result-name">{zone.name}</div>
                <div className="result-meta">
                  <span className={`severity-badge ${zone.severity}`}>
                    {zone.severity}
                  </span>
                  <span className="result-score">
                    Damage: {(zone.damage_score * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SearchBar;
