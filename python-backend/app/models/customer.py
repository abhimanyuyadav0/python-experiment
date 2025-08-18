from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(50), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    
    # Address fields
    address_line1 = Column(String(255), nullable=True)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True)
    
    # Customer details
    date_of_birth = Column(String(10), nullable=True)  # YYYY-MM-DD format
    gender = Column(String(20), nullable=True)
    company_name = Column(String(255), nullable=True)
    tax_id = Column(String(50), nullable=True)
    
    # Status and preferences
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    phone_verified = Column(Boolean, default=False, nullable=False)
    
    # Marketing preferences
    marketing_emails = Column(Boolean, default=True, nullable=False)
    marketing_sms = Column(Boolean, default=False, nullable=False)
    
    # Notes and metadata
    notes = Column(Text, nullable=True)
    tags = Column(String(500), nullable=True)  # Comma-separated tags
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    orders = relationship("Order", back_populates="customer", lazy="dynamic")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.customer_id:
            self.customer_id = f"CUST_{uuid.uuid4().hex[:8].upper()}"
        if not self.username:
            self.username = self._generate_username()
    
    def _generate_username(self):
        """Generate a unique username based on first and last name"""
        base_username = f"{self.first_name.lower()}{self.last_name.lower()}"
        base_username = ''.join(c for c in base_username if c.isalnum())
        
        # If username is too long, truncate it
        if len(base_username) > 20:
            base_username = base_username[:20]
        
        # Add random suffix to ensure uniqueness
        suffix = uuid.uuid4().hex[:4]
        return f"{base_username}{suffix}"
    
    @property
    def full_name(self):
        """Get the full name of the customer"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_address(self):
        """Get the formatted full address"""
        address_parts = []
        if self.address_line1:
            address_parts.append(self.address_line1)
        if self.address_line2:
            address_parts.append(self.address_line2)
        if self.city:
            address_parts.append(self.city)
        if self.state:
            address_parts.append(self.state)
        if self.postal_code:
            address_parts.append(self.postal_code)
        if self.country:
            address_parts.append(self.country)
        
        return ", ".join(address_parts) if address_parts else None

# Create indexes for better query performance
Index('idx_customers_email', Customer.email)
Index('idx_customers_username', Customer.username)
Index('idx_customers_customer_id', Customer.customer_id)
Index('idx_customers_phone', Customer.phone)
Index('idx_customers_city', Customer.city)
Index('idx_customers_country', Customer.country)
Index('idx_customers_is_active', Customer.is_active)
Index('idx_customers_created_at', Customer.created_at)
