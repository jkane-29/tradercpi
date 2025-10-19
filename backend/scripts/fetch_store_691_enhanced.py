#!/usr/bin/env python3
"""
Enhanced scraper for Store 691 with anti-detection measures
Uses techniques to bypass API blocks
"""
import asyncio
import json
import csv
import random
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

# Target store
STORE_CODE = "691"
STORE_NAME = "Lincoln Park - 1840 N Clybourn Ave, Chicago, IL 60614"

# All categories including the root "Products" category (ID: 2)
CATEGORIES = [
    {"id": "2", "name": "Products (Root)"},  # THE MISSING CATEGORY!
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
      category_hierarchy {
        name
        __typename
      }
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

async def human_like_delay():
    """Add random human-like delays"""
    await asyncio.sleep(random.uniform(0.3, 0.8))

async def fetch_store_691(page):
    """Fetch ALL products from store 691 with anti-detection"""
    print(f"\n{'='*80}")
    print(f"FETCHING STORE 691: {STORE_NAME}")
    print(f"{'='*80}\n")
    
    all_products = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    page_size = 100  # Maximum page size
    
    total_items_expected = 0
    total_items_fetched = 0
    
    for cat_idx, category in enumerate(CATEGORIES, 1):
        print(f"[{cat_idx}/{len(CATEGORIES)}] {category['name']:25s} ", end='', flush=True)
        
        category_products = []
        current_page = 1
        total_pages = 1
        category_total_count = 0
        
        # Iterate through ALL pages for this category
        while current_page <= total_pages:
            variables = {
                "storeCode": STORE_CODE,
                "categoryId": int(category['id']),
                "currentPage": current_page,
                "pageSize": page_size
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
                            headers: {
                                'Content-Type': 'application/json',
                                'Accept': 'application/json',
                            },
                            body: JSON.stringify(payload)
                        });
                        const text = await response.text();
                        try {
                            return JSON.parse(text);
                        } catch (e) {
                            return { error: 'JSON parse error', text: text.substring(0, 200), status: response.status };
                        }
                    }
                """, payload)
                
                # Check for errors in response
                if 'error' in result:
                    if current_page == 1:
                        error_text = result.get('text', '')[:100]
                        print(f"[API Error {result.get('status', 'unknown')}] ", end='', flush=True)
                        # Log first category error with details
                        if cat_idx == 1:
                            print(f"\n    Error details: {error_text}")
                    break
                
                if 'data' in result and 'products' in result['data']:
                    products_data = result['data']['products']
                    items = products_data.get('items', [])
                    total_count = products_data.get('total_count', 0)
                    page_info = products_data.get('pageInfo', {})
                    
                    if current_page == 1:
                        total_pages = page_info.get('totalPages', 1)
                        category_total_count = total_count
                        total_items_expected += total_count
                        print(f"[{total_count:4d} items, {total_pages:3d} pages] ", end='', flush=True)
                    
                    # Extract product data
                    for item in items:
                        # Get category names
                        categories = []
                        if 'category_hierarchy' in item and item['category_hierarchy']:
                            categories = [cat.get('name', '') for cat in item['category_hierarchy']]
                        
                        product = {
                            'sku': item.get('sku', ''),
                            'item_title': item.get('item_title', ''),
                            'retail_price': item.get('retail_price', ''),
                            'sales_size': item.get('sales_size', ''),
                            'sales_uom_description': item.get('sales_uom_description', ''),
                            'inserted_at': timestamp,
                            'store_code': STORE_CODE,
                            'availability': item.get('availability', ''),
                            'published': item.get('published', ''),
                            'category': category['name'],
                            'category_id': category['id'],
                            'all_categories': ' > '.join(categories)
                        }
                        
                        # Try to get price from price_range if retail_price is empty
                        if not product['retail_price'] and 'price_range' in item:
                            try:
                                price_val = item['price_range']['minimum_price']['final_price']['value']
                                product['retail_price'] = str(price_val)
                            except:
                                pass
                        
                        if product['sku']:
                            category_products.append(product)
                            total_items_fetched += 1
                    
                    print(f".", end='', flush=True)
                    current_page += 1
                    
                    # Human-like delay between pages
                    await human_like_delay()
                else:
                    print(f"[No data returned]", end='', flush=True)
                    break
                    
            except Exception as e:
                print(f"\n    ERROR on page {current_page}: {e}")
                break
        
        all_products.extend(category_products)
        print(f" ✓ ({len(category_products)} products fetched)")
        
        # Longer delay between categories to appear more human
        if cat_idx < len(CATEGORIES):
            await asyncio.sleep(random.uniform(0.5, 1.2))
    
    # Remove duplicates (keep first occurrence)
    unique_products = {}
    for p in all_products:
        sku = p['sku']
        if sku not in unique_products:
            unique_products[sku] = p
    
    products_list = list(unique_products.values())
    
    print(f"\n{'='*80}")
    print(f"STORE 691 COMPLETE")
    print(f"{'='*80}")
    print(f"Total items expected: {total_items_expected}")
    print(f"Total items fetched: {len(all_products)}")
    print(f"Unique products: {len(products_list)}")
    print(f"Duplicates removed: {len(all_products) - len(products_list)}")
    print(f"{'='*80}\n")
    
    return products_list

async def main():
    """Main execution with enhanced anti-detection"""
    print("="*80)
    print("TRADER JOE'S - STORE 691 ENHANCED SCRAPER")
    print("="*80)
    print(f"Start time: {datetime.now()}")
    print(f"Store: {STORE_NAME}")
    print(f"Categories to scan: {len(CATEGORIES)}")
    print(f"Anti-detection: ENABLED\n")
    
    async with async_playwright() as p:
        # Launch with more realistic settings
        browser = await p.chromium.launch(
            headless=False,  # Run visible to appear more human
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
            ]
        )
        
        # Create context with realistic settings
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/Chicago',
            permissions=['geolocation'],
            geolocation={'latitude': 41.9224, 'longitude': -87.6531},  # Lincoln Park coordinates
        )
        
        # Add extra headers
        await context.set_extra_http_headers({
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        page = await context.new_page()
        
        # Apply stealth
        stealth_config = Stealth()
        await stealth_config.apply_stealth_async(page)
        
        # Override navigator.webdriver
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        try:
            # Establish session with human-like behavior
            print("Establishing session...")
            await page.goto('https://www.traderjoes.com/', wait_until='networkidle')
            await asyncio.sleep(random.uniform(3, 5))
            
            # Simulate some human interaction
            print("Simulating human browsing...")
            await page.evaluate('window.scrollBy(0, 500)')
            await asyncio.sleep(random.uniform(1, 2))
            
            # Navigate to products page
            print("Loading products page...")
            await page.goto('https://www.traderjoes.com/home/products', wait_until='networkidle')
            await asyncio.sleep(random.uniform(2, 4))
            
            # Scroll a bit
            await page.evaluate('window.scrollBy(0, 300)')
            await asyncio.sleep(random.uniform(1, 2))
            
            print("✓ Session established\n")
            
            # Fetch all products
            products = await fetch_store_691(page)
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"store_691_complete_{timestamp}.csv"
            
            fieldnames = ['sku', 'retail_price', 'item_title', 'sales_size', 'sales_uom_description',
                         'category', 'category_id', 'all_categories', 'inserted_at', 'store_code',
                         'availability', 'published']
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(products)
            
            print(f"\n{'='*80}")
            print(f"✓✓✓ COMPLETE! ✓✓✓")
            print(f"{'='*80}")
            print(f"Total unique products: {len(products)}")
            print(f"Saved to: {output_file}\n")
            
            # Statistics
            if len(products) > 0:
                with_price = sum(1 for p in products if p.get('retail_price'))
                print(f"Products with prices: {with_price} ({with_price/len(products)*100:.1f}%)")
                
                available = sum(1 for p in products if p.get('availability') == 'Available')
                print(f"Available products: {available} ({available/len(products)*100:.1f}%)")
            else:
                print(f"\n⚠️  WARNING: No products were fetched!")
                print(f"The API may still be blocking requests.")
            
            # Category breakdown
            if len(products) > 0:
                print(f"\n{'='*80}")
                print("CATEGORY BREAKDOWN:")
                print(f"{'='*80}")
                category_counts = {}
                for p in products:
                    cat = p.get('category', 'Unknown')
                    category_counts[cat] = category_counts.get(cat, 0) + 1
                
                for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {cat:25s}: {count:4d} products")
            
            print(f"\n{'='*80}")
            print(f"End time: {datetime.now()}")
            print(f"{'='*80}\n")
            
            return output_file
            
        finally:
            await asyncio.sleep(2)  # Let any final requests complete
            await browser.close()

if __name__ == "__main__":
    result = asyncio.run(main())
    if result:
        print(f"🎉 Store 691 dataset complete: {result}")

