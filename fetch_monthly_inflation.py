#!/usr/bin/env python3
"""
Monthly Inflation Tracker - Fetch 5 stores and APPEND to historical CSV
Designed to run on the 1st of each month via cron
"""
import asyncio
import csv
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import os
import sys

# 5 core stores for CPI tracking
CORE_STORES = {
    "31": "NYC",
    "452": "SF", 
    "546": "Chicago",
    "701": "LA",
    "706": "Brooklyn"
}

# Historical data file (will append to this)
HISTORICAL_FILE = "traderjoes_inflation_tracker.csv"

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
query SearchProducts($categoryId: String, $currentPage: Int, $pageSize: Int, $storeCode: String = "701", $published: String = "1") {
  products(
    filter: {store_code: {eq: $storeCode}, published: {eq: $published}, category_id: {eq: $categoryId}}
    currentPage: $currentPage
    pageSize: $pageSize
  ) {
    items {
      sku
      item_title
      sales_size
      sales_uom_description
      availability
      price_range {
        minimum_price {
          final_price {
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

async def fetch_store(page, code):
    """Fetch all products from one store"""
    all_products = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for category in CATEGORIES:
        current_page = 1
        total_pages = 1
        
        while current_page <= total_pages:
            variables = {
                "storeCode": str(code),
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
                        page_info = products_data.get('pageInfo', {})
                        total_pages = page_info.get('totalPages', 1)
                    
                    for item in items:
                            product = {
                                'sku': item.get('sku', ''),
                                'item_title': item.get('item_title', ''),
                                'retail_price': item.get('retail_price', ''),
                                'sales_size': item.get('sales_size', ''),
                                'sales_uom_description': item.get('sales_uom_description', ''),
                                'inserted_at': timestamp,
                                'store_code': str(code),
                                'availability': item.get('availability', ''),  # Now capturing actual status
                                'published': '1'
                            }
                        
                        if not product['retail_price'] and 'price_range' in item:
                            try:
                                price_val = item['price_range']['minimum_price']['final_price']['value']
                                product['retail_price'] = str(price_val)
                            except:
                                pass
                        
                        if product['sku']:
                            all_products.append(product)
                    
                    current_page += 1
                    await asyncio.sleep(0.2)
                else:
                    break
            except Exception as e:
                print(f"    Error: {e}", file=sys.stderr)
                break
    
    # Remove duplicates
    unique = {}
    for p in all_products:
        if p['sku'] not in unique:
            unique[p['sku']] = p
    
    return list(unique.values())

async def monthly_fetch():
    """Monthly fetch - appends to historical file"""
    run_date = datetime.now().strftime("%Y-%m-%d")
    
    print("="*70)
    print("TRADER JOE'S MONTHLY INFLATION TRACKER")
    print("="*70)
    print(f"Run Date: {run_date}")
    print(f"Stores: {len(CORE_STORES)}")
    print(f"Historical File: {HISTORICAL_FILE}")
    print("="*70)
    
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
            print("\nEstablishing session...")
            await page.goto('https://www.traderjoes.com/', wait_until='networkidle')
            await asyncio.sleep(2)
            print("✓ Ready\n")
            
            all_data = []
            
            for idx, (code, location) in enumerate(CORE_STORES.items(), 1):
                print(f"[{idx}/{len(CORE_STORES)}] Store {code} ({location})...", flush=True)
                products = await fetch_store(page, code)
                all_data.extend(products)
                print(f"  ✓ {len(products)} products collected")
                await asyncio.sleep(1)
            
            # Determine if we need to write header
            file_exists = os.path.exists(HISTORICAL_FILE)
            
            # Append to historical file
            fieldnames = ['sku', 'retail_price', 'item_title', 'inserted_at', 'store_code',
                         'availability', 'sales_size', 'sales_uom_description', 'published']
            
            mode = 'a' if file_exists else 'w'
            
            with open(HISTORICAL_FILE, mode, newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerows(all_data)
            
            action = "Appended to" if file_exists else "Created"
            
            print(f"\n{'='*70}")
            print("✓ MONTHLY FETCH COMPLETE")
            print(f"{'='*70}")
            print(f"{action} {HISTORICAL_FILE}")
            print(f"Records added this run: {len(all_data)}")
            
            # Show file stats
            if file_exists:
                with open(HISTORICAL_FILE, 'r') as f:
                    total_lines = sum(1 for _ in f)
                print(f"Total records in file: {total_lines - 1}")  # -1 for header
            
            # Create dated backup
            backup_file = f"backups/traderjoes_snapshot_{run_date}.csv"
            os.makedirs('backups', exist_ok=True)
            
            with open(backup_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_data)
            
            print(f"Monthly snapshot saved: {backup_file}")
            print(f"\n{'='*70}\n")
            
            return HISTORICAL_FILE
            
        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            sys.exit(1)
        
        finally:
            await browser.close()

if __name__ == "__main__":
    result = asyncio.run(monthly_fetch())
    print(f"✓ Inflation tracker updated: {result}")

