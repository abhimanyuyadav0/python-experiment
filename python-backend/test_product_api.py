#!/usr/bin/env python3
"""
Test script for the Product API
Make sure MongoDB is running and the server is started before running this script
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:5001/api/v1"

def test_create_product():
    """Test creating a new product"""
    print("🧪 Testing product creation...")
    
    product_data = {
        "name": "Premium Wireless Headphones",
        "description": "High-quality wireless headphones with noise cancellation, premium sound quality, and long battery life. Perfect for music lovers and professionals.",
        "category": "electronics",
        "brand": "AudioTech",
        "sku": "AUD-WH-001",
        "base_price": 199.99,
        "compare_price": 249.99,
        "cost_price": 120.00,
        "weight": 0.25,
        "dimensions": {
            "length": 20.0,
            "width": 18.0,
            "height": 8.0
        },
        "tags": ["wireless", "noise-cancelling", "premium", "bluetooth"],
        "images": [
            {
                "url": "https://example.com/images/headphones-1.jpg",
                "alt_text": "Premium Wireless Headphones - Front View",
                "is_primary": True
            },
            {
                "url": "https://example.com/images/headphones-2.jpg",
                "alt_text": "Premium Wireless Headphones - Side View",
                "is_primary": False
            }
        ],
        "variants": [
            {
                "name": "Color",
                "value": "Black",
                "price_adjustment": 0.0,
                "stock_quantity": 50
            },
            {
                "name": "Color",
                "value": "White",
                "price_adjustment": 10.0,
                "stock_quantity": 30
            }
        ],
        "specifications": [
            {
                "key": "Battery Life",
                "value": "30",
                "unit": "hours"
            },
            {
                "key": "Bluetooth Version",
                "value": "5.0",
                "unit": ""
            },
            {
                "key": "Driver Size",
                "value": "40",
                "unit": "mm"
            }
        ],
        "meta_title": "Premium Wireless Headphones - AudioTech",
        "meta_description": "High-quality wireless headphones with noise cancellation. Premium sound quality and long battery life.",
        "is_featured": True,
        "is_taxable": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/products/", json=product_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            product = response.json()
            print("✅ Product created successfully!")
            print(f"Product ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"SKU: {product['sku']}")
            print(f"Price: ${product['base_price']}")
            print(f"Total Stock: {product['total_stock']}")
            return product['id']
        else:
            print(f"❌ Failed to create product: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating product: {str(e)}")
        return None

def test_create_second_product():
    """Test creating a second product"""
    print("\n🧪 Testing second product creation...")
    
    product_data = {
        "name": "Smart Fitness Watch",
        "description": "Advanced fitness tracking watch with heart rate monitor, GPS, and smartphone connectivity.",
        "category": "sports",
        "brand": "FitTech",
        "sku": "FIT-SW-001",
        "base_price": 299.99,
        "compare_price": 349.99,
        "cost_price": 180.00,
        "weight": 0.05,
        "dimensions": {
            "length": 4.5,
            "width": 4.5,
            "height": 1.2
        },
        "tags": ["fitness", "smartwatch", "health", "gps"],
        "images": [
            {
                "url": "https://example.com/images/watch-1.jpg",
                "alt_text": "Smart Fitness Watch - Front View",
                "is_primary": True
            }
        ],
        "variants": [
            {
                "name": "Size",
                "value": "42mm",
                "price_adjustment": 0.0,
                "stock_quantity": 25
            },
            {
                "name": "Size",
                "value": "46mm",
                "price_adjustment": 20.0,
                "stock_quantity": 20
            }
        ],
        "specifications": [
            {
                "key": "Battery Life",
                "value": "7",
                "unit": "days"
            },
            {
                "key": "Water Resistance",
                "value": "50",
                "unit": "meters"
            }
        ],
        "is_featured": False,
        "is_taxable": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/products/", json=product_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            product = response.json()
            print("✅ Second product created successfully!")
            print(f"Product ID: {product['id']}")
            print(f"Name: {product['name']}")
            return product['id']
        else:
            print(f"❌ Failed to create second product: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating second product: {str(e)}")
        return None

def test_get_product(product_id):
    """Test retrieving a product by ID"""
    if not product_id:
        print("❌ No product ID to test")
        return
    
    print(f"\n🧪 Testing product retrieval for ID: {product_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/products/{product_id}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            product = response.json()
            print("✅ Product retrieved successfully!")
            print(f"Name: {product['name']}")
            print(f"Brand: {product['brand']}")
            print(f"Category: {product['category']}")
            print(f"Variants: {len(product['variants'])}")
            print(f"Specifications: {len(product['specifications'])}")
        else:
            print(f"❌ Failed to retrieve product: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving product: {str(e)}")

def test_get_product_by_sku():
    """Test retrieving a product by SKU"""
    print("\n🧪 Testing product retrieval by SKU...")
    
    try:
        response = requests.get(f"{BASE_URL}/products/sku/AUD-WH-001")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            product = response.json()
            print("✅ Product retrieved by SKU successfully!")
            print(f"Name: {product['name']}")
            print(f"SKU: {product['sku']}")
        else:
            print(f"❌ Failed to retrieve product by SKU: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving product by SKU: {str(e)}")

def test_get_products():
    """Test retrieving all products"""
    print("\n🧪 Testing product list retrieval...")
    
    try:
        response = requests.get(f"{BASE_URL}/products/")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Products retrieved successfully!")
            print(f"Total Products: {result['total']}")
            print(f"Page: {result['page']}")
            print(f"Page Size: {result['size']}")
            print(f"Categories: {result['categories']}")
            
            if result['products']:
                print("Sample Products:")
                for product in result['products'][:3]:
                    print(f"  - {product['id']}: {product['name']} - ${product['base_price']}")
        else:
            print(f"❌ Failed to retrieve products: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving products: {str(e)}")

def test_search_products():
    """Test product search functionality"""
    print("\n🧪 Testing product search...")
    
    search_params = {
        "query": "wireless",
        "min_price": 100,
        "max_price": 300,
        "category": "electronics",
        "sort_by": "base_price",
        "sort_order": "asc"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/products/search", json=search_params)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Product search successful!")
            print(f"Found {result['total']} products matching criteria")
            
            if result['products']:
                print("Search Results:")
                for product in result['products']:
                    print(f"  - {product['name']}: ${product['base_price']} ({product['category']})")
        else:
            print(f"❌ Failed to search products: {response.text}")
    except Exception as e:
        print(f"❌ Error searching products: {str(e)}")

def test_update_product(product_id):
    """Test updating a product"""
    if not product_id:
        print("❌ No product ID to test")
        return
    
    print(f"\n🧪 Testing product update for ID: {product_id}")
    
    update_data = {
        "description": "Updated description for the premium wireless headphones with enhanced features.",
        "base_price": 189.99,
        "is_featured": True
    }
    
    try:
        response = requests.put(f"{BASE_URL}/products/{product_id}", json=update_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            product = response.json()
            print("✅ Product updated successfully!")
            print(f"New Price: ${product['base_price']}")
            print(f"Updated At: {product['updated_at']}")
        else:
            print(f"❌ Failed to update product: {response.text}")
    except Exception as e:
        print(f"❌ Error updating product: {str(e)}")

def test_update_inventory():
    """Test inventory update"""
    print("\n🧪 Testing inventory update...")
    
    inventory_update = {
        "sku": "AUD-WH-001",
        "quantity": 10,
        "operation": "add",
        "notes": "Restocking from supplier"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/products/inventory/update", json=inventory_update)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Inventory updated successfully!")
            print(f"SKU: {result['sku']}")
            print(f"Old Quantity: {result['old_quantity']}")
            print(f"New Quantity: {result['new_quantity']}")
            print(f"Operation: {result['operation']}")
        else:
            print(f"❌ Failed to update inventory: {response.text}")
    except Exception as e:
        print(f"❌ Error updating inventory: {str(e)}")

def test_get_featured_products():
    """Test getting featured products"""
    print("\n🧪 Testing featured products retrieval...")
    
    try:
        response = requests.get(f"{BASE_URL}/products/featured/?limit=5")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            products = response.json()
            print("✅ Featured products retrieved successfully!")
            print(f"Found {len(products)} featured products")
            
            for product in products:
                print(f"  - {product['name']}: ${product['base_price']} (Featured: {product['is_featured']})")
        else:
            print(f"❌ Failed to retrieve featured products: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving featured products: {str(e)}")

def test_get_products_by_category():
    """Test getting products by category"""
    print("\n🧪 Testing products by category...")
    
    try:
        response = requests.get(f"{BASE_URL}/products/category/electronics?limit=10")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            products = response.json()
            print("✅ Products by category retrieved successfully!")
            print(f"Found {len(products)} products in electronics category")
            
            for product in products[:3]:
                print(f"  - {product['name']}: ${product['base_price']}")
        else:
            print(f"❌ Failed to retrieve products by category: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving products by category: {str(e)}")

def test_get_product_statistics():
    """Test getting product statistics"""
    print("\n🧪 Testing product statistics...")
    
    try:
        response = requests.get(f"{BASE_URL}/products/statistics/overview")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Product statistics retrieved successfully!")
            print(f"Total Products: {stats['total_products']}")
            print(f"Active Products: {stats['active_products']}")
            print(f"Out of Stock: {stats['out_of_stock']}")
            print(f"Featured Products: {stats['featured_products']}")
            
            if stats['category_distribution']:
                print("Category Distribution:")
                for cat in stats['category_distribution'][:5]:
                    print(f"  - {cat['category']}: {cat['count']} products")
        else:
            print(f"❌ Failed to retrieve product statistics: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving product statistics: {str(e)}")

def test_get_available_categories():
    """Test getting available categories"""
    print("\n🧪 Testing available categories...")
    
    try:
        response = requests.get(f"{BASE_URL}/products/categories/available")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            categories = response.json()
            print("✅ Available categories retrieved successfully!")
            print(f"Found {len(categories)} categories:")
            for category in categories:
                print(f"  - {category}")
        else:
            print(f"❌ Failed to retrieve categories: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving categories: {str(e)}")

def test_get_available_brands():
    """Test getting available brands"""
    print("\n🧪 Testing available brands...")
    
    try:
        response = requests.get(f"{BASE_URL}/products/brands/available")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            brands = response.json()
            print("✅ Available brands retrieved successfully!")
            print(f"Found {len(brands)} brands:")
            for brand in brands:
                print(f"  - {brand}")
        else:
            print(f"❌ Failed to retrieve brands: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving brands: {str(e)}")

def test_get_available_tags():
    """Test getting available tags"""
    print("\n🧪 Testing available tags...")
    
    try:
        response = requests.get(f"{BASE_URL}/products/tags/available")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            tags = response.json()
            print("✅ Available tags retrieved successfully!")
            print(f"Found {len(tags)} tags:")
            for tag in tags:
                print(f"  - {tag}")
        else:
            print(f"❌ Failed to retrieve tags: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving tags: {str(e)}")

def test_update_product_status(product_id):
    """Test updating product status"""
    if not product_id:
        print("❌ No product ID to test")
        return
    
    print(f"\n🧪 Testing product status update for ID: {product_id}")
    
    try:
        # Update status to inactive
        response = requests.patch(f"{BASE_URL}/products/{product_id}/status?status=inactive")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            product = response.json()
            print("✅ Product status updated successfully!")
            print(f"New Status: {product['status']}")
        else:
            print(f"❌ Failed to update product status: {response.text}")
    except Exception as e:
        print(f"❌ Error updating product status: {str(e)}")

def test_toggle_product_featured(product_id):
    """Test toggling product featured status"""
    if not product_id:
        print("❌ No product ID to test")
        return
    
    print(f"\n🧪 Testing product featured toggle for ID: {product_id}")
    
    try:
        # Toggle featured status
        response = requests.patch(f"{BASE_URL}/products/{product_id}/feature?is_featured=false")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            product = response.json()
            print("✅ Product featured status updated successfully!")
            print(f"Featured: {product['is_featured']}")
        else:
            print(f"❌ Failed to update product featured status: {response.text}")
    except Exception as e:
        print(f"❌ Error updating product featured status: {str(e)}")

def main():
    """Run all tests"""
    print("🚀 Starting Product API Tests...")
    print("=" * 60)
    
    # Test product operations
    product_id = test_create_product()
    second_product_id = test_create_second_product()
    
    if product_id:
        test_get_product(product_id)
        test_get_product_by_sku()
        test_get_products()
        test_search_products()
        test_update_product(product_id)
        test_update_inventory()
        test_get_featured_products()
        test_get_products_by_category()
        test_get_product_statistics()
        test_get_available_categories()
        test_get_available_brands()
        test_get_available_tags()
        test_update_product_status(product_id)
        test_toggle_product_featured(product_id)
    
    print("\n" + "=" * 60)
    print("🏁 Product API tests completed!")
    
    if product_id:
        print(f"📝 Created test product with ID: {product_id}")
        print("💡 You can use this ID to test other operations manually")

if __name__ == "__main__":
    main()
