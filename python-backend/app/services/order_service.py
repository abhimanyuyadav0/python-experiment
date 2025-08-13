from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
from app.core.mongodb import get_mongodb
from app.schemas.order import OrderCreateSchema, OrderUpdateSchema, OrderResponseSchema, OrderStatus

class OrderService:
    def __init__(self):
        self.db = get_mongodb()
        self.collection = self.db.orders

    async def create_order(self, order_data: OrderCreateSchema) -> OrderResponseSchema:
        """Create a new order"""
        # Calculate order totals
        subtotal = sum(item.total_price for item in order_data.items)
        tax = subtotal * 0.1  # 10% tax
        shipping_cost = 10.0  # Fixed shipping cost
        total_amount = subtotal + tax + shipping_cost

        # Prepare order document
        order_doc = {
            "customer_id": order_data.customer_id,
            "customer_name": order_data.customer_name,
            "customer_email": order_data.customer_email,
            "customer_phone": order_data.customer_phone,
            "shipping_address": order_data.shipping_address,
            "items": [item.dict() for item in order_data.items],
            "subtotal": round(subtotal, 2),
            "tax": round(tax, 2),
            "shipping_cost": shipping_cost,
            "total_amount": round(total_amount, 2),
            "status": OrderStatus.PENDING,
            "notes": order_data.notes,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        # Insert order into database
        result = await self.collection.insert_one(order_doc)
        order_doc["id"] = str(result.inserted_id)

        return OrderResponseSchema(**order_doc)

    async def get_order_by_id(self, order_id: str) -> Optional[OrderResponseSchema]:
        """Get order by ID"""
        try:
            order_doc = await self.collection.find_one({"_id": ObjectId(order_id)})
            if order_doc:
                order_doc["id"] = str(order_doc["_id"])
                del order_doc["_id"]
                return OrderResponseSchema(**order_doc)
            return None
        except Exception:
            return None

    async def get_orders(
        self, 
        skip: int = 0, 
        limit: int = 10, 
        customer_id: Optional[str] = None,
        status: Optional[OrderStatus] = None
    ) -> Dict[str, Any]:
        """Get orders with pagination and filtering"""
        # Build filter
        filter_query = {}
        if customer_id:
            filter_query["customer_id"] = customer_id
        if status:
            filter_query["status"] = status

        # Get total count
        total = await self.collection.count_documents(filter_query)

        # Get orders with pagination
        cursor = self.collection.find(filter_query).skip(skip).limit(limit).sort("created_at", -1)
        orders = []
        
        async for order_doc in cursor:
            order_doc["id"] = str(order_doc["_id"])
            del order_doc["_id"]
            orders.append(OrderResponseSchema(**order_doc))

        return {
            "orders": orders,
            "total": total,
            "page": skip // limit + 1,
            "size": limit
        }

    async def update_order(self, order_id: str, update_data: OrderUpdateSchema) -> Optional[OrderResponseSchema]:
        """Update order"""
        try:
            # Prepare update document
            update_doc = {"updated_at": datetime.utcnow()}
            if update_data.status is not None:
                update_doc["status"] = update_data.status
            if update_data.shipping_address is not None:
                update_doc["shipping_address"] = update_data.shipping_address
            if update_data.notes is not None:
                update_doc["notes"] = update_data.notes

            # Update order in database
            result = await self.collection.update_one(
                {"_id": ObjectId(order_id)},
                {"$set": update_doc}
            )

            if result.modified_count > 0:
                # Return updated order
                return await self.get_order_by_id(order_id)
            return None
        except Exception:
            return None

    async def delete_order(self, order_id: str) -> bool:
        """Delete order"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(order_id)})
            return result.deleted_count > 0
        except Exception:
            return False

    async def get_orders_by_customer(self, customer_id: str, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
        """Get orders for a specific customer"""
        return await self.get_orders(skip, limit, customer_id=customer_id)

    async def update_order_status(self, order_id: str, status: OrderStatus) -> Optional[OrderResponseSchema]:
        """Update order status"""
        update_data = OrderUpdateSchema(status=status)
        return await self.update_order(order_id, update_data)
