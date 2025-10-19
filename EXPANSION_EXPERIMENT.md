# Store Expansion Experiment

**Branch:** `expansion-test`  
**Created:** October 19, 2025  
**Goal:** Test pulling prices from more stores and adding more products

---

## 🎯 Experiment Goals

1. **More Stores:** Test if you can successfully pull data from additional Trader Joe's locations
2. **More Products:** See if you can capture more products per store
3. **Performance:** Check if the scraper can handle larger volumes
4. **Data Quality:** Verify data consistency across more stores

---

## 📍 Available Store Codes

You have **649 valid store codes** in `backend/data/all_discovered_stores.json`

### Current Stores (5)
- Store 31: Los Angeles, CA
- Store 452: Austin, TX
- Store 546: East Village NYC
- Store 701: South Loop Chicago, IL
- Store 706: Hyde Park Chicago, IL

### Potential Expansion Ideas

**More Major Cities:**
- San Francisco area stores
- Seattle area stores
- Boston area stores
- Miami area stores
- Denver area stores

**Regional Coverage:**
- West Coast: More CA, WA, OR stores
- East Coast: More NYC, Boston, DC area
- South: More TX, FL stores
- Midwest: More IL, MN stores

---

## 🔧 Where to Experiment

### 1. Test Single Store First
Edit `backend/scripts/fetch_all_stores.py` to add one store:

```python
# Current stores
STORES = {
    "LA": 31,
    "Austin": 452,
    "East Village NYC": 546,
    "South Loop Chicago": 701,
    "Hyde Park Chicago": 706,
    # Add test store here
    "San Francisco": 123,  # Example (use real store code)
}
```

### 2. Find Store Codes
Check `backend/data/all_discovered_stores.json` for specific store codes:

```bash
# Search for stores in a specific city
cd backend/data
cat all_discovered_stores.json | grep -i "san francisco"
cat all_discovered_stores.json | grep -i "seattle"
```

### 3. Test Run
```bash
# Run the scraper with your new store(s)
python3 backend/scripts/fetch_all_stores.py
```

---

## 📊 Testing Strategy

### Phase 1: Single Store Test (Recommended First)
1. Add 1 new store to the script
2. Run scraper
3. Check output CSV
4. Verify data quality
5. Check runtime (~3 minutes per store expected)

### Phase 2: Regional Test
1. Add 3-5 stores from same region
2. Run scraper
3. Compare pricing across region
4. Look for regional patterns

### Phase 3: Full Expansion
1. Add 10-20 stores nationwide
2. Run scraper
3. Analyze data consistency
4. Check for regional price variations

---

## 🔍 What to Look For

### Data Collection
- ✅ All stores complete successfully
- ✅ ~2,900-3,000 products per store (baseline)
- ✅ Runtime scales linearly (3-5 min per store)
- ⚠️ Any errors or timeouts

### Price Analysis
- Compare prices across new stores
- Look for regional variations
- Identify which products vary by location
- Calculate price ranges

### Product Coverage
- Are all categories represented?
- Any stores missing categories?
- Total unique products across all stores

---

## 📝 Expected Output

### CSV File Format
Your scraper will generate: `traderjoes_ALL_STORES_YYYYMMDD_HHMMSS.csv`

Columns:
- `store_number`
- `item_title`
- `category`
- `retail_price`
- `sku`
- `availability`
- `timestamp`

### Analysis Scripts You Can Create

**Compare Prices Across Stores:**
```python
import pandas as pd

df = pd.read_csv('backend/data/your_new_file.csv')

# Products available in all stores
common = df.groupby('item_title').filter(lambda x: len(x) == num_stores)

# Price variations
variations = common.groupby('item_title')['retail_price'].agg(['min', 'max', 'std'])
print(variations[variations['std'] > 0])
```

**Store Coverage:**
```python
# Products per store
store_counts = df.groupby('store_number')['item_title'].count()
print(store_counts)

# Unique products per store
unique_per_store = df.groupby('store_number')['item_title'].nunique()
print(unique_per_store)
```

---

## ⚡ Performance Notes

### Current Performance (5 Stores)
- **Runtime:** ~15 minutes total
- **Per Store:** ~3 minutes each
- **Output:** ~14,500 records
- **Size:** ~1.1 MB CSV

### Estimated for Expanded Dataset

**10 Stores:**
- Runtime: ~30 minutes
- Records: ~29,000
- Size: ~2.2 MB

**20 Stores:**
- Runtime: ~60 minutes
- Records: ~58,000
- Size: ~4.4 MB

**50 Stores:**
- Runtime: ~2.5 hours
- Records: ~145,000
- Size: ~11 MB

**All 649 Stores:**
- Runtime: ~32 hours (would need optimization)
- Records: ~1.9 million
- Size: ~143 MB

---

## 🚨 Important Considerations

### Rate Limiting
- Current script has delays between requests
- Adding more stores means longer runtime
- Consider running during off-hours
- May want to add more aggressive rate limiting for large batches

### Data Storage
- Large datasets may need database instead of CSV
- Consider using `traderjoes.db` SQLite database
- Index by store_number and item_title for fast queries

### Website Load
- Be respectful of Trader Joe's servers
- Don't run too frequently
- Consider caching/reusing data where possible

---

## 🎯 Recommended First Test

### Start Small: Add 1 West Coast Store

1. **Pick a store** from `all_discovered_stores.json`
   - Example: Store 645 (San Francisco)

2. **Edit the script:**
   ```bash
   code backend/scripts/fetch_all_stores.py
   # Add store to STORES dictionary
   ```

3. **Test run:**
   ```bash
   python3 backend/scripts/fetch_all_stores.py
   ```

4. **Analyze results:**
   - Compare prices with LA store
   - Check product availability
   - Verify data quality

5. **If successful, expand gradually**

---

## 📈 Integration with Web App

Once you have more stores, you can:

1. **Update map.html** to show more cities
2. **Add more shopping personas** for new cities
3. **Show regional price comparisons**
4. **Create "find cheapest location" feature**

---

## 🔄 Getting Back to Main

When you're done experimenting:

```bash
# Save your work
git add -A
git commit -m "Experiment: Testing N stores"

# Switch back to main
git checkout main

# If experiment was successful, merge it
git merge expansion-test

# If you want to discard and start over
git checkout main
git branch -D expansion-test
```

---

## 📚 Resources

- **Store codes:** `backend/data/all_discovered_stores.json`
- **Current scraper:** `backend/scripts/fetch_all_stores.py`
- **Analysis template:** `backend/docs/PRICE_COMPARISON_OLD_VS_NEW.md`

---

**Good luck with your expansion! 🚀**

*This is a safe branch to experiment in. Your main branch and production files in /web are unchanged.*

