#!/bin/bash

# Log validation completion
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
LOG_DIR=".claude/logs"
LOG_FILE="$LOG_DIR/validation.log"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Log the validation
echo "[$TIMESTAMP] Validation gates completed" >> "$LOG_FILE"
echo "✅ Validation gates completed and logged"
