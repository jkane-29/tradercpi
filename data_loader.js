// Data loader for Trader Joe's Price Index
let priceData = {};
let itemNames = {};
let itemList = [];
let months = [];
let rawMonths = [];

async function loadRealData() {
    try {
        console.log('Starting data load...');
        
        // Load featured items (has better structured data)
        const featuredResponse = await fetch('featured_items.json');
        if (!featuredResponse.ok) throw new Error('Failed to load featured_items.json');
        const featuredData = await featuredResponse.json();
        console.log('Featured data loaded');
        
        // Load dropdown items (for autocomplete)
        const dropdownResponse = await fetch('dropdown_items.json');
        if (!dropdownResponse.ok) throw new Error('Failed to load dropdown_items.json');
        itemList = await dropdownResponse.json();
        console.log('Dropdown items loaded:', itemList.length);
        
        // Extract months (keep raw format for processing)
        // Only use the latest 12 months
        const allMonths = featuredData.months;
        rawMonths = allMonths.slice(-12);
        months = rawMonths;
        console.log('Months loaded (latest 12):', months.length);
        
        // Transform data into format needed by app
        // priceData = { store: { sku: [prices...] } }
        const stores = ['austin', 'chicago', 'newyork', 'la'];
        
        stores.forEach(store => {
            priceData[store] = {};
        });
        
        // Process each item
        Object.entries(featuredData.items).forEach(([sku, itemData]) => {
            // Store item name
            itemNames[sku] = itemData.title;
            
            // Process prices for each store
            stores.forEach(store => {
                if (itemData.stores && itemData.stores[store]) {
                    // Create price array in month order (only last 12 months)
                    const prices = rawMonths.map(month => {
                        return itemData.stores[store][month] || null;
                    });
                    
                    // Only add if we have at least some price data
                    if (prices.some(p => p !== null)) {
                        priceData[store][sku] = prices;
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

function getMonthLabels() {
    return rawMonths.map(m => {
        const [year, month] = m.split('-');
        const date = new Date(year, month - 1);
        return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
    });
}

function searchItems(query) {
    if (!query || query.length < 2) return [];
    
    const lowerQuery = query.toLowerCase();
    return itemList
        .filter(item => item.title.toLowerCase().includes(lowerQuery))
        .slice(0, 10); // Return top 10 matches
}

