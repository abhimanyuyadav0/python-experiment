from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base, SessionLocal
from app.core.mongodb import connect_to_mongo, close_mongo_connection
from app.core.config import APP_NAME, APP_VERSION, PORT
from sqlalchemy import text
from app.api.v1 import api_router

# Import models to ensure they are registered with SQLAlchemy
from app.models.user import User
from app.models.file import File

# Create database tables
print("🔧 Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Database connected: multitenant_app")
print(f"PORT: {PORT}")

# Verify tables exist
with engine.connect() as conn:
    result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
    tables = [row[0] for row in result]
    print(f"📋 Available tables: {tables}")

app = FastAPI(
    title=APP_NAME or "Multi-Tenant API",
    version=APP_VERSION or "1.0.0",
    description="A modern multi-tenant application with role-based access control",
    port=PORT
)

@app.on_event("startup")
async def startup_event():
    # Connect to MongoDB (optional - app can run without it)
    try:
        await connect_to_mongo()
        print("✅ MongoDB connected successfully")
    except Exception as e:
        print(f"⚠️  MongoDB connection failed: {str(e)}")
        print("⚠️  Order API endpoints will not be available")
        print("⚠️  Other API endpoints will continue to work")
    
    print(f"🚀 Server running on port {PORT}")
    print(f"📚 API Documentation: http://localhost:{PORT}/docs")
    print(f"🔍 Health Check: http://localhost:{PORT}/health")

@app.on_event("shutdown")
async def shutdown_event():
    # Close MongoDB connection
    await close_mongo_connection()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(api_router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Multi-Tenant API",
        "version": APP_VERSION or "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/health/mongodb")
async def mongodb_health_check():
    """Test MongoDB connection"""
    try:
        from app.core.mongodb import get_mongodb, mongodb
        
        # Check if MongoDB is connected - compare with None instead of boolean evaluation
        if mongodb.client is None or mongodb.db is None:
            return {
                "status": "MongoDB not connected", 
                "error": "MongoDB connection was not established during startup"
            }
        
        db = get_mongodb()
        # Test connection by running a simple command
        await db.command("ping")
        return {"status": "MongoDB connection successful"}
    except Exception as e:
        return {"status": "MongoDB connection failed", "error": str(e)}

@app.get("/test-db")
def test_database():
    """Test database connection"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
        return {"status": "Database connection successful", "result": result}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}

@app.get("/test-token")
def test_token():
    """Test token creation and expiration"""
    from app.services.user_service import create_access_token, verify_token
    from datetime import datetime
    
    # Create a test token
    token, expires_at = create_access_token(data={"test": "data"})
    
    # Verify the token
    payload = verify_token(token)
    
    # Calculate time until expiration
    now = datetime.utcnow()
    # expires_at is in milliseconds, convert to seconds for fromtimestamp
    expire_time = datetime.fromtimestamp(expires_at / 1000)
    time_until_expiry = expire_time - now
    
    return {
        "token": token,
        "expires_at": expires_at,
        "expire_time": expire_time.isoformat(),
        "time_until_expiry_seconds": time_until_expiry.total_seconds(),
        "is_valid": payload is not None,
        "payload": payload,
        "current_time": now.isoformat(),
        "expire_time_utc": expire_time.isoformat()
    }

@app.get("/test-users")
def test_users():
    """Test user database access"""
    from app.services.user_service import get_user_by_email
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    try:
        # Test getting a user
        user = get_user_by_email(db, "user@example.com")
        if user:
            return {
                "status": "success",
                "user_found": True,
                "user_email": user.email,
                "user_id": user.id,
                "user_role": user.role,
                "is_active": user.is_active,
                "password_hash": user.password[:20] + "..." if user.password else None
            }
        else:
            return {
                "status": "success",
                "user_found": False,
                "message": "User user@example.com not found"
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
    finally:
        db.close()

@app.get("/test-auth-flow")
def test_auth_flow():
    """Test complete authentication flow"""
    from app.services.user_service import get_user_by_email, create_access_token, verify_token, verify_password, hash_password
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    try:
        # Test getting a user
        user = get_user_by_email(db, "user@example.com")
        if not user:
            return {
                "status": "error",
                "message": "Test user not found"
            }
        
        # Test password verification
        password_test = verify_password("user123", user.password)
        
        # Create a token
        token, expires_at = create_access_token(data={"sub": user.id})
        
        # Verify the token
        payload = verify_token(token)
        
        return {
            "status": "success",
            "user_email": user.email,
            "user_id": user.id,
            "is_active": user.is_active,
            "password_verified": password_test,
            "token_created": bool(token),
            "token_length": len(token) if token else 0,
            "expires_at": expires_at,
            "token_verified": payload is not None,
            "payload": payload
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Server running on port {PORT}")
    print("📚 Database connected: multitenant_app")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
