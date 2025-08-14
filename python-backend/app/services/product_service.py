from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from bson import ObjectId
from app.core.mongodb import get_mongodb
from app.schemas.product import (
    ProductCreateSchema, ProductUpdateSchema, ProductResponseSchema, 
    ProductStatus, ProductSearchSchema, ProductBulkUpdateSchema,
    ProductInventoryUpdateSchema, ProductCategorySchema
)
import re

class ProductService:
    def __init__(self):
        self.db = get_mongodb()
        self.collection = self.db.products
        self.categories_collection = self.db.product_categories

    async def create_product(self, product_data: ProductCreateSchema) -> ProductResponseSchema:
        """Create a new product"""
        try:
            # Check if SKU already exists
            existing_product = await self.collection.find_one({"sku": product_data.sku})
            if existing_product:
                raise ValueError(f"Product with SKU '{product_data.sku}' already exists")

            # Calculate total stock from variants
            total_stock = sum(variant.stock_quantity for variant in product_data.variants)
            
            # Prepare product document
            product_doc = {
                "name": product_data.name,
                "description": product_data.description,
                "category": product_data.category,
                "brand": product_data.brand,
                "sku": product_data.sku,
                "base_price": product_data.base_price,
                "compare_price": product_data.compare_price,
                "cost_price": product_data.cost_price,
                "weight": product_data.weight,
                "dimensions": product_data.dimensions,
                "tags": product_data.tags,
                "images": [img.dict() for img in product_data.images],
                "variants": [variant.dict() for variant in product_data.variants],
                "specifications": [spec.dict() for spec in product_data.specifications],
                "meta_title": product_data.meta_title,
                "meta_description": product_data.meta_description,
                "is_featured": product_data.is_featured,
                "is_taxable": product_data.is_taxable,
                "status": ProductStatus.ACTIVE,
                "total_stock": total_stock,
                "average_rating": None,
                "review_count": 0,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }

            # Insert product into database
            result = await self.collection.insert_one(product_doc)
            product_doc["id"] = str(result.inserted_id)

            # Update category product count
            await self._update_category_product_count(product_data.category, 1)

            return ProductResponseSchema(**product_doc)

        except Exception as e:
            raise Exception(f"Failed to create product: {str(e)}")

    async def get_product_by_id(self, product_id: str) -> Optional[ProductResponseSchema]:
        """Get product by ID"""
        try:
            product_doc = await self.collection.find_one({"_id": ObjectId(product_id)})
            if product_doc:
                product_doc["id"] = str(product_doc["_id"])
                del product_doc["_id"]
                return ProductResponseSchema(**product_doc)
            return None
        except Exception:
            return None

    async def get_product_by_sku(self, sku: str) -> Optional[ProductResponseSchema]:
        """Get product by SKU"""
        try:
            product_doc = await self.collection.find_one({"sku": sku})
            if product_doc:
                product_doc["id"] = str(product_doc["_id"])
                del product_doc["_id"]
                return ProductResponseSchema(**product_doc)
            return None
        except Exception:
            return None

    async def search_products(
        self, 
        search_params: ProductSearchSchema,
        skip: int = 0, 
        limit: int = 20
    ) -> Dict[str, Any]:
        """Search products with advanced filtering and sorting"""
        try:
            # Build filter query
            filter_query = {}
            
            # Text search
            if search_params.query:
                filter_query["$or"] = [
                    {"name": {"$regex": search_params.query, "$options": "i"}},
                    {"description": {"$regex": search_params.query, "$options": "i"}},
                    {"tags": {"$in": [re.compile(search_params.query, re.IGNORECASE)]}},
                    {"brand": {"$regex": search_params.query, "$options": "i"}}
                ]

            # Category filter
            if search_params.category:
                filter_query["category"] = search_params.category

            # Brand filter
            if search_params.brand:
                filter_query["brand"] = {"$regex": search_params.brand, "$options": "i"}

            # Price range filter
            if search_params.min_price is not None or search_params.max_price is not None:
                price_filter = {}
                if search_params.min_price is not None:
                    price_filter["$gte"] = search_params.min_price
                if search_params.max_price is not None:
                    price_filter["$lte"] = search_params.max_price
                filter_query["base_price"] = price_filter

            # Tags filter
            if search_params.tags:
                filter_query["tags"] = {"$in": search_params.tags}

            # Status filter
            if search_params.status:
                filter_query["status"] = search_params.status

            # Featured filter
            if search_params.is_featured is not None:
                filter_query["is_featured"] = search_params.is_featured

            # Stock filter
            if search_params.in_stock is not None:
                if search_params.in_stock:
                    filter_query["total_stock"] = {"$gt": 0}
                else:
                    filter_query["total_stock"] = {"$lte": 0}

            # Build sort query
            sort_field = search_params.sort_by
            sort_order = -1 if search_params.sort_order.lower() == "desc" else 1
            sort_query = {sort_field: sort_order}

            # Get total count
            total = await self.collection.count_documents(filter_query)

            # Get products with pagination and sorting
            cursor = self.collection.find(filter_query).skip(skip).limit(limit).sort(sort_query)
            products = []
            
            async for product_doc in cursor:
                product_doc["id"] = str(product_doc["_id"])
                del product_doc["_id"]
                products.append(ProductResponseSchema(**product_doc))

            # Get unique categories in results
            categories = list(set(product.category for product in products))

            return {
                "products": products,
                "total": total,
                "page": skip // limit + 1,
                "size": limit,
                "categories": categories
            }

        except Exception as e:
            raise Exception(f"Failed to search products: {str(e)}")

    async def get_products(
        self, 
        skip: int = 0, 
        limit: int = 20,
        category: Optional[str] = None,
        status: Optional[ProductStatus] = None,
        is_featured: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Get products with basic filtering"""
        try:
            # Build filter
            filter_query = {}
            if category:
                filter_query["category"] = category
            if status:
                filter_query["status"] = status
            if is_featured is not None:
                filter_query["is_featured"] = is_featured

            # Get total count
            total = await self.collection.count_documents(filter_query)

            # Get products with pagination
            cursor = self.collection.find(filter_query).skip(skip).limit(limit).sort("created_at", -1)
            products = []
            
            async for product_doc in cursor:
                product_doc["id"] = str(product_doc["_id"])
                del product_doc["_id"]
                products.append(ProductResponseSchema(**product_doc))

            # Get unique categories in results
            categories = list(set(product.category for product in products))

            return {
                "products": products,
                "total": total,
                "page": skip // limit + 1,
                "size": limit,
                "categories": categories
            }

        except Exception as e:
            raise Exception(f"Failed to retrieve products: {str(e)}")

    async def update_product(self, product_id: str, update_data: ProductUpdateSchema) -> Optional[ProductResponseSchema]:
        """Update product"""
        try:
            # Prepare update document
            update_doc = {"updated_at": datetime.utcnow()}
            
            # Add fields that are not None
            for field, value in update_data.dict(exclude_unset=True).items():
                update_doc[field] = value

            # Update product in database
            result = await self.collection.update_one(
                {"_id": ObjectId(product_id)},
                {"$set": update_doc}
            )

            if result.modified_count > 0:
                # Return updated product
                return await self.get_product_by_id(product_id)
            return None

        except Exception as e:
            raise Exception(f"Failed to update product: {str(e)}")

    async def delete_product(self, product_id: str) -> bool:
        """Delete product"""
        try:
            # Get product before deletion to update category count
            product = await self.get_product_by_id(product_id)
            if not product:
                return False

            # Delete product
            result = await self.collection.delete_one({"_id": ObjectId(product_id)})
            
            if result.deleted_count > 0:
                # Update category product count
                await self._update_category_product_count(product.category, -1)
                return True
            return False

        except Exception as e:
            raise Exception(f"Failed to delete product: {str(e)}")

    async def bulk_update_products(self, bulk_update: ProductBulkUpdateSchema) -> Dict[str, Any]:
        """Bulk update multiple products"""
        try:
            # Convert string IDs to ObjectIds
            object_ids = [ObjectId(pid) for pid in bulk_update.product_ids]
            
            # Prepare update document
            update_doc = {"updated_at": datetime.utcnow()}
            for field, value in bulk_update.updates.dict(exclude_unset=True).items():
                update_doc[field] = value

            # Perform bulk update
            result = await self.collection.update_many(
                {"_id": {"$in": object_ids}},
                {"$set": update_doc}
            )

            return {
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "message": f"Updated {result.modified_count} out of {result.matched_count} products"
            }

        except Exception as e:
            raise Exception(f"Failed to bulk update products: {str(e)}")

    async def update_inventory(self, inventory_update: ProductInventoryUpdateSchema) -> Dict[str, Any]:
        """Update product inventory"""
        try:
            # Find product by SKU
            product = await self.collection.find_one({"sku": inventory_update.sku})
            if not product:
                raise ValueError(f"Product with SKU '{inventory_update.sku}' not found")

            # Calculate new quantity based on operation
            current_quantity = product.get("total_stock", 0)
            
            if inventory_update.operation == "add":
                new_quantity = current_quantity + inventory_update.quantity
            elif inventory_update.operation == "subtract":
                new_quantity = max(0, current_quantity - inventory_update.quantity)
            elif inventory_update.operation == "set":
                new_quantity = inventory_update.quantity
            else:
                raise ValueError("Operation must be 'add', 'subtract', or 'set'")

            # Update product inventory
            result = await self.collection.update_one(
                {"sku": inventory_update.sku},
                {
                    "$set": {
                        "total_stock": new_quantity,
                        "updated_at": datetime.utcnow()
                    }
                }
            )

            if result.modified_count > 0:
                # Update status based on stock
                new_status = ProductStatus.OUT_OF_STOCK if new_quantity == 0 else ProductStatus.ACTIVE
                await self.collection.update_one(
                    {"sku": inventory_update.sku},
                    {"$set": {"status": new_status}}
                )

                return {
                    "sku": inventory_update.sku,
                    "old_quantity": current_quantity,
                    "new_quantity": new_quantity,
                    "operation": inventory_update.operation,
                    "status": new_status,
                    "message": f"Inventory updated successfully"
                }
            else:
                raise Exception("Failed to update inventory")

        except Exception as e:
            raise Exception(f"Failed to update inventory: {str(e)}")

    async def get_featured_products(self, limit: int = 10) -> List[ProductResponseSchema]:
        """Get featured products"""
        try:
            cursor = self.collection.find({
                "is_featured": True,
                "status": ProductStatus.ACTIVE
            }).limit(limit).sort("created_at", -1)
            
            products = []
            async for product_doc in cursor:
                product_doc["id"] = str(product_doc["_id"])
                del product_doc["_id"]
                products.append(ProductResponseSchema(**product_doc))
            
            return products

        except Exception as e:
            raise Exception(f"Failed to get featured products: {str(e)}")

    async def get_products_by_category(self, category: str, limit: int = 20) -> List[ProductResponseSchema]:
        """Get products by category"""
        try:
            cursor = self.collection.find({
                "category": category,
                "status": ProductStatus.ACTIVE
            }).limit(limit).sort("created_at", -1)
            
            products = []
            async for product_doc in cursor:
                product_doc["id"] = str(product_doc["_id"])
                del product_doc["_id"]
                products.append(ProductResponseSchema(**product_doc))
            
            return products

        except Exception as e:
            raise Exception(f"Failed to get products by category: {str(e)}")

    async def _update_category_product_count(self, category: str, change: int):
        """Update product count for a category"""
        try:
            await self.categories_collection.update_one(
                {"name": category},
                {"$inc": {"product_count": change}},
                upsert=True
            )
        except Exception:
            # Silently fail if category update fails
            pass

    async def get_product_statistics(self) -> Dict[str, Any]:
        """Get product statistics"""
        try:
            total_products = await self.collection.count_documents({})
            active_products = await self.collection.count_documents({"status": ProductStatus.ACTIVE})
            out_of_stock = await self.collection.count_documents({"status": ProductStatus.OUT_OF_STOCK})
            featured_products = await self.collection.count_documents({"is_featured": True})
            
            # Get category distribution
            pipeline = [
                {"$group": {"_id": "$category", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            category_stats = []
            async for doc in self.collection.aggregate(pipeline):
                category_stats.append({
                    "category": doc["_id"],
                    "count": doc["count"]
                })

            return {
                "total_products": total_products,
                "active_products": active_products,
                "out_of_stock": out_of_stock,
                "featured_products": featured_products,
                "category_distribution": category_stats
            }

        except Exception as e:
            raise Exception(f"Failed to get product statistics: {str(e)}")
