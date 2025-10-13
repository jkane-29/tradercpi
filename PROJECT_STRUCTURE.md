# Trader Joe's CPI Tracker - Project Structure

**Last Updated:** October 12, 2025

---

## 📊 Main Data Files

### Current Data
- **`all_stores master.csv`** (1.1 MB)
  - Latest complete dataset: 14,454 records
  - 5 stores: LA (31), Austin (452), East Village NYC (546), South Loop Chicago (701), Hyde Park Chicago (706)
  - Date: October 11, 2025
  - Includes: in-stock + out-of-stock items, ~2,900-3,000 products per store

### Historical Data
- **`traderjoes-dump-3.csv`** (163 MB)
  - Historical dataset: 2.4M+ rows
  - Same 5 stores over time
  - Used for price comparison and trend analysis

### Analysis Files
- **`price_comparison_by_store.csv`** (94 KB)
  - 1,224 products available in all 5 stores
  - Side-by-side price comparison
  - Shows Min, Max, Range, Average for each product

- **`items_with_price_variations.csv`** (1.4 KB)
  - Only 18 products with regional price variations
  - 98.5% of products have identical pricing nationwide

---

## 📝 Analysis Reports

### Main Reports
- **`PRICE_COMPARISON_OLD_VS_NEW.md`** (6.5 KB)
  - **KEY REPORT**: Compares historical vs current pricing
  - Shows 94% reduction in price variations over time
  - Details Trader Joe's shift to standardized pricing

- **`PRICE_ANALYSIS_REPORT.md`** (4.4 KB)
  - Current price analysis by store and category
  - Store rankings, category breakdowns
  - Methodology and findings

### Documentation
- **`MONTHLY_TRACKING_README.md`** (5.9 KB)
  - Instructions for monthly inflation tracking
  - Cron job setup guide
  - Data interpretation tips

- **`README.md`** (2.9 KB)
  - Project overview and setup

---

## 🤖 Active Scrapers

### Production Scripts
- **`fetch_all_stores.py`**
  - Main scraper for 5 stores
  - Fetches all 23 categories
  - Removes duplicates
  - ~15 minutes runtime

- **`fetch_monthly_inflation.py`**
  - Monthly automated scraper
  - Appends to `traderjoes_inflation_tracker.csv`
  - Designed for cron job (runs 1st of each month)
  - Creates dated backups

### Setup
- **`setup_monthly_cron.sh`**
  - Shell script to configure cron job
  - Sets up monthly automation

---

## 📚 Reference Data

- **`all_discovered_stores.json`** (43 KB)
  - Complete list of 649 valid Trader Joe's store codes
  - Used for national dataset project (separate repo)

---

## 🖼️ Assets

### `images/` Directory
Contains all logos, banners, and visualization assets:
- Trader Joe's brand logos (black, white, red variants)
- Banner images
- Font files (TraderJoes-JYrx.otf)
- Charts and visualizations
- **11 files total** (~5.5 MB)

---

## 🌐 Web Application

### `web/` Directory
Contains the web dashboard and related files:
- **HTML Files:**
  - `index.html` - Main dashboard
  - `dashboard.html` - Dashboard view
  - `map.html` - Store map visualization
  - `template.html` - Template file
- **Directories:**
  - `css/` - Stylesheets
  - `js/` - JavaScript files
  - `old_site/` - Previous version (archived)
- **Scripts:**
  - `create_basket_essentials.py` - Generates basket data for web app
  - `data_loader.js` - Client-side data loading

---

## 🔄 Related Projects

### National Dataset Repository
- **Location:** `traderjoes-national-dataset/` (separate git repo)
- **Purpose:** Full 649-store scrape for comprehensive national analysis
- **Status:** Set up and ready for full fetch
- **GitHub:** `traderjoes-national-dataset`

---

## 📂 Ignored Files

See `.gitignore` for excluded files:
- `traderjoes_inflation_tracker.csv` (generated monthly)
- Log files (`*.log`)
- Backup directories
- Python cache

---

## 🎯 Key Findings Summary

### Price Consistency
- **98.5%** of products have identical prices across all 5 stores
- Only **18 out of 1,224** common products show price variation
- Maximum variation: $1.00

### Historical Change
- **Old data:** 16.8% of products varied (321 items)
- **Current data:** 1.5% of products vary (18 items)
- **Result:** 94% reduction in price variations

### Store Rankings (Current)
**Cheapest:** Austin (13 times)  
**Most Expensive:** East Village NYC (15 times)

### Category Insights
- **Most Expensive:** Meat (~$5.80 avg)
- **Least Expensive:** Snacks (~$3.51 avg)
- **Biggest Spread:** Beverages (South Loop Chicago $1+ higher than others)

---

## 🚀 Next Steps

1. **Monthly Tracking:** Cron job runs automatically on 1st of each month
2. **National Dataset:** 649-store fetch available in separate repo
3. **Inflation Analysis:** Use `all_stores master.csv` as baseline for monthly comparisons

---

## 💡 Usage

### Quick Analysis
```bash
# View current data
head all_stores\ master.csv

# Check price variations
cat items_with_price_variations.csv

# Read key findings
cat PRICE_COMPARISON_OLD_VS_NEW.md
```

### Run Monthly Scraper
```bash
python3 fetch_monthly_inflation.py
```

### Run Full 5-Store Scraper
```bash
python3 fetch_all_stores.py
```

---

*For detailed methodology and findings, see PRICE_COMPARISON_OLD_VS_NEW.md*
