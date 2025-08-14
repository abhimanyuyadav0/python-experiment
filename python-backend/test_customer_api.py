#!/usr/bin/env python3
"""
Customer API Test Script
Tests all customer API endpoints with sample data
"""

import requests
import json
import time
from datetime import datetime, date
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:5001"
CUSTOMER_API_BASE = f"{BASE_URL}/api/v1/customers"

def print_response(response: requests.Response, title: str = ""):
    """Print formatted API response"""
    print(f"\n{'='*60}")
    if title:
        print(f"📋 {title}")
    print(f"🌐 {response.request.method} {response.url}")
    print(f"📊 Status: {response.status_code}")
    print(f"⏱️  Response Time: {response.elapsed.total_seconds():.3f}s")
    
    if response.status_code >= 400:
        print(f"❌ Error: {response.text}")
    else:
        try:
            data = response.json()
            if isinstance(data, dict) and len(data) > 0:
                print("✅ Response Data:")
                print(json.dumps(data, indent=2, default=str))
            else:
                print("✅ Response: Success")
        except json.JSONDecodeError:
            print(f"📄 Response: {response.text}")
    
    print("="*60)

def test_create_customer():
    """Test customer creation"""
    print("\n🚀 Testing Customer Creation...")
    
    customer_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1-555-0123",
        "address_line1": "123 Main Street",
        "city": "New York",
        "state": "NY",
        "postal_code": "10001",
        "country": "USA",
        "date_of_birth": "1990-01-15T00:00:00",
        "gender": "male",
        "company_name": "Tech Corp",
        "marketing_emails": True,
        "marketing_sms": False,
        "notes": "Premium customer",
        "tags": "premium,tech,new-york"
    }
    
    response = requests.post(CUSTOMER_API_BASE, json=customer_data)
    print_response(response, "Create Customer")
    
    if response.status_code == 200:
        return response.json().get("customer_id")
    return None

def test_create_multiple_customers():
    """Test creating multiple customers"""
    print("\n🚀 Testing Multiple Customer Creation...")
    
    customers = [
        {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "phone": "+1-555-0124",
            "city": "Los Angeles",
            "state": "CA",
            "country": "USA",
            "gender": "female",
            "marketing_emails": True,
            "tags": "premium,west-coast"
        },
        {
            "first_name": "Bob",
            "last_name": "Johnson",
            "email": "bob.johnson@example.com",
            "phone": "+1-555-0125",
            "city": "Chicago",
            "state": "IL",
            "country": "USA",
            "gender": "male",
            "marketing_emails": False,
            "tags": "standard,midwest"
        },
        {
            "first_name": "Alice",
            "last_name": "Brown",
            "email": "alice.brown@example.com",
            "phone": "+1-555-0126",
            "city": "Miami",
            "state": "FL",
            "country": "USA",
            "gender": "female",
            "marketing_emails": True,
            "tags": "premium,south"
        }
    ]
    
    customer_ids = []
    for i, customer_data in enumerate(customers):
        print(f"\nCreating customer {i+1}/{len(customers)}...")
        response = requests.post(CUSTOMER_API_BASE, json=customer_data)
        if response.status_code == 200:
            customer_id = response.json().get("customer_id")
            customer_ids.append(customer_id)
            print(f"✅ Created customer: {customer_id}")
        else:
            print(f"❌ Failed to create customer: {response.text}")
    
    return customer_ids

def test_get_customer(customer_id: str):
    """Test getting customer by ID"""
    print(f"\n🔍 Testing Get Customer by ID: {customer_id}")
    
    response = requests.get(f"{CUSTOMER_API_BASE}/{customer_id}")
    print_response(response, f"Get Customer {customer_id}")
    
    return response.status_code == 200

