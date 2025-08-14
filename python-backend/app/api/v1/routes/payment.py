from fastapi import APIRouter, HTTPException, Query, Depends, Body
from typing import Optional, List
from app.schemas.payment import (
    PaymentCreateSchema, PaymentUpdateSchema, PaymentResponseSchema, 
    PaymentListResponseSchema, PaymentSearchSchema, RefundCreateSchema, RefundResponseSchema,
    PaymentMethodCreateSchema, PaymentMethodUpdateSchema, PaymentMethodResponseSchema,
    PaymentMethodListResponseSchema, PaymentCaptureSchema, PaymentIntentSchema, 
    PaymentIntentResponseSchema, PaymentStatisticsSchema, WebhookEventSchema,
    PaymentStatus, PaymentMethod, PaymentProvider, Currency
)
from app.services.payment_service import PaymentService

router = APIRouter()

# Payment Management Endpoints
@router.post("/", response_model=PaymentResponseSchema, summary="Create a new payment")
async def create_payment(payment_data: PaymentCreateSchema):
    """
    Create a new payment with comprehensive details including:
    
    - **Order Information**: Order ID, customer ID, amount, currency
    - **Payment Method**: Type, provider, account details, card information
    - **Payment Settings**: Capture method, statement descriptor, receipt email
    - **Fees**: Application fee amount for platform charges
    - **Metadata**: Additional custom data for the payment
    """
    try:
        payment_service = PaymentService()
        payment = await payment_service.create_payment(payment_data)
        return payment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create payment: {str(e)}")

@router.get("/{payment_id}", response_model=PaymentResponseSchema, summary="Get payment by ID")
async def get_payment(payment_id: str):
    """
    Retrieve a payment by its unique identifier.
    
    - **payment_id**: The unique identifier of the payment
    """
    payment_service = PaymentService()
    payment = await payment_service.get_payment_by_id(payment_id)
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    return payment

@router.get("/order/{order_id}", response_model=List[PaymentResponseSchema], summary="Get payments by order ID")
async def get_payments_by_order(order_id: str):
    """
    Retrieve all payments associated with a specific order.
    
    - **order_id**: The order ID to get payments for
    """
    try:
        payment_service = PaymentService()
        payments = await payment_service.get_payments_by_order_id(order_id)
        return payments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve payments: {str(e)}")

