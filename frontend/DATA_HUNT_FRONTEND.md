# Data Hunt Frontend Functionality

## Overview
The Data Hunt page has been enhanced with comprehensive functionality to create and view orders, products, and payments using the backend MongoDB APIs. The page now includes dummy data generation for easy testing and demonstration.

## Features

### 1. Orders Management
- **Create Order**: Click "Create Order" button to open a modal with a comprehensive form
- **View Orders**: Click "View Orders" button to see all orders in a modal
- **Generate Sample Data**: Click "Generate Sample Data" button to pre-fill the form with realistic dummy data
- **Order Form Fields**:
  - Customer information (ID, name, email, phone)
  - Shipping address (street, city, state, ZIP code, country)
  - Payment method selection
  - Order items (dynamic list with add/remove functionality)
  - Notes

### 2. Products Management
- **Create Product**: Click "Create Product" button to open a modal with product creation form
- **View Products**: Click "View Products" button to see all products in a modal
- **Generate Sample Data**: Click "Generate Sample Data" button to pre-fill the form with realistic dummy data
- **Product Form Fields**:
  - Basic info (name, description, SKU)
  - Category and brand
  - Price and stock quantity
  - Active status toggle
  - Advanced fields (weight, dimensions, variants, specifications, tags)

### 3. Payments Management
- **Create Payment**: Click "Create Payment" button to open a modal with payment creation form
- **View Payments**: Click "View Payments" button to see all payments in a modal
- **Generate Sample Data**: Click "Generate Sample Data" button to pre-fill the form with realistic dummy data
- **Payment Form Fields**:
  - Order and customer IDs
  - Amount and currency
  - Payment method and provider
  - Transaction type
  - Metadata and payment method details

### 4. Data Display
- Real-time data loading from backend APIs
- Status indicators with color coding
- Responsive grid layouts
- Loading states and error handling

### 5. Dummy Data Generation
- **Realistic Sample Data**: Each entity type generates appropriate sample data
- **Random IDs**: Generates unique customer IDs, order IDs, and SKUs
- **Complete Forms**: Pre-fills all required and optional fields
- **Testing Ready**: Perfect for testing API endpoints and form validation

## Technical Implementation

### Services Used
- **Order Services**: `@/lib/api/services/orderServices`
- **Product Services**: `@/lib/api/services/productServices`
- **Payment Services**: `@/lib/api/services/paymentServices`

### State Management
- React hooks for local state management
- Form state management for each entity type
- Loading states for API calls
- Error handling with toast notifications

### API Integration
- Uses existing axios instance with authentication
- Automatic data refresh after successful operations
- Error handling for failed API calls
- Promise.all for concurrent data loading

### Dummy Data Generation
- **Order Data**: Customer info, shipping address, order items with realistic products
- **Product Data**: Complete product with variants, specifications, and metadata
- **Payment Data**: Payment details with method information and metadata
- **Randomization**: Uses Math.random() for unique identifiers

## Usage Instructions

### Creating Data
1. Click the "Create [Entity]" button for the desired entity type
2. **Optional**: Click "Generate Sample Data" to pre-fill the form with realistic data
3. Modify the generated data as needed or fill out the form manually
4. Click "Create [Entity]" to submit
5. Success message will appear and data will be refreshed

### Viewing Data
1. Click the "View [Entities]" button for the desired entity type
2. Modal will display all existing data
3. Data is automatically loaded when the page loads
4. Real-time count is shown on each section

### Form Validation
- Required fields are marked with appropriate labels
- Numeric fields accept appropriate input types
- Dropdown selections for enumerated values
- Dynamic form updates for complex objects

### Dummy Data Features
- **Realistic Values**: Uses real-world examples (names, addresses, products)
- **Complete Coverage**: Fills all form fields including optional ones
- **Proper Formatting**: Generates valid data formats (emails, phone numbers, etc.)
- **Variety**: Different data for each generation to avoid repetition

## Dependencies
- React 19.1.0
- Next.js 15.4.5
- Tailwind CSS for styling
- React-toastify for notifications
- Lucide React for icons
- Custom Button and Modal components

## File Structure
```
frontend/src/app/(admin)/admin/data-hunt/
├── page.tsx (main component with dummy data generation)
└── ...

frontend/src/lib/api/services/
├── orderServices/index.ts
├── productServices/index.ts
└── paymentServices/index.ts
```

## Future Enhancements
- Edit functionality for existing entities
- Delete functionality with confirmation
- Advanced filtering and search
- Bulk operations
- Export functionality
- Real-time updates with WebSocket
- User management integration
- More diverse dummy data templates
- Customizable dummy data generation
