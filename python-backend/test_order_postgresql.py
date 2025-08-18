#!/usr/bin/env python3
"""
Test script to verify Order API with PostgreSQL integration
"""

import os
import sys
import requests
import json
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test configuration
API_BASE_URL = "http://localhost:5001/api/v1"
TEST_USER = {
    "email": "admin@example.com",
    "password": "admin123"
}

def get_auth_token():
    """Get authentication token"""
    response = requests.post(f"{API_BASE_URL}/auth/login", json=TEST_USER)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"❌ Failed to get auth token: {response.text}")
        return None

def test_create_customer():
    """Create a test customer first"""
    token = get_auth_token()
    if not token:
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    customer_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "address_line1": "123 Main St",
        "city": "Anytown",
        "state": "NY",
        "postal_code": "12345",
        "country": "USA"
    }
    
    response = requests.post(f"{API_BASE_URL}/customers/", json=customer_data, headers=headers)
    if response.status_code == 200:
        customer = response.json()
        print(f"✅ Customer created: {customer['customer_id']}")
        return customer
    else:
        print(f"❌ Failed to create customer: {response.text}")
        return None

def test_create_order(customer_id):
    """Test order creation"""
    token = get_auth_token()
    if not token:
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    order_data = {
        "customer_id": customer_id,
        "customer_name": "John Doe",
        "customer_email": "john.doe@example.com",
        "customer_phone": "+1234567890",
        "shipping_address": "123 Main St, Anytown, NY 12345, USA",
        "items": [
            {
                "product_id": "PROD_001",
                "product_name": "Test Product 1",
                "quantity": 2,
                "unit_price": 25.50,
                "total_price": 51.00
            },
            {
                "product_id": "PROD_002",
                "product_name": "Test Product 2",
                "quantity": 1,
                "unit_price": 15.75,
                "total_price": 15.75
            }
        ],
        "notes": "Test order for PostgreSQL integration"
    }
    
    response = requests.post(f"{API_BASE_URL}/orders/", json=order_data, headers=headers)
    if response.status_code == 200:
        order = response.json()
        print(f"✅ Order created: {order['id']}")
        print(f"   Customer: {order['customer_name']} ({order['customer_id']})")
        print(f"   Total: ${order['total_amount']}")
        print(f"   Status: {order['status']}")
        return order
    else:
        print(f"❌ Failed to create order: {response.text}")
        return None

def test_get_order(order_id):
    """Test getting order by ID"""
    token = get_auth_token()
    if not token:
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/orders/{order_id}", headers=headers)
    if response.status_code == 200:
        order = response.json()
        print(f"✅ Order retrieved: {order['id']}")
        print(f"   Items: {len(order['items'])}")
        return True
    else:
        print(f"❌ Failed to get order: {response.text}")
        return False

def test_get_customer_orders(customer_id):
    """Test getting orders by customer"""
    token = get_auth_token()
    if not token:
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/orders/customer/{customer_id}", headers=headers)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Customer orders retrieved: {result['total']} orders found")
        return True
    else:
        print(f"❌ Failed to get customer orders: {response.text}")
        return False

def test_update_order_status(order_id):
    """Test updating order status"""
    token = get_auth_token()
    if not token:
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.patch(f"{API_BASE_URL}/orders/{order_id}/status?status=confirmed", headers=headers)
    if response.status_code == 200:
        order = response.json()
        print(f"✅ Order status updated: {order['status']}")
        return True
    else:
        print(f"❌ Failed to update order status: {response.text}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Order API with PostgreSQL integration...")
    print("=" * 60)
    
    # Test 1: Create a customer
    print("\n1. Creating test customer...")
    customer = test_create_customer()
    if not customer:
        print("❌ Cannot proceed without customer")
        return
    
    # Test 2: Create an order
    print("\n2. Creating test order...")
    order = test_create_order(customer['customer_id'])
    if not order:
        print("❌ Cannot proceed without order")
        return
    
    # Test 3: Get order by ID
    print("\n3. Retrieving order by ID...")
    test_get_order(order['id'])
    
    # Test 4: Get orders by customer
    print("\n4. Retrieving orders by customer...")
    test_get_customer_orders(customer['customer_id'])
    
    # Test 5: Update order status
    print("\n5. Updating order status...")
    test_update_order_status(order['id'])
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")

if __name__ == "__main__":
    main()
