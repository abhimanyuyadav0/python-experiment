#!/usr/bin/env python3
"""
Test script for file upload API
"""

import requests
import json
import os
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:5001"

def login_user(email: str, password: str):
    """Login and get access token"""
    login_data = {
        "email": email,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/users/authenticate", json=login_data)
    if response.status_code == 200:
        return response.json()["token"]
    else:
        print(f"Login failed: {response.text}")
        return None

def upload_file(token: str, file_path: str):
    """Upload a file"""
    headers = {"Authorization": f"Bearer {token}"}
    
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "application/octet-stream")}
        response = requests.post(f"{BASE_URL}/api/v1/files/upload", headers=headers, files=files)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Upload failed: {response.text}")
        return None

def get_user_files(token: str):
    """Get all files for the user"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/v1/files/", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Get files failed: {response.text}")
        return None

def main():
    print("🧪 Testing File Upload API")
    print("=" * 50)
    
    # Login as regular user
    print("1. Logging in as user@example.com...")
    token = login_user("user@example.com", "user123")
    if not token:
        print("❌ Login failed. Make sure the server is running and user exists.")
        return
    
    print("✅ Login successful!")
    
    # Create a test file
    test_file_path = "test_document.txt"
    with open(test_file_path, "w") as f:
        f.write("This is a test document for file upload API testing.")
    
    print(f"2. Uploading test file: {test_file_path}")
    upload_result = upload_file(token, test_file_path)
    
    if upload_result:
        print("✅ File uploaded successfully!")
        print(f"   File ID: {upload_result['file']['id']}")
        print(f"   Original Name: {upload_result['file']['original_filename']}")
        print(f"   File Type: {upload_result['file']['file_type']}")
        print(f"   File Size: {upload_result['file']['file_size']} bytes")
        print(f"   Access URL: {upload_result['file']['url']}")
    else:
        print("❌ File upload failed!")
        return
    
    # Get user files
    print("\n3. Getting user files...")
    files_result = get_user_files(token)
    
    if files_result:
        print(f"✅ Found {files_result['total']} files:")
        for file in files_result['files']:
            print(f"   - {file['original_filename']} ({file['file_type']}) - {file['file_size']} bytes")
    else:
        print("❌ Failed to get user files!")
    
    # Clean up test file
    if os.path.exists(test_file_path):
        os.remove(test_file_path)
    
    print("\n🎉 File upload API test completed!")

if __name__ == "__main__":
    main()
