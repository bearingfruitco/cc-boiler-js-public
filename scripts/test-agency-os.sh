#!/bin/bash
# Test script for Agency OS integration

echo "🧪 Testing Agency OS Integration and Commands"
echo "============================================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test function
test_item() {
    local test_name="$1"
    local test_command="$2"
    local expected_result="$3"
    
    echo -n "Testing $test_name... "
    
    if eval "$test_command"; then
        echo -e "${GREEN}✓ PASS${NC}"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        echo "  Command: $test_command"
        echo "  Expected: $expected_result"
        return 1
    fi
}

# Track results
TESTS_RUN=0
TESTS_PASSED=0

# Test 1: Agency OS standards exist
echo "## 1. Agency OS Standards"
test_item "Standards directory exists" "test -d .agent-os/standards" "Directory exists"
((TESTS_RUN++)) && ((TESTS_PASSED+=$?==0?1:0))

test_item "Design system standards" "test -f .agent-os/standards/design-system.md" "File exists"
((TESTS_RUN++)) && ((TESTS_PASSED+=$?==0?1:0))

test_item "Tech stack standards" "test -f .agent-os/standards/tech-stack.md" "File exists"
((TESTS_RUN++)) && ((TESTS_PASSED+=$?==0?1:0))

test_item "Best practices standards" "test -f .agent-os/standards/best-practices.md" "File exists"
((TESTS_RUN++)) && ((TESTS_PASSED+=$?==0?1:0))

echo ""

# Test 2: Commands exist
echo "## 2. Command Files"
test_item "analyze-existing command" "test -f .claude/commands/analyze-existing.md" "File exists"
((TESTS_RUN++)) && ((TESTS_PASSED+=$?==0?1:0))

test_item "migrate-to-strict-design command" "test -f .claude/commands/migrate-to-strict-design.md" "File exists"
((TESTS_RUN++)) && ((TESTS_PASSED+=$?==0?1:0))

test_item "create-prd-from-existing command" "test -f .claude/commands/create-prd-from-existing.md" "File exists"
((TESTS_RUN++)) && ((TESTS_PASSED+=$?==0?1:0))

echo ""

# Test 3: Aliases
echo "## 3. Command Aliases"
test_item "ae alias exists" "grep -q '\"ae\": \"analyze-existing\"' .claude/aliases.json" "Alias found"
((TESTS_RUN++)) && ((TESTS_PASSED+=$?==0?1:0))

test_item "mds alias exists" "grep -q '\"mds\": \"migrate-to-strict-design\"' .claude/aliases.json" "Alias found"
((TESTS_RUN++)) && ((TESTS_PASSED+=$?==0?1:0))

test_item "prd-existing alias exists" "grep -q '\"prd-existing\": \"create-prd-from-existing\"' .claude/aliases.json" "Alias found"
((TESTS_RUN++)) && ((TESTS_PASSED+=$?==0?1:0))

echo ""

# Test 4: Chains
echo "## 4. Chain Configuration"
test_item "analyze-existing-project chain" "grep -q '\"analyze-existing-project\"' .claude/chains.json" "Chain exists"
((TESTS_RUN++)) && ((TESTS_PASSED+=$?==0?1:0))

test_item "migrate-design-system chain" "grep -q '\"migrate-design-system\"' .claude/chains.json" "Chain exists"
((TESTS_RUN++)) && ((TESTS_PASSED+=$?==0?1:0))

test_item "onboard-existing chain" "grep -q '\"onboard-existing\"' .claude/chains.json" "Chain exists"
((TESTS_RUN++)) && ((TESTS_PASSED+=$?==0?1:0))

echo ""

# Test 5: Hooks
echo "## 5. Hook Configuration"
test_item "All hooks in settings.json exist" "python3 -c \"
import json
import os
import sys

with open('.claude/settings.json') as f:
    settings = json.load(f)

missing = []
for section in settings['hooks'].values():
    if isinstance(section, list):
        for item in section:
            for hook in item.get('hooks', []):
                path = hook['command'].replace('python3 ', '')
                if not os.path.exists(path):
                    missing.append(path)

if missing:
    print(f'Missing hooks: {missing}')
    sys.exit(1)
else:
    sys.exit(0)
\"" "All hooks exist"
((TESTS_RUN++)) && ((TESTS_PASSED+=$?==0?1:0))

echo ""

# Test 6: Documentation
echo "## 6. Documentation"
test_item "Agency OS guide exists" "test -f docs/AGENCY_OS_GUIDE.md" "File exists"
((TESTS_RUN++)) && ((TESTS_PASSED+=$?==0?1:0))

test_item "Integration guide exists" "test -f .agent-os/INTEGRATION_GUIDE.md" "File exists"
((TESTS_RUN++)) && ((TESTS_PASSED+=$?==0?1:0))

test_item "Complete integration summary exists" "test -f .agent-os/COMPLETE_INTEGRATION_SUMMARY.md" "File exists"
((TESTS_RUN++)) && ((TESTS_PASSED+=$?==0?1:0))

echo ""

# Test 7: Command count
echo "## 7. Command Count Verification"
COMMAND_COUNT=$(find .claude/commands -name "*.md" -type f 2>/dev/null | wc -l)
test_item "Command count (should be 114+)" "[ $COMMAND_COUNT -ge 114 ]" "114+ commands"
((TESTS_RUN++)) && ((TESTS_PASSED+=$?==0?1:0))
echo "  Actual count: $COMMAND_COUNT commands"

echo ""

# Summary
echo "========================================"
echo "## Test Summary"
echo "Tests run: $TESTS_RUN"
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $((TESTS_RUN - TESTS_PASSED))"

if [ $TESTS_PASSED -eq $TESTS_RUN ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
fi
