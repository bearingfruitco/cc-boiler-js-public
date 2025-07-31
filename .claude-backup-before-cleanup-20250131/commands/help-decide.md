# Help Decide - Interactive Workflow Guide

Provides an interactive decision tree to help users choose the right command for their situation.

## Usage

```bash
/help-decide
/hd  # alias
```

## What It Does

Presents a series of questions to guide users to the appropriate command based on their current situation and goals. This is especially helpful when users are:

- New to the system
- Unsure which command to use
- Stuck between multiple options
- Want to understand the workflow better

## Interactive Flow

```
Claude: What are you trying to do?

1. 🚀 Start a new project
2. ✨ Add a new feature
3. 🐛 Fix a bug
4. 🔍 Research/explore a complex problem
5. 📝 I have work in progress
6. 🤷 I'm not sure / I'm stuck

You: 2

Claude: How clear is your implementation path?

1. 💯 I know exactly what to build
2. 🤔 I have an idea but need to flesh it out
3. 🔬 I need to research approaches first

You: 1

Claude: Great! Since you have a clear path, I recommend:

→ `/cti "Your feature description"`
   This will capture your feature as a GitHub issue

After that:
→ `/gt feature-name` - Generate detailed tasks
→ `/fw start [issue#]` - Begin implementation

Would you like me to help you create the issue now?
```

## Decision Trees

### New Project Flow
```
New Project?
  ├─ Yes → /init-project → /gi PROJECT
  └─ No → Continue to feature questions
```

### Feature Addition Flow
```
Clear implementation?
  ├─ Yes → /cti → /gt → /fw start
  ├─ Somewhat → /prd → /gi → /gt
  └─ No → /prp → research → /cti
```

### Bug Fix Flow
```
Bug complexity?
  ├─ Simple (<30 min) → /mt "fix bug"
  ├─ Medium → /bt add → /generate-tests → fix
  └─ Complex → /cti → /gt → /fw start
```

### Research Flow
```
Research needed?
  ├─ Architecture → /think-through → /prp
  ├─ Implementation → /prp → /prp-execute
  └─ Best practices → /research → /cti
```

## Implementation

The command:
1. Asks clarifying questions
2. Analyzes responses
3. Suggests optimal workflow
4. Offers to start the recommended command
5. Provides alternative options

## Benefits

- **Reduces decision paralysis** - No more staring at 100+ commands
- **Teaches workflows** - Learn by doing
- **Prevents mistakes** - Guides to correct approach
- **Saves time** - No trial and error

## Examples

### Scenario: Complex Feature
```
You: /help-decide
Claude: What are you trying to do?
You: Add real-time collaboration
Claude: This sounds complex. Have you researched approaches?
You: No
Claude: I recommend starting with research:

→ `/prp real-time-collaboration`
   This will help you explore WebSocket vs SSE vs polling

After research:
→ `/prp-complete` - Finalize approach
→ `/cti` - Create implementation issue
```

### Scenario: Morning Routine
```
You: /hd
Claude: Good morning! Are you continuing work or starting fresh?
You: Continuing
Claude: Let me check your context...

You have:
- 3 open tasks in "user-auth" feature
- 1 failing test from yesterday
- PR #45 with review comments

I recommend:
→ `/sr` - Resume with full context
→ `/pt user-auth` - Continue task processing

Should I run smart resume for you?
```

## Related Commands

- `/ws` - Work status overview
- `/help` - Command reference
- `/think-through` - AI analysis
- `/sr` - Smart resume

## Configuration

Can be customized in `.claude/commands/help-decide.md`:
- Question flow
- Decision criteria  
- Command recommendations
- Contextual awareness
