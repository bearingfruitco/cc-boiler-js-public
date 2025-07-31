# Issue #2: Folder Reorganization - Completion Plan

## Status: IN PROGRESS → COMPLETING NOW
## Updated: 2025-01-31

## Current State Analysis

### Completed (50%):
- ✅ Created proper folder structure
- ✅ Moved deployment docs to `/docs/deployment/`
- ✅ Moved monitoring docs to `/docs/monitoring/`
- ✅ Created testing documentation structure

### Remaining Tasks:

1. **Clean up archive directory**
   - Move relevant content from `/docs/archive/` to proper locations
   - Remove outdated/duplicate content
   - Keep historical releases for reference

2. **Consolidate duplicate guides**
   - Multiple GETTING_STARTED variants exist
   - Merge into single authoritative version

3. **Organize command documentation**
   - Move command references to `/docs/commands/`
   - Create category-based structure

4. **Update cross-references**
   - Fix all internal links
   - Update README.md with new structure

## Execution Plan

### Step 1: Archive Cleanup
- Review `/docs/archive/root-docs/` for valuable content
- Move `ARCHITECTURE_WORKFLOW_SUMMARY.md` → `/docs/architecture/`
- Move `COMPLETE_GUIDE.md` → `/docs/workflow/`
- Archive old releases properly

### Step 2: Command Documentation
- Create `/docs/commands/categories/`
- Move command reference from features to commands folder
- Organize by command type

### Step 3: Remove Duplicates
- Consolidate multiple GETTING_STARTED files
- Remove outdated async implementation docs
- Clean up old TDD issues (completed)

### Step 4: Final Structure
```
docs/
├── README.md (updated index)
├── architecture/ (system design)
├── commands/ (command reference)
├── deployment/ (deployment guides)
├── design/ (design system)
├── development/ (dev guides)
├── examples/ (usage examples)
├── features/ (feature docs)
├── integrations/ (third-party)
├── monitoring/ (observability)
├── releases/ (version history)
├── roadmap/ (future plans)
├── setup/ (getting started)
├── testing/ (test guides)
├── troubleshooting/ (debug help)
├── workflow/ (dev workflows)
└── archive/ (historical only)
```

## Success Criteria
- [ ] No duplicate documentation
- [ ] Clear folder purposes
- [ ] All links working
- [ ] Archive contains only historical content
- [ ] README.md updated with navigation
