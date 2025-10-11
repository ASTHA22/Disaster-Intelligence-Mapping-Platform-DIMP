# Free Disaster Image Links for Testing

## Quick Test Images (Right-click → Save As)

### 1. Mumbai Flood Images

**Source: Unsplash (Free to use)**

- **Flood Scene 1**: https://images.unsplash.com/photo-1547683905-f686c993aae5?w=800
  - Location: Mumbai (19.0760, 72.8777)
  - Good for: Flood detection testing

- **Flood Scene 2**: https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=800
  - Location: Generic flood
  - Good for: Water increase detection

- **Urban Flooding**: https://images.unsplash.com/photo-1611348524140-53c9a25263d6?w=800
  - Location: Urban area
  - Good for: Infrastructure + flood combo

### 2. Building Damage

- **Damaged Building**: https://images.unsplash.com/photo-1564507592333-c60657eea523?w=800
  - Location: Delhi (28.6139, 77.2090)
  - Good for: Infrastructure damage detection

- **Collapsed Structure**: https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=800
  - Location: Any city
  - Good for: Severe damage detection

### 3. Natural Disasters

- **Wildfire**: https://images.unsplash.com/photo-1603048588665-791ca8aea617?w=800
  - Location: California (37.7749, -122.4194)
  - Good for: Vegetation loss detection

- **Hurricane Damage**: https://images.unsplash.com/photo-1527482797697-8795b05a13fe?w=800
  - Location: Miami (25.7617, -80.1918)
  - Good for: Combined damage detection

### 4. Aerial/Satellite Views

- **Aerial Flood**: https://images.unsplash.com/photo-1611348524140-53c9a25263d6?w=800
  - Good for: Comparison with HERE satellite

- **Urban Aerial**: https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=800
  - Good for: Baseline comparison

## NASA Earth Observatory (Public Domain)

### Real Disaster Images

1. **2024 Floods**:
   - https://eoimages.gsfc.nasa.gov/images/imagerecords/152000/152000/pakistan_floods_2022.jpg
   - Pakistan floods (real satellite imagery)

2. **Wildfires**:
   - https://eoimages.gsfc.nasa.gov/images/imagerecords/151000/151000/california_fires_2020.jpg
   - California wildfires (real satellite)

3. **Hurricanes**:
   - https://eoimages.gsfc.nasa.gov/images/imagerecords/150000/150000/hurricane_ida_2021.jpg
   - Hurricane Ida (real satellite)

## How to Use These Images

### Method 1: Download and Test via Frontend

1. Right-click on any link above
2. Select "Save Image As..."
3. Save to your computer
4. Open http://localhost:3000
5. Scroll to "HERE Cartographic Image Comparison" panel
6. Click "Choose Image" and select downloaded image
7. Set location coordinates
8. Click "Compare with HERE Reference"

### Method 2: Test via cURL

```bash
# Download image first
curl -o flood.jpg "https://images.unsplash.com/photo-1547683905-f686c993aae5?w=800"

# Test comparison
curl -X POST 'http://localhost:8000/api/here/compare-disaster-image?lat=19.0760&lon=72.8777&zoom=15' \
  -F 'file=@flood.jpg'
```

### Method 3: Use Download Script

```bash
cd backend
python3 download_test_images.py
# This downloads all images to test_images/ folder
```

## Recommended Test Scenarios

### Scenario 1: Mumbai Flood Detection
```
Image: https://images.unsplash.com/photo-1547683905-f686c993aae5?w=800
Location: Mumbai (19.0760, 72.8777)
Zoom: 15
Expected: Water increase detected, infrastructure damage
```

### Scenario 2: Building Damage Assessment
```
Image: https://images.unsplash.com/photo-1564507592333-c60657eea523?w=800
Location: Delhi (28.6139, 77.2090)
Zoom: 15
Expected: Infrastructure damage detected, high change percentage
```

### Scenario 3: Wildfire Impact
```
Image: https://images.unsplash.com/photo-1603048588665-791ca8aea617?w=800
Location: California (37.7749, -122.4194)
Zoom: 14
Expected: Vegetation loss, color shift detected
```

## Creating Your Own Test Images

### Option 1: Screenshot Google Earth

1. Open Google Earth
2. Navigate to disaster location
3. Take screenshot
4. Use in comparison

### Option 2: Use Sample Disaster Photos

Search on these free sites:
- **Unsplash**: https://unsplash.com/s/photos/disaster
- **Pexels**: https://www.pexels.com/search/disaster/
- **Pixabay**: https://pixabay.com/images/search/disaster/

### Option 3: Simulate Disaster

1. Take normal aerial photo
2. Use photo editor (GIMP, Photoshop)
3. Darken areas (simulate flooding)
4. Add cracks/damage (simulate earthquake)
5. Test comparison

## Best Images for Demo

### For Impressive Results:

1. **High Contrast Changes**:
   - Before: Clear, sunny day
   - After: Flooded, dark water
   - Result: 60%+ change detected

2. **Clear Infrastructure**:
   - Before: Intact buildings
   - After: Collapsed/damaged
   - Result: Infrastructure damage detected

3. **Vegetation Changes**:
   - Before: Green forest
   - After: Burned/brown
   - Result: Vegetation loss detected

## Quick Download Commands

```bash
# Create test directory
mkdir -p test_images
cd test_images

# Download flood image
curl -o mumbai_flood.jpg "https://images.unsplash.com/photo-1547683905-f686c993aae5?w=800"

# Download building damage
curl -o building_damage.jpg "https://images.unsplash.com/photo-1564507592333-c60657eea523?w=800"

# Download wildfire
curl -o wildfire.jpg "https://images.unsplash.com/photo-1603048588665-791ca8aea617?w=800"

# Download hurricane damage
curl -o hurricane.jpg "https://images.unsplash.com/photo-1527482797697-8795b05a13fe?w=800"

echo "✅ Downloaded 4 test images!"
```

## Testing Tips

1. **Use appropriate zoom levels**:
   - City-wide: zoom 12-13
   - Neighborhood: zoom 14-15
   - Street-level: zoom 16-17

2. **Match image type**:
   - Aerial photo → Use satellite.day map type
   - Ground photo → Use normal.day map type

3. **Set accurate coordinates**:
   - Use Google Maps to find exact location
   - Right-click → "What's here?" → Copy coordinates

4. **Wait between tests**:
   - Rate limit: 2 requests/second
   - Wait 1-2 seconds between comparisons

## Example Test Session

```bash
# 1. Download test image
curl -o test.jpg "https://images.unsplash.com/photo-1547683905-f686c993aae5?w=800"

# 2. Test comparison
curl -X POST 'http://localhost:8000/api/here/compare-disaster-image?lat=19.0760&lon=72.8777&zoom=15' \
  -F 'file=@test.jpg' | python3 -m json.tool

# 3. View results
# Should show:
# - change_percentage: 30-60%
# - water_increase: true
# - infrastructure_damage: possibly true
```

---

**All images are free to use!** Unsplash and NASA images are in the public domain or have permissive licenses.
