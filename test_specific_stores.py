#!/usr/bin/env python3
"""
Test specific store codes that are likely to be valid
Based on common TJ locations
"""
import asyncio
import json
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

# Store codes to test - based on research and patterns
# Major metro areas likely to have stores
TEST_STORES = [
    # Known working
    "31", "452", "546", "701", "706",
    
    # Major cities - test common patterns
    # California (lots of stores)
    "133", "134", "135", "136", "137",  # San Diego area
    "192", "193", "194",  # Orange County
    "640", "641", "642", "643",  # Bay Area
    "702", "703", "704", "705",  # LA area
    
    # New York area
    "32", "33", "34", "35",  # NYC area
    "707", "708", "709",  # NY suburbs
    
    # Chicago area  
    "545", "547", "548", "549",  # Chicago suburbs
    
    # Other major metros
    "73", "74", "75",  # Boston area
    "113", "114", "115",  # Seattle
    "166", "167", "168",  # Portland
    "514", "515", "516",  # Austin/Texas
    "607", "608", "609",  # Denver
    "729", "730", "731",  # Phoenix
    
    # Round numbers often used
    "100", "200", "300", "400", "500", "600", "700", "800"
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

async def test_store(page, store_code):
    """Test if a store code is valid"""
    variables = {
        "storeCode": store_code,
        "availability": "1",
        "published": "1",
        "categoryId": 8,  # Food category
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
            total_count = result['data']['products'].get('total_count', 0)
            items = result['data']['products'].get('items', [])
            
            if total_count > 0:
                # Get a sample product to confirm
                sample = items[0]['item_title'] if items else ''
                return {
                    'code': store_code,
                    'valid': True,
                    'products': total_count,
                    'sample': sample
                }
        
        return None
        
    except:
        return None

async def quick_discovery():
    """Quick test of likely store codes"""
    print("="*70)
    print("QUICK STORE CODE DISCOVERY - Testing Likely Codes")
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
            print("Establishing session...")
            await page.goto('https://www.traderjoes.com/', wait_until='networkidle')
            await asyncio.sleep(2)
            print("✓ Session established\n")
            
            valid_stores = []
            
            print(f"Testing {len(TEST_STORES)} store codes...\n")
            
            for i, code in enumerate(TEST_STORES, 1):
                result = await test_store(page, code)
                
                if result:
                    valid_stores.append(result)
                    print(f"  [{i:3d}] ✓ Store {code:>3s}: {result['products']:4d} products - {result['sample'][:40]}")
                else:
                    if i % 10 == 0:
                        print(f"  [{i:3d}] ... tested {i} codes, found {len(valid_stores)} valid")
                
                await asyncio.sleep(0.15)
            
            print(f"\n{'='*70}")
            print(f"FOUND {len(valid_stores)} VALID STORES")
            print(f"{'='*70}\n")
            
            # Save results
            with open('quick_valid_stores.json', 'w') as f:
                json.dump(valid_stores, f, indent=2)
            
            print("Valid store codes:")
            for store in sorted(valid_stores, key=lambda x: int(x['code'])):
                print(f"  {store['code']:>3s}: {store['products']:4d} products")
            
            print(f"\n✓ Saved to quick_valid_stores.json")
            print(f"\nYou can fetch from these {len(valid_stores)} stores!")
            
            return valid_stores
            
        finally:
            await browser.close()

if __name__ == "__main__":
    stores = asyncio.run(quick_discovery())

