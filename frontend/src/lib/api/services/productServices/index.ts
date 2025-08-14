import axoisInstance from "../../axois";

// Product Types
export interface ProductImage {
  url: string;
  alt_text?: string;
  is_primary?: boolean;
}

export interface ProductVariant {
  name: string;
  value: string;
  price_adjustment?: number;
  stock_quantity?: number;
}

export interface ProductSpecification {
  name: string;
  value: string;
  unit?: string;
}

export interface ProductCreateData {
  name: string;
  description: string;
  sku: string;
  category: string;
  brand?: string;
  price: number;
  sale_price?: number;
  cost_price?: number;
  stock_quantity: number;
  min_stock_level?: number;
  weight?: number;
  dimensions?: {
    length?: number;
    width?: number;
    height?: number;
  };
  images?: ProductImage[];
  variants?: ProductVariant[];
  specifications?: ProductSpecification[];
  tags?: string[];
  is_featured?: boolean;
  is_active?: boolean;
  meta_title?: string;
  meta_description?: string;
}

export interface ProductUpdateData {
  name?: string;
  description?: string;
  category?: string;
  brand?: string;
  price?: number;
  sale_price?: number;
  cost_price?: number;
  stock_quantity?: number;
  min_stock_level?: number;
  weight?: number;
  dimensions?: {
    length?: number;
    width?: number;
    height?: number;
  };
  images?: ProductImage[];
  variants?: ProductVariant[];
  specifications?: ProductSpecification[];
  tags?: string[];
  is_featured?: boolean;
  is_active?: boolean;
  meta_title?: string;
  meta_description?: string;
}

export interface Product {
  _id: string;
  product_id: string;
  name: string;
  description: string;
  sku: string;
  category: string;
  brand?: string;
  price: number;
  sale_price?: number;
  cost_price?: number;
  stock_quantity: number;
  min_stock_level?: number;
  weight?: number;
  dimensions?: {
    length?: number;
    width?: number;
    height?: number;
  };
  images?: ProductImage[];
  variants?: ProductVariant[];
  specifications?: ProductSpecification[];
  tags?: string[];
  is_featured: boolean;
  is_active: boolean;
  meta_title?: string;
  meta_description?: string;
  created_at: string;
  updated_at: string;
}

export interface ProductSearchParams {
  query?: string;
  category?: string;
  brand?: string;
  min_price?: number;
  max_price?: number;
  in_stock?: boolean;
  is_featured?: boolean;
  tags?: string[];
  sort_by?: 'name' | 'price' | 'created_at' | 'updated_at';
  sort_order?: 'asc' | 'desc';
  page?: number;
  limit?: number;
}

// Product API calls
export const createProduct = (data: ProductCreateData) => {
  return axoisInstance.post('/api/v1/products/', data);
};

export const getProductById = (productId: string) => {
  return axoisInstance.get(`/api/v1/products/${productId}`);
};

export const getProductBySku = (sku: string) => {
  return axoisInstance.get(`/api/v1/products/sku/${sku}`);
};

export const getAllProducts = async (params?: {
  page?: number;
  limit?: number;
  category?: string;
  brand?: string;
  is_featured?: boolean;
  is_active?: boolean;
}) => {
  const response = await axoisInstance.get('/api/v1/products/', { params });
  console.log("products response",response.data)
  return response.data
};

export const searchProducts = (searchParams: ProductSearchParams) => {
  return axoisInstance.post('/api/v1/products/search', searchParams);
};

export const updateProduct = (productId: string, data: ProductUpdateData) => {
  return axoisInstance.put(`/api/v1/products/${productId}`, data);
};

export const deleteProduct = (productId: string) => {
  return axoisInstance.delete(`/api/v1/products/${productId}`);
};

export const bulkUpdateProducts = (updates: Array<{ product_id: string; updates: Partial<ProductUpdateData> }>) => {
  return axoisInstance.post('/api/v1/products/bulk-update', { updates });
};

export const updateInventory = (productId: string, quantity: number, operation: 'add' | 'subtract' | 'set') => {
  return axoisInstance.post('/api/v1/products/inventory/update', {
    product_id: productId,
    quantity,
    operation
  });
};

export const getFeaturedProducts = () => {
  return axoisInstance.get('/api/v1/products/featured/');
};

export const getProductsByCategory = (category: string) => {
  return axoisInstance.get(`/api/v1/products/category/${category}`);
};

export const getProductStatistics = () => {
  return axoisInstance.get('/api/v1/products/statistics/overview');
};

export const getAvailableCategories = () => {
  return axoisInstance.get('/api/v1/products/categories/available');
};

export const getAvailableBrands = () => {
  return axoisInstance.get('/api/v1/products/brands/available');
};

export const getAvailableTags = () => {
  return axoisInstance.get('/api/v1/products/tags/available');
};

export const updateProductStatus = (productId: string, is_active: boolean) => {
  return axoisInstance.patch(`/api/v1/products/${productId}/status`, { is_active });
};

export const toggleProductFeatured = (productId: string) => {
  return axoisInstance.patch(`/api/v1/products/${productId}/feature`);
};
