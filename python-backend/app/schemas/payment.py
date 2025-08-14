from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from decimal import Decimal

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    DISPUTED = "disputed"

class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    DIGITAL_WALLET = "digital_wallet"
    CRYPTOCURRENCY = "cryptocurrency"
    CASH = "cash"
    CHECK = "check"
    OTHER = "other"

class PaymentProvider(str, Enum):
    STRIPE = "stripe"
    PAYPAL = "paypal"
    SQUARE = "square"
    BRAINTREE = "braintree"
    ADYEN = "adyen"
    RAZORPAY = "razorpay"
    CUSTOM = "custom"

class TransactionType(str, Enum):
    PAYMENT = "payment"
    REFUND = "refund"
    CHARGEBACK = "chargeback"
    ADJUSTMENT = "adjustment"
    FEE = "fee"

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"
    AUD = "AUD"
    JPY = "JPY"
    INR = "INR"
    CNY = "CNY"
    BRL = "BRL"
    MXN = "MXN"

class PaymentMethodDetails(BaseModel):
    method_type: PaymentMethod = Field(..., description="Type of payment method")
    provider: PaymentProvider = Field(..., description="Payment provider")
    account_id: Optional[str] = Field(None, description="Account identifier with provider")
    last_four: Optional[str] = Field(None, description="Last four digits of card/account")
    expiry_month: Optional[int] = Field(None, ge=1, le=12, description="Expiry month")
    expiry_year: Optional[int] = Field(None, ge=2020, description="Expiry year")
    card_brand: Optional[str] = Field(None, description="Card brand (Visa, Mastercard, etc.)")
    bank_name: Optional[str] = Field(None, description="Bank name for bank transfers")
    wallet_type: Optional[str] = Field(None, description="Digital wallet type")
    crypto_address: Optional[str] = Field(None, description="Cryptocurrency address")

class PaymentCreateSchema(BaseModel):
    order_id: str = Field(..., description="Associated order ID")
    customer_id: str = Field(..., description="Customer ID making the payment")
    amount: float = Field(..., gt=0, description="Payment amount")
    currency: Currency = Field(..., description="Payment currency")
    payment_method: PaymentMethodDetails = Field(..., description="Payment method details")
    description: Optional[str] = Field(None, max_length=500, description="Payment description")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    capture_method: str = Field("automatic", description="Capture method (automatic/manual)")
    statement_descriptor: Optional[str] = Field(None, max_length=22, description="Statement descriptor")
    receipt_email: Optional[str] = Field(None, description="Email for receipt")
    application_fee_amount: Optional[float] = Field(None, ge=0, description="Application fee amount")

class PaymentUpdateSchema(BaseModel):
    description: Optional[str] = Field(None, max_length=500)
    metadata: Optional[Dict[str, Any]] = None
    statement_descriptor: Optional[str] = Field(None, max_length=22)
    receipt_email: Optional[str] = None
    application_fee_amount: Optional[float] = Field(None, ge=0)

class PaymentResponseSchema(BaseModel):
    id: str = Field(..., description="Payment ID")
    order_id: str = Field(..., description="Associated order ID")
    customer_id: str = Field(..., description="Customer ID")
    amount: float = Field(..., description="Payment amount")
    currency: Currency = Field(..., description="Payment currency")
    payment_method: PaymentMethodDetails = Field(..., description="Payment method details")
    status: PaymentStatus = Field(..., description="Payment status")
    description: Optional[str] = Field(None, description="Payment description")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    capture_method: str = Field(..., description="Capture method")
    statement_descriptor: Optional[str] = Field(None, description="Statement descriptor")
    receipt_email: Optional[str] = Field(None, description="Email for receipt")
    application_fee_amount: Optional[float] = Field(None, description="Application fee amount")
    provider_payment_id: Optional[str] = Field(None, description="Provider's payment ID")
    provider_fee_amount: Optional[float] = Field(None, description="Provider fee amount")
    net_amount: float = Field(..., description="Net amount after fees")
    failure_reason: Optional[str] = Field(None, description="Reason for failure if applicable")
    failure_code: Optional[str] = Field(None, description="Failure code if applicable")
    created_at: datetime = Field(..., description="Payment creation timestamp")
    updated_at: datetime = Field(..., description="Payment last update timestamp")
    processed_at: Optional[datetime] = Field(None, description="When payment was processed")

class PaymentListResponseSchema(BaseModel):
    payments: List[PaymentResponseSchema] = Field(..., description="List of payments")
    total: int = Field(..., description="Total number of payments")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")

class PaymentSearchSchema(BaseModel):
    order_id: Optional[str] = Field(None, description="Filter by order ID")
    customer_id: Optional[str] = Field(None, description="Filter by customer ID")
    status: Optional[PaymentStatus] = Field(None, description="Filter by payment status")
    payment_method: Optional[PaymentMethod] = Field(None, description="Filter by payment method")
    provider: Optional[PaymentProvider] = Field(None, description="Filter by payment provider")
    min_amount: Optional[float] = Field(None, ge=0, description="Minimum amount")
    max_amount: Optional[float] = Field(None, ge=0, description="Maximum amount")
    currency: Optional[Currency] = Field(None, description="Filter by currency")
    start_date: Optional[datetime] = Field(None, description="Start date for date range")
    end_date: Optional[datetime] = Field(None, description="End date for date range")
    sort_by: str = Field("created_at", description="Sort field")
    sort_order: str = Field("desc", description="Sort order (asc/desc)")

