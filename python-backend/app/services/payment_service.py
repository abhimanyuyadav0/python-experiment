from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from bson import ObjectId
from app.core.mongodb import get_mongodb
from app.schemas.payment import (
    PaymentCreateSchema, PaymentUpdateSchema, PaymentResponseSchema,
    PaymentStatus, PaymentSearchSchema, RefundCreateSchema, RefundResponseSchema,
    PaymentMethodCreateSchema, PaymentMethodUpdateSchema, PaymentMethodResponseSchema,
    PaymentCaptureSchema, PaymentIntentSchema, PaymentIntentResponseSchema,
    PaymentStatisticsSchema, WebhookEventSchema, PaymentProvider
)
import uuid
import re

class PaymentService:
    def __init__(self):
        try:
            self.db = get_mongodb()
            self.payments_collection = self.db.payments
            self.refunds_collection = self.db.refunds
            self.payment_methods_collection = self.db.payment_methods
            self.payment_intents_collection = self.db.payment_intents
            self.webhook_events_collection = self.db.webhook_events
            print("✅ PaymentService: MongoDB connection successful")
        except Exception as e:
            print(f"❌ PaymentService: MongoDB connection failed: {str(e)}")
            raise RuntimeError(f"MongoDB connection failed: {str(e)}")

    async def create_payment(self, payment_data: PaymentCreateSchema) -> PaymentResponseSchema:
        """Create a new payment"""
        try:
            # Generate unique payment ID
            payment_id = str(uuid.uuid4())
            
            # Calculate net amount (after application fees)
            net_amount = payment_data.amount
            if payment_data.application_fee_amount:
                net_amount -= payment_data.application_fee_amount

            # Prepare payment document
            payment_doc = {
                "_id": ObjectId(payment_id),
                "order_id": payment_data.order_id,
                "customer_id": payment_data.customer_id,
                "amount": payment_data.amount,
                "currency": payment_data.currency,
                "payment_method": payment_data.payment_method.dict(),
                "status": PaymentStatus.PENDING,
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

            # Insert payment into database
            await self.payments_collection.insert_one(payment_doc)
            payment_doc["id"] = str(payment_doc["_id"])
            del payment_doc["_id"]

            return PaymentResponseSchema(**payment_doc)

        except Exception as e:
            raise Exception(f"Failed to create payment: {str(e)}")

    async def get_payment_by_id(self, payment_id: str) -> Optional[PaymentResponseSchema]:
        """Get payment by ID"""
        try:
            payment_doc = await self.payments_collection.find_one({"_id": ObjectId(payment_id)})
            if payment_doc:
                payment_doc["id"] = str(payment_doc["_id"])
                del payment_doc["_id"]
                return PaymentResponseSchema(**payment_doc)
            return None
        except Exception:
            return None

    async def get_payments_by_order_id(self, order_id: str) -> List[PaymentResponseSchema]:
        """Get all payments for a specific order"""
        try:
            cursor = self.payments_collection.find({"order_id": order_id}).sort("created_at", -1)
            payments = []
            
            async for payment_doc in cursor:
                payment_doc["id"] = str(payment_doc["_id"])
                del payment_doc["_id"]
                payments.append(PaymentResponseSchema(**payment_doc))
            
            return payments
        except Exception as e:
            raise Exception(f"Failed to retrieve payments by order ID: {str(e)}")

    async def get_payments_by_customer_id(self, customer_id: str, skip: int = 0, limit: int = 20) -> Dict[str, Any]:
        """Get payments by customer ID with pagination"""
        try:
            # Get total count
            total = await self.payments_collection.count_documents({"customer_id": customer_id})

            # Get payments with pagination
            cursor = self.payments_collection.find({"customer_id": customer_id}).skip(skip).limit(limit).sort("created_at", -1)
            payments = []
            
            async for payment_doc in cursor:
                payment_doc["id"] = str(payment_doc["_id"])
                del payment_doc["_id"]
                payments.append(PaymentResponseSchema(**payment_doc))

            return {
                "payments": payments,
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
            
            # Order ID filter
            if search_params.order_id:
                filter_query["order_id"] = search_params.order_id

            # Customer ID filter
            if search_params.customer_id:
                filter_query["customer_id"] = search_params.customer_id

            # Status filter
            if search_params.status:
                filter_query["status"] = search_params.status

            # Payment method filter
            if search_params.payment_method:
                filter_query["payment_method.method_type"] = search_params.payment_method

            # Provider filter
            if search_params.provider:
                filter_query["payment_method.provider"] = search_params.provider

            # Amount range filter
            if search_params.min_amount is not None or search_params.max_amount is not None:
                amount_filter = {}
                if search_params.min_amount is not None:
                    amount_filter["$gte"] = search_params.min_amount
                if search_params.max_amount is not None:
                    amount_filter["$lte"] = search_params.max_amount
                filter_query["amount"] = amount_filter

            # Currency filter
            if search_params.currency:
                filter_query["currency"] = search_params.currency

            # Date range filter
            if search_params.start_date or search_params.end_date:
                date_filter = {}
                if search_params.start_date:
                    date_filter["$gte"] = search_params.start_date
                if search_params.end_date:
                    date_filter["$lte"] = search_params.end_date
                filter_query["created_at"] = date_filter

            # Build sort query
            sort_field = search_params.sort_by
            sort_order = -1 if search_params.sort_order.lower() == "desc" else 1
            sort_query = {sort_field: sort_order}

            # Get total count
            total = await self.payments_collection.count_documents(filter_query)

            # Get payments with pagination and sorting
            cursor = self.payments_collection.find(filter_query).skip(skip).limit(limit).sort(sort_query)
            payments = []
            
            async for payment_doc in cursor:
                payment_doc["id"] = str(payment_doc["_id"])
                del payment_doc["_id"]
                payments.append(PaymentResponseSchema(**payment_doc))

            return {
                "payments": payments,
                "total": total,
                "page": skip // limit + 1,
                "size": limit
            }

        except Exception as e:
            raise Exception(f"Failed to search payments: {str(e)}")

    async def update_payment(self, payment_id: str, update_data: PaymentUpdateSchema) -> Optional[PaymentResponseSchema]:
        """Update payment"""
        try:
            # Prepare update document
            update_doc = {"updated_at": datetime.utcnow()}
            
            # Add fields that are not None
            for field, value in update_data.dict(exclude_unset=True).items():
                update_doc[field] = value

            # Update payment in database
            result = await self.payments_collection.update_one(
                {"_id": ObjectId(payment_id)},
                {"$set": update_doc}
            )

            if result.modified_count > 0:
                # Return updated payment
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
            update_doc = {
                "status": status,
                "updated_at": datetime.utcnow()
            }

            if provider_payment_id:
                update_doc["provider_payment_id"] = provider_payment_id

            if failure_reason:
                update_doc["failure_reason"] = failure_reason

            if failure_code:
                update_doc["failure_code"] = failure_code

            if status in [PaymentStatus.COMPLETED, PaymentStatus.FAILED]:
                update_doc["processed_at"] = datetime.utcnow()

            result = await self.payments_collection.update_one(
                {"_id": ObjectId(payment_id)},
                {"$set": update_doc}
            )

            return result.modified_count > 0

        except Exception as e:
            raise Exception(f"Failed to update payment status: {str(e)}")

    async def process_payment(self, payment_id: str, provider_payment_id: str, 
                            provider_fee_amount: Optional[float] = None) -> bool:
        """Process a payment (mark as completed)"""
        try:
            # Get payment to calculate net amount
            payment = await self.get_payment_by_id(payment_id)
            if not payment:
                raise ValueError("Payment not found")

            # Calculate net amount after provider fees
            net_amount = payment.amount
            if payment.application_fee_amount:
                net_amount -= payment.application_fee_amount
            if provider_fee_amount:
                net_amount -= provider_fee_amount

            update_doc = {
                "status": PaymentStatus.COMPLETED,
                "provider_payment_id": provider_payment_id,
                "provider_fee_amount": provider_fee_amount,
                "net_amount": net_amount,
                "processed_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }

            result = await self.payments_collection.update_one(
                {"_id": ObjectId(payment_id)},
                {"$set": update_doc}
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
                raise ValueError("Payment not found")

            if payment.status not in [PaymentStatus.COMPLETED, PaymentStatus.PARTIALLY_REFUNDED]:
                raise ValueError("Payment cannot be refunded")

            # Determine refund amount
            refund_amount = refund_data.amount if refund_data.amount else payment.amount

            # Check if refund amount is valid
            if refund_amount > payment.amount:
                raise ValueError("Refund amount cannot exceed payment amount")

            # Generate unique refund ID
            refund_id = str(uuid.uuid4())

            # Prepare refund document
            refund_doc = {
                "_id": ObjectId(refund_id),
                "payment_id": refund_data.payment_id,
                "amount": refund_amount,
                "currency": payment.currency,
                "status": PaymentStatus.PENDING,
                "reason": refund_data.reason,
                "metadata": refund_data.metadata or {},
                "provider_refund_id": None,
                "failure_reason": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "processed_at": None
            }

            # Insert refund into database
            await self.refunds_collection.insert_one(refund_doc)
            refund_doc["id"] = str(refund_doc["_id"])
            del refund_doc["_id"]

            # Update payment status
            new_status = PaymentStatus.REFUNDED if refund_amount == payment.amount else PaymentStatus.PARTIALLY_REFUNDED
            await self.update_payment_status(payment.id, new_status)

            return RefundResponseSchema(**refund_doc)

        except Exception as e:
            raise Exception(f"Failed to create refund: {str(e)}")

    async def get_refund_by_id(self, refund_id: str) -> Optional[RefundResponseSchema]:
        """Get refund by ID"""
        try:
            refund_doc = await self.refunds_collection.find_one({"_id": ObjectId(refund_id)})
            if refund_doc:
                refund_doc["id"] = str(refund_doc["_id"])
                del refund_doc["_id"]
                return RefundResponseSchema(**refund_doc)
            return None
        except Exception:
            return None

    async def get_refunds_by_payment_id(self, payment_id: str) -> List[RefundResponseSchema]:
        """Get all refunds for a specific payment"""
        try:
            cursor = self.refunds_collection.find({"payment_id": payment_id}).sort("created_at", -1)
            refunds = []
            
            async for refund_doc in cursor:
                refund_doc["id"] = str(refund_doc["_id"])
                del refund_doc["_id"]
                refunds.append(RefundResponseSchema(**refund_doc))
            
            return refunds
        except Exception as e:
            raise Exception(f"Failed to retrieve refunds by payment ID: {str(e)}")

    async def create_payment_method(self, method_data: PaymentMethodCreateSchema) -> PaymentMethodResponseSchema:
        """Create a new payment method for a customer"""
        try:
            # Generate unique payment method ID
            method_id = str(uuid.uuid4())

            # If this is the default method, unset other default methods for this customer
            if method_data.is_default:
                await self.payment_methods_collection.update_many(
                    {"customer_id": method_data.customer_id, "is_default": True},
                    {"$set": {"is_default": False}}
                )

            # Prepare payment method document
            method_doc = {
                "_id": ObjectId(method_id),
                "customer_id": method_data.customer_id,
                "payment_method": method_data.payment_method.dict(),
                "is_default": method_data.is_default,
                "is_active": True,
                "metadata": method_data.metadata or {},
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }

            # Insert payment method into database
            await self.payment_methods_collection.insert_one(method_doc)
            method_doc["id"] = str(method_doc["_id"])
            del method_doc["_id"]

            return PaymentMethodResponseSchema(**method_doc)

        except Exception as e:
            raise Exception(f"Failed to create payment method: {str(e)}")

    async def get_payment_method_by_id(self, method_id: str) -> Optional[PaymentMethodResponseSchema]:
        """Get payment method by ID"""
        try:
            method_doc = await self.payment_methods_collection.find_one({"_id": ObjectId(method_id)})
            if method_doc:
                method_doc["id"] = str(method_doc["_id"])
                del method_doc["_id"]
                return PaymentMethodResponseSchema(**method_doc)
            return None
        except Exception:
            return None

    async def get_payment_methods_by_customer_id(self, customer_id: str) -> List[PaymentMethodResponseSchema]:
        """Get all payment methods for a customer"""
        try:
            cursor = self.payment_methods_collection.find({"customer_id": customer_id, "is_active": True}).sort("is_default", -1)
            methods = []
            
            async for method_doc in cursor:
                method_doc["id"] = str(method_doc["_id"])
                del method_doc["_id"]
                methods.append(PaymentMethodResponseSchema(**method_doc))
            
            return methods
        except Exception as e:
            raise Exception(f"Failed to retrieve payment methods by customer ID: {str(e)}")

    async def update_payment_method(self, method_id: str, update_data: PaymentMethodUpdateSchema) -> Optional[PaymentMethodResponseSchema]:
        """Update payment method"""
        try:
            # Prepare update document
            update_doc = {"updated_at": datetime.utcnow()}
            
            # Add fields that are not None
            for field, value in update_data.dict(exclude_unset=True).items():
                update_doc[field] = value

            # If setting as default, unset other default methods for this customer
            if update_data.is_default:
                method = await self.get_payment_method_by_id(method_id)
                if method:
                    await self.payment_methods_collection.update_many(
                        {"customer_id": method.customer_id, "is_default": True, "_id": {"$ne": ObjectId(method_id)}},
                        {"$set": {"is_default": False}}
                    )

            # Update payment method in database
            result = await self.payment_methods_collection.update_one(
                {"_id": ObjectId(method_id)},
                {"$set": update_doc}
            )

            if result.modified_count > 0:
                # Return updated payment method
                return await self.get_payment_method_by_id(method_id)
            return None

        except Exception as e:
            raise Exception(f"Failed to update payment method: {str(e)}")

    async def delete_payment_method(self, method_id: str) -> bool:
        """Delete (deactivate) a payment method"""
        try:
            result = await self.payment_methods_collection.update_one(
                {"_id": ObjectId(method_id)},
                {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
            )

            return result.modified_count > 0

        except Exception as e:
            raise Exception(f"Failed to delete payment method: {str(e)}")

    async def create_payment_intent(self, intent_data: PaymentIntentSchema) -> PaymentIntentResponseSchema:
        """Create a payment intent for future payment processing"""
        try:
            # Generate unique payment intent ID
            intent_id = str(uuid.uuid4())

            # Prepare payment intent document
            intent_doc = {
                "_id": ObjectId(intent_id),
                "amount": intent_data.amount,
                "currency": intent_data.currency,
                "customer_id": intent_data.customer_id,
                "status": PaymentStatus.PENDING,
                "payment_method": intent_data.payment_method,
                "description": intent_data.description,
                "metadata": intent_data.metadata or {},
                "capture_method": intent_data.capture_method,
                "statement_descriptor": intent_data.statement_descriptor,
                "receipt_email": intent_data.receipt_email,
                "application_fee_amount": intent_data.application_fee_amount,
                "client_secret": f"pi_{intent_id}_secret_{uuid.uuid4().hex[:24]}",
                "next_action": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }

            # Insert payment intent into database
            await self.payment_intents_collection.insert_one(intent_doc)
            intent_doc["id"] = str(intent_doc["_id"])
            del intent_doc["_id"]

            return PaymentIntentResponseSchema(**intent_doc)

        except Exception as e:
            raise Exception(f"Failed to create payment intent: {str(e)}")

    async def get_payment_intent_by_id(self, intent_id: str) -> Optional[PaymentIntentResponseSchema]:
        """Get payment intent by ID"""
        try:
            intent_doc = await self.payment_intents_collection.find_one({"_id": ObjectId(intent_id)})
            if intent_doc:
                intent_doc["id"] = str(intent_doc["_id"])
                del intent_doc["_id"]
                return PaymentIntentResponseSchema(**intent_doc)
            return None
        except Exception:
            return None

    async def update_payment_intent_status(self, intent_id: str, status: PaymentStatus, 
                                        next_action: Optional[Dict[str, Any]] = None) -> bool:
        """Update payment intent status"""
        try:
            update_doc = {
                "status": status,
                "updated_at": datetime.utcnow()
            }

            if next_action:
                update_doc["next_action"] = next_action

            result = await self.payment_intents_collection.update_one(
                {"_id": ObjectId(intent_id)},
                {"$set": update_doc}
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
                raise ValueError("Payment not found")

            if payment.status != PaymentStatus.PROCESSING:
                raise ValueError("Payment is not in processing state")

            # Determine capture amount
            capture_amount = capture_data.amount if capture_data.amount else payment.amount

            # Check if capture amount is valid
            if capture_amount > payment.amount:
                raise ValueError("Capture amount cannot exceed payment amount")

            # Update payment status to completed
            update_doc = {
                "status": PaymentStatus.COMPLETED,
                "processed_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }

            # Add optional fields if provided
            if capture_data.statement_descriptor:
                update_doc["statement_descriptor"] = capture_data.statement_descriptor
            if capture_data.receipt_email:
                update_doc["receipt_email"] = capture_data.receipt_email
            if capture_data.metadata:
                update_doc["metadata"] = {**payment.metadata, **capture_data.metadata}

            result = await self.payments_collection.update_one(
                {"_id": ObjectId(payment_id)},
                {"$set": update_doc}
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

            # Base filter
            base_filter = {}
            if date_filter:
                base_filter["created_at"] = date_filter

            # Get basic counts
            total_payments = await self.payments_collection.count_documents(base_filter)
            successful_payments = await self.payments_collection.count_documents({
                **base_filter, "status": {"$in": [PaymentStatus.COMPLETED, PaymentStatus.PARTIALLY_REFUNDED]}
            })
            failed_payments = await self.payments_collection.count_documents({
                **base_filter, "status": PaymentStatus.FAILED
            })
            pending_payments = await self.payments_collection.count_documents({
                **base_filter, "status": {"$in": [PaymentStatus.PENDING, PaymentStatus.PROCESSING]}
            })

            # Get amount statistics
            pipeline = [
                {"$match": base_filter} if base_filter else {"$match": {}},
                {"$group": {
                    "_id": None,
                    "total_amount": {"$sum": "$amount"},
                    "avg_amount": {"$avg": "$amount"}
                }}
            ]
            
            amount_stats = await self.payments_collection.aggregate(pipeline).to_list(1)
            total_amount = amount_stats[0]["total_amount"] if amount_stats else 0
            average_payment_amount = amount_stats[0]["avg_amount"] if amount_stats else 0

            # Get refund statistics
            refund_pipeline = [
                {"$match": {"status": {"$in": [PaymentStatus.REFUNDED, PaymentStatus.PARTIALLY_REFUNDED]}}},
                {"$group": {"_id": None, "total_refunded": {"$sum": "$amount"}}}
            ]
            
            refund_stats = await self.refunds_collection.aggregate(refund_pipeline).to_list(1)
            refunded_amount = refund_stats[0]["total_refunded"] if refund_stats else 0

            # Calculate net revenue
            net_revenue = total_amount - refunded_amount

            # Get currency distribution
            currency_pipeline = [
                {"$match": base_filter} if base_filter else {"$match": {}},
                {"$group": {"_id": "$currency", "count": {"$sum": 1}, "total": {"$sum": "$amount"}}},
                {"$sort": {"total": -1}}
            ]
            
            currency_distribution = []
            async for doc in self.payments_collection.aggregate(currency_pipeline):
                currency_distribution.append({
                    "currency": doc["_id"],
                    "count": doc["count"],
                    "total": doc["total"]
                })

            # Get payment method distribution
            method_pipeline = [
                {"$match": base_filter} if base_filter else {"$match": {}},
                {"$group": {"_id": "$payment_method.method_type", "count": {"$sum": 1}, "total": {"$sum": "$amount"}}},
                {"$sort": {"total": -1}}
            ]
            
            method_distribution = []
            async for doc in self.payments_collection.aggregate(method_pipeline):
                method_distribution.append({
                    "method": doc["_id"],
                    "count": doc["count"],
                    "total": doc["total"]
                })

            # Get provider distribution
            provider_pipeline = [
                {"$match": base_filter} if base_filter else {"$match": {}},
                {"$group": {"_id": "$payment_method.provider", "count": {"$sum": 1}, "total": {"$sum": "$amount"}}},
                {"$sort": {"total": -1}}
            ]
            
            provider_distribution = []
            async for doc in self.payments_collection.aggregate(provider_pipeline):
                provider_distribution.append({
                    "provider": doc["_id"],
                    "count": doc["count"],
                    "total": doc["total"]
                })

            return PaymentStatisticsSchema(
                total_payments=total_payments,
                total_amount=total_amount,
                successful_payments=successful_payments,
                failed_payments=failed_payments,
                pending_payments=pending_payments,
                refunded_amount=refunded_amount,
                net_revenue=net_revenue,
                average_payment_amount=average_payment_amount,
                currency_distribution=currency_distribution,
                method_distribution=method_distribution,
                provider_distribution=provider_distribution
            )

        except Exception as e:
            raise Exception(f"Failed to get payment statistics: {str(e)}")

    async def create_webhook_event(self, event_data: WebhookEventSchema) -> WebhookEventSchema:
        """Create a webhook event for processing"""
        try:
            # Generate unique webhook event ID
            event_id = str(uuid.uuid4())

            # Prepare webhook event document
            event_doc = {
                "_id": ObjectId(event_id),
                "provider": event_data.provider,
                "event_type": event_data.event_type,
                "payment_id": event_data.payment_id,
                "data": event_data.data,
                "processed": False,
                "created_at": datetime.utcnow(),
                "processed_at": None
            }

            # Insert webhook event into database
            await self.webhook_events_collection.insert_one(event_doc)
            event_doc["id"] = str(event_doc["_id"])
            del event_doc["_id"]

            return WebhookEventSchema(**event_doc)

        except Exception as e:
            raise Exception(f"Failed to create webhook event: {str(e)}")

    async def mark_webhook_event_processed(self, event_id: str) -> bool:
        """Mark a webhook event as processed"""
        try:
            result = await self.webhook_events_collection.update_one(
                {"_id": ObjectId(event_id)},
                {"$set": {"processed": True, "processed_at": datetime.utcnow()}}
            )

            return result.modified_count > 0

        except Exception as e:
            raise Exception(f"Failed to mark webhook event as processed: {str(e)}")

    async def get_unprocessed_webhook_events(self, provider: Optional[PaymentProvider] = None) -> List[WebhookEventSchema]:
        """Get unprocessed webhook events"""
        try:
            filter_query = {"processed": False}
            if provider:
                filter_query["provider"] = provider

            cursor = self.webhook_events_collection.find(filter_query).sort("created_at", 1)
            events = []
            
            async for event_doc in cursor:
                event_doc["id"] = str(event_doc["_id"])
                del event_doc["_id"]
                events.append(WebhookEventSchema(**event_doc))
            
            return events
        except Exception as e:
            raise Exception(f"Failed to retrieve unprocessed webhook events: {str(e)}")
