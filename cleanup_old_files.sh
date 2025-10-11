#!/bin/bash
# Clean up old test/scraper files

echo "=== Cleaning up old test files ==="
echo

# List of files to remove (old test scripts and outputs)
OLD_FILES=(
    "fetch_traderjoes.py"
    "fetch_stealth.py"
    "fetch_with_browser.py"
    "fetch_all_products.py"
    "fetch_store_specific.py"
    "fetch_graphql_direct.py"
    "fetch_with_pagination.py"
    "fetch_all_pages.py"
    "introspect_api.py"
    "inspect_real_queries.py"
    "reprocess_responses.py"
    "parse_api_responses.py"
    "create_basket_essentials.py"
    
    # Old CSV outputs (keep only final ones)
    "traderjoes-20251010-190549.csv"
    "traderjoes-20251010.csv"
    "traderjoes_full_20251010_191908.csv"
    "traderjoes_full_20251010_192841.csv"
    "traderjoes_complete_20251010_195315.csv"
    "traderjoes_reprocessed_20251010_193858.csv"
    "traderjoes_ALL_20251010_201834.csv"
    "fresh_traderjoes_oct2025.csv"
    
    # JSON response files (intermediate)
    "api_responses.json"
    "all_api_responses.json"
    "all_categories_responses.json"
    "paginated_responses_20251010_195315.json"
    "captured_graphql_requests.json"
    "captured_graphql_responses.json"
    "working_pagination_query.json"
    
    # Other test files
    "basket_essentials_dropdown.json"
    "basket_essentials.json"
    "dropdown_items.json"
    "featured_items.json"
    "price_data.json"
    
    # Log files
    "fetch_log.txt"
    "fetch_run.log"
    "pagination_fetch.log"
    "all_pages_fetch.log"
    "inspect_output.log"
    
    # HTML test files
    "debug-logo.html"
    "debug-markers.html"
    "test-image.html"
    "test-transparency.html"
    "final_page.html"
    "page_content.html"
    "dashboard.html"
    "template.html"
    "map.html"
    
    # Misc
    "SELECT"
)

# Files to KEEP
KEEP_FILES=(
    "fetch_final_working.py"
    "fetch_all_categories.py"
    "traderjoes-dump-3.csv"
    "sample_latest_data.csv"
    "traderjoes.db"
    "README.md"
    "index.html"
    "data_loader.js"
    "RUN_SCRAPERS.md"
    "SCRAPER_STATUS.md"
    "SCRAPER_RESULTS_SUMMARY.md"
    "check_progress.sh"
    "cleanup_old_files.sh"
)

echo "Files that will be removed:"
count=0
for file in "${OLD_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  - $file"
        ((count++))
    fi
done

echo
echo "Total files to remove: $count"
echo

read -p "Proceed with cleanup? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo
    echo "Removing files..."
    for file in "${OLD_FILES[@]}"; do
        if [ -f "$file" ]; then
            rm "$file"
            echo "  ✓ Removed: $file"
        fi
    done
    
    echo
    echo "✓ Cleanup complete!"
    echo
    echo "Remaining scraper files:"
    ls -1 *.py 2>/dev/null | grep -E "fetch|scrape" || echo "  (none)"
    
    echo
    echo "Remaining CSV files:"
    ls -1h *.csv 2>/dev/null | head -5
else
    echo "Cleanup cancelled."
fi

