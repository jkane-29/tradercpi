# Mobile Testing Checklist 📱

Use this checklist to verify all mobile improvements are working correctly.

---

## 🎯 Navigation Testing

- [ ] Bottom navigation bar appears on mobile
- [ ] Bottom nav has two tabs: Item Search (🔍) and Basket Builder (🛒)
- [ ] Tapping "Item Search" tab shows Item Search section
- [ ] Tapping "Basket Builder" tab shows Basket Builder section
- [ ] Active tab is highlighted with pink background
- [ ] Navigation bar stays fixed at bottom when scrolling
- [ ] Safe area padding works on iPhone notch devices

---

## 🔍 Item Search Testing

### Search Interface
- [ ] Store selector appears and works
- [ ] Store selector doesn't zoom when tapped (font-size 16px)
- [ ] Item search input is prominent
- [ ] Item search input doesn't zoom when tapped
- [ ] Search placeholder text is visible

### Autocomplete Dropdown
- [ ] Typing shows autocomplete suggestions
- [ ] Suggestions dropdown scrolls smoothly
- [ ] Each suggestion is easy to tap (60px min height)
- [ ] Tapping a suggestion adds it to the chart
- [ ] Dropdown closes after selection
- [ ] Can scroll suggestions without triggering items

### Chart Display
- [ ] Chart appears after selecting an item
- [ ] Mobile time period controls show (3M, 6M, 1Y, ALL)
- [ ] Time period buttons are easy to tap (44px min)
- [ ] Changing time period updates the chart
- [ ] Active time period button is highlighted
- [ ] Chart responds to touch/drag interactions
- [ ] Mobile price display shows when touching chart
- [ ] Price display is prominent (large text, colored background)

### Comparison Mode
- [ ] Can add multiple items to comparison
- [ ] Overlay list shows all compared items
- [ ] Each item has a colored indicator
- [ ] Item names are readable (truncate if too long)
- [ ] Remove button (×) is easy to tap (44x44px)
- [ ] Removing items updates the chart immediately

---

## 🛒 Basket Builder Testing

### Basket Interface
- [ ] Store selector appears and works
- [ ] Item search input works
- [ ] Autocomplete shows basket-specific items
- [ ] Quantity selector is easy to use
- [ ] "Load CPI Basket" button works
- [ ] All controls are properly sized for touch

### Receipt Display
- [ ] Current receipt shows on top (stacked layout)
- [ ] Historical receipt shows below
- [ ] Both receipts are readable
- [ ] Receipt headers are properly sized
- [ ] Items list is clear
- [ ] Remove buttons (×) work on basket items
- [ ] Totals calculate correctly

### Basket Chart
- [ ] Chart shows when basket has items
- [ ] Time period buttons work
- [ ] Chart is readable at mobile size (300px height)
- [ ] Chart shows total basket cost over time

---

## 📐 Layout & Spacing

- [ ] All content has proper padding (1rem)
- [ ] No horizontal scrolling
- [ ] Content doesn't hide behind bottom nav
- [ ] Safe area respected on iPhone notch devices
- [ ] Proper spacing between sections
- [ ] Cards have proper border-radius (8px)

---

## ⚡ Performance & Interactions

- [ ] Scrolling is smooth (momentum scrolling on iOS)
- [ ] No lag when tapping buttons
- [ ] Charts render quickly
- [ ] Autocomplete is responsive
- [ ] No unwanted zoom on any input
- [ ] Button press feedback visible (scale animation)
- [ ] No double-tap zoom on buttons

---

## 🎨 Visual Design

- [ ] Trader Joe's red color (#bb3a39) used correctly
- [ ] Trader Joes font shows on labels
- [ ] Consistent spacing throughout
- [ ] Shadows provide proper elevation
- [ ] Active states are clearly visible
- [ ] Text is readable (sufficient contrast)
- [ ] Icons/emojis display correctly

---

## 🌐 Browser Testing

### iOS Safari
- [ ] All features work
- [ ] Safe area insets work
- [ ] Smooth scrolling works
- [ ] Touch events work
- [ ] Font rendering is good

### iOS Chrome
- [ ] All features work
- [ ] Consistent with Safari
- [ ] No zoom issues

### Android Chrome
- [ ] All features work
- [ ] Navigation bar works
- [ ] Touch interactions work
- [ ] Chart interactions work

### Android Firefox
- [ ] All features work
- [ ] Consistent experience
- [ ] No layout issues

---

## 📱 Device Testing

### Small Phones (iPhone SE, iPhone 12 mini)
- [ ] All content fits
- [ ] Buttons are still tappable
- [ ] Text is readable
- [ ] Charts display properly

### Standard Phones (iPhone 14, Pixel 6)
- [ ] Optimal layout
- [ ] All features accessible
- [ ] Good use of space

### Large Phones (iPhone 14 Pro Max, Galaxy S23 Ultra)
- [ ] Content scales appropriately
- [ ] No awkward spacing
- [ ] Still mobile-optimized (not desktop)

### Tablets (iPad Mini, iPad)
- [ ] Should switch to desktop layout at 769px+
- [ ] Mobile layout only shows up to 768px

---

## 🔄 Orientation Testing

### Portrait Mode
- [ ] Default and primary orientation
- [ ] All features work
- [ ] Navigation at bottom
- [ ] Charts are readable

### Landscape Mode
- [ ] Layout adapts appropriately
- [ ] Bottom nav still accessible
- [ ] Charts use available width
- [ ] No cut-off content

---

## 🐛 Edge Cases

- [ ] Very long item names truncate properly
- [ ] Many comparison items don't break layout
- [ ] Large basket (20+ items) scrolls properly
- [ ] Empty states show correctly
- [ ] Loading states work
- [ ] Network errors handled gracefully

---

## ✅ Final Verification

- [ ] No console errors
- [ ] No broken images
- [ ] All fonts load
- [ ] Data loads correctly
- [ ] Charts render without errors
- [ ] Autocomplete data loads

---

## 📊 Performance Metrics

Ideal targets:
- **First Contentful Paint:** < 1.5s
- **Time to Interactive:** < 3s
- **Smooth scrolling:** 60fps
- **Button response:** < 100ms

---

## 🚨 Critical Issues to Watch For

1. **Input zoom** - If any input causes zoom, font-size needs to be 16px+
2. **Bottom nav overlap** - Content should never hide behind nav bar
3. **Touch target size** - All interactive elements must be 44x44px minimum
4. **Chart touch** - Must respond to touch events, not just mouse
5. **Autocomplete scroll** - Must scroll smoothly without closing

---

## 📝 Reporting Issues

If you find issues, note:
1. Device model and OS version
2. Browser name and version
3. Steps to reproduce
4. Expected vs actual behavior
5. Screenshot if visual issue

---

**Ready to test?** Start with the navigation and work your way down the list! ✨

