#!/usr/bin/env python3
"""
Test authentication and token handling
"""
import requests
import json

BASE_URL = "http://localhost:5001"

def test_authentication():
    """Test the authentication flow"""
    print("1. Testing authentication...")
    auth_data = {"email": "user@example.com", "password": "user123"}
    response = requests.post(f"{BASE_URL}/api/v1/users/authenticate", json=auth_data)
    print(f"Auth response status: {response.status_code}")
    if response.status_code == 200:
        auth_result = response.json()
        print(f"Auth successful: {auth_result}")
        token = auth_result.get("token")
        user = auth_result.get("user")
        if token and user:
            print(f"Token: {token[:20]}...")
            print(f"User: {user.get('email')} (ID: {user.get('id')})")
            print("\n2. Testing file endpoints with token...")
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test file auth endpoint
            files_response = requests.get(f"{BASE_URL}/api/v1/files/test-auth", headers=headers)
            print(f"Files auth test status: {files_response.status_code}")
            print(f"Files auth test response: {files_response.text}")
            
            # Test file list endpoint
            files_list_response = requests.get(f"{BASE_URL}/api/v1/files/", headers=headers)
            print(f"Files list status: {files_list_response.status_code}")
            print(f"Files list response: {files_list_response.text}")
            
            # Test user endpoint
            user_response = requests.get(f"{BASE_URL}/api/v1/users/{user.get('id')}", headers=headers)
            print(f"User endpoint status: {user_response.status_code}")
            print(f"User endpoint response: {user_response.text}")
        else:
            print("No token or user in response")
    else:
        print(f"Authentication failed: {response.text}")

def test_health_endpoints():
    """Test health endpoints"""
    print("\n3. Testing health endpoints...")
    health_response = requests.get(f"{BASE_URL}/health")
    print(f"Health response: {health_response.json()}")
    
    db_response = requests.get(f"{BASE_URL}/test-db")
    print(f"Database test: {db_response.json()}")
    
    users_response = requests.get(f"{BASE_URL}/test-users")
    print(f"Users test: {users_response.json()}")
    
    auth_flow_response = requests.get(f"{BASE_URL}/test-auth-flow")
    print(f"Auth flow test: {auth_flow_response.json()}")
    
    token_test_response = requests.get(f"{BASE_URL}/test-token")
    print(f"Token test: {token_test_response.json()}")

if __name__ == "__main__":
    print("🧪 Testing Authentication and File API")
    print("=" * 50)
    test_health_endpoints()
    test_authentication()
