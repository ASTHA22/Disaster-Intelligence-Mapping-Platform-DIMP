# DIMP System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         DIMP Platform                            │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
        ┌───────▼────────┐            ┌────────▼────────┐
        │   Frontend      │            │    Backend      │
        │   React SPA     │◄──────────►│   FastAPI       │
        │   Port 3000     │   REST API │   Port 8000     │
        └────────┬────────┘            └────────┬────────┘
                 │                              │
                 │                              │
        ┌────────▼────────┐            ┌────────▼────────┐
        │  Map Rendering  │            │  AI Processing  │
        │  • Mapbox/HERE  │            │  • PyTorch      │
        │  • Markers      │            │  • Transformers │
        │  • Layers       │            │  • OpenCV       │
        └─────────────────┘            └────────┬────────┘
                                                │
                                       ┌────────▼────────┐
                                       │  Data Sources   │
                                       │  • Sample Data  │
                                       │  • Future: APIs │
                                       └─────────────────┘
```

## Component Breakdown

### Frontend Layer

```
frontend/
├── src/
│   ├── App.js                    # Main application component
│   ├── components/
│   │   ├── DisasterMap.js        # Interactive map with markers
│   │   ├── Dashboard.js          # Statistics and layer controls
│   │   ├── AlertPanel.js         # Real-time alerts display
│   │   ├── SocialFeed.js         # Social media intelligence
│   │   └── Header.js             # Top navigation and stats
│   └── services/
│       └── api.js                # API client for backend
```

**Technologies**:
- React 18 (UI framework)
- Mapbox GL (temporary mapping - ready for HERE)
- Axios (HTTP client)
- Lucide React (icons)
- date-fns (date formatting)

**Responsibilities**:
1. Render interactive disaster map
2. Display real-time data from backend
3. Handle user interactions (layer toggles, marker clicks)
4. Visualize statistics and alerts
5. Show social media intelligence feed

### Backend Layer

```
backend/
├── main.py                       # FastAPI application & routes
├── damage_detector.py            # AI damage detection
├── social_analyzer.py            # NLP social media analysis
└── data_generator.py             # Sample data generation
```

**Technologies**:
- FastAPI (async web framework)
- PyTorch + torchvision (deep learning)
- Transformers (NLP models)
- OpenCV (computer vision)
- NumPy (numerical computing)

**Responsibilities**:
1. Serve REST API endpoints
2. Process satellite/drone imagery
3. Analyze social media posts
4. Generate disaster intelligence
5. Provide data to frontend

## Data Flow

### 1. Disaster Zone Detection

```
Satellite Image Upload
        │
        ▼
┌─────────────────┐
│ damage_detector │
│   .py           │
└────────┬────────┘
         │
         ├──► ResNet50 CNN
         │    (Damage Classification)
         │
         ├──► OpenCV
         │    (Flood Detection)
         │
         └──► Edge Detection
              (Infrastructure Count)
         │
         ▼
┌─────────────────┐
│  JSON Response  │
│  • damage_score │
│  • severity     │
│  • flood_detect │
│  • recommend.   │
└─────────────────┘
```

### 2. Social Media Analysis

```
Social Media Post
        │
        ▼
┌─────────────────┐
│ social_analyzer │
│   .py           │
└────────┬────────┘
         │
         ├──► Keyword Matching
         │    (Urgency Classification)
         │
         ├──► DistilBERT
         │    (Sentiment Analysis)
         │
         ├──► Regex Patterns
         │    (Location Extraction)
         │
         └──► Entity Recognition
              (Numbers, Resources)
         │
         ▼
┌─────────────────┐
│  JSON Response  │
│  • urgency      │
│  • categories   │
│  • location     │
│  • priority     │
│  • actions      │
└─────────────────┘
```

### 3. Map Rendering

```
Frontend Load
        │
        ▼
API Calls (Parallel)
        │
        ├──► /api/disaster-zones
        ├──► /api/flood-areas
        ├──► /api/infrastructure-damage
        ├──► /api/population-displacement
        ├──► /api/alerts
        └──► /api/social-feed
        │
        ▼
Data Aggregation
        │
        ▼
Map Rendering
        │
        ├──► Disaster Markers (Red)
        ├──► Flood Markers (Blue)
        ├──► Infrastructure Markers (Orange)
        └──► Displacement Markers (Purple)
