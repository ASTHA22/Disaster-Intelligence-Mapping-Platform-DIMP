import React, { useState } from 'react';
import { Upload, Image as ImageIcon, AlertCircle, CheckCircle, XCircle } from 'lucide-react';
import './ImageComparisonPanel.css';

const ImageComparisonPanel = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [location, setLocation] = useState({ lat: 19.0760, lon: 72.8777 });
  const [zoom, setZoom] = useState(15);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [referenceImage, setReferenceImage] = useState(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
    }
  };

  const fetchReferenceImage = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/here/reference-image?lat=${location.lat}&lon=${location.lon}&zoom=${zoom}&map_type=satellite.day`
      );
      const data = await response.json();
      
      if (data.success) {
        setReferenceImage(`data:image/png;base64,${data.image_base64}`);
      }
    } catch (error) {
      console.error('Failed to fetch reference image:', error);
    }
  };

  const handleCompare = async () => {
    if (!selectedFile) {
      alert('Please select an image first');
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      // First, get reference image
      await fetchReferenceImage();

      // Then compare
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('lat', location.lat);
      formData.append('lon', location.lon);
      formData.append('zoom', zoom);

      const response = await fetch(
        `http://localhost:8000/api/here/compare-disaster-image?lat=${location.lat}&lon=${location.lon}&zoom=${zoom}`,
        {
          method: 'POST',
          body: formData
        }
      );

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Comparison failed:', error);
      setResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (percentage) => {
    if (percentage > 50) return '#ef4444'; // red
    if (percentage > 30) return '#f59e0b'; // orange
    if (percentage > 15) return '#eab308'; // yellow
    return '#10b981'; // green
  };

  const getSeverityLabel = (percentage) => {
    if (percentage > 50) return 'CRITICAL';
    if (percentage > 30) return 'HIGH';
    if (percentage > 15) return 'MEDIUM';
    return 'LOW';
  };

  return (
    <div className="image-comparison-panel">
      <div className="panel-header">
        <ImageIcon size={24} />
        <h2>HERE Cartographic Image Comparison</h2>
      </div>

      <div className="comparison-content">
        {/* Upload Section */}
        <div className="upload-section">
          <h3>1. Upload Disaster Image</h3>
          <div className="upload-area">
            <input
              type="file"
              id="disaster-image"
              accept="image/*"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />
            <label htmlFor="disaster-image" className="upload-button">
              <Upload size={20} />
              {selectedFile ? selectedFile.name : 'Choose Image'}
            </label>
          </div>

          {previewUrl && (
            <div className="image-preview">
              <img src={previewUrl} alt="Disaster preview" />
              <p className="preview-label">Disaster Image</p>
            </div>
          )}
        </div>

        {/* Location Section */}
        <div className="location-section">
          <h3>2. Set Location</h3>
          <div className="location-inputs">
            <div className="input-group">
              <label>Latitude:</label>
              <input
                type="number"
                step="0.0001"
                value={location.lat}
                onChange={(e) => setLocation({ ...location, lat: parseFloat(e.target.value) })}
              />
            </div>
            <div className="input-group">
              <label>Longitude:</label>
              <input
                type="number"
                step="0.0001"
                value={location.lon}
                onChange={(e) => setLocation({ ...location, lon: parseFloat(e.target.value) })}
              />
            </div>
            <div className="input-group">
              <label>Zoom:</label>
              <input
                type="number"
                min="1"
                max="20"
                value={zoom}
                onChange={(e) => setZoom(parseInt(e.target.value))}
              />
            </div>
          </div>
          <div className="preset-locations">
            <button onClick={() => setLocation({ lat: 19.0760, lon: 72.8777 })}>Mumbai</button>
            <button onClick={() => setLocation({ lat: 28.6139, lon: 77.2090 })}>Delhi</button>
            <button onClick={() => setLocation({ lat: 12.9716, lon: 77.5946 })}>Bangalore</button>
          </div>
        </div>

        {/* Compare Button */}
        <div className="compare-section">
          <button
            className="compare-button"
            onClick={handleCompare}
            disabled={!selectedFile || loading}
          >
            {loading ? 'Comparing...' : 'Compare with HERE Reference'}
          </button>
        </div>

        {/* Results Section */}
        {result && (
          <div className="results-section">
            <h3>3. Comparison Results</h3>
            
            {result.error ? (
              <div className="error-message">
                <XCircle size={20} />
                <span>Error: {result.error}</span>
              </div>
            ) : (
              <>
                {/* Images Side by Side */}
                <div className="images-comparison">
                  <div className="comparison-image">
                    <img src={previewUrl} alt="Disaster" />
                    <p>Disaster Image</p>
                  </div>
                  <div className="comparison-arrow">→</div>
                  <div className="comparison-image">
                    {referenceImage ? (
                      <img src={referenceImage} alt="HERE Reference" />
                    ) : (
                      <div className="loading-placeholder">Loading reference...</div>
                    )}
                    <p>HERE Reference</p>
                  </div>
                </div>

                {/* Change Metrics */}
                <div className="change-metrics">
                  <div
                    className="change-percentage"
                    style={{ borderColor: getSeverityColor(result.change_percentage) }}
                  >
                    <div className="percentage-value" style={{ color: getSeverityColor(result.change_percentage) }}>
                      {result.change_percentage}%
                    </div>
                    <div className="percentage-label">
                      {getSeverityLabel(result.change_percentage)} CHANGE
                    </div>
                  </div>

                  {/* Detected Changes */}
                  <div className="detected-changes">
                    <h4>Detected Changes:</h4>
                    <div className="change-items">
                      <div className={`change-item ${result.changes_detected?.water_increase ? 'detected' : ''}`}>
                        {result.changes_detected?.water_increase ? <CheckCircle size={16} /> : <XCircle size={16} />}
                        <span>Water Increase (Flooding)</span>
                      </div>
                      <div className={`change-item ${result.changes_detected?.vegetation_loss ? 'detected' : ''}`}>
                        {result.changes_detected?.vegetation_loss ? <CheckCircle size={16} /> : <XCircle size={16} />}
                        <span>Vegetation Loss</span>
                      </div>
                      <div className={`change-item ${result.changes_detected?.infrastructure_damage ? 'detected' : ''}`}>
                        {result.changes_detected?.infrastructure_damage ? <CheckCircle size={16} /> : <XCircle size={16} />}
                        <span>Infrastructure Damage</span>
                      </div>
                      <div className={`change-item ${result.changes_detected?.color_shift_detected ? 'detected' : ''}`}>
                        {result.changes_detected?.color_shift_detected ? <CheckCircle size={16} /> : <XCircle size={16} />}
                        <span>Color Shift Detected</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Analysis */}
                <div className="analysis-section">
                  <h4>AI Analysis:</h4>
                  <div className="analysis-text">
                    <AlertCircle size={18} />
                    <p>{result.analysis}</p>
                  </div>
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ImageComparisonPanel;
