from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.services.customer_service import CustomerService
from app.models.customer import Customer
from app.schemas.customer import (
    CustomerCreateSchema,
    CustomerUpdateSchema,
    CustomerResponseSchema,
    CustomerListResponseSchema,
    CustomerSearchSchema,
    CustomerBulkUpdateSchema,
    CustomerStatisticsSchema
)

router = APIRouter()

@router.post("/", response_model=CustomerResponseSchema, summary="Create Customer", description="Create a new customer with auto-generated username and customer_id")
async def create_customer(
    customer_data: CustomerCreateSchema,
    db: Session = Depends(get_db)
):
    """Create a new customer"""
    customer_service = CustomerService(db)
    
    # Check if email already exists
    existing_customer = customer_service.get_customer_by_email(customer_data.email)
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer with this email already exists"
        )
    
    customer = customer_service.create_customer(customer_data)
    return customer

@router.get("/{customer_id}", response_model=CustomerResponseSchema, summary="Get Customer by ID", description="Retrieve customer information by customer_id")
async def get_customer(
    customer_id: str,
    db: Session = Depends(get_db)
):
    """Get customer by customer_id"""
    customer_service = CustomerService(db)
    customer = customer_service.get_customer_by_id(customer_id)
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return customer

@router.get("/username/{username}", response_model=CustomerResponseSchema, summary="Get Customer by Username", description="Retrieve customer information by username")
async def get_customer_by_username(
    username: str,
    db: Session = Depends(get_db)
):
    """Get customer by username"""
    customer_service = CustomerService(db)
    customer = customer_service.get_customer_by_username(username)
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return customer

@router.get("/email/{email}", response_model=CustomerResponseSchema, summary="Get Customer by Email", description="Retrieve customer information by email")
async def get_customer_by_email(
    email: str,
    db: Session = Depends(get_db)
):
    """Get customer by email"""
    customer_service = CustomerService(db)
    customer = customer_service.get_customer_by_email(email)
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return customer

