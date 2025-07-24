# Completion Verification System - Migration Guide

## Overview

The Completion Verification System enhances your existing TDD workflow by automatically verifying completion claims. It works alongside your existing hooks without disrupting current workflows.

## What's New

### 1. New Hook: `14-completion-verifier.py`
- Detects when Claude claims something is "complete" or "done"
- Runs quick verification checks (tests exist, tests pass, TypeScript compiles)
- Provides TDD-focused guidance when verification fails
- Non-blocking by default (uses stdout for visibility)

### 2. New Command: `/verify`
- Manual verification command
- Quick mode (default): Tests exist, TypeScript compiles
- Full mode: Includes coverage and regression checks
- Integrates with TDD workflow

### 3. Enhanced Commands
- `/pt` - Now includes automatic verification status
- `/feature-complete` - Requires verification before marking complete

### 4. New Configuration
- Added `verification_system` section to `config.json`
- Tracks TDD metrics in `verification-manifest.json`

## Migration Steps

### Phase 1: Initial Setup (Complete)
✅ Created completion verifier hook
✅ Added verification manifest
✅ Created /verify command
✅ Updated process-tasks.md
✅ Updated feature-complete.md
✅ Added config settings
✅ Activated hook in settings.json

### Phase 2: Testing & Refinement
1. Test with a simple completion claim
2. Verify TDD workflow enhancement
3. Check integration with existing hooks
4. Adjust thresholds if needed

### Phase 3: Team Rollout
1. Announce to team
2. Update documentation
3. Monitor metrics
4. Gather feedback

## How It Enhances TDD

### Before
```
1. Write implementation
2. Claude: "✅ Done!"
3. Later: Tests fail, TypeScript errors
```

### After
```
1. Write implementation
2. Claude: "✅ Done!"
3. Hook: "📋 TDD Check: No tests found!"
4. Guidance: Create tests first with /test
5. Follow TDD workflow
```

## Configuration Options

### Strict Mode (Future)
```json
{
  "verification_system": {
    "strict_mode": true,
    "block_on_failure": true
  }
}
```

### Disable for Specific Files
```json
{
  "verification_system": {
    "skip_patterns": ["*.config.ts", "*.d.ts"]
  }
}
```

## Metrics Tracking

The system tracks:
- Tests written first vs after (TDD compliance)
- Completion claims verified vs failed
- Average test count per feature
- Coverage trends

View metrics:
```bash
cat .claude/verification-manifest.json | jq .tdd_metrics
```

## Troubleshooting

### Hook Not Running
1. Restart Claude Code
2. Check Python 3 installed: `python3 --version`
3. Verify hook in settings.json

### Too Many False Positives
Adjust completion phrases in config.json:
```json
"completion_phrases": [
  // Remove overly generic phrases
]
```

### Performance Issues
Switch to quick mode only:
```json
"verification_levels": {
  "quick": ["test_exists"]
}
```

## Best Practices

1. **Let it Guide, Not Block** - Default mode provides guidance without blocking
2. **Use with TDD Workflow** - Works best when following test-first development
3. **Run Full Verification Before PR** - Use `/verify --full` before creating PRs
4. **Update Baseline After Major Changes** - Keep regression tests current

## Gradual Adoption

### Week 1: Observation Mode
- Hook runs but only logs to stdout
- Gather metrics on completion claims
- No workflow disruption

### Week 2: Guidance Mode (Current)
- Provides TDD guidance on failures
- Suggests commands to fix issues
- Still non-blocking

### Week 3: Enforcement Mode (Optional)
- Can enable blocking mode
- Requires verification for task completion
- Full TDD enforcement

## Integration Points

### With Smart Resume (`/sr`)
Shows last verification status:
```
🕒 LAST ACTIVITY (25 min ago):
✓ Added email validation
⚠️ Verification: Tests missing for EmailValidator
```

### With Bug Tracking (`/bt`)
Failed verifications can create bugs:
```
/bt add "Tests failing for UserAuth feature"
```

### With Stage Validation (`/sv`)
Verification results included in stage checks:
```
Stage 2: Core Features ⚠️ IN PROGRESS (82%)
  Verification: 3 features unverified
```

## Future Enhancements

1. **Auto-Test Generation** - Generate test stubs when missing
2. **Coverage Trends** - Track coverage over time
3. **Team Dashboard** - Shared verification metrics
4. **CI Integration** - Run verification in GitHub Actions

## Questions?

The system is designed to enhance, not replace, your TDD workflow. It provides guardrails while maintaining flexibility.

For issues or suggestions, update this guide or create a GitHub issue.
