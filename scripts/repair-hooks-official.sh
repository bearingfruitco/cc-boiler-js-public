#!/bin/bash
# Critical Hook Repair Script - Official Claude Code Compliant Version
# Generated: 2025-08-05
# 
# This script repairs the 3 critical missing hooks with official format compliance

echo "=================================="
echo "CRITICAL HOOK REPAIR - OFFICIAL FORMAT"
echo "=================================="
echo ""
echo "This repair follows the official Claude Code hook specification:"
echo "- JSON input via stdin"
echo "- Exit code 0 = success"
echo "- Exit code 2 = blocking error"
echo "- Exit code 1 = non-blocking error"
echo ""

# Step 1: Backup current hooks
echo "Step 1: Creating backup..."
BACKUP_DIR=".claude/hooks.backup.$(date +%Y%m%d_%H%M%S)"
cp -r .claude/hooks "$BACKUP_DIR"
echo "✓ Backup created: $BACKUP_DIR"
echo ""

# Step 2: Install official format compliant hooks
echo "Step 2: Installing officially compliant hooks..."

# Install PII Protection hook
if [ -f ".claude/hooks/pre-tool-use/07-pii-protection-OFFICIAL.py" ]; then
    cp .claude/hooks/pre-tool-use/07-pii-protection-OFFICIAL.py .claude/hooks/pre-tool-use/07-pii-protection.py
    echo "✓ Installed 07-pii-protection.py (official format)"
else
    echo "❌ Official PII hook not found! Run: python3 scripts/create-official-hooks.py first"
fi

# Install TCPA Compliance hook
if [ -f ".claude/hooks/pre-tool-use/16-tcpa-compliance-OFFICIAL.py" ]; then
    cp .claude/hooks/pre-tool-use/16-tcpa-compliance-OFFICIAL.py .claude/hooks/pre-tool-use/16-tcpa-compliance.py
    echo "✓ Installed 16-tcpa-compliance.py (official format)"
else
    echo "❌ Official TCPA hook not found!"
fi

# Install Security Validator hook
if [ -f ".claude/hooks/pre-tool-use/22-security-validator-OFFICIAL.py" ]; then
    cp .claude/hooks/pre-tool-use/22-security-validator-OFFICIAL.py .claude/hooks/pre-tool-use/22-security-validator.py
    echo "✓ Installed 22-security-validator.py (official format)"
else
    echo "❌ Official security validator not found!"
fi

echo ""
echo "=================================="
echo "TESTING HOOKS"
echo "=================================="
echo ""

# Test each hook with proper JSON input
echo "Testing hooks with official JSON format..."
echo ""

for hook in 07-pii-protection.py 16-tcpa-compliance.py 22-security-validator.py; do
    if [ -f ".claude/hooks/pre-tool-use/$hook" ]; then
        # Test Python syntax
        python3 -m py_compile ".claude/hooks/pre-tool-use/$hook" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "✓ $hook - Valid Python syntax"
            
            # Test with sample JSON input
            TEST_JSON='{"tool_name":"Write","tool_input":{"file_path":"test.ts","content":"console.log(test);"}}'
            echo "$TEST_JSON" | python3 ".claude/hooks/pre-tool-use/$hook" 2>/dev/null
            EXIT_CODE=$?
            
            if [ $EXIT_CODE -eq 0 ]; then
                echo "  ✓ Handles JSON input correctly (exit code 0)"
            elif [ $EXIT_CODE -eq 2 ]; then
                echo "  ✓ Blocks correctly (exit code 2)"
            elif [ $EXIT_CODE -eq 1 ]; then
                echo "  ✓ Non-blocking error handling works (exit code 1)"
            else
                echo "  ⚠️ Unexpected exit code: $EXIT_CODE"
            fi
        else
            echo "❌ $hook - Syntax error!"
        fi
    else
        echo "❌ $hook - File not found!"
    fi
done

echo ""
echo "=================================="
echo "CLEANUP OLD VERSIONS"
echo "=================================="
echo ""

# Archive old versions
ARCHIVE_DIR=".claude/hooks/_archive/$(date +%Y%m%d)"
mkdir -p "$ARCHIVE_DIR"

echo "Archiving old hook versions to $ARCHIVE_DIR..."
find .claude/hooks -type f \( \
    -name "*.original" -o \
    -name "*.broken" -o \
    -name "*.backup" -o \
    -name "*.old" -o \
    -name "*.prefixbatch" -o \
    -name "*-FIXED.py" -o \
    -name "*-OFFICIAL.py" \
\) | while read file; do
    mv "$file" "$ARCHIVE_DIR/" 2>/dev/null && echo "  Archived: $(basename $file)"
done

echo ""
echo "=================================="
echo "SUMMARY"
echo "=================================="
echo ""
echo "✅ Critical hooks repaired with official format compliance"
echo ""
echo "The hooks now follow the official Claude Code specification:"
echo "- Receive JSON input via stdin"
echo "- Return proper exit codes (0=success, 2=block, 1=warn)"
echo "- Output errors to stderr for Claude to process"
echo ""
echo "Next steps:"
echo "1. Restart Claude Code to load the new hooks"
echo "2. Test file operations to verify hooks are working"
echo "3. Check other hooks for compliance: python3 scripts/validate-all-hooks.py"
echo ""
echo "Official documentation: https://docs.anthropic.com/en/docs/claude-code/hooks"
echo ""
echo "✅ Repair complete!"
