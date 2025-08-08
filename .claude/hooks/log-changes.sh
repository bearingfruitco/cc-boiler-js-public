#!/bin/bash

# Log all code changes to track what Claude is modifying

LOG_DIR=".claude/logs"
LOG_FILE="$LOG_DIR/changes-$(date +%Y%m%d).log"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Log the change with timestamp
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Code change detected" >> "$LOG_FILE"
echo "  Tool: ${TOOL_NAME:-unknown}" >> "$LOG_FILE"
echo "  File: ${FILE_PATH:-unknown}" >> "$LOG_FILE"
echo "  Agent: ${AGENT_NAME:-primary}" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"

# Keep only last 7 days of logs
find "$LOG_DIR" -name "changes-*.log" -mtime +7 -delete 2>/dev/null

exit 0
