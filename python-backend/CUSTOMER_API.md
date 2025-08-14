# Customer API Documentation

## Overview
The Customer API provides comprehensive customer management functionality using PostgreSQL as the database. It includes auto-generated unique usernames, customer registration, search, updates, and analytics.

## Features

### 🔑 **Auto-Generated Usernames**
- **Unique Username Generation**: Automatically creates unique usernames based on first and last names
- **Collision Handling**: Uses intelligent suffix generation to ensure uniqueness
- **Format**: `{firstname}{lastname}{suffix}` (e.g., `johndoe1234`)

### 🆔 **Auto-Generated Customer IDs**
- **Unique Customer ID**: Automatically generates `CUST_` prefixed unique identifiers
- **UUID Based**: Uses UUID for guaranteed uniqueness
- **Format**: `CUST_{8-character-hex}` (e.g., `CUST_A1B2C3D4`)

### 📊 **Comprehensive Customer Data**
- **Personal Information**: Name, email, phone, date of birth, gender
- **Address Management**: Complete address fields with validation
- **Company Details**: Company name, tax ID
- **Marketing Preferences**: Email and SMS opt-in settings
- **Tags and Notes**: Flexible categorization and notes system

## API Endpoints

### 1. Customer Management

#### Create Customer
```http
POST /api/v1/customers/
```
**Description**: Create a new customer with auto-generated username and customer_id

