#!/bin/bash
cd /Users/shawnsmith/dev/bfc/boilerplate
echo "Running Claude Code /doctor command..."
echo "/doctor" | claude-code 2>&1 | grep -A 20 -B 5 "invalid settings"
