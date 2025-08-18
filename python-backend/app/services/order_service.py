from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, desc
from app.core.database import get_db_session
from app.models.order import Order, OrderItem, OrderStatus
from app.models.customer import Customer
from app.schemas.order import OrderCreateSchema, OrderUpdateSchema, OrderResponseSchema

class OrderService:
    def __init__(self):
        try:
            print("✅ OrderService: PostgreSQL connection successful")
        except Exception as e:
            print(f"❌ OrderService: PostgreSQL connection failed: {str(e)}")
            raise RuntimeError(f"PostgreSQL connection failed: {str(e)}")

    def _get_db_session(self) -> Session:
        """Get a new database session"""
        return get_db_session()

    def create_order(self, order_data: OrderCreateSchema) -> OrderResponseSchema:
        """Create a new order"""
        db = self._get_db_session()
        try:
            # First, find the customer by customer_id (string)
            customer = db.query(Customer).filter(Customer.customer_id == order_data.customer_id).first()
            if not customer:
                raise ValueError(f"Customer with ID {order_data.customer_id} not found")

            # Calculate order totals
            subtotal = sum(item.total_price for item in order_data.items)
            tax = subtotal * 0.1  # 10% tax
            shipping_cost = 10.0  # Fixed shipping cost
            total_amount = subtotal + tax + shipping_cost

            # Create the order
            order = Order(
                customer_id=customer.id,  # Use the internal customer ID
                shipping_address=order_data.shipping_address,
                subtotal=round(subtotal, 2),
                tax=round(tax, 2),
                shipping_cost=shipping_cost,
                total_amount=round(total_amount, 2),
                status=OrderStatus.PENDING,
                notes=order_data.notes,
                payment_id=order_data.payment_id
            )

            db.add(order)
            db.flush()  # Get the order ID

            # Create order items
            for item_data in order_data.items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item_data.product_id,
                    product_name=item_data.product_name,
                    quantity=item_data.quantity,
                    unit_price=item_data.unit_price,
                    total_price=item_data.total_price
                )
                db.add(order_item)

            db.commit()

            # Return the created order with customer info
            return self._order_to_response_schema(order, customer)

        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def get_order_by_id(self, order_id: str) -> Optional[OrderResponseSchema]:
        """Get order by order_id (string)"""
        db = self._get_db_session()
        try:
            order = db.query(Order).options(
                joinedload(Order.customer),
                joinedload(Order.items)
            ).filter(Order.order_id == order_id).first()
            
            if order:
                return self._order_to_response_schema(order, order.customer)
            return None
        finally:
            db.close()

    def get_orders(
        self, 
        skip: int = 0, 
        limit: int = 10, 
        customer_id: Optional[str] = None,
        status: Optional[OrderStatus] = None
    ) -> Dict[str, Any]:
        """Get orders with pagination and filtering"""
        db = self._get_db_session()
        try:
            # Build query
            query = db.query(Order).options(
                joinedload(Order.customer),
                joinedload(Order.items)
            )

            # Apply filters
            if customer_id:
                customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
                if customer:
                    query = query.filter(Order.customer_id == customer.id)
                else:
                    # If customer not found, return empty result
                    return {"orders": [], "total": 0, "page": skip // limit + 1, "size": limit}
            
            if status:
                query = query.filter(Order.status == status)

            # Get total count
            total = query.count()

            # Apply pagination and ordering
            orders = query.order_by(desc(Order.created_at)).offset(skip).limit(limit).all()

            # Convert to response schemas
            order_responses = [self._order_to_response_schema(order, order.customer) for order in orders]

            return {
                "orders": order_responses,
                "total": total,
                "page": skip // limit + 1,
                "size": limit
            }
        finally:
            db.close()

    def update_order(self, order_id: str, update_data: OrderUpdateSchema) -> Optional[OrderResponseSchema]:
        """Update order"""
        db = self._get_db_session()
        try:
            order = db.query(Order).options(
                joinedload(Order.customer),
                joinedload(Order.items)
            ).filter(Order.order_id == order_id).first()
            
            if not order:
                return None

            # Update fields
            if update_data.status is not None:
                order.status = update_data.status
            if update_data.shipping_address is not None:
                order.shipping_address = update_data.shipping_address
            if update_data.notes is not None:
                order.notes = update_data.notes

            order.updated_at = datetime.utcnow()
            db.commit()

            return self._order_to_response_schema(order, order.customer)
        
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def delete_order(self, order_id: str) -> bool:
        """Delete order"""
        db = self._get_db_session()
        try:
            order = db.query(Order).filter(Order.order_id == order_id).first()
            if order:
                db.delete(order)  # Cascade will delete order items
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def get_orders_by_customer(self, customer_id: str, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
        """Get orders for a specific customer"""
        return self.get_orders(skip, limit, customer_id=customer_id)

    def update_order_status(self, order_id: str, status: OrderStatus) -> Optional[OrderResponseSchema]:
        """Update order status"""
        update_data = OrderUpdateSchema(status=status)
        return self.update_order(order_id, update_data)

    def _order_to_response_schema(self, order: Order, customer: Customer) -> OrderResponseSchema:
        """Convert Order model to OrderResponseSchema"""
        from app.schemas.order import OrderItemSchema
        
        # Convert order items
        items = [
            OrderItemSchema(
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price
            )
            for item in order.items
        ]

        return OrderResponseSchema(
            id=order.order_id,
            customer_id=customer.customer_id,
            customer_name=customer.full_name,
            customer_email=customer.email,
            customer_phone=customer.phone,
            shipping_address=order.shipping_address,
            items=items,
            subtotal=order.subtotal,
            tax=order.tax,
            shipping_cost=order.shipping_cost,
            total_amount=order.total_amount,
            status=order.status,
            notes=order.notes,
            created_at=order.created_at,
            updated_at=order.updated_at,
            payment_id=order.payment_id
        )