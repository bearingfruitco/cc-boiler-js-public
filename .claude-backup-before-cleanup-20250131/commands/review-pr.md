---
name: review-pr
description: Perform comprehensive PR review using the code-reviewer sub-agent
---

# Review PR Command

Delegates to the code-reviewer sub-agent for thorough code review and analysis.

## Usage
```
/review-pr [pr-number|branch-name|diff-file] [options]
```

## Arguments
- `pr-number`: GitHub PR number (e.g., #234)
- `branch-name`: Git branch to review against main
- `diff-file`: Path to a diff file
- `options`:
  - `--focus`: security|performance|design|all (default: all)
  - `--strict`: Enable strict mode (fail on warnings)
  - `--suggest`: Generate fix suggestions

## Examples
```bash
# Review a GitHub PR
/review-pr #234

# Review current branch changes
/review-pr feature/user-auth

# Review with security focus
/review-pr #234 --focus=security

# Strict review with suggestions
/review-pr feature/payment --strict --suggest
```

## Execution

use code-reviewer subagent to perform comprehensive code review of ${ARGUMENTS:-the current changes}. Analyze code quality, check design patterns, validate security, review performance impact, verify test coverage, ensure design system compliance, and provide constructive feedback with specific suggestions for improvement.

## Review Categories

The code-reviewer will examine:

### 1. Code Quality
- Clean code principles
- SOLID principles adherence
- DRY (Don't Repeat Yourself)
- Naming conventions
- Code organization

### 2. Design Patterns
- Architectural consistency
- Pattern implementation
- Component structure
- State management
- Error handling patterns

### 3. Security
- Input validation
- Authentication checks
- Authorization patterns
- SQL injection prevention
- XSS protection
- Secret management

### 4. Performance
- Bundle size impact
- Query optimization
- Render performance
- Memory leaks
- Unnecessary re-renders

### 5. Testing
- Test coverage
- Test quality
- Edge cases
- Mocking appropriateness
- E2E scenarios

### 6. Design System
- Typography compliance (text-size-[1-4])
- Spacing grid (4px)
- Color distribution (60/30/10)
- Component consistency
- Mobile responsiveness

## Output Format

The code-reviewer will provide:

```markdown
## Code Review Summary

### Overall Assessment: ✅ Approved with suggestions | ⚠️ Needs changes | ❌ Blocked

### Strengths
- What's done well
- Good patterns used
- Positive highlights

### Critical Issues
- Blocking problems
- Security vulnerabilities
- Major bugs

### Suggestions
1. Specific improvements with code examples
2. Performance optimizations
3. Better patterns to use

### Security Check
- Vulnerability assessment
- Best practice compliance

### Design System Compliance
- Typography: ✅/❌
- Spacing: ✅/❌
- Components: ✅/❌
```

## Integration with Git Hooks

Can be integrated into your workflow:

```bash
# .husky/pre-push
#!/bin/sh
/review-pr $(git branch --show-current) --strict
```

## Automated PR Comments

When integrated with GitHub:
- Posts review summary as PR comment
- Adds inline code suggestions
- Updates PR status checks
- Tracks review resolution

## Follow-up Actions

After review:
1. Address critical issues immediately
2. Create tasks for suggestions
3. Update coding standards if needed
4. Share learnings with team

## Review Philosophy

The code-reviewer follows these principles:
- **Constructive**: Focus on improvement, not criticism
- **Specific**: Provide concrete examples
- **Educational**: Explain the "why" behind suggestions
- **Pragmatic**: Balance ideal vs. practical
- **Consistent**: Apply standards uniformly
