# DIMP - Disaster Intelligence Mapping Platform

![DIMP Banner](https://img.shields.io/badge/DIMP-Disaster%20Intelligence-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

**Live Site:** [Frontend (Vercel)](https://disaster-intelligence-mapping-platf.vercel.app/) | [Backend API (Render)](https://dimp-backend.onrender.com/docs)

**Live Demo:** [Live Demo](https://drive.google.com/file/d/1kdIjYttBiAIXG3q12RQ-1d0kN6LqAbPt/view?usp=drive_link) | **Presentation Deck:** [Presentation Deck](https://docs.google.com/presentation/d/1aAhc5AEBBet1HrA6ChlanV5N4FUKYmqm/edit?usp=drive_link&ouid=109901796126062648088&rtpof=true&sd=true)

### 🏆 Awards & Recognition
**Winner — HERE India Hackathon: Women in Tech 2025!**  

## Overview

**DIMP (Disaster Intelligence Mapping Platform)** is a real-time, AI-powered platform that ingests multi-modal data from satellite imagery, drone footage, and social media to provide actionable disaster intelligence for emergency management teams.

### Innovation Challenge Objective

To develop a real-time, AI-powered platform that ingests multi-modal data — satellite images, drone footage, and social media content — to:
- **Detect damaged infrastructure** - AI-powered damage detection with severity classification
- **Identify flood-affected zones** - Real-time flood zone mapping and tracking
- **Track population displacement** - Displacement zones with shelter capacity tracking
- **Generate actionable, real-time disaster maps** - Interactive multi-layer maps for emergency teams

### Key Features (All Implemented ✅)

#### Core Intelligence
- **AI-Powered Damage Detection** - ResNet50 model for infrastructure damage assessment
- **Flood Detection** - HSV color analysis + edge detection for water identification
- **Social Media Analysis** - DistilBERT sentiment analysis with urgency classification
- **Real-Time Data Sync** - 30-second polling with seamless UI updates

#### HERE Maps Integration (Full Suite)
- **Routing API** - Evacuation route calculation with turn-by-turn directions
- **Isoline API** - Rescue coverage zones (5/10/15-minute response areas)
- **Geocoding API** - Address to coordinates conversion
- **Map Image API** - Cartographic reference images for disaster comparison
- **Image Comparison** - AI-powered change detection using HERE satellite imagery

#### Interactive Mapping
- **Multi-Layer Visualization** - Disaster zones, floods, infrastructure, displacement
- **Map Legend** - Clear indicators for all map elements
- **Route Planning** - Calculate optimal evacuation paths
- **Coverage Analysis** - Visualize rescue team response areas
- **Real-Time Updates** - Live disaster zone tracking

#### Analytics & Reporting
- **Dynamic Statistics** - Real-time calculation from actual data
- **Priority Alerts** - Critical/High/Medium severity notifications
- **Export Functionality** - PDF, JSON, CSV report generation
- **Social Feed** - Verified posts with urgency classification

#### User Experience
- **Dark/Light Mode** - Theme switcher for different conditions
- **Responsive Design** - Works on desktop, tablet, mobile
- **Professional UI** - Clean, modern interface with HERE branding

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│                     DIMP Platform                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Frontend   │  │   Backend    │  │  AI Modules  │      │
│  │    React     │◄─┤   FastAPI    │◄─┤  PyTorch/NLP │      │
│  │  Mapbox/HERE │  │   Python     │  │  Transformers│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Data Sources                            │  │
│  │  • Satellite Images  • Drone Feeds  • Social Media   │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **npm or yarn**

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

The backend will start at `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will start at `http://localhost:3000`

## HERE Maps Integration

The platform includes **full HERE API integration** with backend services ready for production use, including cartographic reference images for disaster comparison.

### Current Implementation

The backend provides complete HERE API wrappers with the following services:

**Core Services** (`backend/here_service.py`):
- Routing & Navigation
- Isoline (Coverage Zones)
- Geocoding & Reverse Geocoding

**Image Services** (`backend/here_image_service.py`):
- Cartographic Reference Images
- Satellite Imagery
- Disaster Image Comparison
- Change Detection

#### 1. Geocoding & Reverse Geocoding
```python
# Convert address to coordinates
POST /api/here/geocode
{
  "address": "Mumbai, Maharashtra, India"
}

# Convert coordinates to address
GET /api/here/reverse-geocode?lat=19.0760&lon=72.8777
```

#### 2. Routing & Evacuation Routes
```python
# Calculate route between two points
POST /api/here/route
{
  "origin_lat": 19.0760,
  "origin_lon": 72.8777,
  "destination_lat": 19.1136,
  "destination_lon": 72.8697,
  "transport_mode": "car"
}

# Calculate optimized evacuation route
POST /api/here/evacuation-route
{
  "origin_lat": 19.0760,  # Disaster zone
  "origin_lon": 72.8777,
  "destination_lat": 19.1136,  # Shelter
  "destination_lon": 72.8697
}
```

#### 3. Isoline (Reachable Areas)
```python
# Calculate areas reachable within time limits
POST /api/here/isoline
{
  "origin_lat": 19.0760,
  "origin_lon": 72.8777,
  "range_minutes": [5, 10, 15],
  "transport_mode": "car"
}

# Get rescue team coverage area
GET /api/here/rescue-coverage?lat=19.0760&lon=72.8777
```

### Setup HERE API Credentials

1. **Get API Key**:
   - Go to [HERE Developer Portal](https://developer.here.com/)
   - Sign up / Log in
   - Create a new project
   - Generate API Key

2. **Add to Backend**:
```bash
# In backend directory
cp .env.example .env

# Edit .env and add your HERE API key
HERE_API_KEY=your_actual_here_api_key
```

3. **Restart Backend**:
```bash
python main.py
```

### HERE Services in DIMP

| Service | Endpoint | Use Case |
|---------|----------|----------|
| **Geocoding** | `/api/here/geocode` | Convert disaster location names to coordinates |
| **Reverse Geocoding** | `/api/here/reverse-geocode` | Get address from map clicks |
| **Routing** | `/api/here/route` | Calculate evacuation routes |
| **Evacuation Routes** | `/api/here/evacuation-route` | Optimized routes avoiding disaster zones |
| **Isoline** | `/api/here/isoline` | Show reachable areas for rescue teams |
| **Rescue Coverage** | `/api/here/rescue-coverage` | Visualize 5/10/15-minute response zones |
| **Reference Images** | `/api/here/reference-image` | Get cartographic reference images (satellite/terrain) |
| **Image Comparison** | `/api/here/compare-disaster-image` | Compare disaster images with HERE reference maps |
| **Area Comparison** | `/api/here/area-comparison` | Get reference images for before/after analysis |

#### NEW: Cartographic Image Comparison

**Use Case:** Compare disaster images (flood, damage) against HERE's cartographic reference images to detect changes.

```python
# Get HERE satellite reference image
GET /api/here/reference-image?lat=19.0760&lon=72.8777&zoom=15&map_type=satellite.day

# Compare disaster image with reference
POST /api/here/compare-disaster-image
Form Data:
  - file: disaster_image.jpg
  - lat: 19.0760
  - lon: 72.8777
  - zoom: 15

Response:
{
  "success": true,
  "change_percentage": 42.5,
  "changes_detected": {
    "water_increase": true,
    "vegetation_loss": false,
    "infrastructure_damage": true
  },
  "analysis": "HIGH: Significant changes detected | Possible flooding detected | Structural changes detected"
}
```

**How it works:**
1. Upload disaster image (satellite/drone photo)
2. System fetches HERE cartographic reference for same location
3. AI compares images pixel-by-pixel
4. Detects: flooding, vegetation loss, infrastructure damage
5. Returns change percentage and detailed analysis

### Frontend Integration

The frontend uses **Leaflet.js with Carto tiles** for base mapping and **HERE API services** for routing and analysis:

```javascript
// Map Visualization: Leaflet.js (free, no API key required)
<TileLayer
  url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
/>

// - Routing & Analysis: HERE API (backend integration)
// - Evacuation route calculation
// - Rescue coverage zones (5/10/15 min isolines)
// - Geocoding and reverse geocoding
```

**Current Implementation:**
- **Base Maps**: Leaflet.js with Carto tiles (no API key needed)
- **Routing Services**: HERE API via backend (API key in backend/.env)
- **Coverage Zones**: HERE Isoline API with flexible polyline decoding
- **Route Visualization**: Polyline rendering on Leaflet maps

## API Endpoints

### Disaster Data

- `GET /api/disaster-zones` - Get all disaster zones
- `GET /api/flood-areas` - Get flood-affected areas
- `GET /api/infrastructure-damage` - Get damaged infrastructure
- `GET /api/population-displacement` - Get displacement data
- `GET /api/alerts` - Get real-time alerts
- `GET /api/social-feed` - Get analyzed social media posts
- `GET /api/statistics` - Get disaster statistics

### AI Analysis

- `POST /api/analyze-image` - Upload and analyze satellite/drone image
- `POST /api/analyze-social-media` - Analyze social media post

### HERE Maps Services

- `POST /api/here/geocode` - Convert address to coordinates
- `GET /api/here/reverse-geocode` - Convert coordinates to address
- `POST /api/here/route` - Calculate route between two points
- `POST /api/here/evacuation-route` - Calculate optimized evacuation route
- `POST /api/here/isoline` - Calculate reachable areas (isolines)
- `GET /api/here/rescue-coverage` - Get rescue team coverage zones
- `GET /api/here-config` - Get HERE API configuration status

### Export

- `GET /api/export/pdf` - Export disaster report as PDF
- `GET /api/export/json` - Export all data as JSON
- `GET /api/export/csv` - Export disaster zones as CSV

## AI Models

### 1. Damage Detection
- **Model**: ResNet50 (pre-trained on ImageNet)
- **Task**: Semantic segmentation for damage assessment
- **Output**: Damage score (0-1), severity level, recommendations

### 2. Flood Detection
- **Method**: HSV color space analysis + edge detection
- **Task**: Identify water-covered areas
- **Output**: Boolean flood detection, water percentage

### 3. Social Media Analysis
- **Model**: DistilBERT (sentiment analysis)
- **Task**: Urgency classification, entity extraction, location inference
- **Output**: Urgency level, categories, priority score, action items

## Technology Stack

### Implementation vs Requirements

| Component | Required | Implemented | Status |
|-----------|----------|-------------|--------|
| **Data Ingestion** | AWS S3, Kafka, OpenDroneMap, Planet API | Sample data generator + API endpoints | ✅ Demo Ready |
| **Processing** | PyTorch, TensorFlow, OpenCV, Hugging Face | PyTorch, OpenCV, Transformers (DistilBERT) | ✅ Implemented |
| **Geospatial** | GDAL, Rasterio, QGIS, Leaflet.js, Kepler.gl | Leaflet.js, GeoJSON, HERE API | ✅ Implemented |
| **Backend** | FastAPI, PostgreSQL + PostGIS | FastAPI, In-memory (ready for PostgreSQL) | ✅ Implemented |
| **Frontend** | React, Mapbox GL, Deck.gl | React, Leaflet.js (ready for HERE Maps) | ✅ Implemented |
| **Deployment** | Kubernetes, Docker, CI/CD | Docker-ready, deployment configs | ✅ Ready |

### Backend Stack
- **FastAPI** - High-performance async API framework
- **PyTorch** - Deep learning framework for damage detection
- **Transformers (Hugging Face)** - DistilBERT for NLP/social media analysis
- **OpenCV** - Computer vision processing for image analysis
- **NumPy/Pandas** - Data processing and manipulation
- **Requests** - HTTP client for external APIs
- **Python-dotenv** - Environment variable management

### Frontend Stack
- **React 18** - Modern UI framework with hooks
- **Leaflet.js** - Interactive map library (HERE-compatible)
- **Lucide React** - Modern icon library
- **Axios** - HTTP client for API calls
- **date-fns** - Date/time utilities
- **CSS Variables** - Theme system (dark/light mode)

### AI & Analytics Modules

| Task | Model/Method | Output | Status |
|------|--------------|--------|--------|
| **Damage Detection** | ResNet50 (PyTorch) | Damage score, severity, recommendations | ✅ |
| **Flood Detection** | HSV color analysis + edge detection | Flood zones, water percentage | ✅ |
| **Infrastructure Detection** | Object detection simulation | Damaged buildings, roads, bridges | ✅ |
| **Social Media Analysis** | DistilBERT (sentiment) | Urgency, categories, priority, actions | ✅ |
| **Entity Recognition** | NLP text processing | Locations, casualties, resources | ✅ |
| **Geolocation Inference** | Text-based location extraction | Coordinates from text | ✅ |

## Features Breakdown

### Dashboard
- Real-time statistics
- Layer controls (zones, floods, infrastructure, displacement)
- Damage metrics and counts

### Interactive Map
- Multi-layer visualization
- Color-coded severity indicators
- Clickable markers with detailed popups
- Legend and info panels

### Alert System
- Priority-based alerts
- Real-time notifications
- Status tracking (active/responding/resolved)

### Social Media Feed
- Urgency classification (critical/high/medium/low)
- Verified post badges
- Location extraction
- Timestamp tracking

## Data Sources

### Real-Time Data Integration
- **NASA EONET** - Real global disaster events (earthquakes, wildfires, storms)
- **USGS Earthquake API** - Live earthquake data
- **Social Media** - Real disaster-related posts (cached, refreshed every 60s)

### Simulation Data
- 50 Mumbai disaster zones with realistic coordinates
- 8 flood areas with water level tracking
- 20 infrastructure damage points
- 10 displacement zones with shelter capacity
- Real-time social media feed (sample + live data)
- 12 active alerts with priority classification

## Future Enhancements

- [ ] Real satellite API integration (Sentinel, Maxar)
- [ ] Live drone feed processing
- [ ] Enhanced social media API integration (Twitter/X API, Facebook Graph API)
- [ ] Predictive flood modeling with ML
- [ ] Weather data integration (OpenWeather, NOAA)
- [ ] Mobile app for field agents
- [ ] Offline mode support
- [ ] Multi-language support
- [ ] PostgreSQL database integration for persistent storage
- [ ] WebSocket real-time updates
- [ ] Advanced HERE Maps features (traffic, weather layers)

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Project Structure

```
Reskill_hackathon/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── damage_detector.py      # AI damage detection
│   ├── social_analyzer.py      # NLP social media analysis
│   ├── data_generator.py       # Sample data generation
│   ├── requirements.txt        # Python dependencies
│   └── .env.example           # Environment variables template
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── DisasterMap.js
│   │   │   ├── Dashboard.js
│   │   │   ├── AlertPanel.js
│   │   │   ├── SocialFeed.js
│   │   │   └── Header.js
│   │   ├── services/
│   │   │   └── api.js         # API client
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
└── README.md
```

## Contributing

This is an MVP built for a hackathon. Contributions welcome!

## License

MIT License - feel free to use for disaster relief efforts

## Support

For issues or questions, please open a GitHub issue.

## Deployment

The platform is deployed using modern cloud services for maximum reliability and scalability.

### Backend (Render)

**Platform:** [Render](https://render.com)  
**Service Type:** Web Service (Python)  
**Deployment:** Automatic from GitHub  

**Quick Deploy:**
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect to your GitHub repository
4. Configure:
   - **Build Command:** `cd backend && pip install -r requirements.txt`
   - **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variable:** `HERE_API_KEY=your_api_key`
4. Deploy automatically

**Documentation:** [Render Python Deployment Guide](https://render.com/docs/deploy-fastapi)

### Frontend (Vercel)

**Platform:** [Vercel](https://vercel.com)  
**Framework:** React  
**Deployment:** Automatic from GitHub  

**Quick Deploy:**
1. Push code to GitHub
2. Import project in Vercel
3. Configure:
   - **Framework Preset:** Create React App
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `build`
4. Deploy automatically

**Documentation:** [Vercel React Deployment Guide](https://vercel.com/docs/frameworks/react)

---

**Built for disaster relief and emergency management**

Powered by HERE Maps API | Real-time AI Analysis | Production Ready
