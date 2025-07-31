#!/bin/bash

# PRP Sync Script
# Synchronizes PRPs with architecture changes

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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
    npx ts-node lib/prp-regenerator/cli.ts "$@"
}

# Main script logic
case "$1" in
    status)
        echo -e "${BLUE}Checking PRP synchronization status...${NC}"
        run_cli status
        ;;
    analyze)
        shift
        echo -e "${BLUE}Analyzing architecture impact on PRPs...${NC}"
        run_cli analyze "$@"
        ;;
    update)
        echo -e "${BLUE}Updating PRPs based on architecture changes...${NC}"
        run_cli update --interactive
        ;;
    update-all)
        echo -e "${YELLOW}Updating ALL outdated PRPs...${NC}"
        run_cli update --all
        ;;
    sync-all)
        echo -e "${YELLOW}Synchronizing all PRPs with architecture...${NC}"
        run_cli sync-all
        ;;
    dry-run)
        echo -e "${BLUE}Running update preview (dry run)...${NC}"
        run_cli update --all --dry-run
        ;;
    restore)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Please provide a PRP file to restore${NC}"
            echo "Usage: $0 restore <prp-file>"
            exit 1
        fi
        run_cli restore "$2"
        ;;
    help|--help|-h)
        echo "PRP Sync - Synchronize PRPs with architecture changes"
        echo ""
        echo "Usage: $0 <command> [options]"
        echo ""
        echo "Commands:"
        echo "  status         Check synchronization status"
        echo "  analyze        Analyze which PRPs need updates"
        echo "    --since <date>  Analyze changes since date"
        echo "  update         Update PRPs interactively"
        echo "  update-all     Update all outdated PRPs"
        echo "  sync-all       Full synchronization"
        echo "  dry-run        Preview updates without changes"
        echo "  restore <file> Restore PRP from backup"
        echo "  help           Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0 status"
        echo "  $0 analyze --since \"2024-01-01\""
        echo "  $0 update"
        echo "  $0 dry-run"
        echo "  $0 restore authentication-service-prp.md"
        echo ""
        echo "Workflow:"
        echo "  1. Run 'status' to check current state"
        echo "  2. Run 'analyze' to see what needs updating"
        echo "  3. Run 'update' to interactively update PRPs"
        echo "  4. Or run 'sync-all' for full synchronization"
        ;;
    *)
        if [ -z "$1" ]; then
            echo -e "${BLUE}PRP Sync Status:${NC}"
            run_cli status
        else
            echo -e "${RED}Unknown command: $1${NC}"
            echo "Use '$0 help' for usage information"
            exit 1
        fi
        ;;
esac
