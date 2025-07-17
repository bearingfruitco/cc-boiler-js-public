#!/bin/bash

# Make PRP runner executable
chmod +x PRPs/scripts/prp-runner.ts

# Install any needed dependencies (if not already installed)
if ! command -v bun &> /dev/null; then
    echo "Bun is required but not installed. Please install Bun first."
    echo "Run: curl -fsSL https://bun.sh/install | bash"
    exit 1
fi

echo "✅ PRP system setup complete!"
echo ""
echo "Quick start commands:"
echo "  /create-prp [feature]  - Create a new PRP"
echo "  /prp-execute [name]    - Run validation loops"
echo "  /prp [feature]         - Alias for create-prp"
echo ""
echo "Example:"
echo "  /prp user authentication with JWT"
echo "  /prp-execute user-authentication"
