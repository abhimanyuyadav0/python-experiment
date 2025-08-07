#!/usr/bin/env python3
"""
Example usage of the FastAPI User API
This script demonstrates how to interact with all the user endpoints
"""

import requests
import json
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def make_request(method: str, endpoint: str, data: Dict[Any, Any] = None, params: Dict[str, Any] = None) -> Dict[Any, Any]:
    """Helper function to make HTTP requests"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, params=params)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data)
        elif method.upper() == "PATCH":
            response = requests.patch(url, json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response.json() if response.content else {"message": "Success"}
        
    except requests.exceptions.RequestException as e:
        print(f"Error making {method} request to {endpoint}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None

def main():
    """Main function demonstrating API usage"""
    print("🚀 FastAPI User API Example Usage\n")
    
    # 1. Create a new user
    print("1. Creating a new user...")
    new_user = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securepassword123",
        "is_active": True
    }
    
    created_user = make_request("POST", "/users/", data=new_user)
    if created_user:
        print(f"✅ User created: {created_user['name']} (ID: {created_user['id']})")
        user_id = created_user['id']
    else:
        print("❌ Failed to create user")
        return
    
    print()
    
    # 2. Get all users (paginated)
    print("2. Getting all users...")
    users_response = make_request("GET", "/users/", params={"page": 1, "per_page": 10})
    if users_response:
        print(f"✅ Found {users_response['total']} users")
        for user in users_response['users']:
            print(f"   - {user['name']} ({user['email']})")
    else:
        print("❌ Failed to get users")
    
    print()
    
    # 3. Get user by ID
    print(f"3. Getting user by ID ({user_id})...")
    user_by_id = make_request("GET", f"/users/{user_id}")
    if user_by_id:
        print(f"✅ User found: {user_by_id['name']} ({user_by_id['email']})")
    else:
        print("❌ Failed to get user by ID")
    
    print()
    
    # 4. Get user by email
    print("4. Getting user by email...")
    user_by_email = make_request("GET", f"/users/email/{new_user['email']}")
    if user_by_email:
        print(f"✅ User found by email: {user_by_email['name']}")
    else:
        print("❌ Failed to get user by email")
    
    print()
    
    # 5. Update user
    print("5. Updating user...")
    update_data = {
        "name": "John Smith",
        "email": "john.smith@example.com"
    }
    updated_user = make_request("PUT", f"/users/{user_id}", data=update_data)
    if updated_user:
        print(f"✅ User updated: {updated_user['name']} ({updated_user['email']})")
    else:
        print("❌ Failed to update user")
    
    print()
    
    # 6. Partial update user
    print("6. Partially updating user...")
    partial_update = {
        "is_active": False
    }
    partially_updated_user = make_request("PATCH", f"/users/{user_id}", data=partial_update)
    if partially_updated_user:
        print(f"✅ User partially updated: is_active = {partially_updated_user['is_active']}")
    else:
        print("❌ Failed to partially update user")
    
    print()
    
    # 7. Authenticate user
    print("7. Authenticating user...")
    auth_params = {
        "email": "john.smith@example.com",
        "password": "securepassword123"
    }
    auth_user = make_request("POST", "/users/authenticate", params=auth_params)
    if auth_user:
        print(f"✅ User authenticated: {auth_user['name']}")
    else:
        print("❌ Failed to authenticate user")
    
    print()
    
    # 8. Create another user for demonstration
    print("8. Creating another user...")
    second_user = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "password": "anotherpassword123",
        "is_active": True
    }
    
    created_second_user = make_request("POST", "/users/", data=second_user)
    if created_second_user:
        print(f"✅ Second user created: {created_second_user['name']} (ID: {created_second_user['id']})")
        second_user_id = created_second_user['id']
    else:
        print("❌ Failed to create second user")
        second_user_id = None
    
    print()
    
    # 9. Get users with filter
    print("9. Getting active users only...")
    active_users = make_request("GET", "/users/", params={"is_active": True, "page": 1, "per_page": 10})
    if active_users:
        print(f"✅ Found {active_users['total']} active users")
        for user in active_users['users']:
            print(f"   - {user['name']} (Active: {user['is_active']})")
    else:
        print("❌ Failed to get active users")
    
    print()
    
    # 10. Delete users
    print("10. Cleaning up - deleting users...")
    if second_user_id:
        delete_result = make_request("DELETE", f"/users/{second_user_id}")
        if delete_result:
            print(f"✅ Second user deleted")
        else:
            print("❌ Failed to delete second user")
    
    delete_result = make_request("DELETE", f"/users/{user_id}")
    if delete_result:
        print(f"✅ First user deleted")
    else:
        print("❌ Failed to delete first user")
    
    print()
    print("🎉 API demonstration completed!")

if __name__ == "__main__":
    main() 