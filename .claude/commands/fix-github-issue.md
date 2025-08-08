---
name: fix-github-issue
description: Automatically fix a GitHub issue end-to-end - from reading the issue to creating a PR
args: [issue_number]
---

# Fix GitHub Issue {{issue_number}}

## Workflow

### 1. Read Issue
```bash
gh issue view {{issue_number}}
```

### 2. Understand Requirements
- Parse issue description
- Identify acceptance criteria
- Note any linked issues

### 3. Create Feature Branch
```bash
git checkout -b fix/issue-{{issue_number}}
```

### 4. Implement Solution
- Make necessary code changes
- Follow our design system
- Add proper error handling

### 5. Invoke Validation Gates
Call the validation-gates agent to:
- Write comprehensive tests
- Ensure everything works
- Validate performance

### 6. Commit Changes
```bash
git add -A
git commit -m "fix: resolve issue #{{issue_number}}

- [Description of changes]
- [Tests added]

Closes #{{issue_number}}"
```

### 7. Push and Create PR
```bash
git push -u origin fix/issue-{{issue_number}}

gh pr create \
  --title "Fix: Issue #{{issue_number}}" \
  --body "## Summary
  
Fixes #{{issue_number}}

## Changes
- [List changes]

## Testing
- [List tests added]

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes" \
  --assignee @me
```

### 8. Report Success
Provide PR link and summary of changes.
