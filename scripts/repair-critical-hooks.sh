#!/bin/bash
# Critical Hook Repair Script - Manual Review Version
# Generated: 2025-08-05
# 
# This script repairs the 3 critical missing hooks that are blocking operations

echo "=================================="
echo "CRITICAL HOOK REPAIR"
echo "=================================="
echo ""

# Step 1: Backup current hooks
echo "Step 1: Creating backup..."
BACKUP_DIR=".claude/hooks.backup.$(date +%Y%m%d_%H%M%S)"
cp -r .claude/hooks "$BACKUP_DIR"
echo "✓ Backup created: $BACKUP_DIR"
echo ""

# Step 2: Fix 07-pii-protection.py (both versions broken, use our fixed version)
echo "Step 2: Installing fixed PII Protection hook..."
if [ -f ".claude/hooks/pre-tool-use/07-pii-protection-FIXED.py" ]; then
    cp .claude/hooks/pre-tool-use/07-pii-protection-FIXED.py .claude/hooks/pre-tool-use/07-pii-protection.py
    echo "✓ Installed fixed 07-pii-protection.py"
else
    echo "❌ Fixed PII hook not found! Run: python3 scripts/repair-hooks-manual.py first"
    exit 1
fi

# Step 3: Fix 16-tcpa-compliance.py (original has syntax error, use fixed version)
echo "Step 3: Installing fixed TCPA Compliance hook..."
if [ -f ".claude/hooks/pre-tool-use/16-tcpa-compliance-FIXED.py" ]; then
    cp .claude/hooks/pre-tool-use/16-tcpa-compliance-FIXED.py .claude/hooks/pre-tool-use/16-tcpa-compliance.py
    echo "✓ Installed fixed 16-tcpa-compliance.py"
else
    echo "⚠️  Fixed TCPA hook not found, skipping..."
fi

# Step 4: Fix 22-security-validator.py (original is valid)
echo "Step 4: Restoring Security Validator hook..."
if [ -f ".claude/hooks/pre-tool-use/22-security-validator.py.original" ]; then
    cp .claude/hooks/pre-tool-use/22-security-validator.py.original .claude/hooks/pre-tool-use/22-security-validator.py
    echo "✓ Restored 22-security-validator.py from .original"
else
    echo "❌ Original security validator not found!"
fi

echo ""
echo "=================================="
echo "TESTING HOOKS"
echo "=================================="
echo ""

# Test each hook
echo "Testing hooks (checking Python syntax)..."
echo ""

for hook in 07-pii-protection.py 16-tcpa-compliance.py 22-security-validator.py; do
    if [ -f ".claude/hooks/pre-tool-use/$hook" ]; then
        python3 -m py_compile ".claude/hooks/pre-tool-use/$hook" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "✓ $hook - Valid Python syntax"
        else
            echo "❌ $hook - Syntax error!"
            python3 -m py_compile ".claude/hooks/pre-tool-use/$hook"
        fi
    else
        echo "❌ $hook - File not found!"
    fi
done

echo ""
echo "=================================="
echo "SUMMARY"
echo "=================================="
echo ""
echo "Critical hooks have been repaired."
echo ""
echo "Next steps:"
echo "1. Test file operations in Claude Code to verify hooks are working"
echo "2. Handle duplicate hooks with: python3 scripts/analyze-hooks-detailed.py"
echo "3. Archive old versions:"
echo "   mkdir -p .claude/hooks/_archive/$(date +%Y%m%d)"
echo "   find .claude/hooks -name '*.original' -o -name '*.broken' -o -name '*.backup' | xargs -I {} mv {} .claude/hooks/_archive/$(date +%Y%m%d)/"
echo ""
echo "✅ Critical repair complete!"
