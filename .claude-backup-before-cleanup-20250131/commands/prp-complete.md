---
name: prp-complete
aliases: [finish-prp, archive-prp, prp-done]
description: Move completed PRP to archive with lessons learned
category: PRPs
---

# Complete PRP: $ARGUMENTS

Archive a completed PRP and capture lessons learned for future reference.

## Completion Process:

### 1. Final Validation
Run comprehensive checks:
```bash
/prp-execute $ARGUMENTS --all-levels
/grade --prp $ARGUMENTS
/review-requirements  # If pinned
```

### 2. Capture Metrics
```yaml
Final Metrics:
- Implementation Time: 6h 45m
- Actual vs Estimated: 112%
- Validation Passes: 4/4
- Bug Count: 3 (all resolved)
- Grade Score: 92%
- Confidence vs Reality: 8/10 → 9/10
```

### 3. Extract Patterns
Identify successful patterns for reuse:
```
Successful Patterns:
✅ JWT implementation approach
✅ Async context manager usage
✅ Test structure for auth flows
✅ Error handling pattern

New Gotchas Discovered:
⚠️ Rate limiter needs Redis
⚠️ Token refresh edge case
```

### 4. Update Knowledge Base

#### Add to AI Docs
```bash
# Extract key learnings
Gotcha: Redis required for distributed rate limiting
Pattern: Use @require_auth decorator for all protected routes
Performance: Batch user lookups for 10x speed improvement
```

#### Update Templates
If patterns are reusable, update PRP templates:
- Add to `PRPs/templates/prp_auth.md`
- Include discovered gotchas
- Reference this implementation

### 5. Create Summary Report
```markdown
# PRP Completion Report: user-authentication

## Summary
- Started: 2024-01-15
- Completed: 2024-01-16  
- Duration: 2 days
- Grade: 92%

## Key Achievements
- Implemented secure JWT auth
- 100% test coverage
- Sub-200ms response times
- Zero security vulnerabilities

## Lessons Learned
1. Redis is essential for scalable rate limiting
2. Refresh token rotation prevents security issues
3. Async patterns improved performance by 3x

## Reusable Assets
- JWT utility class → lib/auth/jwt.py
- Auth middleware → middleware/auth.py
- Test fixtures → tests/fixtures/auth.py

## Team Feedback
"Clean implementation, well-documented" - @backend-team
"Easy to integrate with frontend" - @frontend-team
```

### 6. Archive PRP
```bash
# Move to completed
mv PRPs/active/$ARGUMENTS.md PRPs/completed/$ARGUMENTS.md

# Add completion metadata
cat >> PRPs/completed/$ARGUMENTS.md << EOF

---
## Completion Metadata
- Completed: $(date)
- Final Grade: 92%
- Time Spent: 6h 45m
- Patterns Extracted: 4
- Templates Updated: prp_auth.md
EOF
```

### 7. Update Tracking
- Clear from active PRP list
- Update context manager
- Archive validation history
- Update team dashboard

## Output:
```
✅ PRP Completed: user-authentication

📊 Final Stats:
- Duration: 2 days (6h 45m active)
- Grade: 92% (Excellent)
- Patterns: 4 extracted
- Gotchas: 2 documented

📁 Archived to: PRPs/completed/user-authentication.md
📚 Updated: PRPs/templates/prp_auth.md
🎯 Ready for reuse in similar features

🎉 Great work! Lessons learned will help future implementations.
```

## Options:
```bash
# Basic completion
/prp-complete auth

# Skip final validation
/prp-complete auth --skip-validation

# Extract extra patterns
/prp-complete auth --deep-extraction

# Create detailed report
/prp-complete auth --detailed-report
```

## Best Practices:
1. Always run final validation
2. Document unexpected discoveries
3. Update templates with learnings
4. Share success patterns with team
5. Use completed PRPs as references