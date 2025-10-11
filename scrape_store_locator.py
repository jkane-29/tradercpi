#!/usr/bin/env python3
"""
Scrape Trader Joe's store locator to find actual store codes
"""
import asyncio
from playwright.async_api import async_playwright

async def find_store_codes():
    """Scrape the TJ store locator for store numbers/codes"""
    print("="*70)
    print("SCRAPING TRADER JOE'S STORE LOCATOR")
    print("="*70)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            print("\nLoading store locator...")
            await page.goto('https://locations.traderjoes.com/', wait_until='networkidle')
            await asyncio.sleep(3)
            
            print("✓ Page loaded\n")
            print("Analyzing page structure...")
            
            # Try to find state links
            states = await page.query_selector_all('a[href*="/locations/"]')
            print(f"Found {len(states)} location links\n")
            
            if states:
                print("Sample links:")
                for i, state in enumerate(states[:10]):
                    href = await state.get_attribute('href')
                    text = await state.inner_text()
                    print(f"  {text}: {href}")
            
            # Try to find store pages
            print("\nLooking for store detail pages...")
            
            # Visit California (lots of stores)
            print("\nVisiting California stores...")
            ca_link = await page.query_selector('a[href*="california"]')
            if ca_link:
                await ca_link.click()
                await asyncio.sleep(3)
                
                # Find individual stores
                store_links = await page.query_selector_all('a[href*="/stores/"]')
                print(f"Found {len(store_links)} California stores\n")
                
                if store_links:
                    print("Sample CA stores:")
                    for i, link in enumerate(store_links[:5]):
                        href = await link.get_attribute('href')
                        text = await link.inner_text()
                        print(f"  {text}")
                        print(f"    URL: {href}")
                        
                        # Try to visit one store page
                        if i == 0:
                            print(f"\n    Visiting store page to find code...")
                            await link.click()
                            await asyncio.sleep(3)
                            
                            # Look for store number/code in page
                            content = await page.content()
                            
                            # Check URL
                            url = page.url
                            print(f"    Store URL: {url}")
                            
                            # Look for patterns
                            if 'store' in url:
                                parts = url.split('/')
                                print(f"    URL parts: {parts}")
                            
                            # Search page for number patterns
                            print(f"    Searching page for 'store number', 'store code', etc...")
                            
                            # Go back
                            await page.go_back()
                            await asyncio.sleep(2)
            
            print("\n\nKeeping browser open for inspection...")
            await asyncio.sleep(10)
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(find_store_codes())