class RefundCreateSchema(BaseModel):
    payment_id: str = Field(..., description="Payment ID to refund")
    amount: Optional[float] = Field(None, gt=0, description="Refund amount (full if not specified)")
    reason: Optional[str] = Field(None, max_length=500, description="Refund reason")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    receipt_email: Optional[str] = Field(None, description="Email for refund receipt")

class RefundResponseSchema(BaseModel):
    id: str = Field(..., description="Refund ID")
    payment_id: str = Field(..., description="Original payment ID")
    amount: float = Field(..., description="Refund amount")
    currency: Currency = Field(..., description="Refund currency")
    status: PaymentStatus = Field(..., description="Refund status")
    reason: Optional[str] = Field(None, description="Refund reason")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    provider_refund_id: Optional[str] = Field(None, description="Provider's refund ID")
    failure_reason: Optional[str] = Field(None, description="Reason for failure if applicable")
    created_at: datetime = Field(..., description="Refund creation timestamp")
    updated_at: datetime = Field(..., description="Refund last update timestamp")
    processed_at: Optional[datetime] = Field(None, description="When refund was processed")

class PaymentMethodCreateSchema(BaseModel):
    customer_id: str = Field(..., description="Customer ID")
    payment_method: PaymentMethodDetails = Field(..., description="Payment method details")
    is_default: bool = Field(False, description="Whether this is the default payment method")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class PaymentMethodUpdateSchema(BaseModel):
    is_default: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None

class PaymentMethodResponseSchema(BaseModel):
    id: str = Field(..., description="Payment method ID")
    customer_id: str = Field(..., description="Customer ID")
    payment_method: PaymentMethodDetails = Field(..., description="Payment method details")
    is_default: bool = Field(..., description="Whether this is the default payment method")
    is_active: bool = Field(..., description="Whether this payment method is active")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    created_at: datetime = Field(..., description="Payment method creation timestamp")
    updated_at: datetime = Field(..., description="Payment method last update timestamp")

class PaymentMethodListResponseSchema(BaseModel):
    payment_methods: List[PaymentMethodResponseSchema] = Field(..., description="List of payment methods")
    total: int = Field(..., description="Total number of payment methods")

class PaymentCaptureSchema(BaseModel):
    amount: Optional[float] = Field(None, gt=0, description="Amount to capture (full if not specified)")
    statement_descriptor: Optional[str] = Field(None, max_length=22, description="Statement descriptor")
    receipt_email: Optional[str] = Field(None, description="Email for receipt")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class PaymentIntentSchema(BaseModel):
    amount: float = Field(..., gt=0, description="Payment amount")
    currency: Currency = Field(..., description="Payment currency")
    customer_id: str = Field(..., description="Customer ID")
    payment_method: Optional[str] = Field(None, description="Payment method ID")
    description: Optional[str] = Field(None, max_length=500, description="Payment description")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    capture_method: str = Field("automatic", description="Capture method (automatic/manual)")
    statement_descriptor: Optional[str] = Field(None, max_length=22, description="Statement descriptor")
    receipt_email: Optional[str] = Field(None, description="Email for receipt")
    application_fee_amount: Optional[float] = Field(None, ge=0, description="Application fee amount")

class PaymentIntentResponseSchema(BaseModel):
    id: str = Field(..., description="Payment intent ID")
    amount: float = Field(..., description="Payment amount")
    currency: Currency = Field(..., description="Payment currency")
    customer_id: str = Field(..., description="Customer ID")
    status: PaymentStatus = Field(..., description="Payment intent status")
    payment_method: Optional[str] = Field(None, description="Payment method ID")
    description: Optional[str] = Field(None, description="Payment description")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    capture_method: str = Field(..., description="Capture method")
    statement_descriptor: Optional[str] = Field(None, description="Statement descriptor")
    receipt_email: Optional[str] = Field(None, description="Email for receipt")
    application_fee_amount: Optional[float] = Field(None, description="Application fee amount")
    client_secret: Optional[str] = Field(None, description="Client secret for frontend")
    next_action: Optional[Dict[str, Any]] = Field(None, description="Next action required")
    created_at: datetime = Field(..., description="Payment intent creation timestamp")
    updated_at: datetime = Field(..., description="Payment intent last update timestamp")

class PaymentStatisticsSchema(BaseModel):
    total_payments: int = Field(..., description="Total number of payments")
    total_amount: float = Field(..., description="Total payment amount")
    successful_payments: int = Field(..., description="Number of successful payments")
    failed_payments: int = Field(..., description="Number of failed payments")
    pending_payments: int = Field(..., description="Number of pending payments")
    refunded_amount: float = Field(..., description="Total refunded amount")
    net_revenue: float = Field(..., description="Net revenue after refunds")
    average_payment_amount: float = Field(..., description="Average payment amount")
    currency_distribution: List[Dict[str, Any]] = Field(..., description="Distribution by currency")
    method_distribution: List[Dict[str, Any]] = Field(..., description="Distribution by payment method")
    provider_distribution: List[Dict[str, Any]] = Field(..., description="Distribution by provider")

class WebhookEventSchema(BaseModel):
    id: str = Field(..., description="Webhook event ID")
    provider: PaymentProvider = Field(..., description="Payment provider")
    event_type: str = Field(..., description="Type of webhook event")
    payment_id: Optional[str] = Field(None, description="Associated payment ID")
    data: Dict[str, Any] = Field(..., description="Webhook event data")
    processed: bool = Field(False, description="Whether event has been processed")
    created_at: datetime = Field(..., description="Webhook event creation timestamp")
    processed_at: Optional[datetime] = Field(None, description="When event was processed")
