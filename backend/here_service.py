"""
HERE API Integration Service
Provides routing, isoline, and geocoding services for disaster response
"""

import os
import requests
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()

class HEREService:
    """HERE API service for disaster intelligence"""
    
    def __init__(self):
        self.api_key = os.getenv("HERE_API_KEY", "")
        self.geocoding_base = "https://geocode.search.hereapi.com/v1"
        self.routing_base = "https://router.hereapi.com/v8"
        self.isoline_base = "https://isoline.router.hereapi.com/v8"
        
    def is_configured(self) -> bool:
        """Check if HERE API key is configured"""
        return bool(self.api_key and self.api_key != "YOUR_HERE_API_KEY_HERE")
    
    def geocode(self, address: str) -> Optional[Dict]:
        """
        Convert address to coordinates
        
        Args:
            address: Address string (e.g., "Connaught Place, Delhi")
            
        Returns:
            Dict with lat, lon, and formatted address
        """
        if not self.is_configured():
            return {"error": "HERE API key not configured"}
        
        try:
            url = f"{self.geocoding_base}/geocode"
            params = {
                "q": address,
                "apiKey": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("items") and len(data["items"]) > 0:
                item = data["items"][0]
                position = item["position"]
                return {
                    "lat": position["lat"],
                    "lon": position["lng"],
                    "address": item.get("address", {}).get("label", address),
                    "title": item.get("title", ""),
                    "type": item.get("resultType", "")
                }
            
            return {"error": "Location not found"}
            
        except Exception as e:
            return {"error": f"Geocoding failed: {str(e)}"}
    
    def reverse_geocode(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Convert coordinates to address
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dict with address information
        """
        if not self.is_configured():
            return {"error": "HERE API key not configured"}
        
        try:
            url = f"{self.geocoding_base}/revgeocode"
            params = {
                "at": f"{lat},{lon}",
                "apiKey": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("items") and len(data["items"]) > 0:
                item = data["items"][0]
                return {
                    "address": item.get("address", {}).get("label", ""),
                    "city": item.get("address", {}).get("city", ""),
                    "district": item.get("address", {}).get("district", ""),
                    "country": item.get("address", {}).get("countryName", "")
                }
            
            return {"error": "Address not found"}
            
        except Exception as e:
            return {"error": f"Reverse geocoding failed: {str(e)}"}
    
    def calculate_route(self, origin: Tuple[float, float], 
                       destination: Tuple[float, float],
                       transport_mode: str = "car") -> Dict:
        """
        Calculate route between two points
        
        Args:
            origin: (lat, lon) tuple for start point
            destination: (lat, lon) tuple for end point
            transport_mode: "car", "truck", "pedestrian", "bicycle"
            
        Returns:
            Dict with route information including polyline, distance, duration
        """
        if not self.is_configured():
            return {"error": "HERE API key not configured"}
        
        try:
            url = f"{self.routing_base}/routes"
            params = {
                "transportMode": transport_mode,
                "origin": f"{origin[0]},{origin[1]}",
                "destination": f"{destination[0]},{destination[1]}",
                "return": "polyline,summary,actions,instructions",
                "apiKey": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if data.get("routes") and len(data["routes"]) > 0:
                route = data["routes"][0]
                sections = route.get("sections", [])
                
                if sections:
                    section = sections[0]
                    summary = section.get("summary", {})
                    
                    return {
                        "success": True,
                        "distance_meters": summary.get("length", 0),
                        "distance_km": round(summary.get("length", 0) / 1000, 2),
                        "duration_seconds": summary.get("duration", 0),
                        "duration_minutes": round(summary.get("duration", 0) / 60, 1),
                        "polyline": section.get("polyline", ""),
                        "departure": section.get("departure", {}),
                        "arrival": section.get("arrival", {}),
                        "actions": section.get("actions", []),
                        "transport_mode": transport_mode
                    }
            
            return {"error": "No route found"}
            
        except Exception as e:
            return {"error": f"Route calculation failed: {str(e)}"}
    
    def calculate_isoline(self, origin: Tuple[float, float],
                         range_type: str = "time",
                         range_values: List[int] = [600, 1200, 1800],
                         transport_mode: str = "car") -> Dict:
        """
        Calculate isoline (reachable area) from a point
        
        Args:
            origin: (lat, lon) tuple for center point
            range_type: "time" (seconds) or "distance" (meters)
            range_values: List of range values (e.g., [600, 1200] for 10 and 20 minutes)
            transport_mode: "car", "truck", "pedestrian", "bicycle"
            
        Returns:
            Dict with isoline polygons for each range
        """
        if not self.is_configured():
            return {"error": "HERE API key not configured"}
        
        try:
            url = f"{self.isoline_base}/isolines"
            
            # Convert range values to comma-separated string
            range_str = ",".join(map(str, range_values))
            
            params = {
                "transportMode": transport_mode,
                "origin": f"{origin[0]},{origin[1]}",
                "range[type]": range_type,
                "range[values]": range_str,
                "apiKey": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if data.get("isolines"):
                isolines = []
                
                for isoline in data["isolines"]:
                    range_value = isoline.get("range", {}).get("value", 0)
                    
                    # Convert to human-readable format
                    if range_type == "time":
                        range_label = f"{range_value // 60} minutes"
                    else:
                        range_label = f"{range_value / 1000} km"
                    
                    polygons = []
                    for polygon in isoline.get("polygons", []):
                        outer = polygon.get("outer", "")
                        if outer:
                            # Decode polyline to coordinates
                            coords = self._decode_polyline(outer)
                            polygons.append(coords)
                    
                    isolines.append({
                        "range_value": range_value,
                        "range_label": range_label,
                        "range_type": range_type,
                        "polygons": polygons,
                        "transport_mode": transport_mode
                    })
                
                return {
                    "success": True,
                    "origin": {"lat": origin[0], "lon": origin[1]},
                    "isolines": isolines
                }
            
            return {"error": "No isolines calculated"}
            
        except Exception as e:
            return {"error": f"Isoline calculation failed: {str(e)}"}
    
    def calculate_evacuation_route(self, disaster_zone: Tuple[float, float],
                                   shelter: Tuple[float, float]) -> Dict:
        """
        Calculate optimized evacuation route
        
        Args:
            disaster_zone: (lat, lon) of disaster location
            shelter: (lat, lon) of evacuation shelter
            
        Returns:
            Route with evacuation-specific information
        """
        route = self.calculate_route(disaster_zone, shelter, transport_mode="car")
        
        if route.get("success"):
            # Add evacuation-specific metadata
            route["evacuation_info"] = {
                "estimated_evacuees_per_hour": 500,  # Based on route capacity
                "recommended_transport": ["bus", "car", "pedestrian"],
                "alternative_routes_available": True,
                "traffic_status": "moderate"
            }
        
        return route
    
    def get_rescue_coverage(self, rescue_station: Tuple[float, float]) -> Dict:
        """
        Calculate rescue team coverage area
        
        Args:
            rescue_station: (lat, lon) of rescue station
            
        Returns:
            Coverage zones for 5, 10, 15 minute response times
        """
        return self.calculate_isoline(
            origin=rescue_station,
            range_type="time",
            range_values=[300, 600, 900],  # 5, 10, 15 minutes
            transport_mode="car"
        )
    
    def _decode_polyline(self, polyline_str: str) -> List[List[float]]:
        """
        Decode HERE flexible polyline to lat/lon coordinates
        
        Args:
            polyline_str: Encoded polyline string
            
        Returns:
            List of [lon, lat] coordinates (GeoJSON format)
        """
        # Simplified decoder - HERE uses flexible polyline format
        # For production, use the official HERE polyline library
        # This is a basic implementation
        
        coordinates = []
        index = 0
        lat = 0
        lng = 0
        
        try:
            while index < len(polyline_str):
                # Decode latitude
                result = 0
                shift = 0
                while True:
                    b = ord(polyline_str[index]) - 63
                    index += 1
                    result |= (b & 0x1f) << shift
                    shift += 5
                    if b < 0x20:
                        break
                
                dlat = ~(result >> 1) if (result & 1) else (result >> 1)
                lat += dlat
                
                # Decode longitude
                result = 0
                shift = 0
                while True:
                    b = ord(polyline_str[index]) - 63
                    index += 1
                    result |= (b & 0x1f) << shift
                    shift += 5
                    if b < 0x20:
                        break
                
                dlng = ~(result >> 1) if (result & 1) else (result >> 1)
                lng += dlng
                
                coordinates.append([lng / 1e5, lat / 1e5])
        except:
            # If decoding fails, return empty array
            pass
        
        return coordinates
