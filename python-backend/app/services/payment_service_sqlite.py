from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import uuid
import json
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.payment import (
    PaymentCreateSchema, PaymentUpdateSchema, PaymentResponseSchema,
    PaymentStatus, PaymentSearchSchema, RefundCreateSchema, RefundResponseSchema,
    PaymentMethodCreateSchema, PaymentMethodUpdateSchema, PaymentMethodResponseSchema,
    PaymentCaptureSchema, PaymentIntentSchema, PaymentIntentResponseSchema,
    PaymentStatisticsSchema, WebhookEventSchema, PaymentProvider
)

class PaymentServiceSQLite:
    """Temporary SQLite-based payment service for development when MongoDB is not available"""
    
    def __init__(self):
        print("✅ PaymentServiceSQLite: Using SQLite for development")
    
    async def create_payment(self, payment_data: PaymentCreateSchema) -> PaymentResponseSchema:
        """Create a new payment using SQLite"""
        try:
            # Generate unique payment ID
            payment_id = str(uuid.uuid4())
            
            # Calculate net amount (after application fees)
            net_amount = payment_data.amount
            if payment_data.application_fee_amount:
                net_amount -= payment_data.application_fee_amount

            # Prepare payment document (simulating MongoDB document structure)
            payment_doc = {
                "id": payment_id,
                "order_id": payment_data.order_id,
                "customer_id": payment_data.customer_id,
                "amount": payment_data.amount,
                "currency": payment_data.currency.value,
                "payment_method": payment_data.payment_method.dict(),
                "status": PaymentStatus.PENDING.value,
                "description": payment_data.description,
                "metadata": payment_data.metadata or {},
                "capture_method": payment_data.capture_method,
                "statement_descriptor": payment_data.statement_descriptor,
                "receipt_email": payment_data.receipt_email,
                "application_fee_amount": payment_data.application_fee_amount,
                "provider_payment_id": None,
                "provider_fee_amount": None,
                "net_amount": net_amount,
                "failure_reason": None,
                "failure_code": None,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "processed_at": None
            }

            # For now, just return the payment document
            # In a real implementation, you would save this to SQLite
            print(f"✅ Payment created successfully: {payment_id}")
            return PaymentResponseSchema(**payment_doc)

        except Exception as e:
            raise Exception(f"Failed to create payment: {str(e)}")

    async def get_payment_by_id(self, payment_id: str) -> Optional[PaymentResponseSchema]:
        """Get payment by ID"""
        try:
            # For development, return a mock payment
            mock_payment = {
                "id": payment_id,
                "order_id": "ORD_MOCK_001",
                "customer_id": "CUST_MOCK_001",
                "amount": 100.0,
                "currency": "USD",
                "payment_method": {
                    "method_type": "credit_card",
                    "provider": "stripe",
                    "last_four": "4242",
                    "card_brand": "visa",
                    "expiry_month": 12,
                    "expiry_year": 2026
                },
                "status": "completed",
                "description": "Mock payment for development",
                "metadata": {},
                "capture_method": "automatic",
                "statement_descriptor": None,
                "receipt_email": None,
                "application_fee_amount": None,
                "provider_payment_id": "pi_mock_123",
                "provider_fee_amount": 2.9,
                "net_amount": 97.1,
                "failure_reason": None,
                "failure_code": None,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "processed_at": datetime.utcnow().isoformat()
            }
            return PaymentResponseSchema(**mock_payment)
        except Exception:
            return None

    async def get_payments_by_order_id(self, order_id: str) -> List[PaymentResponseSchema]:
        """Get all payments for a specific order"""
        try:
            # Return mock payments for development
            mock_payments = [
                {
                    "id": str(uuid.uuid4()),
                    "order_id": order_id,
                    "customer_id": "CUST_MOCK_001",
                    "amount": 100.0,
                    "currency": "USD",
                    "payment_method": {
                        "method_type": "credit_card",
                        "provider": "stripe",
                        "last_four": "4242",
                        "card_brand": "visa",
                        "expiry_month": 12,
                        "expiry_year": 2026
                    },
                    "status": "completed",
                    "description": "Mock payment for development",
                    "metadata": {},
                    "capture_method": "automatic",
                    "statement_descriptor": None,
                    "receipt_email": None,
                    "application_fee_amount": None,
                    "provider_payment_id": "pi_mock_123",
                    "provider_fee_amount": 2.9,
                    "net_amount": 97.1,
                    "failure_reason": None,
                    "failure_code": None,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                    "processed_at": datetime.utcnow().isoformat()
                }
            ]
            
            return [PaymentResponseSchema(**payment) for payment in mock_payments]
        except Exception as e:
            raise Exception(f"Failed to retrieve payments by order ID: {str(e)}")

    async def get_payments_by_customer_id(self, customer_id: str, skip: int = 0, limit: int = 20) -> Dict[str, Any]:
        """Get payments by customer ID with pagination"""
        try:
            # Return mock payments for development
            mock_payments = [
                {
                    "id": str(uuid.uuid4()),
                    "order_id": "ORD_MOCK_001",
                    "customer_id": customer_id,
                    "amount": 100.0,
                    "currency": "USD",
                    "payment_method": {
                        "method_type": "credit_card",
                        "provider": "stripe",
                        "last_four": "4242",
                        "card_brand": "visa",
                        "expiry_month": 12,
                        "expiry_year": 2026
                    },
                    "status": "completed",
                    "description": "Mock payment for development",
                    "metadata": {},
                    "capture_method": "automatic",
                    "statement_descriptor": None,
                    "receipt_email": None,
                    "application_fee_amount": None,
                    "provider_payment_id": "pi_mock_123",
                    "provider_fee_amount": 2.9,
                    "net_amount": 97.1,
                    "failure_reason": None,
                    "failure_code": None,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                    "processed_at": datetime.utcnow().isoformat()
                }
            ]
            
            return {
                "payments": [PaymentResponseSchema(**payment) for payment in mock_payments],
                "total": len(mock_payments),
                "page": skip // limit + 1,
                "size": limit
            }
        except Exception as e:
            raise Exception(f"Failed to retrieve payments by customer ID: {str(e)}")

    async def search_payments(
        self, 
        search_params: PaymentSearchSchema,
        skip: int = 0, 
        limit: int = 20
    ) -> Dict[str, Any]:
        """Search payments with advanced filtering and sorting"""
        try:
            # Return mock payments for development
            mock_payments = [
                {
                    "id": str(uuid.uuid4()),
                    "order_id": "ORD_MOCK_001",
                    "customer_id": "CUST_MOCK_001",
                    "amount": 100.0,
                    "currency": "USD",
                    "payment_method": {
                        "method_type": "credit_card",
                        "provider": "stripe",
                        "last_four": "4242",
                        "card_brand": "visa",
                        "expiry_month": 12,
                        "expiry_year": 2026
                    },
                    "status": "completed",
                    "description": "Mock payment for development",
                    "metadata": {},
                    "capture_method": "automatic",
                    "statement_descriptor": None,
                    "receipt_email": None,
                    "application_fee_amount": None,
                    "provider_payment_id": "pi_mock_123",
                    "provider_fee_amount": 2.9,
                    "net_amount": 97.1,
                    "failure_reason": None,
                    "failure_code": None,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                    "processed_at": datetime.utcnow().isoformat()
                }
            ]
            
            return {
                "payments": [PaymentResponseSchema(**payment) for payment in mock_payments],
                "total": len(mock_payments),
                "page": skip // limit + 1,
                "size": limit
            }
        except Exception as e:
            raise Exception(f"Failed to search payments: {str(e)}")

    # Add other required methods with mock implementations
    async def update_payment(self, payment_id: str, update_data: PaymentUpdateSchema) -> Optional[PaymentResponseSchema]:
        """Update payment"""
        return await self.get_payment_by_id(payment_id)

    async def update_payment_status(self, payment_id: str, status: PaymentStatus, 
                                  provider_payment_id: Optional[str] = None,
                                  failure_reason: Optional[str] = None,
                                  failure_code: Optional[str] = None) -> bool:
        """Update payment status"""
        return True

    async def process_payment(self, payment_id: str, provider_payment_id: str, 
                            provider_fee_amount: Optional[float] = None) -> bool:
        """Process a payment"""
        return True

    async def create_refund(self, refund_data: RefundCreateSchema) -> RefundResponseSchema:
        """Create a refund for a payment"""
        # Mock implementation
        return RefundResponseSchema(
            id=str(uuid.uuid4()),
            refund_id=str(uuid.uuid4()),
            payment_id=refund_data.payment_id,
            amount=refund_data.amount,
            reason=refund_data.reason,
            status="completed",
            metadata=refund_data.metadata or {},
            provider_refund_id="ref_mock_123",
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )

    async def get_refund_by_id(self, refund_id: str) -> Optional[RefundResponseSchema]:
        """Get refund by ID"""
        return None

    async def get_refunds_by_payment_id(self, payment_id: str) -> List[RefundResponseSchema]:
        """Get all refunds for a specific payment"""
        return []

    async def create_payment_method(self, method_data: PaymentMethodCreateSchema) -> PaymentMethodResponseSchema:
        """Create a new payment method for a customer"""
        # Mock implementation
        return PaymentMethodResponseSchema(
            id=str(uuid.uuid4()),
            payment_method_id=str(uuid.uuid4()),
            customer_id=method_data.customer_id,
            payment_type="card",
            payment_provider="stripe",
            is_default=method_data.is_default or False,
            is_active=True,
            payment_method_details=method_data.payment_method_details,
            metadata=method_data.metadata or {},
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )

    async def get_payment_method_by_id(self, method_id: str) -> Optional[PaymentMethodResponseSchema]:
        """Get payment method by ID"""
        return None

    async def get_payment_methods_by_customer_id(self, customer_id: str) -> List[PaymentMethodResponseSchema]:
        """Get all payment methods for a customer"""
        return []

    async def update_payment_method(self, method_id: str, update_data: PaymentMethodUpdateSchema) -> Optional[PaymentMethodResponseSchema]:
        """Update payment method"""
        return None

    async def delete_payment_method(self, method_id: str) -> bool:
        """Delete (deactivate) a payment method"""
        return True

    async def create_payment_intent(self, intent_data: PaymentIntentSchema) -> PaymentIntentResponseSchema:
        """Create a payment intent for future payment processing"""
        # Mock implementation
        return PaymentIntentResponseSchema(
            id=str(uuid.uuid4()),
            payment_intent_id=str(uuid.uuid4()),
            amount=intent_data.amount,
            currency=intent_data.currency,
            customer_id=intent_data.customer_id,
            payment_method_types=intent_data.payment_method_types,
            status="requires_payment_method",
            description=intent_data.description,
            metadata=intent_data.metadata or {},
            capture_method=intent_data.capture_method,
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )

    async def get_payment_intent_by_id(self, intent_id: str) -> Optional[PaymentIntentResponseSchema]:
        """Get payment intent by ID"""
        return None

    async def update_payment_intent_status(self, intent_id: str, status: PaymentStatus, 
                                        next_action: Optional[Dict[str, Any]] = None) -> bool:
        """Update payment intent status"""
        return True

    async def capture_payment(self, payment_id: str, capture_data: PaymentCaptureSchema) -> bool:
        """Capture a previously authorized payment"""
        return True

    async def get_payment_statistics(self, start_date: Optional[datetime] = None, 
                                   end_date: Optional[datetime] = None) -> PaymentStatisticsSchema:
        """Get comprehensive payment statistics"""
        # Mock implementation
        return PaymentStatisticsSchema(
            total_payments=10,
            total_amount=1000.0,
            successful_payments=8,
            failed_payments=1,
            pending_payments=1,
            refunded_amount=50.0,
            net_revenue=950.0,
            average_payment_amount=100.0,
            currency_distribution=[{"currency": "USD", "count": 10, "total": 1000.0}],
            method_distribution=[{"method": "credit_card", "count": 10, "total": 1000.0}],
            provider_distribution=[{"provider": "stripe", "count": 10, "total": 1000.0}]
        )

    async def create_webhook_event(self, event_data: WebhookEventSchema) -> WebhookEventSchema:
        """Create a webhook event for processing"""
        # Mock implementation
        return WebhookEventSchema(
            id=str(uuid.uuid4()),
            provider=event_data.provider,
            event_type=event_data.event_type,
            payment_id=event_data.payment_id,
            data=event_data.data,
            processed=False,
            created_at=datetime.utcnow().isoformat(),
            processed_at=None
        )

    async def mark_webhook_event_processed(self, event_id: str) -> bool:
        """Mark a webhook event as processed"""
        return True

    async def get_unprocessed_webhook_events(self, provider: Optional[PaymentProvider] = None) -> List[WebhookEventSchema]:
        """Get unprocessed webhook events"""
        return []
