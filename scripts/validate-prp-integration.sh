#!/bin/bash
# Validate PRP System Integration

echo "🔍 Validating PRP System Integration"
echo "===================================="
echo ""

# Track validation results
ERRORS=0
WARNINGS=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo "✅ $2"
    else
        echo "❌ MISSING: $2 ($1)"
        ((ERRORS++))
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo "✅ $2"
    else
        echo "❌ MISSING: $2 ($1)"
        ((ERRORS++))
    fi
}

# Function to check command in file
check_command() {
    if grep -q "$2" "$1" 2>/dev/null; then
        echo "✅ Command '$2' found"
    else
        echo "❌ MISSING: Command '$2' in $1"
        ((ERRORS++))
    fi
}

# Function to check alias
check_alias() {
    if grep -q "\"$1\"" .claude/aliases.json 2>/dev/null; then
        echo "✅ Alias '$1' configured"
    else
        echo "⚠️  WARNING: Alias '$1' not found"
        ((WARNINGS++))
    fi
}

echo "📁 Checking Directory Structure..."
check_dir "PRPs" "PRPs root directory"
check_dir "PRPs/templates" "PRP templates"
check_dir "PRPs/ai_docs" "AI documentation"
check_dir "PRPs/active" "Active PRPs"
check_dir "PRPs/completed" "Completed PRPs"
check_dir "PRPs/scripts" "PRP scripts"
check_dir ".claude/metrics/prp_progress" "PRP progress tracking"
check_dir ".claude/metrics/prp_validation" "PRP validation history"
check_dir ".claude/context" "Unified context"

echo ""
echo "📄 Checking Core Files..."
check_file "PRPs/README.md" "PRP documentation"
check_file "PRPs/templates/prp_base.md" "Base PRP template"
check_file "PRPs/scripts/prp-runner.ts" "PRP runner script"
check_file "docs/workflow/UNIFIED_PRP_WORKFLOW.md" "Unified workflow guide"

echo ""
echo "🔧 Checking Commands..."
check_file ".claude/commands/prd-to-prp.md" "prd-to-prp command"
check_file ".claude/commands/prp-validate.md" "prp-validate command"
check_file ".claude/commands/prp-status.md" "prp-status command"
check_file ".claude/commands/prp-complete.md" "prp-complete command"

echo ""
echo "🔗 Checking Aliases..."
check_alias "convert-to-prp"
check_alias "prp-validate"
check_alias "prp-status"
check_alias "prp-complete"

echo ""
echo "🪝 Checking Hooks..."
check_file ".claude/hooks/pre-tool-use/05b-prp-context-loader.py" "PRP context loader"
check_file ".claude/hooks/post-tool-use/10-prp-progress-tracker.py" "PRP progress tracker"
check_file ".claude/utils/hook_coordinator.py" "Hook coordinator"
check_file ".claude/utils/unified_context.py" "Unified context manager"

echo ""
echo "📦 Checking Scripts Integration..."
if [ -f "scripts/quick-setup.sh" ]; then
    if grep -q "PRP system" scripts/quick-setup.sh; then
        echo "✅ PRP integrated in quick-setup.sh"
    else
        echo "❌ PRP not integrated in quick-setup.sh"
        ((ERRORS++))
    fi
fi

if [ -f "scripts/add-to-existing.sh" ]; then
    if grep -q "PRP" scripts/add-to-existing.sh; then
        echo "✅ PRP integrated in add-to-existing.sh"
    else
        echo "❌ PRP not integrated in add-to-existing.sh"
        ((ERRORS++))
    fi
fi

echo ""
echo "⚙️ Checking Configuration..."
if [ -f ".claude/config.json" ]; then
    if grep -q "prp_system" .claude/config.json; then
        echo "✅ PRP system configured"
    else
        echo "❌ PRP system not in config.json"
        ((ERRORS++))
    fi
fi

echo ""
echo "🔄 Checking Hook Conflicts..."
# Check if hooks have proper guards
if grep -q "PRP files (handled by 05b)" .claude/hooks/pre-tool-use/05a-auto-context-inclusion.py 2>/dev/null; then
    echo "✅ Context hooks properly separated"
else
    echo "⚠️  WARNING: Potential context hook conflict"
    ((WARNINGS++))
fi

if grep -q "Only runs when editing PRP files" .claude/hooks/pre-tool-use/16a-prp-validator.py 2>/dev/null; then
    echo "✅ PRP validator properly scoped"
else
    echo "⚠️  WARNING: PRP validator may conflict with design validator"
    ((WARNINGS++))
fi

echo ""
echo "📋 Checking Generate Tasks Enhancement..."
if grep -q -- "--from-prp" .claude/commands/generate-tasks.md 2>/dev/null; then
    echo "✅ Generate tasks supports --from-prp"
else
    echo "❌ Generate tasks missing --from-prp support"
    ((ERRORS++))
fi

echo ""
echo "📊 Validation Summary"
echo "===================="
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo "✅ PRP System fully integrated and operational!"
    else
        echo "✅ PRP System integrated with $WARNINGS warnings to review"
    fi
    echo ""
    echo "Ready to use:"
    echo "- /create-prp [feature] - Create comprehensive PRP"
    echo "- /prd-to-prp [feature] - Convert existing PRD"
    echo "- /prp-validate [feature] - Check completeness"
    echo "- /gt [feature] --from-prp - Generate enhanced tasks"
    echo "- /prp-execute [feature] - Run validation loops"
    echo "- /prp-status [feature] - Check progress"
    echo "- /prp-complete [feature] - Archive and learn"
else
    echo "❌ PRP System has $ERRORS errors that need fixing!"
    echo ""
    echo "Run './scripts/quick-setup.sh' to fix missing components"
fi