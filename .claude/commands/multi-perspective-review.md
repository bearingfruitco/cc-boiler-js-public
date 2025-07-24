---
name: multi-perspective-review
aliases: [mpr, multi-review, review-multi]
description: Review code from multiple expert perspectives simultaneously
category: code-quality
---

# Multi-Perspective Code Review

Leverages your existing persona system to review code from multiple expert angles simultaneously, providing comprehensive coverage beyond traditional single-reviewer approaches.

## Arguments
- $TARGET: File, directory, or PR to review (defaults to current changes)
- --perspectives: Specific perspectives to include (default: security,performance,frontend,architect)
- --synthesize: Generate unified review summary (default: true)
- --pr: Review specific pull request number
- --worktree: Review specific worktree

## Usage Examples

### Review Current Changes
```bash
# Review all staged changes from multiple perspectives
/mpr

# Review specific file
/mpr components/forms/CheckoutForm.tsx

# Review entire feature directory
/mpr features/authentication/
```

### Review Pull Request
```bash
# Review PR from multiple angles
/mpr --pr 156

# Quick command
/pr-multi 156
```

### Review Worktree
```bash
# Review changes in specific worktree
/mpr --worktree auth-feature

# Review all worktrees
/mpr --worktree all
```

### Custom Perspectives
```bash
# Security and performance only
/mpr --perspectives security,performance

# Add business logic review
/mpr --perspectives security,performance,architect,analyzer
```

## Available Review Perspectives

### Security Review
**Persona**: security
**Focus Areas**:
- OWASP Top 10 vulnerabilities
- Authentication/authorization flaws
- Data exposure risks
- Input validation
- Cryptographic weaknesses
- Injection vulnerabilities

### Performance Review  
**Persona**: performance
**Focus Areas**:
- N+1 queries
- Bundle size impact
- Memory leaks
- Render performance
- Database optimization
- Caching opportunities

### Frontend UX Review
**Persona**: frontend
**Focus Areas**:
- Accessibility (WCAG compliance)
- Mobile responsiveness
- Loading states
- Error handling UX
- Design system compliance
- Cross-browser compatibility

### Architecture Review
**Persona**: architect
**Focus Areas**:
- Design patterns
- Code organization
- Dependency management
- Scalability concerns
- Technical debt
- API design

### Additional Perspectives

#### Business Logic Review
**Persona**: analyzer
**Focus Areas**:
- Requirements compliance
- Edge case handling
- Business rule implementation
- Data integrity

#### Quality Assurance Review
**Persona**: qa
**Focus Areas**:
- Test coverage
- Test quality
- Error scenarios
- Integration points

## How It Works

### 1. Parallel Analysis
Each persona reviews independently:
```
Security Agent: "Analyzing for vulnerabilities..."
Performance Agent: "Checking for bottlenecks..."
Frontend Agent: "Reviewing UX patterns..."
Architect Agent: "Evaluating design decisions..."
```

### 2. Deep Examination
Each agent uses their specialized knowledge:
- Security: Checks against known attack vectors
- Performance: Profiles potential hotspots
- Frontend: Validates accessibility and responsiveness
- Architect: Assesses maintainability and scalability

### 3. Synthesis
Lead reviewer combines all findings:
```
MULTI-PERSPECTIVE REVIEW SUMMARY
================================

🔒 SECURITY (3 issues)
- Critical: Unvalidated user input in API endpoint
- Warning: Missing CSRF protection
- Info: Consider rate limiting on auth endpoints

⚡ PERFORMANCE (2 issues)
- Warning: Potential N+1 query in user loader
- Info: Large bundle import could be lazy loaded

🎨 FRONTEND (4 issues)
- Error: Missing alt text on images
- Warning: Non-responsive layout on mobile
- Info: Inconsistent error handling
- Info: Could improve loading states

🏗️ ARCHITECTURE (1 issue)
- Info: Consider extracting shared logic to hook

OVERALL: 10 issues (1 critical, 4 warnings, 5 info)
Recommended: Address critical security issue before merge
```

## Integration with Existing Workflows

### With PR Workflow
```bash
# After creating PR
/fw complete
/mpr --pr  # Multi-perspective review
/pr-feedback  # Traditional status check
```

### With Worktree Workflow
```bash
# After implementing in worktree
/wt-switch auth-feature
/mpr --worktree .
# Fix issues
/wt-pr auth-feature
```

### With TDD Workflow
```bash
# After tests pass
/tdd-cycle
/mpr  # Review implementation
/grade  # Check alignment
```

## Customization

### Define Custom Perspective Sets
Create `.claude/review-perspectives.json`:
```json
{
  "perspectives": {
    "api-review": ["backend", "security", "performance"],
    "ui-review": ["frontend", "performance", "qa"],
    "full-review": ["security", "performance", "frontend", "architect", "qa"],
    "quick-review": ["security", "frontend"]
  }
}
```

Then use:
```bash
/mpr --perspective-set api-review
```

### Add Review Templates
Each persona can have custom review templates in:
`.claude/personas/review-templates/[persona]-review.md`

## Benefits Over Single Review

1. **Comprehensive Coverage**: Multiple experts catch different issues
2. **Parallel Processing**: Reviews happen simultaneously
3. **Unbiased Perspectives**: Each reviewer has a specific lens
4. **Learning Opportunity**: See how different experts think
5. **Consistent Quality**: Same high standards every time

## Best Practices

1. **Run Before PR**: Catch issues before they reach GitHub
2. **Focus on Critical**: Address security/performance first
3. **Iterative Improvement**: Run again after fixes
4. **Combine with Tests**: Reviews complement, don't replace tests
5. **Document Decisions**: When overriding suggestions, document why

## Notes

- Reviews are advisory - use judgment on suggestions
- Some issues may be false positives
- Context matters - reviewers might miss business logic nuances
- Works best on focused changes (not massive PRs)
