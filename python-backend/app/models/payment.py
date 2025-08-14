from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, JSON, Index, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
from datetime import datetime

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(String(50), unique=True, index=True, nullable=False)
    order_id = Column(String(50), nullable=False, index=True)
    customer_id = Column(String(50), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    payment_method_data = Column(JSON, nullable=False)  # Store PaymentMethodDetails as JSON
    status = Column(String(20), nullable=False, default="pending")
    description = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)
    capture_method = Column(String(20), nullable=False, default="automatic")
    statement_descriptor = Column(String(22), nullable=True)
    receipt_email = Column(String(255), nullable=True)
    application_fee_amount = Column(Float, nullable=True)
    provider_payment_id = Column(String(100), nullable=True)
    provider_fee_amount = Column(Float, nullable=True)
    net_amount = Column(Float, nullable=False)
    failure_reason = Column(Text, nullable=True)
    failure_code = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.payment_id:
            self.payment_id = f"PAY_{uuid.uuid4().hex[:8].upper()}"

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    method_id = Column(String(50), unique=True, index=True, nullable=False)
    customer_id = Column(String(50), nullable=False, index=True)
    payment_type = Column(String(20), nullable=False)
    payment_provider = Column(String(20), nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    payment_method_details = Column(JSON, nullable=False)  # Store PaymentMethodDetails as JSON
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.method_id:
            self.method_id = f"PM_{uuid.uuid4().hex[:8].upper()}"

class PaymentIntent(Base):
    __tablename__ = "payment_intents"

    id = Column(Integer, primary_key=True, index=True)
    intent_id = Column(String(50), unique=True, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    customer_id = Column(String(50), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="requires_payment_method")
    payment_method = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)
    capture_method = Column(String(20), nullable=False, default="automatic")
    statement_descriptor = Column(String(22), nullable=True)
    receipt_email = Column(String(255), nullable=True)
    application_fee_amount = Column(Float, nullable=True)
    client_secret = Column(String(255), nullable=True)
    next_action = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.intent_id:
            self.intent_id = f"PI_{uuid.uuid4().hex[:8].upper()}"

class Refund(Base):
    __tablename__ = "refunds"

    id = Column(Integer, primary_key=True, index=True)
    refund_id = Column(String(50), unique=True, index=True, nullable=False)
    payment_id = Column(String(50), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    reason = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)
    provider_refund_id = Column(String(100), nullable=True)
    failure_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.refund_id:
            self.refund_id = f"REF_{uuid.uuid4().hex[:8].upper()}"

class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String(50), unique=True, index=True, nullable=False)
    provider = Column(String(20), nullable=False)
    event_type = Column(String(100), nullable=False)
    payment_id = Column(String(50), nullable=True, index=True)
    data = Column(JSON, nullable=False)
    processed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.event_id:
            self.event_id = f"WEB_{uuid.uuid4().hex[:8].upper()}"

# Create indexes for better query performance
Index('idx_payments_order_id', Payment.order_id)
Index('idx_payments_customer_id', Payment.customer_id)
Index('idx_payments_status', Payment.status)
Index('idx_payments_created_at', Payment.created_at)
Index('idx_payments_currency', Payment.currency)

Index('idx_payment_methods_customer_id', PaymentMethod.customer_id)
Index('idx_payment_methods_is_default', PaymentMethod.is_default)
Index('idx_payment_methods_is_active', PaymentMethod.is_active)

Index('idx_payment_intents_customer_id', PaymentIntent.customer_id)
Index('idx_payment_intents_status', PaymentIntent.status)

Index('idx_refunds_payment_id', Refund.payment_id)
Index('idx_refunds_status', Refund.status)

Index('idx_webhook_events_provider', WebhookEvent.provider)
Index('idx_webhook_events_processed', WebhookEvent.processed)
Index('idx_webhook_events_created_at', WebhookEvent.created_at)
