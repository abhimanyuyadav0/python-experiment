# Order API Documentation

This document describes the Order API endpoints for managing orders in the system. The Order API uses MongoDB as its database and provides comprehensive CRUD operations for order management.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Data Models](#data-models)
- [Examples](#examples)
- [Testing](#testing)

## Overview

The Order API is built with FastAPI and provides a RESTful interface for managing orders. It includes:

- **Order Management**: Create, read, update, and delete orders
- **Status Tracking**: Track order status through various stages
- **Customer Orders**: Retrieve orders for specific customers
- **Pagination**: Support for paginated results
- **Filtering**: Filter orders by customer ID and status
- **MongoDB Integration**: Uses MongoDB for data persistence

## Prerequisites

- Python 3.8+
- MongoDB running locally or accessible via network
- FastAPI application running

## Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **MongoDB Setup**
   - Install MongoDB locally or use MongoDB Atlas
   - Ensure MongoDB is running on the configured port (default: 27017)

3. **Environment Configuration**
   ```bash
   cp env.example .env
   # Edit .env with your MongoDB connection details
   ```

## Configuration

### Environment Variables

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=order_db
```

### MongoDB Connection

The API automatically connects to MongoDB on startup and manages connections through the `OrderService` class.

## API Endpoints

### Base URL
```
http://localhost:5001/api/v1/orders
```

### 1. Create Order

**POST** `/orders/`

Creates a new order with customer information and order items.

**Request Body:**
```json
{
  "customer_id": "cust_001",
  "customer_name": "John Doe",
  "customer_email": "john.doe@example.com",
  "customer_phone": "+1234567890",
  "shipping_address": "123 Main St, City, State 12345",
  "items": [
    {
      "product_id": "prod_001",
      "product_name": "Laptop",
      "quantity": 1,
      "unit_price": 999.99,
      "total_price": 999.99
    }
  ],
  "notes": "Please deliver during business hours"
}
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "customer_id": "cust_001",
  "customer_name": "John Doe",
  "customer_email": "john.doe@example.com",
  "customer_phone": "+1234567890",
  "shipping_address": "123 Main St, City, State 12345",
  "items": [...],
  "subtotal": 999.99,
  "tax": 100.0,
  "shipping_cost": 10.0,
  "total_amount": 1109.99,
  "status": "pending",
  "notes": "Please deliver during business hours",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

### 2. Get Order by ID

**GET** `/orders/{order_id}`

Retrieves a specific order by its ID.

**Response:** Order object (same as create response)

### 3. Get All Orders

**GET** `/orders/`

Retrieves a paginated list of orders with optional filtering.

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Number of records to return (default: 10, max: 100)
- `customer_id` (string, optional): Filter by customer ID
- `status` (string, optional): Filter by order status

**Response:**
```json
{
  "orders": [...],
  "total": 25,
  "page": 1,
  "size": 10
}
```

### 4. Update Order

**PUT** `/orders/{order_id}`

Updates an existing order with new information.

**Request Body:**
```json
{
  "status": "confirmed",
  "shipping_address": "456 New St, City, State 12345",
  "notes": "Updated delivery instructions"
}
```

**Response:** Updated order object

### 5. Delete Order

**DELETE** `/orders/{order_id}`

Deletes an order by its ID.

**Response:**
```json
{
  "message": "Order deleted successfully"
}
```

### 6. Get Customer Orders

**GET** `/orders/customer/{customer_id}`

Retrieves all orders for a specific customer.

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Number of records to return (default: 10, max: 100)

**Response:** Same as get all orders

### 7. Update Order Status

**PATCH** `/orders/{order_id}/status`

Updates the status of an order.

**Query Parameters:**
- `status` (string): New order status

**Response:** Updated order object

## Data Models

### Order Status Enum

```python
class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
```

### Order Item Schema

```python
class OrderItemSchema(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    total_price: float
```

### Order Schemas

- `OrderCreateSchema`: For creating new orders
- `OrderUpdateSchema`: For updating existing orders
- `OrderResponseSchema`: For API responses
- `OrderListResponseSchema`: For paginated order lists

## Business Logic

### Automatic Calculations

The API automatically calculates:
- **Subtotal**: Sum of all item total prices
- **Tax**: 10% of subtotal
- **Shipping Cost**: Fixed $10.00
- **Total Amount**: Subtotal + Tax + Shipping Cost

### Order Status Flow

1. **PENDING**: Order created, awaiting confirmation
2. **CONFIRMED**: Order confirmed by staff
3. **PROCESSING**: Order being prepared
4. **SHIPPED**: Order shipped to customer
5. **DELIVERED**: Order delivered successfully
6. **CANCELLED**: Order cancelled

## Examples

### Create a Simple Order

```bash
curl -X POST "http://localhost:5001/api/v1/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cust_001",
    "customer_name": "Jane Smith",
    "customer_email": "jane.smith@example.com",
    "shipping_address": "789 Oak Ave, City, State 12345",
    "items": [
      {
        "product_id": "prod_002",
        "product_name": "Mouse",
        "quantity": 1,
        "unit_price": 25.99,
        "total_price": 25.99
      }
    ]
  }'
```

### Update Order Status

```bash
curl -X PATCH "http://localhost:5001/api/v1/orders/507f1f77bcf86cd799439011/status?status=confirmed"
```

### Get Customer Orders

```bash
curl "http://localhost:5001/api/v1/orders/customer/cust_001?limit=5"
```

## Testing

### Run Test Script

```bash
python test_order_api.py
```

### Manual Testing

1. **Start the server:**
   ```bash
   python run.py
   ```

2. **Check MongoDB health:**
   ```bash
   curl http://localhost:5001/health/mongodb
   ```

3. **Access API documentation:**
   ```
   http://localhost:5001/docs
   ```

## Error Handling

The API provides comprehensive error handling:

- **400 Bad Request**: Invalid input data
- **404 Not Found**: Order not found
- **500 Internal Server Error**: Server-side errors

All errors include descriptive messages to help with debugging.

## Performance Considerations

- **Pagination**: Default limit of 10 records per page
- **Indexing**: MongoDB indexes on `customer_id` and `status` fields
- **Connection Pooling**: Efficient MongoDB connection management
- **Async Operations**: Non-blocking I/O operations

## Security

- Input validation using Pydantic schemas
- MongoDB injection protection through proper query construction
- Error message sanitization to prevent information leakage

## Monitoring

- Health check endpoints for MongoDB connectivity
- Comprehensive logging for debugging
- Performance metrics through FastAPI's built-in monitoring

## Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   - Check if MongoDB is running
   - Verify connection string in environment variables
   - Check network connectivity

2. **Order Creation Fails**
   - Validate request body against schema
   - Check MongoDB permissions
   - Verify database exists

3. **Performance Issues**
   - Check MongoDB indexes
   - Monitor connection pool usage
   - Review query patterns

### Debug Mode

Enable debug logging by setting the appropriate log level in your environment.

## Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the test script for usage examples
3. Check MongoDB logs for database-related issues
4. Verify environment configuration
