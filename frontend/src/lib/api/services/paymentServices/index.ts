import axoisInstance from "../../axois";

// Payment Types
export interface PaymentMethodDetails {
  card_last4?: string;
  card_brand?: string;
  card_exp_month?: number;
  card_exp_year?: number;
  bank_last4?: string;
  bank_name?: string;
  account_type?: string;
}

export interface PaymentCreateData {
  order_id: string;
  customer_id: string;
  amount: number;
  currency: string;
  payment_method: string;
  payment_provider: string;
  transaction_type: 'purchase' | 'refund' | 'capture' | 'void';
  description?: string;
  metadata?: Record<string, any>;
  payment_method_details?: PaymentMethodDetails;
}

export interface PaymentUpdateData {
  amount?: number;
  currency?: string;
  payment_method?: string;
  payment_provider?: string;
  description?: string;
  metadata?: Record<string, any>;
  payment_method_details?: PaymentMethodDetails;
}

export interface Payment {
  _id: string;
  payment_id: string;
  order_id: string;
  customer_id: string;
  amount: number;
  currency: string;
  payment_method: string;
  payment_provider: string;
  transaction_type: 'purchase' | 'refund' | 'capture' | 'void';
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'cancelled' | 'refunded';
  description?: string;
  metadata?: Record<string, any>;
  payment_method_details?: PaymentMethodDetails;
  provider_transaction_id?: string;
  provider_response?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface RefundCreateData {
  payment_id: string;
  amount: number;
  reason: string;
  metadata?: Record<string, any>;
}

export interface Refund {
  _id: string;
  refund_id: string;
  payment_id: string;
  amount: number;
  reason: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  metadata?: Record<string, any>;
  provider_refund_id?: string;
  created_at: string;
  updated_at: string;
}

export interface PaymentMethodCreateData {
  customer_id: string;
  payment_type: 'card' | 'bank_account' | 'digital_wallet';
  payment_provider: string;
  is_default?: boolean;
  payment_method_details: PaymentMethodDetails;
  metadata?: Record<string, any>;
}

export interface PaymentMethod {
  _id: string;
  payment_method_id: string;
  customer_id: string;
  payment_type: 'card' | 'bank_account' | 'digital_wallet';
  payment_provider: string;
  is_default: boolean;
  is_active: boolean;
  payment_method_details: PaymentMethodDetails;
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface PaymentIntentCreateData {
  customer_id: string;
  amount: number;
  currency: string;
  payment_method_types: string[];
  description?: string;
  metadata?: Record<string, any>;
  capture_method?: 'automatic' | 'manual';
}

export interface PaymentIntent {
  _id: string;
  payment_intent_id: string;
  customer_id: string;
  amount: number;
  currency: string;
  payment_method_types: string[];
  status: 'requires_payment_method' | 'requires_confirmation' | 'requires_action' | 'processing' | 'requires_capture' | 'canceled' | 'succeeded';
  description?: string;
  metadata?: Record<string, any>;
  capture_method: 'automatic' | 'manual';
  created_at: string;
  updated_at: string;
}

export interface PaymentSearchParams {
  customer_id?: string;
  order_id?: string;
  status?: string;
  payment_method?: string;
  payment_provider?: string;
  min_amount?: number;
  max_amount?: number;
  start_date?: string;
  end_date?: string;
  sort_by?: 'created_at' | 'amount' | 'status';
  sort_order?: 'asc' | 'desc';
  page?: number;
  limit?: number;
}

// Payment API calls
export const createPayment = (data: PaymentCreateData) => {
  return axoisInstance.post('/api/v1/payments/', data);
};

export const getAllPayments = async (params?: {
  page?: number;
  limit?: number;
  customer_id?: string;
  order_id?: string;
  status?: string;
  payment_method?: string;
  payment_provider?: string;
}) => {
  const response = await axoisInstance.get('/api/v1/payments/', { params });
  console.log("payments response",response.data)
  return response.data
};

export const getPaymentById = (paymentId: string) => {
  return axoisInstance.get(`/api/v1/payments/${paymentId}`);
};

export const getPaymentsByOrderId = (orderId: string) => {
  return axoisInstance.get(`/api/v1/payments/order/${orderId}`);
};

export const getPaymentsByCustomerId = (customerId: string) => {
  return axoisInstance.get(`/api/v1/payments/customer/${customerId}`);
};

export const searchPayments = (searchParams: PaymentSearchParams) => {
  return axoisInstance.post('/api/v1/payments/search', searchParams);
};

export const updatePayment = (paymentId: string, data: PaymentUpdateData) => {
  return axoisInstance.put(`/api/v1/payments/${paymentId}`, data);
};

export const updatePaymentStatus = (paymentId: string, status: string) => {
  return axoisInstance.patch(`/api/v1/payments/${paymentId}/status`, { status });
};

export const processPayment = (paymentId: string) => {
  return axoisInstance.post(`/api/v1/payments/${paymentId}/process`);
};

export const deletePayment = (paymentId: string) => {
  return axoisInstance.delete(`/api/v1/payments/${paymentId}`);
};

// Refund API calls
export const createRefund = (data: RefundCreateData) => {
  return axoisInstance.post('/api/v1/payments/refunds/', data);
};

export const getRefundById = (refundId: string) => {
  return axoisInstance.get(`/api/v1/payments/refunds/${refundId}`);
};

export const getRefundsByPaymentId = (paymentId: string) => {
  return axoisInstance.get(`/api/v1/payments/refunds/payment/${paymentId}`);
};

// Payment Method API calls
export const createPaymentMethod = (data: PaymentMethodCreateData) => {
  return axoisInstance.post('/api/v1/payments/methods/', data);
};

export const getPaymentMethodById = (methodId: string) => {
  return axoisInstance.get(`/api/v1/payments/methods/${methodId}`);
};

export const getPaymentMethodsByCustomerId = (customerId: string) => {
  return axoisInstance.get(`/api/v1/payments/methods/customer/${customerId}`);
};

export const updatePaymentMethod = (methodId: string, data: Partial<PaymentMethodCreateData>) => {
  return axoisInstance.put(`/api/v1/payments/methods/${methodId}`, data);
};

export const deletePaymentMethod = (methodId: string) => {
  return axoisInstance.delete(`/api/v1/payments/methods/${methodId}`);
};

// Payment Intent API calls
export const createPaymentIntent = (data: PaymentIntentCreateData) => {
  return axoisInstance.post('/api/v1/payments/intents/', data);
};

export const getPaymentIntentById = (intentId: string) => {
  return axoisInstance.get(`/api/v1/payments/intents/${intentId}`);
};

export const updatePaymentIntentStatus = (intentId: string, status: string) => {
  return axoisInstance.patch(`/api/v1/payments/intents/${intentId}/status`, { status });
};

export const capturePayment = (paymentId: string, amount?: number) => {
  return axoisInstance.post(`/api/v1/payments/${paymentId}/capture`, { amount });
};

// Utility API calls
export const getPaymentStatistics = () => {
  return axoisInstance.get('/api/v1/payments/statistics/overview');
};

export const getAvailableCurrencies = () => {
  return axoisInstance.get('/api/v1/payments/currencies/available');
};

export const getAvailablePaymentMethods = () => {
  return axoisInstance.get('/api/v1/payments/methods/available');
};

export const getAvailablePaymentProviders = () => {
  return axoisInstance.get('/api/v1/payments/providers/available');
};

export const getAvailablePaymentStatuses = () => {
  return axoisInstance.get('/api/v1/payments/statuses/available');
};
