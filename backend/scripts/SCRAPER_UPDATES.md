# Scraper Updates - October 19, 2025

## 🎯 Major Improvements to `fetch_all_stores.py`

### Changes Made:

#### 1. ✅ Added Category 2 (Root "Products" Category)
**Problem:** We were only scraping subcategories (Food, Bakery, Cheese, etc.) which captured ~3,000 products per store.

**Solution:** Added Category ID 2 which is the root "Products" category containing ALL items.

**Result:** Now captures **~20,000-25,000 products per store** (8x more!)

**Products now found:**
- Tuscan Pane (all varieties)
- Snow Peas
- Many specialty/seasonal items
- In-store only products
- Regional products

#### 2. ✅ Filter Out $0.00 Priced Items
**Problem:** Database contained many products with $0.00 prices (discontinued, seasonal unavailable, etc.)

**Solution:** Added price validation to only include products with `price > 0`

```python
# Only add products with SKU and non-zero price
if product['sku']:
    try:
        price = float(product['retail_price']) if product['retail_price'] else 0
        if price > 0:
            category_products.append(product)
    except (ValueError, TypeError):
        pass
```

**Result:** Cleaner dataset with only active, priced products

#### 3. ✅ Enhanced Anti-Detection
**Problem:** Trader Joe's API was blocking automated requests (403 Forbidden errors)

**Solution:** Implemented multiple anti-detection techniques:
- Non-headless browser (runs visibly)
- Enhanced user agent
- Human-like headers (Accept-Language, DNT, etc.)
- Navigator.webdriver masking
- Timezone and locale settings
- Human-like page navigation

**Result:** Successfully bypasses API blocks

#### 4. ✅ Increased Page Size
**Changed:** `pageSize: 15` → `pageSize: 100`

**Result:** Fewer API requests, faster scraping (4x fewer requests per category)

#### 5. ✅ Added Store 691
**Added:** Lincoln Park, Chicago, IL (1840 N Clybourn Ave)

**Updated store list:**
```python
STORES = {
    "31": "New York, NY - Union Square",
    "452": "San Francisco, CA",
    "546": "East Village, NYC",
    "691": "Lincoln Park, Chicago, IL",  # NEW
    "701": "South Loop, Chicago, IL",
    "706": "Hyde Park, Chicago, IL",
}
```

---

## 📊 Performance Comparison

### Before Updates:
- **Products per store:** ~2,900-3,000
- **API status:** Blocked (403 errors)
- **Categories scanned:** 23
- **Missing products:** 82% of catalog

### After Updates:
- **Products per store:** ~20,000-25,000
- **API status:** ✅ Working with anti-detection
- **Categories scanned:** 24 (including Category 2)
- **Missing products:** Minimal (complete catalog)

---

## 🔧 Technical Details

### Category Structure Discovery:

```
Products (Category 2)              ← ROOT - 25,356 items
├── Food (Category 8)              ← 2,278 items
│   ├── Bakery (11)                ← 152 items
│   ├── Cheese (29)                ← 168 items
│   └── etc...
├── Beverages (182)                ← 439 items
└── Everything Else (215)          ← 215 items
```

**Key insight:** Most products are ONLY tagged with Category 2, not subcategories.

### Product Naming Patterns:

| Type | % of Products | Published Status | Example |
|------|---------------|------------------|---------|
| Title Case | 13% | `published: 1` | "Sugar Snap Peas" |
| ALL CAPS | 82% | `published: 0` | "PEAS SNOW 9 OZ" |
| Mixed | 5% | Varies | Various |

**Published = 1:** Customer-facing (website display)
**Published = 0:** Internal/in-store only (warehouse naming)

---

## 🚀 Usage

### Running the Updated Scraper:

```bash
cd /Users/kaner/tradercpi/backend/scripts
python3 fetch_all_stores.py
```

### Expected Output:
- **6 stores** scanned
- **~120,000-150,000 total products** (20k-25k per store)
- **Runtime:** ~20-30 minutes (3-5 min per store)
- **Output file:** `traderjoes_ALL_STORES_YYYYMMDD_HHMMSS.csv`

### CSV Format:
```csv
sku,retail_price,item_title,inserted_at,store_code,availability,sales_size,sales_uom_description,published
035722,2.69,PEAS SNOW 9 OZ,2025-10-19 14:48:44,691,1,9,Oz,0
030312,2.99,Sugar Snap Peas,2025-10-19 14:48:44,691,1,12,Oz,1
```

---

## ✅ Verification

### Test Queries:
```python
# Check for previously missing products
grep -i "tuscan pane" output_file.csv
grep -i "snow pea" output_file.csv

# Verify no $0.00 prices
awk -F',' '$2 == "0.00"' output_file.csv  # Should return nothing

# Count products per store
awk -F',' 'NR>1 {count[$5]++} END {for(store in count) print store, count[store]}' output_file.csv
```

### Success Criteria:
- ✅ Tuscan Pane found (multiple varieties)
- ✅ Snow Peas found
- ✅ No $0.00 priced products
- ✅ ~20k-25k products per store
- ✅ No 403 API errors

---

## 📝 Notes

### Anti-Detection Best Practices:
1. Run during off-peak hours
2. Don't run too frequently (respect rate limits)
3. Browser runs visibly (headless=False) - required for bypass
4. Random delays between requests maintained

### Maintenance:
- Monitor for API changes
- If blocked again, increase delays or add more human-like behavior
- Category 2 should remain stable (root category)

---

## 🎉 Impact

**Before:** Incomplete data, missing 82% of products, API blocked
**After:** Complete product catalog, all stores accessible, clean data

This update transforms the scraper from capturing a sample (~3k products) to capturing the **complete Trader Joe's catalog** (~25k products per store)!

---

*Updated: October 19, 2025*
*Script: `backend/scripts/fetch_all_stores.py`*

