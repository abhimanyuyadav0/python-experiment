from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from decimal import Decimal

class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    BOOKS = "books"
    HOME_GARDEN = "home_garden"
    SPORTS = "sports"
    BEAUTY = "beauty"
    AUTOMOTIVE = "automotive"
    TOYS = "toys"
    FOOD_BEVERAGE = "food_beverage"
    HEALTH = "health"
    OTHER = "other"

class ProductStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"
    OUT_OF_STOCK = "out_of_stock"

class ProductImageSchema(BaseModel):
    url: str = Field(..., description="Image URL")
    alt_text: Optional[str] = Field(None, description="Alternative text for accessibility")
    is_primary: bool = Field(False, description="Whether this is the primary image")

class ProductVariantSchema(BaseModel):
    name: str = Field(..., description="Variant name (e.g., 'Color', 'Size')")
    value: str = Field(..., description="Variant value (e.g., 'Red', 'Large')")
    price_adjustment: float = Field(0.0, description="Price adjustment for this variant")
    stock_quantity: int = Field(0, ge=0, description="Stock quantity for this variant")

class ProductSpecificationSchema(BaseModel):
    key: str = Field(..., description="Specification key")
    value: str = Field(..., description="Specification value")
    unit: Optional[str] = Field(None, description="Unit of measurement")

class ProductCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    description: str = Field(..., min_length=10, max_length=2000, description="Product description")
    category: ProductCategory = Field(..., description="Product category")
    brand: Optional[str] = Field(None, max_length=100, description="Product brand")
    sku: str = Field(..., min_length=1, max_length=50, description="Stock Keeping Unit")
    base_price: float = Field(..., gt=0, description="Base price of the product")
    compare_price: Optional[float] = Field(None, gt=0, description="Compare at price (original price)")
    cost_price: Optional[float] = Field(None, gt=0, description="Cost price for profit calculation")
    weight: Optional[float] = Field(None, ge=0, description="Product weight in kg")
    dimensions: Optional[Dict[str, float]] = Field(None, description="Product dimensions (length, width, height)")
    tags: List[str] = Field(default_factory=list, description="Product tags for search")
    images: List[ProductImageSchema] = Field(default_factory=list, description="Product images")
    variants: List[ProductVariantSchema] = Field(default_factory=list, description="Product variants")
    specifications: List[ProductSpecificationSchema] = Field(default_factory=list, description="Product specifications")
    meta_title: Optional[str] = Field(None, max_length=60, description="SEO meta title")
    meta_description: Optional[str] = Field(None, max_length=160, description="SEO meta description")
    is_featured: bool = Field(False, description="Whether product is featured")
    is_taxable: bool = Field(True, description="Whether product is taxable")
    created_by: str = Field(..., description="Product creator")
class ProductUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=10, max_length=2000)
    category: Optional[ProductCategory] = None
    brand: Optional[str] = Field(None, max_length=100)
    base_price: Optional[float] = Field(None, gt=0)
    compare_price: Optional[float] = Field(None, gt=0)
    cost_price: Optional[float] = Field(None, gt=0)
    weight: Optional[float] = Field(None, ge=0)
    dimensions: Optional[Dict[str, float]] = None
    tags: Optional[List[str]] = None
    images: Optional[List[ProductImageSchema]] = None
    variants: Optional[List[ProductVariantSchema]] = None
    specifications: Optional[List[ProductSpecificationSchema]] = None
    meta_title: Optional[str] = Field(None, max_length=60)
    meta_description: Optional[str] = Field(None, max_length=160)
    is_featured: Optional[bool] = None
    is_taxable: Optional[bool] = None
    status: Optional[ProductStatus] = None
    created_by: Optional[str] = None
class ProductResponseSchema(BaseModel):
    id: str = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")
    description: str = Field(..., description="Product description")
    category: ProductCategory = Field(..., description="Product category")
    brand: Optional[str] = Field(None, description="Product brand")
    sku: str = Field(..., description="Stock Keeping Unit")
    base_price: float = Field(..., description="Base price of the product")
    compare_price: Optional[float] = Field(None, description="Compare at price")
    cost_price: Optional[float] = Field(None, description="Cost price")
    weight: Optional[float] = Field(None, description="Product weight in kg")
    dimensions: Optional[Dict[str, float]] = Field(None, description="Product dimensions")
    tags: List[str] = Field(..., description="Product tags")
    images: List[ProductImageSchema] = Field(..., description="Product images")
    variants: List[ProductVariantSchema] = Field(..., description="Product variants")
    specifications: List[ProductSpecificationSchema] = Field(..., description="Product specifications")
    meta_title: Optional[str] = Field(None, description="SEO meta title")
    meta_description: Optional[str] = Field(None, description="SEO meta description")
    is_featured: bool = Field(..., description="Whether product is featured")
    is_taxable: bool = Field(..., description="Whether product is taxable")
    status: ProductStatus = Field(..., description="Product status")
    total_stock: int = Field(..., description="Total stock across all variants")
    average_rating: Optional[float] = Field(None, ge=0, le=5, description="Average product rating")
    review_count: int = Field(0, description="Number of reviews")
    created_by: str = Field(..., description="Product creator")
    created_at: datetime = Field(..., description="Product creation timestamp")
    updated_at: datetime = Field(..., description="Product last update timestamp")

class ProductListResponseSchema(BaseModel):
    products: List[ProductResponseSchema] = Field(..., description="List of products")
    total: int = Field(..., description="Total number of products")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    categories: List[str] = Field(..., description="Available categories in results")

class ProductSearchSchema(BaseModel):
    query: Optional[str] = Field(None, description="Search query")
    category: Optional[ProductCategory] = Field(None, description="Filter by category")
    brand: Optional[str] = Field(None, description="Filter by brand")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    status: Optional[ProductStatus] = Field(None, description="Filter by status")
    is_featured: Optional[bool] = Field(None, description="Filter featured products")
    in_stock: Optional[bool] = Field(None, description="Filter by stock availability")
    sort_by: str = Field("created_at", description="Sort field")
    sort_order: str = Field("desc", description="Sort order (asc/desc)")

class ProductBulkUpdateSchema(BaseModel):
    product_ids: List[str] = Field(..., min_items=1, description="List of product IDs to update")
    updates: ProductUpdateSchema = Field(..., description="Updates to apply to all products")

class ProductInventoryUpdateSchema(BaseModel):
    sku: str = Field(..., description="Product SKU")
    quantity: int = Field(..., description="Quantity to add/subtract")
    operation: str = Field(..., description="Operation: 'add', 'subtract', or 'set'")
    notes: Optional[str] = Field(None, description="Notes about the inventory change")

class ProductCategorySchema(BaseModel):
    id: str = Field(..., description="Category ID")
    name: str = Field(..., description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    parent_id: Optional[str] = Field(None, description="Parent category ID")
    image_url: Optional[str] = Field(None, description="Category image URL")
    product_count: int = Field(0, description="Number of products in this category")
    is_active: bool = Field(True, description="Whether category is active")
    created_at: datetime = Field(..., description="Category creation timestamp")
    updated_at: datetime = Field(..., description="Category last update timestamp")
