#!/bin/bash
# Test all critical commands exist

echo "🔍 Testing Command Files..."
echo ""

# Critical commands list
commands=(
    "sr" "fw" "chain" "agent" "prp-execute" "create-prp"
    "cc" "gt" "pt" "analyze-existing" "create-prd"
    "spawn" "orch" "tdd" "metrics" "checkpoint"
    "compress" "help" "ut" "vd" "tr"
)

passed=0
failed=0

for cmd in "${commands[@]}"; do
    if [ -f "/Users/shawnsmith/dev/bfc/boilerplate/.claude/commands/$cmd.md" ]; then
        echo "✅ /$cmd"
        ((passed++))
    else
        echo "❌ /$cmd - NOT FOUND"
        ((failed++))
    fi
done

echo ""
echo "Summary: $passed passed, $failed failed"
