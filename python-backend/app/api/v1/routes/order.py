from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from app.schemas.order import (
    OrderCreateSchema, 
    OrderUpdateSchema, 
    OrderResponseSchema, 
    OrderListResponseSchema,
    OrderStatus
)
from app.services.order_service import OrderService

router = APIRouter()
print("🔄 Order router initialized")

@router.post("/", response_model=OrderResponseSchema, summary="Create a new order")
def create_order(order_data: OrderCreateSchema):
    """
    Create a new order with the following information:
    
    - **customer_id**: Unique identifier for the customer
    - **customer_name**: Full name of the customer
    - **customer_email**: Email address of the customer
    - **customer_phone**: Phone number (optional)
    - **shipping_address**: Delivery address
    - **items**: List of order items with product details
    - **notes**: Additional notes (optional)
    """
    print("🔄 create_order function called")
    print(f"🔄 Order data received: {order_data}")
    
    try:
        order_service = OrderService()
        order = order_service.create_order(order_data)
        print(f"✅ Order created successfully: {order.id}")
        return order
    except ValueError as e:
        print(f"❌ Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        print(f"❌ OrderService initialization failed: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
    except Exception as e:
        print(f"❌ Order creation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create order: {str(e)}")

@router.get("/", response_model=OrderListResponseSchema, summary="Get all orders")
def get_orders(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    customer_id: Optional[str] = Query(None, description="Filter by customer ID"),
    status: Optional[OrderStatus] = Query(None, description="Filter by order status")
):
    """
    Retrieve a paginated list of orders with optional filtering.
    
    - **skip**: Number of records to skip for pagination
    - **limit**: Maximum number of records to return
    - **customer_id**: Filter orders by customer ID
    - **status**: Filter orders by status
    """
    print("🔄 get_orders function called")
    try:
        order_service = OrderService()
        result = order_service.get_orders(skip, limit, customer_id, status)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve orders: {str(e)}")

@router.get("/{order_id}", response_model=OrderResponseSchema, summary="Get order by ID")
def get_order(order_id: str):
    """
    Retrieve an order by its unique identifier.
    
    - **order_id**: The unique identifier of the order
    """
    order_service = OrderService()
    order = order_service.get_order_by_id(order_id)
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order

@router.put("/{order_id}", response_model=OrderResponseSchema, summary="Update order")
def update_order(order_id: str, update_data: OrderUpdateSchema):
    """
    Update an existing order with new information.
    
    - **order_id**: The unique identifier of the order to update
    - **update_data**: The new order data to apply
    """
    try:
        order_service = OrderService()
        updated_order = order_service.update_order(order_id, update_data)
        
        if not updated_order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return updated_order
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update order: {str(e)}")

@router.delete("/{order_id}", summary="Delete order")
def delete_order(order_id: str):
    """
    Delete an order by its unique identifier.
    
    - **order_id**: The unique identifier of the order to delete
    """
    try:
        order_service = OrderService()
        success = order_service.delete_order(order_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return {"message": "Order deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete order: {str(e)}")

@router.get("/customer/{customer_id}", response_model=OrderListResponseSchema, summary="Get orders by customer")
def get_customer_orders(
    customer_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return")
):
    """
    Retrieve all orders for a specific customer.
    
    - **customer_id**: The unique identifier of the customer
    - **skip**: Number of records to skip for pagination
    - **limit**: Maximum number of records to return
    """
    try:
        order_service = OrderService()
        result = order_service.get_orders_by_customer(customer_id, skip, limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve customer orders: {str(e)}")

@router.patch("/{order_id}/status", response_model=OrderResponseSchema, summary="Update order status")
def update_order_status(order_id: str, status: OrderStatus):
    """
    Update the status of an order.
    
    - **order_id**: The unique identifier of the order
    - **status**: The new status to set
    """
    try:
        order_service = OrderService()
        updated_order = order_service.update_order_status(order_id, status)
        
        if not updated_order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return updated_order
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update order status: {str(e)}")