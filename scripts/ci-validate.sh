#!/usr/bin/env bash

# Claude Code CI/CD Validation Script
# 
# This script runs Claude Code quality gates in non-interactive mode
# suitable for CI/CD pipelines.
#
# Usage: ./scripts/ci-validate.sh [all|design|security|stage|deps|tests]

set -e

# Colors for output (disabled in CI)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    NC=''
fi

# Check if Claude Code is installed
if ! command -v claude &> /dev/null; then
    echo -e "${RED}Error: Claude Code is not installed${NC}"
    echo "Run: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${RED}Error: ANTHROPIC_API_KEY environment variable not set${NC}"
    exit 1
fi

# Set non-interactive mode
export CLAUDE_NON_INTERACTIVE=true

# Default to running all checks
CHECKS="${1:-all}"

# Track overall status
OVERALL_STATUS=0

# Helper function to run a check
run_check() {
    local name=$1
    local command=$2
    local output_file="${3:-${name}-results.json}"
    
    echo -e "\n${YELLOW}Running ${name}...${NC}"
    
    if claude --non-interactive "$command" > "$output_file" 2>&1; then
        echo -e "${GREEN}✓ ${name} passed${NC}"
        
        # Show summary if available
        if [ -f "$output_file" ] && command -v jq &> /dev/null; then
            if [ "$name" = "Design Validation" ]; then
                violations=$(jq -r '.totalViolations // 0' "$output_file" 2>/dev/null || echo "0")
                echo "  No violations found"
            elif [ "$name" = "Stage Validation" ]; then
                progress=$(jq -r '.progress // 0' "$output_file" 2>/dev/null || echo "0")
                echo "  Progress: ${progress}%"
            elif [ "$name" = "Security Check" ]; then
                issues=$(jq -r '.issues // 0' "$output_file" 2>/dev/null || echo "0")
                if [ "$issues" = "0" ]; then
                    echo "  No security issues found"
                fi
            fi
        fi
    else
        echo -e "${RED}✗ ${name} failed${NC}"
        OVERALL_STATUS=1
        
        # Show error details if available
        if [ -f "$output_file" ] && command -v jq &> /dev/null; then
            error=$(jq -r '.error // .message // "Unknown error"' "$output_file" 2>/dev/null)
            echo "  Error: $error"
        fi
    fi
}

# Create results directory
mkdir -p ci-results

# Run checks based on argument
case $CHECKS in
    all)
        echo "Running all quality gates..."
        run_check "Design Validation" "/validate-design all" "ci-results/design-results.json"
        run_check "Stage Validation" "/stage-validate check current" "ci-results/stage-results.json"
        run_check "Security Check" "/security-check all" "ci-results/security-results.json"
        run_check "Dependency Scan" "/deps scan" "ci-results/deps-results.json"
        run_check "Test Runner" "/test-runner all" "ci-results/test-results.json"
        run_check "Async Validation" "/validate-async" "ci-results/async-results.json"
        
        # Check for active PRPs
        if [ -d "PRPs/active" ] && [ "$(ls -A PRPs/active 2>/dev/null)" ]; then
            run_check "PRP Validation" "/prp-execute --level 1" "ci-results/prp-results.json"
        fi
        ;;
    design)
        run_check "Design Validation" "/validate-design all" "ci-results/design-results.json"
        ;;
    security)
        run_check "Security Check" "/security-check all" "ci-results/security-results.json"
        ;;
    stage)
        run_check "Stage Validation" "/stage-validate check current" "ci-results/stage-results.json"
        ;;
    deps)
        run_check "Dependency Scan" "/deps scan" "ci-results/deps-results.json"
        ;;
    tests)
        run_check "Test Runner" "/test-runner all" "ci-results/test-results.json"
        ;;
    *)
        echo -e "${RED}Unknown check: $CHECKS${NC}"
        echo "Usage: $0 [all|design|security|stage|deps|tests]"
        exit 1
        ;;
esac

# Generate summary report
echo -e "\n${YELLOW}=== Quality Gates Summary ===${NC}"
echo "Results saved to: ci-results/"

if [ -d "ci-results" ] && command -v jq &> /dev/null; then
    # Count passes and failures
    total_checks=$(ls ci-results/*.json 2>/dev/null | wc -l)
    failed_checks=0
    
    for result in ci-results/*.json; do
        if [ -f "$result" ]; then
            success=$(jq -r '.success // .status // "unknown"' "$result" 2>/dev/null)
            if [ "$success" != "true" ] && [ "$success" != "passed" ] && [ "$success" != "complete" ]; then
                failed_checks=$((failed_checks + 1))
            fi
        fi
    done
    
    passed_checks=$((total_checks - failed_checks))
    
    echo "Total checks: $total_checks"
    echo -e "${GREEN}Passed: $passed_checks${NC}"
    if [ $failed_checks -gt 0 ]; then
        echo -e "${RED}Failed: $failed_checks${NC}"
    fi
fi

# Exit with overall status
if [ $OVERALL_STATUS -eq 0 ]; then
    echo -e "\n${GREEN}All quality gates passed!${NC}"
else
    echo -e "\n${RED}Some quality gates failed. See results above.${NC}"
fi

exit $OVERALL_STATUS
