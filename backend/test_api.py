"""
Simple test script to verify all API endpoints are working
Run: python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, description, data=None):
    """Test a single endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Endpoint: {method} {endpoint}")
    print(f"{'='*60}")
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success!")
            print(f"Response Preview: {json.dumps(result, indent=2)[:500]}...")
            return True
        else:
            print(f"❌ Failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("DIMP API Test Suite")
    print("="*60)
    
    tests = [
        ("GET", "/", "Root endpoint"),
        ("GET", "/api/disaster-zones", "Get disaster zones"),
        ("GET", "/api/flood-areas", "Get flood areas"),
        ("GET", "/api/infrastructure-damage", "Get infrastructure damage"),
        ("GET", "/api/population-displacement", "Get displacement data"),
        ("GET", "/api/alerts", "Get active alerts"),
        ("GET", "/api/social-feed", "Get social media feed"),
        ("GET", "/api/statistics", "Get statistics"),
        ("GET", "/api/here-config", "Get HERE configuration"),
        ("POST", "/api/analyze-social-media", "Analyze social media post", {
            "text": "Urgent! Building collapsed at Connaught Place. People trapped!",
            "location": "Connaught Place",
            "timestamp": "2025-10-10T19:00:00"
        })
    ]
    
    results = []
    for test in tests:
        if len(test) == 3:
            method, endpoint, description = test
            data = None
        else:
            method, endpoint, description, data = test
        
        success = test_endpoint(method, endpoint, description, data)
        results.append((description, success))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {description}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! API is ready!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the backend.")

if __name__ == "__main__":
    print("\n⚠️  Make sure the backend is running (python main.py)")
    input("Press Enter to start tests...")
    main()
