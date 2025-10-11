"""
HERE Map Image API Integration
Provides cartographic reference images for disaster comparison and change detection
"""

import os
import requests
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import time
from functools import wraps

load_dotenv()

def rate_limit(max_per_second=2):
    """Rate limiter decorator - limits to max_per_second requests"""
    min_interval = 1.0 / max_per_second
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

class HEREImageService:
    """HERE Map Image API service for cartographic reference images"""
    
    def __init__(self):
        self.api_key = os.getenv("HERE_API_KEY", "")
        self.map_image_base = "https://image.maps.ls.hereapi.com/mia/1.6"
        self._cache = {}  # Simple in-memory cache
        
    def is_configured(self) -> bool:
        """Check if HERE API key is configured"""
        return bool(self.api_key and self.api_key != "YOUR_HERE_API_KEY_HERE")
    
    @rate_limit(max_per_second=2)  # Limit to 2 requests per second
    def get_reference_image(
        self, 
        lat: float, 
        lon: float, 
        zoom: int = 15,
        width: int = 512,
        height: int = 512,
        map_type: str = "normal.day"
    ) -> Optional[Dict]:
        """
        Get HERE cartographic reference image for a location
        
        Args:
            lat: Latitude
            lon: Longitude
            zoom: Zoom level (1-20, higher = more detail)
            width: Image width in pixels
            height: Image height in pixels
            map_type: Map style (normal.day, satellite.day, terrain.day, hybrid.day)
            
        Returns:
            Dict with image data and metadata
        """
        if not self.is_configured():
            return {"error": "HERE API key not configured"}
        
        # Check cache first
        cache_key = f"{lat}_{lon}_{zoom}_{width}_{height}_{map_type}"
        if cache_key in self._cache:
            print(f"✅ Returning cached image for {lat}, {lon}")
            return self._cache[cache_key]
        
        try:
            # HERE Map Image API endpoint
            url = f"{self.map_image_base}/mapview"
            
            params = {
                "c": f"{lat},{lon}",  # Center coordinates
                "z": zoom,
                "w": width,
                "h": height,
                "t": 0,  # Map type: 0=normal, 1=satellite, 2=terrain, 3=hybrid
                "apiKey": self.api_key
            }
            
            # Map type conversion
            type_map = {
                "normal.day": 0,
                "satellite.day": 1,
                "terrain.day": 2,
                "hybrid.day": 3
            }
            params["t"] = type_map.get(map_type, 0)
            
            response = requests.get(url, params=params, timeout=15)
            
            # Handle rate limiting with better error message
            if response.status_code == 429:
                return {
                    "error": "Rate limit reached. Please wait 30-60 seconds and try again. HERE API limits requests per second.",
                    "retry_after": 60,
                    "status": "rate_limited"
                }
            
            response.raise_for_status()
            
            # Convert image to base64 for easy transmission
            image_data = base64.b64encode(response.content).decode('utf-8')
            
            result = {
                "success": True,
                "image_base64": image_data,
                "location": {"lat": lat, "lon": lon},
                "zoom": zoom,
                "dimensions": {"width": width, "height": height},
                "map_type": map_type,
                "format": "png"
            }
            
            # Cache the result
            self._cache[cache_key] = result
            print(f"✅ Cached image for {lat}, {lon}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch reference image: {str(e)}"}
    
    def get_satellite_reference(
        self,
        lat: float,
        lon: float,
        zoom: int = 15,
        width: int = 512,
        height: int = 512
    ) -> Optional[Dict]:
        """
        Get satellite imagery reference for disaster comparison
        
        Args:
            lat: Latitude
            lon: Longitude
            zoom: Zoom level
            width: Image width
            height: Image height
            
        Returns:
            Dict with satellite image data
        """
        return self.get_reference_image(lat, lon, zoom, width, height, "satellite.day")
    
    def compare_disaster_image(
        self,
        disaster_image_path: str,
        lat: float,
        lon: float,
        zoom: int = 15
    ) -> Optional[Dict]:
        """
        Compare disaster image with HERE reference cartographic image
        
        Args:
            disaster_image_path: Path to disaster image
            lat: Location latitude
            lon: Location longitude
            zoom: Zoom level for reference image
            
        Returns:
            Dict with comparison results and change detection metrics
        """
        if not self.is_configured():
            return {"error": "HERE API key not configured"}
        
        try:
            # Load disaster image
            disaster_img = Image.open(disaster_image_path)
            disaster_array = np.array(disaster_img)
            
            # Get HERE reference image
            ref_result = self.get_satellite_reference(lat, lon, zoom, 
                                                     disaster_img.width, 
                                                     disaster_img.height)
            
            if "error" in ref_result:
                return ref_result
            
            # Decode reference image
            ref_image_data = base64.b64decode(ref_result["image_base64"])
            ref_img = Image.open(BytesIO(ref_image_data))
            ref_array = np.array(ref_img)
            
            # Ensure same dimensions
            if disaster_array.shape != ref_array.shape:
                ref_img = ref_img.resize((disaster_img.width, disaster_img.height))
                ref_array = np.array(ref_img)
            
            # Calculate change detection metrics
            difference = np.abs(disaster_array.astype(float) - ref_array.astype(float))
            change_percentage = (np.sum(difference > 30) / difference.size) * 100
            
            # Detect specific changes
            changes = self._analyze_changes(disaster_array, ref_array)
            
            return {
                "success": True,
                "location": {"lat": lat, "lon": lon},
                "change_percentage": round(change_percentage, 2),
                "changes_detected": changes,
                "disaster_image_size": disaster_array.shape,
                "reference_image_size": ref_array.shape,
                "analysis": self._generate_analysis(change_percentage, changes)
            }
            
        except Exception as e:
            return {"error": f"Image comparison failed: {str(e)}"}
    
    def _analyze_changes(self, disaster_img: np.ndarray, ref_img: np.ndarray) -> Dict:
        """
        Analyze specific types of changes between images
        
        Args:
            disaster_img: Disaster image array
            ref_img: Reference image array
            
        Returns:
            Dict with detected changes
        """
        changes = {
            "water_increase": False,
            "vegetation_loss": False,
            "infrastructure_damage": False,
            "color_shift_detected": False
        }
        
        # Convert to grayscale for analysis
        if len(disaster_img.shape) == 3:
            disaster_gray = np.mean(disaster_img, axis=2)
            ref_gray = np.mean(ref_img, axis=2)
        else:
            disaster_gray = disaster_img
            ref_gray = ref_img
        
        # Detect water (darker areas in disaster image)
        water_threshold = -20
        water_change = np.mean(disaster_gray - ref_gray)
        if water_change < water_threshold:
            changes["water_increase"] = True
        
        # Detect vegetation loss (color analysis if RGB)
        if len(disaster_img.shape) == 3 and disaster_img.shape[2] >= 3:
            # Green channel analysis
            green_loss = np.mean(ref_img[:,:,1]) - np.mean(disaster_img[:,:,1])
            if green_loss > 10:
                changes["vegetation_loss"] = True
        
        # Detect infrastructure damage (edge/texture changes)
        edge_change = np.std(disaster_gray) - np.std(ref_gray)
        if abs(edge_change) > 15:
            changes["infrastructure_damage"] = True
        
        # Overall color shift
        if len(disaster_img.shape) == 3:
            color_diff = np.mean(np.abs(disaster_img - ref_img))
            if color_diff > 25:
                changes["color_shift_detected"] = True
        
        return changes
    
    def _generate_analysis(self, change_pct: float, changes: Dict) -> str:
        """Generate human-readable analysis"""
        analysis_parts = []
        
        if change_pct > 50:
            analysis_parts.append("CRITICAL: Major changes detected (>50% pixel difference)")
        elif change_pct > 30:
            analysis_parts.append("HIGH: Significant changes detected (>30% pixel difference)")
        elif change_pct > 15:
            analysis_parts.append("MEDIUM: Moderate changes detected (>15% pixel difference)")
        else:
            analysis_parts.append("LOW: Minor changes detected (<15% pixel difference)")
        
        if changes["water_increase"]:
            analysis_parts.append("Possible flooding detected (increased dark/water areas)")
        
        if changes["vegetation_loss"]:
            analysis_parts.append("Vegetation loss detected (decreased green coverage)")
        
        if changes["infrastructure_damage"]:
            analysis_parts.append("Structural changes detected (texture/edge differences)")
        
        return " | ".join(analysis_parts)
    
    def get_area_comparison(
        self,
        lat: float,
        lon: float,
        radius_km: float = 1.0,
        zoom: int = 14
    ) -> Optional[Dict]:
        """
        Get reference images for area comparison (before/after disaster)
        
        Args:
            lat: Center latitude
            lon: Center longitude
            radius_km: Radius to cover in kilometers
            zoom: Zoom level
            
        Returns:
            Dict with reference image and area info
        """
        if not self.is_configured():
            return {"error": "HERE API key not configured"}
        
        # Calculate bounding box based on radius
        # Rough approximation: 1 degree ≈ 111 km
        lat_offset = radius_km / 111.0
        lon_offset = radius_km / (111.0 * np.cos(np.radians(lat)))
        
        bbox = {
            "north": lat + lat_offset,
            "south": lat - lat_offset,
            "east": lon + lon_offset,
            "west": lon - lon_offset
        }
        
        # Get reference image
        ref_image = self.get_satellite_reference(lat, lon, zoom, 1024, 1024)
        
        if "error" in ref_image:
            return ref_image
        
        return {
            "success": True,
            "center": {"lat": lat, "lon": lon},
            "radius_km": radius_km,
            "bounding_box": bbox,
            "reference_image": ref_image,
            "coverage_area_km2": round(np.pi * radius_km * radius_km, 2)
        }
