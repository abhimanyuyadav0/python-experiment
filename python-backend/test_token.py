#!/usr/bin/env python3
"""
Test JWT token creation and expiration
"""

from app.services.user_service import create_access_token, verify_token
from datetime import datetime, timedelta

def test_token_creation():
    print("🧪 Testing JWT Token Creation and Expiration...")
    
    # Test 1: Create token with default expiration (5 minutes)
    print("\n1. Creating token with default expiration (5 minutes):")
    token, expires_at = create_access_token(data={"test": "data"})
    print(f"   Token: {token[:50]}...")
    print(f"   Expires at: {expires_at}")
    
    # Convert to datetime for readability
    expire_time = datetime.fromtimestamp(expires_at)
    now = datetime.utcnow()
    time_until_expiry = expire_time - now
    
    print(f"   Expire time: {expire_time}")
    print(f"   Time until expiry: {time_until_expiry.total_seconds():.0f} seconds")
    
    # Test 2: Verify token is valid
    print("\n2. Verifying token is valid:")
    payload = verify_token(token)
    print(f"   Token valid: {payload is not None}")
    if payload:
        print(f"   Payload: {payload}")
    
    # Test 3: Create token with custom expiration (1 minute)
    print("\n3. Creating token with custom expiration (1 minute):")
    custom_token, custom_expires_at = create_access_token(
        data={"test": "custom"}, 
        expires_delta=timedelta(minutes=1)
    )
    print(f"   Token: {custom_token[:50]}...")
    print(f"   Expires at: {custom_expires_at}")
    
    custom_expire_time = datetime.fromtimestamp(custom_expires_at)
    custom_time_until_expiry = custom_expire_time - now
    print(f"   Expire time: {custom_expire_time}")
    print(f"   Time until expiry: {custom_time_until_expiry.total_seconds():.0f} seconds")
    
    # Test 4: Verify custom token
    print("\n4. Verifying custom token:")
    custom_payload = verify_token(custom_token)
    print(f"   Token valid: {custom_payload is not None}")
    
    print("\n✅ Token tests completed!")

if __name__ == "__main__":
    test_token_creation()
