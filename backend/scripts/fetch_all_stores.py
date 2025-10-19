#!/usr/bin/env python3
"""
Fetch products from ALL Trader Joe's stores
Creates comprehensive multi-store dataset
"""
import asyncio
import json
import csv
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

# Known valid store codes (from old data)
STORES = {
    "31": "New York, NY - Union Square",
    "452": "San Francisco, CA",
    "546": "Chicago, IL",
    "701": "Los Angeles, CA",
    "706": "Brooklyn, NY"
}

# All categories
CATEGORIES = [
    {"id": "8", "name": "Food"},
    {"id": "11", "name": "Bakery"},
    {"id": "29", "name": "Cheese"},
    {"id": "44", "name": "Dairy & Eggs"},
    {"id": "59", "name": "Dips & Sauces"},
    {"id": "80", "name": "Fresh Prepared"},
    {"id": "95", "name": "Freezer"},
    {"id": "107", "name": "Desserts"},
    {"id": "113", "name": "Produce"},
    {"id": "122", "name": "Meat/Plant-Based"},
    {"id": "131", "name": "Seafood"},
    {"id": "137", "name": "Pantry"},
    {"id": "167", "name": "Snacks"},
    {"id": "182", "name": "Beverages"},
    {"id": "191", "name": "Non-Dairy Beverages"},
    {"id": "47", "name": "Milk & Cream"},
    {"id": "197", "name": "Sodas"},
    {"id": "200", "name": "Alcohol"},
    {"id": "203", "name": "Flowers"},
    {"id": "215", "name": "Everything Else"},
    {"id": "218", "name": "Household"},
    {"id": "221", "name": "Beauty"},
    {"id": "224", "name": "Pet"},
]

GRAPHQL_QUERY = """
query SearchProducts($categoryId: String, $currentPage: Int, $pageSize: Int, $storeCode: String = "701") {
  products(
    filter: {store_code: {eq: $storeCode}, category_id: {eq: $categoryId}}
    currentPage: $currentPage
    pageSize: $pageSize
  ) {
    items {
      sku
      item_title
      sales_size
      sales_uom_description
      availability
      published
      price_range {
        minimum_price {
          final_price {
            currency
            value
            __typename
          }
          __typename
        }
        __typename
      }
      retail_price
      __typename
    }
    total_count
    pageInfo: page_info {
      currentPage: current_page
      totalPages: total_pages
      __typename
    }
    __typename
  }
}
"""

async def fetch_store(page, store_code, store_name):
    """Fetch all products for one store"""
    print(f"\n{'='*70}")
    print(f"FETCHING STORE: {store_name} (Code: {store_code})")
    print(f"{'='*70}\n")
    
    all_products = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for cat_idx, category in enumerate(CATEGORIES, 1):
        print(f"[{cat_idx}/{len(CATEGORIES)}] {category['name']:20s} ", end='', flush=True)
        
        category_products = []
        current_page = 1
        total_pages = 1
        
        while current_page <= total_pages:
            variables = {
                "storeCode": store_code,
                "categoryId": int(category['id']),
                "currentPage": current_page,
                "pageSize": 15
            }
            
            payload = {
                "operationName": "SearchProducts",
                "variables": variables,
                "query": GRAPHQL_QUERY
            }
            
            try:
                result = await page.evaluate("""
                    async (payload) => {
                        const response = await fetch('https://www.traderjoes.com/api/graphql', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify(payload)
                        });
                        return await response.json();
                    }
                """, payload)
                
                if 'data' in result and 'products' in result['data']:
                    products_data = result['data']['products']
                    items = products_data.get('items', [])
                    total_count = products_data.get('total_count', 0)
                    page_info = products_data.get('pageInfo', {})
                    
                    if current_page == 1:
                        total_pages = page_info.get('totalPages', 1)
                        print(f"[{total_count:4d} products, {total_pages:2d} pages] ", end='', flush=True)
                    
                    for item in items:
                        product = {
                            'sku': item.get('sku', ''),
                            'item_title': item.get('item_title', ''),
                            'retail_price': item.get('retail_price', ''),
                            'sales_size': item.get('sales_size', ''),
                            'sales_uom_description': item.get('sales_uom_description', ''),
                            'inserted_at': timestamp,
                            'store_code': store_code,
                            'availability': item.get('availability', ''),
                            'published': item.get('published', '')
                        }
                        
                        if not product['retail_price'] and 'price_range' in item:
                            try:
                                price_val = item['price_range']['minimum_price']['final_price']['value']
                                product['retail_price'] = str(price_val)
                            except:
                                pass
                        
                        if product['sku']:
                            category_products.append(product)
                    
                    current_page += 1
                    await asyncio.sleep(0.2)
                else:
                    break
                    
            except Exception as e:
                print(f"Error: {e}")
                break
        
        all_products.extend(category_products)
        print(f"✓ ({len(category_products)} products)")
    
    # Remove duplicates
    unique_products = {}
    for p in all_products:
        sku = p['sku']
        if sku not in unique_products:
            unique_products[sku] = p
    
    products_list = list(unique_products.values())
    
    print(f"\n{'='*70}")
    print(f"Store {store_code} Complete: {len(products_list)} unique products")
    print(f"{'='*70}\n")
    
    return products_list

async def fetch_all_stores():
    """Fetch from all stores"""
    print("="*70)
    print("TRADER JOE'S - MULTI-STORE COMPREHENSIVE FETCH")
    print("="*70)
    print(f"Start time: {datetime.now()}")
    print(f"Stores to fetch: {len(STORES)}")
    print(f"Categories per store: {len(CATEGORIES)}\n")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        )
        
        page = await context.new_page()
        stealth_config = Stealth()
        await stealth_config.apply_stealth_async(page)
        
        try:
            # Establish session
            print("Establishing session...")
            await page.goto('https://www.traderjoes.com/', wait_until='networkidle')
            await asyncio.sleep(2)
            print("✓ Session established\n")
            
            all_stores_data = []
            store_summary = {}
            
            for store_code, store_name in STORES.items():
                products = await fetch_store(page, store_code, store_name)
                all_stores_data.extend(products)
                store_summary[store_code] = {
                    'name': store_name,
                    'products': len(products)
                }
                
                # Small delay between stores
                await asyncio.sleep(2)
            
            # Save combined results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"traderjoes_ALL_STORES_{timestamp}.csv"
            
            fieldnames = ['sku', 'retail_price', 'item_title', 'inserted_at', 'store_code',
                         'availability', 'sales_size', 'sales_uom_description', 'published']
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_stores_data)
            
            print(f"\n{'='*70}")
            print(f"✓✓✓ ALL STORES COMPLETE! ✓✓✓")
            print(f"{'='*70}")
            print(f"Total records: {len(all_stores_data)}")
            print(f"Saved to: {output_file}\n")
            
            print("Products per store:")
            for store_code, info in sorted(store_summary.items()):
                print(f"  {store_code} ({info['name']:35s}): {info['products']:4d} products")
            
            # Count unique products across all stores
            unique_skus = set(p['sku'] for p in all_stores_data)
            print(f"\nUnique products across all stores: {len(unique_skus)}")
            
            # Statistics
            with_price = sum(1 for p in all_stores_data if p.get('retail_price'))
            print(f"Records with prices: {with_price} ({with_price/len(all_stores_data)*100:.1f}%)")
            
            print(f"\n{'='*70}\n")
            
            return output_file
            
        finally:
            await browser.close()

if __name__ == "__main__":
    result = asyncio.run(fetch_all_stores())
    if result:
        print(f"🎉 Multi-store dataset complete: {result}")