```

## API Architecture

### REST Endpoints

| Endpoint | Method | Purpose | Response |
|----------|--------|---------|----------|
| `/` | GET | API info | System status |
| `/api/disaster-zones` | GET | Get disaster zones | Array of zones |
| `/api/flood-areas` | GET | Get flood areas | Array of flood data |
| `/api/infrastructure-damage` | GET | Get damaged infrastructure | Array of infrastructure |
| `/api/population-displacement` | GET | Get displacement data | Array of displacement zones |
| `/api/alerts` | GET | Get active alerts | Array of alerts |
| `/api/social-feed` | GET | Get social posts | Array of analyzed posts |
| `/api/statistics` | GET | Get dashboard stats | Statistics object |
| `/api/analyze-image` | POST | Analyze disaster image | Damage analysis result |
| `/api/analyze-social-media` | POST | Analyze social post | NLP analysis result |
| `/api/here-config` | GET | Get HERE API config | Configuration object |

### Data Models

#### Disaster Zone
```json
{
  "id": "zone_1",
  "name": "Connaught Place",
  "coordinates": {
    "lat": 28.6139,
    "lon": 77.2090
  },
  "severity": "critical",
  "damage_score": 0.85,
  "affected_area_km2": 12.5,
  "last_updated": "2025-10-10T19:00:00"
}
```

#### Flood Area
```json
{
  "id": "flood_1",
  "location": "Karol Bagh",
  "coordinates": { "lat": 28.65, "lon": 77.19 },
  "water_level_m": 2.5,
  "affected_population": 3500,
  "status": "rising",
  "evacuation_required": true,
  "timestamp": "2025-10-10T19:00:00"
}
```

#### Social Media Post
```json
{
  "id": "post_1",
  "text": "Urgent! Building collapsed...",
  "location": "Connaught Place",
  "coordinates": { "lat": 28.61, "lon": 77.20 },
  "urgency": "critical",
  "verified": true,
  "timestamp": "2025-10-10T18:45:00",
  "source": "Twitter"
}
```

## AI/ML Architecture

### Damage Detection Pipeline

```
Input Image (RGB)
        │
        ▼
Preprocessing
├── Resize to 224x224
├── Normalize (ImageNet stats)
└── Convert to Tensor
        │
        ▼
ResNet50 Forward Pass
        │
        ▼
Feature Extraction
        │
        ▼
Damage Scoring
├── Softmax activation
├── Class probability aggregation
└── Threshold-based classification
        │
        ▼
Parallel Analysis
├── Flood Detection (HSV color analysis)
├── Infrastructure Detection (Edge detection)
└── Severity Calculation
        │
        ▼
Output: Damage Report
```

### NLP Pipeline

```
Input Text
        │
        ▼
Preprocessing
├── Lowercase conversion
├── Tokenization
└── Pattern matching
        │
        ▼
Parallel Analysis
├── Keyword Matching (Urgency)
├── DistilBERT (Sentiment)
├── Regex (Location)
└── Entity Extraction (Numbers, Resources)
        │
        ▼
Priority Scoring
├── Urgency weight
├── Category boost
└── Sentiment factor
        │
        ▼
Output: Intelligence Report
```

## Scalability Considerations

### Current MVP
- Single-server deployment
- In-memory data
- Sample datasets
- Synchronous processing

### Production Ready (Future)

```
┌──────────────────────────────────────────────────────────────┐
│                      Load Balancer                           │
└────────┬────────────────────────────────────┬────────────────┘
         │                                    │
    ┌────▼────┐                          ┌────▼────┐
    │ FastAPI │                          │ FastAPI │
    │ Instance│                          │ Instance│
    └────┬────┘                          └────┬────┘
         │                                    │
         └────────────┬───────────────────────┘
                      │
         ┌────────────▼────────────┐
         │   Message Queue (Kafka) │
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │   AI Workers (GPU)      │
         │   • Damage Detection    │
         │   • NLP Analysis        │
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │   Database (PostGIS)    │
         │   • Geospatial Data     │
         │   • Time-series Data    │
         └─────────────────────────┘
```

### Horizontal Scaling
- **Frontend**: CDN + multiple instances
- **Backend**: Kubernetes pods with auto-scaling
- **AI Processing**: GPU worker pool
- **Database**: PostGIS with read replicas
- **Caching**: Redis for hot data

## Security Architecture

### Current (MVP)
- CORS enabled for development
- No authentication (demo purposes)
- Public API endpoints

### Production (Future)
- JWT authentication
- API rate limiting
- HTTPS/TLS encryption
- Role-based access control (RBAC)
- Input validation and sanitization
- SQL injection prevention (using ORMs)

## Deployment Architecture

### Development (Current)
```
Local Machine
├── Backend: localhost:8000
└── Frontend: localhost:3000
```

### Production (Future)
```
Cloud Infrastructure (AWS/GCP/Azure)
├── Frontend: CloudFront/CDN
├── Backend: ECS/Kubernetes
├── Database: RDS/Cloud SQL
├── Storage: S3/Cloud Storage
├── AI Processing: GPU instances
└── Monitoring: CloudWatch/Stackdriver
```

## Integration Points

### HERE Maps (Tomorrow)
- **Geocoding**: Convert social media locations to coordinates
- **Routing**: Calculate evacuation routes
- **Isolines**: Show rescue team coverage
- **Map Tiles**: Base map visualization

### Future Integrations
- **Satellite APIs**: Sentinel, Maxar, Planet
- **Drone Platforms**: DJI, Skydio APIs
- **Social Media**: Twitter API, Facebook Graph API
- **Weather**: OpenWeatherMap, NOAA
- **Emergency Services**: National disaster management APIs

## Performance Metrics

### Target Performance
- **API Response Time**: < 200ms (data endpoints)
- **AI Processing**: < 5s (image analysis)
- **Map Load Time**: < 2s (initial render)
- **Real-time Updates**: 30s refresh interval
- **Concurrent Users**: 1000+ (with scaling)

### Monitoring
- Request latency
- Error rates
- AI model accuracy
- Data freshness
- User engagement

---

**This architecture is designed for rapid MVP development while maintaining production-ready scalability paths.**
