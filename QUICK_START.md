# ⚡ DIMP Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Option 1: Automated Start (Recommended)

```bash
cd /Users/astha/Desktop/Reskill_hackathon
./start.sh
```

That's it! The script will:
- ✅ Set up Python virtual environment
- ✅ Install all dependencies
- ✅ Start backend on http://localhost:8000
- ✅ Start frontend on http://localhost:3000

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm start
```

## 🎯 First Time Setup

### 1. Verify Prerequisites
```bash
python3 --version  # Should be 3.8+
node --version     # Should be 16+
npm --version      # Should be 8+
```

### 2. Install Dependencies

**Backend** (~2 minutes):
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend** (~3-5 minutes):
```bash
cd frontend
npm install
```

### 3. Start Services

**Backend:**
```bash
cd backend
source venv/bin/activate
python main.py
```

Wait for: `Uvicorn running on http://0.0.0.0:8000`

**Frontend:**
```bash
cd frontend
npm start
```

Wait for: `Compiled successfully!`

## 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main application UI |
| **Backend API** | http://localhost:8000 | REST API server |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **API JSON** | http://localhost:8000/openapi.json | OpenAPI specification |

## ✅ Verification Checklist

After starting, verify:

1. **Backend is running:**
   ```bash
   curl http://localhost:8000/
   # Should return: {"message": "DIMP API - Disaster Intelligence Mapping Platform", ...}
   ```

2. **Frontend is accessible:**
   - Open http://localhost:3000 in browser
   - Should see DIMP header and map

3. **API endpoints work:**
   - Visit http://localhost:8000/docs
   - Try GET `/api/disaster-zones`
   - Should return JSON with sample data

4. **Map displays correctly:**
   - See disaster zone markers (red)
   - See flood area markers (blue)
   - Click markers to see popups

## 🎮 Quick Demo

### 1. Explore the Map
- Toggle layers on/off in the left panel
- Click on different colored markers
- Read popup information

### 2. Check Social Feed
- Right panel shows analyzed social media posts
- Notice urgency levels (Critical/High/Medium)
- See verified badges

### 3. View Alerts
- Left panel bottom shows active alerts
- Different severity levels
- Real-time status

### 4. Test AI Analysis

**Via API Docs (http://localhost:8000/docs):**

1. Click on `POST /api/analyze-social-media`
2. Click "Try it out"
3. Paste this JSON:
   ```json
   {
     "text": "Urgent! Building collapsed at Connaught Place. People trapped inside!",
     "location": "Connaught Place"
   }
   ```
4. Click "Execute"
5. See AI analysis result with urgency, categories, and recommendations

## 📊 Sample API Calls

### Get Disaster Zones
```bash
curl http://localhost:8000/api/disaster-zones
```

### Get Statistics
```bash
curl http://localhost:8000/api/statistics
```

### Analyze Social Media
```bash
curl -X POST http://localhost:8000/api/analyze-social-media \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Severe flooding in Karol Bagh. Water level rising!",
    "location": "Karol Bagh"
  }'
```

## 🗺️ HERE Maps Setup (Tomorrow)

### 1. Get API Key
- Go to https://developer.here.com/
- Sign up / Log in
- Create project
- Generate API key

### 2. Add to Backend
```bash
cd backend
cp .env.example .env
# Edit .env and add: HERE_API_KEY=your_key_here
```

### 3. Add to Frontend
```bash
cd frontend
cp .env.example .env
# Edit .env and add: REACT_APP_HERE_API_KEY=your_key_here
```

### 4. Follow Integration Guide
See `HERE_INTEGRATION_GUIDE.md` for detailed steps

## 🔧 Common Commands

### Stop Services
- **Backend**: Press `Ctrl+C` in backend terminal
- **Frontend**: Press `Ctrl+C` in frontend terminal

### Restart Services
```bash
# Backend
cd backend
source venv/bin/activate
python main.py

# Frontend
cd frontend
npm start
```

### Clear Cache
```bash
# Backend
cd backend
rm -rf __pycache__

# Frontend
cd frontend
rm -rf node_modules/.cache
npm start
```

### Reinstall Dependencies
```bash
# Backend
cd backend
pip install -r requirements.txt --force-reinstall

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📁 Project Structure

```
Reskill_hackathon/
├── backend/              # Python FastAPI server
│   ├── main.py          # API routes
│   ├── damage_detector.py   # AI damage detection
│   ├── social_analyzer.py   # NLP analysis
│   └── data_generator.py    # Sample data
├── frontend/            # React application
│   ├── src/
│   │   ├── components/  # React components
│   │   └── services/    # API client
│   └── public/
├── README.md            # Main documentation
├── DEMO_GUIDE.md        # How to demo
├── HERE_INTEGRATION_GUIDE.md  # HERE Maps setup
├── ARCHITECTURE.md      # System architecture
├── TROUBLESHOOTING.md   # Problem solving
└── start.sh            # Automated startup script
```

## 🎯 Next Steps

1. ✅ Get the system running
2. ✅ Explore the UI and features
3. ✅ Test API endpoints
4. ✅ Read DEMO_GUIDE.md for presentation tips
5. ✅ Tomorrow: Add HERE API keys
6. ✅ Tomorrow: Follow HERE_INTEGRATION_GUIDE.md

## 🆘 Need Help?

### Issue: Port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### Issue: Module not found
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: npm errors
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### More Help
- See `TROUBLESHOOTING.md` for detailed solutions
- Check terminal output for error messages
- Open browser console (F12) for frontend errors

## 📞 Support Resources

- **README.md** - Complete documentation
- **DEMO_GUIDE.md** - Presentation guide
- **ARCHITECTURE.md** - Technical details
- **TROUBLESHOOTING.md** - Problem solving
- **HERE_INTEGRATION_GUIDE.md** - Maps integration

---

**You're ready to go! 🚀**

**Time to build: ~5 minutes**
**Time to demo: ~15 minutes**
**Time to impress: Priceless! 😎**
