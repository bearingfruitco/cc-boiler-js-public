#!/bin/bash
# Comprehensive test of the Claude Code Boilerplate v4.0.0

echo "================================================"
echo "  Claude Code Boilerplate v4.0.0 System Test"
echo "================================================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
total_tests=0
passed_tests=0
failed_tests=0

# Function to run a test
run_test() {
    local test_name=$1
    local test_command=$2
    
    ((total_tests++))
    
    echo -n "Testing $test_name... "
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASSED${NC}"
        ((passed_tests++))
        return 0
    else
        echo -e "${RED}❌ FAILED${NC}"
        ((failed_tests++))
        return 1
    fi
}

echo "1. TESTING FILE STRUCTURE"
echo "--------------------------"
run_test "Commands directory" "[ -d /Users/shawnsmith/dev/bfc/boilerplate/.claude/commands ]"
run_test "Hooks directory" "[ -d /Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks ]"
run_test "Agents directory" "[ -d /Users/shawnsmith/dev/bfc/boilerplate/.claude/agents ]"
run_test "Config directory" "[ -d /Users/shawnsmith/dev/bfc/boilerplate/.claude/config ]"
run_test "Utils directory" "[ -d /Users/shawnsmith/dev/bfc/boilerplate/.claude/utils ]"

echo ""
echo "2. TESTING CRITICAL COMMANDS"
echo "-----------------------------"
run_test "/sr command" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/.claude/commands/sr.md ]"
run_test "/fw command" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/.claude/commands/fw.md ]"
run_test "/chain command" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/.claude/commands/chain.md ]"
run_test "/agent command" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/.claude/commands/agent.md ]"
run_test "/create-prp command" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/.claude/commands/create-prp.md ]"
run_test "/prp-execute command" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/.claude/commands/prp-execute.md ]"

echo ""
echo "3. TESTING CRITICAL HOOKS"
echo "-------------------------"
run_test "Design check hook" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks/pre-tool-use/02-design-check.py ]"
run_test "Actually works hook" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks/pre-tool-use/04-actually-works.py ]"
run_test "State save hook" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks/post-tool-use/01-state-save.py ]"

echo ""
echo "4. TESTING CONFIGURATION FILES"
echo "-------------------------------"
run_test "chains.json" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/.claude/config/chains.json ]"
run_test "settings.json" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/.claude/settings.json ]"
run_test "version.json" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/.claude/version.json ]"

echo ""
echo "5. TESTING AGENT FILES"
echo "----------------------"
run_test "Frontend agent" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/frontend.md ]"
run_test "Backend agent" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/backend.md ]"
run_test "Security agent" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/security.md ]"
run_test "QA agent" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/qa.md ]"

echo ""
echo "6. TESTING DOCUMENTATION"
echo "------------------------"
run_test "System overview" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/docs/SYSTEM_OVERVIEW.md ]"
run_test "Claude.md" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/CLAUDE.md ]"
run_test "README" "[ -f /Users/shawnsmith/dev/bfc/boilerplate/README.md ]"

echo ""
echo "7. TESTING PYTHON SYNTAX"
echo "------------------------"
# Count Python files
py_count=$(find /Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks -name "*.py" ! -path "*/__pycache__/*" ! -name "*.backup" | wc -l)
echo "Found $py_count Python hook files"

# Test a sample hook
run_test "Sample hook syntax" "python3 -m py_compile /Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks/pre-tool-use/02-design-check.py"

echo ""
echo "================================================"
echo "                TEST SUMMARY"
echo "================================================"
echo -e "Total Tests: $total_tests"
echo -e "Passed: ${GREEN}$passed_tests${NC}"
echo -e "Failed: ${RED}$failed_tests${NC}"

if [ $failed_tests -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✨ ALL TESTS PASSED! System is ready.${NC}"
    exit 0
else
    echo ""
    echo -e "${YELLOW}⚠️  Some tests failed. Review the output above.${NC}"
    exit 1
fi
