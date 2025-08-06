#!/bin/bash

# ============================================================================
# Claude Code Boilerplate Quick Integration
# 
# Downloads and runs the integration wizard
# ============================================================================

set -e

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}Claude Code Boilerplate Integration${NC}"
echo "===================================="
echo ""

# Create temp directory
TEMP_DIR="/tmp/claude-integration-$$"
mkdir -p "$TEMP_DIR"

# Download the integration wizard
echo -e "${YELLOW}Downloading integration wizard...${NC}"
curl -sSL https://raw.githubusercontent.com/bearingfruitco/cc-boiler-js-public/main/scripts/integration-wizard.sh -o "$TEMP_DIR/wizard.sh"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Downloaded successfully${NC}"
    echo ""
    
    # Make executable
    chmod +x "$TEMP_DIR/wizard.sh"
    
    # Run the wizard
    exec bash "$TEMP_DIR/wizard.sh"
else
    echo -e "${RED}✗ Failed to download integration wizard${NC}"
    echo "Please check your internet connection and try again."
    exit 1
fi
