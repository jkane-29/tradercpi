# Trader Joe's Price Index

An interactive web application that tracks inflation across different cities and shopping archetypes, inspired by Riley Walz's playful data-driven projects and the clean design of FRED (Federal Reserve Economic Data).

**Live Site:** [tj-prices.com](https://tj-prices.com) 🚀

---

## 🏗️ Project Structure

```
tradercpi/
├── web/                    # 🌐 PRODUCTION - Deploy this to tj-prices.com
│   ├── index.html          # Main entry point
│   ├── dashboard.html      # City dashboard
│   ├── map.html           # Interactive US map
│   ├── css/               # Styles
│   ├── js/                # JavaScript
│   ├── images/            # Assets
│   └── *.json            # Data files
│
├── backend/               # 🔧 BACKEND - Keep on development machine
│   ├── scripts/          # Data collection scripts
│   ├── data/             # Raw data and databases
│   └── docs/             # Technical documentation
│
├── README.md             # This file
└── DEPLOYMENT.md         # Deployment guide
```

**Important:** Only the `/web` directory should be deployed to production. See `DEPLOYMENT.md` for details.

---

## 🎯 User Flow

1. **Splash Screen** - Red Trader Joe's branding with 2-second auto-transition
2. **Interactive Map** - Select from Austin, Chicago, NYC, or LA
3. **City Dashboard** - View shopping archetypes specific to selected city
4. **Receipt Display** - Realistic Trader Joe's receipts with inflation data

---

## ✨ Features

### Multi-City Experience
- **4 Major Cities:** Austin, Chicago (2 locations), NYC, Los Angeles
- **City-Specific Branding:** UT/UChicago/NYU/UCLA references
- **Local Context:** Austin ISD/CPS/NYC DOE/LAUSD for teacher archetype

### 5 Shopping Personas Per City
1. **Grad Student** - Ramen, frozen meals, cheap wine
2. **Teacher** - Breakfast items, healthy lunches, coffee
3. **Family of 4** - Kid-friendly snacks, family meals
4. **Fed Chair** - Premium items, economist basket
5. **CPI Comparison** - Standard basket vs. Federal Reserve data

### Authentic Details
- ✅ Realistic Trader Joe's receipt format
- ✅ Actual SKU numbers from product database
- ✅ Accurate tax calculations by state
- ✅ Real pricing data from 5 stores
- ✅ Inflation tracking over time

### Design
- 🎨 Trader Joe's red (#d41e36) color scheme
- 📱 Mobile-responsive design
- 🗺️ Proper US map with accurate state outlines
- ✨ Smooth transitions and hover effects
- 🎭 FRED-inspired clean data presentation
- 🎪 Riley Walz-inspired playful UX

---

## 🚀 Quick Start

### For Users
Visit **tj-prices.com** to use the live application.

### For Local Development
```bash
cd web/
python3 -m http.server 8000
open http://localhost:8000
```

### For Deployment
See detailed instructions in `DEPLOYMENT.md`

---

## 📊 Data

The web app uses pre-generated static JSON files from our backend data collection:

- **Source Data:** 5 Trader Joe's stores across 4 cities
- **Products:** ~3,000 products per store
- **Updated:** Monthly (automated)
- **Coverage:** October 2025 baseline with historical comparisons

### Key Findings
- **98.5%** of products have identical prices nationwide
- Only **18 out of 1,224** products show regional variation
- **94% reduction** in price variations compared to historical data

See `/backend/docs/PRICE_COMPARISON_OLD_VS_NEW.md` for detailed analysis.

---

## 🔧 Backend Tools

Backend scripts for data collection are located in `/backend`:

```bash
# Collect data from all 5 stores
python3 backend/scripts/fetch_all_stores.py

# Run monthly update
python3 backend/scripts/fetch_monthly_inflation.py

# Set up automated monthly collection
bash backend/scripts/setup_monthly_cron.sh
```

See `/backend/README.md` for complete backend documentation.

---

## 📁 Repository Organization

### `/web` - Production Files
Everything needed for the live website:
- HTML pages
- CSS styles
- JavaScript functionality
- Images and fonts
- Data JSON files

**Deploy this directory to tj-prices.com**

### `/backend` - Development Tools
Backend infrastructure (NOT for production):
- Data collection scripts
- Raw datasets (CSV, SQLite)
- Analysis and documentation
- Automation tools

**Keep this on your development machine**

---

## 🌐 Deployment

The site is deployed at **tj-prices.com** using static hosting.

**Quick Deploy:**
```bash
# Using Netlify
netlify deploy --dir=web --prod

# Using Vercel
vercel --prod web
```

For complete deployment instructions, DNS setup, and troubleshooting, see `DEPLOYMENT.md`.

---

## 🎨 Technical Stack

- **Frontend:** Pure HTML, CSS, JavaScript (no frameworks)
- **Data:** Static JSON files generated from backend
- **Hosting:** Static site hosting (Netlify/Vercel recommended)
- **Backend:** Python scrapers using Playwright
- **Database:** SQLite for local analysis

---

## 📈 Future Enhancements

- [ ] Custom basket builder functionality
- [ ] API endpoint for real-time data
- [ ] Historical inflation trend charts
- [ ] More cities and regional variations
- [ ] Social sharing of inflation baskets
- [ ] Export/print receipt functionality
- [ ] Monthly automated data updates via GitHub Actions

---

## 📚 Documentation

- **`DEPLOYMENT.md`** - Complete deployment guide for tj-prices.com
- **`/backend/README.md`** - Backend scripts and data documentation
- **`/backend/docs/`** - Technical documentation and analysis reports

---

## 🧹 Project Status

**Last Cleanup:** October 19, 2025

The project has been fully audited and reorganized:
- ✅ Removed duplicate files
- ✅ Separated production (`/web`) from backend (`/backend`)
- ✅ Cleaned up test files and empty directories
- ✅ Created comprehensive deployment documentation
- ✅ Ready for production deployment

---

## 📞 About

A data-driven exploration of price consistency and inflation tracking at Trader Joe's stores across America.

**Inspired by:**
- Riley Walz's creative data projects
- FRED's clean economic data presentation
- The Federal Reserve's CPI methodology

**Data Collection:** October 2025  
**Baseline:** 5 stores, 4 cities, 15,000+ price points

---

**Ready to deploy! 🎉** See `DEPLOYMENT.md` for next steps.
