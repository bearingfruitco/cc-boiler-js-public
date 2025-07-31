#!/bin/bash

# Documentation Updater Script
# Automatically updates documentation based on code changes

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if node is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    exit 1
fi

# Check if ts-node is installed
if ! command -v npx ts-node &> /dev/null; then
    echo -e "${YELLOW}Installing ts-node...${NC}"
    npm install -D ts-node
fi

# Function to run the CLI
run_cli() {
    cd "$PROJECT_ROOT"
    npx ts-node lib/doc-updater/cli.ts "$@"
}

# Main script logic
case "$1" in
    init)
        echo -e "${BLUE}Initializing documentation structure...${NC}"
        run_cli init
        ;;
    update)
        shift
        echo -e "${BLUE}Updating documentation...${NC}"
        run_cli update "$@"
        ;;
    watch)
        echo -e "${BLUE}Starting documentation watcher...${NC}"
        echo -e "${CYAN}Documentation will auto-update as you code${NC}"
        run_cli watch
        ;;
    check)
        echo -e "${BLUE}Checking documentation status...${NC}"
        run_cli check
        ;;
    analyze)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Please provide a file to analyze${NC}"
            echo "Usage: $0 analyze <file>"
            exit 1
        fi
        echo -e "${BLUE}Analyzing $2...${NC}"
        run_cli analyze "$2"
        ;;
    quick-update)
        echo -e "${YELLOW}Quick documentation update (components only)...${NC}"
        run_cli update --pattern "components/**/*.tsx"
        ;;
    full-update)
        echo -e "${YELLOW}Full documentation update...${NC}"
        run_cli update
        ;;
    dry-run)
        echo -e "${BLUE}Running documentation update preview...${NC}"
        run_cli update --dry-run
        ;;
    help|--help|-h)
        echo "Documentation Updater - Keep docs in sync with code"
        echo ""
        echo "Usage: $0 <command> [options]"
        echo ""
        echo "Commands:"
        echo "  init           Initialize documentation structure"
        echo "  update         Update documentation for changed files"
        echo "  watch          Watch files and auto-update docs"
        echo "  check          Check documentation coverage"
        echo "  analyze <file> Analyze what would be extracted"
        echo "  quick-update   Update component docs only"
        echo "  full-update    Update all documentation"
        echo "  dry-run        Preview updates without changes"
        echo "  help           Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0 init"
        echo "  $0 watch"
        echo "  $0 update components/Button.tsx"
        echo "  $0 check"
        echo "  $0 analyze lib/utils.ts"
        echo ""
        echo "Documentation Workflow:"
        echo "  1. Add JSDoc comments to your code"
        echo "  2. Run 'update' or enable 'watch' mode"
        echo "  3. Documentation is generated/updated"
        echo "  4. Custom sections are preserved"
        ;;
    *)
        if [ -z "$1" ]; then
            echo -e "${BLUE}Documentation Status:${NC}"
            run_cli check
            echo ""
            echo -e "${CYAN}Tip: Use '$0 watch' to enable auto-updates${NC}"
        else
            echo -e "${RED}Unknown command: $1${NC}"
            echo "Use '$0 help' for usage information"
            exit 1
        fi
        ;;
esac
