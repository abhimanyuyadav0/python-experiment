#!/usr/bin/env python3
"""
Test script for the Payment API
Make sure MongoDB is running and the server is started before running this script
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:5001/api/v1"

def test_create_payment():
    """Test creating a new payment"""
    print("🧪 Testing payment creation...")
    
    payment_data = {
        "order_id": "order_123",
        "customer_id": "customer_456",
        "amount": 99.99,
        "currency": "USD",
        "payment_method": {
            "method_type": "credit_card",
            "provider": "stripe",
            "account_id": "acct_123456",
            "last_four": "4242",
            "expiry_month": 12,
            "expiry_year": 2025,
            "card_brand": "Visa"
        },
        "description": "Payment for premium subscription",
        "metadata": {
            "subscription_type": "premium",
            "billing_cycle": "monthly"
        },
        "capture_method": "automatic",
        "statement_descriptor": "PREMIUM SUB",
        "receipt_email": "customer@example.com",
        "application_fee_amount": 2.99
    }
    
    try:
        response = requests.post(f"{BASE_URL}/payments/", json=payment_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            payment = response.json()
            print("✅ Payment created successfully!")
            print(f"Payment ID: {payment['id']}")
            print(f"Order ID: {payment['order_id']}")
            print(f"Amount: ${payment['amount']} {payment['currency']}")
            print(f"Status: {payment['status']}")
            print(f"Net Amount: ${payment['net_amount']}")
            return payment['id']
        else:
            print(f"❌ Failed to create payment: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating payment: {str(e)}")
        return None

def test_create_second_payment():
    """Test creating a second payment"""
    print("\n🧪 Testing second payment creation...")
    
    payment_data = {
        "order_id": "order_124",
        "customer_id": "customer_456",
        "amount": 149.99,
        "currency": "USD",
        "payment_method": {
            "method_type": "digital_wallet",
            "provider": "paypal",
            "account_id": "paypal_123456",
            "wallet_type": "PayPal"
        },
        "description": "Payment for annual plan",
        "metadata": {
            "plan_type": "annual",
            "discount": "20%"
        },
        "capture_method": "manual",
        "receipt_email": "customer@example.com"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/payments/", json=payment_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            payment = response.json()
            print("✅ Second payment created successfully!")
            print(f"Payment ID: {payment['id']}")
            print(f"Amount: ${payment['amount']}")
            return payment['id']
        else:
            print(f"❌ Failed to create second payment: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating second payment: {str(e)}")
        return None

def test_get_payment(payment_id):
    """Test retrieving a payment by ID"""
    if not payment_id:
        print("❌ No payment ID to test")
        return
    
    print(f"\n🧪 Testing payment retrieval for ID: {payment_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/payments/{payment_id}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            payment = response.json()
            print("✅ Payment retrieved successfully!")
            print(f"Order ID: {payment['order_id']}")
            print(f"Customer ID: {payment['customer_id']}")
            print(f"Amount: ${payment['amount']} {payment['currency']}")
            print(f"Status: {payment['status']}")
            print(f"Payment Method: {payment['payment_method']['method_type']}")
        else:
            print(f"❌ Failed to retrieve payment: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving payment: {str(e)}")

def test_get_payments_by_order():
    """Test retrieving payments by order ID"""
    print("\n🧪 Testing payments by order retrieval...")
    
    try:
        response = requests.get(f"{BASE_URL}/payments/order/order_123")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            payments = response.json()
            print("✅ Payments by order retrieved successfully!")
            print(f"Found {len(payments)} payments for order")
            
            for payment in payments:
                print(f"  - {payment['id']}: ${payment['amount']} ({payment['status']})")
        else:
            print(f"❌ Failed to retrieve payments by order: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving payments by order: {str(e)}")

def test_get_payments_by_customer():
    """Test retrieving payments by customer ID"""
    print("\n🧪 Testing payments by customer retrieval...")
    
    try:
        response = requests.get(f"{BASE_URL}/payments/customer/customer_456?limit=5")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Payments by customer retrieved successfully!")
            print(f"Total Payments: {result['total']}")
            print(f"Page: {result['page']}")
            print(f"Page Size: {result['size']}")
            
            if result['payments']:
                print("Customer Payments:")
                for payment in result['payments']:
                    print(f"  - {payment['id']}: ${payment['amount']} - {payment['status']}")
        else:
            print(f"❌ Failed to retrieve payments by customer: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving payments by customer: {str(e)}")

def test_search_payments():
    """Test payment search functionality"""
    print("\n🧪 Testing payment search...")
    
    search_params = {
        "status": "pending",
        "currency": "USD",
        "min_amount": 50,
        "max_amount": 200,
        "sort_by": "amount",
        "sort_order": "desc"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/payments/search", json=search_params)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Payment search successful!")
            print(f"Found {result['total']} payments matching criteria")
            
            if result['payments']:
                print("Search Results:")
                for payment in result['payments']:
                    print(f"  - {payment['id']}: ${payment['amount']} ({payment['status']})")
        else:
            print(f"❌ Failed to search payments: {response.text}")
    except Exception as e:
        print(f"❌ Error searching payments: {str(e)}")

def test_update_payment_status(payment_id):
    """Test updating payment status"""
    if not payment_id:
        print("❌ No payment ID to test")
        return
    
    print(f"\n🧪 Testing payment status update for ID: {payment_id}")
    
    try:
        # Update status to processing
        response = requests.patch(f"{BASE_URL}/payments/{payment_id}/status?status=processing&provider_payment_id=pi_123456")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Payment status updated successfully!")
            print(f"Message: {result['message']}")
        else:
            print(f"❌ Failed to update payment status: {response.text}")
    except Exception as e:
        print(f"❌ Error updating payment status: {str(e)}")

def test_process_payment(payment_id):
    """Test processing a payment"""
    if not payment_id:
        print("❌ No payment ID to test")
        return
    
    print(f"\n🧪 Testing payment processing for ID: {payment_id}")
    
    try:
        process_data = {
            "provider_payment_id": "pi_123456",
            "provider_fee_amount": 1.99
        }
        
        response = requests.post(f"{BASE_URL}/payments/{payment_id}/process", json=process_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Payment processed successfully!")
            print(f"Message: {result['message']}")
        else:
            print(f"❌ Failed to process payment: {response.text}")
    except Exception as e:
        print(f"❌ Error processing payment: {str(e)}")

def test_create_refund(payment_id):
    """Test creating a refund"""
    if not payment_id:
        print("❌ No payment ID to test")
        return
    
    print(f"\n🧪 Testing refund creation for payment ID: {payment_id}")
    
    refund_data = {
        "payment_id": payment_id,
        "amount": 49.99,
        "reason": "Customer requested partial refund",
        "metadata": {
            "refund_type": "partial",
            "requested_by": "customer"
        },
        "receipt_email": "customer@example.com"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/payments/refunds", json=refund_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            refund = response.json()
            print("✅ Refund created successfully!")
            print(f"Refund ID: {refund['id']}")
            print(f"Amount: ${refund['amount']}")
            print(f"Status: {refund['status']}")
            return refund['id']
        else:
            print(f"❌ Failed to create refund: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating refund: {str(e)}")
        return None

def test_get_refund(refund_id):
    """Test retrieving a refund by ID"""
    if not refund_id:
        print("❌ No refund ID to test")
        return
    
    print(f"\n🧪 Testing refund retrieval for ID: {refund_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/payments/refunds/{refund_id}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            refund = response.json()
            print("✅ Refund retrieved successfully!")
            print(f"Payment ID: {refund['payment_id']}")
            print(f"Amount: ${refund['amount']}")
            print(f"Status: {refund['status']}")
            print(f"Reason: {refund['reason']}")
        else:
            print(f"❌ Failed to retrieve refund: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving refund: {str(e)}")

def test_create_payment_method():
    """Test creating a payment method"""
    print("\n🧪 Testing payment method creation...")
    
    method_data = {
        "customer_id": "customer_456",
        "payment_method": {
            "method_type": "credit_card",
            "provider": "stripe",
            "account_id": "acct_789012",
            "last_four": "5555",
            "expiry_month": 6,
            "expiry_year": 2026,
            "card_brand": "Mastercard"
        },
        "is_default": True,
        "metadata": {
            "card_nickname": "Personal Card",
            "billing_address": "123 Main St"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/payments/methods", json=method_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            payment_method = response.json()
            print("✅ Payment method created successfully!")
            print(f"Method ID: {payment_method['id']}")
            print(f"Customer ID: {payment_method['customer_id']}")
            print(f"Type: {payment_method['payment_method']['method_type']}")
            print(f"Default: {payment_method['is_default']}")
            return payment_method['id']
        else:
            print(f"❌ Failed to create payment method: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating payment method: {str(e)}")
        return None

def test_get_payment_methods_by_customer():
    """Test retrieving payment methods by customer ID"""
    print("\n🧪 Testing payment methods by customer retrieval...")
    
    try:
        response = requests.get(f"{BASE_URL}/payments/methods/customer/customer_456")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Payment methods by customer retrieved successfully!")
            print(f"Total Methods: {result['total']}")
            
            if result['payment_methods']:
                print("Customer Payment Methods:")
                for method in result['payment_methods']:
                    print(f"  - {method['id']}: {method['payment_method']['method_type']} (Default: {method['is_default']})")
        else:
            print(f"❌ Failed to retrieve payment methods: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving payment methods: {str(e)}")

def test_create_payment_intent():
    """Test creating a payment intent"""
    print("\n🧪 Testing payment intent creation...")
    
    intent_data = {
        "amount": 199.99,
        "currency": "USD",
        "customer_id": "customer_456",
        "description": "Payment intent for premium upgrade",
        "metadata": {
            "upgrade_type": "premium",
            "feature": "advanced_analytics"
        },
        "capture_method": "manual",
        "statement_descriptor": "PREMIUM UPGRADE",
        "receipt_email": "customer@example.com"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/payments/intents", json=intent_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            payment_intent = response.json()
            print("✅ Payment intent created successfully!")
            print(f"Intent ID: {payment_intent['id']}")
            print(f"Amount: ${payment_intent['amount']}")
            print(f"Status: {payment_intent['status']}")
            print(f"Client Secret: {payment_intent['client_secret'][:20]}...")
            return payment_intent['id']
        else:
            print(f"❌ Failed to create payment intent: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating payment intent: {str(e)}")
        return None

def test_get_payment_statistics():
    """Test getting payment statistics"""
    print("\n🧪 Testing payment statistics...")
    
    try:
        response = requests.get(f"{BASE_URL}/payments/statistics/overview")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Payment statistics retrieved successfully!")
            print(f"Total Payments: {stats['total_payments']}")
            print(f"Total Amount: ${stats['total_amount']}")
            print(f"Successful Payments: {stats['successful_payments']}")
            print(f"Failed Payments: {stats['failed_payments']}")
            print(f"Pending Payments: {stats['pending_payments']}")
            print(f"Refunded Amount: ${stats['refunded_amount']}")
            print(f"Net Revenue: ${stats['net_revenue']}")
            print(f"Average Payment Amount: ${stats['average_payment_amount']}")
            
            if stats['currency_distribution']:
                print("Currency Distribution:")
                for curr in stats['currency_distribution'][:3]:
                    print(f"  - {curr['currency']}: {curr['count']} payments, ${curr['total']}")
        else:
            print(f"❌ Failed to retrieve payment statistics: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving payment statistics: {str(e)}")

def test_get_available_options():
    """Test getting available payment options"""
    print("\n🧪 Testing available payment options...")
    
    # Test currencies
    try:
        response = requests.get(f"{BASE_URL}/payments/currencies/available")
        if response.status_code == 200:
            currencies = response.json()
            print(f"✅ Available currencies: {len(currencies)} found")
            print(f"  Sample: {currencies[:5]}")
    except Exception as e:
        print(f"❌ Error getting currencies: {str(e)}")
    
    # Test payment methods
    try:
        response = requests.get(f"{BASE_URL}/payments/methods/available")
        if response.status_code == 200:
            methods = response.json()
            print(f"✅ Available payment methods: {len(methods)} found")
            print(f"  Sample: {methods[:5]}")
    except Exception as e:
        print(f"❌ Error getting payment methods: {str(e)}")
    
    # Test payment providers
    try:
        response = requests.get(f"{BASE_URL}/payments/providers/available")
        if response.status_code == 200:
            providers = response.json()
            print(f"✅ Available payment providers: {len(providers)} found")
            print(f"  Sample: {providers[:5]}")
    except Exception as e:
        print(f"❌ Error getting payment providers: {str(e)}")
    
    # Test payment statuses
    try:
        response = requests.get(f"{BASE_URL}/payments/statuses/available")
        if response.status_code == 200:
            statuses = response.json()
            print(f"✅ Available payment statuses: {len(statuses)} found")
            print(f"  Sample: {statuses[:5]}")
    except Exception as e:
        print(f"❌ Error getting payment statuses: {str(e)}")

def test_webhook_events():
    """Test webhook event functionality"""
    print("\n🧪 Testing webhook events...")
    
    # Create webhook event
    event_data = {
        "provider": "stripe",
        "event_type": "payment_intent.succeeded",
        "payment_id": "payment_123",
        "data": {
            "id": "pi_123456",
            "object": "payment_intent",
            "status": "succeeded"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/payments/webhooks/events", json=event_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            webhook_event = response.json()
            print("✅ Webhook event created successfully!")
            print(f"Event ID: {webhook_event['id']}")
            print(f"Provider: {webhook_event['provider']}")
            print(f"Event Type: {webhook_event['event_type']}")
            
            # Get unprocessed events
            response = requests.get(f"{BASE_URL}/payments/webhooks/events/unprocessed")
            if response.status_code == 200:
                events = response.json()
                print(f"✅ Found {len(events)} unprocessed webhook events")
                
                if events:
                    # Mark first event as processed
                    event_id = events[0]['id']
                    response = requests.patch(f"{BASE_URL}/payments/webhooks/events/{event_id}/processed")
                    if response.status_code == 200:
                        print(f"✅ Webhook event {event_id} marked as processed")
        else:
            print(f"❌ Failed to create webhook event: {response.text}")
    except Exception as e:
        print(f"❌ Error testing webhook events: {str(e)}")

def main():
    """Run all tests"""
    print("🚀 Starting Payment API Tests...")
    print("=" * 60)
    
    # Test payment operations
    payment_id = test_create_payment()
    second_payment_id = test_create_second_payment()
    
    if payment_id:
        test_get_payment(payment_id)
        test_get_payments_by_order()
        test_get_payments_by_customer()
        test_search_payments()
        test_update_payment_status(payment_id)
        test_process_payment(payment_id)
        
        # Test refunds
        refund_id = test_create_refund(payment_id)
        if refund_id:
            test_get_refund(refund_id)
    
    # Test payment methods
    method_id = test_create_payment_method()
    if method_id:
        test_get_payment_methods_by_customer()
    
    # Test payment intents
    intent_id = test_create_payment_intent()
    
    # Test statistics and utilities
    test_get_payment_statistics()
    test_get_available_options()
    
    # Test webhooks
    test_webhook_events()
    
    print("\n" + "=" * 60)
    print("🏁 Payment API tests completed!")
    
    if payment_id:
        print(f"📝 Created test payment with ID: {payment_id}")
        print("💡 You can use this ID to test other operations manually")

if __name__ == "__main__":
    main()
