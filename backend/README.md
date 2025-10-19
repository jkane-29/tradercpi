# Backend - Trader Joe's CPI Tracker

This directory contains all backend scripts, data files, and documentation for the Trader Joe's Price Index project.

**⚠️ DO NOT DEPLOY THIS DIRECTORY TO PRODUCTION**

---

## 📁 Directory Structure

```
backend/
├── scripts/           # Data collection and automation scripts
│   ├── fetch_all_stores.py          # Main scraper (5 stores)
│   ├── fetch_monthly_inflation.py   # Monthly automation script
│   └── setup_monthly_cron.sh        # Cron job setup
│
├── data/              # Raw data and analysis files
│   ├── all_stores master.csv        # Latest dataset (Oct 2025)
│   ├── traderjoes-dump-3.csv        # Historical data (2.4M rows)
│   ├── price_comparison_by_store.csv
│   ├── items_with_price_variations.csv
│   ├── traderjoes.db                # SQLite database
│   └── all_discovered_stores.json   # 649 store codes
│
└── docs/              # Technical documentation
    ├── PROJECT_STRUCTURE.md
    ├── PRICE_COMPARISON_OLD_VS_NEW.md
    ├── PRICE_ANALYSIS_REPORT.md
    ├── MONTHLY_TRACKING_README.md
    ├── WEB_APP_STATUS.md
    └── CLEANUP_SUMMARY.md
```

---

## 🔧 Scripts

### fetch_all_stores.py
Main scraper for collecting data from 5 target stores:
- LA (Store 31)
- Austin (Store 452)
- East Village NYC (Store 546)
- South Loop Chicago (Store 701)
- Hyde Park Chicago (Store 706)

**Usage:**
```bash
python3 backend/scripts/fetch_all_stores.py
```

**Runtime:** ~15 minutes  
**Output:** Dated CSV file with all products from all stores

### fetch_monthly_inflation.py
Automated monthly scraper designed for cron jobs.

**Usage:**
```bash
python3 backend/scripts/fetch_monthly_inflation.py
```

**Features:**
- Appends to `traderjoes_inflation_tracker.csv`
- Creates automatic backups
- Designed for 1st-of-month automation

### setup_monthly_cron.sh
Sets up automated monthly data collection.

**Usage:**
```bash
bash backend/scripts/setup_monthly_cron.sh
```

---

## 📊 Data Files

### Primary Dataset
**`all_stores master.csv`** (1.1 MB)
- 14,454 records
- 5 stores, ~2,900-3,000 products each
- Date: October 11, 2025
- Includes in-stock and out-of-stock items

### Historical Data
**`traderjoes-dump-3.csv`** (163 MB)
- 2.4M+ rows
- Same 5 stores over time
- Used for price trend analysis

### Analysis Files
**`price_comparison_by_store.csv`**
- 1,224 products available in all 5 stores
- Side-by-side price comparison

**`items_with_price_variations.csv`**
- Only 18 products with regional price variations
- 98.5% of products have identical pricing nationwide

### Reference Data
**`all_discovered_stores.json`**
- Complete list of 649 valid Trader Joe's store codes
- Used for potential national dataset expansion

---

## 📈 Key Findings

### Price Consistency
- **98.5%** of products have identical prices across all stores
- Only **18 out of 1,224** common products show price variation
- Maximum variation: $1.00

### Historical Change
- Old data: 16.8% of products varied (321 items)
- Current data: 1.5% of products vary (18 items)
- Result: **94% reduction in price variations**

### Store Rankings
- **Cheapest:** Austin (13 times)
- **Most Expensive:** East Village NYC (15 times)

### Category Insights
- Most Expensive: Meat (~$5.80 avg)
- Least Expensive: Snacks (~$3.51 avg)

---

## 🔄 Updating Web App Data

To regenerate JSON files for the web app:

```bash
cd /Users/kaner/tradercpi/web
python3 create_basket_essentials.py
```

This reads from `backend/data/all_stores master.csv` and generates:
- `dropdown_items.json`
- `featured_items.json`
- `basket_essentials.json`
- `price_data.json`

---

## 📚 Documentation

See `/backend/docs` for detailed documentation:
- **PROJECT_STRUCTURE.md** - Complete project overview
- **PRICE_COMPARISON_OLD_VS_NEW.md** - Key findings report
- **PRICE_ANALYSIS_REPORT.md** - Current price analysis
- **MONTHLY_TRACKING_README.md** - Automation guide

---

## 🛠️ Development Workflow

1. **Collect Data**
   ```bash
   python3 backend/scripts/fetch_all_stores.py
   ```

2. **Analyze Data**
   ```bash
   # Use your preferred data analysis tools
   # SQLite database available at backend/data/traderjoes.db
   ```

3. **Update Web App**
   ```bash
   cd web
   python3 create_basket_essentials.py
   ```

4. **Test Locally**
   ```bash
   cd web
   python3 -m http.server 8000
   ```

---

## 🚀 Production Separation

- **Backend files** (this directory): Stay on development machine
- **Web files** (`/web` directory): Deploy to tj-prices.com
- Clear separation between data collection and presentation

---

## 📝 Notes

- Backend data is NOT needed for web app to function
- Web app uses pre-generated static JSON files
- Backend scripts require Python 3 and appropriate packages
- Database file (`traderjoes.db`) is for analysis only

---

For deployment instructions, see `/DEPLOYMENT.md` in project root.

