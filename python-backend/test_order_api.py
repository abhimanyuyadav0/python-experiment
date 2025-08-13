#!/usr/bin/env python3
"""
Test script for the Order API
Make sure MongoDB is running and the server is started before running this script
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:5001/api/v1"

def test_create_order():
    """Test creating a new order"""
    print("🧪 Testing order creation...")
    
    order_data = {
        "customer_id": "cust_001",
        "customer_name": "John Doe",
        "customer_email": "john.doe@example.com",
        "customer_phone": "+1234567890",
        "shipping_address": "123 Main St, City, State 12345",
        "items": [
            {
                "product_id": "prod_001",
                "product_name": "Laptop",
                "quantity": 1,
                "unit_price": 999.99,
                "total_price": 999.99
            },
            {
                "product_id": "prod_002",
                "product_name": "Mouse",
                "quantity": 2,
                "unit_price": 25.99,
                "total_price": 51.98
            }
        ],
        "notes": "Please deliver during business hours"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/orders/", json=order_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            order = response.json()
            print("✅ Order created successfully!")
            print(f"Order ID: {order['id']}")
            print(f"Total Amount: ${order['total_amount']}")
            print(f"Status: {order['status']}")
            return order['id']
        else:
            print(f"❌ Failed to create order: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating order: {str(e)}")
        return None

def test_get_order(order_id):
    """Test retrieving an order by ID"""
    if not order_id:
        print("❌ No order ID to test")
        return
    
    print(f"\n🧪 Testing order retrieval for ID: {order_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/orders/{order_id}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            order = response.json()
            print("✅ Order retrieved successfully!")
            print(f"Customer: {order['customer_name']}")
            print(f"Items: {len(order['items'])}")
            print(f"Total: ${order['total_amount']}")
        else:
            print(f"❌ Failed to retrieve order: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving order: {str(e)}")

def test_get_orders():
    """Test retrieving all orders"""
    print("\n🧪 Testing order list retrieval...")
    
    try:
        response = requests.get(f"{BASE_URL}/orders/")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Orders retrieved successfully!")
            print(f"Total Orders: {result['total']}")
            print(f"Page: {result['page']}")
            print(f"Page Size: {result['size']}")
            
            if result['orders']:
                print("Sample Orders:")
                for order in result['orders'][:3]:  # Show first 3 orders
                    print(f"  - {order['id']}: {order['customer_name']} - ${order['total_amount']}")
        else:
            print(f"❌ Failed to retrieve orders: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving orders: {str(e)}")

def test_update_order_status(order_id):
    """Test updating order status"""
    if not order_id:
        print("❌ No order ID to test")
        return
    
    print(f"\n🧪 Testing order status update for ID: {order_id}")
    
    try:
        # Update status to confirmed
        response = requests.patch(f"{BASE_URL}/orders/{order_id}/status?status=confirmed")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            order = response.json()
            print("✅ Order status updated successfully!")
            print(f"New Status: {order['status']}")
            print(f"Updated At: {order['updated_at']}")
        else:
            print(f"❌ Failed to update order status: {response.text}")
    except Exception as e:
        print(f"❌ Error updating order status: {str(e)}")

def test_customer_orders():
    """Test retrieving orders for a specific customer"""
    print("\n🧪 Testing customer orders retrieval...")
    
    try:
        response = requests.get(f"{BASE_URL}/orders/customer/cust_001")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Customer orders retrieved successfully!")
            print(f"Total Orders: {result['total']}")
            
            if result['orders']:
                print("Customer Orders:")
                for order in result['orders']:
                    print(f"  - {order['id']}: ${order['total_amount']} - {order['status']}")
        else:
            print(f"❌ Failed to retrieve customer orders: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving customer orders: {str(e)}")

def test_health_endpoints():
    """Test health check endpoints"""
    print("\n🧪 Testing health check endpoints...")
    
    try:
        # Test general health
        response = requests.get("http://localhost:5001/health")
        print(f"General Health Status: {response.status_code}")
        
        # Test MongoDB health
        response = requests.get("http://localhost:5001/health/mongodb")
        print(f"MongoDB Health Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ MongoDB is healthy!")
        else:
            print("❌ MongoDB health check failed")
            
    except Exception as e:
        print(f"❌ Error checking health: {str(e)}")

def main():
    """Run all tests"""
    print("🚀 Starting Order API Tests...")
    print("=" * 50)
    
    # Test health endpoints first
    test_health_endpoints()
    
    # Test order operations
    order_id = test_create_order()
    test_get_order(order_id)
    test_get_orders()
    test_update_order_status(order_id)
    test_customer_orders()
    
    print("\n" + "=" * 50)
    print("🏁 Order API tests completed!")
    
    if order_id:
        print(f"📝 Created test order with ID: {order_id}")
        print("💡 You can use this ID to test other operations manually")

if __name__ == "__main__":
    main()
