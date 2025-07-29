#!/bin/bash
# Make all environment hooks executable

chmod +x .claude/hooks/pre-tool-use/24-environment-guard.py
chmod +x .claude/hooks/pre-tool-use/25-deployment-validator.py
chmod +x .claude/hooks/pre-tool-use/26-database-environment-check.py
chmod +x .claude/hooks/notification/environment-awareness.py
chmod +x scripts/migrate.ts
chmod +x scripts/seed.ts
chmod +x scripts/env-switch.js
chmod +x scripts/setup-environments.sh

echo "✅ All environment hooks are now executable"
