#!/usr/bin/env python3
"""
Test database connection and model imports
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing database connection...")
    
    # Test config
    from app.core.config import DATABASE_URL
    print(f"Database URL: {DATABASE_URL}")
    
    # Test database connection
    from app.core.database import engine
    with engine.connect() as conn:
        result = conn.execute("SELECT 1").scalar()
        print(f"Database connection test: {result}")
    
    print("✅ Database connection successful")
    
    # Test model imports
    print("\nTesting model imports...")
    
    # Import models
    from app.models.user import User
    from app.models.file import File
    
    print("✅ Models imported successfully")
    
    # Test table creation
    from app.core.database import Base
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")
    
    print("\n🎉 All tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
