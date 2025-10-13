import pandas as pd
import json
from collections import defaultdict
from datetime import datetime

# Read the raw CSV data
print("Loading raw data...")
df = pd.read_csv('traderjoes-dump-3.csv', dtype={'sku': str, 'store_code': str}, low_memory=False)

# Convert columns to correct types
df['retail_price'] = pd.to_numeric(df['retail_price'], errors='coerce')
df['inserted_at'] = pd.to_datetime(df['inserted_at'], errors='coerce')
df = df.dropna(subset=['inserted_at', 'retail_price'])  # Remove any rows with invalid data

# Define essential items by keywords (prioritize household staples)
essential_keywords = {
    'dairy_basics': [
        'whole milk', '2% milk', 'skim milk', 'reduced fat milk', 'organic milk',
        'butter', 'eggs', 'large eggs', 'cage free eggs', 'organic eggs'
    ],
    'cheese_basics': [
        'cheddar cheese', 'mozzarella cheese', 'parmesan cheese', 'swiss cheese',
        'cream cheese', 'string cheese'
    ],
    'bread': [
        'whole wheat bread', 'white bread', 'sourdough', 'bagels', 'english muffins',
        'tortillas', 'pita bread'
    ],
    'produce': [
        'bananas', 'apples', 'oranges', 'strawberries', 'blueberries',
        'carrots', 'broccoli', 'spinach', 'lettuce', 'tomatoes', 'potatoes',
        'onions', 'garlic', 'avocados', 'lemons', 'limes'
    ],
    'meat': [
        'chicken breast', 'ground beef', 'ground turkey', 'bacon', 'salmon',
        'pork chops', 'turkey breast', 'sausage'
    ],
    'pantry': [
        'olive oil', 'vegetable oil', 'flour', 'sugar', 'brown sugar',
        'rice', 'pasta', 'spaghetti', 'penne', 'beans', 'canned tomatoes',
        'tomato sauce', 'chicken broth', 'beef broth', 'peanut butter',
        'jam', 'honey', 'oatmeal', 'cereal'
    ],
    'condiments': [
        'ketchup', 'mustard', 'mayonnaise', 'hot sauce', 'soy sauce',
        'salsa', 'ranch dressing', 'balsamic vinegar'
    ],
    'beverages': [
        'orange juice', 'apple juice', 'coffee', 'tea'
    ],
    'frozen': [
        'frozen vegetables', 'frozen fruit', 'ice cream', 'frozen pizza'
    ]
}

# Flatten keywords list
all_keywords = []
for category, keywords in essential_keywords.items():
    all_keywords.extend(keywords)

# Filter for essential items
print("Filtering for essential items...")
def is_essential_item(title):
    title_lower = title.lower()
    # Exclude certain terms
    exclude_terms = ['gift', 'card', 'candle', 'decoration', 'toy', 'pet', 'dog', 'cat']
    if any(term in title_lower for term in exclude_terms):
        return False
    
    # Check if title contains any essential keyword
    return any(keyword in title_lower for keyword in all_keywords)

df['is_essential'] = df['item_title'].apply(is_essential_item)
essential_df = df[df['is_essential']]

print(f"Found {len(essential_df['sku'].unique())} essential items")

# Map store codes to names
store_map = {
    '452': 'austin',
    '701': 'chicago',
    '546': 'newyork',
    '31': 'la'
}

# Filter for items available in all 4 stores
print("Filtering for items in all stores...")
items_by_store = essential_df.groupby('sku')['store_code'].apply(
    lambda x: set(str(code) for code in x.unique())
)
items_in_all_stores = items_by_store[items_by_store.apply(
    lambda stores: all(code in stores for code in store_map.keys())
)].index.tolist()

essential_df = essential_df[essential_df['sku'].isin(items_in_all_stores)]
print(f"Items available in all 4 stores: {len(items_in_all_stores)}")

# Get the last 12 months of data
latest_date = essential_df['inserted_at'].max()
twelve_months_ago = latest_date - pd.DateOffset(months=12)
essential_df = essential_df[essential_df['inserted_at'] >= twelve_months_ago]

# Create month labels
essential_df['month'] = essential_df['inserted_at'].dt.to_period('M').astype(str)
months = sorted(essential_df['month'].unique())[-12:]  # Last 12 months
print(f"Using {len(months)} months of data: {months[0]} to {months[-1]}")

# Build the output structure
output = {
    'months': months,
    'items': {}
}

# Process each item
print("Processing items...")
for sku in items_in_all_stores:
    item_data = essential_df[essential_df['sku'] == sku]
    
    if len(item_data) == 0:
        continue
    
    # Get item title (clean it)
    title = item_data['item_title'].iloc[0]
    # Remove common suffixes
    title = title.replace(' 2 of 8 assets', '').replace(' 1 of 8 assets', '').strip()
    
    # Build store data
    stores_data = {}
    for store_code, store_name in store_map.items():
        store_items = item_data[item_data['store_code'].astype(str) == store_code]
        
        if len(store_items) == 0:
            continue
        
        # Get monthly prices
        monthly_prices = {}
        for month in months:
            month_data = store_items[store_items['month'] == month]
            if len(month_data) > 0:
                # Use median price for the month
                monthly_prices[month] = round(month_data['retail_price'].median(), 2)
        
        # Only include if we have at least 6 months of data
        if len(monthly_prices) >= 6:
            stores_data[store_name] = monthly_prices
    
    # Only include item if it has data for at least 3 stores
    if len(stores_data) >= 3:
        output['items'][str(sku)] = {
            'title': title,
            'stores': stores_data
        }

print(f"Final dataset: {len(output['items'])} essential items")

# Save to JSON
output_file = 'basket_essentials.json'
with open(output_file, 'w') as f:
    json.dump(output, f, indent=2)

print(f"Saved to {output_file}")

# Print some sample items
print("\nSample items included:")
for i, (sku, data) in enumerate(list(output['items'].items())[:20]):
    print(f"  - {data['title']}")
    if i >= 19:
        break

