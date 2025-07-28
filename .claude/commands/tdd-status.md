# TDD Status

Check the status of test generation for a feature.

## Usage: /tdd-status $ARGUMENTS

```bash
#!/bin/bash

FEATURE_NAME="${ARGUMENTS:-current}"

# Check task file
TASK_FILE=".claude/tasks/tdd-generation.json"

if [ -f "$TASK_FILE" ]; then
    echo "🧪 TDD Generation Status"
    echo "======================="
    echo ""
    
    # Parse task file
    STATUS=$(jq -r '.status' "$TASK_FILE" 2>/dev/null || echo "unknown")
    FEATURE=$(jq -r '.context.feature_name' "$TASK_FILE" 2>/dev/null || echo "unknown")
    CREATED=$(jq -r '.created' "$TASK_FILE" 2>/dev/null || echo "unknown")
    
    if [ "$FEATURE" = "$FEATURE_NAME" ] || [ "$FEATURE_NAME" = "current" ]; then
        echo "Feature: $FEATURE"
        echo "Status: $STATUS"
        echo "Started: $CREATED"
        echo ""
        
        # Check for generated test files
        echo "Looking for test files..."
        find . -name "*${FEATURE}*.test.*" -type f 2>/dev/null | while read -r test_file; do
            echo "  ✅ Found: $test_file"
        done
        
        # Check progress logs
        LOG_FILE=".claude/logs/progress/tdd-$(date +%Y-%m-%d).log"
        if [ -f "$LOG_FILE" ]; then
            echo ""
            echo "Recent activity:"
            grep -i "$FEATURE" "$LOG_FILE" | tail -5
        fi
    else
        echo "❌ No active generation for: $FEATURE_NAME"
        echo "   Current task is for: $FEATURE"
    fi
else
    echo "❌ No TDD generation tasks found"
    echo ""
    echo "To start TDD generation:"
    echo "1. Try to implement a feature without tests"
    echo "2. Or use: /tdd-workflow <feature-name>"
fi
```

## Related Commands:
- `/tdd-workflow` - Start TDD workflow
- `/tdd-dashboard` - View TDD metrics
- `/test` - Run tests

