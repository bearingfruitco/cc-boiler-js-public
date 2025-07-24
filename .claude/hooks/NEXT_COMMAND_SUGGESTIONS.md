# Next Command Suggestions

The Claude Code boilerplate now includes intelligent next command suggestions after every command execution. This feature guides you through optimal workflows without needing to memorize command sequences.

## How It Works

After executing any command, the system analyzes:
- What command you just ran
- The results and context
- Your current work state
- Time of day
- Open tasks and bugs

It then suggests the most logical next steps with explanations.

## Example Flows

### Creating an Issue
```bash
/cti "Fix import script validation"
# ✅ Created issue #17

💡 Next steps:
  → /gt import-validation - Break down into detailed tasks
  → /fw start 17 - Start working immediately
  → /prp import-validation - If research needed

📚 Need help?
  • /help - See all available commands
  • /think-through "what should I do next?" - Get AI guidance
```

### Complex Feature Detection
```bash
/cti "Research ML approaches for lead scoring"
# ✅ Created issue #23

💡 Next steps:
  → /prp ml-lead-scoring - Complex feature - research recommended
  → /gt ml-lead-scoring - Break down into detailed tasks
  → /fw start 23 - Start working immediately
```

### Task Generation with Orchestration
```bash
/gt user-authentication
# 📊 Generated 15 tasks across 3 domains

💡 Next steps:
  → /orch user-authentication --agents=3 - Save ~45 minutes with parallel execution
  → /fw start 12 - Begin implementation
  → /pt user-authentication - Process tasks systematically
```

### Time-Based Suggestions
```bash
# After 5 PM
/pt user-profile
# ✅ Task completed

💡 Next steps:
  → /test - Verify your implementation
  → /checkpoint - Save your progress

⏰ End of day approaching:
  • /checkpoint - Save your progress
  • /todo add "Continue tomorrow" - Note where you left off
```

## Suggestion Intelligence

The system provides different levels of suggestions:

### Level 1: Essential Next Step
Shows the single most important next action.

### Level 2: Multiple Options
When there are valid alternatives, shows up to 3 primary suggestions.

### Level 3: Contextual Help
Includes time-based suggestions, help options, and context-specific guidance.

## Customization

You can disable suggestions by editing `.claude/hooks/config.json`:

```json
{
  "post-tool-use": [
    {
      "script": "04-next-command-suggester.py",
      "enabled": false  // Set to false to disable
    }
  ]
}
```

## Command Flow Patterns

The suggester recognizes these common workflows:

### Issue → Tasks → Implementation
```
/cti → /gt → /fw start → /pt → /test → /fw complete
```

### PRD → Issues → Tasks
```
/prd → /gi → /fw start → /gt → /pt
```

### Research → Implementation
```
/prp → /prp-execute → /prp-complete → /cti → /gt
```

### Bug Fix Flow
```
/bt add → /generate-tests → fix → /test → /bt resolve
```

## Benefits

1. **Reduced Cognitive Load** - No need to remember what comes next
2. **Discover Features** - Learn about commands naturally
3. **Optimal Workflows** - Always take the best path
4. **Context Awareness** - Suggestions adapt to your situation
5. **Time Savings** - Know when orchestration helps

## Future Enhancements

The suggestion system will learn from:
- Your personal command patterns
- Team-wide successful workflows
- Project-specific sequences
- Time-to-completion metrics

This creates an increasingly intelligent assistant that guides you through development with minimal friction.
