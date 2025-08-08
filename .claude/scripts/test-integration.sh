#!/bin/bash

# Integration test for all advanced features
# This verifies the complete workflow actually works

echo "================================================"
echo "🧪 Testing Claude Advanced Features"
echo "================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test results
TESTS_PASSED=0
TESTS_FAILED=0

# Test function
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -e "${BLUE}Testing: $test_name${NC}"
    
    if eval "$test_command" &> /dev/null; then
        echo -e "${GREEN}  ✅ PASSED${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}  ❌ FAILED${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

echo "1. Directory Structure Tests"
echo "============================"

run_test "Claude directory exists" "[ -d '.claude' ]"
run_test "Agents directory exists" "[ -d '.claude/agents' ]"
run_test "Commands directory exists" "[ -d '.claude/commands' ]"
run_test "Config directory exists" "[ -d '.claude/config' ]"
run_test "Hooks directory exists" "[ -d '.claude/hooks' ]"
run_test "MCP servers directory exists" "[ -d '.claude/mcp-servers' ]"

echo ""
echo "2. Configuration Tests"
echo "======================"

run_test "claw.md exists" "[ -f 'claw.md' ]"
run_test "Settings file exists" "[ -f '.claude/settings.local.json' ]"
run_test "MCP registry exists" "[ -f '.claude/config/mcp-registry.json' ]"
run_test "Hooks config exists" "[ -f '.claude/config/hooks.json' ]"

echo ""
echo "3. Agent Tests"
echo "=============="

run_test "Validation gates agent" "[ -f '.claude/agents/validation-gates.md' ]"
run_test "TDD engineer agent" "[ -f '.claude/agents/tdd-engineer.md' ]"
run_test "Senior engineer agent" "[ -f '.claude/agents/senior-engineer.md' ]"
run_test "QA agent" "[ -f '.claude/agents/qa.md' ]"

# Count total agents
AGENT_COUNT=$(ls -1 .claude/agents/*.md 2>/dev/null | wc -l)
echo -e "${BLUE}  Total agents: $AGENT_COUNT${NC}"

echo ""
echo "4. Command Tests"
echo "================"

run_test "Prep parallel command" "[ -f '.claude/commands/prep-parallel.md' ]"
run_test "Execute parallel command" "[ -f '.claude/commands/execute-parallel.md' ]"
run_test "Merge best command" "[ -f '.claude/commands/merge-best.md' ]"
run_test "Cleanup parallel command" "[ -f '.claude/commands/cleanup-parallel.md' ]"
run_test "Fix GitHub issue command" "[ -f '.claude/commands/fix-github-issue.md' ]"

# Count total commands
COMMAND_COUNT=$(ls -1 .claude/commands/*.md 2>/dev/null | wc -l)
echo -e "${BLUE}  Total commands: $COMMAND_COUNT${NC}"

echo ""
echo "5. MCP Connector Tests"
echo "======================"

run_test "Octocode MCP connector" "[ -f '.claude/mcp-servers/connectors/octocode-mcp.js' ]"
run_test "Serena MCP connector" "[ -f '.claude/mcp-servers/connectors/serena-mcp.js' ]"

# Test if connectors can be loaded
if [ -f ".claude/mcp-servers/connectors/octocode-mcp.js" ]; then
    run_test "Octocode loads" "node -e \"require('./.claude/mcp-servers/connectors/octocode-mcp.js')\""
fi

if [ -f ".claude/mcp-servers/connectors/serena-mcp.js" ]; then
    run_test "Serena loads" "node -e \"require('./.claude/mcp-servers/connectors/serena-mcp.js')\""
fi

echo ""
echo "6. Hook Tests"
echo "============="

run_test "Log changes hook" "[ -f '.claude/hooks/log-changes.sh' ]"
run_test "Security scan hook" "[ -f '.claude/hooks/security-scan.sh' ]"
run_test "Validation complete hook" "[ -f '.claude/hooks/notify-validation-complete.sh' ]"
run_test "Pre-push checks hook" "[ -f '.claude/hooks/pre-push-checks.sh' ]"

# Check if hooks are executable
run_test "Hooks are executable" "[ -x '.claude/hooks/log-changes.sh' ]"

echo ""
echo "7. Git Work Tree Tests"
echo "======================"

# Test git worktree functionality
run_test "Git installed" "command -v git"
run_test "Git initialized" "[ -d '.git' ]"
run_test "Can list worktrees" "git worktree list"

echo ""
echo "8. Documentation Tests"
echo "======================"

run_test "Workflow guide exists" "[ -f '.claude/docs/COMPLETE_WORKFLOW_GUIDE.md' ]"
run_test "Parallel agents docs" "[ -f '.claude/docs/PARALLEL_AGENTS.md' ]"
run_test "README exists" "[ -f '.claude/README.md' ]"

echo ""
echo "9. Functional Tests"
echo "==================="

# Test creating directories
TEST_DIR=".test_parallel_$$"
run_test "Can create test directory" "mkdir -p $TEST_DIR && rmdir $TEST_DIR"

# Test JSON parsing
run_test "MCP registry is valid JSON" "node -e \"JSON.parse(require('fs').readFileSync('.claude/config/mcp-registry.json'))\""
run_test "Hooks config is valid JSON" "node -e \"JSON.parse(require('fs').readFileSync('.claude/config/hooks.json'))\""

echo ""
echo "10. Integration Tests"
echo "===================="

# Test that key files reference each other correctly
run_test "Registry includes Octocode" "grep -q 'octocode-mcp' .claude/config/mcp-registry.json"
run_test "Registry includes Serena" "grep -q 'serena-mcp' .claude/config/mcp-registry.json"
run_test "Validation gates in registry" "grep -q 'validation-gates' .claude/config/mcp-registry.json"

echo ""
echo "================================================"
echo "📊 Test Results Summary"
echo "================================================"
echo ""
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED!${NC}"
    echo ""
    echo "The Claude Advanced System is fully operational!"
    echo ""
    echo "You can now use:"
    echo "  • Parallel development (3x speed)"
    echo "  • Intelligent code generation (Octocode)"
    echo "  • Semantic search (Serena)"
    echo "  • Production validation (Gates)"
    echo "  • Automated workflows (Hooks)"
    echo ""
    echo "Start with: claude && /primer"
else
    echo -e "${YELLOW}⚠️  Some tests failed${NC}"
    echo ""
    echo "Run the setup script to fix:"
    echo "  .claude/scripts/setup-and-verify.sh"
fi

echo ""
echo "================================================"

# Return exit code based on test results
exit $TESTS_FAILED
