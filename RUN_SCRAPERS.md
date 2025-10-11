# Trader Joe's Product Scraper - How to Run

## Overview
We have created improved scrapers to fetch **thousands of products** with **store-specific pricing and availability**.

### Current Status
- **Old fetch**: 285 products, NO store codes, NO prices
- **Goal**: Get 1000s of products WITH store codes and prices (like sample_latest_data.csv)

## Available Scrapers

### 1. **fetch_graphql_direct.py** (RECOMMENDED TO TRY FIRST)
**Fastest - Direct API queries**

Directly queries the GraphQL API with different approaches:
- Tries pagination to get all products
- Tests multiple query variations
- Attempts store-specific queries for stores: 31, 546, 701, 452, 706

**Run:**
```bash
cd /Users/kaner/tradercpi
python3 fetch_graphql_direct.py
```

**Pros:** 
- Fast (no browser)
- Tests multiple API approaches
- Shows which queries work

**Cons:**
- API may not return prices without proper auth/cookies
- May not get store-specific data if API doesn't support it

---

### 2. **fetch_store_specific.py** (COMPREHENSIVE)
**Most thorough - Browser-based with store codes**

Uses Playwright browser automation to:
- Visit ALL 23 product categories
- Scroll extensively to load ALL products
- Attempt to set store codes (31, 546, 701, 452, 706)
- Capture API responses with pricing

**Dependencies:**
```bash
pip3 install playwright playwright-stealth
python3 -m playwright install chromium
```

**Run:**
```bash
cd /Users/kaner/tradercpi
python3 fetch_store_specific.py
```

**Pros:**
- Most comprehensive
- Gets data exactly as website sees it
- Captures all lazy-loaded products
- Tries all categories

**Cons:**
- Slower (5 stores × 23 categories)
- Browser visible (headless=False to avoid detection)
- May take 30-60 minutes

---

### 3. **fetch_all_categories.py** (EXISTING)
**Your current working scraper**

Visits all categories but doesn't differentiate by store.

**Run:**
```bash
python3 fetch_all_categories.py
```

## Expected Results

### What we want (like sample_latest_data.csv):
```csv
sku,retail_price,item_title,inserted_at,store_code,availability
081523,5.49,"Strawberry Doodle Cookies","2025-06-03 00:00:07",546,1
079514,2.99,"Dark Chocolate Thins","2025-06-03 00:00:07",546,1
```

### Store Codes:
- **31**: New York, NY - Union Square
- **452**: San Francisco, CA
- **546**: Chicago, IL
- **701**: Los Angeles, CA
- **706**: Brooklyn, NY

## Recommended Approach

1. **Start with Quick Test:**
   ```bash
   python3 fetch_graphql_direct.py
   ```
   This will quickly test which API approaches work and save results.

2. **If Direct API doesn't get prices, run comprehensive:**
   ```bash
   python3 fetch_store_specific.py
   ```
   This will take longer but should capture everything.

3. **Check the output:**
   - Look for files like `traderjoes_graphql_direct_YYYYMMDD_HHMMSS.csv`
   - Or `traderjoes_multi_store_YYYYMMDD_HHMMSS.csv`
   - Check how many products have prices and store codes

## Troubleshooting

### If you get only 285 products with no prices:
- The API doesn't provide prices without authentication
- Try the browser-based scrapers instead
- The old data source may have been different

### If getting blocked/403 errors:
- Add longer delays between requests
- Use VPN or different network
- The website may have improved bot detection

### If store codes aren't being captured:
- The website may not expose store inventory via public API
- May need to reverse engineer how the website sets/stores the user's preferred store
- Old data source might have used internal/employee API

## Next Steps

After running scrapers, analyze results:
```bash
# Count products
wc -l traderjoes_*.csv

# Check for prices
awk -F',' 'NR>1 && $2 != "" {count++} END {print count " products with prices"}' traderjoes_*.csv

# Check store codes  
awk -F',' 'NR>1 {print $5}' traderjoes_*.csv | sort -u
```

