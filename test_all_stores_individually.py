#!/usr/bin/env python3
"""
Test store codes 1-650 INDIVIDUALLY using the proven working method
"""
import asyncio
import json
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

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

async def test_individual_store(page, code):
    """Test a single store code using the proven method"""
    variables = {
        "storeCode": str(code),
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
            if total > 0:
                return {'code': str(code), 'products': total, 'valid': True}
        
        return None
    except:
        return None

async def discover_all():
    """Test codes 1-650 individually"""
    print("="*70)
    print("COMPREHENSIVE INDIVIDUAL STORE CODE TESTING")
    print("Testing codes 1-650 using proven working method")
    print("="*70)
    
    async with async_playwright() as p:
        # Use visible browser - headless seems to fail
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
            print("✓ Session ready\n")
            
            valid_stores = []
            start_code = 1
            end_code = 651
            
            print(f"Testing {end_code - start_code} store codes...")
            print("This will take approximately 45-60 minutes.\n")
            print("Valid stores will be displayed immediately when found.\n")
            print("="*70)
            
            for code in range(start_code, end_code):
                result = await test_individual_store(page, code)
                
                if result:
                    valid_stores.append(result)
                    print(f"✓ FOUND Store {code:>3d}: {result['products']:>4d} products")
                
                # Progress indicator every 50 codes
                if code % 50 == 0:
                    print(f"  ... tested {code}/{end_code-1} codes, found {len(valid_stores)} valid stores")
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.1)
            
            print(f"\n{'='*70}")
            print(f"DISCOVERY COMPLETE!")
            print(f"{'='*70}")
            print(f"Codes tested: {end_code - start_code}")
            print(f"Valid stores found: {len(valid_stores)}\n")
            
            # Save results
            with open('all_discovered_stores.json', 'w') as f:
                json.dump(valid_stores, f, indent=2)
            print(f"✓ Saved to all_discovered_stores.json\n")
            
            # Display all
            print("ALL VALID STORE CODES:")
            print("="*70)
            for store in sorted(valid_stores, key=lambda x: int(x['code'])):
                print(f"  Store {store['code']:>3s}: {store['products']:>4d} products")
            
            print(f"\n{'='*70}")
            print(f"You can fetch from {len(valid_stores)} stores!")
            print(f"{'='*70}\n")
            
            # Create Python list for easy copy
            codes = [s['code'] for s in sorted(valid_stores, key=lambda x: int(x['code']))]
            print(f"Store codes as list:")
            print(f"VALID_STORES = {codes}\n")
            
            return valid_stores
            
        finally:
            await browser.close()

if __name__ == "__main__":
    stores = asyncio.run(discover_all())
    print(f"\n🎉 Discovery complete! Found {len(stores)} valid Trader Joe's stores")

