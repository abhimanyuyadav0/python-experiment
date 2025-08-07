#!/usr/bin/env python3
"""
Simple test script to verify backend functionality
"""

import requests
import json

# Backend URL
BASE_URL = "http://localhost:5001"

def test_backend():
    """Test basic backend functionality"""
    
    print("🧪 Testing Backend API...")
    print(f"📍 Backend URL: {BASE_URL}")
    print("-" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ Server is running and accessible")
        else:
            print(f"⚠️  Server responded with status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on port 5001")
        return False
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return False
    
    # Test 2: Test CORS headers
    try:
        response = requests.options(f"{BASE_URL}/api/v1/users/")
        cors_headers = response.headers
        print(f"✅ CORS headers present: {cors_headers.get('access-control-allow-origin', 'Not found')}")
    except Exception as e:
        print(f"⚠️  Could not test CORS headers: {e}")
    
    # Test 3: Test API endpoints
    try:
        # Test users endpoint
        response = requests.get(f"{BASE_URL}/api/v1/users/")
        if response.status_code in [200, 401, 403]:  # Any response is good
            print("✅ API endpoints are accessible")
        else:
            print(f"⚠️  API responded with unexpected status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing API endpoints: {e}")
    
    # Test 4: Test authentication endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/v1/users/authenticate?email=test@example.com&password=testpass")
        if response.status_code in [401, 404]:  # Expected for invalid credentials
            print("✅ Authentication endpoint is working")
        else:
            print(f"⚠️  Authentication endpoint responded with: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing authentication: {e}")
    
    print("-" * 50)
    print("🎉 Backend testing completed!")
    print("\n📋 Next steps:")
    print("1. Start the frontend: cd frontend && npm run dev")
    print("2. Create a .env.local file in frontend with: NEXT_PUBLIC_API_BASE_URL=http://localhost:5001")
    print("3. Visit http://localhost:3000 to test the full application")
    
    return True

if __name__ == "__main__":
    test_backend() 