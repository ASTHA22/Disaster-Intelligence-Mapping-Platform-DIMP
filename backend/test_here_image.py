"""
Test script for HERE Map Image API integration
Demonstrates cartographic reference image retrieval and disaster comparison
"""

import requests
import json
from here_image_service import HEREImageService

def test_reference_image():
    """Test getting HERE reference image"""
    print("\n=== Testing HERE Reference Image API ===")
    
    service = HEREImageService()
    
    # Mumbai coordinates
    lat, lon = 19.0760, 72.8777
    
    print(f"Fetching satellite reference for Mumbai ({lat}, {lon})...")
    result = service.get_satellite_reference(lat, lon, zoom=15)
    
    if result.get("success"):
        print("✅ SUCCESS!")
        print(f"   Image size: {result['dimensions']['width']}x{result['dimensions']['height']}")
        print(f"   Map type: {result['map_type']}")
        print(f"   Format: {result['format']}")
        print(f"   Base64 length: {len(result['image_base64'])} characters")
    else:
        print(f"❌ ERROR: {result.get('error')}")

def test_area_comparison():
    """Test area comparison for disaster analysis"""
    print("\n=== Testing Area Comparison ===")
    
    service = HEREImageService()
    
    # Mumbai flood-prone area
    lat, lon = 19.0760, 72.8777
    radius_km = 2.0
    
    print(f"Getting reference images for {radius_km}km radius around Mumbai...")
    result = service.get_area_comparison(lat, lon, radius_km, zoom=14)
    
    if result.get("success"):
        print("✅ SUCCESS!")
        print(f"   Coverage area: {result['coverage_area_km2']} km²")
        print(f"   Bounding box: N={result['bounding_box']['north']:.4f}, "
              f"S={result['bounding_box']['south']:.4f}, "
              f"E={result['bounding_box']['east']:.4f}, "
              f"W={result['bounding_box']['west']:.4f}")
    else:
        print(f"❌ ERROR: {result.get('error')}")

def test_via_api():
    """Test via FastAPI endpoint"""
    print("\n=== Testing via API Endpoint ===")
    
    url = "http://localhost:8000/api/here/reference-image"
    params = {
        "lat": 19.0760,
        "lon": 72.8777,
        "zoom": 15,
        "map_type": "satellite.day"
    }
    
    print(f"Calling API: {url}")
    try:
        response = requests.get(url, params=params, timeout=20)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ API SUCCESS!")
                print(f"   Location: {data['location']}")
                print(f"   Zoom: {data['zoom']}")
                print(f"   Image received: {len(data['image_base64'])} chars")
            else:
                print(f"❌ API returned error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("HERE Map Image API - Test Suite")
    print("=" * 60)
    
    # Test 1: Direct service call
    test_reference_image()
    
    # Test 2: Area comparison
    test_area_comparison()
    
    # Test 3: Via API endpoint (requires running backend)
    test_via_api()
    
    print("\n" + "=" * 60)
    print("Test suite completed!")
    print("=" * 60)
