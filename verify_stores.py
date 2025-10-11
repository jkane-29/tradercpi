#!/usr/bin/env python3
"""
Verify our known stores work and understand the query pattern
"""
import asyncio
import json
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

KNOWN_STORES = ["31", "452", "546", "701", "706"]

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
      retail_price
    }
    total_count
  }
}
"""

async def verify():
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
            
            print("\nTesting KNOWN working stores:\n")
            
            for code in KNOWN_STORES:
                variables = {
                    "storeCode": code,
                    "availability": "1",
                    "published": "1",
                    "categoryId": 8,
                    "currentPage": 1,
                    "pageSize": 5
                }
                
                payload = {
                    "operationName": "SearchProducts",
                    "variables": variables,
                    "query": GRAPHQL_QUERY
                }
                
                print(f"Testing store {code}...")
                print(f"  Payload: {json.dumps(variables, indent=4)}")
                
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
                
                print(f"  Response keys: {list(result.keys())}")
                
                if 'data' in result:
                    if 'products' in result['data']:
                        total = result['data']['products'].get('total_count', 0)
                        items = len(result['data']['products'].get('items', []))
                        print(f"  ✓ SUCCESS: {total} total products, got {items} items")
                    else:
                        print(f"  ✗ No 'products' in data")
                        print(f"  Data: {result.get('data', {})}")
                else:
                    print(f"  ✗ No 'data' in response")
                    if 'errors' in result:
                        print(f"  Errors: {result['errors']}")
                
                print()
                await asyncio.sleep(1)
            
        finally:
            await asyncio.sleep(3)
            await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())

