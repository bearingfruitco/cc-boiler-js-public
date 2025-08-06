# Issue: CI Workflow Failing - Investigate Anthropic Max Plan GitHub Actions Integration

**Priority**: High  
**Type**: Bug/Configuration  
**Created**: January 31, 2025

## Problem

The Claude Code Quality Gates workflow is failing on every push with "Design System Validation Failed". The workflow expects an `ANTHROPIC_API_KEY` secret, but as an Anthropic Max plan subscriber, GitHub Actions integration should be included without needing to manually add API keys.

## Current Behavior

- Every push triggers the workflow
- Design System Validation fails immediately
- All subsequent jobs are skipped
- GitHub sends failure notifications

## Expected Behavior

As an Anthropic Max plan subscriber:
- GitHub Actions should have automatic access to Claude Code
- No manual API key configuration should be required
- The workflow should run successfully with included integration

## Investigation Needed

1. **Verify Max Plan Integration**
   - Check if GitHub Actions integration is automatic for Max plan
   - Determine if special configuration is needed
   - Find documentation on Max plan GitHub Actions setup

2. **Alternative Approaches**
   - Use GitHub's built-in Anthropic integration (if available)
   - Check for special environment variables or configs for Max plan
   - Investigate if workflow needs different authentication method

## Temporary Solution Implemented

The workflow has been disabled by renaming:
- From: `.github/workflows/claude-quality-gates.yml`
- To: `.github/workflows/claude-quality-gates.yml.disabled`

## Proposed Solutions

### Option 1: Fix Max Plan Integration
If Max plan includes GitHub Actions:
1. Find correct configuration method
2. Update workflow to use Max plan authentication
3. Re-enable workflow

### Option 2: Modify Workflow for Local-Only Validation
If GitHub Actions isn't included:
1. Keep CI workflow disabled
2. Rely on local hooks for validation
3. Document that quality gates run locally only

### Option 3: Create Alternative CI
Replace Claude Code commands with:
1. Traditional linting (ESLint/Biome)
2. TypeScript checking
3. Basic design system validation scripts
4. Security scanning tools

## Action Items

- [ ] Research Anthropic Max plan GitHub Actions documentation
- [ ] Contact Anthropic support if needed about Max plan features
- [ ] Decide on approach based on Max plan coverage
- [ ] Either fix integration or create alternative CI approach
- [ ] Update documentation to reflect CI status

## Code References

Current workflow location:
```
.github/workflows/claude-quality-gates.yml.disabled
```

Workflow expects:
```yaml
env:
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

## Questions for Anthropic Support

1. Does the Max plan include GitHub Actions integration?
2. If yes, what's the correct configuration method?
3. Are there special environment variables for Max plan users?
4. Is there a different authentication flow for CI/CD?

## Impact

- No automated quality checks on push
- Developers must run validation locally
- Risk of non-compliant code being merged
- Manual verification required for PRs

## Workaround

Until resolved, developers should run these commands locally before pushing:
```bash
/validate-design all
/stage-validate check current
/security-check
/deps scan
```

---

**Note**: This is a critical issue as it affects the automated quality assurance pipeline. The Max plan should include this functionality, so investigation is priority before implementing workarounds.