**Request Body**:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1-555-0123",
  "address_line1": "123 Main Street",
  "city": "New York",
  "state": "NY",
  "postal_code": "10001",
  "country": "USA",
  "date_of_birth": "1990-01-15T00:00:00",
  "gender": "male",
  "company_name": "Tech Corp",
  "marketing_emails": true,
  "marketing_sms": false,
  "notes": "Premium customer",
  "tags": "premium,tech,new-york"
}
```

**Response**:
```json
{
  "id": 1,
  "customer_id": "CUST_A1B2C3D4",
  "username": "johndoe1234",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1-555-0123",
  "address_line1": "123 Main Street",
  "city": "New York",
  "state": "NY",
  "postal_code": "10001",
  "country": "USA",
  "date_of_birth": "1990-01-15T00:00:00",
  "gender": "male",
  "company_name": "Tech Corp",
  "is_active": true,
  "is_verified": false,
  "email_verified": false,
  "phone_verified": false,
  "marketing_emails": true,
  "marketing_sms": false,
  "notes": "Premium customer",
  "tags": "premium,tech,new-york",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "last_login_at": null,
  "full_name": "John Doe",
  "full_address": "123 Main Street, New York, NY, 10001, USA"
}
```

#### Get Customer by ID
```http
GET /api/v1/customers/{customer_id}
```

#### Get Customer by Username
```http
GET /api/v1/customers/username/{username}
```

#### Get Customer by Email
```http
GET /api/v1/customers/email/{email}
```

#### Get All Customers
```http
GET /api/v1/customers/?skip=0&limit=100&is_active=true
```

**Query Parameters**:
- `skip`: Number of records to skip (pagination)
- `limit`: Number of records to return (max 1000)
- `is_active`: Filter by active status

### 2. Customer Search

#### Advanced Search
```http
POST /api/v1/customers/search
```

**Request Body**:
```json
{
  "query": "john",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "city": "New York",
  "country": "USA",
  "is_active": true,
  "is_verified": false,
  "company_name": "Tech Corp",
  "tags": "premium,tech",
  "created_after": "2024-01-01T00:00:00Z",
  "created_before": "2024-12-31T23:59:59Z",
  "sort_by": "created_at",
  "sort_order": "desc",
  "page": 1,
  "limit": 10
}
```

**Response**:
```json
{
  "customers": [...],
  "total": 150,
  "page": 1,
  "limit": 10,
  "total_pages": 15
}
```

### 3. Customer Updates

#### Update Customer
```http
PUT /api/v1/customers/{customer_id}
```

**Request Body**: Same as create, but all fields are optional

#### Bulk Update Customers
```http
POST /api/v1/customers/bulk-update
```

**Request Body**:
```json
{
  "customer_ids": ["CUST_A1B2C3D4", "CUST_B2C3D4E5"],
  "updates": {
    "marketing_emails": false,
    "notes": "Bulk updated customer",
    "tags": "bulk-updated"
  }
}
```

### 4. Customer Verification

#### Verify Email
```http
PATCH /api/v1/customers/{customer_id}/verify-email
```

#### Verify Phone
```http
PATCH /api/v1/customers/{customer_id}/verify-phone
```

#### Update Last Login
```http
PATCH /api/v1/customers/{customer_id}/last-login
```

### 5. Customer Analytics

#### Get Statistics
```http
GET /api/v1/customers/statistics/overview
```

**Response**:
```json
{
  "total_customers": 1250,
  "active_customers": 1180,
  "verified_customers": 890,
  "new_customers_today": 15,
  "new_customers_this_week": 89,
  "new_customers_this_month": 234,
  "customers_by_country": {
    "USA": 850,
    "Canada": 120,
    "UK": 95
  },
  "customers_by_city": {
    "New York": 125,
    "Los Angeles": 98,
    "Chicago": 87
  },
  "average_customer_age": 32.5,
  "gender_distribution": {
    "male": 620,
    "female": 580,
    "other": 50
  }
}
```

### 6. Location-Based Queries

#### Get Customers by Tags
```http
GET /api/v1/customers/tags/{tags}
```
**Example**: `/api/v1/customers/tags/premium,tech`

#### Get Customers by Location
```http
GET /api/v1/customers/location/search?city=New York&country=USA
```

#### Get Available Locations
```http
GET /api/v1/customers/available/countries
GET /api/v1/customers/available/cities?country=USA
GET /api/v1/customers/available/states?country=USA
```

### 7. Customer Deletion

#### Soft Delete
```http
DELETE /api/v1/customers/{customer_id}
```
Sets `is_active` to `false`

#### Hard Delete
```http
DELETE /api/v1/customers/{customer_id}/hard
```
Permanently removes customer from database

## Data Models

### Customer Model
```python
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
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String(20), nullable=True)
    company_name = Column(String(255), nullable=True)
    tax_id = Column(String(50), nullable=True)
    
    # Status and preferences
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    phone_verified = Column(Boolean, default=False, nullable=False)
    marketing_emails = Column(Boolean, default=True, nullable=False)
    marketing_sms = Column(Boolean, default=False, nullable=False)
    
    # Notes and metadata
    notes = Column(Text, nullable=True)
    tags = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True), nullable=True)
