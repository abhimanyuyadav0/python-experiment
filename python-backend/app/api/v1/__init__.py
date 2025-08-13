from fastapi import APIRouter
from app.api.v1.routes import user_router, file_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(file_router, prefix="/files", tags=["Files"])
