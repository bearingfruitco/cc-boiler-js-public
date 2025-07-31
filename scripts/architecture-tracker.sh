#!/bin/bash

# Architecture Tracker Script
# Simplifies using the architecture change tracker

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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
    npx ts-node lib/architecture-tracker/cli.ts "$@"
}

# Main script logic
case "$1" in
    init)
        echo -e "${GREEN}Initializing architecture tracking...${NC}"
        run_cli init
        ;;
    record)
        echo -e "${GREEN}Recording architecture change...${NC}"
        run_cli record --interactive
        ;;
    list)
        shift
        run_cli list "$@"
        ;;
    impact)
        echo -e "${GREEN}Running impact analysis...${NC}"
        run_cli impact --interactive
        ;;
    adr)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Please provide a change ID${NC}"
            echo "Usage: $0 adr <change-id>"
            exit 1
        fi
        run_cli adr "$2"
        ;;
    diff)
        shift
        run_cli diff "$@"
        ;;
    help|--help|-h)
        echo "Architecture Tracker - Track and manage architecture changes"
        echo ""
        echo "Usage: $0 <command> [options]"
        echo ""
        echo "Commands:"
        echo "  init              Initialize architecture tracking"
        echo "  record            Record a new architecture change (interactive)"
        echo "  list [options]    List architecture changes"
        echo "    --since <date>    Show changes since date"
        echo "    --until <date>    Show changes until date"
        echo "    --category <cat>  Filter by category"
        echo "    --component <id>  Show changes for component"
        echo "  impact            Analyze impact of proposed change (interactive)"
        echo "  adr <id>          Generate ADR for a change"
        echo "  diff              Show architecture differences"
        echo "    --from <date>     From date (required)"
        echo "    --to <date>       To date (required)"
        echo "  help              Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0 init"
        echo "  $0 record"
        echo "  $0 list --since \"2024-01-01\""
        echo "  $0 list --category backend"
        echo "  $0 impact"
        echo "  $0 adr arch-change-20240115-a7x9k"
        echo "  $0 diff --from \"2024-01-01\" --to \"2024-02-01\""
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
