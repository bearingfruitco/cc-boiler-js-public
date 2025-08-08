#!/bin/bash

# Log code changes
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
LOG_DIR=".claude/logs"
LOG_FILE="$LOG_DIR/changes.log"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Log the change
echo "[$TIMESTAMP] Code changes made by Claude" >> "$LOG_FILE"

# Count changed files
CHANGED_FILES=$(git status --porcelain | wc -l)
echo "  Changed files: $CHANGED_FILES" >> "$LOG_FILE"
