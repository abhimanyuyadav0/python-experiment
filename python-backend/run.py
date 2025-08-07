#!/usr/bin/env python3
"""
Startup script for the FastAPI User API
"""

import uvicorn
from app.core.config import PORT

if __name__ == "__main__":
    print("🚀 Starting FastAPI User API...")
    print(f"📡 Server will be available at: http://localhost:{PORT}")
    print(f"📚 API Documentation: http://localhost:{PORT}/docs")
    print(f"📖 ReDoc Documentation: http://localhost:{PORT}/redoc")
    print("Press Ctrl+C to stop the server\n")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True,
        log_level="info"
    ) 