# pin-requirements

Extract and lock requirements from GitHub issue to prevent any deviation during implementation.

## Usage
```
/pin-requirements [Issue #] [Component]
/pin 42 ContactForm
/lock-req 15 UserDashboard
```

## What It Does

1. **Fetches GitHub Issue** - Retrieves the specified issue from your repository
2. **Extracts Requirements** - Uses AI to parse:
   - Field counts and names
   - Required features
   - UI specifications
   - Business rules
   - Constraints
3. **Creates Locked File** - Saves to `.claude/requirements/locked/[Component].json`
4. **Adds Context Anchors** - Critical requirements become immutable context
5. **Generates Validation Rules** - Creates enforceable rules for hooks

## Example

```bash
/pin-requirements 42 ContactForm
```

Output:
```
📌 PINNING REQUIREMENTS FROM ISSUE #42
=====================================

Extracted Requirements:
- Component: ContactForm
- Fields: 13 (firstName, lastName, email, phone...)
- Required validations: email format, phone pattern
- Constraints: All fields required except company

✅ Locked to: .claude/requirements/locked/ContactForm.json
✅ Added 3 context anchors
✅ Generated 5 validation rules

⚠️  These requirements are now IMMUTABLE. Any attempt to deviate will be blocked.
```

## Locked File Format

```json
{
  "id": "req_ContactForm_42",
  "source": {
    "type": "github_issue",
    "reference": "42",
    "url": "https://github.com/user/repo/issues/42"
  },
  "component": "ContactForm",
  "requirements": {
    "fields": {
      "count": 13,
      "names": ["firstName", "lastName", "email", ...],
      "required": ["firstName", "lastName", "email", ...]
    }
  },
  "locked": true,
  "lockedAt": "2024-01-15T10:00:00Z",
  "lockedBy": "/pin-requirements"
}
```

## Integration with Hooks

Once pinned, the following hooks enforce requirements:
- `06-requirement-drift-detector.py` - Blocks changes that violate locked requirements
- `11-truth-enforcer.py` - Treats locked requirements as immutable facts
- `14-creation-guard.py` - Ensures new components match requirements

## Unlocking Requirements

To modify locked requirements:
```bash
/unlock-requirements ContactForm --reason="Client requested 2 additional fields"
```

This creates an audit trail and requires explicit confirmation.
