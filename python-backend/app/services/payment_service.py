from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import uuid
import json
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.mongodb import get_mongodb
from app.schemas.payment import (
    PaymentCreateSchema, PaymentUpdateSchema, PaymentResponseSchema,
    PaymentStatus, PaymentSearchSchema, RefundCreateSchema, RefundResponseSchema,
    PaymentMethodCreateSchema, PaymentMethodUpdateSchema, PaymentMethodResponseSchema,
    PaymentCaptureSchema, PaymentIntentSchema, PaymentIntentResponseSchema,
    PaymentStatisticsSchema, WebhookEventSchema, PaymentProvider
)

class PaymentService:
    """MongoDB-based payment service using Motor async driver"""
    
    def __init__(self):
        print("✅ PaymentService: Using MongoDB with Motor async driver")
        self.db: AsyncIOMotorDatabase = get_mongodb()
        self.payments_collection = self.db.payments
        self.payment_methods_collection = self.db.payment_methods
        self.payment_intents_collection = self.db.payment_intents
        self.refunds_collection = self.db.refunds
        self.webhook_events_collection = self.db.webhook_events
    
    async def create_payment(self, payment_data: PaymentCreateSchema) -> PaymentResponseSchema:
        """Create a new payment using MongoDB"""
        try:
            # Generate unique payment ID
            payment_id = f"PAY_{uuid.uuid4().hex[:8].upper()}"
            
            # Calculate net amount (after application fees)
            net_amount = payment_data.amount
            if payment_data.application_fee_amount:
                net_amount -= payment_data.application_fee_amount

            # Prepare payment document
            payment_doc = {
                "id": payment_id,  # Use 'id' to match PaymentResponseSchema
                "payment_id": payment_id,
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
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "processed_at": None
            }

            # Insert into MongoDB
            result = await self.payments_collection.insert_one(payment_doc)
            
            print(f"✅ Payment created successfully: {payment_id}")
            return PaymentResponseSchema(**payment_doc)

        except Exception as e:
            raise Exception(f"Failed to create payment: {str(e)}")

    async def get_payment_by_id(self, payment_id: str) -> Optional[PaymentResponseSchema]:
        """Get payment by ID"""
        try:
            payment_doc = await self.payments_collection.find_one({"payment_id": payment_id})
            
            if payment_doc:
                # Convert ObjectId to string for JSON serialization
                payment_doc["_id"] = str(payment_doc["_id"])
                # Ensure id field exists
                if "id" not in payment_doc and "payment_id" in payment_doc:
                    payment_doc["id"] = payment_doc["payment_id"]
                return PaymentResponseSchema(**payment_doc)
            return None
            
        except Exception as e:
            raise Exception(f"Failed to retrieve payment: {str(e)}")

    async def get_payments_by_order_id(self, order_id: str) -> List[PaymentResponseSchema]:
        """Get all payments for a specific order"""
        try:
            cursor = self.payments_collection.find({"order_id": order_id})
            payments = await cursor.to_list(length=None)
            
            # Convert ObjectIds to strings and ensure id field is set
            for payment in payments:
                payment["_id"] = str(payment["_id"])
                # Ensure id field exists (use payment_id if id is missing)
                if "id" not in payment and "payment_id" in payment:
                    payment["id"] = payment["payment_id"]
            
            return [PaymentResponseSchema(**payment) for payment in payments]
            
        except Exception as e:
            raise Exception(f"Failed to retrieve payments by order ID: {str(e)}")

    async def get_payments_by_customer_id(self, customer_id: str, skip: int = 0, limit: int = 20) -> Dict[str, Any]:
        """Get payments by customer ID with pagination"""
        try:
            # Get total count
            total = await self.payments_collection.count_documents({"customer_id": customer_id})
            
            # Get paginated results
            cursor = self.payments_collection.find({"customer_id": customer_id})
            cursor = cursor.sort("created_at", -1).skip(skip).limit(limit)
            payments = await cursor.to_list(length=None)
            
            # Convert ObjectIds to strings and ensure id field is set
            for payment in payments:
                payment["_id"] = str(payment["_id"])
                # Ensure id field exists (use payment_id if id is missing)
                if "id" not in payment and "payment_id" in payment:
                    payment["id"] = payment["payment_id"]
            
            return {
                "payments": [PaymentResponseSchema(**payment) for payment in payments],
                "total": total,
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
            # Build filter query
            filter_query = {}
            
            if search_params.order_id:
                filter_query["order_id"] = search_params.order_id
            if search_params.customer_id:
                filter_query["customer_id"] = search_params.customer_id
            if search_params.status:
                filter_query["status"] = search_params.status.value
            if search_params.currency:
                filter_query["currency"] = search_params.currency.value
            if search_params.min_amount or search_params.max_amount:
                amount_filter = {}
                if search_params.min_amount:
                    amount_filter["$gte"] = search_params.min_amount
                if search_params.max_amount:
                    amount_filter["$lte"] = search_params.max_amount
                filter_query["amount"] = amount_filter
            if search_params.start_date or search_params.end_date:
                date_filter = {}
                if search_params.start_date:
                    date_filter["$gte"] = search_params.start_date
                if search_params.end_date:
                    date_filter["$lte"] = search_params.end_date
                filter_query["created_at"] = date_filter
            
            # Get total count
            total = await self.payments_collection.count_documents(filter_query)
            
            # Build sort query
            sort_direction = -1 if search_params.sort_order.lower() == "desc" else 1
            sort_field = search_params.sort_by if hasattr(search_params, search_params.sort_by) else "created_at"
            
            # Get paginated results
            cursor = self.payments_collection.find(filter_query)
            cursor = cursor.sort(sort_field, sort_direction).skip(skip).limit(limit)
            payments = await cursor.to_list(length=None)
            
            # Convert ObjectIds to strings and ensure id field is set
            for payment in payments:
                payment["_id"] = str(payment["_id"])
                # Ensure id field exists (use payment_id if id is missing)
                if "id" not in payment and "payment_id" in payment:
                    payment["id"] = payment["payment_id"]
            
            return {
                "payments": [PaymentResponseSchema(**payment) for payment in payments],
                "total": total,
                "page": skip // limit + 1,
                "size": limit
            }
            
        except Exception as e:
            raise Exception(f"Failed to search payments: {str(e)}")

    async def update_payment(self, payment_id: str, update_data: PaymentUpdateSchema) -> Optional[PaymentResponseSchema]:
        """Update payment"""
        try:
            # Prepare update data
            update_fields = update_data.dict(exclude_unset=True)
            update_fields["updated_at"] = datetime.utcnow()
            
            # Update in MongoDB
            result = await self.payments_collection.update_one(
                {"payment_id": payment_id},
                {"$set": update_fields}
            )
            
            if result.modified_count > 0:
                # Get updated payment
                return await self.get_payment_by_id(payment_id)
            return None
            
        except Exception as e:
            raise Exception(f"Failed to update payment: {str(e)}")

    async def update_payment_status(self, payment_id: str, status: PaymentStatus, 
                                  provider_payment_id: Optional[str] = None,
                                  failure_reason: Optional[str] = None,
                                  failure_code: Optional[str] = None) -> bool:
        """Update payment status"""
        try:
            update_fields = {
                "status": status.value,
                "updated_at": datetime.utcnow()
            }
            
            if provider_payment_id:
                update_fields["provider_payment_id"] = provider_payment_id
            if failure_reason:
                update_fields["failure_reason"] = failure_reason
            if failure_code:
                update_fields["failure_code"] = failure_code
            
            if status == PaymentStatus.COMPLETED:
                update_fields["processed_at"] = datetime.utcnow()
            
            result = await self.payments_collection.update_one(
                {"payment_id": payment_id},
                {"$set": update_fields}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            raise Exception(f"Failed to update payment status: {str(e)}")

    async def process_payment(self, payment_id: str, provider_payment_id: str, 
                            provider_fee_amount: Optional[float] = None) -> bool:
        """Process a payment"""
        try:
            update_fields = {
                "provider_payment_id": provider_payment_id,
                "status": PaymentStatus.COMPLETED.value,
                "processed_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            if provider_fee_amount:
                update_fields["provider_fee_amount"] = provider_fee_amount
            
            result = await self.payments_collection.update_one(
                {"payment_id": payment_id},
                {"$set": update_fields}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            raise Exception(f"Failed to process payment: {str(e)}")

    async def create_refund(self, refund_data: RefundCreateSchema) -> RefundResponseSchema:
        """Create a refund for a payment"""
        try:
            # Get the original payment
            payment = await self.get_payment_by_id(refund_data.payment_id)
            if not payment:
                raise Exception("Payment not found")
            
            # Determine refund amount (full if not specified)
            refund_amount = refund_data.amount if refund_data.amount else payment.amount
            
            # Generate refund ID
            refund_id = f"REF_{uuid.uuid4().hex[:8].upper()}"
            
            # Create refund document
            refund_doc = {
                "refund_id": refund_id,
                "payment_id": refund_data.payment_id,
                "amount": refund_amount,
                "currency": payment.currency,
                "status": "completed",
                "reason": refund_data.reason,
                "metadata": refund_data.metadata or {},
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "processed_at": datetime.utcnow()
            }
            
            # Insert refund
            await self.refunds_collection.insert_one(refund_doc)
            
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
            
            return RefundResponseSchema(**refund_doc)
            
        except Exception as e:
            raise Exception(f"Failed to create refund: {str(e)}")

    async def get_refund_by_id(self, refund_id: str) -> Optional[RefundResponseSchema]:
        """Get refund by ID"""
        try:
            refund_doc = await self.refunds_collection.find_one({"refund_id": refund_id})
            
            if refund_doc:
                refund_doc["_id"] = str(refund_doc["_id"])
                return RefundResponseSchema(**refund_doc)
            return None
            
        except Exception as e:
            raise Exception(f"Failed to retrieve refund: {str(e)}")

    async def get_refunds_by_payment_id(self, payment_id: str) -> List[RefundResponseSchema]:
        """Get all refunds for a specific payment"""
        try:
            cursor = self.refunds_collection.find({"payment_id": payment_id})
            refunds = await cursor.to_list(length=None)
            
            # Convert ObjectIds to strings
            for refund in refunds:
                refund["_id"] = str(refund["_id"])
            
            return [RefundResponseSchema(**refund) for refund in refunds]
            
        except Exception as e:
            raise Exception(f"Failed to retrieve refunds: {str(e)}")

    async def create_payment_method(self, method_data: PaymentMethodCreateSchema) -> PaymentMethodResponseSchema:
        """Create a new payment method for a customer"""
        try:
            # If this is the default method, unset other defaults for this customer
            if method_data.is_default:
                await self.payment_methods_collection.update_many(
                    {"customer_id": method_data.customer_id, "is_default": True},
                    {"$set": {"is_default": False}}
                )
            
            # Generate method ID
            method_id = f"PM_{uuid.uuid4().hex[:8].upper()}"
            
            # Create payment method document
            payment_method_doc = {
                "method_id": method_id,
                "customer_id": method_data.customer_id,
                "payment_type": method_data.payment_method.method_type.value,
                "payment_provider": method_data.payment_method.provider.value,
                "is_default": method_data.is_default or False,
                "is_active": True,
                "payment_method_details": method_data.payment_method.dict(),
                "metadata": method_data.metadata or {},
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Insert payment method
            await self.payment_methods_collection.insert_one(payment_method_doc)
            
            return PaymentMethodResponseSchema(**payment_method_doc)
            
        except Exception as e:
            raise Exception(f"Failed to create payment method: {str(e)}")

    async def get_payment_method_by_id(self, method_id: str) -> Optional[PaymentMethodResponseSchema]:
        """Get payment method by ID"""
        try:
            method_doc = await self.payment_methods_collection.find_one({"method_id": method_id})
            
            if method_doc:
                method_doc["_id"] = str(method_doc["_id"])
                return PaymentMethodResponseSchema(**method_doc)
            return None
            
        except Exception as e:
            raise Exception(f"Failed to retrieve payment method: {str(e)}")

    async def get_payment_methods_by_customer_id(self, customer_id: str) -> List[PaymentMethodResponseSchema]:
        """Get all payment methods for a customer"""
        try:
            cursor = self.payment_methods_collection.find({
                "customer_id": customer_id,
                "is_active": True
            })
            payment_methods = await cursor.to_list(length=None)
            
            # Convert ObjectIds to strings
            for method in payment_methods:
                method["_id"] = str(method["_id"])
            
            return [PaymentMethodResponseSchema(**method) for method in payment_methods]
            
        except Exception as e:
            raise Exception(f"Failed to retrieve payment methods: {str(e)}")

    async def update_payment_method(self, method_id: str, update_data: PaymentMethodUpdateSchema) -> Optional[PaymentMethodResponseSchema]:
        """Update payment method"""
        try:
            # If setting as default, unset other defaults for this customer
            if update_data.is_default:
                method = await self.payment_methods_collection.find_one({"method_id": method_id})
                if method:
                    await self.payment_methods_collection.update_many(
                        {
                            "customer_id": method["customer_id"],
                            "method_id": {"$ne": method_id},
                            "is_default": True
                        },
                        {"$set": {"is_default": False}}
                    )
            
            # Prepare update data
            update_fields = update_data.dict(exclude_unset=True)
            update_fields["updated_at"] = datetime.utcnow()
            
            # Update payment method
            result = await self.payment_methods_collection.update_one(
                {"method_id": method_id},
                {"$set": update_fields}
            )
            
            if result.modified_count > 0:
                return await self.get_payment_method_by_id(method_id)
            return None
            
        except Exception as e:
            raise Exception(f"Failed to update payment method: {str(e)}")

    async def delete_payment_method(self, method_id: str) -> bool:
        """Delete (deactivate) a payment method"""
        try:
            result = await self.payment_methods_collection.update_one(
                {"method_id": method_id},
                {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            raise Exception(f"Failed to delete payment method: {str(e)}")

    async def create_payment_intent(self, intent_data: PaymentIntentSchema) -> PaymentIntentResponseSchema:
        """Create a payment intent for future payment processing"""
        try:
            # Generate intent ID
            intent_id = f"PI_{uuid.uuid4().hex[:8].upper()}"
            
            # Create payment intent document
            payment_intent_doc = {
                "intent_id": intent_id,
                "amount": intent_data.amount,
                "currency": intent_data.currency.value,
                "customer_id": intent_data.customer_id,
                "status": "requires_payment_method",
                "payment_method": intent_data.payment_method,
                "description": intent_data.description,
                "metadata": intent_data.metadata or {},
                "capture_method": intent_data.capture_method,
                "statement_descriptor": intent_data.statement_descriptor,
                "receipt_email": intent_data.receipt_email,
                "application_fee_amount": intent_data.application_fee_amount,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Insert payment intent
            await self.payment_intents_collection.insert_one(payment_intent_doc)
            
            return PaymentIntentResponseSchema(**payment_intent_doc)
            
        except Exception as e:
            raise Exception(f"Failed to create payment intent: {str(e)}")

    async def get_payment_intent_by_id(self, intent_id: str) -> Optional[PaymentIntentResponseSchema]:
        """Get payment intent by ID"""
        try:
            intent_doc = await self.payment_intents_collection.find_one({"intent_id": intent_id})
            
            if intent_doc:
                intent_doc["_id"] = str(intent_doc["_id"])
                return PaymentIntentResponseSchema(**intent_doc)
            return None
            
        except Exception as e:
            raise Exception(f"Failed to retrieve payment intent: {str(e)}")

    async def update_payment_intent_status(self, intent_id: str, status: PaymentStatus, 
                                        next_action: Optional[Dict[str, Any]] = None) -> bool:
        """Update payment intent status"""
        try:
            update_fields = {
                "status": status.value,
                "updated_at": datetime.utcnow()
            }
            
            if next_action:
                update_fields["next_action"] = next_action
            
            result = await self.payment_intents_collection.update_one(
                {"intent_id": intent_id},
                {"$set": update_fields}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            raise Exception(f"Failed to update payment intent status: {str(e)}")

    async def capture_payment(self, payment_id: str, capture_data: PaymentCaptureSchema) -> bool:
        """Capture a previously authorized payment"""
        try:
            # Get the payment
            payment = await self.get_payment_by_id(payment_id)
            if not payment:
                return False
            
            # Prepare update fields
            update_fields = {
                "status": PaymentStatus.COMPLETED.value,
                "processed_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            if capture_data.statement_descriptor:
                update_fields["statement_descriptor"] = capture_data.statement_descriptor
            if capture_data.receipt_email:
                update_fields["receipt_email"] = capture_data.receipt_email
            if capture_data.metadata:
                # Merge with existing metadata
                existing_metadata = payment.metadata or {}
                existing_metadata.update(capture_data.metadata)
                update_fields["metadata"] = existing_metadata
            
            # Update payment
            result = await self.payments_collection.update_one(
                {"payment_id": payment_id},
                {"$set": update_fields}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            raise Exception(f"Failed to capture payment: {str(e)}")

    async def get_payment_statistics(self, start_date: Optional[datetime] = None, 
                                   end_date: Optional[datetime] = None) -> PaymentStatisticsSchema:
        """Get comprehensive payment statistics"""
        try:
            # Build date filter
            date_filter = {}
            if start_date or end_date:
                if start_date:
                    date_filter["$gte"] = start_date
                if end_date:
                    date_filter["$lte"] = end_date
            
            # Get basic statistics
            match_stage = {"$match": date_filter} if date_filter else {}
            
            pipeline = [
                match_stage,
                {
                    "$group": {
                        "_id": None,
                        "total_payments": {"$sum": 1},
                        "total_amount": {"$sum": "$amount"},
                        "successful_payments": {
                            "$sum": {"$cond": [{"$eq": ["$status", "completed"]}, 1, 0]}
                        },
                        "failed_payments": {
                            "$sum": {"$cond": [{"$eq": ["$status", "failed"]}, 1, 0]}
                        },
                        "pending_payments": {
                            "$sum": {"$cond": [{"$eq": ["$status", "pending"]}, 1, 0]}
                        }
                    }
                }
            ]
            
            # Remove empty match stage if no date filter
            if not date_filter:
                pipeline.pop(0)
            
            stats_result = await self.payments_collection.aggregate(pipeline).to_list(length=1)
            stats = stats_result[0] if stats_result else {
                "total_payments": 0,
                "total_amount": 0,
                "successful_payments": 0,
                "failed_payments": 0,
                "pending_payments": 0
            }
            
            # Get refund statistics
            refund_filter = date_filter.copy() if date_filter else {}
            refund_pipeline = [
                {"$match": refund_filter},
                {
                    "$group": {
                        "_id": None,
                        "refunded_amount": {"$sum": "$amount"}
                    }
                }
            ]
            
            if not refund_filter:
                refund_pipeline.pop(0)
            
            refund_result = await self.refunds_collection.aggregate(refund_pipeline).to_list(length=1)
            refunded_amount = refund_result[0]["refunded_amount"] if refund_result else 0.0
            
            # Calculate derived statistics
            total_amount = stats["total_amount"]
            net_revenue = total_amount - refunded_amount
            average_payment_amount = total_amount / stats["total_payments"] if stats["total_payments"] > 0 else 0.0
            
            # Get currency distribution
            currency_pipeline = [
                match_stage,
                {
                    "$group": {
                        "_id": "$currency",
                        "count": {"$sum": 1},
                        "total": {"$sum": "$amount"}
                    }
                }
            ]
            
            if not date_filter:
                currency_pipeline.pop(0)
            
            currency_distribution = await self.payments_collection.aggregate(currency_pipeline).to_list(length=None)
            currency_dist = [
                {"currency": item["_id"], "count": item["count"], "total": float(item["total"])}
                for item in currency_distribution
            ]
            
            # Simplified distributions for now
            method_distribution = [{"method": "credit_card", "count": stats["total_payments"], "total": total_amount}]
            provider_distribution = [{"provider": "stripe", "count": stats["total_payments"], "total": total_amount}]
            
            return PaymentStatisticsSchema(
                total_payments=stats["total_payments"],
                total_amount=float(total_amount),
                successful_payments=stats["successful_payments"],
                failed_payments=stats["failed_payments"],
                pending_payments=stats["pending_payments"],
                refunded_amount=float(refunded_amount),
                net_revenue=float(net_revenue),
                average_payment_amount=float(average_payment_amount),
                currency_distribution=currency_dist,
                method_distribution=method_distribution,
                provider_distribution=provider_distribution
            )
            
        except Exception as e:
            raise Exception(f"Failed to get payment statistics: {str(e)}")

    async def create_webhook_event(self, event_data: WebhookEventSchema) -> WebhookEventSchema:
        """Create a webhook event for processing"""
        try:
            # Generate event ID
            event_id = f"WEB_{uuid.uuid4().hex[:8].upper()}"
            
            # Create webhook event document
            webhook_event_doc = {
                "event_id": event_id,
                "provider": event_data.provider.value,
                "event_type": event_data.event_type,
                "payment_id": event_data.payment_id,
                "data": event_data.data,
                "processed": False,
                "created_at": datetime.utcnow(),
                "processed_at": None
            }
            
            # Insert webhook event
            await self.webhook_events_collection.insert_one(webhook_event_doc)
            
            return WebhookEventSchema(**webhook_event_doc)
            
        except Exception as e:
            raise Exception(f"Failed to create webhook event: {str(e)}")

    async def mark_webhook_event_processed(self, event_id: str) -> bool:
        """Mark a webhook event as processed"""
        try:
            result = await self.webhook_events_collection.update_one(
                {"event_id": event_id},
                {
                    "$set": {
                        "processed": True,
                        "processed_at": datetime.utcnow()
                    }
                }
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            raise Exception(f"Failed to mark webhook event as processed: {str(e)}")

    async def get_unprocessed_webhook_events(self, provider: Optional[PaymentProvider] = None) -> List[WebhookEventSchema]:
        """Get unprocessed webhook events"""
        try:
            filter_query = {"processed": False}
            if provider:
                filter_query["provider"] = provider.value
            
            cursor = self.webhook_events_collection.find(filter_query).sort("created_at", 1)
            webhook_events = await cursor.to_list(length=None)
            
            # Convert ObjectIds to strings
            for event in webhook_events:
                event["_id"] = str(event["_id"])
            
            return [WebhookEventSchema(**event) for event in webhook_events]
            
        except Exception as e:
            raise Exception(f"Failed to retrieve unprocessed webhook events: {str(e)}")
