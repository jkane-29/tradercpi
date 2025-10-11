#!/bin/bash
# Monitor the scraper progress

echo "=== SCRAPER PROGRESS CHECK ==="
echo

# Check if process is running
if ps aux | grep -q "[p]ython3.*fetch_with_pagination"; then
    echo "✓ Scraper is RUNNING"
else
    echo "✗ Scraper is NOT running"
fi

echo

# Show log tail
if [ -f pagination_fetch.log ]; then
    lines=$(wc -l < pagination_fetch.log)
    echo "Log file has $lines lines"
    echo
    echo "=== Last 30 lines of log ==="
    tail -30 pagination_fetch.log
else
    echo "No log file yet"
fi

echo
echo "=== Recent CSV files ==="
ls -lht traderjoes*.csv 2>/dev/null | head -5

echo
echo "=== JSON response files ==="
ls -lht *responses*.json 2>/dev/null | head -3

echo
echo "To watch live: tail -f pagination_fetch.log"

