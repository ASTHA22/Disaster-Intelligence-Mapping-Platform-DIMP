# HERE Maps Integration Guide

## 🗺️ Integrating HERE APIs into DIMP

This guide will help you integrate HERE APIs tomorrow once you have your credentials.

## Step 1: Get HERE API Credentials

1. Visit [HERE Developer Portal](https://developer.here.com/)
2. Sign up for a free account
3. Create a new project: "DIMP - Disaster Intelligence Platform"
4. Generate an API Key (JavaScript API Key for frontend, REST API Key for backend)

## Step 2: Backend Integration

### Update Environment Variables

```bash
cd backend
cp .env.example .env
```

Edit `.env`:
```env
HERE_API_KEY=your_here_api_key_here
```

### Add HERE Geocoding Service

Create `backend/here_service.py`:

```python
import os
import requests
from typing import Dict, Optional

class HEREService:
    def __init__(self):
        self.api_key = os.getenv("HERE_API_KEY")
        self.geocode_url = "https://geocode.search.hereapi.com/v1"
        self.routing_url = "https://router.hereapi.com/v8"
        self.isoline_url = "https://isoline.router.hereapi.com/v8"
    
    def geocode(self, address: str) -> Optional[Dict]:
        """Convert address to coordinates"""
        params = {
            "q": address,
            "apiKey": self.api_key
        }
        response = requests.get(f"{self.geocode_url}/geocode", params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("items"):
                return data["items"][0]["position"]
        return None
    
    def reverse_geocode(self, lat: float, lon: float) -> Optional[Dict]:
        """Convert coordinates to address"""
        params = {
            "at": f"{lat},{lon}",
            "apiKey": self.api_key
        }
        response = requests.get(f"{self.geocode_url}/revgeocode", params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("items"):
                return data["items"][0]["address"]
        return None
    
    def calculate_route(self, origin: tuple, destination: tuple, 
                       transport_mode: str = "car") -> Optional[Dict]:
        """Calculate evacuation route"""
        params = {
            "transportMode": transport_mode,
            "origin": f"{origin[0]},{origin[1]}",
            "destination": f"{destination[0]},{destination[1]}",
            "return": "polyline,summary",
            "apiKey": self.api_key
        }
        response = requests.get(f"{self.routing_url}/routes", params=params)
        if response.status_code == 200:
            return response.json()
        return None
    
    def calculate_isoline(self, center: tuple, range_value: int, 
                         range_type: str = "time") -> Optional[Dict]:
        """Calculate reachable area for rescue teams"""
        params = {
            "transportMode": "car",
            "origin": f"{center[0]},{center[1]}",
            "range[type]": range_type,
            "range[values]": range_value,
            "apiKey": self.api_key
        }
        response = requests.get(f"{self.isoline_url}/isolines", params=params)
        if response.status_code == 200:
            return response.json()
        return None
```

### Update main.py

Add these endpoints to `backend/main.py`:

```python
from here_service import HEREService

here_service = HEREService()

@app.post("/api/geocode")
async def geocode_address(address: str):
    """Geocode an address using HERE"""
    result = here_service.geocode(address)
    return {"coordinates": result}

@app.get("/api/route")
async def calculate_route(
    origin_lat: float, 
    origin_lon: float,
    dest_lat: float,
    dest_lon: float
):
    """Calculate evacuation route"""
    route = here_service.calculate_route(
        (origin_lat, origin_lon),
        (dest_lat, dest_lon)
    )
    return route

@app.get("/api/rescue-coverage")
async def get_rescue_coverage(lat: float, lon: float, range_minutes: int = 30):
    """Get rescue team coverage area (isoline)"""
    isoline = here_service.calculate_isoline(
        (lat, lon),
        range_minutes * 60,  # Convert to seconds
        "time"
    )
    return isoline
```

## Step 3: Frontend Integration

### Install HERE Maps SDK

```bash
cd frontend
npm install @here/maps-api-for-javascript
```

### Create HERE Map Component

Create `frontend/src/components/HEREDisasterMap.js`:

```javascript
import React, { useEffect, useRef, useState } from 'react';
import H from '@here/maps-api-for-javascript';

const HEREDisasterMap = ({ zones, floodAreas, infrastructure, displacement }) => {
  const mapRef = useRef(null);
  const map = useRef(null);
  const platform = useRef(null);

  useEffect(() => {
    if (!mapRef.current) return;

    // Initialize HERE Platform
    platform.current = new H.service.Platform({
      apikey: process.env.REACT_APP_HERE_API_KEY
    });

    const defaultLayers = platform.current.createDefaultLayers();

    // Initialize map
    map.current = new H.Map(
      mapRef.current,
      defaultLayers.vector.normal.map,
      {
        center: { lat: 28.6139, lng: 77.2090 },
        zoom: 11,
        pixelRatio: window.devicePixelRatio || 1
      }
    );

    // Add map events
    const behavior = new H.mapevents.Behavior(
      new H.mapevents.MapEvents(map.current)
    );
    const ui = H.ui.UI.createDefault(map.current, defaultLayers);

    // Cleanup
    return () => {
      map.current.dispose();
    };
  }, []);

  useEffect(() => {
    if (!map.current) return;

    // Clear existing markers
    map.current.removeObjects(map.current.getObjects());

    // Add disaster zone markers
    zones.forEach(zone => {
      const marker = new H.map.Marker({
        lat: zone.coordinates.lat,
        lng: zone.coordinates.lon
      });
      
      marker.setData({
        type: 'zone',
        data: zone
      });

      marker.addEventListener('tap', (evt) => {
        const bubble = new H.ui.InfoBubble(evt.target.getGeometry(), {
          content: `
            <div style="padding: 10px;">
              <h3>${zone.name}</h3>
              <p>Severity: ${zone.severity}</p>
              <p>Damage: ${(zone.damage_score * 100).toFixed(0)}%</p>
            </div>
          `
        });
        ui.addBubble(bubble);
      });

      map.current.addObject(marker);
    });

    // Add flood areas, infrastructure, displacement similarly...
  }, [zones, floodAreas, infrastructure, displacement]);

  return <div ref={mapRef} style={{ width: '100%', height: '100%' }} />;
};

export default HEREDisasterMap;
```

### Update App.js

Replace the import in `frontend/src/App.js`:

```javascript
// Change from:
import DisasterMap from './components/DisasterMap';

// To:
import DisasterMap from './components/HEREDisasterMap';
```

### Add Environment Variable

Create `frontend/.env`:

```env
REACT_APP_HERE_API_KEY=your_here_api_key_here
REACT_APP_API_URL=http://localhost:8000
```

## Step 4: Advanced HERE Features

### Add Routing Visualization

```javascript
const displayRoute = async (origin, destination) => {
  const response = await fetch(
    `/api/route?origin_lat=${origin.lat}&origin_lon=${origin.lng}&dest_lat=${destination.lat}&dest_lon=${destination.lng}`
  );
  const routeData = await response.json();
  
  const lineString = H.geo.LineString.fromFlexiblePolyline(
    routeData.routes[0].sections[0].polyline
  );
  
  const routeLine = new H.map.Polyline(lineString, {
    style: { strokeColor: 'blue', lineWidth: 3 }
  });
  
  map.current.addObject(routeLine);
};
```

### Add Isoline (Rescue Coverage)

```javascript
const displayRescueCoverage = async (center, rangeMinutes) => {
  const response = await fetch(
    `/api/rescue-coverage?lat=${center.lat}&lon=${center.lng}&range_minutes=${rangeMinutes}`
  );
  const isolineData = await response.json();
  
  const polygon = new H.map.Polygon(
    H.geo.LineString.fromFlexiblePolyline(
      isolineData.isolines[0].polygons[0].outer
    ),
    {
      style: {
        fillColor: 'rgba(59, 130, 246, 0.3)',
        strokeColor: 'rgba(59, 130, 246, 0.8)',
        lineWidth: 2
      }
    }
  );
  
  map.current.addObject(polygon);
};
```

## Step 5: Testing

```bash
# Start backend
cd backend
python main.py

# Start frontend (in new terminal)
cd frontend
npm start
```

Visit `http://localhost:3000` and verify:
- ✅ HERE map loads correctly
- ✅ Disaster markers appear
- ✅ Geocoding works
- ✅ Routing displays
- ✅ Isolines render

## HERE API Services Summary

| Service | Endpoint | Use Case |
|---------|----------|----------|
| **Geocoding** | `/v1/geocode` | Convert addresses from social media to coordinates |
| **Reverse Geocoding** | `/v1/revgeocode` | Get location names from coordinates |
| **Routing** | `/v8/routes` | Calculate evacuation routes |
| **Isoline** | `/v8/isolines` | Show rescue team coverage areas |
| **Map Tiles** | Vector/Raster tiles | Base map visualization |

## Benefits of HERE Integration

1. ✅ **Better Geocoding** - More accurate location extraction from social media
2. ✅ **Evacuation Routes** - Calculate optimal escape paths
3. ✅ **Rescue Coverage** - Visualize which areas rescue teams can reach
4. ✅ **Offline Maps** - Download maps for disaster areas
5. ✅ **Traffic Data** - Real-time traffic for route planning

## Resources

- [HERE Developer Documentation](https://developer.here.com/documentation)
- [HERE Maps API for JavaScript](https://developer.here.com/documentation/maps/3.1.41.3/dev_guide/index.html)
- [HERE Routing API v8](https://developer.here.com/documentation/routing-api/8.16.0/dev_guide/index.html)
- [HERE Geocoding API](https://developer.here.com/documentation/geocoding-search-api/dev_guide/index.html)

---

**Ready to integrate tomorrow! 🚀**
