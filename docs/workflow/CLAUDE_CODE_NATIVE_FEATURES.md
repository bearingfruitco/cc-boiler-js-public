# Claude Code Native Features Guide

> Features built into Claude Code that enhance our boilerplate workflows

## 🖼️ Visual Debugging with Ctrl+V

Claude Code has native image support that complements our `/vp` command:

### Quick Visual Debug Flow
1. **Capture Issue**: Screenshot the UI problem
2. **Paste Directly**: In Claude Code prompt, press `Ctrl+V` (or `Cmd+V` on Mac)
3. **Describe Problem**: "Why is this button misaligned on mobile?"
4. **Get Analysis**: Claude analyzes visual issues without needing commands

### Best Use Cases
- **Design Violations**: "This doesn't follow our 4px grid"
- **Mobile Issues**: "Touch target looks too small"
- **Layout Problems**: "Elements overlapping on tablet"
- **Visual Bugs**: "Loading spinner stuck on screen"

### Integration with Existing Commands
```bash
# For complex visual planning, still use:
/vp dashboard redesign

# For quick visual debugging:
Ctrl+V → "Fix this alignment issue"
```

## 🚀 Non-Interactive Mode

Run Claude Code without UI for automation:

### Basic Usage
```bash
# Quick queries without thinking process
claude --non-interactive "What's the current branch?"
claude --non-interactive "/sv status"
claude --non-interactive "/bt list --open"
```

### CI/CD Integration
```yaml
# .github/workflows/claude-check.yml
- name: Check Stage Validation
  run: |
    claude --non-interactive "/sv check 2" > stage-status.txt
    if grep -q "FAILED" stage-status.txt; then
      echo "Stage 2 validation failed"
      exit 1
    fi
```

### Bulk Operations
```bash
# Check all components for violations
claude --non-interactive "/vd all" > violations.log

# Generate status report
claude --non-interactive "/ws && /ts && /bt list" > daily-status.md
```

### Debug Non-Interactive Sessions
```bash
# Resume to see full conversation
claude --resume

# Or continue from last
claude --continue
```

## ↩️ Undo Typing: Ctrl+-

Lost a long command? Claude Code supports undo:
- **Windows/Linux**: `Ctrl+-`
- **Mac**: `Cmd+-`

Saves you from retyping complex commands or PRD descriptions.

## 🕐 Session History Navigation

### Resume Specific Conversations
```bash
# List recent sessions
claude --resume

# Shows:
# 1. "Implementing user auth..." (main branch)
# 2. "Fixing mobile layout..." (fix/mobile-layout branch)
# 3. "Adding payment integration..." (feature/payments branch)
```

### Branch-Aware Context
Each session remembers:
- Active branch at the time
- Open PRPs
- Active bugs
- Modified files

## 🎯 Advanced Thinking Triggers

Beyond `/ultra-think`, you can trigger in prompts:

```bash
# Inline thinking triggers
"think: how should we handle offline state?"
"think hard: optimize this database query"
"think harder: solve the race condition"
"ultra think: design real-time collaboration"
```

**Note**: These consume tokens rapidly. Your `/ut` command is more controlled.

## 🔗 Multi-Directory Context

Reference other repos or modules:

```bash
# Add read-only reference
claude --add ../shared-components
claude --add ~/reference-implementations

# Now can reference in prompts:
"Follow the Button pattern from shared-components"
```

### Use Cases
- Referencing design system repos
- Looking at similar implementations
- Checking API contracts in separate repos

## 💡 Best Practices

1. **Visual Debug First**: Try Ctrl+V before complex debugging
2. **Non-Interactive for CI**: Automate validation checks
3. **Session History**: Use branch info when resuming
4. **Think Sparingly**: Your `/ut` is better than inline triggers
5. **Reference Wisely**: Only add repos you'll actually reference

These native features complement your sophisticated command system without adding overhead or duplication.
