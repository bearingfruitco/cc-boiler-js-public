#!/usr/bin/env bash

# Example script showing non-interactive command usage
# This replaces old interactive commands with new non-interactive versions

set -e  # Exit on error

echo "🚀 Running Claude Code Quality Gates (Non-Interactive)"
echo "=================================================="

# Set non-interactive mode
export CLAUDE_NON_INTERACTIVE=true

# Create results directory
mkdir -p validation-results
cd validation-results

# 1. Design System Validation
echo -n "Checking design system compliance... "
if claude --non-interactive "/validate-design all" > design-validation.json; then
    echo "✅ PASSED"
else
    violations=$(jq -r '.results.totalViolations' design-validation.json 2>/dev/null || echo "unknown")
    echo "❌ FAILED ($violations violations)"
fi

# 2. Stage Validation
echo -n "Checking stage progress... "
if claude --non-interactive "/stage-validate check current" > stage-validation.json; then
    progress=$(jq -r '.progress' stage-validation.json 2>/dev/null || echo "0")
    echo "✅ Stage complete ($progress%)"
else
    progress=$(jq -r '.progress' stage-validation.json 2>/dev/null || echo "0")
    echo "⚠️  Stage incomplete ($progress%)"
fi

# 3. Security Check
echo -n "Running security scan... "
if claude --non-interactive "/security-check all" > security-check.json; then
    echo "✅ SECURE"
else
    issues=$(jq -r '.results.vulnerabilities' security-check.json 2>/dev/null || echo "unknown")
    echo "❌ ISSUES FOUND ($issues vulnerabilities)"
fi

# 4. Dependency Scan
echo -n "Scanning dependencies... "
if claude --non-interactive "/deps scan" > dependency-scan.json; then
    echo "✅ CLEAN"
else
    echo "⚠️  Vulnerabilities found"
fi

# 5. Test Runner (if tests exist)
if [ -f "../package.json" ] && grep -q '"test"' ../package.json; then
    echo -n "Running tests... "
    if claude --non-interactive "/test-runner all" > test-results.json; then
        echo "✅ ALL TESTS PASS"
    else
        echo "❌ TEST FAILURES"
    fi
fi

# Generate summary
echo ""
echo "📊 Summary Report"
echo "=================="

# Count passes and failures
total=0
passed=0

for result in *.json; do
    if [ -f "$result" ]; then
        ((total++))
        if jq -e '.success // .status == "complete"' "$result" > /dev/null 2>&1; then
            ((passed++))
        fi
    fi
done

echo "Total checks: $total"
echo "Passed: $passed"
echo "Failed: $((total - passed))"

# Exit with appropriate code
if [ $passed -eq $total ]; then
    echo ""
    echo "✅ All quality gates passed!"
    exit 0
else
    echo ""
    echo "❌ Some quality gates failed. Check validation-results/*.json for details."
    exit 1
fi