```

### Schema Classes
- **CustomerCreateSchema**: For creating new customers
- **CustomerUpdateSchema**: For updating existing customers
- **CustomerResponseSchema**: For API responses
- **CustomerSearchSchema**: For advanced search queries
- **CustomerBulkUpdateSchema**: For bulk operations
- **CustomerStatisticsSchema**: For analytics data

## Business Logic

### Username Generation Algorithm
1. **Base Username**: Combine first and last names (lowercase, alphanumeric only)
2. **Length Check**: Truncate to 20 characters if too long
3. **Uniqueness Check**: Add numeric suffix if username exists
4. **Fallback**: Use UUID suffix if too many attempts

### Customer ID Generation
1. **Prefix**: Always starts with "CUST_"
2. **Unique Part**: 8-character hexadecimal string from UUID
3. **Format**: `CUST_{8-char-hex}`

### Email Uniqueness
- Email addresses must be unique across all customers
- Validation occurs during creation and updates
- Prevents duplicate customer accounts

## Error Handling

### HTTP Status Codes
- **200**: Success
- **201**: Created
- **400**: Bad Request (validation errors, duplicate email)
- **404**: Not Found (customer doesn't exist)
- **422**: Validation Error (invalid data format)
- **500**: Internal Server Error

### Error Response Format
```json
{
  "detail": "Customer with this email already exists"
}
```

## Performance Features

### Database Indexes
- **Primary Key**: `id`
- **Unique Indexes**: `customer_id`, `username`, `email`
- **Search Indexes**: `phone`, `city`, `country`, `is_active`, `created_at`
- **Composite Indexes**: For location-based queries

### Query Optimization
- **Pagination**: Efficient handling of large datasets
- **Filtering**: Database-level filtering for better performance
- **Sorting**: Optimized sorting with proper indexes
- **Search**: Full-text search capabilities

## Security Features

### Data Validation
- **Input Sanitization**: All inputs are validated and sanitized
- **Email Validation**: Proper email format validation
- **Phone Validation**: Phone number format validation
- **SQL Injection Prevention**: Parameterized queries

### Access Control
- **Authentication**: JWT-based authentication (when implemented)
- **Authorization**: Role-based access control (when implemented)
- **Rate Limiting**: API rate limiting (when implemented)

## Testing

### Test Script
Run the comprehensive test script:
```bash
python test_customer_api.py
```

### Test Coverage
- ✅ Customer Creation
- ✅ Customer Retrieval
- ✅ Customer Search
- ✅ Customer Updates
- ✅ Customer Verification
- ✅ Customer Statistics
- ✅ Customer Deletion
- ✅ Bulk Operations
- ✅ Location Queries
- ✅ Tag-based Queries

## Usage Examples

### Python Client Example
```python
import requests

# Create customer
customer_data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0123"
}

response = requests.post("http://localhost:8000/api/v1/customers/", json=customer_data)
customer = response.json()

# Get customer by ID
customer_id = customer["customer_id"]
response = requests.get(f"http://localhost:8000/api/v1/customers/{customer_id}")
customer = response.json()

# Search customers
search_params = {
    "query": "john",
    "city": "New York",
    "page": 1,
    "limit": 10
}

response = requests.post("http://localhost:8000/api/v1/customers/search", json=search_params)
results = response.json()
```

### cURL Examples
```bash
# Create customer
curl -X POST "http://localhost:8000/api/v1/customers/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  }'

# Get customer by ID
curl "http://localhost:8000/api/v1/customers/CUST_A1B2C3D4"

# Search customers
curl -X POST "http://localhost:8000/api/v1/customers/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "john", "page": 1, "limit": 10}'
```

## Future Enhancements

### Planned Features
- **Customer Authentication**: Login/logout functionality
- **Password Management**: Secure password handling
- **Profile Pictures**: Avatar and image management
- **Social Login**: OAuth integration
- **Two-Factor Authentication**: Enhanced security
- **Customer Groups**: Organization and segmentation
- **Activity Tracking**: Customer behavior analytics
- **Integration APIs**: Third-party service connections

### Performance Improvements
- **Caching**: Redis-based caching for frequently accessed data
- **Async Processing**: Background job processing for bulk operations
- **Database Sharding**: Horizontal scaling for large datasets
- **CDN Integration**: Content delivery for customer assets

## Troubleshooting

### Common Issues

#### Username Collision
- **Problem**: Username already exists
- **Solution**: System automatically adds suffix to ensure uniqueness
- **Prevention**: Use UUID fallback for extreme cases

#### Email Duplication
- **Problem**: Email already registered
- **Solution**: Check existing customers before creation
- **Prevention**: Implement email verification workflow

#### Database Connection
- **Problem**: PostgreSQL connection issues
- **Solution**: Check database configuration and connectivity
- **Prevention**: Implement connection pooling and retry logic

### Debug Mode
Enable debug logging in the application configuration for detailed error information.

## Support

For technical support or questions about the Customer API:
- **Documentation**: This file and inline code comments
- **Test Scripts**: Use `test_customer_api.py` for validation
- **API Explorer**: Access `/docs` endpoint for interactive API documentation
- **Health Check**: Use `/health` endpoint for system status
