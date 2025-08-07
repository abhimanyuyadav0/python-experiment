# Multi-Tenant Frontend Application

A modern Next.js application with authentication and multi-tenant support using React Context API.

## Features

- ✅ User authentication (login/signup)
- ✅ Protected routes
- ✅ Dashboard with statistics
- ✅ Tenant portal with project management
- ✅ Responsive design with Tailwind CSS
- ✅ React Context for state management

## Setup

### Prerequisites

- Node.js 18+ 
- Backend API running on port 5001

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create a `.env.local` file in the root directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:5001
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Project Structure

```
src/
├── app/
│   ├── (dashboard)/          # Dashboard layout and pages
│   │   ├── layout.tsx        # Dashboard layout with navigation
│   │   └── dashboard/
│   │       └── page.tsx      # Dashboard overview page
│   ├── (tenant)/             # Tenant layout and pages
│   │   ├── layout.tsx        # Tenant layout with navigation
│   │   └── tenant/
│   │       └── page.tsx      # Tenant overview page
│   ├── auth/                 # Authentication pages
│   │   ├── login/
│   │   │   └── page.tsx      # Login page
│   │   └── signup/
│   │       └── page.tsx      # Signup page
│   ├── layout.tsx            # Root layout with AuthProvider
│   └── page.tsx              # Home page with redirects
├── components/
│   └── ProtectedRoute.tsx    # Route protection component
├── contexts/
│   └── AuthContext.tsx       # Authentication context
└── lib/
    └── api/                  # API configuration and services
        ├── axois.ts          # Axios instance with interceptors
        └── services/
            └── userServices/
                └── index.ts  # User API services
```

## Authentication Flow

1. **Login**: Users can log in with email and password
2. **Signup**: New users can create accounts
3. **Protected Routes**: Unauthenticated users are redirected to login
4. **Context Management**: User state is managed with React Context
5. **Token Management**: JWT tokens are stored in localStorage

## Pages

### Dashboard (`/dashboard`)
- Overview statistics
- Recent activity feed
- User information display

### Tenant Portal (`/tenant`)
- Tenant-specific statistics
- Project management
- Quick actions for tenant operations

### Authentication
- **Login** (`/auth/login`): User login form
- **Signup** (`/auth/signup`): User registration form

## API Integration

The frontend integrates with the FastAPI backend running on port 5001. The API endpoints include:

- `POST /api/v1/users/` - Create new user (signup)
- `GET /api/v1/users/authenticate` - User authentication (login)
- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

### State Management

The application uses React Context API for state management:

- **AuthContext**: Manages user authentication state
- **ProtectedRoute**: Handles route protection
- **Local Storage**: Stores authentication tokens

## Styling

The application uses Tailwind CSS for styling with a modern, responsive design. The color scheme includes:

- **Dashboard**: Indigo theme
- **Tenant Portal**: Green theme
- **Authentication**: Clean, minimal design

## Security Features

- Protected routes for authenticated users
- Token-based authentication
- Automatic token refresh handling
- Secure API communication
- Input validation and error handling
