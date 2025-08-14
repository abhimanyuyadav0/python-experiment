from fastapi import APIRouter, HTTPException, Query, Depends, Body
from typing import Optional, List
from app.schemas.product import (
    ProductCreateSchema, ProductUpdateSchema, ProductResponseSchema, 
    ProductListResponseSchema, ProductSearchSchema, ProductBulkUpdateSchema,
    ProductInventoryUpdateSchema, ProductStatus, ProductCategory
)
from app.services.product_service import ProductService
from app.services.product_service_sqlite import ProductServiceSQLite

router = APIRouter()

def get_product_service():
    """Dynamically get the appropriate product service based on MongoDB availability"""
    try:
        from app.core.mongodb import get_mongodb
        # Try to get MongoDB connection
        get_mongodb()
        print("✅ Using MongoDB ProductService")
        return ProductService()
    except Exception as e:
        print(f"⚠️ MongoDB not available, using SQLite ProductService: {str(e)}")
        return ProductServiceSQLite()

@router.post("/", response_model=ProductResponseSchema, summary="Create a new product")
async def create_product(product_data: ProductCreateSchema):
    """
    Create a new product with comprehensive details including:
    
    - **Basic Info**: Name, description, category, brand, SKU
    - **Pricing**: Base price, compare price, cost price
    - **Inventory**: Variants with stock quantities
    - **Media**: Images with alt text and primary image flag
    - **Specifications**: Technical details and measurements
    - **SEO**: Meta title and description
    - **Settings**: Featured status, tax settings
    """
    try:
        product_service = get_product_service()
        print("product_data", product_data)
        product = await product_service.create_product(product_data)
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create product: {str(e)}")

@router.get("/", response_model=ProductListResponseSchema, summary="Get all products")
async def get_products(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of records to return"),
    category: Optional[ProductCategory] = Query(None, description="Filter by product category"),
    status: Optional[ProductStatus] = Query(None, description="Filter by product status"),
    is_featured: Optional[bool] = Query(None, description="Filter featured products")
):
    """
    Retrieve a paginated list of products with optional filtering.
    
    - **skip**: Number of records to skip for pagination
    - **limit**: Maximum number of records to return (max 100)
    - **category**: Filter products by category
    - **status**: Filter products by status
    - **is_featured**: Filter featured products
    """
    try:
        product_service = get_product_service()
        result = await product_service.get_products(skip, limit, category, status, is_featured)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve products: {str(e)}")

