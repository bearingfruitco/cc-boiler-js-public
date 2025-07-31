# .claude Directory Structure

> Last Updated: 2025-07-31
> Part of Issue #16: File Cleanup and Consolidation

## Directory Organization

```
.claude/
├── agents/              # Sub-agents for Claude Code
├── commands/            # Custom commands
├── hooks/               # Hook scripts (no docs)
├── config/              # All configuration files
│   ├── main.json        # Primary configuration
│   ├── aliases.json     # Command aliases
│   ├── chains.json      # Workflow chains
│   ├── command-registry.json
│   ├── feature-flags.json
│   ├── optimization-config.json
│   ├── security-config.json
│   ├── tcpa-config.json
│   └── tdd-config.json
├── backups/             # Backup files
├── archive/             # Old/deprecated files
└── [other active dirs]  # Various operational directories
```

## What Changed

### Moved to /config/
- All configuration JSON files now in one place
- Renamed `config.json` to `main.json` for clarity
- Removed duplicate versions

### Moved to /archive/
- chains-enhanced.json (outdated)
- aliases-clean.json
- aliases-recommended.json (and version with space in name)
- command-registry-updated.json
- project-config.json (template)

### Moved to /backups/
- chains.json.backup
- aliases.backup.json

### Relocated Documentation
- `.claude/docs/*` → `/docs/claude/`
- `.claude/troubleshooting/*` → `/scripts/claude/`
- `IMPLEMENTATION_COMPLETE.md` → `/docs/claude/`

## Configuration Files

### Core Configs
- **main.json**: Primary Claude configuration
- **aliases.json**: Command shortcuts and aliases
- **chains.json**: Multi-command workflows

### Feature Configs
- **feature-flags.json**: Enable/disable features
- **security-config.json**: Security settings
- **tdd-config.json**: Test-driven development settings
- **tcpa-config.json**: Type checking and analysis
- **optimization-config.json**: Performance optimizations

### Registry
- **command-registry.json**: All available commands

## Usage

All tools and commands should now reference configurations from the `/config/` subdirectory. For example:
- Old: `.claude/aliases.json`
- New: `.claude/config/aliases.json`

## Backup Policy

1. Active backups go in `/backups/`
2. Old versions go in `/archive/`
3. Temporary backups during major changes go in `/archive/cleanup-backup-[date]/`

## Notes

- No more duplicate files with "updated", "clean", or "recommended" in names
- All configs are now the single source of truth
- Documentation has been moved to the main docs structure
- Scripts have been moved to the main scripts structure
