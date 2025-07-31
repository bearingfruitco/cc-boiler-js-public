# Issue #16: Clean Up Duplicate Files and Consolidate Configuration

## Overview
Critical cleanup needed - the .claude directory contains many duplicate files, old versions, and scattered documentation that needs consolidation. This is causing confusion and making the system harder to maintain.

## Problem Statement
We have multiple issues:
- Duplicate configuration files with similar names
- Backup files mixed with active files
- Documentation scattered across multiple directories
- Old/outdated files not properly archived
- Unclear which files are the "source of truth"

## Files Needing Cleanup

### Duplicate/Redundant Files in .claude/
```
Configuration Files:
- chains.json (active)
- chains-enhanced.json (duplicate?)
- chains.json.backup (should be in backups/)

- config.json
- project-config.json (which is primary?)
- optimization-config.json (appears twice in list)
- tdd-config.json
- tcpa.config.json (should these be consolidated?)

Command Registry:
- command-registry.json
- command-registry-updated.json (appears twice)

Aliases:
- aliases.json (active)
- aliases.backup.json
- aliases-recommended.json
- aliases-recommended 2.json (space in filename!)
- aliases-clean.json

Documentation:
- IMPLEMENTATION_COMPLETE.md (should be in docs?)
```

### Directories Needing Review
```
.claude/
├── docs/              # Should this be consolidated with /docs?
├── troubleshooting/   # Should be in /docs/troubleshooting?
├── scripts/           # Should be in /scripts?
├── release/           # Should be in /docs/releases?
├── hooks/             # Contains docs that need cleaning
```

## Cleanup Plan

### Phase 1: Backup Everything
1. Create `.claude/archive/cleanup-backup-[timestamp]/`
2. Copy ALL files before making changes
3. Document what was where

### Phase 2: Consolidate Configuration
1. **Chains**: 
   - Keep `chains.json` as primary
   - Archive `chains-enhanced.json` if outdated
   - Move `chains.json.backup` to backups/
   
2. **Config Files**:
   - Determine primary config structure
   - Merge related configs if possible
   - Create single `config.json` with sections
   
3. **Command Registry**:
   - Keep latest version only
   - Archive older versions

4. **Aliases**:
   - Keep `aliases.json` as primary
   - Archive all others
   - Fix filename with space

### Phase 3: Reorganize Documentation
1. Move `.claude/docs/` content to main `/docs/claude/`
2. Move `.claude/troubleshooting/` to `/docs/troubleshooting/`
3. Move `.claude/release/` to `/docs/releases/`
4. Clean up hook documentation in `.claude/hooks/`

### Phase 4: Script Organization
1. Evaluate scripts in `.claude/scripts/`
2. Move to main `/scripts/claude/` if needed
3. Remove duplicates

### Phase 5: Create Structure Documentation
```
.claude/
├── agents/            # Sub-agents (keep here)
├── commands/          # Custom commands (keep here)
├── hooks/             # Hook scripts only (no docs)
├── backups/           # All backup files
├── archive/           # Old/deprecated files
├── config/            # All configuration files
│   ├── main.json      # Primary config
│   ├── aliases.json   # Command aliases
│   └── chains.json    # Workflow chains
└── README.md          # Explains structure
```

## Success Criteria
- [ ] No duplicate files in .claude/
- [ ] Clear file naming (no spaces)
- [ ] All configs in one place
- [ ] Documentation properly organized
- [ ] Backup of everything before changes
- [ ] README explaining new structure
- [ ] No "updated" or "clean" versions - just one primary

## Benefits
1. **Clarity**: Know which file is the source of truth
2. **Maintainability**: Easier to update configurations
3. **Discoverability**: Find files where expected
4. **Performance**: Less files to search through
5. **Onboarding**: New developers understand structure

## Risks & Mitigation
- **Risk**: Breaking existing functionality
  - **Mitigation**: Complete backup, test after each phase
  
- **Risk**: Losing important variations
  - **Mitigation**: Archive everything, document differences

- **Risk**: Commands/hooks breaking
  - **Mitigation**: Update all references, test thoroughly

## Implementation Order
1. Create comprehensive backup
2. Document current state
3. Consolidate configs
4. Reorganize docs
5. Clean scripts
6. Update references
7. Test everything
8. Document new structure

## Priority: HIGH 🔴
This cleanup is essential for system maintainability and directly impacts developer experience.
