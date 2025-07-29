#!/bin/bash

# Test Architecture Enhancement Implementation
# This script verifies that the architecture phase is properly implemented

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🧪 Testing Architecture Enhancement Implementation${NC}"
echo ""

# Test directories
BOILERPLATE="/Users/shawnsmith/dev/bfc/boilerplate"
DEBT_TOFU="/Users/shawnsmith/dev/bfc/debt-tofu-report"

# Function to check file exists
check_file() {
    local file=$1
    local desc=$2
    if [ -f "$file" ]; then
        echo -e "✅ $desc exists"
        return 0
    else
        echo -e "❌ $desc missing: $file"
        return 1
    fi
}

# Function to check command in registry
check_command_registry() {
    local dir=$1
    local cmd=$2
    if grep -q "\"$cmd\"" "$dir/.claude/command-registry.json" 2>/dev/null; then
        echo -e "✅ $cmd registered in $(basename $dir)"
    else
        echo -e "❌ $cmd not registered in $(basename $dir)"
    fi
}

# Function to check alias
check_alias() {
    local dir=$1
    local alias=$2
    local target=$3
    if grep -q "\"$alias\": \"$target\"" "$dir/.claude/aliases.json" 2>/dev/null; then
        echo -e "✅ Alias $alias → $target in $(basename $dir)"
    else
        echo -e "❌ Alias $alias missing in $(basename $dir)"
    fi
}

echo -e "${YELLOW}1. Checking Commands${NC}"
for dir in "$BOILERPLATE" "$DEBT_TOFU"; do
    echo "  In $(basename $dir):"
    check_file "$dir/.claude/commands/create-architecture.md" "create-architecture command"
    check_file "$dir/.claude/commands/validate-architecture.md" "validate-architecture command"
    check_command_registry "$dir" "create-architecture"
    check_command_registry "$dir" "validate-architecture"
    echo ""
done

echo -e "${YELLOW}2. Checking Aliases${NC}"
for dir in "$BOILERPLATE" "$DEBT_TOFU"; do
    echo "  In $(basename $dir):"
    check_alias "$dir" "arch" "create-architecture"
    check_alias "$dir" "va" "validate-architecture"
    echo ""
done

echo -e "${YELLOW}3. Checking Agent${NC}"
for dir in "$BOILERPLATE" "$DEBT_TOFU"; do
    check_file "$dir/.claude/agents/system-architect.md" "system-architect agent ($(basename $dir))"
done
echo ""

echo -e "${YELLOW}4. Checking Templates${NC}"
templates=(
    "SYSTEM_DESIGN.md"
    "DATABASE_SCHEMA.md"
    "API_SPECIFICATION.md"
    "FRONTEND_ARCHITECTURE.md"
    "SECURITY_DESIGN.md"
    "TECHNICAL_ROADMAP.md"
)
for dir in "$BOILERPLATE" "$DEBT_TOFU"; do
    echo "  In $(basename $dir):"
    for template in "${templates[@]}"; do
        if [ -f "$dir/.claude/templates/architecture/$template" ]; then
            echo -e "    ✅ $template"
        else
            echo -e "    ❌ $template missing"
        fi
    done
    echo ""
done

echo -e "${YELLOW}5. Checking Hooks${NC}"
for dir in "$BOILERPLATE" "$DEBT_TOFU"; do
    echo "  In $(basename $dir):"
    check_file "$dir/.claude/hooks/pre-tool-use/17-architecture-enforcer.py" "architecture enforcer hook"
    check_file "$dir/.claude/hooks/post-tool-use/04a-architecture-suggester.py" "architecture suggester hook"
    # Check if executable
    if [ -x "$dir/.claude/hooks/pre-tool-use/17-architecture-enforcer.py" ]; then
        echo -e "    ✅ Enforcer hook is executable"
    else
        echo -e "    ❌ Enforcer hook not executable"
    fi
    echo ""
done

echo -e "${YELLOW}6. Checking Chain${NC}"
for dir in "$BOILERPLATE" "$DEBT_TOFU"; do
    if grep -q "architecture-design" "$dir/.claude/chains.json" 2>/dev/null; then
        echo -e "✅ architecture-design chain exists in $(basename $dir)"
        if grep -q "\"ad\": \"architecture-design\"" "$dir/.claude/chains.json" 2>/dev/null; then
            echo -e "✅ Shortcut 'ad' configured in $(basename $dir)"
        else
            echo -e "❌ Shortcut 'ad' missing in $(basename $dir)"
        fi
    else
        echo -e "❌ architecture-design chain missing in $(basename $dir)"
    fi
done
echo ""

echo -e "${YELLOW}7. Testing Scenario: Debt-Tofu-Report${NC}"
if [ -f "$DEBT_TOFU/docs/project/PROJECT_PRD.md" ]; then
    echo -e "✅ PRD exists"
else
    echo -e "❌ PRD missing"
fi

if [ -d "$DEBT_TOFU/docs/architecture" ]; then
    echo -e "❌ Architecture directory already exists (should not exist for test)"
else
    echo -e "✅ Architecture directory missing (correct for test scenario)"
fi

echo ""
echo -e "${GREEN}🎯 Summary${NC}"
echo "The architecture enhancement should:"
echo "1. Block '/gi PROJECT' command when PRD exists but architecture is missing"
echo "2. Suggest '/arch' or '/chain architecture-design' commands"
echo "3. Guide through architecture design process"
echo "4. Generate 6 architecture documents"
echo "5. Create component PRPs automatically"
echo ""
echo "To test in debt-tofu-report:"
echo "  cd $DEBT_TOFU"
echo "  /gi PROJECT  # Should be blocked"
echo "  /arch        # Should start architecture design"
