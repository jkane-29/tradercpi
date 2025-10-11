#!/usr/bin/env python3
"""
Fetch COMPLETE inventory including out-of-stock items
Gets ~1,900 products per store instead of ~1,500
"""
import asyncio
import csv
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

# Store code to fetch
STORE_CODE = "691"  # Chicago Lincoln Park - change as needed

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

# Modified query - NO availability filter!
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

async def fetch_complete():
    """Fetch ALL items including out-of-stock"""
    print("="*70)
    print(f"FETCHING COMPLETE INVENTORY - STORE {STORE_CODE}")
    print("Including in-stock AND out-of-stock items")
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
            await page.goto('https://www.traderjoes.com/', wait_until='networkidle')
            await asyncio.sleep(2)
            print("✓ Session established\n")
            
            all_products = []
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for cat_idx, category in enumerate(CATEGORIES, 1):
                current_page = 1
                total_pages = 1
                category_products = []
                
                while current_page <= total_pages:
                    variables = {
                        "storeCode": STORE_CODE,
                        "published": "1",  # Only published, but ANY availability
                        "categoryId": int(category['id']),
                        "currentPage": current_page,
                        "pageSize": 15
                    }
                    
                    payload = {
                        "operationName": "SearchProducts",
                        "variables": variables,
                        "query": GRAPHQL_QUERY
                    }
                    
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
                            print(f"[{cat_idx:2d}/23] {category['name']:20s} [{total_count:4d} products, {total_pages:3d} pages] ", end='', flush=True)
                        
                        for item in items:
                            product = {
                                'sku': item.get('sku', ''),
                                'item_title': item.get('item_title', ''),
                                'retail_price': item.get('retail_price', ''),
                                'sales_size': item.get('sales_size', ''),
                                'sales_uom_description': item.get('sales_uom_description', ''),
                                'inserted_at': timestamp,
                                'store_code': STORE_CODE,
                                'availability': item.get('availability', ''),  # Now capturing this!
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
                
                all_products.extend(category_products)
                print(f"✓ ({len(category_products)} collected)")
            
            # Remove duplicates
            unique = {}
            for p in all_products:
                if p['sku'] not in unique:
                    unique[p['sku']] = p
            
            products_list = list(unique.values())
            
            # Save
            output_file = f"traderjoes_COMPLETE_STORE_{STORE_CODE}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            fieldnames = ['sku', 'retail_price', 'item_title', 'inserted_at', 'store_code',
                         'availability', 'sales_size', 'sales_uom_description', 'published']
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(products_list)
            
            print(f"\n{'='*70}")
            print(f"✓ COMPLETE INVENTORY - STORE {STORE_CODE}")
            print(f"{'='*70}")
            print(f"Total unique products: {len(products_list)}")
            print(f"Saved to: {output_file}")
            
            # Statistics
            in_stock = sum(1 for p in products_list if p.get('availability') == '1')
            out_stock = sum(1 for p in products_list if p.get('availability') == '0')
            unknown = len(products_list) - in_stock - out_stock
            with_price = sum(1 for p in products_list if p.get('retail_price'))
            
            print(f"\nBreakdown:")
            print(f"  In stock (availability=1): {in_stock}")
            print(f"  Out of stock (availability=0): {out_stock}")
            print(f"  Unknown availability: {unknown}")
            print(f"  With prices: {with_price} ({with_price/len(products_list)*100:.1f}%)")
            
            # Find stir fry
            stir_fry = [p for p in products_list if 'stir fry veggie blend' in p['item_title'].lower()]
            if stir_fry:
                print(f"\nStir Fry Veggie Blend found:")
                for item in stir_fry:
                    avail_status = "IN STOCK" if item['availability'] == '1' else "OUT OF STOCK"
                    print(f"  SKU {item['sku']}: ${item['retail_price']} - {avail_status}")
            
            print(f"\n{'='*70}\n")
            
        finally:
            await browser.close()

asyncio.run(fetch_complete())

EOFPYTHON
