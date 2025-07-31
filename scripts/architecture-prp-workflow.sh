#!/bin/bash

# Architecture-PRP Integration Script
# Workflow for architecture changes that affect PRPs

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Function to display workflow header
show_header() {
    echo -e "${CYAN}================================${NC}"
    echo -e "${CYAN}Architecture-PRP Workflow${NC}"
    echo -e "${CYAN}================================${NC}"
    echo ""
}

# Function to run architecture tracker
run_arch_tracker() {
    "$SCRIPT_DIR/architecture-tracker.sh" "$@"
}

# Function to run PRP sync
run_prp_sync() {
    "$SCRIPT_DIR/prp-sync.sh" "$@"
}

# Main workflow
case "$1" in
    record-and-sync)
        show_header
        echo -e "${BLUE}Step 1: Recording architecture change...${NC}"
        run_arch_tracker record
        
        echo -e "\n${BLUE}Step 2: Analyzing PRP impact...${NC}"
        run_prp_sync analyze
        
        echo -e "\n${YELLOW}Would you like to update affected PRPs? (y/n)${NC}"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            echo -e "\n${BLUE}Step 3: Updating PRPs...${NC}"
            run_prp_sync update
        fi
        ;;
        
    analyze-all)
        show_header
        echo -e "${BLUE}Analyzing all architecture changes and PRP status...${NC}\n"
        
        echo -e "${YELLOW}Architecture Changes:${NC}"
        run_arch_tracker list --since "30 days ago"
        
        echo -e "\n${YELLOW}PRP Synchronization Status:${NC}"
        run_prp_sync status
        
        echo -e "\n${YELLOW}Impact Analysis:${NC}"
        run_prp_sync analyze
        ;;
        
    full-sync)
        show_header
        echo -e "${YELLOW}This will:${NC}"
        echo "1. List recent architecture changes"
        echo "2. Show PRP sync status"
        echo "3. Update all affected PRPs"
        echo ""
        echo -e "${YELLOW}Continue? (y/n)${NC}"
        read -r response
        
        if [[ "$response" =~ ^[Yy]$ ]]; then
            echo -e "\n${BLUE}Step 1: Recent architecture changes...${NC}"
            run_arch_tracker list --since "7 days ago"
            
            echo -e "\n${BLUE}Step 2: PRP sync status...${NC}"
            run_prp_sync status
            
            echo -e "\n${BLUE}Step 3: Updating PRPs...${NC}"
            run_prp_sync sync-all
        fi
        ;;
        
    impact)
        show_header
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Please specify a component${NC}"
            echo "Usage: $0 impact <component-name>"
            exit 1
        fi
        
        echo -e "${BLUE}Analyzing impact for component: $2${NC}\n"
        
        echo -e "${YELLOW}Architecture changes affecting $2:${NC}"
        run_arch_tracker list --component "$2"
        
        echo -e "\n${YELLOW}PRP status for $2:${NC}"
        # This would check specific PRP status
        prp_file="$2-prp.md"
        if [ -f "$PROJECT_ROOT/PRPs/$prp_file" ]; then
            echo -e "${GREEN}✓ PRP exists: $prp_file${NC}"
            run_prp_sync analyze | grep -A5 "$prp_file" || echo "PRP is up to date"
        else
            echo -e "${RED}✗ PRP missing: $prp_file${NC}"
        fi
        ;;
        
    validate)
        show_header
        echo -e "${BLUE}Validating architecture-PRP alignment...${NC}\n"
        
        # Check for recent unsynced changes
        echo -e "${YELLOW}Recent architecture changes (last 7 days):${NC}"
        recent_changes=$(run_arch_tracker list --since "7 days ago" | grep -c "arch-change")
        echo "Found $recent_changes changes"
        
        # Check PRP sync status
        echo -e "\n${YELLOW}PRP synchronization:${NC}"
        run_prp_sync status
        
        # Provide recommendation
        echo -e "\n${CYAN}Recommendation:${NC}"
        outdated=$(run_prp_sync status | grep "Outdated:" | awk '{print $2}')
        if [ "$outdated" -gt 0 ]; then
            echo -e "${YELLOW}⚠️  $outdated PRPs need updating${NC}"
            echo "Run: $0 full-sync"
        else
            echo -e "${GREEN}✓ All PRPs are synchronized${NC}"
        fi
        ;;
        
    help|--help|-h)
        show_header
        echo "Integrated workflow for architecture changes and PRP updates"
        echo ""
        echo "Usage: $0 <command> [options]"
        echo ""
        echo "Commands:"
        echo "  record-and-sync    Record architecture change and update PRPs"
        echo "  analyze-all        Show all changes and sync status"
        echo "  full-sync          Complete synchronization workflow"
        echo "  impact <component> Analyze impact on specific component"
        echo "  validate           Check architecture-PRP alignment"
        echo "  help               Show this help message"
        echo ""
        echo "Workflow Examples:"
        echo ""
        echo "1. After making architecture changes:"
        echo "   $0 record-and-sync"
        echo ""
        echo "2. Weekly maintenance check:"
        echo "   $0 validate"
        echo ""
        echo "3. Full synchronization:"
        echo "   $0 full-sync"
        echo ""
        echo "4. Component-specific analysis:"
        echo "   $0 impact authentication-service"
        ;;
        
    *)
        show_header
        echo -e "${RED}Unknown command: $1${NC}"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac

echo -e "\n${CYAN}================================${NC}"
