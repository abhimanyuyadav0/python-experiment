from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import uuid
import json
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from app.core.database import get_db_session
from app.models.payment import Payment, PaymentMethod, PaymentIntent, Refund, WebhookEvent
from app.schemas.payment import (
    PaymentCreateSchema, PaymentUpdateSchema, PaymentResponseSchema,
    PaymentStatus, PaymentSearchSchema, RefundCreateSchema, RefundResponseSchema,
    PaymentMethodCreateSchema, PaymentMethodUpdateSchema, PaymentMethodResponseSchema,
    PaymentCaptureSchema, PaymentIntentSchema, PaymentIntentResponseSchema,
    PaymentStatisticsSchema, WebhookEventSchema, PaymentProvider
)

class PaymentServiceSQLite:
    """SQLite-based payment service using SQLAlchemy ORM"""
    
    def __init__(self):
        print("✅ PaymentServiceSQLite: Using SQLite with SQLAlchemy ORM")
    
    async def create_payment(self, payment_data: PaymentCreateSchema) -> PaymentResponseSchema:
        """Create a new payment using SQLite"""
        try:
            db = get_db_session()
            
            # Calculate net amount (after application fees)
            net_amount = payment_data.amount
            if payment_data.application_fee_amount:
                net_amount -= payment_data.application_fee_amount

            # Create payment record
            payment = Payment(
                order_id=payment_data.order_id,
                customer_id=payment_data.customer_id,
                amount=payment_data.amount,
                currency=payment_data.currency.value,
                payment_method_data=payment_data.payment_method.dict(),
                status=PaymentStatus.PENDING.value,
                description=payment_data.description,
                metadata=payment_data.metadata or {},
                capture_method=payment_data.capture_method,
                statement_descriptor=payment_data.statement_descriptor,
                receipt_email=payment_data.receipt_email,
                application_fee_amount=payment_data.application_fee_amount,
                net_amount=net_amount
            )
            
            db.add(payment)
            db.commit()
            db.refresh(payment)
            
            print(f"✅ Payment created successfully: {payment.payment_id}")
            
            # Convert to response schema
            return self._payment_to_response(payment)
            
        except Exception as e:
            if 'db' in locals():
                db.rollback()
            raise Exception(f"Failed to create payment: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def get_payment_by_id(self, payment_id: str) -> Optional[PaymentResponseSchema]:
        """Get payment by ID"""
        try:
            db = get_db_session()
            payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
            
            if payment:
                return self._payment_to_response(payment)
            return None
            
        except Exception as e:
            raise Exception(f"Failed to retrieve payment: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def get_payments_by_order_id(self, order_id: str) -> List[PaymentResponseSchema]:
        """Get all payments for a specific order"""
        try:
            db = get_db_session()
            payments = db.query(Payment).filter(Payment.order_id == order_id).all()
            
            return [self._payment_to_response(payment) for payment in payments]
            
        except Exception as e:
            raise Exception(f"Failed to retrieve payments by order ID: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def get_payments_by_customer_id(self, customer_id: str, skip: int = 0, limit: int = 20) -> Dict[str, Any]:
        """Get payments by customer ID with pagination"""
        try:
            db = get_db_session()
            
            # Get total count
            total = db.query(Payment).filter(Payment.customer_id == customer_id).count()
            
            # Get paginated results
            payments = db.query(Payment).filter(
                Payment.customer_id == customer_id
            ).offset(skip).limit(limit).order_by(desc(Payment.created_at)).all()
            
            return {
                "payments": [self._payment_to_response(payment) for payment in payments],
                "total": total,
                "page": skip // limit + 1,
                "size": limit
            }
            
        except Exception as e:
            raise Exception(f"Failed to retrieve payments by customer ID: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def search_payments(
        self, 
        search_params: PaymentSearchSchema,
        skip: int = 0, 
        limit: int = 20
    ) -> Dict[str, Any]:
        """Search payments with advanced filtering and sorting"""
        try:
            db = get_db_session()
            
            # Build query with filters
            query = db.query(Payment)
            
            if search_params.order_id:
                query = query.filter(Payment.order_id == search_params.order_id)
            if search_params.customer_id:
                query = query.filter(Payment.customer_id == search_params.customer_id)
            if search_params.status:
                query = query.filter(Payment.status == search_params.status.value)
            if search_params.currency:
                query = query.filter(Payment.currency == search_params.currency.value)
            if search_params.min_amount:
                query = query.filter(Payment.amount >= search_params.min_amount)
            if search_params.max_amount:
                query = query.filter(Payment.amount <= search_params.max_amount)
            if search_params.start_date:
                query = query.filter(Payment.created_at >= search_params.start_date)
            if search_params.end_date:
                query = query.filter(Payment.created_at <= search_params.end_date)
            
            # Get total count
            total = query.count()
            
            # Apply sorting
            if search_params.sort_order.lower() == "desc":
                query = query.order_by(desc(getattr(Payment, search_params.sort_by)))
            else:
                query = query.order_by(asc(getattr(Payment, search_params.sort_by)))
            
            # Apply pagination
            payments = query.offset(skip).limit(limit).all()
            
            return {
                "payments": [self._payment_to_response(payment) for payment in payments],
                "total": total,
                "page": skip // limit + 1,
                "size": limit
            }
            
        except Exception as e:
            raise Exception(f"Failed to search payments: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def update_payment(self, payment_id: str, update_data: PaymentUpdateSchema) -> Optional[PaymentResponseSchema]:
        """Update payment"""
        try:
            db = get_db_session()
            payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
            
            if not payment:
                return None
            
            # Update fields
            for field, value in update_data.dict(exclude_unset=True).items():
                setattr(payment, field, value)
            
            payment.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(payment)
            
            return self._payment_to_response(payment)
            
        except Exception as e:
            if 'db' in locals():
                db.rollback()
            raise Exception(f"Failed to update payment: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def update_payment_status(self, payment_id: str, status: PaymentStatus, 
                                  provider_payment_id: Optional[str] = None,
                                  failure_reason: Optional[str] = None,
                                  failure_code: Optional[str] = None) -> bool:
        """Update payment status"""
        try:
            db = get_db_session()
            payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
            
            if not payment:
                return False
            
            payment.status = status.value
            if provider_payment_id:
                payment.provider_payment_id = provider_payment_id
            if failure_reason:
                payment.failure_reason = failure_reason
            if failure_code:
                payment.failure_code = failure_code
            
            payment.updated_at = datetime.utcnow()
            
            if status == PaymentStatus.COMPLETED:
                payment.processed_at = datetime.utcnow()
            
            db.commit()
            return True
            
        except Exception as e:
            if 'db' in locals():
                db.rollback()
            raise Exception(f"Failed to update payment status: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def process_payment(self, payment_id: str, provider_payment_id: str, 
                            provider_fee_amount: Optional[float] = None) -> bool:
        """Process a payment"""
        try:
            db = get_db_session()
            payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
            
            if not payment:
                return False
            
            payment.provider_payment_id = provider_payment_id
            if provider_fee_amount:
                payment.provider_fee_amount = provider_fee_amount
            payment.status = PaymentStatus.COMPLETED.value
            payment.processed_at = datetime.utcnow()
            payment.updated_at = datetime.utcnow()
            
            db.commit()
            return True
            
        except Exception as e:
            if 'db' in locals():
                db.rollback()
            raise Exception(f"Failed to process payment: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def create_refund(self, refund_data: RefundCreateSchema) -> RefundResponseSchema:
        """Create a refund for a payment"""
        try:
            db = get_db_session()
            
            # Get the original payment
            payment = db.query(Payment).filter(Payment.payment_id == refund_data.payment_id).first()
            if not payment:
                raise Exception("Payment not found")
            
            # Determine refund amount (full if not specified)
            refund_amount = refund_data.amount if refund_data.amount else payment.amount
            
            # Create refund record
            refund = Refund(
                payment_id=refund_data.payment_id,
                amount=refund_amount,
                currency=payment.currency,
                reason=refund_data.reason,
                metadata=refund_data.metadata or {}
            )
            
            db.add(refund)
            db.commit()
            db.refresh(refund)
            
            # Update payment status if full refund
            if refund_amount >= payment.amount:
                await self.update_payment_status(
                    refund_data.payment_id, 
                    PaymentStatus.REFUNDED
                )
            else:
                await self.update_payment_status(
                    refund_data.payment_id, 
                    PaymentStatus.PARTIALLY_REFUNDED
                )
            
            return self._refund_to_response(refund)
            
        except Exception as e:
            if 'db' in locals():
                db.rollback()
            raise Exception(f"Failed to create refund: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def get_refund_by_id(self, refund_id: str) -> Optional[RefundResponseSchema]:
        """Get refund by ID"""
        try:
            db = get_db_session()
            refund = db.query(Refund).filter(Refund.refund_id == refund_id).first()
            
            if refund:
                return self._refund_to_response(refund)
            return None
            
        except Exception as e:
            raise Exception(f"Failed to retrieve refund: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def get_refunds_by_payment_id(self, payment_id: str) -> List[RefundResponseSchema]:
        """Get all refunds for a specific payment"""
        try:
            db = get_db_session()
            refunds = db.query(Refund).filter(Refund.payment_id == payment_id).all()
            
            return [self._refund_to_response(refund) for refund in refunds]
            
        except Exception as e:
            raise Exception(f"Failed to retrieve refunds: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def create_payment_method(self, method_data: PaymentMethodCreateSchema) -> PaymentMethodResponseSchema:
        """Create a new payment method for a customer"""
        try:
            db = get_db_session()
            
            # If this is the default method, unset other defaults for this customer
            if method_data.is_default:
                db.query(PaymentMethod).filter(
                    PaymentMethod.customer_id == method_data.customer_id,
                    PaymentMethod.is_default == True
                ).update({"is_default": False})
            
            # Create payment method record
            payment_method = PaymentMethod(
                customer_id=method_data.customer_id,
                payment_type=method_data.payment_method.method_type.value,
                payment_provider=method_data.payment_method.provider.value,
                is_default=method_data.is_default or False,
                payment_method_details=method_data.payment_method.dict(),
                metadata=method_data.metadata or {}
            )
            
            db.add(payment_method)
            db.commit()
            db.refresh(payment_method)
            
            return self._payment_method_to_response(payment_method)
            
        except Exception as e:
            if 'db' in locals():
                db.rollback()
            raise Exception(f"Failed to create payment method: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def get_payment_method_by_id(self, method_id: str) -> Optional[PaymentMethodResponseSchema]:
        """Get payment method by ID"""
        try:
            db = get_db_session()
            payment_method = db.query(PaymentMethod).filter(PaymentMethod.method_id == method_id).first()
            
            if payment_method:
                return self._payment_method_to_response(payment_method)
            return None
            
        except Exception as e:
            raise Exception(f"Failed to retrieve payment method: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def get_payment_methods_by_customer_id(self, customer_id: str) -> List[PaymentMethodResponseSchema]:
        """Get all payment methods for a customer"""
        try:
            db = get_db_session()
            payment_methods = db.query(PaymentMethod).filter(
                PaymentMethod.customer_id == customer_id,
                PaymentMethod.is_active == True
            ).all()
            
            return [self._payment_method_to_response(method) for method in payment_methods]
            
        except Exception as e:
            raise Exception(f"Failed to retrieve payment methods: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def update_payment_method(self, method_id: str, update_data: PaymentMethodUpdateSchema) -> Optional[PaymentMethodResponseSchema]:
        """Update payment method"""
        try:
            db = get_db_session()
            payment_method = db.query(PaymentMethod).filter(PaymentMethod.method_id == method_id).first()
            
            if not payment_method:
                return None
            
            # If setting as default, unset other defaults for this customer
            if update_data.is_default:
                db.query(PaymentMethod).filter(
                    PaymentMethod.customer_id == payment_method.customer_id,
                    PaymentMethod.method_id != method_id,
                    PaymentMethod.is_default == True
                ).update({"is_default": False})
            
            # Update fields
            for field, value in update_data.dict(exclude_unset=True).items():
                setattr(payment_method, field, value)
            
            payment_method.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(payment_method)
            
            return self._payment_method_to_response(payment_method)
            
        except Exception as e:
            if 'db' in locals():
                db.rollback()
            raise Exception(f"Failed to update payment method: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def delete_payment_method(self, method_id: str) -> bool:
        """Delete (deactivate) a payment method"""
        try:
            db = get_db_session()
            payment_method = db.query(PaymentMethod).filter(PaymentMethod.method_id == method_id).first()
            
            if not payment_method:
                return False
            
            payment_method.is_active = False
            payment_method.updated_at = datetime.utcnow()
            
            db.commit()
            return True
            
        except Exception as e:
            if 'db' in locals():
                db.rollback()
            raise Exception(f"Failed to delete payment method: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def create_payment_intent(self, intent_data: PaymentIntentSchema) -> PaymentIntentResponseSchema:
        """Create a payment intent for future payment processing"""
        try:
            db = get_db_session()
            
            # Create payment intent record
            payment_intent = PaymentIntent(
                amount=intent_data.amount,
                currency=intent_data.currency.value,
                customer_id=intent_data.customer_id,
                payment_method=intent_data.payment_method,
                description=intent_data.description,
                metadata=intent_data.metadata or {},
                capture_method=intent_data.capture_method,
                statement_descriptor=intent_data.statement_descriptor,
                receipt_email=intent_data.receipt_email,
                application_fee_amount=intent_data.application_fee_amount
            )
            
            db.add(payment_intent)
            db.commit()
            db.refresh(payment_intent)
            
            return self._payment_intent_to_response(payment_intent)
            
        except Exception as e:
            if 'db' in locals():
                db.rollback()
            raise Exception(f"Failed to create payment intent: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def get_payment_intent_by_id(self, intent_id: str) -> Optional[PaymentIntentResponseSchema]:
        """Get payment intent by ID"""
        try:
            db = get_db_session()
            payment_intent = db.query(PaymentIntent).filter(PaymentIntent.intent_id == intent_id).first()
            
            if payment_intent:
                return self._payment_intent_to_response(payment_intent)
            return None
            
        except Exception as e:
            raise Exception(f"Failed to retrieve payment intent: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def update_payment_intent_status(self, intent_id: str, status: PaymentStatus, 
                                        next_action: Optional[Dict[str, Any]] = None) -> bool:
        """Update payment intent status"""
        try:
            db = get_db_session()
            payment_intent = db.query(PaymentIntent).filter(PaymentIntent.intent_id == intent_id).first()
            
            if not payment_intent:
                return False
            
            payment_intent.status = status.value
            if next_action:
                payment_intent.next_action = next_action
            payment_intent.updated_at = datetime.utcnow()
            
            db.commit()
            return True
            
        except Exception as e:
            if 'db' in locals():
                db.rollback()
            raise Exception(f"Failed to update payment intent status: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def capture_payment(self, payment_id: str, capture_data: PaymentCaptureSchema) -> bool:
        """Capture a previously authorized payment"""
        try:
            db = get_db_session()
            payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
            
            if not payment:
                return False
            
            # Update payment with capture information
            if capture_data.statement_descriptor:
                payment.statement_descriptor = capture_data.statement_descriptor
            if capture_data.receipt_email:
                payment.receipt_email = capture_data.receipt_email
            if capture_data.metadata:
                payment.metadata = {**(payment.metadata or {}), **capture_data.metadata}
            
            payment.status = PaymentStatus.COMPLETED.value
            payment.processed_at = datetime.utcnow()
            payment.updated_at = datetime.utcnow()
            
            db.commit()
            return True
            
        except Exception as e:
            if 'db' in locals():
                db.rollback()
            raise Exception(f"Failed to capture payment: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def get_payment_statistics(self, start_date: Optional[datetime] = None, 
                                   end_date: Optional[datetime] = None) -> PaymentStatisticsSchema:
        """Get comprehensive payment statistics"""
        try:
            db = get_db_session()
            
            # Build base query
            query = db.query(Payment)
            
            if start_date:
                query = query.filter(Payment.created_at >= start_date)
            if end_date:
                query = query.filter(Payment.created_at <= end_date)
            
            # Get basic statistics
            total_payments = query.count()
            total_amount = query.with_entities(db.func.sum(Payment.amount)).scalar() or 0.0
            
            # Get status-based counts
            successful_payments = query.filter(Payment.status == PaymentStatus.COMPLETED.value).count()
            failed_payments = query.filter(Payment.status == PaymentStatus.FAILED.value).count()
            pending_payments = query.filter(Payment.status == PaymentStatus.PENDING.value).count()
            
            # Get refund statistics
            refund_query = db.query(Refund)
            if start_date:
                refund_query = refund_query.filter(Refund.created_at >= start_date)
            if end_date:
                refund_query = refund_query.filter(Refund.created_at <= end_date)
            
            refunded_amount = refund_query.with_entities(db.func.sum(Refund.amount)).scalar() or 0.0
            net_revenue = total_amount - refunded_amount
            
            # Calculate average
            average_payment_amount = total_amount / total_payments if total_payments > 0 else 0.0
            
            # Get currency distribution
            currency_distribution = db.query(
                Payment.currency,
                db.func.count(Payment.id).label('count'),
                db.func.sum(Payment.amount).label('total')
            ).group_by(Payment.currency).all()
            
            currency_dist = [
                {"currency": item.currency, "count": item.count, "total": float(item.total)}
                for item in currency_distribution
            ]
            
            # Get method distribution (simplified)
            method_distribution = [{"method": "credit_card", "count": total_payments, "total": total_amount}]
            
            # Get provider distribution (simplified)
            provider_distribution = [{"provider": "stripe", "count": total_payments, "total": total_amount}]
            
            return PaymentStatisticsSchema(
                total_payments=total_payments,
                total_amount=float(total_amount),
                successful_payments=successful_payments,
                failed_payments=failed_payments,
                pending_payments=pending_payments,
                refunded_amount=float(refunded_amount),
                net_revenue=float(net_revenue),
                average_payment_amount=float(average_payment_amount),
                currency_distribution=currency_dist,
                method_distribution=method_distribution,
                provider_distribution=provider_distribution
            )
            
        except Exception as e:
            raise Exception(f"Failed to get payment statistics: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def create_webhook_event(self, event_data: WebhookEventSchema) -> WebhookEventSchema:
        """Create a webhook event for processing"""
        try:
            db = get_db_session()
            
            # Create webhook event record
            webhook_event = WebhookEvent(
                provider=event_data.provider.value,
                event_type=event_data.event_type,
                payment_id=event_data.payment_id,
                data=event_data.data
            )
            
            db.add(webhook_event)
            db.commit()
            db.refresh(webhook_event)
            
            return self._webhook_event_to_response(webhook_event)
            
        except Exception as e:
            if 'db' in locals():
                db.rollback()
            raise Exception(f"Failed to create webhook event: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def mark_webhook_event_processed(self, event_id: str) -> bool:
        """Mark a webhook event as processed"""
        try:
            db = get_db_session()
            webhook_event = db.query(WebhookEvent).filter(WebhookEvent.event_id == event_id).first()
            
            if not webhook_event:
                return False
            
            webhook_event.processed = True
            webhook_event.processed_at = datetime.utcnow()
            
            db.commit()
            return True
            
        except Exception as e:
            if 'db' in locals():
                db.rollback()
            raise Exception(f"Failed to mark webhook event as processed: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    async def get_unprocessed_webhook_events(self, provider: Optional[PaymentProvider] = None) -> List[WebhookEventSchema]:
        """Get unprocessed webhook events"""
        try:
            db = get_db_session()
            
            query = db.query(WebhookEvent).filter(WebhookEvent.processed == False)
            
            if provider:
                query = query.filter(WebhookEvent.provider == provider.value)
            
            webhook_events = query.order_by(WebhookEvent.created_at).all()
            
            return [self._webhook_event_to_response(event) for event in webhook_events]
            
        except Exception as e:
            raise Exception(f"Failed to retrieve unprocessed webhook events: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    # Helper methods to convert database models to response schemas
    def _payment_to_response(self, payment: Payment) -> PaymentResponseSchema:
        """Convert Payment model to PaymentResponseSchema"""
        from app.schemas.payment import PaymentMethodDetails
        
        # Parse payment method data from JSON
        payment_method_data = payment.payment_method_data
        if isinstance(payment_method_data, str):
            payment_method_data = json.loads(payment_method_data)
        
        payment_method = PaymentMethodDetails(**payment_method_data)
        
        return PaymentResponseSchema(
            id=payment.payment_id,
            order_id=payment.order_id,
            customer_id=payment.customer_id,
            amount=payment.amount,
            currency=payment.currency,
            payment_method=payment_method,
            status=payment.status,
            description=payment.description,
            metadata=payment.metadata,
            capture_method=payment.capture_method,
            statement_descriptor=payment.statement_descriptor,
            receipt_email=payment.receipt_email,
            application_fee_amount=payment.application_fee_amount,
            provider_payment_id=payment.provider_payment_id,
            provider_fee_amount=payment.provider_fee_amount,
            net_amount=payment.net_amount,
            failure_reason=payment.failure_reason,
            failure_code=payment.failure_code,
            created_at=payment.created_at,
            updated_at=payment.updated_at,
            processed_at=payment.processed_at
        )

    def _refund_to_response(self, refund: Refund) -> RefundResponseSchema:
        """Convert Refund model to RefundResponseSchema"""
        return RefundResponseSchema(
            id=refund.refund_id,
            refund_id=refund.refund_id,
            payment_id=refund.payment_id,
            amount=refund.amount,
            currency=refund.currency,
            status=refund.status,
            reason=refund.reason,
            metadata=refund.metadata,
            provider_refund_id=refund.provider_refund_id,
            failure_reason=refund.failure_reason,
            created_at=refund.created_at,
            updated_at=refund.updated_at,
            processed_at=refund.processed_at
        )

    def _payment_method_to_response(self, payment_method: PaymentMethod) -> PaymentMethodResponseSchema:
        """Convert PaymentMethod model to PaymentMethodResponseSchema"""
        from app.schemas.payment import PaymentMethodDetails
        
        # Parse payment method details from JSON
        details_data = payment_method.payment_method_details
        if isinstance(details_data, str):
            details_data = json.loads(details_data)
        
        details = PaymentMethodDetails(**details_data)
        
        return PaymentMethodResponseSchema(
            id=payment_method.method_id,
            payment_method_id=payment_method.method_id,
            customer_id=payment_method.customer_id,
            payment_type=payment_method.payment_type,
            payment_provider=payment_method.payment_provider,
            is_default=payment_method.is_default,
            is_active=payment_method.is_active,
            payment_method_details=details,
            metadata=payment_method.metadata,
            created_at=payment_method.created_at,
            updated_at=payment_method.updated_at
        )

    def _payment_intent_to_response(self, payment_intent: PaymentIntent) -> PaymentIntentResponseSchema:
        """Convert PaymentIntent model to PaymentIntentResponseSchema"""
        return PaymentIntentResponseSchema(
            id=payment_intent.intent_id,
            payment_intent_id=payment_intent.intent_id,
            amount=payment_intent.amount,
            currency=payment_intent.currency,
            customer_id=payment_intent.customer_id,
            status=payment_intent.status,
            payment_method=payment_intent.payment_method,
            description=payment_intent.description,
            metadata=payment_intent.metadata,
            capture_method=payment_intent.capture_method,
            statement_descriptor=payment_intent.statement_descriptor,
            receipt_email=payment_intent.receipt_email,
            application_fee_amount=payment_intent.application_fee_amount,
            client_secret=payment_intent.client_secret,
            next_action=payment_intent.next_action,
            created_at=payment_intent.created_at,
            updated_at=payment_intent.updated_at
        )

    def _webhook_event_to_response(self, webhook_event: WebhookEvent) -> WebhookEventSchema:
        """Convert WebhookEvent model to WebhookEventSchema"""
        return WebhookEventSchema(
            id=webhook_event.event_id,
            provider=webhook_event.provider,
            event_type=webhook_event.event_type,
            payment_id=webhook_event.payment_id,
            data=webhook_event.data,
            processed=webhook_event.processed,
            created_at=webhook_event.created_at,
            processed_at=webhook_event.processed_at
        )
