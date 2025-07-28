# TDD Dashboard

View real-time TDD progress and metrics across all features.

## Arguments:
- $PERIOD: today|week|month (default: today)
- $FORMAT: console|markdown|json (default: console)

## Examples:
```bash
/tdd-dashboard              # Today's progress
/tdd-dashboard week         # Last 7 days
/tdd-dashboard month json   # Export monthly data
```

## Steps:

```bash
# Determine time period
case "${1:-today}" in
    today)
        DAYS=1
        ;;
    week)
        DAYS=7
        ;;
    month)
        DAYS=30
        ;;
    *)
        DAYS=1
        ;;
esac

# Run dashboard script
python3 .claude/scripts/tdd-dashboard.py --days $DAYS

# Also show quick stats
echo -e "\n## Quick Stats"

# Count active features
ACTIVE_FEATURES=$(find PRPs/active -name "*.md" 2>/dev/null | wc -l)
echo "Active PRPs: $ACTIVE_FEATURES"

# Show recent test runs
echo -e "\n## Recent Test Results"
if [ -f ".claude/logs/dashboards/current.json" ]; then
    cat .claude/logs/dashboards/current.json | jq -r '.events[] | select(.type == "test_run") | "\(.timestamp | split("T")[0]) \(.feature): \(.status)"' | head -5
fi

# Check TDD compliance
echo -e "\n## TDD Compliance Check"

# Look for recent violations
VIOLATIONS=$(grep -l "TDD Enforcer" .claude/logs/progress/daily/*.jsonl 2>/dev/null | wc -l)
if [ "$VIOLATIONS" -gt 0 ]; then
    echo "⚠️  Found $VIOLATIONS TDD violations today"
else
    echo "✅ Full TDD compliance!"
fi

# Show coverage trend
echo -e "\n## Coverage Trend"
if [ -d ".claude/logs/metrics/test-coverage" ]; then
    # Get latest coverage
    LATEST_COVERAGE=$(find .claude/logs/metrics/test-coverage -name "*.json" -exec cat {} \; | jq -r '.features | to_entries | map(.value.lines) | add/length' 2>/dev/null || echo "0")
    echo "Average Coverage: ${LATEST_COVERAGE:-0}%"
fi

# Suggest next actions
echo -e "\n## Suggested Actions"

if [ "$ACTIVE_FEATURES" -gt 0 ]; then
    echo "📋 Continue with active features:"
    find PRPs/active -name "*.md" -exec basename {} .md \; | head -3 | sed 's/^/  - /'
fi

# Low coverage features
echo -e "\n🔍 Features needing coverage:"
find .claude/logs/metrics/test-coverage -name "*.json" -exec cat {} \; | \
    jq -r '.features | to_entries | select(.value.lines < 80) | "\(.key): \(.value.lines)%"' 2>/dev/null | \
    head -3 | sed 's/^/  - /'

# Export option
if [ "${2:-console}" == "json" ]; then
    OUTPUT_FILE=".claude/logs/dashboards/export-$(date +%Y%m%d).json"
    
    echo -e "\n📤 Exporting data to $OUTPUT_FILE..."
    
    # Collect all data
    {
        echo "{"
        echo "  \"period\": \"$1\","
        echo "  \"generated\": \"$(date -Iseconds)\","
        echo "  \"logs\": ["
        
        # Export logs
        find .claude/logs/progress/daily -name "*.jsonl" -mtime -$DAYS -exec cat {} \; | \
            sed 's/$/,/' | sed '$ s/,$//'
        
        echo "  ]"
        echo "}"
    } > "$OUTPUT_FILE"
    
    echo "✅ Exported to $OUTPUT_FILE"
fi

# Auto-refresh option
if [ "$3" == "--auto" ]; then
    echo -e "\n🔄 Auto-refresh mode enabled. Press Ctrl+C to exit."
    python3 .claude/scripts/tdd-dashboard.py --days $DAYS --auto-refresh
fi
```

## Dashboard Sections:

### 📊 Summary
- TDD Compliance Score
- Overall Test Coverage
- Test Pass Rate

### 🎯 Key Metrics
- Total Tests Written
- Pass/Fail Counts
- Features with TDD
- Active Features

### 🚀 Feature Progress
- Coverage per feature
- Test counts
- Status indicators

### 📋 Recent Activity
- Last 10 TDD events
- Timestamps
- Event details

### 🤖 Agent Activity
- Which agents are active
- Task counts
- Feature coverage

### 📈 Trends
- Coverage over time
- Test velocity
- Compliance trends

### 💡 Recommendations
- Low coverage warnings
- Failed test alerts
- Missing test notifications

## Related Commands:
- `/tdd-status [feature]` - Status for specific feature
- `/tdd-coverage` - Coverage report
- `/tdd-agents` - Agent performance
- `/chain tdd-feature-complete` - Run full TDD workflow
