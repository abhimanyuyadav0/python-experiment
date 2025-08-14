#!/usr/bin/env python3
"""
Database recreation script for Multi-Tenant Application
This script drops all tables and recreates them with the new schema
"""

import os
import sys
from sqlalchemy import create_engine, text
from app.core.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.models.customer import Customer
from app.models.file import File
from app.models.payment import Payment, PaymentMethod, PaymentIntent, Refund, WebhookEvent
from app.services.user_service import hash_password

def recreate_database():
    """Drop all tables and recreate them with the new schema"""
    
    # Drop all tables
    print("Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ All tables dropped successfully!")
    
    # Create all tables with new schema
    print("Creating database tables with new schema...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin_user:
            print("Creating admin user...")
            admin_user = User(
                name="Admin User",
                email="admin@example.com",
                password=hash_password("admin123"),
                role=UserRole.admin,
                is_active=1
            )
            db.add(admin_user)
            print("✅ Admin user created!")
        else:
            print("✅ Admin user already exists!")
        
        # Check if tenant user already exists
        tenant_user = db.query(User).filter(User.email == "tenant@example.com").first()
        if not tenant_user:
            print("Creating tenant user...")
            tenant_user = User(
                name="Tenant User",
                email="tenant@example.com",
                password=hash_password("tenant123"),
                role=UserRole.tenant,
                is_active=1
            )
            db.add(tenant_user)
            print("✅ Tenant user created!")
        else:
            print("✅ Tenant user already exists!")
        
        # Check if regular user already exists
        regular_user = db.query(User).filter(User.email == "user@example.com").first()
        if not regular_user:
            print("Creating regular user...")
            regular_user = User(
                name="Regular User",
                email="user@example.com",
                password=hash_password("user123"),
                role=UserRole.user,
                is_active=1
            )
            db.add(regular_user)
            print("✅ Regular user created!")
        else:
            print("✅ Regular user already exists!")
        
        # Commit all changes
        db.commit()
        print("\n🎉 Database recreation completed successfully!")
        print("\nDefault users created:")
        print("  Admin:    admin@example.com / admin123")
        print("  Tenant:   tenant@example.com / tenant123")
        print("  User:     user@example.com / user123")
        print("\nPayment tables created:")
        print("  - payments")
        print("  - payment_methods")
        print("  - payment_intents")
        print("  - refunds")
        print("  - webhook_events")
        print("\n⚠️  Note: All existing data has been lost!")
        
    except Exception as e:
        print(f"❌ Error during database recreation: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Recreating Multi-Tenant Application Database...")
    print("⚠️  WARNING: This will delete all existing data!")
    
    # Ask for confirmation
    response = input("Are you sure you want to continue? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Database recreation cancelled.")
        sys.exit(0)
    
    recreate_database()
