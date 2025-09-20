# Trader Joe's Price Index

An interactive web application that tracks inflation across different cities and shopping archetypes, inspired by Riley Walz's playful data-driven projects and the clean design of FRED (Federal Reserve Economic Data).

## Project Structure

```
tradercpi/
├── index.html          # Splash screen (entry point)
├── map.html            # Interactive US map for city selection
├── dashboard.html      # City-specific inflation dashboard
├── css/
│   └── styles.css      # Shared styles for all pages
├── js/
│   └── app.js          # Shared JavaScript functionality
└── template.html       # Original single-file version (legacy)
```

## User Flow

1. **Splash Screen** (`index.html`) - Red Trader Joe's branding with 2-second auto-transition
2. **Interactive Map** (`map.html`) - Proper US map with city markers for Austin, Chicago, NYC, LA
3. **City Dashboard** (`dashboard.html`) - Shopping archetypes and inflation data specific to selected city
4. **Receipt Display** - Realistic Trader Joe's receipts with SKU numbers, tax calculations, and inflation data

## Features

- **Multi-screen experience** with smooth transitions between pages
- **City selection** that updates archetype names (UT/UChicago/NYU/UCLA, Austin ISD/CPS/NYC DOE/LAUSD)
- **5 shopping personas** per city:
  - Grad Student (ramen, frozen meals, cheap wine)
  - Teacher (breakfast items, healthy lunches, coffee)
  - Family of 4 (kid-friendly snacks, family meals)
  - Fed Chair (premium items, economist basket)
  - CPI Comparison (standard basket vs. Federal Reserve data)
- **Authentic Trader Joe's receipts** with realistic SKU numbers, tax calculations, and inflation tracking
- **Mobile-responsive design** with Trader Joe's red (#d41e36) color scheme
- **Proper US map** with accurate state outlines and geographic positioning

## Technical Implementation

- **Shared CSS**: Consistent styling across all pages with Trader Joe's branding
- **Shared JavaScript**: Common functionality for navigation, data handling, and receipt generation
- **URL parameters**: City selection passed between pages for context
- **Local storage**: Could be extended for user preferences and custom baskets

## Design Philosophy

Clean, data-forward presentation (FRED-inspired) combined with playful, engaging UX (Riley Walz-inspired). Uses modern CSS animations, hover effects, and a professional but approachable aesthetic.

## Getting Started

1. Open `index.html` in a web browser
2. Wait for the splash screen (2 seconds)
3. Select a city on the interactive map
4. Choose a shopping archetype to see inflation data
5. View the realistic Trader Joe's receipt with inflation calculations

## Future Enhancements

- Custom basket builder functionality
- Real-time data integration
- Historical inflation trends
- More cities and regional variations
- Social sharing of inflation baskets
