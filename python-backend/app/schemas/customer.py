from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"
    prefer_not_to_say = "prefer_not_to_say"

class CustomerCreateSchema(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100, description="Customer's first name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Customer's last name")
    email: EmailStr = Field(..., description="Customer's email address")
    phone: Optional[str] = Field(None, max_length=20, description="Customer's phone number")
    
    # Address fields
    address_line1: Optional[str] = Field(None, max_length=255, description="Primary address line")
    address_line2: Optional[str] = Field(None, max_length=255, description="Secondary address line")
    city: Optional[str] = Field(None, max_length=100, description="City")
    state: Optional[str] = Field(None, max_length=100, description="State/Province")
    postal_code: Optional[str] = Field(None, max_length=20, description="Postal/ZIP code")
    country: Optional[str] = Field(None, max_length=100, description="Country")
    
    # Customer details
    date_of_birth: Optional[str] = Field(None, description="Date of birth (YYYY-MM-DD format)")
    gender: Optional[Gender] = Field(None, description="Gender")
    company_name: Optional[str] = Field(None, max_length=255, description="Company name")
    tax_id: Optional[str] = Field(None, max_length=50, description="Tax identification number")
    
    # Marketing preferences
    marketing_emails: bool = Field(True, description="Opt-in for marketing emails")
    marketing_sms: bool = Field(False, description="Opt-in for marketing SMS")
    
    # Notes and metadata
    notes: Optional[str] = Field(None, description="Additional notes about the customer")
    tags: Optional[str] = Field(None, max_length=500, description="Comma-separated tags")

class CustomerUpdateSchema(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = Field(None)
    phone: Optional[str] = Field(None, max_length=20)
    
    # Address fields
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    
    # Customer details
    date_of_birth: Optional[str] = Field(None, description="Date of birth (YYYY-MM-DD format)")
    gender: Optional[Gender] = Field(None)
    company_name: Optional[str] = Field(None, max_length=255)
    tax_id: Optional[str] = Field(None, max_length=50)
    
    # Status fields
    is_active: Optional[bool] = Field(None)
    is_verified: Optional[bool] = Field(None)
    email_verified: Optional[bool] = Field(None)
    phone_verified: Optional[bool] = Field(None)
    
    # Marketing preferences
    marketing_emails: Optional[bool] = Field(None)
    marketing_sms: Optional[bool] = Field(None)
    
    # Notes and metadata
    notes: Optional[str] = Field(None)
    tags: Optional[str] = Field(None, max_length=500)

class CustomerResponseSchema(BaseModel):
    id: int
    customer_id: str
    username: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    
    # Address fields
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    
    # Customer details
    date_of_birth: Optional[str]
    gender: Optional[str]
    company_name: Optional[str]
    tax_id: Optional[str]
    
    # Status and preferences
    is_active: bool
    is_verified: bool
    email_verified: bool
    phone_verified: bool
    marketing_emails: bool
    marketing_sms: bool
    
    # Notes and metadata
    notes: Optional[str]
    tags: Optional[str]
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime]
    
    # Computed properties
    full_name: str
    full_address: Optional[str]
    
    class Config:
        from_attributes = True

class CustomerListResponseSchema(BaseModel):
    customers: List[CustomerResponseSchema]
    total: int
    page: int
    limit: int
    total_pages: int

class CustomerSearchSchema(BaseModel):
    query: Optional[str] = Field(None, description="Search query for name, email, or username")
    first_name: Optional[str] = Field(None, description="Filter by first name")
    last_name: Optional[str] = Field(None, description="Filter by last name")
    email: Optional[str] = Field(None, description="Filter by email")
    phone: Optional[str] = Field(None, description="Filter by phone")
    city: Optional[str] = Field(None, description="Filter by city")
    state: Optional[str] = Field(None, description="Filter by state")
    country: Optional[str] = Field(None, description="Filter by country")
    is_active: Optional[bool] = Field(None, description="Filter by active status")
    is_verified: Optional[bool] = Field(None, description="Filter by verification status")
    company_name: Optional[str] = Field(None, description="Filter by company name")
    tags: Optional[str] = Field(None, description="Filter by tags (comma-separated)")
    created_after: Optional[datetime] = Field(None, description="Filter by creation date (after)")
    created_before: Optional[datetime] = Field(None, description="Filter by creation date (before)")
    sort_by: str = Field("created_at", description="Sort field")
    sort_order: str = Field("desc", description="Sort order (asc/desc)")
    page: int = Field(1, ge=1, description="Page number")
    limit: int = Field(10, ge=1, le=100, description="Items per page")

class CustomerBulkUpdateSchema(BaseModel):
    customer_ids: List[str] = Field(..., description="List of customer IDs to update")
    updates: CustomerUpdateSchema = Field(..., description="Updates to apply to all customers")

class CustomerStatisticsSchema(BaseModel):
    total_customers: int
    active_customers: int
    verified_customers: int
    new_customers_today: int
    new_customers_this_week: int
    new_customers_this_month: int
    customers_by_country: dict
    customers_by_city: dict
    average_customer_age: Optional[float]
    gender_distribution: dict
