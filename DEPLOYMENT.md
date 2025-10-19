# Deployment Guide for tj-prices.com

**Last Updated:** October 19, 2025  
**Domain:** tj-prices.com  
**Status:** Ready for Deployment ✅

---

## 📦 What to Deploy

Deploy **ONLY** the `/web` directory to your hosting provider. This directory contains all production-ready files.

```
web/
├── index.html              # Main entry point
├── dashboard.html          # Dashboard page
├── map.html               # Store map visualization
├── template.html          # Legacy template (can be removed)
├── data_loader.js         # Data loading utilities
├── create_basket_essentials.py  # Data generation script
├── css/
│   └── styles.css         # All styles
├── js/
│   └── app.js            # JavaScript functionality
├── images/               # All logos, banners, fonts
├── *.json               # Data files for the app
└── old_site/            # Archived version (can be removed)
```

---

## 🚀 Deployment Options

### Option 1: Static Site Hosting (Recommended)

**Netlify** (Easiest)
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy from project root
cd /Users/kaner/tradercpi
netlify deploy --dir=web --prod
```

**Vercel**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from project root
cd /Users/kaner/tradercpi
vercel --prod web
```

**GitHub Pages**
```bash
# Push web directory to gh-pages branch
git subtree push --prefix web origin gh-pages
```

### Option 2: Traditional Web Hosting

Upload the contents of the `/web` directory via FTP/SFTP to your hosting provider's public_html or www directory.

**Popular Providers:**
- SiteGround
- Bluehost
- HostGator
- DreamHost

---

## 🔧 Pre-Deployment Checklist

- [x] Remove duplicate files from root
- [x] Organize backend scripts into `/backend`
- [x] All production files in `/web` directory
- [ ] Update any hardcoded localhost URLs
- [ ] Test all functionality locally
- [ ] Optimize images for web (if needed)
- [ ] Set up custom domain (tj-prices.com)
- [ ] Configure SSL certificate (auto with Netlify/Vercel)

---

## 🌐 Domain Configuration

### DNS Settings for tj-prices.com

**For Netlify:**
1. Go to Netlify Dashboard → Domain Settings
2. Add custom domain: `tj-prices.com`
3. Configure DNS:
   - A Record: `75.2.60.5`
   - CNAME for www: `your-site.netlify.app`

**For Vercel:**
1. Go to Vercel Dashboard → Domains
2. Add domain: `tj-prices.com`
3. Follow DNS configuration instructions

**For Traditional Hosting:**
1. Point A record to hosting provider's IP
2. Point CNAME for www to main domain

---

## 📊 Data Updates

The web app currently uses static JSON files generated from the backend data.

### Updating Data
```bash
# Run from project root
cd /Users/kaner/tradercpi/web
python3 create_basket_essentials.py
```

This regenerates:
- `dropdown_items.json`
- `featured_items.json`
- `basket_essentials.json`
- `price_data.json`

### Automated Updates (Future)
Consider setting up:
1. GitHub Actions to regenerate data monthly
2. API endpoint to serve live data
3. Webhook to trigger rebuilds on data changes

---

## 🧹 Optional Cleanup for Production

Before deploying, you can optionally remove:

```bash
cd web/
rm -rf old_site/           # Remove archived version
rm template.html           # Remove legacy template
rm create_basket_essentials.py  # Keep in backend only
```

---

## 🔒 Security Notes

- ✅ No sensitive data in web files
- ✅ No API keys or credentials
- ✅ All data is pre-generated static JSON
- ⚠️ Backend directory (`/backend`) should NOT be deployed
- ⚠️ Database file (`traderjoes.db`) stays on backend only

---

## 📱 Testing Production Build

Test locally before deploying:

```bash
# Start local server
cd /Users/kaner/tradercpi/web
python3 -m http.server 8000

# Open in browser
open http://localhost:8000
```

Test all features:
- [ ] Splash screen loads and transitions
- [ ] Map displays correctly
- [ ] City selection works
- [ ] Shopping archetypes display
- [ ] Receipts generate properly
- [ ] Mobile responsive design
- [ ] All images load
- [ ] Links work correctly

---

## 🎯 Post-Deployment

1. **Verify Domain:** Visit https://tj-prices.com
2. **Test All Pages:** Check index, map, dashboard
3. **Mobile Test:** Verify responsive design
4. **Performance:** Run Lighthouse audit
5. **Analytics:** Set up Google Analytics (optional)
6. **Monitor:** Set up uptime monitoring (optional)

---

## 📈 Future Enhancements

- [ ] Set up automated data updates via GitHub Actions
- [ ] Add API endpoint for real-time data
- [ ] Implement caching strategy
- [ ] Add meta tags for social sharing
- [ ] Set up sitemap.xml
- [ ] Add robots.txt
- [ ] Configure CDN for faster loading

---

## 🆘 Troubleshooting

**404 Errors:**
- Ensure all paths are relative (not absolute)
- Check that all files uploaded correctly
- Verify directory structure matches expected layout

**Images Not Loading:**
- Check `images/` directory uploaded correctly
- Verify image paths in HTML/CSS are correct
- Ensure case-sensitivity matches (important on Linux servers)

**Blank Pages:**
- Check browser console for JavaScript errors
- Verify all JSON files are present and valid
- Test with different browsers

**Slow Loading:**
- Consider optimizing large JSON files (`featured_items_FULL.json` is 2.9MB)
- Enable gzip compression on server
- Use CDN for static assets

---

## 📞 Support

For issues or questions about the deployment:
1. Check `/backend/docs` for technical documentation
2. Review `CLEANUP_SUMMARY.md` for project history
3. Consult `PROJECT_STRUCTURE.md` for file organization

---

**Ready to deploy! 🚀**

Choose your hosting method above and follow the steps. The `/web` directory is production-ready.

