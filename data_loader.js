// Data loader for Trader Joe's Price Index
let priceData = {};
let priceDataFull = {}; // Full history for all items
let itemNames = {};
let itemList = [];
let basketItemList = []; // Separate list for basket builder
let months = [];
let rawMonths = [];
let monthsFull = []; // Full month history
let rawMonthsFull = [];

// Helper function to fill in missing months (2025-07, 2025-08, 2025-09)
function fillMissingMonths(monthsArray) {
    const filled = [...monthsArray];
    const missingMonths = ['2025-07', '2025-08', '2025-09'];
    
    // Find where 2025-06 is
    const june2025Index = filled.indexOf('2025-06');
    const oct2025Index = filled.indexOf('2025-10');
    
    // If we have June and October 2025, insert the missing months
    if (june2025Index >= 0 && oct2025Index >= 0) {
        // Insert at the position after June
        filled.splice(june2025Index + 1, 0, ...missingMonths);
    }
    
    return filled;
}

// Helper function to fill prices for missing months (use June 2025 price)
function fillPricesForMissingMonths(prices, months) {
    const june2025Index = months.indexOf('2025-06');
    const july2025Index = months.indexOf('2025-07');
    
    if (june2025Index >= 0 && july2025Index >= 0) {
        const junePrice = prices[june2025Index];
        // Fill July, August, September 2025 with June's price
        prices[july2025Index] = junePrice;
        prices[july2025Index + 1] = junePrice;
        prices[july2025Index + 2] = junePrice;
    }
    
    return prices;
}

