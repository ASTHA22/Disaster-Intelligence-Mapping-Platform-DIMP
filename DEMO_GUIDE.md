# DIMP Demo Guide

## 🎯 How to Demo the Platform

This guide will help you present DIMP effectively for your hackathon.

## Quick Start

```bash
# Make start script executable
chmod +x start.sh

# Run the platform
./start.sh
```

Or manually:

```bash
# Terminal 1 - Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

# Terminal 2 - Frontend
cd frontend
npm install
npm start
```

## Demo Flow (10-15 minutes)

### 1. Introduction (2 min)
"DIMP is a real-time disaster intelligence platform that combines AI, satellite imagery, and social media to help emergency teams respond faster to disasters."

**Show**: Landing page with live statistics

### 2. Interactive Map (3 min)
"Our interactive map shows multiple data layers in real-time."

**Demonstrate**:
- Click layer toggles (Disaster Zones, Floods, Infrastructure, Displacement)
- Click on different markers to show popups
- Highlight color-coded severity levels
- Show the legend

**Key Points**:
- Red zones = Critical damage
- Blue zones = Flood areas
- Yellow/Orange = Infrastructure damage
- Purple = Population displacement

### 3. AI Damage Detection (2 min)
"Our AI analyzes satellite and drone imagery to detect damage automatically."

**Show**:
- Navigate to `http://localhost:8000/docs`
- Demonstrate `/api/analyze-image` endpoint
- Upload a sample disaster image
- Show the JSON response with damage score and recommendations

**Key Points**:
- Uses ResNet50 CNN for damage detection
- Provides damage score (0-1)
- Classifies severity (critical/high/medium/low)
- Generates actionable recommendations

### 4. Social Media Intelligence (3 min)
"We analyze social media posts to extract emergency information."

**Show**:
- Social Feed panel on the right
- Point out urgency levels (Critical/High/Medium)
- Show verified badges
- Click on a post to see details

**Demonstrate API**:
- Go to `/docs` → `/api/analyze-social-media`
- Try sample text: "Urgent! Building collapsed at Connaught Place. People trapped inside!"
- Show the analysis result with urgency, categories, and action items

**Key Points**:
- NLP-based urgency classification
- Automatic location extraction
- Priority scoring
- Actionable recommendations

### 5. Alert System (2 min)
"Real-time alerts help teams prioritize their response."

**Show**:
- Alert panel on the left
- Different severity levels
- Status tracking (active/responding/resolved)
- Timestamps

**Key Points**:
- Priority-based sorting
- Real-time updates
- Integration with map markers

### 6. Dashboard & Statistics (2 min)
"The dashboard provides comprehensive disaster metrics."

**Show**:
- Statistics cards (damaged buildings, flooded zones, displaced people)
- Header statistics (active operations, affected area)
- Live status indicator

### 7. HERE Maps Integration (1 min)
"The platform is ready for HERE API integration for advanced features."

**Show**:
- Map info box mentioning HERE integration
- Briefly mention: routing, isolines, geocoding
- Reference the `HERE_INTEGRATION_GUIDE.md`

**Key Points**:
- Evacuation route calculation
- Rescue team coverage areas (isolines)
- Enhanced geocoding for social media

## Key Talking Points

### Problem Statement
- Disasters require rapid, accurate information
- Multiple data sources (satellite, drone, social media) are siloed
- Manual analysis is too slow
- Emergency teams need actionable intelligence

### Solution
- **Multi-modal data fusion**: Combines imagery + text
- **AI-powered analysis**: Automated damage detection and NLP
- **Real-time visualization**: Interactive maps with multiple layers
- **Actionable insights**: Priority-based alerts and recommendations

### Technical Highlights
- **Backend**: FastAPI (high-performance Python)
- **AI**: PyTorch (ResNet50), Transformers (DistilBERT)
- **Frontend**: React with interactive mapping
- **Scalable**: Ready for real satellite/drone feeds
- **Extensible**: HERE API integration ready

### Impact
- Faster emergency response
- Better resource allocation
- Lives saved through rapid damage assessment
- Data-driven decision making

## Sample Demo Scenarios

### Scenario 1: Flood Emergency
1. Toggle "Flood Areas" layer
2. Click on a flood marker
3. Show water level, affected population
4. Point out evacuation requirements
5. Show related social media posts

### Scenario 2: Building Collapse
1. Click on a critical disaster zone
2. Show damage score and severity
3. Navigate to social feed
4. Find related urgent posts
5. Show alert panel with active response

### Scenario 3: Infrastructure Assessment
1. Toggle "Infrastructure" layer
2. Click on damaged infrastructure
3. Show damage level and operational status
4. Highlight repair time estimates
5. Discuss priority for restoration

## API Endpoints to Demonstrate

### Live in Browser
- `http://localhost:8000/` - API info
- `http://localhost:8000/docs` - Interactive API documentation
- `http://localhost:8000/api/disaster-zones` - JSON data
- `http://localhost:8000/api/statistics` - Dashboard stats

### Interactive Testing (Swagger UI)
1. `/api/analyze-social-media` - Paste emergency text
2. `/api/analyze-image` - Upload disaster image
3. `/api/alerts` - Get active alerts
4. `/api/social-feed` - Get analyzed posts

## Questions You Might Get

**Q: Is this using real satellite data?**
A: Currently using sample data for MVP. Ready to integrate with Sentinel, Maxar, or Planet APIs.

**Q: How accurate is the AI?**
A: Using pre-trained ResNet50 (90%+ accuracy on ImageNet). Can be fine-tuned on disaster-specific datasets for better performance.

**Q: Can this scale to real-time?**
A: Yes! FastAPI is async, can handle thousands of requests/sec. Can deploy on Kubernetes for horizontal scaling.

**Q: What about HERE Maps?**
A: Platform is architected for HERE integration. Will add routing, isolines, and enhanced geocoding tomorrow with API keys.

**Q: How do you handle false positives from social media?**
A: Multi-step verification: NLP urgency scoring, verified badge system, and cross-referencing with satellite data.

**Q: Can this work offline?**
A: Currently requires internet. Future enhancement: offline mode with cached maps and local AI models.

## Tips for a Great Demo

1. ✅ **Start with the map** - Visual impact
2. ✅ **Show real interactions** - Click things, toggle layers
3. ✅ **Demonstrate AI** - Upload image or analyze text live
4. ✅ **Tell a story** - Use scenarios (flood, collapse, etc.)
5. ✅ **Highlight scalability** - Mention production-ready architecture
6. ✅ **Show the code** - Briefly show clean API structure
7. ✅ **End with impact** - Lives saved, faster response

## Backup Plan

If something breaks:
1. Have screenshots ready
2. Use the API docs (`/docs`) as fallback
3. Show the code structure
4. Discuss architecture and future plans

## Post-Demo

Share:
- GitHub repository
- README.md with setup instructions
- HERE_INTEGRATION_GUIDE.md for tomorrow
- API documentation link

---

**Good luck with your demo! 🚀**
