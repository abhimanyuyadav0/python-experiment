# Routes package
from .user import router as user_router
from .file import router as file_router
from .order import router as order_router
from .product import router as product_router
from .payment import router as payment_router
from .customer import router as customer_router

__all__ = ["user_router", "file_router", "order_router", "product_router", "payment_router", "customer_router"]