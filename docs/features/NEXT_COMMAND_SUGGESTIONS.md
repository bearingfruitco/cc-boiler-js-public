# Next Command Suggestion System

## Overview

The Next Command Suggestion System provides intelligent, contextual command suggestions after every action in the Claude Code boilerplate. It reduces cognitive load by guiding users through optimal workflows based on their current context and the complexity of their tasks.

## Features

### 1. Intelligent Command Suggestions
- Analyzes command results and suggests logical next steps
- Detects task complexity and recommends appropriate workflows
- Shows time savings when orchestration would help
- Provides context-aware suggestions based on time of day

### 2. Decision Tree Logic
- Comprehensive coverage of all workflows from command-decision-guide
- Smart routing based on:
  - Project state (new vs existing)
  - Task clarity (clear path vs needs research)
  - Complexity level (simple fix vs complex architecture)
  - Current context (has PRD, has tasks, etc.)

### 3. Interactive Decision Guide (`/help-decide`)
- Step-by-step questionnaire to find the right command
- Learns from user choices over time
- Provides explanations for recommendations

### 4. Conflict Prevention
- Respects existing suggestions from other hooks
- Doesn't duplicate orchestration or persona suggestions
- Integrates seamlessly with existing systems

## Implementation

### Hook Architecture
```
.claude/hooks/
├── post-tool-use/
│   └── 04-next-command-suggester.py    # Main suggestion engine
├── utils/
│   └── suggestion_utils.py             # Shared utilities
└── config.json                         # Configuration
```

### Configuration
```json
{
  "suggestion_system": {
    "enabled": true,
    "max_suggestions": 3,
    "show_help_when_stuck": true,
    "stuck_threshold_minutes": 5,
    "respect_existing_suggestions": true
  }
}
```

## Workflow Coverage

### Project Initialization
```
New Project? → /init-project → /gi PROJECT → /fw start 1
```

### Feature Development
```
Clear path? 
  ├─ Yes → /cti → /gt → /fw start → /pt → /test → /fw complete
  ├─ Somewhat → /prd → /gi → /gt → /fw start
  └─ No → /prp → /prp-execute → /prp-complete → /cti
```

### Bug Fixes
```
Bug complexity?
  ├─ Simple → /mt "fix bug" → /test
  ├─ Medium → /bt add → /generate-tests → fix → /test
  └─ Complex → /cti → /gt → /fw start
```

### Research & Exploration
```
Need research?
  ├─ Architecture → /think-through → /prp
  ├─ Implementation → /prp → /prp-execute
  └─ Best practices → /research → /cti
```

## Examples

### Simple Fix Workflow
```bash
You: /mt "Fix import error in leadprosper.py"
✅ Fixed in 5 minutes

💡 Next steps:
  → `/test`           # Verify your fix
  → `/commit-review`  # Review changes
```

### Complex Feature Workflow
```bash
You: /cti "Implement ML-based lead scoring"
✅ Created issue #45

💡 Next steps:
  → `/prp ml-lead-scoring`  # Complex feature - research recommended
  → `/gt ml-scoring`        # Break down into tasks
  → `/fw start 45`          # Start immediately

You: /prp ml-lead-scoring
✅ PRP created

💡 Next steps:
  → `/prp-execute ml-lead-scoring`  # Begin research phase
  → `/think-through "ML approach"`  # Brainstorm solutions
```

### Morning Routine
```bash
You: /sr
✅ Resumed context

☀️ Good morning! Based on your context:
- 3 tasks remaining in "user-auth"
- 1 failing test from yesterday
- 2 open bugs

💡 Next steps:
  → `/pt user-auth`      # Continue task processing
  → `/test`              # Fix failing test
  → `/bt list --open`    # Review bugs
```

## Situational Awareness

### Time-Based Suggestions
- **Morning (6-10am)**: Suggests `/sr`, bug review, status check
- **Evening (5-10pm)**: Suggests `/checkpoint`, TODO notes, WIP PR
- **Weekend**: Lighter suggestions, documentation focus

### Context-Based Suggestions
- **Many bugs**: Prioritizes bug fixes
- **Stuck (5+ min idle)**: Offers help commands
- **No tasks**: Suggests task generation
- **Tests failing**: Debug assistance

## Testing

Comprehensive test suite covers:
- All command scenarios
- Complexity analysis
- Orchestration calculations
- Situational suggestions
- Conflict detection
- End-to-end workflows

Run tests:
```bash
pytest tests/hooks/test_next_command_suggester.py -v
```

## Benefits

1. **Reduced Cognitive Load**: No need to memorize workflows
2. **Faster Development**: Always know the next step
3. **Learning Tool**: Discover optimal patterns
4. **Prevents Mistakes**: Guides to best practices
5. **Context Preservation**: Never lose your place

## Future Enhancements

1. **Machine Learning**: Learn from successful patterns
2. **Team Patterns**: Share optimal workflows
3. **Custom Workflows**: Define project-specific chains
4. **Analytics**: Track most successful paths
5. **AI Enhancement**: Deeper context understanding

## Troubleshooting

### Suggestions not appearing
1. Check if enabled in config.json
2. Verify hook is running: `ls .claude/hooks/post-tool-use/`
3. Check for conflicts with other hooks

### Wrong suggestions
1. Update context with `/sr`
2. Check project state files
3. Manually specify workflow with `/help-decide`

### Performance issues
1. Reduce suggestion computation with config
2. Disable time-based suggestions if not needed
3. Check context file sizes

## Philosophy

> "The best interface is no interface - the system should know what you need next."

This system embodies the principle of progressive disclosure and contextual assistance, making the powerful Claude Code boilerplate accessible to everyone from beginners to experts.
