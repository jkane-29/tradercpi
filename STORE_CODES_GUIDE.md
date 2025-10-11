# Trader Joe's Store Codes - Complete Guide

## 🏪 Store Code System

Trader Joe's uses numeric store codes to identify each physical location. Based on analysis of your old data and current scraping, here's what we know:

---

## ✅ Confirmed Valid Store Codes

### From Your Old Data (traderjoes-dump-3.csv):

| Code | Location | Region | Records | Status |
|------|----------|--------|---------|--------|
| **31** | New York, NY - Union Square | Northeast | 573,381 | 🔄 Fetching now |
| **452** | San Francisco, CA | West Coast | 569,841 | ⏳ Queued |
| **546** | Chicago, IL | Midwest | 568,503 | ⏳ Queued |
| **701** | Los Angeles, CA | West Coast | 660,369 | ✅ Complete (1,552 products) |
| **706** | Brooklyn, NY | Northeast | 1,850 | ⏳ Queued |

### Current Scraper Default:
- **701** (Los Angeles) - Auto-selected by website, probably based on IP geolocation

---

## 🌍 How Many Stores Could You Get?

### Total Trader Joe's Stores:
Trader Joe's has **~560 stores nationwide** (as of 2024)

### Possible Store Codes:
Based on the pattern (numeric codes), you could potentially query:
- **All 560+ stores** if you can find their codes
- Codes likely range from **1-999**
- Not all numbers are valid (gaps exist)

### How to Discover Them:

**Option 1: Run the Discovery Tool**
```bash
python3 discover_all_stores.py
```
This will:
- Test store codes 1-999
- Find all valid ones
- Show product count for each
- Save results to `valid_store_codes.json`
- **Time**: ~30-60 minutes (tests hundreds of codes)

**Option 2: Use Trader Joe's Store Locator**
Visit: https://locations.traderjoes.com/
- Search by city/zip
- Note the store numbers
- Some stores display their code on the website

**Option 3: Extract from Website Data**
The TJ website might have a store list API endpoint we could query

---

## 🗺️ Store Code Patterns (Analysis)

From old data, codes seem to follow patterns:

### Geographic Clustering:
- **1-99**: Early/original stores (East Coast?)
  - 31 = New York
- **400-499**: California/West Coast
  - 452 = San Francisco
- **500-599**: Midwest/Central
  - 546 = Chicago
- **700-799**: California/West Coast
  - 701 = Los Angeles
  - 706 = Brooklyn (possibly renumbered)

### Hypothesis:
Codes might be assigned chronologically (opening order) or by region.

---

## 📊 Product Variation By Store

### What We're Seeing:
- **LA (701)**: 1,552 products
- **NYC (31)**: Fetching now, expecting ~1,550-1,600

### Why Differences?
1. **Regional products** - Some items only in certain regions
2. **Seasonal availability** - Different climates = different seasons
3. **Inventory levels** - Some stores have more SKUs
4. **Local preferences** - Stores stock what sells locally

### Expected Unique Products:
If you fetch all 5 stores:
- **Per store**: ~1,500-1,600 products
- **Total records**: ~7,500-8,000
- **Unique SKUs**: ~1,700-2,000 (many products in multiple stores)

---

## 🚀 Fetching Strategies

### Strategy 1: Core 5 Stores (CURRENT)
**Stores**: 31, 452, 546, 701, 706
**Time**: 90 minutes (currently running)
**Coverage**: Major metro areas
**Result**: ~7,500 records

### Strategy 2: Major Metro Expansion
Add stores from top 20 cities:
- Seattle, Portland, Boston, Austin, Denver, etc.
**Time**: 4-6 hours
**Result**: ~30,000 records

### Strategy 3: Complete National Coverage
Discover and fetch ALL 560+ stores
**Time**: 2-3 days
**Result**: ~850,000+ records (560 stores × 1,500 products)

### Strategy 4: Regional Focus
Pick one region (e.g., California)
Find all CA store codes
**Time**: 2-4 hours
**Result**: 50,000-100,000 records

---

## 🔍 How to Find Specific Store Codes

### Method 1: Trader Joe's Website
1. Go to https://locations.traderjoes.com/
2. Search for your city
3. Click on a store
4. Check URL or page source for store number

### Method 2: Run Discovery Script
```bash
python3 discover_all_stores.py
```
Tests codes 1-999 and shows which are valid

### Method 3: Manual Testing
Edit `fetch_final_working.py`:
```python
STORE_CODE = "123"  # Test any code
```
Run and see if it returns products

---

## 📝 Store Code Reference

### Confirmed Valid Codes:

| Code | City | State | Products |
|------|------|-------|----------|
| 31 | New York | NY | ~1,550 |
| 452 | San Francisco | CA | ~1,550 |
| 546 | Chicago | IL | ~1,550 |
| 701 | Los Angeles | CA | 1,552 ✓ |
| 706 | Brooklyn | NY | ~1,550 |

### To Add More:
1. Run `discover_all_stores.py` to find codes
2. Edit `fetch_all_stores.py` STORES dictionary:
   ```python
   STORES = {
       "31": "New York, NY",
       "123": "Your New Store",  # Add here
       # ... etc
   }
   ```
3. Run `python3 fetch_all_stores.py`

---

## ⚡ Quick Reference

### Current Status:
- ✅ **Committed to git** - Your work is saved!
- 🔄 **Multi-store fetch running** - Getting all 5 stores
- ⏰ **ETA**: ~60 more minutes

### When Complete:
You'll have:
- **~7,500-8,000 records** across 5 stores
- **~1,600-1,700 unique products**
- **Store-specific pricing** for each location
- **Complete dataset** for CPI analysis

### Next Actions:
1. Wait for multi-store fetch to complete
2. Push the final dataset to git
3. Optionally run store discovery to find more codes
4. Use data in your CPI tracker!

---

## 🎯 Answer to Your Question

### "How many store codes could I get?"

**Theoretical Maximum**: **560+ stores** (all US Trader Joe's locations)

**Practical Targets**:
- **5 stores**: What we're doing now (1-2 hours)
- **20 stores**: Major metros (4-6 hours)  
- **50 stores**: Regional coverage (12-24 hours)
- **500+ stores**: Complete national (2-3 days)

**Current**: Using the 5 stores from your old data (31, 452, 546, 701, 706)

**To discover more**: Run `discover_all_stores.py` - it will test hundreds of codes and tell you which ones are valid!

---

**Bottom line**: You can get as many stores as you want! Each store takes ~15-20 minutes to fully fetch. The scraper is proven to work, so it's just a matter of running it for more store codes.

