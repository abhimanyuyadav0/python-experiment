#!/usr/bin/env python3
"""
MongoDB initialization script for Multi-Tenant Application
Creates necessary collections and sample data for payments, products, and orders
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta
from bson import ObjectId
import uuid

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.mongodb import connect_to_mongo, close_mongo_connection, get_mongodb

async def init_mongodb():
    """Initialize MongoDB with collections and sample data"""
    
    try:
        # Connect to MongoDB
        print("🔌 Connecting to MongoDB...")
        await connect_to_mongo()
        db = get_mongodb()
        print("✅ Connected to MongoDB successfully!")
        
        # Create collections if they don't exist
        collections = ['payments', 'products', 'orders', 'customers']
        
        for collection_name in collections:
            if collection_name not in await db.list_collection_names():
                await db.create_collection(collection_name)
                print(f"✅ Created collection: {collection_name}")
            else:
                print(f"✅ Collection already exists: {collection_name}")
        
        # Check if collections have data
        payments_count = await db.payments.count_documents({})
        products_count = await db.products.count_documents({})
        orders_count = await db.orders.count_documents({})
        
        print(f"\n📊 Current data counts:")
        print(f"  Payments: {payments_count}")
        print(f"  Products: {products_count}")
        print(f"  Orders: {orders_count}")
        
        # Create sample data if collections are empty
        if payments_count == 0:
            print("\n📝 Creating sample payments...")
            sample_payments = [
                {
                    "_id": ObjectId(),
                    "payment_id": f"PAY_{uuid.uuid4().hex[:8].upper()}",
                    "order_id": "ORD_001",
                    "customer_id": "CUST_001",
                    "amount": 299.99,
                    "currency": "USD",
                    "payment_method": {
                        "method_type": "credit_card",
                        "provider": "stripe",
                        "card_last4": "4242",
                        "card_brand": "visa"
                    },
                    "status": "completed",
                    "description": "Payment for electronics order",
                    "created_at": datetime.utcnow() - timedelta(days=5),
                    "updated_at": datetime.utcnow() - timedelta(days=5),
                    "processed_at": datetime.utcnow() - timedelta(days=5)
                },
                {
                    "_id": ObjectId(),
                    "payment_id": f"PAY_{uuid.uuid4().hex[:8].upper()}",
                    "order_id": "ORD_002",
                    "customer_id": "CUST_002",
                    "amount": 149.99,
                    "currency": "USD",
                    "payment_method": {
                        "method_type": "debit_card",
                        "provider": "stripe",
                        "card_last4": "1234",
                        "card_brand": "mastercard"
                    },
                    "status": "completed",
                    "description": "Payment for clothing order",
                    "created_at": datetime.utcnow() - timedelta(days=3),
                    "updated_at": datetime.utcnow() - timedelta(days=3),
                    "processed_at": datetime.utcnow() - timedelta(days=3)
                }
            ]
            await db.payments.insert_many(sample_payments)
            print(f"✅ Created {len(sample_payments)} sample payments")
        
        if products_count == 0:
            print("\n📝 Creating sample products...")
            sample_products = [
                {
                    "_id": ObjectId(),
                    "product_id": f"PROD_{uuid.uuid4().hex[:8].upper()}",
                    "name": "Laptop Computer",
                    "description": "High-performance laptop with latest specifications",
                    "sku": "LAPTOP-001",
                    "category": "Electronics",
                    "brand": "TechCorp",
                    "price": 1299.99,
                    "stock_quantity": 25,
                    "is_active": True,
                    "created_at": datetime.utcnow() - timedelta(days=10),
                    "updated_at": datetime.utcnow() - timedelta(days=10)
                },
                {
                    "_id": ObjectId(),
                    "product_id": f"PROD_{uuid.uuid4().hex[:8].upper()}",
                    "name": "Wireless Mouse",
                    "description": "Ergonomic wireless mouse with precision tracking",
                    "sku": "MOUSE-001",
                    "category": "Electronics",
                    "brand": "TechCorp",
                    "price": 29.99,
                    "stock_quantity": 100,
                    "is_active": True,
                    "created_at": datetime.utcnow() - timedelta(days=8),
                    "updated_at": datetime.utcnow() - timedelta(days=8)
                }
            ]
            await db.products.insert_many(sample_products)
            print(f"✅ Created {len(sample_products)} sample products")
        
        if orders_count == 0:
            print("\n📝 Creating sample orders...")
            sample_orders = [
                {
                    "_id": ObjectId(),
                    "order_id": f"ORD_{uuid.uuid4().hex[:8].upper()}",
                    "customer_id": "CUST_001",
                    "customer_name": "John Doe",
                    "customer_email": "john.doe@example.com",
                    "customer_phone": "+1-555-0123",
                    "total_amount": 299.99,
                    "status": "delivered",
                    "items": [
                        {
                            "product_id": "PROD_001",
                            "product_name": "Laptop Computer",
                            "quantity": 1,
                            "unit_price": 299.99,
                            "subtotal": 299.99
                        }
                    ],
                    "shipping_address": {
                        "street": "123 Main Street",
                        "city": "New York",
                        "state": "NY",
                        "zip_code": "10001",
                        "country": "USA"
                    },
                    "payment_method": "credit_card",
                    "created_at": datetime.utcnow() - timedelta(days=5),
                    "updated_at": datetime.utcnow() - timedelta(days=5)
                },
                {
                    "_id": ObjectId(),
                    "order_id": f"ORD_{uuid.uuid4().hex[:8].upper()}",
                    "customer_id": "CUST_002",
                    "customer_name": "Jane Smith",
                    "customer_email": "jane.smith@example.com",
                    "customer_phone": "+1-555-0456",
                    "total_amount": 149.99,
                    "status": "shipped",
                    "items": [
                        {
                            "product_id": "PROD_002",
                            "product_name": "Wireless Mouse",
                            "quantity": 5,
                            "unit_price": 29.99,
                            "subtotal": 149.95
                        }
                    ],
                    "shipping_address": {
                        "street": "456 Oak Avenue",
                        "city": "Los Angeles",
                        "state": "CA",
                        "zip_code": "90210",
                        "country": "USA"
                    },
                    "payment_method": "debit_card",
                    "created_at": datetime.utcnow() - timedelta(days=3),
                    "updated_at": datetime.utcnow() - timedelta(days=3)
                }
            ]
            await db.orders.insert_many(sample_orders)
            print(f"✅ Created {len(sample_orders)} sample orders")
        
        # Final data counts
        final_payments_count = await db.payments.count_documents({})
        final_products_count = await db.products.count_documents({})
        final_orders_count = await db.orders.count_documents({})
        
        print(f"\n🎉 MongoDB initialization completed successfully!")
        print(f"📊 Final data counts:")
        print(f"  Payments: {final_payments_count}")
        print(f"  Products: {final_products_count}")
        print(f"  Orders: {final_orders_count}")
        
    except Exception as e:
        print(f"❌ Error during MongoDB initialization: {e}")
        sys.exit(1)
    finally:
        # Close MongoDB connection
        await close_mongo_connection()
        print("🔌 MongoDB connection closed")

if __name__ == "__main__":
    print("🚀 Initializing MongoDB for Multi-Tenant Application...")
    asyncio.run(init_mongodb())
