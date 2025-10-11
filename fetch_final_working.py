#!/usr/bin/env python3
"""
FINAL WORKING SCRAPER - Uses the exact query structure from the website
"""
import asyncio
import json
import csv
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

# Store code discovered from actual queries
STORE_CODE = "701"  # Los Angeles - change this to test other stores

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

# Exact query from the website (discovered via inspection)
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
      category_hierarchy {
        id
        name
        __typename
      }
      sales_size
      sales_uom_description
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

async def fetch_all_products():
    """Fetch ALL products using the correct query structure"""
    print("="*70)
    print("TRADER JOE'S - FINAL WORKING SCRAPER")
    print("="*70)
    print(f"Store Code: {STORE_CODE}")
    print(f"Start time: {datetime.now()}\n")
    
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
            
            all_products = []
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for cat_idx, category in enumerate(CATEGORIES, 1):
                print(f"{'='*70}")
                print(f"[{cat_idx}/{len(CATEGORIES)}] {category['name']}")
                print(f"{'='*70}")
                
                category_products = []
                current_page = 1
                total_pages = 1
                
                while current_page <= total_pages:
                    variables = {
                        "storeCode": STORE_CODE,
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
                    
                    # Make request using browser context
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
                            print(f"  Total products: {total_count}")
                            print(f"  Total pages: {total_pages}")
                        
                        # Process items
                        for item in items:
                            product = {
                                'sku': item.get('sku', ''),
                                'item_title': item.get('item_title', ''),
                                'retail_price': item.get('retail_price', ''),
                                'sales_size': item.get('sales_size', ''),
                                'sales_uom_description': item.get('sales_uom_description', ''),
                                'inserted_at': timestamp,
                                'store_code': STORE_CODE,
                                'availability': '1',  # Filtered by availability=1
                                'published': '1'
                            }
                            
                            # Get price from price_range if not in retail_price
                            if not product['retail_price'] and 'price_range' in item:
                                try:
                                    price_val = item['price_range']['minimum_price']['final_price']['value']
                                    product['retail_price'] = str(price_val)
                                except:
                                    pass
                            
                            if product['sku']:
                                category_products.append(product)
                        
                        print(f"  Page {current_page}/{total_pages}: {len(items)} products")
                        current_page += 1
                        await asyncio.sleep(0.3)  # Small delay
                    else:
                        print(f"  ✗ No data for page {current_page}")
                        break
                
                all_products.extend(category_products)
                print(f"  ✓ Category complete: {len(category_products)} products")
                print(f"  Running total: {len(all_products)} products\n")
                
                await asyncio.sleep(0.5)
            
            # Remove duplicates
            unique_products = {}
            for p in all_products:
                sku = p['sku']
                if sku not in unique_products:
                    unique_products[sku] = p
            
            products_list = list(unique_products.values())
            
            # Save
            output_file = f"traderjoes_FINAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            fieldnames = ['sku', 'retail_price', 'item_title', 'inserted_at', 'store_code',
                         'availability', 'sales_size', 'sales_uom_description', 'published']
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(products_list)
            
            print(f"\n{'='*70}")
            print(f"✓✓✓ SUCCESS! ✓✓✓")
            print(f"{'='*70}")
            print(f"Total products collected: {len(all_products)}")
            print(f"Unique products: {len(products_list)}")
            print(f"Store code: {STORE_CODE}")
            print(f"Saved to: {output_file}")
            
            with_price = sum(1 for p in products_list if p.get('retail_price'))
            print(f"\nStatistics:")
            print(f"  With prices: {with_price} ({with_price/len(products_list)*100:.1f}%)")
            
            print(f"\nSample products:")
            for p in sorted(products_list, key=lambda x: float(x.get('retail_price') or 999))[:10]:
                if p.get('retail_price'):
                    size = f" ({p['sales_size']} {p['sales_uom_description']})" if p.get('sales_size') else ""
                    print(f"  [{p['store_code']}] {p['sku']}: {p['item_title'][:45]:45} ${p['retail_price']:>6}{size}")
            
            print(f"\n{'='*70}\n")
            
            return output_file
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            await asyncio.sleep(2)
            await browser.close()

if __name__ == "__main__":
    result = asyncio.run(fetch_all_products())
    if result:
        print(f"🎉 Complete! All products saved to: {result}")

