#!/usr/bin/env python3
"""
Comprehensive store code discovery for Trader Joe's
Tests store codes systematically to find ALL valid ones
"""
import asyncio
import json
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

# The WORKING GraphQL query (from our successful scrapers)
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

async def test_store_code(page, code):
    """Test if a store code returns products"""
    variables = {
        "storeCode": str(code),
        "availability": "1",
        "published": "1",
        "categoryId": 8,  # Food category (biggest category)
        "currentPage": 1,
        "pageSize": 5
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
            total = result['data']['products'].get('total_count', 0)
            items = result['data']['products'].get('items', [])
            
            if total > 0 and items:
                return {'code': str(code), 'products': total, 'valid': True}
        
        return None
    except:
        return None

async def discover_all_stores():
    """Discover all valid Trader Joe's store codes"""
    print("="*70)
    print("COMPREHENSIVE TRADER JOE'S STORE CODE DISCOVERY")
    print("="*70)
    print("Testing store codes to find ALL valid stores...")
    print("This may take 30-60 minutes.\n")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Headless for speed
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
            
            valid_stores = []
            
            # Test ranges strategically
            # Based on patterns: 1-999, focusing on common patterns
            test_ranges = [
                (1, 100, "1-99"),
                (100, 200, "100-199"),
                (200, 300, "200-299"),
                (300, 400, "300-399"),
                (400, 500, "400-499"),
                (500, 600, "500-599"),
                (600, 700, "600-699"),
                (700, 800, "700-799"),
                (800, 900, "800-899"),
                (900, 1000, "900-999"),
            ]
            
            total_tested = 0
            
            for start, end, label in test_ranges:
                print(f"\nTesting range {label}...")
                print("-" * 70)
                
                range_start_count = len(valid_stores)
                
                for code in range(start, end):
                    result = await test_store_code(page, code)
                    total_tested += 1
                    
                    if result:
                        valid_stores.append(result)
                        print(f"  ✓ FOUND Store {code}: {result['products']} products")
                    
                    # Progress every 25 codes
                    if total_tested % 25 == 0:
                        print(f"  ... tested {total_tested} total, found {len(valid_stores)} valid stores")
                    
                    await asyncio.sleep(0.05)  # Small delay
                
                found_in_range = len(valid_stores) - range_start_count
                print(f"  Range {label}: Found {found_in_range} valid stores")
            
            print(f"\n{'='*70}")
            print(f"DISCOVERY COMPLETE!")
            print(f"{'='*70}")
            print(f"Total codes tested: {total_tested}")
            print(f"Valid stores found: {len(valid_stores)}\n")
            
            # Save results
            results_file = 'all_valid_stores.json'
            with open(results_file, 'w') as f:
                json.dump(valid_stores, f, indent=2)
            print(f"✓ Saved to {results_file}\n")
            
            # Display all valid stores
            print("ALL VALID STORE CODES:")
            print("="*70)
            for store in sorted(valid_stores, key=lambda x: int(x['code'])):
                print(f"  Store {store['code']:>3s}: {store['products']:>4d} products in Food category")
            
            # Create quick reference
            store_codes = [s['code'] for s in valid_stores]
            print(f"\n{'='*70}")
            print(f"Quick copy list of store codes:")
            print(f"{'='*70}")
            print(f"STORE_CODES = {json.dumps(store_codes)}")
            
            print(f"\n{'='*70}")
            print(f"✓ You can fetch from {len(valid_stores)} different stores!")
            print(f"{'='*70}\n")
            
            return valid_stores
            
        finally:
            await browser.close()

if __name__ == "__main__":
    stores = asyncio.run(discover_all_stores())
    print(f"\n🎉 Discovery complete! Found {len(stores)} valid Trader Joe's store codes")

