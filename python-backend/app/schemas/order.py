from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderItemSchema(BaseModel):
    product_id: str = Field(..., description="Product ID")
    product_name: str = Field(..., description="Product name")
    quantity: int = Field(..., gt=0, description="Quantity of the product")
    unit_price: float = Field(..., gt=0, description="Unit price of the product")
    total_price: float = Field(..., gt=0, description="Total price for this item")

class OrderCreateSchema(BaseModel):
    customer_id: str = Field(..., description="Customer ID")
    customer_name: str = Field(..., description="Customer name")
    customer_email: str = Field(..., description="Customer email")
    customer_phone: Optional[str] = Field(None, description="Customer phone number")
    shipping_address: str = Field(..., description="Shipping address")
    items: List[OrderItemSchema] = Field(..., min_items=1, description="Order items")
    notes: Optional[str] = Field(None, description="Additional notes")
    payment_id: Optional[str] = Field(None, description="Payment ID")
class OrderUpdateSchema(BaseModel):
    status: Optional[OrderStatus] = Field(None, description="Order status")
    shipping_address: Optional[str] = Field(None, description="Shipping address")
    notes: Optional[str] = Field(None, description="Additional notes")

class OrderResponseSchema(BaseModel):
    id: str = Field(..., description="Order ID")
    customer_id: str = Field(..., description="Customer ID")
    customer_name: str = Field(..., description="Customer name")
    customer_email: str = Field(..., description="Customer email")
    customer_phone: Optional[str] = Field(None, description="Customer phone number")
    shipping_address: str = Field(..., description="Shipping address")
    items: List[OrderItemSchema] = Field(..., description="Order items")
    subtotal: float = Field(..., description="Subtotal amount")
    tax: float = Field(..., description="Tax amount")
    shipping_cost: float = Field(..., description="Shipping cost")
    total_amount: float = Field(..., description="Total order amount")
    status: OrderStatus = Field(..., description="Order status")
    notes: Optional[str] = Field(None, description="Additional notes")
    created_at: datetime = Field(..., description="Order creation timestamp")
    updated_at: datetime = Field(..., description="Order last update timestamp")
    payment_id: Optional[str] = Field(None, description="Payment ID")
class OrderListResponseSchema(BaseModel):
    orders: List[OrderResponseSchema] = Field(..., description="List of orders")
    total: int = Field(..., description="Total number of orders")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
