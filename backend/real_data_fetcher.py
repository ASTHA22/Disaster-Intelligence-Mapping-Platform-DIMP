"""
Real-time data fetcher from free public APIs
No API keys needed for most sources!
"""

import requests
from datetime import datetime
from typing import List, Dict

class RealDataFetcher:
    """Fetch real disaster data from free public APIs"""
    
    def __init__(self):
        # NASA FIRMS - Get free key from: https://firms.modaps.eosdis.nasa.gov/api/area/
        # For demo, using public endpoint (limited)
        self.nasa_firms_key = "MAP_KEY"  # Replace with your free key
    
    def _get_india_region(self, lat, lon):
        """Determine Indian state/region from coordinates"""
        # Approximate state boundaries
        if 21 <= lat <= 27 and 85 <= lon <= 89:
            return "West Bengal"
        elif 21 <= lat <= 25 and 83 <= lon <= 87:
            if lat > 23:
                return "Jharkhand"
            else:
                return "Chhattisgarh"
        elif 18 <= lat <= 21 and 72 <= lon <= 75:
            return "Maharashtra"
        elif 8 <= lat <= 13 and 76 <= lon <= 78:
            return "Kerala"
        elif 12 <= lat <= 18 and 77 <= lon <= 80:
            return "Karnataka"
        elif 10 <= lat <= 14 and 79 <= lon <= 82:
            return "Tamil Nadu"
        elif 23 <= lat <= 28 and 70 <= lon <= 74:
            return "Rajasthan"
        elif 28 <= lat <= 32 and 75 <= lon <= 77:
            return "Punjab/Haryana"
        elif 26 <= lat <= 30 and 78 <= lon <= 81:
            return "Uttar Pradesh"
        elif 23 <= lat <= 27 and 78 <= lon <= 82:
            return "Madhya Pradesh"
        else:
            return "India"
        
    def fetch_nasa_fires(self, country="IND", days=1) -> List[Dict]:
        """
        Fetch real-time fire data from NASA FIRMS
        FREE - Just need to register for key (takes 2 minutes)
        https://firms.modaps.eosdis.nasa.gov/api/area/
        """
        try:
            # Using public endpoint (no key needed but limited)
            url = f"https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_South_Asia_24h.csv"
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                print(f"NASA FIRMS returned status {response.status_code}")
                return []
            
            # Parse CSV
            lines = response.text.strip().split('\n')
            if len(lines) < 2:
                return []
            
            headers = lines[0].split(',')
            fires = []
            
            for line in lines[1:]:
                values = line.split(',')
                if len(values) < 10:
                    continue
                    
                try:
                    lat = float(values[0])
                    lon = float(values[1])
                    brightness = float(values[2])
                    confidence = int(values[8]) if len(values) > 8 else 50
                    
                    # Filter for India region (approximate)
                    if 8 <= lat <= 35 and 68 <= lon <= 97:
                        # Determine region/state for better searchability
                        region = self._get_india_region(lat, lon)
                        
                        fires.append({
                            "id": f"fire_{lat}_{lon}",
                            "name": f"Fire in {region}",
                            "location": f"{lat:.2f}°N, {lon:.2f}°E",
                            "region": region,
                            "type": "fire",
                            "coordinates": {"lat": lat, "lon": lon},
                            "brightness": brightness,
                            "confidence": confidence,
                            "severity": "critical" if confidence > 80 else "high",
                            "damage_score": min(confidence / 100, 1.0),
                            "affected_area_km2": 0.5,
                            "last_updated": datetime.now().isoformat(),
                            "source": "NASA FIRMS"
                        })
                except (ValueError, IndexError) as e:
                    continue
            
            return fires[:20]  # Limit to 20 most recent
        except Exception as e:
            print(f"Error fetching NASA fires: {e}")
            return []
    
    def fetch_earthquakes(self, min_magnitude=2.5) -> List[Dict]:
        """
        Fetch real-time earthquake data from USGS
        FREE - No authentication needed!
        https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
        """
        try:
            url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            earthquakes = []
            for feature in data.get('features', []):
                props = feature['properties']
                coords = feature['geometry']['coordinates']
                
                mag = props.get('mag', 0)
                if mag < min_magnitude:
                    continue
                
                earthquakes.append({
                    "id": feature['id'],
                    "name": props.get('place', 'Unknown location'),
                    "type": "earthquake",
                    "coordinates": {
                        "lat": coords[1],
                        "lon": coords[0]
                    },
                    "magnitude": mag,
                    "depth": coords[2],
                    "severity": "critical" if mag > 6 else "high" if mag > 4 else "medium",
                    "damage_score": min(mag / 10, 1.0),
                    "affected_area_km2": mag * 10,
                    "last_updated": datetime.fromtimestamp(props.get('time', 0) / 1000).isoformat(),
                    "source": "USGS"
                })
            
            return earthquakes[:15]  # Limit to 15
        except Exception as e:
            print(f"Error fetching earthquakes: {e}")
            return []
    
    def fetch_weather_alerts(self) -> List[Dict]:
        """
        Fetch weather alerts from OpenWeatherMap
        FREE tier available - 60 calls/minute
        Get free key: https://openweathermap.org/api
        """
        try:
            # Using free weather API (no key needed for basic data)
            # For production, get free OpenWeatherMap API key
            url = "https://api.open-meteo.com/v1/forecast?latitude=19.0760&longitude=72.8777&current_weather=true"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            weather = data.get('current_weather', {})
            alerts = []
            
            # Create alert if severe weather
            if weather.get('windspeed', 0) > 50:  # Strong winds
                alerts.append({
                    "id": "weather_wind_mumbai",
                    "name": "High Wind Alert - Mumbai",
                    "type": "weather",
                    "coordinates": {"lat": 19.0760, "lon": 72.8777},
                    "severity": "high",
                    "damage_score": 0.6,
                    "affected_area_km2": 100,
                    "last_updated": datetime.now().isoformat(),
                    "source": "Open-Meteo"
                })
            
            return alerts
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return []
    
    def get_all_real_data(self) -> Dict:
        """
        Fetch all available real-time data
        Returns combined data from all free sources
        """
        print("Fetching real-time disaster data from free APIs...")
        
        fires = self.fetch_nasa_fires()
        print(f"✓ Found {len(fires)} active fires (NASA FIRMS)")
        
        earthquakes = self.fetch_earthquakes()
        print(f"✓ Found {len(earthquakes)} earthquakes (USGS)")
        
        weather = self.fetch_weather_alerts()
        print(f"✓ Found {len(weather)} weather alerts (Open-Meteo)")
        
        # Combine all into zones format
        all_zones = fires + earthquakes + weather
        
        return {
            "zones": all_zones,
            "total_count": len(all_zones),
            "sources": ["NASA FIRMS", "USGS", "Open-Meteo"],
            "last_updated": datetime.now().isoformat()
        }

# Example usage
if __name__ == "__main__":
    fetcher = RealDataFetcher()
    
    print("\n" + "="*60)
    print("FETCHING REAL-TIME DISASTER DATA (FREE SOURCES)")
    print("="*60 + "\n")
    
    data = fetcher.get_all_real_data()
    
    print(f"\nTotal disasters found: {data['total_count']}")
    print(f"Data sources: {', '.join(data['sources'])}")
    print(f"Last updated: {data['last_updated']}")
    
    if data['zones']:
        print(f"\n--- Sample Data ---")
        print(f"First disaster: {data['zones'][0]}")
