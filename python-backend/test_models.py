#!/usr/bin/env python3
"""
Test script to check model imports
"""

try:
    print("Testing model imports...")
    
    # Test importing User model
    print("1. Importing User model...")
    from app.models.user import User, UserRole
    print("✅ User model imported successfully")
    
    # Test importing File model
    print("2. Importing File model...")
    from app.models.file import File, FileType
    print("✅ File model imported successfully")
    
    # Test importing both together
    print("3. Testing both models together...")
    from app.models.user import User
    from app.models.file import File
    print("✅ Both models imported together successfully")
    
    # Test database connection
    print("4. Testing database connection...")
    from app.core.database import engine, Base
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
    
    print("\n🎉 All tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
