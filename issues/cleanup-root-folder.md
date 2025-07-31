# Root Folder Cleanup Issues

## Issue #1: Consolidate and Archive Cleanup Reports
**Priority**: High  
**Type**: Cleanup

### Description
Multiple cleanup-related markdown files in root need to be consolidated and moved to appropriate locations.

### Files to Handle
- `CLEANUP_ANALYSIS_REPORT.md` - Move to `.claude/archive/cleanup-reports/`
- `CLEANUP_COMPLETE.md` - Move to `.claude/archive/cleanup-reports/`
- `CLEANUP_SUMMARY_v4.0.1.md` - Keep in root as latest summary
- `COMMAND_CONSOLIDATION.md` - Move to `.claude/archive/cleanup-reports/`
- `ENHANCEMENT_SUMMARY.md` - Move to `docs/releases/`

### Tasks
- [ ] Create `.claude/archive/cleanup-reports/` directory
- [ ] Move historical cleanup files
- [ ] Update any references to these files
- [ ] Keep only essential cleanup summary in root

---

## Issue #2: Organize Analysis and Utility Scripts
**Priority**: Medium  
**Type**: Organization

### Description
Python and shell scripts for analysis should be in a proper scripts directory.

### Files to Handle
- `analyze-alias-duplication.py` - Move to `scripts/maintenance/`
- `analyze-commands.py` - Move to `scripts/maintenance/`
- `clean-aliases.sh` - Move to `scripts/maintenance/`
- `create-all-aliases.sh` - Move to `scripts/maintenance/`
- `complete-playwright-integration.sh` - Move to `scripts/setup/`
- `fix-commands.sh` - Move to `scripts/maintenance/`

### Tasks
- [ ] Create `scripts/maintenance/` directory
- [ ] Create `scripts/setup/` directory
- [ ] Move scripts to appropriate locations
- [ ] Update any references in documentation
- [ ] Add README.md to scripts directories

---

## Issue #3: Consolidate Changelog Files
**Priority**: High  
**Type**: Documentation

### Description
Two changelog files exist - need to merge and maintain single source of truth.

### Files to Handle
- `BOILERPLATE_CHANGELOG.md` - Contains tracking system info
- `CHANGELOG.md` - Main changelog

### Tasks
- [ ] Review content of both files
- [ ] Merge BOILERPLATE_CHANGELOG tracking info into main CHANGELOG
- [ ] Keep single CHANGELOG.md
- [ ] Archive or remove BOILERPLATE_CHANGELOG.md

---

## Issue #4: Clean Up Git Push Scripts
**Priority**: Low  
**Type**: Cleanup

### Description
Multiple git push related files in root that may be temporary or project-specific.

### Files to Handle
- `GIT_PUSH_DUAL_REPOS_PROMPT.md` - Review and possibly move to `docs/guides/`
- `GIT_PUSH_QUICK_PROMPT.md` - Review and possibly move to `docs/guides/`
- `execute-push.sh` - Move to `scripts/git/` or remove if obsolete
- `push-to-both-repos.sh` - Move to `scripts/git/` or remove if obsolete

### Tasks
- [ ] Review if git push scripts are still needed
- [ ] Move to appropriate location or remove
- [ ] Document git workflow if keeping

---

## Issue #5: Organize Agent-Related Documentation
**Priority**: Medium  
**Type**: Documentation

### Description
Agent handoff and onboarding docs should be in proper location.

### Files to Handle
- `CLAUDE_AGENT_COMPLETE_ONBOARDING.md` - Move to `docs/agents/`
- `CLAUDE_AGENT_HANDOFF.md` - Move to `docs/agents/`
- `CLAUDE_AGENT_QUICK_PROMPT.md` - Move to `docs/agents/`

### Tasks
- [ ] Create `docs/agents/` directory
- [ ] Move agent documentation files
- [ ] Update references in main CLAUDE.md
- [ ] Add index to agent docs

---

## Issue #6: Review and Organize Test/Demo Files
**Priority**: Low  
**Type**: Review

### Description
Test and validation files in root need review.

### Files to Handle
- `test-integration-docs.sh` - Move to `scripts/tests/` or `tests/`
- `test-validation/` directory - Already in subdirectory, verify contents

### Tasks
- [ ] Review if test scripts are current
- [ ] Move to appropriate test directories
- [ ] Remove if obsolete

---

## Issue #7: Archive or Remove Temporary Files
**Priority**: Medium  
**Type**: Cleanup

### Description
Some files appear to be temporary or backups.

### Files to Investigate
- `.claude-backup-before-cleanup-20250131/` - Verify if needed
- `.claude.full_backup_20250727_102756/` - Old backup, consider archiving
- `.trash-to-delete/` - Should be empty or removed
- `.tsconfig.staged.json` - Review if needed

### Tasks
- [ ] Check if backups are still needed
- [ ] Archive old backups to external storage
- [ ] Remove empty directories
- [ ] Document any special config files

---

## Summary

### Proposed Root Directory Structure After Cleanup
```
/boilerplate/
├── .claude/                 # Core Claude Code config
├── .agent-os/              # Agent OS standards
├── .github/                # GitHub config
├── .husky/                 # Git hooks
├── app/                    # Next.js app
├── components/             # React components
├── docs/                   # All documentation
├── field-registry/         # Security features
├── hooks/                  # React hooks
├── lib/                    # Libraries
├── PRPs/                   # Product Requirement Prompts
├── scripts/                # All scripts organized
├── styles/                 # CSS/styling
├── templates/              # Component templates
├── tests/                  # Test files
├── CHANGELOG.md           # Single changelog
├── CLAUDE.md              # AI instructions
├── README.md              # Project readme
├── package.json           # Node config
└── [config files]         # Essential configs only
```

### Files to Keep in Root
- Essential config files (package.json, tsconfig.json, etc.)
- README files
- License files
- Active changelog
- Main CLAUDE.md instruction file

### Everything Else
- Move to appropriate subdirectories
- Archive if historical
- Remove if obsolete
