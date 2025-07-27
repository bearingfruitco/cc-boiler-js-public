#!/bin/bash
# Test sub-agent integration for Claude Code v2.8.0

echo "🧪 Testing Claude Code Sub-Agents v2.8.0"
echo "======================================="

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test results
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_result="$3"
    
    echo -e "\n📋 Testing: $test_name"
    
    if eval "$test_command"; then
        echo -e "${GREEN}✅ PASSED${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAILED${NC}: $test_name"
        ((TESTS_FAILED++))
    fi
}

# Test 1: Count agents
echo -e "\n${YELLOW}Test 1: Agent Count${NC}"
AGENT_COUNT=$(ls -1 .claude/agents/*.md 2>/dev/null | grep -v -E "(template|README|QUICK|agent-tool)" | wc -l)
echo "Found $AGENT_COUNT sub-agents"
if [ $AGENT_COUNT -ge 20 ]; then
    echo -e "${GREEN}✅ PASSED${NC}: Found $AGENT_COUNT agents (expected 20+)"
    ((TESTS_PASSED++))
else
    echo -e "${RED}❌ FAILED${NC}: Only found $AGENT_COUNT agents (expected 20+)"
    ((TESTS_FAILED++))
fi

# Test 2: Check critical agents
echo -e "\n${YELLOW}Test 2: Critical Agents${NC}"
CRITICAL_AGENTS=(
    "security-threat-analyst"
    "frontend-ux-specialist"
    "backend-reliability-engineer"
    "qa-test-engineer"
    "pm-orchestrator"
    "tdd-engineer"
    "code-reviewer"
    "documentation-writer"
)

for agent in "${CRITICAL_AGENTS[@]}"; do
    if [ -f ".claude/agents/${agent}.md" ]; then
        echo -e "  ${GREEN}✅${NC} ${agent}"
    else
        echo -e "  ${RED}❌${NC} ${agent} - Missing!"
        ((TESTS_FAILED++))
    fi
done

# Test 3: Verify agent format
echo -e "\n${YELLOW}Test 3: Agent Format Validation${NC}"
VALID_AGENTS=0
for agent_file in .claude/agents/*.md; do
    if [[ -f "$agent_file" ]] && ! [[ "$agent_file" =~ (template|README|QUICK|agent-tool) ]]; then
        # Check for YAML frontmatter
        if head -1 "$agent_file" | grep -q "^---$" && grep -q "^name:" "$agent_file"; then
            ((VALID_AGENTS++))
        else
            echo -e "  ${RED}⚠️${NC} Invalid format: $(basename "$agent_file")"
        fi
    fi
done
echo "Valid agents: $VALID_AGENTS"

# Test 4: Check aliases
echo -e "\n${YELLOW}Test 4: Alias Configuration${NC}"
if [ -f ".claude/aliases.json" ]; then
    KEY_ALIASES=("fe" "be" "qa" "sec" "tdd" "cr" "doc" "pm")
    FOUND_ALIASES=0
    
    for alias in "${KEY_ALIASES[@]}"; do
        if grep -q "\"$alias\":" .claude/aliases.json && grep -q "subagent to" .claude/aliases.json; then
            ((FOUND_ALIASES++))
        fi
    done
    
    echo "Key aliases found: $FOUND_ALIASES/${#KEY_ALIASES[@]}"
    if [ $FOUND_ALIASES -ge 6 ]; then
        echo -e "${GREEN}✅ PASSED${NC}: Aliases properly configured"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAILED${NC}: Missing key aliases"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}❌ FAILED${NC}: aliases.json not found"
    ((TESTS_FAILED++))
fi

# Test 5: Check hooks
echo -e "\n${YELLOW}Test 5: Hook Integration${NC}"
if [ -f ".claude/settings.json" ]; then
    HOOKS_FOUND=0
    
    # Check for subagent suggester
    if grep -q "20-subagent-suggester.py" .claude/settings.json; then
        echo -e "  ${GREEN}✅${NC} PostToolUse hook: subagent-suggester"
        ((HOOKS_FOUND++))
    fi
    
    # Check for flow controller
    if grep -q "02-flow-controller.py" .claude/settings.json; then
        echo -e "  ${GREEN}✅${NC} SubagentStop hook: flow-controller"
        ((HOOKS_FOUND++))
    fi
    
    # Check for agent summary
    if grep -q "03-agent-summary.py" .claude/settings.json; then
        echo -e "  ${GREEN}✅${NC} Stop hook: agent-summary"
        ((HOOKS_FOUND++))
    fi
    
    if [ $HOOKS_FOUND -ge 2 ]; then
        echo -e "${GREEN}✅ PASSED${NC}: Hooks integrated"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAILED${NC}: Some hooks missing"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}❌ FAILED${NC}: settings.json not found"
    ((TESTS_FAILED++))
fi

# Test 6: Check chains
echo -e "\n${YELLOW}Test 6: Workflow Chains${NC}"
if [ -f ".claude/chains.json" ]; then
    CHAIN_COUNT=$(grep -c "chain\":" .claude/chains.json)
    AGENT_CHAINS=0
    
    # Check for specific agent chains
    for chain in "security-audit-chain" "feature-development-chain" "database-migration-chain"; do
        if grep -q "\"$chain\"" .claude/chains.json; then
            ((AGENT_CHAINS++))
        fi
    done
    
    echo "Total chains: $CHAIN_COUNT"
    echo "Agent-based chains: $AGENT_CHAINS"
    
    if [ $AGENT_CHAINS -ge 3 ]; then
        echo -e "${GREEN}✅ PASSED${NC}: Agent chains configured"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAILED${NC}: Missing agent chains"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${RED}❌ FAILED${NC}: chains.json not found"
    ((TESTS_FAILED++))
fi

# Test 7: Check commands
echo -e "\n${YELLOW}Test 7: Command Integration${NC}"
INTEGRATED_COMMANDS=0

# Check specific command files
for cmd in "security-check" "create-tests" "review-pr"; do
    if [ -f ".claude/commands/${cmd}.md" ]; then
        if grep -q "subagent" ".claude/commands/${cmd}.md"; then
            echo -e "  ${GREEN}✅${NC} ${cmd} delegates to sub-agent"
            ((INTEGRATED_COMMANDS++))
        fi
    fi
done

if [ $INTEGRATED_COMMANDS -ge 2 ]; then
    echo -e "${GREEN}✅ PASSED${NC}: Commands integrated with sub-agents"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}⚠️ WARNING${NC}: Some commands not fully integrated"
fi

# Test 8: Documentation
echo -e "\n${YELLOW}Test 8: Documentation${NC}"
DOC_COUNT=0

if [ -f ".claude/agents/QUICK_REFERENCE.md" ]; then
    echo -e "  ${GREEN}✅${NC} Quick reference guide"
    ((DOC_COUNT++))
fi

if [ -f ".claude/docs/AGENT_ALIAS_PATTERNS.md" ]; then
    echo -e "  ${GREEN}✅${NC} Alias patterns guide"
    ((DOC_COUNT++))
fi

if [ -f ".claude/agents/agent-tool-specifications.md" ]; then
    echo -e "  ${GREEN}✅${NC} Tool specifications"
    ((DOC_COUNT++))
fi

if [ $DOC_COUNT -ge 2 ]; then
    echo -e "${GREEN}✅ PASSED${NC}: Documentation complete"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}⚠️ WARNING${NC}: Some documentation missing"
fi

# Summary
echo -e "\n${YELLOW}========================================${NC}"
echo -e "${YELLOW}Test Summary${NC}"
echo -e "${YELLOW}========================================${NC}"
echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}✨ All tests passed! Sub-agent system is ready.${NC}"
    echo -e "\n📝 Usage examples:"
    echo "  use security-threat-analyst subagent to analyze auth system"
    echo "  sa check for SQL injection vulnerabilities"
    echo "  pm orchestrate user profile feature"
    echo "  chain security-audit-chain"
    exit 0
else
    echo -e "\n${RED}⚠️ Some tests failed. Please check the output above.${NC}"
    exit 1
fi
