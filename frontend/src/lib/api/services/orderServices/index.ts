import axoisInstance from "../../axois";

// Order Types
export interface OrderItem {
  product_id: string;
  product_name: string;
  quantity: number;
  unit_price: number;
  subtotal: number;
}

export interface OrderCreateData {
  customer_id: string;
  customer_name: string;
  customer_email: string;
  customer_phone?: string;
  items: OrderItem[];
  shipping_address: {
    street: string;
    city: string;
    state: string;
    zip_code: string;
    country: string;
  };
  billing_address?: {
    street: string;
    city: string;
    state: string;
    zip_code: string;
    country: string;
  };
  payment_method: string;
  notes?: string;
}

export interface OrderUpdateData {
  customer_name?: string;
  customer_email?: string;
  customer_phone?: string;
  items?: OrderItem[];
  shipping_address?: {
    street: string;
    city: string;
    state: string;
    zip_code: string;
    country: string;
  };
  billing_address?: {
    street: string;
    city: string;
    state: string;
    zip_code: string;
    country: string;
  };
  payment_method?: string;
  notes?: string;
}

export interface Order {
  _id: string;
  order_id: string;
  customer_id: string;
  customer_name: string;
  customer_email: string;
  customer_phone?: string;
  items: OrderItem[];
  subtotal: number;
  tax_amount: number;
  total_amount: number;
  status: 'pending' | 'confirmed' | 'processing' | 'shipped' | 'delivered' | 'cancelled' | 'refunded';
  payment_status: 'pending' | 'paid' | 'failed' | 'refunded';
  shipping_address: {
    street: string;
    city: string;
    state: string;
    zip_code: string;
    country: string;
  };
  billing_address?: {
    street: string;
    city: string;
    state: string;
    zip_code: string;
    country: string;
  };
  payment_method: string;
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

export const updateOrderStatus = (orderId: string, status: string) => {
  return axoisInstance.patch(`/api/v1/orders/${orderId}/status`, { status });
};

export const deleteOrder = (orderId: string) => {
  return axoisInstance.delete(`/api/v1/orders/${orderId}`);
};
