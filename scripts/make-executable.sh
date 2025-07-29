#!/bin/bash

# Make all Python scripts executable
chmod +x scripts/*.py

echo "✅ Made all Python scripts executable"

# List all executable scripts
echo -e "\n📋 Executable scripts:"
ls -la scripts/*.py | grep -E "^-rwx"
