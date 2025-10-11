# Monthly Inflation Tracker - Setup Guide

## 🎯 **Purpose**

Automatically scrape Trader Joe's prices from 5 stores on the **1st of each month** and append to a historical CSV for inflation tracking.

---

## ✅ **Quick Setup**

```bash
cd /Users/kaner/tradercpi
./setup_monthly_cron.sh
```

This sets up a cron job to run automatically on the 1st of each month at 2:00 AM.

---

## 📊 **How It Works**

### **Stores Tracked:**
- 31 (NYC)
- 452 (SF)
- 546 (Chicago)
- 701 (LA)
- 706 (Brooklyn)

### **Schedule:**
- **When:** 1st of every month at 2:00 AM
- **Duration:** ~90 minutes
- **Output:** Appends to `traderjoes_inflation_tracker.csv`

### **Data Flow:**
```
Month 1 (Nov 2025): ~7,500 records added
Month 2 (Dec 2025): ~7,500 more records appended
Month 3 (Jan 2026): ~7,500 more records appended
...
After 12 months: ~90,000 records with full price history!
```

---

## 📁 **File Structure**

```
traderjoes_inflation_tracker.csv    ← Main historical file (grows each month)
backups/
  ├── traderjoes_snapshot_2025-11-01.csv
  ├── traderjoes_snapshot_2025-12-01.csv
  └── traderjoes_snapshot_2026-01-01.csv
logs/
  ├── monthly_fetch_202511.log
  ├── monthly_fetch_202512.log
  └── monthly_fetch_202601.log
```

---

## 🔧 **Manual Testing**

Test the scraper before the cron runs:

```bash
cd /Users/kaner/tradercpi
python3 fetch_monthly_inflation.py
```

This will:
1. Fetch from 5 stores (~90 minutes)
2. Append to `traderjoes_inflation_tracker.csv`
3. Create backup in `backups/`
4. Show you the results

---

## 📈 **Using the Data**

### **Track Inflation:**

```python
import pandas as pd

# Load historical data
df = pd.read_csv('traderjoes_inflation_tracker.csv')

# Convert date
df['month'] = pd.to_datetime(df['inserted_at']).dt.to_period('M')

# Calculate price changes over time for specific product
bananas = df[df['sku'] == '048053']  # Bananas
banana_prices = bananas.groupby(['month', 'store_code'])['retail_price'].mean()

# Calculate month-over-month inflation
inflation = banana_prices.pct_change() * 100
```

### **Compare Stores:**

```python
# Average prices by store and month
avg_by_store = df.groupby(['month', 'store_code'])['retail_price'].mean()

# Find most/least expensive markets
store_comparison = df.groupby('store_code')['retail_price'].agg(['mean', 'median'])
```

### **Track Specific Items:**

```python
# Get specific item history
item_sku = '033372'  # Organic Sweet Potatoes
item_history = df[df['sku'] == item_sku][['inserted_at', 'store_code', 'retail_price']]
```

---

## 🔍 **Monitoring**

### **Check if cron is scheduled:**
```bash
crontab -l | grep fetch_monthly
```

### **View last run:**
```bash
ls -lt logs/*.log | head -1
tail -50 logs/monthly_fetch_*.log
```

### **Check data file:**
```bash
wc -l traderjoes_inflation_tracker.csv
tail -20 traderjoes_inflation_tracker.csv
```

---

## ⚙️ **Configuration**

### **Change Schedule:**
Edit cron job:
```bash
crontab -e
```

Cron format: `MIN HOUR DAY MONTH DAYOFWEEK`
- Current: `0 2 1 * *` = 2:00 AM on 1st of month
- Change to 1st at 3 AM: `0 3 1 * *`
- Change to 15th at 2 AM: `0 2 15 * *`

### **Change Stores:**
Edit `fetch_monthly_inflation.py` line 15:
```python
CORE_STORES = {
    "31": "NYC",
    "100": "Different store",  # Add/change stores
    # ...
}
```

---

## 🛠️ **Troubleshooting**

### **Cron didn't run:**
1. Check cron is enabled: `crontab -l`
2. Check logs: `ls logs/`
3. Test manually: `python3 fetch_monthly_inflation.py`

### **Script failed:**
1. Check log file: `tail -100 logs/monthly_fetch_YYYYMM.log`
2. Verify playwright installed: `python3 -c "import playwright; print('OK')"`
3. Test connection: `curl https://www.traderjoes.com`

### **Data looks wrong:**
1. Check file: `tail -20 traderjoes_inflation_tracker.csv`
2. Verify dates: `awk -F',' '{print $4}' traderjoes_inflation_tracker.csv | sort -u`
3. Count per month: `awk -F',' 'NR>1 {print substr($4,1,7)}' traderjoes_inflation_tracker.csv | sort | uniq -c`

---

## 📊 **Expected Growth**

| Month | Records | File Size |
|-------|---------|-----------|
| 1 | 7,500 | ~500 KB |
| 3 | 22,500 | ~1.5 MB |
| 6 | 45,000 | ~3 MB |
| 12 | 90,000 | ~6 MB |
| 24 | 180,000 | ~12 MB |

---

## 🔄 **Maintenance**

### **Monthly (automatic):**
- Cron runs on 1st at 2 AM
- Data appends to CSV
- Backup created

### **Quarterly (manual):**
- Review logs for errors
- Check data quality
- Analyze trends

### **Yearly (manual):**
- Archive old backups
- Analyze annual trends
- Update scraper if website changes

---

## 🎯 **Use Cases**

1. **Personal Inflation Tracking**
   - Track your grocery bill over time
   - Compare stores in your area
   - Budget planning

2. **Economic Analysis**
   - Regional inflation rates
   - Product category trends
   - Geographic price dispersion

3. **Research**
   - Retail pricing studies
   - Cost-of-living research
   - Economic indicators

---

## ⚠️ **Important Notes**

1. **Computer must be on** - Cron only runs if Mac is awake
2. **Browser visible** - Script uses headless=False to avoid detection
3. **Network required** - Needs internet connection
4. **Takes ~90 minutes** - Plan accordingly for 2 AM runs

### **Alternative: Use launchd (Mac-specific)**

For better reliability on Mac, consider using `launchd` instead of cron:
- Runs even if you were asleep at 2 AM
- Better logging
- More reliable on macOS

(Let me know if you want launchd setup!)

---

## ✅ **Verification**

After first run, verify:

```bash
# Check historical file exists
ls -lh traderjoes_inflation_tracker.csv

# Check backup created
ls -lh backups/

# View recent data
tail -20 traderjoes_inflation_tracker.csv

# Count records
wc -l traderjoes_inflation_tracker.csv
```

---

## 🎊 **Benefits**

- ✅ **Automatic** - Set and forget
- ✅ **Historical** - Builds over time
- ✅ **Comprehensive** - 5 major metros
- ✅ **Timestamped** - Track changes precisely
- ✅ **Backed up** - Monthly snapshots saved

**Perfect for long-term inflation analysis!** 📈

