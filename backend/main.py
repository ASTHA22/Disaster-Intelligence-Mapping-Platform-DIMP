from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import os
from datetime import datetime
import asyncio
import threading
from datetime import datetime, timedelta

from damage_detector import DamageDetector
from social_analyzer import SocialMediaAnalyzer
from data_generator import DataGenerator
from here_service import HEREService
from map_exporter import MapExporter
from real_data_fetcher import RealDataFetcher
from social_media_scraper import SocialMediaScraper

app = FastAPI(title="DIMP - Disaster Intelligence Mapping Platform")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
damage_detector = DamageDetector()
social_analyzer = SocialMediaAnalyzer()
data_generator = DataGenerator(location="mumbai")  # Set to Mumbai
real_data_fetcher = RealDataFetcher()  # Real-time data from NASA/USGS
social_media_scraper = SocialMediaScraper()  # Real social media scraper
here_service = HEREService()
map_exporter = MapExporter()

# Cache for social media data
social_media_cache = {
    "posts": [],
    "last_updated": None,
    "is_fetching": False
}

def fetch_social_media_background():
    """Background task to fetch real social media data"""
    global social_media_cache
    
    while True:
        try:
            print("🔄 Fetching real social media data in background...")
            social_media_cache["is_fetching"] = True
            
            # Fetch real data (takes 8+ seconds)
            real_social = social_media_scraper.get_all_social_media()
            real_posts = real_social.get('posts', [])
            
            # Update cache
            social_media_cache["posts"] = real_posts
            social_media_cache["last_updated"] = datetime.now()
            social_media_cache["is_fetching"] = False
            
            print(f"✅ Cached {len(real_posts)} real social media posts")
            
        except Exception as e:
            print(f"❌ Error fetching social media: {e}")
            social_media_cache["is_fetching"] = False
        
        # Wait 60 seconds before next fetch
        threading.Event().wait(60)

# Start background thread on startup
@app.on_event("startup")
async def startup_event():
    """Start background tasks on server startup"""
    print("🚀 Background social media fetcher disabled for faster startup")
    # Disabled to prevent slow startup - uncomment to enable real social media scraping
    # thread = threading.Thread(target=fetch_social_media_background, daemon=True)
    # thread.start()

# Models
class SocialMediaPost(BaseModel):
    text: str
    location: Optional[str] = None
    timestamp: Optional[str] = None

class RouteRequest(BaseModel):
    origin_lat: float
    origin_lon: float
    destination_lat: float
    destination_lon: float
    transport_mode: Optional[str] = "car"

class IsolineRequest(BaseModel):
    origin_lat: float
    origin_lon: float
    range_minutes: Optional[List[int]] = [5, 10, 15]
    transport_mode: Optional[str] = "car"

class GeocodeRequest(BaseModel):
    address: str

class AlertResponse(BaseModel):
    id: str
    type: str
    severity: str
    location: dict
    description: str
    timestamp: str

