from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import user
from app.core.database import engine, Base, SessionLocal
from app.core.config import APP_NAME, APP_VERSION, PORT
from sqlalchemy import text
from app.api.v1 import api_router

# Create database tables
print("🔧 Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Database connected: multitenant_app")
print(f"PORT: {PORT}")

app = FastAPI(
    title=APP_NAME or "Multi-Tenant API",
    version=APP_VERSION or "1.0.0",
    description="A modern multi-tenant application with role-based access control",
    port=PORT
)

@app.on_event("startup")
async def startup_event():
    print(f"🚀 Server running on port {PORT}")
    print(f"📚 API Documentation: http://localhost:{PORT}/docs")
    print(f"🔍 Health Check: http://localhost:{PORT}/health")

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
        "payload": payload
    }

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Server running on port {PORT}")
    print("📚 Database connected: multitenant_app")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
