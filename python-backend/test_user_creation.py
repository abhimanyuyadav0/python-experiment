#!/usr/bin/env python3
"""
Test user creation and authentication
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing user creation and authentication...")
    
    # Test database connection
    from app.core.database import engine, Base, SessionLocal
    from app.models.user import User
    from app.schemas.user import UserCreate
    from app.services.user_service import create_user, authenticate_user, hash_password
    
    # Create tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Test user creation
        print("\nTesting user creation...")
        test_user_data = UserCreate(
            name="Test User",
            email="test@example.com",
            password="test123",
            role="user",
            is_active=1
        )
        
        print(f"Creating user: {test_user_data}")
        created_user = create_user(db, test_user_data)
        print(f"✅ User created successfully: ID={created_user.id}, Email={created_user.email}")
        
        # Test authentication
        print("\nTesting authentication...")
        authenticated_user = authenticate_user(db, "test@example.com", "test123")
        if authenticated_user:
            print(f"✅ Authentication successful: {authenticated_user.email}")
        else:
            print("❌ Authentication failed")
        
        # Test with wrong password
        print("\nTesting wrong password...")
        wrong_auth = authenticate_user(db, "test@example.com", "wrongpassword")
        if wrong_auth:
            print("❌ Authentication should have failed with wrong password")
        else:
            print("✅ Correctly rejected wrong password")
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
