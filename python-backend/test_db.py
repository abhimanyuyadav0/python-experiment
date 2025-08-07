#!/usr/bin/env python3
"""
Test database connection
"""

from app.core.database import engine
from sqlalchemy import text

def test_database():
    try:
        print("Testing database connection...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            print(f"✅ Database connection successful! Result: {result}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_database()
