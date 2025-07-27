#!/bin/bash
# Check for Master Workflow Guide references across the project

echo "📚 Checking Master Workflow Guide Integration..."
echo "=============================================="
echo ""

# Check if the file exists
if [ -f "MASTER_WORKFLOW_GUIDE.md" ]; then
    echo "✅ MASTER_WORKFLOW_GUIDE.md exists"
else
    echo "❌ MASTER_WORKFLOW_GUIDE.md not found!"
    exit 1
fi

echo ""
echo "📍 Files referencing the Master Workflow Guide:"
echo ""

# Find all references
grep -r "MASTER_WORKFLOW_GUIDE" . --include="*.md" --exclude-dir=node_modules --exclude-dir=.git | grep -v "MASTER_WORKFLOW_GUIDE.md:" | while IFS=: read -r file rest; do
    echo "  ✓ $file"
done

echo ""
echo "📍 Key documentation files that should reference it:"
echo ""

# Check key files
key_files=(
    "README.md"
    "docs/claude/NEW_CHAT_CONTEXT.md"
    ".claude/QUICK_REFERENCE.md"
    "docs/setup/DAY_1_COMPLETE_GUIDE.md"
    "docs/workflow/DAILY_WORKFLOW.md"
)

for file in "${key_files[@]}"; do
    if [ -f "$file" ]; then
        if grep -q "MASTER_WORKFLOW_GUIDE" "$file"; then
            echo "  ✅ $file - References master guide"
        else
            echo "  ⚠️  $file - No reference found"
        fi
    else
        echo "  ❌ $file - File not found"
    fi
done

echo ""
echo "=============================================="
echo "📊 Summary:"
echo ""

# Count references
total_refs=$(grep -r "MASTER_WORKFLOW_GUIDE" . --include="*.md" --exclude-dir=node_modules --exclude-dir=.git | wc -l)
echo "Total references found: $total_refs"

echo ""
echo "✨ Master Workflow Guide is your single source of truth for:"
echo "  - Complete command reference"
echo "  - When to use PRP vs PRD"
echo "  - Testing automation details"
echo "  - Context management"
echo "  - Daily workflows"
echo "  - Troubleshooting"
