# Multi-Tenant Application Backend

A FastAPI-based backend for a multi-tenant application with role-based access control (RBAC).

## Features

- ✅ **Authentication & Authorization**: JWT-based authentication with role-based access control
- ✅ **User Management**: CRUD operations for users with role management
- ✅ **Role-Based Access Control**: Three roles (admin, tenant, user) with different permissions
- ✅ **PostgreSQL Database**: Local PostgreSQL database with SQLAlchemy ORM
- ✅ **CORS Enabled**: Cross-origin requests allowed for frontend development
- ✅ **Token-based authentication with 5-minute expiration**
- ✅ **Automatic logout on token expiration**
- ✅ **Input validation and error handling**

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (local)
- **ORM**: SQLAlchemy
- **Authentication**: JWT (PyJWT)
- **Database Management**: pgAdmin (local)
- **Password Hashing**: SHA-256

## Prerequisites

1. **PostgreSQL**: Install PostgreSQL on your system
2. **pgAdmin**: Install pgAdmin for database management
3. **Python**: Python 3.8+ with pip

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pyrhon-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL Database**
   
   **Using pgAdmin:**
   - Open pgAdmin
   - Create a new database named `multitenant_app`
   - Create a user with appropriate permissions (or use default postgres user)

   **Using psql:**
   ```sql
   CREATE DATABASE multitenant_app;
   CREATE USER app_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE multitenant_app TO app_user;
   ```

5. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

6. **Initialize the database**
   ```bash
   python init_db.py
   ```

7. **Run the application**
   ```bash
   python -m uvicorn app.main:app --reload --port 5001
   ```

## API Endpoints

### Authentication

#### Login User
```http
POST /api/v1/users/authenticate
Content-Type: application/json

{
    "email": "admin@example.com",
    "password": "admin123"
}
```

**Response:**
```json
{
    "user": {
        "id": 1,
        "name": "Admin User",
        "email": "admin@example.com",
        "is_active": true,
        "role": "admin",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "expires_at": 1704067500
}
```

### User Management

#### Create User
```http
POST /api/v1/users/
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "role": "user",
    "is_active": true
}
```

#### Get All Users
```http
GET /api/v1/users/?skip=0&limit=10
```

#### Get User by ID
```http
GET /api/v1/users/{user_id}
```

#### Get Users by Role
```http
GET /api/v1/users/role/{role}?skip=0&limit=10
```

#### Update User Role
```http
PATCH /api/v1/users/{user_id}/role?role=admin
```

#### Delete User
```http
DELETE /api/v1/users/{user_id}
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    role VARCHAR NOT NULL DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Default Users

The initialization script creates these default users:

- **Admin**: `admin@example.com` / `admin123`
- **Tenant**: `tenant@example.com` / `tenant123`
- **User**: `user@example.com` / `user123`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:password@localhost:5432/multitenant_app` |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `DB_NAME` | Database name | `multitenant_app` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | `password` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-here` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `5` |

## CORS Configuration

The backend is configured to allow requests from all origins (`*`) to support frontend development and testing:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
```

**Note**: For production, you should restrict `allow_origins` to specific domains for security.

## Token Management

- **Expiration**: Tokens expire after 5 minutes
- **Auto-logout**: Users are automatically logged out when tokens expire
- **Countdown**: Frontend displays a countdown timer showing token expiration time
- **Refresh**: In a production environment, implement token refresh mechanism

### Using Tokens

Include the token in the Authorization header for authenticated requests:

```http
Authorization: Bearer your_token_here
```

## Role-Based Access Control

The system supports three user roles with different permissions:

### Role Hierarchy
- **Admin**: Full system access, can manage all users and roles
- **Tenant**: Can manage their own tenant's users and projects
- **User**: Basic access to assigned projects and tasks

### Role Permissions
- **Admin**: User management, role updates, system-wide access
- **Tenant**: Project management, user management within tenant
- **User**: Project access, task management, profile updates

## Development

### Running in Development Mode
```bash
python -m uvicorn app.main:app --reload --port 5001
```

### API Documentation
- **Swagger UI**: http://localhost:5001/docs
- **ReDoc**: http://localhost:5001/redoc

### Database Management with pgAdmin
1. Open pgAdmin
2. Connect to your PostgreSQL server
3. Navigate to the `multitenant_app` database
4. Use the Query Tool to run SQL commands
5. Monitor tables and data through the GUI

## Production Deployment

For production deployment:

1. **Security**: Change default passwords and secret keys
2. **Database**: Use a production PostgreSQL instance
3. **CORS**: Restrict origins to your frontend domain
4. **HTTPS**: Enable HTTPS for all communications
5. **Environment**: Use proper environment variables
6. **Monitoring**: Add logging and monitoring

## Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database `multitenant_app` exists
- Verify user permissions

### Import Errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Port Already in Use
- Change port in `.env` file
- Or kill the process using the port