#!/usr/bin/env python3
"""
Test login endpoint to see what token data is returned
"""

import requests
import json
from datetime import datetime

def test_login():
    print("🧪 Testing Login Endpoint...")
    
    # Test login with default admin user
    login_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            "http://localhost:5001/api/v1/users/authenticate",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"Token: {data['token'][:50]}...")
            print(f"Expires at: {data['expires_at']}")
            
            # Convert to datetime for readability
            expire_time = datetime.fromtimestamp(data['expires_at'])
            now = datetime.utcnow()
            time_until_expiry = expire_time - now
            
            print(f"Expire time: {expire_time}")
            print(f"Time until expiry: {time_until_expiry.total_seconds():.0f} seconds")
            print(f"User: {data['user']['name']} ({data['user']['email']})")
            
            # Test token verification
            from app.services.user_service import verify_token
            payload = verify_token(data['token'])
            print(f"Token valid: {payload is not None}")
            if payload:
                print(f"Token payload: {payload}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_login()
