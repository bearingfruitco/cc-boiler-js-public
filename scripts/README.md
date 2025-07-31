# Scripts Directory

This directory contains all utility and maintenance scripts for the Claude Code Boilerplate system.

## Directory Structure

```
scripts/
├── maintenance/     # Scripts for maintaining and analyzing the system
├── setup/          # Setup and installation scripts
├── git/            # Git workflow automation scripts
├── tests/          # Test-related scripts
└── *.sh/py         # Core scripts (architecture, PRP, docs)
```

## Subdirectories

### /maintenance
Scripts for system maintenance and analysis:
- `analyze-alias-duplication.py` - Find and remove duplicate command aliases
- `analyze-commands.py` - Analyze command usage and structure
- `clean-aliases.sh` - Clean up excessive aliases
- `create-all-aliases.sh` - Generate all command aliases
- `fix-commands.sh` - Fix command file issues

### /setup
Installation and setup scripts:
- `complete-playwright-integration.sh` - Set up Playwright for browser testing
- Various initialization scripts

### /git
Git workflow automation:
- `execute-push.sh` - Execute git push operations
- `push-to-both-repos.sh` - Push to both private and public repositories

### /tests
Test automation scripts:
- `test-integration-docs.sh` - Test documentation integration

## Core Scripts

In the main scripts directory:
- Architecture tracking scripts
- PRP synchronization scripts
- Documentation automation scripts
- V4 system initialization scripts

## Usage

Most scripts can be run directly:
```bash
./scripts/maintenance/analyze-aliases.py
./scripts/setup/complete-playwright-integration.sh
```

Some scripts are called by npm commands:
```bash
npm run architecture:init   # Calls architecture scripts
npm run docs:watch         # Calls documentation scripts
```

## Adding New Scripts

When adding new scripts:
1. Place in appropriate subdirectory
2. Make executable: `chmod +x script-name.sh`
3. Add documentation here
4. Update any related npm scripts in package.json
