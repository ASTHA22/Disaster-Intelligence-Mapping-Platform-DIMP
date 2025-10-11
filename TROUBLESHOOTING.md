# Troubleshooting Guide

## Common Issues and Solutions

### Backend Issues

#### 1. Port 8000 already in use

**Error**: `Address already in use`

**Solution**:
```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn main:app --port 8001
```

#### 2. Module not found errors

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. PyTorch installation issues

**Error**: Large download or installation failure

**Solution**:
```bash
# Install CPU-only version (smaller, faster)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

#### 4. Transformers model download slow

**Error**: Slow download of DistilBERT model

**Solution**: First run will download ~250MB model. Subsequent runs will use cached version. Be patient on first run.

### Frontend Issues

#### 1. npm install fails

**Error**: Various npm errors

**Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 2. Port 3000 already in use

**Error**: `Port 3000 is already in use`

**Solution**:
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or run on different port
PORT=3001 npm start
```

#### 3. Map not loading

**Error**: Blank map or "Map failed to load"

**Solution**:
- Mapbox token in the code is a placeholder
- Map will show base tiles but some features may be limited
- Tomorrow: Replace with HERE Maps using your API key

#### 4. CORS errors

**Error**: `Access to fetch blocked by CORS policy`

**Solution**:
- Make sure backend is running on port 8000
- Check `REACT_APP_API_URL` in `.env`
- Backend already has CORS enabled for all origins

### Integration Issues

#### 1. Frontend can't connect to backend

**Symptoms**: No data loading, API errors in console

**Solution**:
```bash
# Verify backend is running
curl http://localhost:8000/

# Check frontend .env file
cat frontend/.env
# Should have: REACT_APP_API_URL=http://localhost:8000

# Restart both services
```

#### 2. Data not appearing on map

**Symptoms**: Map loads but no markers

**Solution**:
- Open browser console (F12)
- Check for JavaScript errors
- Verify API responses: `http://localhost:8000/api/disaster-zones`
- Check layer toggles are enabled

### Performance Issues

#### 1. Backend slow to start

**Cause**: Loading PyTorch models on first run

**Solution**: Normal behavior. First request will be slow (~5-10 seconds) while models load. Subsequent requests are fast.

#### 2. High memory usage

**Cause**: PyTorch models in memory

**Solution**:
```bash
# Use CPU-only version to reduce memory
# Already configured in damage_detector.py

# Or increase system swap space
```

### Development Issues

#### 1. Changes not reflecting

**Frontend**:
```bash
# Hard refresh browser
Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

# Clear React cache
rm -rf node_modules/.cache
npm start
```

**Backend**:
```bash
# FastAPI auto-reloads, but if not:
# Stop (Ctrl+C) and restart
python main.py
```

#### 2. ESLint warnings

**Solution**: Warnings are okay for MVP. To disable:
```javascript
// Add to top of file
/* eslint-disable */
```

### HERE Maps Integration (Tomorrow)

#### 1. HERE API key not working

**Checklist**:
- [ ] API key is for JavaScript (frontend) or REST (backend)
- [ ] Project is active on HERE Developer Portal
- [ ] API key has correct permissions
- [ ] No typos in `.env` file
- [ ] Restarted both frontend and backend after adding key

#### 2. HERE map not loading

**Solution**:
```javascript
// Check browser console for errors
// Verify API key in network tab
// Make sure you're using the correct HERE Maps SDK version
```

## Testing Checklist

Before demo, verify:

- [ ] Backend starts without errors: `python main.py`
- [ ] Frontend starts without errors: `npm start`
- [ ] Can access `http://localhost:8000/docs`
- [ ] Can access `http://localhost:3000`
- [ ] Map displays with markers
- [ ] Can toggle layers on/off
- [ ] Can click markers and see popups
- [ ] Social feed shows posts
- [ ] Alerts panel shows alerts
- [ ] Statistics display correctly
- [ ] Can test API endpoints in `/docs`

## Quick Diagnostic Commands

```bash
# Check if backend is running
curl http://localhost:8000/

# Check if frontend is running
curl http://localhost:3000/

# Check Python version
python3 --version  # Should be 3.8+

# Check Node version
node --version     # Should be 16+

# Check installed packages (backend)
pip list

# Check installed packages (frontend)
npm list --depth=0

# View backend logs
# (Check terminal where python main.py is running)

# View frontend logs
# (Check browser console - F12)
```

## Getting Help

1. **Check logs**: Always check terminal output and browser console
2. **Read error messages**: They usually tell you exactly what's wrong
3. **Google the error**: Most errors have solutions online
4. **Check documentation**: README.md, HERE_INTEGRATION_GUIDE.md
5. **Simplify**: Comment out code to isolate the issue

## Emergency Fallback

If everything breaks before demo:

1. Use the API documentation: `http://localhost:8000/docs`
2. Show the code structure and architecture
3. Demonstrate individual components
4. Walk through the README and architecture diagrams
5. Discuss the technical approach and future plans

---

**Most issues are simple fixes. Stay calm and debug systematically! 🔧**
