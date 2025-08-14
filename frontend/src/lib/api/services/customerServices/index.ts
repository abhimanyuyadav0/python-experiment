import axoisInstance from "../../axois";


// Customer data interfaces
export interface Customer {
  id: number;
  customer_id: string;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  date_of_birth?: string;
  gender?: "male" | "female" | "other" | "prefer_not_to_say";
  company_name?: string;
  tax_id?: string;
  is_active: boolean;
  is_verified: boolean;
  email_verified: boolean;
  phone_verified: boolean;
  marketing_emails: boolean;
  marketing_sms: boolean;
  notes?: string;
  tags?: string;
  created_at: string;
  updated_at: string;
  last_login_at?: string;
}

export interface CustomerCreateData {
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  date_of_birth?: string;
  gender?: "male" | "female" | "other" | "prefer_not_to_say";
  company_name?: string;
  tax_id?: string;
  marketing_emails?: boolean;
  marketing_sms?: boolean;
  notes?: string;
  tags?: string;
}

export interface CustomerUpdateData extends Partial<CustomerCreateData> {
  is_active?: boolean;
  is_verified?: boolean;
  email_verified?: boolean;
  phone_verified?: boolean;
}

export interface CustomerSearchParams {
  search?: string;
  is_active?: boolean;
  city?: string;
  country?: string;
  tags?: string;
  created_after?: string;
  created_before?: string;
  limit?: number;
  offset?: number;
}

export interface CustomerListResponse {
  data: Customer[];
  total: number;
  limit: number;
  offset: number;
}

export interface CustomerStatistics {
  total_customers: number;
  active_customers: number;
  verified_customers: number;
  new_customers_this_month: number;
  top_cities: Array<{ city: string; count: number }>;
  top_countries: Array<{ country: string; count: number }>;
}

// Customer API functions
export const createCustomer = async (customerData: CustomerCreateData) => {
  try {
    const response = await axoisInstance.post(`/api/v1/customers/`, customerData);
    return response.data;
  } catch (error) {
    console.error("Error creating customer:", error);
    throw error;
  }
};

export const getCustomerById = async (customerId: string) => {
  try {
    const response = await axoisInstance.get(`/api/v1/customers/${customerId}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching customer:", error);
    throw error;
  }
};

export const getCustomerByUsername = async (username: string) => {
  try {
    const response = await axoisInstance.get(`/api/v1/customers/username/${username}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching customer by username:", error);
    throw error;
  }
};

export const getCustomerByEmail = async (email: string) => {
  try {
    const response = await axoisInstance.get(`/api/v1/customers/email/${email}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching customer by email:", error);
    throw error;
  }
};

export const getAllCustomers = async (params?: CustomerSearchParams) => {
  try {
    const response = await axoisInstance.get(`/api/v1/customers/`, { params });
    console.log("customers response",response.data)
    return response.data;
  } catch (error) {
    console.error("Error fetching customers:", error);
    throw error;
  }
};

export const searchCustomers = async (searchParams: CustomerSearchParams) => {
  try {
    const response = await axoisInstance.post(`/api/v1/customers/search`, searchParams);
    return response.data;
  } catch (error) {
    console.error("Error searching customers:", error);
    throw error;
  }
};

export const updateCustomer = async (customerId: string, updateData: CustomerUpdateData) => {
  try {
    const response = await axoisInstance.put(`/api/v1/customers/${customerId}`, updateData);
    return response.data;
  } catch (error) {
    console.error("Error updating customer:", error);
    throw error;
  }
};

export const deleteCustomer = async (customerId: string) => {
  try {
    const response = await axoisInstance.delete(`/api/v1/customers/${customerId}`);
    return response.data;
  } catch (error) {
    console.error("Error deleting customer:", error);
    throw error;
  }
};

export const hardDeleteCustomer = async (customerId: string) => {
  try {
    const response = await axoisInstance.delete(`/api/v1/customers/${customerId}/hard`);
    return response.data;
  } catch (error) {
    console.error("Error hard deleting customer:", error);
    throw error;
  }
};

export const bulkUpdateCustomers = async (customerIds: string[], updateData: CustomerUpdateData) => {
  try {
    const response = await axoisInstance.post(`/api/v1/customers/bulk-update`, {
      customer_ids: customerIds,
      update_data: updateData
    });
    return response.data;
  } catch (error) {
    console.error("Error bulk updating customers:", error);
    throw error;
  }
};

export const verifyCustomerEmail = async (customerId: string) => {
  try {
    const response = await axoisInstance.patch(`/api/v1/customers/${customerId}/verify-email`);
    return response.data;
  } catch (error) {
    console.error("Error verifying customer email:", error);
    throw error;
  }
};

export const verifyCustomerPhone = async (customerId: string) => {
  try {
    const response = await axoisInstance.patch(`/api/v1/customers/${customerId}/verify-phone`);
    return response.data;
  } catch (error) {
    console.error("Error verifying customer phone:", error);
    throw error;
  }
};

export const updateCustomerLastLogin = async (customerId: string) => {
  try {
    const response = await axoisInstance.patch(`/api/v1/customers/${customerId}/last-login`);
    return response.data;
  } catch (error) {
    console.error("Error updating customer last login:", error);
    throw error;
  }
};

export const getCustomerStatistics = async () => {
  try {
    const response = await axoisInstance.get(`/api/v1/customers/statistics/overview`);
    return response.data;
  } catch (error) {
    console.error("Error fetching customer statistics:", error);
    throw error;
  }
};

export const getCustomersByTags = async (tags: string) => {
  try {
    const response = await axoisInstance.get(`/api/v1/customers/tags/${tags}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching customers by tags:", error);
    throw error;
  }
};

export const searchCustomersByLocation = async (city?: string, state?: string, country?: string) => {
  try {
    const params = new URLSearchParams();
    if (city) params.append("city", city);
    if (state) params.append("state", state);
    if (country) params.append("country", country);
    
    const response = await axoisInstance.get(`/api/v1/customers/location/search?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error("Error searching customers by location:", error);
    throw error;
  }
};

export const getAvailableCountries = async () => {
  try {
    const response = await axoisInstance.get(`/api/v1/customers/available/countries`);
    return response.data;
  } catch (error) {
    console.error("Error fetching available countries:", error);
    throw error;
  }
};

export const getAvailableCities = async (country?: string) => {
  try {
    const params = country ? { country } : {};
    const response = await axoisInstance.get(`/api/v1/customers/available/cities`, { params });
    return response.data;
  } catch (error) {
    console.error("Error fetching available cities:", error);
    throw error;
  }
};

export const getAvailableStates = async (country?: string) => {
  try {
    const params = country ? { country } : {};
      const response = await axoisInstance.get(`/api/v1/customers/available/states`, { params });
    return response.data;
  } catch (error) {
    console.error("Error fetching available states:", error);
    throw error;
  }
};