async function loadRealData() {
    try {
        console.log('Starting data load...');
        
        // Load featured items (for item search) - using FULL version with complete history
        const featuredResponse = await fetch('featured_items_FULL.json');
        if (!featuredResponse.ok) throw new Error('Failed to load featured_items_FULL.json');
        const featuredData = await featuredResponse.json();
        console.log('Featured data loaded (FULL history)');
        
        // Load basket essentials (for basket builder)
        const basketResponse = await fetch('basket_essentials.json');
        if (!basketResponse.ok) throw new Error('Failed to load basket_essentials.json');
        const basketData = await basketResponse.json();
        console.log('Basket essentials loaded');
        
        // Load dropdown items (for item search autocomplete)
        const dropdownResponse = await fetch('dropdown_items.json');
        if (!dropdownResponse.ok) throw new Error('Failed to load dropdown_items.json');
        itemList = await dropdownResponse.json();
        console.log('Dropdown items loaded:', itemList.length);
        
        // Load basket dropdown (for basket builder autocomplete)
        const basketDropdownResponse = await fetch('basket_essentials_dropdown.json');
        if (!basketDropdownResponse.ok) throw new Error('Failed to load basket_essentials_dropdown.json');
        basketItemList = await basketDropdownResponse.json();
        console.log('Basket dropdown items loaded:', basketItemList.length);
        
        // Extract months (keep raw format for processing)
        // Store FULL unfiltered history for "Show Full History" feature
        const allMonths = featuredData.months;
        
        // Fill in missing months (July, August, September) with placeholder
        const filledMonths = fillMissingMonths(allMonths);
        rawMonthsFull = filledMonths;
        monthsFull = rawMonthsFull;
        
        // Default to latest 12 months from all available data
        const monthsToShow = Math.min(12, filledMonths.length);
        rawMonths = filledMonths.slice(-monthsToShow);
        months = rawMonths;
        console.log('Months loaded (latest ' + monthsToShow + '):', months.length);
        console.log('Date range:', rawMonths[0], 'to', rawMonths[rawMonths.length - 1]);
        console.log('Full history available:', monthsFull.length, 'months (including filled gaps)');
        
        // Transform data into format needed by app
        // priceData = { store: { sku: [prices...] } }
        const stores = ['austin', 'chicago', 'newyork', 'la'];
        
        stores.forEach(store => {
            priceData[store] = {};
            priceDataFull[store] = {};
        });
        
        // Process featured items (for item search)
        Object.entries(featuredData.items).forEach(([sku, itemData]) => {
            // Store item name
            itemNames[sku] = itemData.title;
            
            // Process prices for each store
            stores.forEach(store => {
                if (itemData.stores && itemData.stores[store]) {
                    // Create price array for last 12 months (filtered)
                    let prices = rawMonths.map(month => {
                        return itemData.stores[store][month] || null;
                    });
                    
                    // Create FULL UNFILTERED price array for "Show Full History"
                    let pricesFull = rawMonthsFull.map(month => {
                        return itemData.stores[store][month] || null;
                    });
                    
                    // Fill missing months with June price
                    prices = fillPricesForMissingMonths(prices, rawMonths);
                    pricesFull = fillPricesForMissingMonths(pricesFull, rawMonthsFull);
                    
                    // Only add if we have at least some price data
                    if (prices.some(p => p !== null)) {
                        priceData[store][sku] = prices;
                        priceDataFull[store][sku] = pricesFull;
                    }
                }
            });
        });
        
        // Process basket essentials (for basket builder)
        Object.entries(basketData.items).forEach(([sku, itemData]) => {
            // Store item name (overwrite if exists, as basket essentials are more complete)
            itemNames[sku] = itemData.title;
            
            // Process prices for each store
            stores.forEach(store => {
                if (itemData.stores && itemData.stores[store]) {
                    // Get all available basket months and fill missing ones
                    const allBasketMonths = fillMissingMonths(basketData.months);
                    
                    // Create price array for last 12 months
                    const monthsToShow = Math.min(12, allBasketMonths.length);
                    const basketMonths = allBasketMonths.slice(-monthsToShow);
                    let prices = basketMonths.map(month => {
                        return itemData.stores[store][month] || null;
                    });
                    
                    // Create FULL UNFILTERED price array for "Show Full History"
                    let pricesFull = allBasketMonths.map(month => {
                        return itemData.stores[store][month] || null;
                    });
                    
                    // Fill missing months with June price
                    prices = fillPricesForMissingMonths(prices, basketMonths);
                    pricesFull = fillPricesForMissingMonths(pricesFull, allBasketMonths);
                    
                    // Only add if we have at least some price data
                    if (prices.some(p => p !== null)) {
                        priceData[store][sku] = prices;
                        priceDataFull[store][sku] = pricesFull;
                    }
                }
            });
        });
        
        console.log('Data transformation complete');
        console.log('Price data keys:', Object.keys(priceData));
        console.log('Sample Austin items:', Object.keys(priceData.austin || {}).slice(0, 5));
        
        return true;
    } catch (error) {
        console.error('Error loading data:', error);
        return false;
    }
}

function getMonthLabels(useFull = false) {
    const monthsToUse = useFull ? rawMonthsFull : rawMonths;
    return monthsToUse.map(m => {
        const [year, month] = m.split('-');
        const date = new Date(year, month - 1);
        return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
    });
}

function searchItems(query, useBasketItems = false) {
    if (!query || query.length < 2) return [];
    
    const lowerQuery = query.toLowerCase();
    const sourceList = useBasketItems ? basketItemList : itemList;
    
    // Get the current store to show relevant prices
    const currentStore = useBasketItems ? 
        document.getElementById('basketStore')?.value || 'austin' : 
        document.getElementById('searchStore')?.value || 'austin';
    
    return sourceList
        .filter(item => item.title.toLowerCase().includes(lowerQuery))
        .map(item => {
            // Get current price for this item at the selected store
            let currentPrice = null;
            if (priceData[currentStore] && priceData[currentStore][item.sku]) {
                const prices = priceData[currentStore][item.sku];
                // Get the last non-null price
                for (let i = prices.length - 1; i >= 0; i--) {
                    if (prices[i] !== null) {
                        currentPrice = prices[i];
                        break;
                    }
                }
            }
            return {
                ...item,
                current_price: currentPrice
            };
        })
        .slice(0, 10); // Return top 10 matches
}

