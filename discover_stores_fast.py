#!/usr/bin/env python3
"""
Fast store discovery - test many codes quickly
"""
import asyncio
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

async def test_stores_batch(page, codes):
    """Test multiple store codes"""
    valid = []
    
    for code in codes:
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
                    valid.append({'code': str(code), 'products': total})
                    print(f"  ✓ Store {code}: {total} products")
            
            await asyncio.sleep(0.05)
        except:
            pass
    
    return valid

async def quick_discovery():
    """Quick discovery of valid stores"""
    print("="*70)
    print("RAPID STORE CODE DISCOVERY")
    print("="*70)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Visible to avoid blocks
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
            
            all_valid = []
            
            # Test strategic ranges
            test_batches = [
                (range(1, 150), "1-149"),
                (range(150, 300), "150-299"),
                (range(300, 450), "300-449"),
                (range(450, 600), "450-599"),
                (range(600, 750), "600-749"),
                (range(750, 900), "750-899"),
            ]
            
            for codes, label in test_batches:
                print(f"\nTesting {label}...")
                valid = await test_stores_batch(page, codes)
                all_valid.extend(valid)
                print(f"  Found {len(valid)} valid stores in this range")
            
            print(f"\n{'='*70}")
            print(f"TOTAL VALID STORES FOUND: {len(all_valid)}")
            print(f"{'='*70}\n")
            
            for store in sorted(all_valid, key=lambda x: int(x['code'])):
                print(f"  {store['code']:>3s}: {store['products']:>4d} products")
            
            # Save
            import json
            with open('discovered_stores.json', 'w') as f:
                json.dump(all_valid, f, indent=2)
            
            print(f"\n✓ Saved to discovered_stores.json")
            
            return all_valid
            
        finally:
            await asyncio.sleep(3)
            await browser.close()

if __name__ == "__main__":
    stores = asyncio.run(quick_discovery())
    print(f"\n🎉 Found {len(stores)} valid stores!")

