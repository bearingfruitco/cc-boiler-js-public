---
title: Update All Version References to v4.0.0
labels: documentation, good first issue, priority:medium
assignees: ''
---

## 📋 Description

Update all documentation to reference v4.0.0 instead of older versions, ensuring consistency across all non-archive documentation.

## 🎯 Acceptance Criteria

- [ ] No v2.x or v3.x references outside of archive folders
- [ ] All current documentation references v4.0.0
- [ ] Version history accurately reflects current state
- [ ] What's New document updated for v4.0.0

## 📝 Tasks

### 1. Find Outdated Version References

```bash
# Find all version references outside archive
grep -r "v[0-9]\." docs/ --include="*.md" | grep -v archive | grep -v "v4.0"

# Find specific v2.x references
grep -r "v2\." docs/ --include="*.md" | grep -v archive

# Find specific v3.x references  
grep -r "v3\." docs/ --include="*.md" | grep -v archive
```

### 2. Update Key Files

- [ ] `/docs/claude/WHATS_NEW.md`
  - Add v4.0.0 features
  - Highlight major improvements
  - Update from v3.x guide

- [ ] All README.md files
  - Ensure current version listed
  - Update any version-specific instructions

- [ ] Setup guides
  - Update version requirements
  - Update installation instructions

### 3. Update Feature Documentation

- [ ] Review each feature doc for version mentions
- [ ] Update any "added in version X" notes
- [ ] Ensure compatibility notes are current

### 4. Update Command Documentation

- [ ] Check command files for version requirements
- [ ] Update any deprecated command notices
- [ ] Add v4.0.0 command additions

### 5. Verify Updates

- [ ] Run version check script again
- [ ] Manual review of key documents
- [ ] Ensure consistency across all docs

## 🔍 Files Likely Needing Updates

Based on preliminary scan:
- `/docs/claude/WHATS_NEW.md`
- `/docs/setup/README.md`
- `/docs/SYSTEM_OVERVIEW.md`
- Various command documentation files
- Integration guides

## ⏱️ Time Estimate

2 hours

## 🏷️ Labels

- documentation
- good first issue
- priority: medium

## 💡 Tips

- Use find/replace carefully - some version numbers might be in code examples
- Check context before updating - historical references should remain
- Update incrementally and test links after changes
