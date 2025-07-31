# Claude Code Settings Backup Log
Date: 2025-07-27 12:39:29

## Backups Available:

1. **Full System Backup**
   - Location: /Users/shawnsmith/dev/bfc/boilerplate/.claude.full_backup_20250727_102756/
   - Contains: Complete .claude directory with all 70+ hooks, commands, configs
   - Created: 2025-07-27 10:27:56

2. **Pre-Fix Working Settings**
   - Location: /Users/shawnsmith/dev/bfc/boilerplate/.claude/settings-backup-2025_07_27_123929.json
   - Contains: Minimal working configuration (no hooks)
   - Status: Known working state

3. **Fixed Configuration Ready**
   - Location: /Users/shawnsmith/dev/bfc/boilerplate/.claude/settings-fixed.json
   - Contains: All 70+ hooks with corrected matcher format
   - Status: Ready to apply

## To Restore if Needed:
```bash
# Restore to minimal working state
cp .claude/settings-backup-2025_07_27_123929.json .claude/settings.json

# Or restore from full backup
cp .claude.full_backup_20250727_102756/settings.json .claude/settings.json
```