@router.get("/{product_id}", response_model=ProductResponseSchema, summary="Get product by ID")
async def get_product(product_id: str):
    """
    Retrieve a product by its unique identifier.
    
    - **product_id**: The unique identifier of the product
    """
    product_service = get_product_service()
    product = await product_service.get_product_by_id(product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product

@router.get("/sku/{sku}", response_model=ProductResponseSchema, summary="Get product by SKU")
async def get_product_by_sku(sku: str):
    """
    Retrieve a product by its SKU (Stock Keeping Unit).
    
    - **sku**: The SKU of the product
    """
    product_service = get_product_service()
    product = await product_service.get_product_by_sku(sku)
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product

@router.post("/search", response_model=ProductListResponseSchema, summary="Search products")
async def search_products(
    search_params: ProductSearchSchema,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of records to return")
):
    """
    Advanced product search with multiple filters and sorting options.
    
    **Search Parameters:**
    - **query**: Text search in name, description, tags, and brand
    - **category**: Filter by product category
    - **brand**: Filter by brand name
    - **min_price/max_price**: Price range filtering
    - **tags**: Filter by specific tags
    - **status**: Filter by product status
    - **is_featured**: Filter featured products
    - **in_stock**: Filter by stock availability
    - **sort_by**: Sort field (created_at, name, price, etc.)
    - **sort_order**: Sort direction (asc/desc)
    """
    try:
        product_service = get_product_service()
        result = await product_service.search_products(search_params, skip, limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search products: {str(e)}")

@router.put("/{product_id}", response_model=ProductResponseSchema, summary="Update product")
async def update_product(product_id: str, update_data: ProductUpdateSchema):
    """
    Update an existing product with new information.
    
    - **product_id**: The unique identifier of the product to update
    - **update_data**: The new product data to apply
    """
    try:
        product_service = get_product_service()
        updated_product = await product_service.update_product(product_id, update_data)
        
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return updated_product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update product: {str(e)}")

@router.delete("/{product_id}", summary="Delete product")
async def delete_product(product_id: str):
    """
    Delete a product by its unique identifier.
    
    - **product_id**: The unique identifier of the product to delete
    """
    try:
        product_service = get_product_service()
        success = await product_service.delete_product(product_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return {"message": "Product deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete product: {str(e)}")

@router.post("/bulk-update", summary="Bulk update products")
async def bulk_update_products(bulk_update: ProductBulkUpdateSchema):
    """
    Update multiple products at once with the same changes.
    
    - **product_ids**: List of product IDs to update
    - **updates**: The changes to apply to all products
    """
    try:
        product_service = get_product_service()
        result = await product_service.bulk_update_products(bulk_update)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to bulk update products: {str(e)}")

@router.post("/inventory/update", summary="Update product inventory")
async def update_inventory(inventory_update: ProductInventoryUpdateSchema):
    """
    Update product inventory levels.
    
    - **sku**: Product SKU to update
    - **quantity**: Quantity to add/subtract/set
    - **operation**: Operation type ('add', 'subtract', or 'set')
    - **notes**: Optional notes about the inventory change
    """
    try:
        product_service = get_product_service()
        result = await product_service.update_inventory(inventory_update)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update inventory: {str(e)}")

@router.get("/featured/", response_model=List[ProductResponseSchema], summary="Get featured products")
async def get_featured_products(
    limit: int = Query(10, ge=1, le=50, description="Number of featured products to return")
):
    """
    Retrieve featured products for display on homepage or promotional areas.
    
    - **limit**: Maximum number of featured products to return
    """
    try:
        product_service = get_product_service()
        products = await product_service.get_featured_products(limit)
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve featured products: {str(e)}")

@router.get("/category/{category}", response_model=List[ProductResponseSchema], summary="Get products by category")
async def get_products_by_category(
    category: ProductCategory,
    limit: int = Query(20, ge=1, le=100, description="Number of products to return")
):
    """
    Retrieve products from a specific category.
    
    - **category**: The product category to filter by
    - **limit**: Maximum number of products to return
    """
    try:
        product_service = get_product_service()
        products = await product_service.get_products_by_category(category, limit)
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve products by category: {str(e)}")

@router.get("/statistics/overview", summary="Get product statistics")
async def get_product_statistics():
    """
    Retrieve comprehensive product statistics including:
    
    - Total product count
    - Active vs inactive products
    - Out of stock products
    - Featured products count
    - Category distribution
    """
    try:
        product_service = get_product_service()
        stats = await product_service.get_product_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve product statistics: {str(e)}")

@router.get("/categories/available", response_model=List[str], summary="Get available categories")
async def get_available_categories():
    """
    Retrieve list of all available product categories.
    """
    try:
        # Return all enum values from ProductCategory
        return [category.value for category in ProductCategory]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve categories: {str(e)}")

@router.get("/brands/available", response_model=List[str], summary="Get available brands")
async def get_available_brands():
    """
    Retrieve list of all available product brands.
    """
    try:
        product_service = get_product_service()
        # Get unique brands from products collection
        pipeline = [
            {"$match": {"brand": {"$exists": True, "$ne": None}}},
            {"$group": {"_id": "$brand"}},
            {"$sort": {"_id": 1}}
        ]
        
        brands = []
        async for doc in product_service.collection.aggregate(pipeline):
            brands.append(doc["_id"])
        
        return brands
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve brands: {str(e)}")

@router.get("/tags/available", response_model=List[str], summary="Get available tags")
async def get_available_tags():
    """
    Retrieve list of all available product tags.
    """
    try:
        product_service = get_product_service()
        # Get unique tags from products collection
        pipeline = [
            {"$unwind": "$tags"},
            {"$group": {"_id": "$tags"}},
            {"$sort": {"_id": 1}}
        ]
        
        tags = []
        async for doc in product_service.collection.aggregate(pipeline):
            tags.append(doc["_id"])
        
        return tags
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tags: {str(e)}")

@router.patch("/{product_id}/status", response_model=ProductResponseSchema, summary="Update product status")
async def update_product_status(product_id: str, status: ProductStatus):
    """
    Update the status of a product.
    
    - **product_id**: The unique identifier of the product
    - **status**: The new status to set
    """
    try:
        update_data = ProductUpdateSchema(status=status)
        product_service = get_product_service()
        updated_product = await product_service.update_product(product_id, update_data)
        
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return updated_product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update product status: {str(e)}")

@router.patch("/{product_id}/feature", response_model=ProductResponseSchema, summary="Toggle product featured status")
async def toggle_product_featured(product_id: str, is_featured: bool):
    """
    Toggle the featured status of a product.
    
    - **product_id**: The unique identifier of the product
    - **is_featured**: Whether the product should be featured
    """
    try:
        update_data = ProductUpdateSchema(is_featured=is_featured)
        product_service = get_product_service()
        updated_product = await product_service.update_product(product_id, update_data)
        
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return updated_product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update product featured status: {str(e)}")
