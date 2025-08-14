from fastapi import APIRouter
from app.api.v1.routes import user_router, file_router, order_router, product_router, payment_router, customer_router

api_router = APIRouter(prefix="/api/v1")

print("🔄 api_router initialized")
# Postgres db routes
api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(file_router, prefix="/files", tags=["Files"])
api_router.include_router(customer_router, prefix="/customers", tags=["Customers"])

# MongoDB routes
api_router.include_router(order_router, prefix="/orders", tags=["Orders"])
api_router.include_router(product_router, prefix="/products", tags=["Products"])
api_router.include_router(payment_router, prefix="/payments", tags=["Payments"])