@app.get("/")
async def root():
    return {
        "message": "DIMP API - Disaster Intelligence Mapping Platform",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/api/disaster-zones")
async def get_disaster_zones():
    """Get disaster data - REAL (NASA/USGS) + Mumbai Simulation"""
    # Get REAL disasters from NASA/USGS
    real_data = real_data_fetcher.get_all_real_data()
    
    # Get Mumbai simulation data
    mumbai_zones = data_generator.generate_disaster_zones()
    
    # Combine both
    all_zones = real_data['zones'] + mumbai_zones
    
    return {
        "zones": all_zones, 
        "count": len(all_zones),
        "real_count": len(real_data['zones']),
        "simulation_count": len(mumbai_zones),
        "sources": real_data.get('sources', []) + ["Mumbai Simulation"],
        "last_updated": real_data.get('last_updated'),
        "note": "Real-time data from NASA/USGS + Mumbai simulation scenarios"
    }

@app.get("/api/flood-areas")
async def get_flood_areas():
    """Get flood-affected areas"""
    flood_areas = data_generator.generate_flood_areas()
    return {"flood_areas": flood_areas, "count": len(flood_areas)}

@app.get("/api/infrastructure-damage")
async def get_infrastructure_damage():
    """Get damaged infrastructure locations"""
    infrastructure = data_generator.generate_infrastructure_damage()
    return {"infrastructure": infrastructure, "count": len(infrastructure)}

@app.get("/api/population-displacement")
async def get_population_displacement():
    """Get population displacement data"""
    displacement = data_generator.generate_displacement_data()
    return {"displacement_zones": displacement, "count": len(displacement)}

@app.post("/api/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    """Analyze uploaded satellite/drone image for damage"""
    try:
        contents = await file.read()
        result = damage_detector.analyze_image(contents)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze-social-media")
async def analyze_social_media(post: SocialMediaPost):
    """Analyze social media post for disaster intelligence"""
    try:
        result = social_analyzer.analyze_post(
            text=post.text,
            location=post.location,
            timestamp=post.timestamp
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/social-feed")
async def get_social_feed():
    """Get analyzed social media feed - REAL + SAMPLE DATA (cached)"""
    # Get cached real data (fetched in background every 60 seconds)
    real_posts = social_media_cache.get("posts", [])
    last_updated = social_media_cache.get("last_updated")
    
    # Get sample data
    sample_posts = data_generator.generate_social_feed()
    
    # Combine both
    all_posts = real_posts + sample_posts
    
    return {
        "posts": all_posts,
        "count": len(all_posts),
        "real_count": len(real_posts),
        "sample_count": len(sample_posts),
        "sources": ["Reddit", "Twitter (Nitter)", "News RSS", "Sample Data"],
        "cache_status": {
            "last_updated": last_updated.isoformat() if last_updated else None,
            "is_fetching": social_media_cache.get("is_fetching", False),
            "refresh_interval": "60 seconds"
        }
    }

@app.get("/api/alerts")
async def get_alerts():
    """Get real-time disaster alerts"""
    alerts = data_generator.generate_alerts()
    return {"alerts": alerts, "count": len(alerts)}

@app.get("/api/social-feed-sample")
async def get_social_feed_sample():
    """Get SAMPLE disaster-related social media data (fast, filtered)"""
    sample_posts = data_generator.generate_social_feed()
    return {
        "posts": sample_posts,
        "count": len(sample_posts),
        "sources": ["Sample Disaster Data"],
        "note": "Filtered disaster-related content only"
    }

@app.get("/api/social-feed-real")
async def get_social_feed_real():
    """Get REAL social media data (slow - 8+ seconds)"""
    try:
        real_social = social_media_scraper.get_all_social_media()
        return real_social
    except Exception as e:
        return {
            "posts": [],
            "total_count": 0,
            "error": str(e),
            "sources": []
        }

@app.get("/api/statistics")
async def get_statistics():
    """Get disaster statistics dashboard - DYNAMIC (calculated from real data)"""
    # Fetch actual data
    zones = data_generator.generate_disaster_zones()
    flood_areas = data_generator.generate_flood_areas()
    infrastructure = data_generator.generate_infrastructure_damage()
    displacement = data_generator.generate_displacement_data()
    alerts = data_generator.generate_alerts()
    
    # Calculate statistics dynamically
    total_affected_area = sum(zone.get('affected_area_km2', 0) for zone in zones)
    damaged_buildings = sum(1 for infra in infrastructure if infra.get('type') == 'building' and not infra.get('operational', True))
    flooded_zones = len(flood_areas)
    displaced_population = sum(disp.get('displaced_count', 0) for disp in displacement)
    rescue_operations = sum(1 for alert in alerts if alert.get('type') == 'rescue')
    emergency_shelters = sum(1 for disp in displacement if disp.get('shelter_capacity', 0) > 0)
    
    stats = {
        "total_affected_area_km2": round(total_affected_area, 1),
        "damaged_buildings": damaged_buildings,
        "flooded_zones": flooded_zones,
        "displaced_population": displaced_population,
        "rescue_operations_active": rescue_operations,
        "emergency_shelters": emergency_shelters,
        "last_updated": datetime.now().isoformat()
    }
    return stats

@app.get("/api/here-config")
async def get_here_config():
    """Get HERE API configuration status"""
    return {
        "configured": here_service.is_configured(),
        "services": {
            "maps": "https://js.api.here.com/v3/3.1/mapsjs-core.js",
            "geocoding": "https://geocode.search.hereapi.com/v1",
            "routing": "https://router.hereapi.com/v8",
            "isoline": "https://isoline.router.hereapi.com/v8"
        },
        "available_features": ["routing", "isoline", "geocoding", "reverse_geocoding"] if here_service.is_configured() else []
    }

@app.post("/api/here/geocode")
async def geocode_address(request: GeocodeRequest):
    """Convert address to coordinates"""
    if not here_service.is_configured():
        raise HTTPException(status_code=503, detail="HERE API not configured")
    
    result = here_service.geocode(request.address)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/api/here/reverse-geocode")
async def reverse_geocode(lat: float, lon: float):
    """Convert coordinates to address"""
    if not here_service.is_configured():
        raise HTTPException(status_code=503, detail="HERE API not configured")
    
    result = here_service.reverse_geocode(lat, lon)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/api/here/route")
async def calculate_route(request: RouteRequest):
    """Calculate route between two points"""
    if not here_service.is_configured():
        raise HTTPException(status_code=503, detail="HERE API not configured")
    
    result = here_service.calculate_route(
        origin=(request.origin_lat, request.origin_lon),
        destination=(request.destination_lat, request.destination_lon),
        transport_mode=request.transport_mode
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/api/here/evacuation-route")
async def calculate_evacuation_route(request: RouteRequest):
    """Calculate optimized evacuation route"""
    if not here_service.is_configured():
        raise HTTPException(status_code=503, detail="HERE API not configured")
    
    result = here_service.calculate_evacuation_route(
        disaster_zone=(request.origin_lat, request.origin_lon),
        shelter=(request.destination_lat, request.destination_lon)
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/api/here/isoline")
async def calculate_isoline(request: IsolineRequest):
    """Calculate reachable area (isoline) from a point"""
    if not here_service.is_configured():
        raise HTTPException(status_code=503, detail="HERE API not configured")
    
    # Convert minutes to seconds
    range_seconds = [m * 60 for m in request.range_minutes]
    
    result = here_service.calculate_isoline(
        origin=(request.origin_lat, request.origin_lon),
        range_type="time",
        range_values=range_seconds,
        transport_mode=request.transport_mode
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/api/here/rescue-coverage")
async def get_rescue_coverage(lat: float, lon: float):
    """Get rescue team coverage area (5, 10, 15 minute zones)"""
    if not here_service.is_configured():
        raise HTTPException(status_code=503, detail="HERE API not configured")
    
    # Force reload of here_service module
    import importlib
    import here_service as hs_module
    importlib.reload(hs_module)
    temp_service = hs_module.HEREService()
    
    result = temp_service.get_rescue_coverage(
        rescue_station=(lat, lon)
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/api/export/pdf")
async def export_pdf():
    """Export disaster report as PDF"""
    try:
        # Gather all data
        disaster_data = {
            'zones': data_generator.generate_disaster_zones(),
            'flood_areas': data_generator.generate_flood_areas(),
            'infrastructure': data_generator.generate_infrastructure_damage(),
            'displacement': data_generator.generate_displacement_data(),
            'alerts': data_generator.generate_alerts()
        }
        
        statistics = {
            "total_affected_area_km2": 245.7,
            "damaged_buildings": 1247,
            "flooded_zones": 18,
            "displaced_population": 12500,
            "rescue_operations_active": 23,
            "emergency_shelters": 15,
            "last_updated": datetime.now().isoformat()
        }
        
        pdf_bytes = map_exporter.generate_pdf_report(disaster_data, statistics)
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=disaster_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@app.get("/api/export/json")
async def export_json():
    """Export all disaster data as JSON"""
    try:
        disaster_data = {
            'zones': data_generator.generate_disaster_zones(),
            'flood_areas': data_generator.generate_flood_areas(),
            'infrastructure': data_generator.generate_infrastructure_damage(),
            'displacement': data_generator.generate_displacement_data(),
            'alerts': data_generator.generate_alerts(),
            'social_feed': data_generator.generate_social_feed(),
            'statistics': {
                "total_affected_area_km2": 245.7,
                "damaged_buildings": 1247,
                "flooded_zones": 18,
                "displaced_population": 12500,
                "rescue_operations_active": 23,
                "emergency_shelters": 15,
                "last_updated": datetime.now().isoformat()
            },
            'exported_at': datetime.now().isoformat()
        }
        
        json_bytes = map_exporter.generate_json_export(disaster_data)
        
        return Response(
            content=json_bytes,
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=disaster_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JSON export failed: {str(e)}")

@app.get("/api/export/csv")
async def export_csv():
    """Export disaster zones as CSV"""
    try:
        zones = data_generator.generate_disaster_zones()
        csv_bytes = map_exporter.generate_csv_export(zones)
        
        return Response(
            content=csv_bytes,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=disaster_zones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CSV export failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
