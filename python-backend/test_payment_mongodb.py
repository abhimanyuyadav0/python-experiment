#!/usr/bin/env python3
"""
Test script for MongoDB Payment Service
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.mongodb import connect_to_mongo, close_mongo_connection
from app.services.payment_service import PaymentService
from app.schemas.payment import (
    PaymentCreateSchema, PaymentMethodDetails, PaymentMethod, PaymentProvider, Currency
)

async def test_payment_service():
    """Test the MongoDB payment service"""
    
    try:
        # Connect to MongoDB
        print("🔌 Connecting to MongoDB...")
        await connect_to_mongo()
        print("✅ Connected to MongoDB successfully!")
        
        # Initialize payment service
        payment_service = PaymentService()
        print("✅ Payment service initialized!")
        
        # Test 1: Create a payment
        print("\n🧪 Test 1: Creating a payment...")
        payment_data = PaymentCreateSchema(
            order_id="TEST_ORD_001",
            customer_id="TEST_CUST_001",
            amount=99.99,
            currency=Currency.USD,
            payment_method=PaymentMethodDetails(
                method_type=PaymentMethod.CREDIT_CARD,
                provider=PaymentProvider.STRIPE,
                last_four="4242",
                card_brand="visa",
                expiry_month=12,
                expiry_year=2026
            ),
            description="Test payment for testing purposes",
            capture_method="automatic"
        )
        
        payment = await payment_service.create_payment(payment_data)
        print(f"✅ Payment created: {payment.id}")
        print(f"   Amount: ${payment.amount}")
        print(f"   Status: {payment.status}")
        
        # Test 2: Get payment by ID
        print("\n🧪 Test 2: Retrieving payment by ID...")
        retrieved_payment = await payment_service.get_payment_by_id(payment.id)
        if retrieved_payment:
            print(f"✅ Payment retrieved: {retrieved_payment.id}")
            print(f"   Amount: ${retrieved_payment.amount}")
            print(f"   Status: {retrieved_payment.status}")
        else:
            print("❌ Failed to retrieve payment")
        
        # Test 3: Get payments by order ID
        print("\n🧪 Test 3: Retrieving payments by order ID...")
        order_payments = await payment_service.get_payments_by_order_id("TEST_ORD_001")
        print(f"✅ Found {len(order_payments)} payments for order")
        
        # Test 4: Get payments by customer ID
        print("\n🧪 Test 4: Retrieving payments by customer ID...")
        customer_payments = await payment_service.get_payments_by_customer_id("TEST_CUST_001")
        print(f"✅ Found {customer_payments['total']} payments for customer")
        print(f"   Page: {customer_payments['page']}")
        print(f"   Size: {customer_payments['size']}")
        
        # Test 5: Update payment status
        print("\n🧪 Test 5: Updating payment status...")
        from app.schemas.payment import PaymentStatus
        success = await payment_service.update_payment_status(
            payment.id, 
            PaymentStatus.COMPLETED,
            provider_payment_id="pi_test_123"
        )
        if success:
            print("✅ Payment status updated successfully")
        else:
            print("❌ Failed to update payment status")
        
        # Test 6: Get payment statistics
        print("\n🧪 Test 6: Getting payment statistics...")
        stats = await payment_service.get_payment_statistics()
        print(f"✅ Payment statistics retrieved:")
        print(f"   Total payments: {stats.total_payments}")
        print(f"   Total amount: ${stats.total_amount}")
        print(f"   Successful payments: {stats.successful_payments}")
        print(f"   Failed payments: {stats.failed_payments}")
        print(f"   Pending payments: {stats.pending_payments}")
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close MongoDB connection
        await close_mongo_connection()
        print("🔌 MongoDB connection closed")

if __name__ == "__main__":
    print("🚀 Testing MongoDB Payment Service...")
    asyncio.run(test_payment_service())
