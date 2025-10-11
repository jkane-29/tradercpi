#!/usr/bin/env python3
"""
Fetch ALL Trader Joe's products by visiting each category page
"""
import asyncio
import json
import csv
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

CATEGORIES = [
    "/home/products/category/food-8",
    "/home/products/category/bakery-11",
    "/home/products/category/cheese-29",
    "/home/products/category/dairy-and-eggs-44",
    "/home/products/category/dips-sauces-and-dressings-59",
    "/home/products/category/fresh-prepared-foods-80",
    "/home/products/category/from-the-freezer-95",
    "/home/products/category/cool-desserts-107",
    "/home/products/category/fresh-fruits-and-veggies-113",
    "/home/products/category/meat-seafood-and-plant-based-122",
    "/home/products/category/fish-seafood-131",
    "/home/products/category/for-the-pantry-137",
    "/home/products/category/snacks-and-sweets-167",
    "/home/products/category/beverages-182",
    "/home/products/category/non-dairy-bev-191",
    "/home/products/category/milk-cream-47",
    "/home/products/category/sodas-mixers-197",
    "/home/products/category/wine-beer-liquor-200",
    "/home/products/category/flowers-plants-203",
    "/home/products/category/everything-else-215",
    "/home/products/category/household-essentials-218",
    "/home/products/category/for-the-face-body-221",
    "/home/products/category/pet-stuff-224",
]

async def fetch_all_categories():
    """Fetch products from all categories"""
    print("Starting comprehensive category fetch...")
    print(f"Timestamp: {datetime.now()}")
    print(f"Categories to fetch: {len(CATEGORIES)}\n")
    
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(
            headless=False,  # Visible browser avoids detection
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US'
        )
        
        page = await context.new_page()
        
        # Apply stealth
        stealth_config = Stealth()
        await stealth_config.apply_stealth_async(page)
        
        # Storage for API responses
        all_graphql_responses = []
        
        async def handle_response(response):
            """Intercept GraphQL responses"""
            if '/api/graphql' in response.url:
                try:
                    data = await response.json()
                    if 'data' in data and 'products' in data.get('data', {}):
                        items = data['data']['products'].get('items', [])
                        if items:
                            all_graphql_responses.append(data)
                except:
                    pass
        
        page.on('response', handle_response)
        
        try:
            # Visit homepage first to establish session
            print("Loading homepage to establish session...")
            await page.goto('https://www.traderjoes.com/', wait_until='networkidle', timeout=60000)
            await asyncio.sleep(2)
            print(f"✓ Session established\n")
            
            # Visit each category
            for i, category_url in enumerate(CATEGORIES, 1):
                category_name = category_url.split('/')[-1]
                print(f"[{i}/{len(CATEGORIES)}] Fetching: {category_name}")
                
                responses_before = len(all_graphql_responses)
                
                try:
                    full_url = f"https://www.traderjoes.com{category_url}"
                    await page.goto(full_url, wait_until='networkidle', timeout=60000)
                    await asyncio.sleep(3)
                    
                    # Extensive scrolling to load ALL products in category
                    last_response_count = len(all_graphql_responses)
                    no_new_data_count = 0
                    
                    for scroll in range(100):  # Up to 100 scrolls per category
                        await page.evaluate('window.scrollBy(0, 1200)')
                        await asyncio.sleep(1)
                        
                        # Check if we got new data
                        current_count = len(all_graphql_responses)
                        if current_count > last_response_count:
                            last_response_count = current_count
                            no_new_data_count = 0
                        else:
                            no_new_data_count += 1
                        
                        # Stop if no new data after 15 scrolls
                        if no_new_data_count >= 15:
                            break
                        
                        # Progress indicator every 10 scrolls
                        if (scroll + 1) % 10 == 0:
                            print(f"    Scrolled {scroll + 1} times, total responses: {current_count}")
                    
                    responses_after = len(all_graphql_responses)
                    new_responses = responses_after - responses_before
                    print(f"  ✓ Captured {new_responses} API responses from this category")
                    
                except Exception as e:
                    print(f"  ✗ Error: {e}")
                
                # Small delay between categories
                await asyncio.sleep(1)
            
            print(f"\n✓ Finished! Total API responses: {len(all_graphql_responses)}")
            
            # Save all responses
            with open('all_categories_responses.json', 'w') as f:
                json.dump(all_graphql_responses, f, indent=2)
            print(f"✓ Saved responses to all_categories_responses.json")
            
            # Parse and save products
            all_products = []
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for resp in all_graphql_responses:
                if 'data' in resp and 'products' in resp['data']:
                    items = resp['data']['products'].get('items', [])
                    for product in items:
                        all_products.append({
                            'sku': product.get('sku', ''),
                            'retail_price': product.get('retail_price', ''),
                            'item_title': product.get('item_title', ''),
                            'inserted_at': timestamp,
                            'store_code': product.get('store_code', ''),
                            'availability': product.get('availability', '')
                        })
            
            # Remove duplicates
            unique_products = {}
            for product in all_products:
                sku = product['sku']
                if sku and sku not in unique_products:
                    unique_products[sku] = product
            
            products_list = list(unique_products.values())
            print(f"\n✓ Total unique products: {len(products_list)}")
            
            # Count products with prices
            with_price = sum(1 for p in products_list if p['retail_price'])
            print(f"  Products with prices: {with_price}")
            print(f"  Products without prices: {len(products_list) - with_price}")
            
            # Save to CSV
            if products_list:
                output_file = f"traderjoes_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=['sku', 'retail_price', 'item_title', 'inserted_at', 'store_code', 'availability'])
                    writer.writeheader()
                    writer.writerows(products_list)
                
                print(f"\n✓✓✓ SUCCESS! Saved {len(products_list)} products to {output_file} ✓✓✓")
                
                # Show sample
                print("\nSample products with prices:")
                count = 0
                for product in products_list:
                    if product['retail_price'] and count < 10:
                        print(f"  {product['sku']}: {product['item_title'][:50]} - ${product['retail_price']}")
                        count += 1
                
                return output_file
            else:
                print("\n✗ No products found")
                return None
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            await browser.close()

if __name__ == "__main__":
    result = asyncio.run(fetch_all_categories())
    if result:
        print(f"\n🎉 Data fetch complete! New file: {result}")