@router.get("/", response_model=CustomerListResponseSchema, summary="Get All Customers", description="Retrieve all customers with pagination and filtering")
async def get_customers(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """Get all customers with optional filtering"""
    customer_service = CustomerService(db)
    customers = customer_service.get_all_customers(skip=skip, limit=limit, is_active=is_active)
    
    total = db.query(Customer).count()
    
    return {
        "customers": customers,
        "total": total,
        "page": (skip // limit) + 1,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit
    }

@router.post("/search", response_model=CustomerListResponseSchema, summary="Search Customers", description="Advanced customer search with filtering, sorting, and pagination")
async def search_customers(
    search_params: CustomerSearchSchema,
    db: Session = Depends(get_db)
):
    """Search customers with advanced filtering"""
    customer_service = CustomerService(db)
    result = customer_service.search_customers(search_params)
    return result

@router.put("/{customer_id}", response_model=CustomerResponseSchema, summary="Update Customer", description="Update customer information")
async def update_customer(
    customer_id: str,
    customer_data: CustomerUpdateSchema,
    db: Session = Depends(get_db)
):
    """Update customer information"""
    customer_service = CustomerService(db)
    
    # Check if email is being updated and if it already exists
    if customer_data.email:
        existing_customer = customer_service.get_customer_by_email(customer_data.email)
        if existing_customer and existing_customer.customer_id != customer_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer with this email already exists"
            )
    
    customer = customer_service.update_customer(customer_id, customer_data)
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return customer

@router.delete("/{customer_id}", summary="Delete Customer", description="Soft delete customer (sets is_active to False)")
async def delete_customer(
    customer_id: str,
    db: Session = Depends(get_db)
):
    """Delete customer (soft delete)"""
    customer_service = CustomerService(db)
    success = customer_service.delete_customer(customer_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return {"message": "Customer deleted successfully"}

@router.delete("/{customer_id}/hard", summary="Hard Delete Customer", description="Permanently delete customer from database")
async def hard_delete_customer(
    customer_id: str,
    db: Session = Depends(get_db)
):
    """Hard delete customer"""
    customer_service = CustomerService(db)
    success = customer_service.hard_delete_customer(customer_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return {"message": "Customer permanently deleted"}

@router.post("/bulk-update", summary="Bulk Update Customers", description="Update multiple customers at once")
async def bulk_update_customers(
    bulk_update_data: CustomerBulkUpdateSchema,
    db: Session = Depends(get_db)
):
    """Bulk update customers"""
    customer_service = CustomerService(db)
    result = customer_service.bulk_update_customers(bulk_update_data)
    return result

@router.patch("/{customer_id}/verify-email", summary="Verify Customer Email", description="Mark customer email as verified")
async def verify_customer_email(
    customer_id: str,
    db: Session = Depends(get_db)
):
    """Verify customer email"""
    customer_service = CustomerService(db)
    success = customer_service.verify_customer_email(customer_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return {"message": "Customer email verified successfully"}

@router.patch("/{customer_id}/verify-phone", summary="Verify Customer Phone", description="Mark customer phone as verified")
async def verify_customer_phone(
    customer_id: str,
    db: Session = Depends(get_db)
):
    """Verify customer phone"""
    customer_service = CustomerService(db)
    success = customer_service.verify_customer_phone(customer_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return {"message": "Customer phone verified successfully"}

@router.patch("/{customer_id}/last-login", summary="Update Last Login", description="Update customer's last login timestamp")
async def update_last_login(
    customer_id: str,
    db: Session = Depends(get_db)
):
    """Update customer last login"""
    customer_service = CustomerService(db)
    success = customer_service.update_last_login(customer_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return {"message": "Last login updated successfully"}

@router.get("/statistics/overview", response_model=CustomerStatisticsSchema, summary="Get Customer Statistics", description="Get comprehensive customer statistics and analytics")
async def get_customer_statistics(
    db: Session = Depends(get_db)
):
    """Get customer statistics"""
    customer_service = CustomerService(db)
    statistics = customer_service.get_customer_statistics()
    return statistics

@router.get("/tags/{tags}", summary="Get Customers by Tags", description="Get customers by specific tags")
async def get_customers_by_tags(
    tags: str,
    db: Session = Depends(get_db)
):
    """Get customers by tags"""
    customer_service = CustomerService(db)
    tag_list = [tag.strip() for tag in tags.split(',')]
    customers = customer_service.get_customers_by_tags(tag_list)
    return {"customers": customers, "tags": tag_list}

@router.get("/location/search", summary="Get Customers by Location", description="Get customers by city, state, or country")
async def get_customers_by_location(
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state"),
    country: Optional[str] = Query(None, description="Filter by country"),
    db: Session = Depends(get_db)
):
    """Get customers by location"""
    customer_service = CustomerService(db)
    customers = customer_service.get_customers_by_location(city=city, state=state, country=country)
    return {"customers": customers, "filters": {"city": city, "state": state, "country": country}}

@router.get("/available/countries", summary="Get Available Countries", description="Get list of all countries where customers exist")
async def get_available_countries(
    db: Session = Depends(get_db)
):
    """Get available countries"""
    from app.models.customer import Customer
    from sqlalchemy import func
    
    countries = db.query(Customer.country, func.count(Customer.id)).filter(
        Customer.country.isnot(None)
    ).group_by(Customer.country).all()
    
    return {"countries": [{"country": country, "count": count} for country, count in countries]}

@router.get("/available/cities", summary="Get Available Cities", description="Get list of all cities where customers exist")
async def get_available_cities(
    country: Optional[str] = Query(None, description="Filter by country"),
    db: Session = Depends(get_db)
):
    """Get available cities"""
    from app.models.customer import Customer
    from sqlalchemy import func
    
    query = db.query(Customer.city, func.count(Customer.id)).filter(
        Customer.city.isnot(None)
    )
    
    if country:
        query = query.filter(Customer.country == country)
    
    cities = query.group_by(Customer.city).all()
    
    return {"cities": [{"city": city, "count": count} for city, count in cities]}

@router.get("/available/states", summary="Get Available States", description="Get list of all states where customers exist")
async def get_available_states(
    country: Optional[str] = Query(None, description="Filter by country"),
    db: Session = Depends(get_db)
):
    """Get available states"""
    from app.models.customer import Customer
    from sqlalchemy import func
    
    query = db.query(Customer.state, func.count(Customer.id)).filter(
        Customer.state.isnot(None)
    )
    
    if country:
        query = query.filter(Customer.country == country)
    
    states = query.group_by(Customer.state).all()
    
    return {"states": [{"state": state, "count": count} for state, count in states]}
