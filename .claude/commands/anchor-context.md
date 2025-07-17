# anchor-context

Add immutable context that appears in EVERY prompt to prevent requirement drift.

## Usage
```
/anchor-context "Issue #42 requires EXACTLY 13 form fields"
/ac "ContactForm must include all fields from the PRD"
/anchor "Never reduce the number of form fields"
```

## What It Does

1. **Creates Immutable Context** - Adds unremovable context to all future prompts
2. **Enforces Requirements** - Appears in system message for every interaction
3. **Prevents Drift** - AI cannot ignore or override anchored context
4. **Persists Across Sessions** - Survives context windows and resumptions

## Priority Levels

- **Critical** (default) - Cannot be overridden, appears first
- **High** - Important context, appears after critical
- **Normal** - Helpful context, appears last

## Examples

### Basic Usage
```bash
/anchor-context "ContactForm has 13 fields per Issue #42"
```

### With Priority
```bash
/anchor-context "Use only approved color palette" --priority=high
```

### Multiple Anchors
```bash
/ac "Issue #42: 13 fields required"
/ac "All fields are mandatory except company"
/ac "Email validation must use corporate domain check"
```

## How It Works

1. Anchors are stored in `.claude/context/anchors/`
2. Each anchor gets a unique ID and timestamp
3. Hooks inject anchors into every prompt
4. Anchors appear as system-level requirements

## Viewing Current Anchors
```bash
/anchor-context --list

ACTIVE CONTEXT ANCHORS
======================
🔒 CRITICAL (3):
- "Issue #42 requires EXACTLY 13 form fields"
- "ContactForm must validate email with corporate check"
- "Never remove required fields"

📌 HIGH (1):
- "Use design system colors only"

📋 NORMAL (2):
- "Prefer async/await over promises"
- "Add comments for complex logic"
```

## Removing Anchors
```bash
/anchor-context --remove [id]
/anchor-context --clear  # Remove all (requires confirmation)
```

## Integration with Other Commands

- `/pin-requirements` automatically creates critical anchors
- `/fw start` loads issue-specific anchors
- `/sr` restores all anchors from previous session

## Best Practices

1. **Be Specific** - "13 fields" not "multiple fields"
2. **Reference Sources** - Include issue numbers or PRD names
3. **Keep Concise** - Each anchor should be one clear statement
4. **Use Sparingly** - Too many anchors can clutter context

## Storage Format

```json
{
  "id": "anchor_1234567890",
  "text": "Issue #42 requires EXACTLY 13 form fields",
  "priority": "critical",
  "source": "Issue #42",
  "createdAt": "2024-01-15T10:00:00Z",
  "createdBy": "/pin-requirements",
  "immutable": true
}
```