@router.get("/customer/{customer_id}", response_model=PaymentListResponseSchema, summary="Get payments by customer ID")
async def get_payments_by_customer(
    customer_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of records to return")
):
    """
    Retrieve a paginated list of payments for a specific customer.
    
    - **customer_id**: The customer ID to get payments for
    - **skip**: Number of records to skip for pagination
    - **limit**: Maximum number of records to return (max 100)
    """
    try:
        payment_service = PaymentService()
        result = await payment_service.get_payments_by_customer_id(customer_id, skip, limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve payments: {str(e)}")

@router.get("/", response_model=PaymentListResponseSchema, summary="Get all payments")
async def get_payments(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of records to return"),
    status: Optional[PaymentStatus] = Query(None, description="Filter by payment status"),
    payment_method: Optional[PaymentMethod] = Query(None, description="Filter by payment method"),
    provider: Optional[PaymentProvider] = Query(None, description="Filter by payment provider"),
    currency: Optional[Currency] = Query(None, description="Filter by currency")
):
    """
    Retrieve a paginated list of payments with optional filtering.
    
    - **skip**: Number of records to skip for pagination
    - **limit**: Maximum number of records to return (max 100)
    - **status**: Filter payments by status
    - **payment_method**: Filter by payment method type
    - **provider**: Filter by payment provider
    - **currency**: Filter by currency
    """
    try:
        # Build search parameters
        search_params = PaymentSearchSchema(
            status=status,
            payment_method=payment_method,
            provider=provider,
            currency=currency
        )
        
        payment_service = PaymentService()
        result = await payment_service.search_payments(search_params, skip, limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve payments: {str(e)}")

@router.post("/search", response_model=PaymentListResponseSchema, summary="Search payments")
async def search_payments(
    search_params: PaymentSearchSchema,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of records to return")
):
    """
    Advanced payment search with multiple filters and sorting options.
    
    **Search Parameters:**
    - **order_id**: Filter by order ID
    - **customer_id**: Filter by customer ID
    - **status**: Filter by payment status
    - **payment_method**: Filter by payment method type
    - **provider**: Filter by payment provider
    - **min_amount/max_amount**: Amount range filtering
    - **currency**: Filter by currency
    - **start_date/end_date**: Date range filtering
    - **sort_by**: Sort field (created_at, amount, etc.)
    - **sort_order**: Sort direction (asc/desc)
    """
    try:
        payment_service = PaymentService()
        result = await payment_service.search_payments(search_params, skip, limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search payments: {str(e)}")

@router.put("/{payment_id}", response_model=PaymentResponseSchema, summary="Update payment")
async def update_payment(payment_id: str, update_data: PaymentUpdateSchema):
    """
    Update an existing payment with new information.
    
    - **payment_id**: The unique identifier of the payment to update
    - **update_data**: The new payment data to apply
    """
    try:
        payment_service = PaymentService()
        updated_payment = await payment_service.update_payment(payment_id, update_data)
        
        if not updated_payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        return updated_payment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update payment: {str(e)}")

@router.patch("/{payment_id}/status", summary="Update payment status")
async def update_payment_status(
    payment_id: str, 
    status: PaymentStatus,
    provider_payment_id: Optional[str] = Query(None, description="Provider's payment ID"),
    failure_reason: Optional[str] = Query(None, description="Reason for failure"),
    failure_code: Optional[str] = Query(None, description="Failure code")
):
    """
    Update the status of a payment.
    
    - **payment_id**: The unique identifier of the payment
    - **status**: The new status to set
    - **provider_payment_id**: Provider's payment ID (optional)
    - **failure_reason**: Reason for failure if applicable (optional)
    - **failure_code**: Failure code if applicable (optional)
    """
    try:
        payment_service = PaymentService()
        success = await payment_service.update_payment_status(
            payment_id, status, provider_payment_id, failure_reason, failure_code
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        return {"message": f"Payment status updated to {status}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update payment status: {str(e)}")

@router.post("/{payment_id}/process", summary="Process payment")
async def process_payment(
    payment_id: str,
    provider_payment_id: str = Body(..., description="Provider's payment ID"),
    provider_fee_amount: Optional[float] = Body(None, description="Provider fee amount")
):
    """
    Process a payment (mark as completed) after successful processing by payment provider.
    
    - **payment_id**: The unique identifier of the payment to process
    - **provider_payment_id**: Provider's payment ID
    - **provider_fee_amount**: Provider fee amount (optional)
    """
    try:
        payment_service = PaymentService()
        success = await payment_service.process_payment(payment_id, provider_payment_id, provider_fee_amount)
        
        if not success:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        return {"message": "Payment processed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process payment: {str(e)}")

@router.post("/{payment_id}/capture", summary="Capture payment")
async def capture_payment(payment_id: str, capture_data: PaymentCaptureSchema):
    """
    Capture a previously authorized payment.
    
    - **payment_id**: The unique identifier of the payment to capture
    - **capture_data**: Capture details including amount, statement descriptor, etc.
    """
    try:
        payment_service = PaymentService()
        success = await payment_service.capture_payment(payment_id, capture_data)
        
        if not success:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        return {"message": "Payment captured successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to capture payment: {str(e)}")

# Refund Management Endpoints
@router.post("/refunds", response_model=RefundResponseSchema, summary="Create refund")
async def create_refund(refund_data: RefundCreateSchema):
    """
    Create a refund for a completed payment.
    
    - **payment_id**: The payment ID to refund
    - **amount**: Refund amount (full if not specified)
    - **reason**: Reason for the refund
    - **metadata**: Additional metadata for the refund
    """
    try:
        payment_service = PaymentService()
        refund = await payment_service.create_refund(refund_data)
        return refund
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create refund: {str(e)}")

@router.get("/refunds/{refund_id}", response_model=RefundResponseSchema, summary="Get refund by ID")
async def get_refund(refund_id: str):
    """
    Retrieve a refund by its unique identifier.
    
    - **refund_id**: The unique identifier of the refund
    """
    payment_service = PaymentService()
    refund = await payment_service.get_refund_by_id(refund_id)
    
    if not refund:
        raise HTTPException(status_code=404, detail="Refund not found")
    
    return refund

@router.get("/{payment_id}/refunds", response_model=List[RefundResponseSchema], summary="Get refunds by payment ID")
async def get_refunds_by_payment(payment_id: str):
    """
    Retrieve all refunds for a specific payment.
    
    - **payment_id**: The payment ID to get refunds for
    """
    try:
        payment_service = PaymentService()
        refunds = await payment_service.get_refunds_by_payment_id(payment_id)
        return refunds
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve refunds: {str(e)}")

# Payment Method Management Endpoints
@router.post("/methods", response_model=PaymentMethodResponseSchema, summary="Create payment method")
async def create_payment_method(method_data: PaymentMethodCreateSchema):
    """
    Create a new payment method for a customer.
    
    - **customer_id**: The customer ID to associate the payment method with
    - **payment_method**: Payment method details (type, provider, account info)
    - **is_default**: Whether this is the default payment method
    - **metadata**: Additional metadata for the payment method
    """
    try:
        payment_service = PaymentService()
        payment_method = await payment_service.create_payment_method(method_data)
        return payment_method
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create payment method: {str(e)}")

@router.get("/methods/{method_id}", response_model=PaymentMethodResponseSchema, summary="Get payment method by ID")
async def get_payment_method(method_id: str):
    """
    Retrieve a payment method by its unique identifier.
    
    - **method_id**: The unique identifier of the payment method
    """
    payment_service = PaymentService()
    payment_method = await payment_service.get_payment_method_by_id(method_id)
    
    if not payment_method:
        raise HTTPException(status_code=404, detail="Payment method not found")
    
    return payment_method

@router.get("/methods/customer/{customer_id}", response_model=PaymentMethodListResponseSchema, summary="Get payment methods by customer ID")
async def get_payment_methods_by_customer(customer_id: str):
    """
    Retrieve all payment methods for a specific customer.
    
    - **customer_id**: The customer ID to get payment methods for
    """
    try:
        payment_service = PaymentService()
        payment_methods = await payment_service.get_payment_methods_by_customer_id(customer_id)
        return {
            "payment_methods": payment_methods,
            "total": len(payment_methods)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve payment methods: {str(e)}")

@router.put("/methods/{method_id}", response_model=PaymentMethodResponseSchema, summary="Update payment method")
async def update_payment_method(method_id: str, update_data: PaymentMethodUpdateSchema):
    """
    Update an existing payment method.
    
    - **method_id**: The unique identifier of the payment method to update
    - **update_data**: The new payment method data to apply
    """
    try:
        payment_service = PaymentService()
        updated_method = await payment_service.update_payment_method(method_id, update_data)
        
        if not updated_method:
            raise HTTPException(status_code=404, detail="Payment method not found")
        
        return updated_method
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update payment method: {str(e)}")

@router.delete("/methods/{method_id}", summary="Delete payment method")
async def delete_payment_method(method_id: str):
    """
    Delete (deactivate) a payment method.
    
    - **method_id**: The unique identifier of the payment method to delete
    """
    try:
        payment_service = PaymentService()
        success = await payment_service.delete_payment_method(method_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Payment method not found")
        
        return {"message": "Payment method deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete payment method: {str(e)}")

# Payment Intent Endpoints
@router.post("/intents", response_model=PaymentIntentResponseSchema, summary="Create payment intent")
async def create_payment_intent(intent_data: PaymentIntentSchema):
    """
    Create a payment intent for future payment processing.
    
    - **amount**: Payment amount
    - **currency**: Payment currency
    - **customer_id**: Customer ID
    - **payment_method**: Payment method ID (optional)
    - **description**: Payment description
    - **capture_method**: Capture method (automatic/manual)
    """
    try:
        payment_service = PaymentService()
        payment_intent = await payment_service.create_payment_intent(intent_data)
        return payment_intent
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create payment intent: {str(e)}")

@router.get("/intents/{intent_id}", response_model=PaymentIntentResponseSchema, summary="Get payment intent by ID")
async def get_payment_intent(intent_id: str):
    """
    Retrieve a payment intent by its unique identifier.
    
    - **intent_id**: The unique identifier of the payment intent
    """
    payment_service = PaymentService()
    payment_intent = await payment_service.get_payment_intent_by_id(intent_id)
    
    if not payment_intent:
        raise HTTPException(status_code=404, detail="Payment intent not found")
    
    return payment_intent

@router.patch("/intents/{intent_id}/status", summary="Update payment intent status")
async def update_payment_intent_status(
    intent_id: str,
    status: PaymentStatus,
    next_action: Optional[dict] = Body(None, description="Next action required")
):
    """
    Update the status of a payment intent.
    
    - **intent_id**: The unique identifier of the payment intent
    - **status**: The new status to set
    - **next_action**: Next action required (optional)
    """
    try:
        payment_service = PaymentService()
        success = await payment_service.update_payment_intent_status(intent_id, status, next_action)
        
        if not success:
            raise HTTPException(status_code=404, detail="Payment intent not found")
        
        return {"message": f"Payment intent status updated to {status}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update payment intent status: {str(e)}")

# Statistics and Analytics Endpoints
@router.get("/statistics/overview", response_model=PaymentStatisticsSchema, summary="Get payment statistics")
async def get_payment_statistics(
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)")
):
    """
    Retrieve comprehensive payment statistics including:
    
    - Total payments and amounts
    - Success/failure rates
    - Refund statistics
    - Currency and method distributions
    - Provider performance metrics
    """
    try:
        from datetime import datetime
        
        # Parse dates if provided
        parsed_start_date = None
        parsed_end_date = None
        
        if start_date:
            parsed_start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            parsed_end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        payment_service = PaymentService()
        stats = await payment_service.get_payment_statistics(parsed_start_date, parsed_end_date)
        return stats
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve payment statistics: {str(e)}")

# Webhook Management Endpoints
@router.post("/webhooks/events", response_model=WebhookEventSchema, summary="Create webhook event")
async def create_webhook_event(event_data: WebhookEventSchema):
    """
    Create a webhook event for processing payment provider notifications.
    
    - **provider**: Payment provider (Stripe, PayPal, etc.)
    - **event_type**: Type of webhook event
    - **payment_id**: Associated payment ID (optional)
    - **data**: Webhook event data
    """
    try:
        payment_service = PaymentService()
        webhook_event = await payment_service.create_webhook_event(event_data)
        return webhook_event
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create webhook event: {str(e)}")

@router.get("/webhooks/events/unprocessed", response_model=List[WebhookEventSchema], summary="Get unprocessed webhook events")
async def get_unprocessed_webhook_events(
    provider: Optional[PaymentProvider] = Query(None, description="Filter by payment provider")
):
    """
    Retrieve unprocessed webhook events for background processing.
    
    - **provider**: Filter by payment provider (optional)
    """
    try:
        payment_service = PaymentService()
        events = await payment_service.get_unprocessed_webhook_events(provider)
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve webhook events: {str(e)}")

@router.patch("/webhooks/events/{event_id}/processed", summary="Mark webhook event as processed")
async def mark_webhook_event_processed(event_id: str):
    """
    Mark a webhook event as processed.
    
    - **event_id**: The unique identifier of the webhook event
    """
    try:
        payment_service = PaymentService()
        success = await payment_service.mark_webhook_event_processed(event_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Webhook event not found")
        
        return {"message": "Webhook event marked as processed"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark webhook event as processed: {str(e)}")

# Utility Endpoints
@router.get("/currencies/available", response_model=List[str], summary="Get available currencies")
async def get_available_currencies():
    """
    Retrieve list of all available payment currencies.
    """
    try:
        return [currency.value for currency in Currency]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve currencies: {str(e)}")

@router.get("/methods/available", response_model=List[str], summary="Get available payment methods")
async def get_available_payment_methods():
    """
    Retrieve list of all available payment method types.
    """
    try:
        return [method.value for method in PaymentMethod]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve payment methods: {str(e)}")

@router.get("/providers/available", response_model=List[str], summary="Get available payment providers")
async def get_available_payment_providers():
    """
    Retrieve list of all available payment providers.
    """
    try:
        return [provider.value for provider in PaymentProvider]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve payment providers: {str(e)}")

@router.get("/statuses/available", response_model=List[str], summary="Get available payment statuses")
async def get_available_payment_statuses():
    """
    Retrieve list of all available payment statuses.
    """
    try:
        return [status.value for status in PaymentStatus]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve payment statuses: {str(e)}")
