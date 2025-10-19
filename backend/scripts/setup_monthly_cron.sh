#!/bin/bash
# Setup monthly cron job for inflation tracker

SCRIPT_DIR="/Users/kaner/tradercpi"
SCRIPT_NAME="fetch_monthly_inflation.py"
LOG_FILE="$SCRIPT_DIR/logs/monthly_fetch_\$(date +\%Y\%m).log"

# Create log directory
mkdir -p "$SCRIPT_DIR/logs"
mkdir -p "$SCRIPT_DIR/backups"

echo "="
echo "SETTING UP MONTHLY INFLATION TRACKER CRON JOB"
echo "="*70

# Create the cron command
CRON_CMD="0 2 1 * * cd $SCRIPT_DIR && /usr/bin/python3 $SCRIPT_NAME > logs/monthly_fetch_\$(date +\%Y\%m).log 2>&1"

echo ""
echo "This will run the scraper:"
echo "  - Day: 1st of each month"
echo "  - Time: 2:00 AM"
echo "  - Script: $SCRIPT_NAME"
echo "  - Output: Appends to traderjoes_inflation_tracker.csv"
echo "  - Logs: logs/monthly_fetch_YYYYMM.log"
echo ""

# Show current crontab
echo "Current crontab:"
crontab -l 2>/dev/null || echo "  (no crontab yet)"
echo ""

# Create temp crontab
TEMP_CRON=$(mktemp)
crontab -l 2>/dev/null > "$TEMP_CRON" || true

# Check if already exists
if grep -q "fetch_monthly_inflation.py" "$TEMP_CRON" 2>/dev/null; then
    echo "⚠️  Cron job already exists!"
    echo ""
    grep "fetch_monthly_inflation" "$TEMP_CRON"
    echo ""
    read -p "Replace existing cron job? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        rm "$TEMP_CRON"
        exit 0
    fi
    # Remove old entry
    grep -v "fetch_monthly_inflation.py" "$TEMP_CRON" > "${TEMP_CRON}.new"
    mv "${TEMP_CRON}.new" "$TEMP_CRON"
fi

# Add new cron job
echo "" >> "$TEMP_CRON"
echo "# Trader Joe's Monthly Inflation Tracker - Runs 1st of month at 2 AM" >> "$TEMP_CRON"
echo "$CRON_CMD" >> "$TEMP_CRON"

# Install crontab
echo "Installing cron job..."
crontab "$TEMP_CRON"
rm "$TEMP_CRON"

echo ""
echo "✓ Cron job installed!"
echo ""
echo "New crontab:"
crontab -l | tail -3
echo ""

echo "="*70
echo "SETUP COMPLETE"
echo "="*70
echo ""
echo "The scraper will now run automatically on the 1st of each month at 2 AM."
echo ""
echo "Files:"
echo "  - Data appends to: traderjoes_inflation_tracker.csv"
echo "  - Monthly backups: backups/traderjoes_snapshot_YYYY-MM-DD.csv"
echo "  - Logs: logs/monthly_fetch_YYYYMM.log"
echo ""
echo "To test manually:"
echo "  python3 fetch_monthly_inflation.py"
echo ""
echo "To view/edit cron:"
echo "  crontab -l  # view"
echo "  crontab -e  # edit"
echo ""
echo "To remove:"
echo "  crontab -l | grep -v fetch_monthly_inflation | crontab -"
echo ""

