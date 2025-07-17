# Requirement Fidelity System

## Overview

The Requirement Fidelity System prevents AI coding assistants from deviating from source-of-truth specifications. It solves the critical problem of "requirement drift" where AI makes unauthorized changes to specifications during implementation.

## The Problem It Solves

Without this system:
- AI might change a 13-field form to 7 fields
- AI might "optimize" by removing required features
- AI might justify changes after the fact
- Context is lost between sessions
- Requirements drift from the original spec

With this system:
- Requirements are locked and immutable
- Any deviation is immediately blocked
- Source of truth is preserved
- Context survives all sessions
- 100% requirement compliance

## Core Components

### 1. Requirement Locking (`/pin-requirements`)
```bash
/pin-requirements 42 ContactForm
```
- Extracts requirements from GitHub issues
- Creates immutable specification
- Blocks ANY deviation

### 2. Context Anchoring (`/anchor-context`)
```bash
/anchor-context "Issue #42 requires EXACTLY 13 fields"
```
- Adds unremovable context to every prompt
- Survives context windows
- Cannot be overridden by AI

### 3. Drift Detection (Hook System)
- `06-requirement-drift-detector.py` - Blocks violating changes
- `requirement-context-preserver.py` - Preserves context during compaction
- `continuous-requirement-validator.py` - Checks every 10 commands

### 4. Compliance Review (`/review-requirements`)
```bash
/review-requirements ContactForm
```
- Post-implementation validation
- Shows what passed/failed
- Blocks progression on violations

### 5. Test Generation (`/test-requirements`)
```bash
/test-requirements ContactForm
```
- Generates tests from locked requirements
- Ensures regression prevention
- Fails if requirements violated

## Workflow Integration

### The New "Set It and Enforce It" Workflow

```bash
# 1. Start from GitHub issue
/fw start 42

# 2. Lock requirements (CRITICAL NEW STEP)
/pin-requirements 42 ContactForm

# 3. Add immutable context
/anchor-context "13 fields required per Issue #42"

# 4. Generate PRD with locked requirements
/prd ContactForm --strict

# 5. Check confidence BEFORE coding
/grade --requirements
# If confidence < 8, STOP and clarify

# 6. Create component (drift detector active)
/cc ContactForm

# 7. Generate requirement tests
/test-requirements ContactForm

# 8. Review compliance
/review-requirements ContactForm
# Must be 100% before proceeding

# 9. Complete workflow
/fw complete
```

## File Structure

```
.claude/
├── requirements/
│   ├── locked/           # Immutable requirement files
│   │   └── ContactForm.json
│   └── schema.ts         # TypeScript interfaces
├── context/
│   └── anchors/          # Context anchor files
└── hooks/
    ├── pre-tool-use/
    │   └── 06-requirement-drift-detector.py
    ├── pre-compact/
    │   └── requirement-context-preserver.py
    └── notification/
        └── continuous-requirement-validator.py
```

## Configuration

Add to `.claude/config.json`:

```json
{
  "requirement_enforcement": {
    "enabled": true,
    "strict_mode": true,
    "continuous_validation": true,
    "validation_frequency": 10,
    "auto_test_generation": true,
    "block_on_violation": true
  }
}
```

## How It Prevents Drift

### Before (Without System)
```
Issue: "13 fields required"
↓
AI reads issue
↓
AI implements 7 fields (decides 13 is "too many")
↓
AI justifies: "7 fields is better UX"
↓
❌ Requirement drift occurred
```

### After (With System)
```
Issue: "13 fields required"
↓
/pin-requirements locks specification
↓
AI attempts to implement 7 fields
↓
🚫 BLOCKED: "Violates Issue #42: requires 13 fields"
↓
✅ Requirements enforced
```

## Example Locked Requirement

```json
{
  "id": "req_ContactForm_42",
  "source": {
    "type": "github_issue",
    "reference": "42"
  },
  "component": "ContactForm",
  "requirements": {
    "fields": {
      "count": 13,
      "names": ["firstName", "lastName", ...]
    }
  },
  "locked": true,
  "lockedAt": "2024-01-15T10:00:00Z"
}
```

## Benefits

1. **Zero Requirement Drift** - Impossible to deviate
2. **Early Detection** - Catches issues before implementation
3. **Automated Enforcement** - No manual checking needed
4. **Audit Trail** - All changes tracked
5. **Reduced Rework** - Get it right the first time

## Commands Reference

| Command | Alias | Purpose |
|---------|-------|---------|
| `/pin-requirements [Issue] [Component]` | `/pin`, `/pr` | Lock requirements from issue |
| `/anchor-context "text"` | `/ac` | Add immutable context |
| `/review-requirements [Component]` | `/rr` | Check compliance |
| `/test-requirements [Component]` | `/tr-gen` | Generate tests |
| `/grade --requirements` | `/grade -r` | Pre-implementation check |

## Troubleshooting

### "Requirement violations detected"
1. Run `/review-requirements [Component]` to see details
2. Fix the specific violations listed
3. Re-run validation

### "Confidence score too low"
1. Review locked requirements
2. Update implementation plan
3. Ensure all requirements included

### "Context anchors not appearing"
1. Check `.claude/context/anchors/` directory
2. Run `/anchor-context --list` to verify
3. Restart Claude Code if needed

## Best Practices

1. **Always pin requirements** before starting implementation
2. **Check confidence** before coding
3. **Don't skip validation** - it's there to help
4. **Fix violations immediately** - don't let them accumulate
5. **Keep requirements updated** - use audit trail for changes

## Migration for Existing Projects

```bash
# 1. Scan for components with issues
/requirement-scan

# 2. Pin all requirements
/pin-requirements-bulk

# 3. Generate tests
/test-requirements --all

# 4. Enable strict mode
# Update config.json
```

This system ensures Claude Code becomes a reliable implementation partner that respects requirements as immutable truth.
