# Demo: HERE Cartographic Image Comparison Feature

## What We Built

A complete **image comparison system** that uses HERE's cartographic reference images to detect disaster changes.

## How to Demo This Feature

### Step 1: Start the Application

```bash
# Terminal 1: Backend
cd backend
python3 -m uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm start
```

### Step 2: Access the Image Comparison Panel

1. Open http://localhost:3000
2. Scroll down in the left panel
3. Find **"HERE Cartographic Image Comparison"** panel (between Rescue Coverage and Dashboard)

### Step 3: Upload a Disaster Image

**Option A: Use Sample Images**
- Download sample disaster images from:
  - Flood images: Search "Mumbai flood aerial" on Google Images
  - Building damage: Search "earthquake damage satellite"
  - Save any disaster image to your computer

**Option B: Create Test Image**
- Take any aerial/satellite photo
- Use photo editing to simulate flooding (darken areas)
- Or use building damage photos

### Step 4: Set Location

The panel has three preset locations:
- **Mumbai**: 19.0760, 72.8777
- **Delhi**: 28.6139, 77.2090
- **Bangalore**: 12.9716, 77.5946

Or manually enter coordinates.

### Step 5: Compare

1. Click **"Compare with HERE Reference"**
2. System will:
   - Fetch HERE satellite reference image for that location
   - Compare your disaster image with the reference
   - Show both images side-by-side
   - Display change percentage
   - Highlight detected changes

### Step 6: View Results

The panel shows:

**Change Percentage**
- 🟢 LOW (<15%): Minor changes
- 🟡 MEDIUM (15-30%): Moderate changes
- 🟠 HIGH (30-50%): Significant changes
- 🔴 CRITICAL (>50%): Major changes

**Detected Changes**
- ✅ Water Increase (Flooding)
- ✅ Vegetation Loss
- ✅ Infrastructure Damage
- ✅ Color Shift Detected

**AI Analysis**
- Human-readable explanation of what changed

## Example Demo Flow

### Scenario: Mumbai Flood Detection

1. **Upload**: Flood image from Mumbai monsoon
2. **Location**: Set to Mumbai (19.0760, 72.8777)
3. **Zoom**: 15 (street level detail)
4. **Click**: "Compare with HERE Reference"

**Expected Result:**
```
Change Percentage: 42.5%
Severity: HIGH

Detected Changes:
✅ Water Increase (Flooding) - DETECTED
❌ Vegetation Loss - NOT DETECTED
✅ Infrastructure Damage - DETECTED
✅ Color Shift Detected - DETECTED

AI Analysis:
"HIGH: Significant changes detected (>30% pixel difference) | 
Possible flooding detected (increased dark/water areas) | 
Structural changes detected (texture/edge differences)"
```

## Technical Features Demonstrated

### 1. HERE Map Image API Integration
- Real-time fetching of cartographic reference images
- Multiple map types (satellite, terrain, normal, hybrid)
- Global coverage

### 2. AI Change Detection
- Pixel-level comparison
- Flood detection (water increase)
- Vegetation analysis (green channel)
- Infrastructure damage (edge/texture)
- Color shift detection

### 3. Visual Comparison
- Side-by-side image display
- Before (HERE reference) vs After (disaster)
- Color-coded severity indicators
- Detailed change breakdown

## API Endpoints Used

```javascript
// Get HERE reference image
GET /api/here/reference-image
  ?lat=19.0760
  &lon=72.8777
  &zoom=15
  &map_type=satellite.day

// Compare disaster image
POST /api/here/compare-disaster-image
  ?lat=19.0760
  &lon=72.8777
  &zoom=15
Form Data: file=disaster_image.jpg
```

## Troubleshooting

### "429 Too Many Requests"
- HERE API has rate limits on free tier
- Wait a few minutes between requests
- Or upgrade to paid tier for production

### "Failed to fetch reference image"
- Check HERE_API_KEY in backend/.env
- Ensure backend is running on port 8000
- Check internet connection

### Images don't match
- Ensure coordinates are accurate
- Try adjusting zoom level (14-16 works best)
- Make sure disaster image is from same location

## Why This Matters

### For Disaster Management:
1. **Objective Validation**: Compare against authoritative HERE data
2. **Quantifiable Impact**: Get exact percentage of change
3. **Automated Detection**: No manual inspection needed
4. **Multiple Disaster Types**: Works for floods, fires, earthquakes, etc.

### For Hackathon Judges:
1. **Innovative Use of HERE API**: Beyond just routing/geocoding
2. **AI Integration**: Computer vision + cartographic data
3. **Practical Application**: Real disaster response use case
4. **Production Ready**: Full error handling, responsive UI

## Screenshots to Show

1. **Upload Interface**: Clean, intuitive file upload
2. **Location Selection**: Preset cities + manual input
3. **Side-by-Side Comparison**: Before/After images
4. **Change Metrics**: Color-coded severity + detected changes
5. **AI Analysis**: Human-readable explanation

## Key Talking Points

1. **"We use HERE's cartographic library as a baseline"**
   - Authoritative, up-to-date reference images
   - Global coverage, multiple map types

2. **"AI detects specific change types"**
   - Not just "something changed"
   - Identifies flooding, damage, vegetation loss

3. **"Quantifiable results"**
   - Exact percentage of change
   - Severity levels (LOW/MEDIUM/HIGH/CRITICAL)

4. **"Production-ready implementation"**
   - Full error handling
   - Responsive design
   - API rate limiting awareness

## Future Enhancements (Mention if Asked)

- Real-time change detection with streaming
- Multi-temporal analysis (track changes over time)
- Machine learning for better classification
- Automated alerts when thresholds exceeded
- Integration with drone feeds
- Historical comparison (before/during/after)

---

**Status**: ✅ Fully implemented and ready to demo  
**Based on**: Mentor feedback on HERE cartographic library  
**Commit**: b5cba04
