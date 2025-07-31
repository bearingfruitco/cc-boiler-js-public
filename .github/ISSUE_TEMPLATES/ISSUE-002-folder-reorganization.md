---
title: Reorganize Documentation Folder Structure
labels: documentation, enhancement, priority:high, good first issue
assignees: ''
---

## 📋 Description

Reorganize the documentation folder structure to eliminate redundancy, improve navigation, and create a cleaner hierarchy.

## 🎯 Acceptance Criteria

- [ ] New folder structure is created
- [ ] All files are moved to appropriate locations
- [ ] No broken links remain
- [ ] Redundant folders are removed
- [ ] All paths in documentation are updated

## 📝 Tasks

### 1. Create New Folders
```bash
mkdir -p docs/deployment
mkdir -p docs/commands  
mkdir -p docs/testing
mkdir -p docs/monitoring
```

### 2. Delete Empty/Redundant Folders
```bash
# Remove project folder (only contains empty features folder)
rm -rf docs/project
```

### 3. Move Files to Appropriate Locations

- [ ] Move feature documentation:
  ```bash
  mv docs/CHAIN_AUTOMATION.md docs/features/
  ```

- [ ] Move deployment documentation:
  ```bash
  mv docs/CI_CD_SETUP.md docs/deployment/
  mv docs/DEPLOYMENT.md docs/deployment/README.md
  ```

- [ ] Archive temporary documentation:
  ```bash
  mv docs/DOCUMENTATION_REORG_COMPLETE.md docs/archive/root-docs/
  ```

- [ ] Archive setup summaries:
  ```bash
  mkdir -p docs/archive/setup
  mv docs/setup/DOCUMENTATION_CLEANUP_SUMMARY.md docs/archive/setup/
  mv docs/setup/INTEGRATION_COMPLETE_SUMMARY.md docs/archive/setup/
  mv docs/setup/SMART_INTEGRATION_SUMMARY.md docs/archive/setup/
  ```

### 4. Rename Redundant Filenames
```bash
mv docs/troubleshooting/troubleshooting-guide.md docs/troubleshooting/guide.md
```

### 5. Update Internal Links

- [ ] Search for moved files and update references:
  ```bash
  # Find all references to moved files
  grep -r "CHAIN_AUTOMATION.md" docs/ --include="*.md"
  grep -r "CI_CD_SETUP.md" docs/ --include="*.md"
  grep -r "DEPLOYMENT.md" docs/ --include="*.md"
  ```

- [ ] Update paths in all affected files

### 6. Verify Structure

- [ ] Run link checker to ensure no broken links
- [ ] Verify all files are in correct locations
- [ ] Update main README.md with new structure

## 🔗 Expected Final Structure

```
docs/
├── architecture/     # System design docs
├── claude/          # AI integration docs
├── commands/        # Command reference (NEW)
├── deployment/      # Deployment guides (NEW)
├── design/          # Design system
├── development/     # Dev guides
├── examples/        # Code examples
├── features/        # Feature documentation
├── integrations/    # Third-party integrations
├── legal/           # Compliance docs
├── monitoring/      # Monitoring guides (NEW)
├── releases/        # Release notes
├── roadmap/         # Future plans
├── setup/           # Getting started
├── testing/         # Testing guides (NEW)
├── troubleshooting/ # Problem solving
├── workflow/        # Daily workflows
└── archive/         # Historical docs
```

## ⏱️ Time Estimate

2 hours

## 🏷️ Labels

- documentation
- enhancement
- priority: high
- good first issue
