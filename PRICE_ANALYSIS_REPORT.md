# Trader Joe's Price Analysis by Store & Category

**Analysis Date:** October 11, 2025  
**Data Source:** `all_stores master.csv`  
**Records Analyzed:** 7,795 in-stock items  
**Unique Products:** 1,743 SKUs

---

## Executive Summary

### Store Price Ranking (Cheapest → Most Expensive)
1. **East Village, NYC** - $4.50 avg
2. **Austin, TX** - $4.61 avg (+$0.11)
3. **Hyde Park, Chicago** - $4.71 avg (+$0.21)
4. **Los Angeles, CA** - $4.71 avg (+$0.21)
5. **South Loop, Chicago** - $4.77 avg (+$0.27)

**Key Finding:** Only $0.27 difference between cheapest and most expensive stores on average.

---

## Price Consistency

### Identical Pricing Across Stores
- **98.5%** of products (1,206 out of 1,224 common products) have **identical prices** across all 5 stores
- Only **1.5%** of products (18 items) show price variations
- Average price difference when there IS variation: $0.35

**Conclusion:** Trader Joe's maintains remarkably consistent pricing nationwide, with very few regional adjustments.

---

## Biggest Price Differences

### Top 5 Products with Regional Price Variations

1. **Bruschetta Sauce** - $1.00 spread
   - LA/Austin: $2.99
   - NYC/Chicago: $3.99
   
2. **Seedless Lemons** - $1.00 spread
   - LA/Austin: $2.99
   - NYC/Chicago: $3.99

3. **White Sliced Bread** - $0.50 spread
   - Most stores: $1.99
   - NYC: $2.49

4. **Carb Savvy Whole Wheat Tortillas** - $0.50 spread
   - NYC/Chicago: $2.99
   - LA/Austin: $3.49

5. **Shishito Peppers** - $0.50 spread
   - NYC/Chicago: $2.49
   - LA/Austin: $2.99

---

## Category Price Comparison

### Average Price by Category & Store

| Category  | Austin, TX | East Village, NYC | Hyde Park, Chicago | Los Angeles, CA | South Loop, Chicago |
|-----------|-----------|-------------------|-------------------|-----------------|---------------------|
| **Alcohol** | $4.05 | $3.77 | $5.85 | $5.38 | $5.85 |
| **Bakery** | $4.25 | $4.21 | $4.32 | $4.34 | $4.41 |
| **Beverages** | $5.16 | $5.24 | $5.21 | $5.27 | $6.32 |
| **Cheese** | $5.18 | $5.25 | $5.14 | $5.25 | $5.15 |
| **Dairy** | $4.22 | $4.11 | $4.17 | $4.22 | $4.10 |
| **Frozen** | $4.46 | $4.43 | $4.46 | $4.73 | $4.46 |
| **Meat** | $5.76 | $5.94 | $5.89 | $5.77 | $5.86 |
| **Pantry** | $3.83 | $3.87 | $3.86 | $3.92 | $3.80 |
| **Produce** | $4.04 | $4.05 | $4.05 | $3.99 | $4.03 |
| **Snacks** | $3.50 | $3.50 | $3.51 | $3.52 | $3.51 |

### Most/Least Expensive Categories by Store

**Los Angeles, CA:**
- Most Expensive: Meat ($5.77 avg)
- Least Expensive: Snacks ($3.52 avg)

**Austin, TX:**
- Most Expensive: Meat ($5.76 avg)
- Least Expensive: Snacks ($3.50 avg)

**East Village, NYC:**
- Most Expensive: Meat ($5.94 avg)
- Least Expensive: Snacks ($3.50 avg)

**South Loop, Chicago:**
- Most Expensive: Beverages ($6.32 avg) ⚠️ Notably high
- Least Expensive: Snacks ($3.51 avg)

**Hyde Park, Chicago:**
- Most Expensive: Meat ($5.89 avg)
- Least Expensive: Snacks ($3.51 avg)

---

## Regional Insights

### Chicago Store Comparison
- **Hyde Park:** $4.71 avg
- **South Loop:** $4.77 avg
- **Difference:** Only $0.06 between the two Chicago locations

### Notable Patterns

1. **Austin, TX** gets the best deals on La Colombe cold brew products ($2.69 vs $2.99 elsewhere)

2. **East Village, NYC** pays premium on:
   - White Sliced Bread (+$0.50)
   - Lemon Chicken & Arugula Salad (+$0.50)

3. **Los Angeles, CA** pays more for:
   - Traditional Indian Flatbread (+$0.50)
   - Shishito Peppers (+$0.50)
   
4. **South Loop, Chicago** has notably expensive beverages category (+$1.10 vs Austin)

---

## Data Quality Notes

- Analysis based on **in-stock items only** (availability = 1)
- Common products = items available in all 5 stores (1,224 SKUs)
- Category classification based on product title keywords
- Price data as of October 2025

---

## Methodology

Products were categorized using keyword matching:
- **Cheese:** cheese, brie, cheddar, gouda, mozzarella, parmesan
- **Produce:** organic, potatoes, onions, lettuce, spinach, tomatoes, bananas, apples  
- **Frozen:** frozen, ice cream
- **Snacks:** chips, crackers, cookies, nuts, trail mix, popcorn
- **Beverages:** juice, coffee, tea, soda, water, kombucha
- **Meat:** chicken, beef, pork, lamb, turkey, sausage, bacon
- **Dairy:** milk, yogurt, butter, eggs, cream
- **Pantry:** pasta, rice, beans, sauce, oil, vinegar
- **Alcohol:** wine, beer, vodka, gin, whiskey
- **Bakery:** bread, bagels, muffins, croissant

Products not matching keywords classified as "Other"

