import axoisInstance from "../../axois";

// Order Types
export interface OrderItem {
  product_id: string;
  product_name: string;
  quantity: number;
  unit_price: number;
  total_price: number;  // Changed from subtotal to total_price to match backend
}

export interface OrderCreateData {
  customer_id: string;
  customer_name: string;
  customer_email: string;
  customer_phone?: string;
  items: OrderItem[];
  shipping_address: string;  // Changed from object to string to match backend
  notes?: string;
}

export interface OrderUpdateData {
  status?: 'pending' | 'confirmed' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  shipping_address?: string;  // Changed from object to string to match backend
  notes?: string;
}

export interface Order {
  id: string;  // Changed from _id to id to match backend
  customer_id: string;
  customer_name: string;
  customer_email: string;
  customer_phone?: string;
  items: OrderItem[];
  subtotal: number;
  tax: number;  // Changed from tax_amount to tax to match backend
  shipping_cost: number;  // Added to match backend
  total_amount: number;
  status: 'pending' | 'confirmed' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  shipping_address: string;  // Changed from object to string to match backend
  notes?: string;
  created_at: string;
  updated_at: string;
}

// Order API calls
export const createOrder = (data: OrderCreateData) => {
  return axoisInstance.post('/api/v1/orders/', data);
};

export const getOrderById = (orderId: string) => {
  return axoisInstance.get(`/api/v1/orders/${orderId}`);
};

export const getAllOrders = async () => {
  const response = await axoisInstance.get('/api/v1/orders/');
  console.log("orders response",response.data)
  return response.data
};

export const getOrdersByCustomer = (customerId: string) => {
  return axoisInstance.get(`/api/v1/orders/customer/${customerId}`);
};

export const updateOrder = (orderId: string, data: OrderUpdateData) => {
  return axoisInstance.put(`/api/v1/orders/${orderId}`, data);
};

export const updateOrderStatus = (orderId: string, status: 'pending' | 'confirmed' | 'processing' | 'shipped' | 'delivered' | 'cancelled') => {
  return axoisInstance.patch(`/api/v1/orders/${orderId}/status`, status);
};

export const deleteOrder = (orderId: string) => {
  return axoisInstance.delete(`/api/v1/orders/${orderId}`);
};