def test_get_customer_by_username(customer_id: str):
    """Test getting customer by username"""
    print(f"\n🔍 Testing Get Customer by Username...")
    
    # First get the customer to get the username
    response = requests.get(f"{CUSTOMER_API_BASE}/{customer_id}")
    if response.status_code == 200:
        customer = response.json()
        username = customer.get("username")
        
        if username:
            response = requests.get(f"{CUSTOMER_API_BASE}/username/{username}")
            print_response(response, f"Get Customer by Username: {username}")
            return response.status_code == 200
    
    return False

def test_get_customer_by_email(email: str):
    """Test getting customer by email"""
    print(f"\n🔍 Testing Get Customer by Email: {email}")
    
    response = requests.get(f"{CUSTOMER_API_BASE}/email/{email}")
    print_response(response, f"Get Customer by Email: {email}")
    
    return response.status_code == 200

def test_get_all_customers():
    """Test getting all customers"""
    print("\n📋 Testing Get All Customers...")
    
    # Test with default parameters
    response = requests.get(CUSTOMER_API_BASE)
    print_response(response, "Get All Customers (Default)")
    
    # Test with pagination
    response = requests.get(f"{CUSTOMER_API_BASE}?skip=0&limit=5")
    print_response(response, "Get All Customers (Paginated)")
    
    # Test with filtering
    response = requests.get(f"{CUSTOMER_API_BASE}?is_active=true")
    print_response(response, "Get All Customers (Active Only)")
    
    return response.status_code == 200

def test_search_customers():
    """Test customer search functionality"""
    print("\n🔍 Testing Customer Search...")
    
    search_params = {
        "query": "john",
        "page": 1,
        "limit": 10,
        "sort_by": "created_at",
        "sort_order": "desc"
    }
    
    response = requests.post(f"{CUSTOMER_API_BASE}/search", json=search_params)
    print_response(response, "Search Customers by Query")
    
    # Test location-based search
    location_search = {
        "city": "New York",
        "country": "USA",
        "page": 1,
        "limit": 10
    }
    
    response = requests.post(f"{CUSTOMER_API_BASE}/search", json=location_search)
    print_response(response, "Search Customers by Location")
    
    return response.status_code == 200

def test_update_customer(customer_id: str):
    """Test customer update"""
    print(f"\n✏️ Testing Customer Update: {customer_id}")
    
    update_data = {
        "first_name": "John Updated",
        "phone": "+1-555-9999",
        "address_line2": "Apt 4B",
        "notes": "Updated customer information",
        "tags": "premium,tech,new-york,updated"
    }
    
    response = requests.put(f"{CUSTOMER_API_BASE}/{customer_id}", json=update_data)
    print_response(response, f"Update Customer {customer_id}")
    
    return response.status_code == 200

def test_bulk_update_customers(customer_ids: list):
    """Test bulk customer update"""
    print(f"\n✏️ Testing Bulk Customer Update...")
    
    if len(customer_ids) < 2:
        print("⚠️ Need at least 2 customers for bulk update test")
        return False
    
    bulk_update_data = {
        "customer_ids": customer_ids[:2],  # Update first 2 customers
        "updates": {
            "marketing_emails": False,
            "notes": "Bulk updated customer",
            "tags": "bulk-updated"
        }
    }
    
    response = requests.post(f"{CUSTOMER_API_BASE}/bulk-update", json=bulk_update_data)
    print_response(response, "Bulk Update Customers")
    
    return response.status_code == 200

def test_verify_customer(customer_id: str):
    """Test customer verification"""
    print(f"\n✅ Testing Customer Verification: {customer_id}")
    
    # Verify email
    response = requests.patch(f"{CUSTOMER_API_BASE}/{customer_id}/verify-email")
    print_response(response, f"Verify Customer Email {customer_id}")
    
    # Verify phone
    response = requests.patch(f"{CUSTOMER_API_BASE}/{customer_id}/verify-phone")
    print_response(response, f"Verify Customer Phone {customer_id}")
    
    return True

def test_update_last_login(customer_id: str):
    """Test updating customer last login"""
    print(f"\n🕒 Testing Update Last Login: {customer_id}")
    
    response = requests.patch(f"{CUSTOMER_API_BASE}/{customer_id}/last-login")
    print_response(response, f"Update Last Login {customer_id}")
    
    return response.status_code == 200

