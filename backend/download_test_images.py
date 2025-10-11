"""
Download sample disaster images for testing
Uses free, public domain disaster images
"""

import requests
import os

# Create test_images directory
os.makedirs("test_images", exist_ok=True)

# Free disaster images from public sources
SAMPLE_IMAGES = {
    "mumbai_flood.jpg": {
        "url": "https://images.unsplash.com/photo-1547683905-f686c993aae5?w=800",
        "description": "Flood scene (Unsplash - free)",
        "location": {"lat": 19.0760, "lon": 72.8777, "name": "Mumbai"}
    },
    "building_damage.jpg": {
        "url": "https://images.unsplash.com/photo-1564507592333-c60657eea523?w=800",
        "description": "Damaged building (Unsplash - free)",
        "location": {"lat": 28.6139, "lon": 77.2090, "name": "Delhi"}
    },
    "earthquake_damage.jpg": {
        "url": "https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=800",
        "description": "Earthquake damage (Unsplash - free)",
        "location": {"lat": 34.0522, "lon": -118.2437, "name": "Los Angeles"}
    },
    "wildfire.jpg": {
        "url": "https://images.unsplash.com/photo-1603048588665-791ca8aea617?w=800",
        "description": "Wildfire scene (Unsplash - free)",
        "location": {"lat": 37.7749, "lon": -122.4194, "name": "California"}
    },
    "hurricane_damage.jpg": {
        "url": "https://images.unsplash.com/photo-1527482797697-8795b05a13fe?w=800",
        "description": "Hurricane damage (Unsplash - free)",
        "location": {"lat": 25.7617, "lon": -80.1918, "name": "Miami"}
    }
}

def download_image(filename, url, description):
    """Download image from URL"""
    try:
        print(f"Downloading {filename}...")
        print(f"  Description: {description}")
        print(f"  URL: {url}")
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        filepath = os.path.join("test_images", filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"  ✅ Saved to {filepath}")
        print()
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        print()
        return False

def main():
    print("=" * 60)
    print("Downloading Sample Disaster Images")
    print("=" * 60)
    print()
    
    success_count = 0
    for filename, info in SAMPLE_IMAGES.items():
        if download_image(filename, info["url"], info["description"]):
            success_count += 1
    
    print("=" * 60)
    print(f"Downloaded {success_count}/{len(SAMPLE_IMAGES)} images")
    print("=" * 60)
    print()
    
    # Print usage instructions
    print("Usage:")
    print("------")
    for filename, info in SAMPLE_IMAGES.items():
        filepath = os.path.join("test_images", filename)
        if os.path.exists(filepath):
            loc = info["location"]
            print(f"\n{filename}:")
            print(f"  Location: {loc['name']} ({loc['lat']}, {loc['lon']})")
            print(f"  Test command:")
            print(f"    curl -X POST 'http://localhost:8000/api/here/compare-disaster-image?lat={loc['lat']}&lon={loc['lon']}&zoom=15' \\")
            print(f"      -F 'file=@{filepath}'")

if __name__ == "__main__":
    main()
