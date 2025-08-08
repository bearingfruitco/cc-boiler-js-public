---
name: merge-best
description: Merge the best implementation from parallel development back to main branch
args: [feature_name, best_version]
---

# Merge Best Implementation

Merging the best implementation of {{feature_name}} (version {{best_version}}) back to main.

## Process

### 1. Validate Selection
```bash
# Verify the work tree exists
if [ ! -d ".trees/{{feature_name}}-v{{best_version}}" ]; then
  echo "❌ Work tree not found: .trees/{{feature_name}}-v{{best_version}}"
  exit 1
fi

# Run tests in selected version
cd .trees/{{feature_name}}-v{{best_version}}
npm test
cd -
```

### 2. Prepare for Merge
```bash
# Ensure we're on main branch
git checkout main
git pull origin main

# Check for conflicts
git merge --no-commit --no-ff feature/{{feature_name}}-v{{best_version}}
```

### 3. Review Changes
```bash
# Show what will be merged
git diff --cached --stat

# List all changed files
git diff --cached --name-only
```

### 4. Complete Merge
```bash
# If everything looks good, complete the merge
git commit -m "feat: merge best implementation of {{feature_name}} (v{{best_version}})

Selected implementation v{{best_version}} after parallel development.
This version was chosen for:
- Best performance metrics
- Cleanest code structure
- Highest test coverage
- Most maintainable approach

Parallel development results:
- 3 implementations created
- All passed tests
- Version {{best_version}} selected as optimal"
```

### 5. Push to Remote
```bash
# Push the merged changes
git push origin main
```

### 6. Cleanup Work Trees
```bash
# Remove work trees (optional - you may want to keep for reference)
echo "Clean up work trees? (y/n)"
read -r response

if [ "$response" = "y" ]; then
  for i in 1 2 3; do
    git worktree remove .trees/{{feature_name}}-v$i
    git branch -d feature/{{feature_name}}-v$i
  done
  echo "✅ Work trees cleaned up"
else
  echo "📁 Work trees preserved for reference"
fi
```

### 7. Document Decision
Create a decision record:
```markdown
# Decision Record: {{feature_name}}

## Date
$(date '+%Y-%m-%d')

## Selected Implementation
Version {{best_version}}

## Comparison Matrix
| Metric | v1 | v2 | v3 |
|--------|----|----|----| 
| Tests | ✅ | ✅ | ✅ |
| Coverage | 85% | 88% | 82% |
| Performance | Good | Best | Good |
| Maintainability | Good | Best | Fair |

## Rationale
Version {{best_version}} was selected because:
- [Specific reasons based on metrics]
- [Code quality observations]
- [Performance characteristics]

## Lessons Learned
- [What worked well]
- [What could be improved]
- [Insights for future parallel development]
```

Save to: `.claude/docs/decisions/{{feature_name}}-decision.md`

## Success Output
```
✅ Successfully merged {{feature_name}} v{{best_version}} to main
📊 Performance improvement: X%
🧪 Test coverage: Y%
🚀 Ready for deployment
```

## Important Notes
- Always run tests before merging
- Review all changes carefully
- Document the decision rationale
- Consider keeping work trees for learning
- Share insights with team
