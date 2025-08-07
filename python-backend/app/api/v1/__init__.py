from fastapi import APIRouter
from app.api.v1.routes import user

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(user.router, prefix="/users", tags=["Users"])
