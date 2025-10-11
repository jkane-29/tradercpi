#!/usr/bin/env python3
"""
Fetch from 16 representative stores covering all pricing regions
Smart sampling strategy - gets pricing diversity without redundancy
"""
import asyncio
import json
import csv
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

# Representative stores from different pricing regions and store types
REPRESENTATIVE_STORES = {
    "31": "NYC area (standard pricing region 1)",
    "78": "East Coast cluster",
    "100": "Mid-Atlantic range",
    "150": "Northeast range",
    "200": "Eastern range",
    "250": "Central range",
    "350": "Midwest range",
    "400": "Central-West range",
    "452": "West Coast (SF area - different pricing)",
    "500": "Mountain/West range",
    "546": "Midwest (Chicago - different pricing)",
    "564": "Super store (1,922 products!)",
    "575": "Smaller specialty store (291 products)",
    "600": "Western range",
    "625": "Specialty store (503 products)",
    "701": "West Coast (LA - different pricing)",
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
query SearchProducts($categoryId: String, $currentPage: Int, $pageSize: Int, $storeCode: String = "701", $availability: String = "1", $published: String = "1") {
  products(
    filter: {store_code: {eq: $storeCode}, published: {eq: $published}, availability: {match: $availability}, category_id: {eq: $categoryId}}
    currentPage: $currentPage
    pageSize: $pageSize
  ) {
    items {
      sku
      item_title
      sales_size
      sales_uom_description
      price_range {
        minimum_price {
          final_price {
            currency
            value
          }
        }
      }
      retail_price
    }
    total_count
    pageInfo: page_info {
      currentPage: current_page
      totalPages: total_pages
    }
  }
}
"""

async def fetch_store(page, store_code, store_desc):
    """Fetch all products from one store"""
    print(f"\n{'='*70}")
    print(f"STORE {store_code}: {store_desc}")
    print(f"{'='*70}\n")
    
    all_products = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for cat_idx, category in enumerate(CATEGORIES, 1):
        current_page = 1
        total_pages = 1
        category_products = []
        
        while current_page <= total_pages:
            variables = {
                "storeCode": store_code,
                "availability": "1",
                "published": "1",
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
                    
                    if current_page == 1:
                        total_count = products_data.get('total_count', 0)
                        page_info = products_data.get('pageInfo', {})
                        total_pages = page_info.get('totalPages', 1)
                        print(f"[{cat_idx:2d}/23] {category['name']:20s} [{total_count:4d} products] ", end='', flush=True)
                    
                    for item in items:
                        product = {
                            'sku': item.get('sku', ''),
                            'item_title': item.get('item_title', ''),
                            'retail_price': item.get('retail_price', ''),
                            'sales_size': item.get('sales_size', ''),
                            'sales_uom_description': item.get('sales_uom_description', ''),
                            'inserted_at': timestamp,
                            'store_code': store_code,
                            'availability': '1',
                            'published': '1'
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
        print(f"✓ ({len(category_products)} collected)")
    
    # Remove duplicates
    unique = {}
    for p in all_products:
        sku = p['sku']
        if sku not in unique:
            unique[sku] = p
    
    products_list = list(unique.values())
    print(f"\n✓ Store {store_code} complete: {len(products_list)} unique products\n")
    
    return products_list

async def fetch_representative():
    """Fetch from representative stores"""
    print("="*70)
    print("FETCHING FROM REPRESENTATIVE STORES")
    print(f"Stores: {len(REPRESENTATIVE_STORES)}")
    print("="*70)
    print(f"Start: {datetime.now()}\n")
    
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
            print("Establishing session...")
            await page.goto('https://www.traderjoes.com/', wait_until='networkidle')
            await asyncio.sleep(2)
            print("✓ Ready\n")
            
            all_data = []
            summary = {}
            
            for idx, (code, desc) in enumerate(REPRESENTATIVE_STORES.items(), 1):
                print(f"\n>>> [{idx}/{len(REPRESENTATIVE_STORES)}] Fetching store {code}...")
                products = await fetch_store(page, code, desc)
                all_data.extend(products)
                summary[code] = len(products)
                
                await asyncio.sleep(1)
            
            # Save
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"traderjoes_REPRESENTATIVE_{timestamp}.csv"
            
            fieldnames = ['sku', 'retail_price', 'item_title', 'inserted_at', 'store_code',
                         'availability', 'sales_size', 'sales_uom_description', 'published']
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_data)
            
            print(f"\n{'='*70}")
            print("✓✓✓ REPRESENTATIVE FETCH COMPLETE! ✓✓✓")
            print(f"{'='*70}")
            print(f"Total records: {len(all_data):,}")
            print(f"Saved to: {output_file}\n")
            
            print("Products per store:")
            for code, count in sorted(summary.items()):
                print(f"  {code}: {count:,} products")
            
            # Unique products
            unique_skus = set(p['sku'] for p in all_data)
            print(f"\nUnique products across all stores: {len(unique_skus):,}")
            
            return output_file
            
        finally:
            await browser.close()

if __name__ == "__main__":
    result = asyncio.run(fetch_representative())
    print(f"\n🎉 Representative dataset complete: {result}")

