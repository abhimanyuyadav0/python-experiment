from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import math
import uuid

from app.models.customer import Customer
from app.schemas.customer import (
    CustomerCreateSchema, 
    CustomerUpdateSchema, 
    CustomerSearchSchema,
    CustomerBulkUpdateSchema
)

class CustomerService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_customer(self, customer_data: CustomerCreateSchema) -> Customer:
        """Create a new customer with auto-generated username and customer_id"""
        customer = Customer(**customer_data.dict())
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer
    
    def get_customer_by_id(self, customer_id: str) -> Optional[Customer]:
        """Get customer by customer_id"""
        return self.db.query(Customer).filter(Customer.customer_id == customer_id).first()
    
    def get_customer_by_username(self, username: str) -> Optional[Customer]:
        """Get customer by username"""
        return self.db.query(Customer).filter(Customer.username == username).first()
    
    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email"""
        return self.db.query(Customer).filter(Customer.email == email).first()
    
    def get_customer_by_db_id(self, id: int) -> Optional[Customer]:
        """Get customer by database ID"""
        return self.db.query(Customer).filter(Customer.id == id).first()
    
    def get_all_customers(
        self, 
        skip: int = 0, 
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> List[Customer]:
        """Get all customers with optional filtering"""
        query = self.db.query(Customer)
        
        if is_active is not None:
            query = query.filter(Customer.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    def search_customers(self, search_params: CustomerSearchSchema) -> Dict[str, Any]:
        """Search customers with advanced filtering and pagination"""
        query = self.db.query(Customer)
        
        # Apply filters
        if search_params.query:
            search_term = f"%{search_params.query}%"
            query = query.filter(
                or_(
                    Customer.first_name.ilike(search_term),
                    Customer.last_name.ilike(search_term),
                    Customer.email.ilike(search_term),
                    Customer.username.ilike(search_term)
                )
            )
        
        if search_params.first_name:
            query = query.filter(Customer.first_name.ilike(f"%{search_params.first_name}%"))
        
        if search_params.last_name:
            query = query.filter(Customer.last_name.ilike(f"%{search_params.last_name}%"))
        
        if search_params.email:
            query = query.filter(Customer.email.ilike(f"%{search_params.email}%"))
        
        if search_params.phone:
            query = query.filter(Customer.phone.ilike(f"%{search_params.phone}%"))
        
        if search_params.city:
            query = query.filter(Customer.city.ilike(f"%{search_params.city}%"))
        
        if search_params.state:
            query = query.filter(Customer.state.ilike(f"%{search_params.state}%"))
        
        if search_params.country:
            query = query.filter(Customer.country.ilike(f"%{search_params.country}%"))
        
        if search_params.is_active is not None:
            query = query.filter(Customer.is_active == search_params.is_active)
        
        if search_params.is_verified is not None:
            query = query.filter(Customer.is_verified == search_params.is_verified)
        
        if search_params.company_name:
            query = query.filter(Customer.company_name.ilike(f"%{search_params.company_name}%"))
        
        if search_params.tags:
            tag_list = [tag.strip() for tag in search_params.tags.split(',')]
            for tag in tag_list:
                query = query.filter(Customer.tags.ilike(f"%{tag}%"))
        
        if search_params.created_after:
            query = query.filter(Customer.created_at >= search_params.created_after)
        
        if search_params.created_before:
            query = query.filter(Customer.created_at <= search_params.created_before)
        
        # Apply sorting
        if search_params.sort_order.lower() == "asc":
            query = query.order_by(asc(getattr(Customer, search_params.sort_by)))
        else:
            query = query.order_by(desc(getattr(Customer, search_params.sort_by)))
        
        # Get total count for pagination
        total = query.count()
        
        # Apply pagination
        customers = query.offset((search_params.page - 1) * search_params.limit).limit(search_params.limit).all()
        
        # Calculate pagination info
        total_pages = math.ceil(total / search_params.limit)
        
        return {
            "customers": customers,
            "total": total,
            "page": search_params.page,
            "limit": search_params.limit,
            "total_pages": total_pages
        }
    
    def update_customer(self, customer_id: str, customer_data: CustomerUpdateSchema) -> Optional[Customer]:
        """Update customer information"""
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return None
        
        update_data = customer_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(customer, field, value)
        
        customer.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(customer)
        return customer
    
    def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer (soft delete by setting is_active to False)"""
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return False
        
        customer.is_active = False
        customer.updated_at = datetime.utcnow()
        self.db.commit()
        return True
    
    def hard_delete_customer(self, customer_id: str) -> bool:
        """Permanently delete a customer from the database"""
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return False
        
        self.db.delete(customer)
        self.db.commit()
        return True
    
    def bulk_update_customers(self, bulk_update_data: CustomerBulkUpdateSchema) -> Dict[str, Any]:
        """Update multiple customers at once"""
        updated_count = 0
        failed_updates = []
        
        for customer_id in bulk_update_data.customer_ids:
            try:
                customer = self.get_customer_by_id(customer_id)
                if customer:
                    update_data = bulk_update_data.updates.dict(exclude_unset=True)
                    for field, value in update_data.items():
                        setattr(customer, field, value)
                    customer.updated_at = datetime.utcnow()
                    updated_count += 1
                else:
                    failed_updates.append({"customer_id": customer_id, "reason": "Customer not found"})
            except Exception as e:
                failed_updates.append({"customer_id": customer_id, "reason": str(e)})
        
        self.db.commit()
        
        return {
            "updated_count": updated_count,
            "failed_updates": failed_updates,
            "total_processed": len(bulk_update_data.customer_ids)
        }
    
    def verify_customer_email(self, customer_id: str) -> bool:
        """Mark customer email as verified"""
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return False
        
        customer.email_verified = True
        customer.updated_at = datetime.utcnow()
        self.db.commit()
        return True
    
    def verify_customer_phone(self, customer_id: str) -> bool:
        """Mark customer phone as verified"""
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return False
        
        customer.phone_verified = True
        customer.updated_at = datetime.utcnow()
        self.db.commit()
        return True
    
    def update_last_login(self, customer_id: str) -> bool:
        """Update customer's last login timestamp"""
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return False
        
        customer.last_login_at = datetime.utcnow()
        self.db.commit()
        return True
    
    def get_customer_statistics(self) -> Dict[str, Any]:
        """Get comprehensive customer statistics"""
        now = datetime.utcnow()
        today = now.date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Basic counts
        total_customers = self.db.query(Customer).count()
        active_customers = self.db.query(Customer).filter(Customer.is_active == True).count()
        verified_customers = self.db.query(Customer).filter(Customer.is_verified == True).count()
        
        # New customers
        new_customers_today = self.db.query(Customer).filter(
            func.date(Customer.created_at) == today
        ).count()
        
        new_customers_this_week = self.db.query(Customer).filter(
            Customer.created_at >= week_ago
        ).count()
        
        new_customers_this_month = self.db.query(Customer).filter(
            Customer.created_at >= month_ago
        ).count()
        
        # Geographic distribution
        customers_by_country = self.db.query(
            Customer.country, func.count(Customer.id)
        ).filter(Customer.country.isnot(None)).group_by(Customer.country).all()
        
        customers_by_city = self.db.query(
            Customer.city, func.count(Customer.id)
        ).filter(Customer.city.isnot(None)).group_by(Customer.city).all()
        
        # Gender distribution
        gender_distribution = self.db.query(
            Customer.gender, func.count(Customer.id)
        ).filter(Customer.gender.isnot(None)).group_by(Customer.gender).all()
        
        # Calculate average age (if date_of_birth is available)
        age_query = self.db.query(
            func.avg(func.extract('year', func.age(Customer.date_of_birth)))
        ).filter(Customer.date_of_birth.isnot(None))
        
        average_age_result = age_query.scalar()
        average_customer_age = float(average_age_result) if average_age_result else None
        
        return {
            "total_customers": total_customers,
            "active_customers": active_customers,
            "verified_customers": verified_customers,
            "new_customers_today": new_customers_today,
            "new_customers_this_week": new_customers_this_week,
            "new_customers_this_month": new_customers_this_month,
            "customers_by_country": dict(customers_by_country),
            "customers_by_city": dict(customers_by_city),
            "average_customer_age": average_customer_age,
            "gender_distribution": dict(gender_distribution)
        }
    
    def get_customers_by_tags(self, tags: List[str]) -> List[Customer]:
        """Get customers by specific tags"""
        query = self.db.query(Customer)
        for tag in tags:
            query = query.filter(Customer.tags.ilike(f"%{tag}%"))
        return query.all()
    
    def get_customers_by_location(self, city: str = None, state: str = None, country: str = None) -> List[Customer]:
        """Get customers by location"""
        query = self.db.query(Customer)
        
        if city:
            query = query.filter(Customer.city.ilike(f"%{city}%"))
        if state:
            query = query.filter(Customer.state.ilike(f"%{state}%"))
        if country:
            query = query.filter(Customer.country.ilike(f"%{country}%"))
        
        return query.all()
    
    def generate_unique_username(self, first_name: str, last_name: str) -> str:
        """Generate a unique username for a customer"""
        base_username = f"{first_name.lower()}{last_name.lower()}"
        base_username = ''.join(c for c in base_username if c.isalnum())
        
        if len(base_username) > 20:
            base_username = base_username[:20]
        
        # Check if username exists and add suffix if needed
        username = base_username
        counter = 1
        while self.get_customer_by_username(username):
            suffix = str(counter).zfill(2)
            username = f"{base_username}{suffix}"
            counter += 1
            if counter > 99:  # Fallback to UUID if too many attempts
                username = f"{base_username}{uuid.uuid4().hex[:4]}"
                break
        
        return username
