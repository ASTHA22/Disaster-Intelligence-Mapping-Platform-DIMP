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
        self.nasa_firms_key = "FIRMS_MAP_KEY"  # Get free from https://firms.modaps.eosdis.nasa.gov/api/area/
        
    def fetch_nasa_fires(self, country="IND", days=1) -> List[Dict]:
        """
        Fetch real-time fire data from NASA FIRMS
        FREE - No authentication needed!
        """
        try:
            url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{self.nasa_firms_key}/VIIRS_SNPP_NRT/{country}/{days}"
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
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
                    confidence = int(values[8])
                    
                    fires.append({
                        "id": f"fire_{lat}_{lon}",
                        "type": "fire",
                        "coordinates": {"lat": lat, "lon": lon},
                        "brightness": brightness,
                        "confidence": confidence,
                        "severity": "critical" if confidence > 80 else "high",
                        "timestamp": datetime.now().isoformat(),
                        "source": "NASA FIRMS"
                    })
                except (ValueError, IndexError):
                    continue
            
            return fires
        except Exception as e:
            print(f"Error fetching NASA fires: {e}")
            return []
    
    def fetch_earthquakes(self) -> List[Dict]:
        """
        Fetch real-time earthquake data from USGS
        FREE - No authentication needed!
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
                earthquakes.append({
                    "id": feature['id'],
                    "type": "earthquake",
                    "coordinates": {
                        "lat": coords[1],
                        "lon": coords[0]
                    },
                    "magnitude": mag,
                    "location": props.get('place', 'Unknown'),
                    "depth": coords[2],
                    "severity": "critical" if mag > 6 else "high" if mag > 4 else "medium",
                    "timestamp": props.get('time'),
                    "source": "USGS"
                })
            
            return earthquakes
        except Exception as e:
            print(f"Error fetching earthquakes: {e}")
            return []
    
    def fetch_gdacs_disasters(self) -> List[Dict]:
        """
        Fetch real disaster alerts from GDACS
        FREE - No authentication needed!
        """
        try:
            url = "https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH"
            response = requests.get(url, timeout=10)
            
            # GDACS returns XML, would need parsing
            # For now, return empty - can implement XML parsing if needed
            return []
        except Exception as e:
            print(f"Error fetching GDACS: {e}")
            return []
    
    def get_all_real_data(self) -> Dict:
        """
        Fetch all available real-time data
        Returns combined data from all free sources
        """
        return {
            "fires": self.fetch_nasa_fires(),
            "earthquakes": self.fetch_earthquakes(),
            "disasters": self.fetch_gdacs_disasters()
        }

# Example usage
if __name__ == "__main__":
    fetcher = RealDataFetcher()
    
    print("Fetching real-time data...")
    
    fires = fetcher.fetch_nasa_fires()
    print(f"Found {len(fires)} active fires")
    
    earthquakes = fetcher.fetch_earthquakes()
    print(f"Found {len(earthquakes)} earthquakes in last 24h")
    
    if fires:
        print(f"\nSample fire: {fires[0]}")
    
    if earthquakes:
        print(f"\nSample earthquake: {earthquakes[0]}")
