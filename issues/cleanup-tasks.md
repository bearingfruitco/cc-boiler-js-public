# Root Folder Cleanup Tasks

## Phase 1: Directory Structure Setup
- [ ] Create `scripts/maintenance/` directory
- [ ] Create `scripts/setup/` directory  
- [ ] Create `scripts/git/` directory
- [ ] Create `scripts/tests/` directory
- [ ] Create `docs/agents/` directory
- [ ] Create `docs/releases/` directory
- [ ] Create `docs/guides/` directory
- [ ] Create `.claude/archive/cleanup-reports/` directory

## Phase 2: Move Cleanup Reports
- [ ] Move `CLEANUP_ANALYSIS_REPORT.md` → `.claude/archive/cleanup-reports/`
- [ ] Move `CLEANUP_COMPLETE.md` → `.claude/archive/cleanup-reports/`
- [ ] Move `COMMAND_CONSOLIDATION.md` → `.claude/archive/cleanup-reports/`
- [ ] Keep `CLEANUP_SUMMARY_v4.0.1.md` in root as current status

## Phase 3: Move Scripts
- [ ] Move `analyze-alias-duplication.py` → `scripts/maintenance/`
- [ ] Move `analyze-commands.py` → `scripts/maintenance/`
- [ ] Move `clean-aliases.sh` → `scripts/maintenance/`
- [ ] Move `create-all-aliases.sh` → `scripts/maintenance/`
- [ ] Move `complete-playwright-integration.sh` → `scripts/setup/`
- [ ] Move `fix-commands.sh` → `scripts/maintenance/`
- [ ] Move `test-integration-docs.sh` → `scripts/tests/`

## Phase 4: Move Documentation
- [ ] Move `ENHANCEMENT_SUMMARY.md` → `docs/releases/`
- [ ] Move `V4_RELEASE_SUMMARY.md` → `docs/releases/`
- [ ] Move `CLAUDE_AGENT_COMPLETE_ONBOARDING.md` → `docs/agents/`
- [ ] Move `CLAUDE_AGENT_HANDOFF.md` → `docs/agents/`
- [ ] Move `CLAUDE_AGENT_QUICK_PROMPT.md` → `docs/agents/`

## Phase 5: Handle Git Scripts
- [ ] Review `GIT_PUSH_DUAL_REPOS_PROMPT.md` - move or remove
- [ ] Review `GIT_PUSH_QUICK_PROMPT.md` - move or remove
- [ ] Review `execute-push.sh` - move to `scripts/git/` or remove
- [ ] Review `push-to-both-repos.sh` - move to `scripts/git/` or remove

## Phase 6: Consolidate Changelogs
- [ ] Review content of `BOILERPLATE_CHANGELOG.md`
- [ ] Merge tracking system info into main `CHANGELOG.md`
- [ ] Archive or remove `BOILERPLATE_CHANGELOG.md`

## Phase 7: Handle Backups and Temp Files
- [ ] Review `.claude-backup-before-cleanup-20250131/` - archive externally if needed
- [ ] Review `.claude.full_backup_20250727_102756/` - archive externally or remove
- [ ] Check if `.trash-to-delete/` is empty and remove
- [ ] Review `.tsconfig.staged.json` - document if needed or remove

## Phase 8: Create Documentation
- [ ] Add README.md to `scripts/` explaining subdirectories
- [ ] Add README.md to `scripts/maintenance/` explaining utilities
- [ ] Add README.md to `docs/agents/` explaining agent docs
- [ ] Update main README.md with new structure

## Phase 9: Update References
- [ ] Search for references to moved files in documentation
- [ ] Update any command files that reference moved scripts
- [ ] Update CI/CD configs if they reference moved files
- [ ] Update `.gitignore` if needed

## Phase 10: Final Verification
- [ ] Run all tests to ensure nothing broke
- [ ] Verify all commands still work
- [ ] Check that documentation links are not broken
- [ ] Create backup before final commit

## Expected Outcome

### Before (29 items in root)
```
- Multiple cleanup reports
- Scattered scripts
- Duplicate changelogs
- Mixed documentation
- Temporary files
```

### After (~15 items in root)
```
- Only essential configs
- Single CHANGELOG.md
- Main documentation files
- Core directories
- Clean, organized structure
```

## Notes
- Always move files, don't delete until verified
- Keep historical information in archives
- Document any decisions about removed files
- Test after each phase to ensure nothing breaks
