#!/usr/bin/env python3
"""
Discover ALL available Trader Joe's store codes
Tests store codes to see which ones return valid data
"""
import asyncio
import json
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

# Known stores from old data
KNOWN_STORES = ["31", "452", "546", "701", "706"]

# Additional store codes to test (based on common TJ locations)
# TJ has ~500+ stores, but most likely have numeric codes 1-999
TEST_RANGES = [
    range(1, 100),      # Test 1-99
    range(100, 200),    # Test 100-199
    range(200, 300),    # Test 200-299
    range(400, 500),    # Test 400-499
    range(500, 600),    # Test 500-599
    range(700, 800),    # Test 700-799
]

GRAPHQL_QUERY = """
query SearchProducts($categoryId: String, $currentPage: Int, $pageSize: Int, $storeCode: String, $availability: String = "1", $published: String = "1") {
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

async def test_store_code(page, store_code):
    """Test if a store code returns data"""
    variables = {
        "storeCode": str(store_code),
        "availability": "1",
        "published": "1",
        "categoryId": 8,  # Food category
        "currentPage": 1,
        "pageSize": 5  # Just get a few items to test
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
            total_count = result['data']['products'].get('total_count', 0)
            items = result['data']['products'].get('items', [])
            
            if total_count > 0 or items:
                return {
                    'code': store_code,
                    'valid': True,
                    'product_count': total_count,
                    'sample_items': len(items)
                }
        
        return {'code': store_code, 'valid': False}
        
    except Exception as e:
        return {'code': store_code, 'valid': False, 'error': str(e)}

async def discover_stores():
    """Discover all valid store codes"""
    print("="*70)
    print("DISCOVERING ALL TRADER JOE'S STORE CODES")
    print("="*70)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Run headless for speed
        context = await browser.new_context(
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
            
            valid_stores = []
            
            # Test known stores first
            print("Testing KNOWN store codes:")
            print("-" * 70)
            for store_code in KNOWN_STORES:
                result = await test_store_code(page, store_code)
                if result['valid']:
                    valid_stores.append(result)
                    print(f"  ✓ Store {store_code}: {result['product_count']} products")
                else:
                    print(f"  ✗ Store {store_code}: Invalid")
                await asyncio.sleep(0.2)
            
            print(f"\n✓ Found {len(valid_stores)} known valid stores\n")
            
            # Now test ranges to discover new stores
            print("Discovering additional store codes...")
            print("-" * 70)
            print("(Testing ranges: 1-99, 100-199, 200-299, 400-499, 500-599, 700-799)")
            print("This may take a few minutes...\n")
            
            tested = 0
            for test_range in TEST_RANGES:
                for store_code in test_range:
                    # Skip if already tested
                    if str(store_code) in KNOWN_STORES:
                        continue
                    
                    result = await test_store_code(page, store_code)
                    tested += 1
                    
                    if result['valid']:
                        valid_stores.append(result)
                        print(f"  🆕 FOUND NEW STORE {store_code}: {result['product_count']} products!")
                    
                    # Progress indicator
                    if tested % 50 == 0:
                        print(f"  ... tested {tested} codes, found {len(valid_stores)} valid stores")
                    
                    await asyncio.sleep(0.1)  # Small delay to avoid rate limiting
            
            print(f"\n{'='*70}")
            print(f"DISCOVERY COMPLETE")
            print(f"{'='*70}")
            print(f"Total codes tested: {tested + len(KNOWN_STORES)}")
            print(f"Valid stores found: {len(valid_stores)}\n")
            
            # Save results
            results_file = 'valid_store_codes.json'
            with open(results_file, 'w') as f:
                json.dump(valid_stores, f, indent=2)
            print(f"✓ Saved to {results_file}\n")
            
            # Display all valid stores
            print("ALL VALID STORE CODES:")
            print("-" * 70)
            for store in sorted(valid_stores, key=lambda x: int(x['code'])):
                print(f"  Store {store['code']:>3}: {store['product_count']:>4} products")
            
            print(f"\n{'='*70}\n")
            
            return valid_stores
            
        finally:
            await browser.close()

if __name__ == "__main__":
    stores = asyncio.run(discover_stores())
    print(f"✓ Discovered {len(stores)} valid store codes")
    print(f"\nYou can now fetch data from all {len(stores)} stores!")

