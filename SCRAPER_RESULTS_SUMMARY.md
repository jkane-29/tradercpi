# Trader Joe's Scraper - Results & Analysis

## Executive Summary

### ✅ What We Achieved
- **286 unique products** captured from current Trader Joe's website
- **99.3% have prices** (284/286 products)
- **Full product details**: SKU, title, price, size, availability
- **Automated scraping** via browser interception of GraphQL API

### ❌ Current Limitations
- **NO store codes** - API doesn't provide store-specific data
- **Only ~286 products** - Not the thousands expected
- **No store differentiation** - Same catalog regardless of location attempt

---

## Data Quality Comparison

### Old Data (traderjoes-dump-3.csv)
```
- Total records: 2,431,213
- Unique products per store: ~160-170
- Store codes: 31, 452, 546, 701, 706
- Date range: 2024-01-21 to 2025-06-03
- Has: prices, availability, store codes
```

### New Data (October 2025)
```
- Total products: 286
- With prices: 284 (99.3%)
- Store codes: NONE (not in API)
- Single snapshot: 2025-10-10
- Has: prices, availability, sizes
```

---

## Technical Findings

### API Structure
The Trader Joe's website uses a GraphQL API at `/api/graphql` that returns:

**Available Fields:**
- ✅ `sku` - Product SKU
- ✅ `item_title` - Product name
- ✅ `retail_price` - Price as string (e.g., "3.79")
- ✅ `price_range` - Structured price object
- ✅ `availability` - "1" or "0"
- ✅ `sales_size` - Size as number
- ✅ `sales_uom_description` - Unit (e.g., "Oz")
- ✅ `published` - 1 or 0
- ✅ `category_hierarchy` - Product categories
- ❌ `store_code` - NOT PROVIDED

### Why Store Codes Are Missing

The public API does not include store codes in responses. Possible reasons:
1. **Generic catalog** - Website shows same products to all users
2. **Location-based filtering** - Server filters by IP but doesn't expose store code
3. **Different API** - Old data may have used internal/employee API
4. **Historical accumulation** - Old data collected over months with timestamps

### Direct API Access Blocked

Direct HTTP requests to the GraphQL API return **403 Forbidden**:
```
Access Denied
You don't have permission to access "http://www.traderjoes.com/api/graphql"
```

This requires browser-based scraping to:
1. Establish proper cookies/session
2. Pass anti-bot checks
3. Get proper headers/tokens

---

## Why Only 286 Products?

### Possible Explanations:

1. **Website Limitation**
   - The public product catalog may only show a curated subset
   - Full inventory might not be exposed online

2. **Location Filtering**
   - Products shown based on user's location
   - Different locations see different products
   - But store code not exposed

3. **Lazy Loading Limits**
   - Website may have pagination or scroll limits
   - Some products only appear in search, not category browse

4. **Seasonal Products**
   - Current snapshot vs historical data
   - Old data accumulated products over time

5. **Product Types**
   - Some products may not be in online catalog
   - Store-only items not listed

---

## Sample Data

### Products WITH Prices (284 total)
```csv
sku,retail_price,item_title,sales_size,sales_uom
081428,0.79,"Chocolate Vanilla Creme Joe-Joe's 4 pk",1.758,Oz
078613,0.99,"Greek YogurtHoney Made with Whole Milk",5.3,Oz
093474,1.29,"Hass Avocado",1,Each
080876,1.99,"Antipasto Stick Prosciutto Wrapped",1.5,Oz
051403,2.49,"Solid Light Yellowfin Tuna in Olive Oil",,
080590,2.49,"Organic Silken Tofu",,
082268,3.49,"Ketchup Flavored Lattice Potato Chips",,
081786,3.79,"Harvest Vegetable Hash Egg White Bites",4.2,Oz
...
```

### Products WITHOUT Prices (2 total)
```
080602: Risotto Semplice
079429: Sweet & Spicy Rice Cracker Mix
```

---

## Strategies to Get More Products

### Option 1: Multi-Location Scraping
Run scraper from different geographic locations:
- Use VPN to different cities
- Run from actual different locations
- Associate each run with a store code manually

**Pros:** May get location-specific products
**Cons:** Still won't have store codes in data

### Option 2: Historical Accumulation
Run scraper daily/weekly over time:
- Build database of products over months
- Capture seasonal items as they appear
- Track price changes

**Pros:** Comprehensive over time
**Cons:** Takes months to build

### Option 3: Deep Crawling
Visit every product detail page:
- Extract links to all products
- Visit each individual product page
- May expose more data

**Pros:** Might find more products
**Cons:** Very slow, may get blocked

### Option 4: Search-Based Discovery
Use site search with various terms:
- Search for common food terms
- Discover products not in category pages
- Extract from search results

**Pros:** May find hidden products
**Cons:** Need comprehensive search term list

### Option 5: Accept Limitations
Use current 286-product dataset:
- Focus on the products we can get
- Manually add store codes if needed
- Supplement with other data sources

---

## Files Created

### Scrapers
1. `fetch_graphql_direct.py` - Direct API queries (blocked)
2. `fetch_store_specific.py` - Browser-based multi-store scraper
3. `fetch_all_categories.py` - Category-based scraper (working)
4. `reprocess_responses.py` - Extract all data from JSON responses

### Data Files
1. `traderjoes_reprocessed_YYYYMMDD_HHMMSS.csv` - 286 products with prices
2. `all_categories_responses.json` - Raw API responses (26 responses)
3. `all_api_responses.json` - Additional API captures

### Documentation
1. `RUN_SCRAPERS.md` - How to run the scrapers
2. `SCRAPER_RESULTS_SUMMARY.md` - This file

---

## Recommendations

### For Immediate Use
1. **Use the 286-product dataset** - It has good price coverage
2. **Manually assign store codes** - Based on your use case
3. **Run from multiple locations** - If geographic diversity needed

### For Long-Term Solution
1. **Run scraper weekly** - Build historical database
2. **Track changes over time** - Prices, availability, new products
3. **Supplement with manual data** - For store-specific info

### For Maximum Coverage
1. **Investigate old data source** - How was traderjoes-dump-3.csv created?
2. **Contact Trader Joe's** - Official API or data partnership?
3. **Community crowdsourcing** - Multiple users in different locations

---

## Conclusion

The current public Trader Joe's website API provides:
- ✅ **Good data quality** - 99.3% have prices
- ✅ **Reliable extraction** - Automated via browser
- ❌ **Limited quantity** - Only ~286 products visible
- ❌ **No store differentiation** - Store codes not available

The old dataset with 2.4M records and store codes was likely:
- Historical accumulation over months
- Using different/internal data source
- Multiple store locations captured separately

**Next Steps:**
1. Determine if 286 products is sufficient for your use case
2. If more needed, implement one of the strategies above
3. Consider what the actual source of old data was