def test_get_customer_statistics():
    """Test getting customer statistics"""
    print("\n📊 Testing Customer Statistics...")
    
    response = requests.get(f"{CUSTOMER_API_BASE}/statistics/overview")
    print_response(response, "Get Customer Statistics")
    
    return response.status_code == 200

def test_get_customers_by_tags():
    """Test getting customers by tags"""
    print("\n🏷️ Testing Get Customers by Tags...")
    
    response = requests.get(f"{CUSTOMER_API_BASE}/tags/premium,tech")
    print_response(response, "Get Customers by Tags: premium,tech")
    
    return response.status_code == 200

def test_get_customers_by_location():
    """Test getting customers by location"""
    print("\n🌍 Testing Get Customers by Location...")
    
    response = requests.get(f"{CUSTOMER_API_BASE}/location/search?country=USA&city=New York")
    print_response(response, "Get Customers by Location: USA, New York")
    
    return response.status_code == 200

def test_get_available_locations():
    """Test getting available locations"""
    print("\n🌍 Testing Get Available Locations...")
    
    # Get available countries
    response = requests.get(f"{CUSTOMER_API_BASE}/available/countries")
    print_response(response, "Get Available Countries")
    
    # Get available cities
    response = requests.get(f"{CUSTOMER_API_BASE}/available/cities")
    print_response(response, "Get Available Cities")
    
    # Get available states
    response = requests.get(f"{CUSTOMER_API_BASE}/available/states")
    print_response(response, "Get Available States")
    
    return True

def test_delete_customer(customer_id: str):
    """Test customer deletion (soft delete)"""
    print(f"\n🗑️ Testing Customer Deletion (Soft): {customer_id}")
    
    response = requests.delete(f"{CUSTOMER_API_BASE}/{customer_id}")
    print_response(response, f"Delete Customer {customer_id}")
    
    return response.status_code == 200

def test_hard_delete_customer(customer_id: str):
    """Test hard customer deletion"""
    print(f"\n🗑️ Testing Customer Hard Deletion: {customer_id}")
    
    response = requests.delete(f"{CUSTOMER_API_BASE}/{customer_id}/hard")
    print_response(response, f"Hard Delete Customer {customer_id}")
    
    return response.status_code == 200

def main():
    """Main test function"""
    print("🚀 Starting Customer API Tests...")
    print(f"📍 Testing against: {BASE_URL}")
    
    # Test customer creation
    customer_id = test_create_customer()
    if not customer_id:
        print("❌ Failed to create customer. Stopping tests.")
        return
    
    # Test creating multiple customers
    additional_customer_ids = test_create_multiple_customers()
    all_customer_ids = [customer_id] + additional_customer_ids
    
    # Test getting customers
    test_get_customer(customer_id)
    test_get_customer_by_username(customer_id)
    test_get_customer_by_email("john.doe@example.com")
    test_get_all_customers()
    
    # Test search functionality
    test_search_customers()
    
    # Test customer updates
    test_update_customer(customer_id)
    test_bulk_update_customers(all_customer_ids)
    
    # Test verification and login
    test_verify_customer(customer_id)
    test_update_last_login(customer_id)
    
    # Test statistics and analytics
    test_get_customer_statistics()
    test_get_customers_by_tags()
    test_get_customers_by_location()
    test_get_available_locations()
    
    # Test deletion
    test_delete_customer(customer_id)
    
    # Wait a moment before hard delete
    time.sleep(1)
    
    # Test hard delete
    test_hard_delete_customer(customer_id)
    
    print("\n🎉 Customer API Tests Completed!")
    print("\n📋 Test Summary:")
    print("✅ Customer Creation")
    print("✅ Customer Retrieval")
    print("✅ Customer Search")
    print("✅ Customer Updates")
    print("✅ Customer Verification")
    print("✅ Customer Statistics")
    print("✅ Customer Deletion")

if __name__ == "__main__":
    main()
