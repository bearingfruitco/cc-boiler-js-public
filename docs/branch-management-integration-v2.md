# Branch Management Integration Plan v2

## 🎯 Proper Integration Strategy

### Current System Analysis

Your boilerplate has:
1. **112+ commands** with chains and workflows
2. **Hook system** with pre/post/notification hooks
3. **PRP/PRD workflow** for specification-driven development
4. **Stage validation** system (`/sv`)
5. **Async event system** for non-blocking operations
6. **Design mode toggle** (`/dmoff`, `/dmon`)
7. **TDD workflow** with test-first development
8. **Context management** with GitHub gist persistence

### ✅ Improved Integration Points

#### 1. **Hook Integration**

The hooks should:
- **Respect existing workflows** - Don't block during PRD/PRP development
- **Use correct tool names** - Match Anthropic's documentation
- **Integrate with chains** - Work with command chains like `safe-commit`
- **Honor existing modes** - Respect design mode, TDD mode, etc.

```python
# Correct tool names from Anthropic docs:
ANTHROPIC_TOOLS = [
    'str_replace_based_edit_tool',  # NOT str_replace_editor
    'create_file',                   # NOT create
    'write_file'                     # NOT write
]
```

#### 2. **Command Enhancement**

Instead of standalone commands, enhance existing ones:

```bash
# Enhanced /fw start
/fw start 50
├── Existing: Creates branch, loads issue
├── NEW: Updates branch registry
├── NEW: Checks for related completed features
└── NEW: Sets up feature protection

# Enhanced /sr (smart resume)
/sr
├── Existing: Restores context, shows location
├── NEW: Shows branch health
├── NEW: Warns about protected features
└── NEW: Suggests branch cleanup if needed

# Enhanced /pt (process tasks)
/pt auth-feature
├── Existing: Processes micro-tasks
├── NEW: Checks if modifying protected files
└── NEW: Updates feature state as tasks complete
```

#### 3. **Workflow Chain Integration**

Create new chains that integrate with existing ones:

```markdown
# New chain: safe-feature-complete
/chain safe-feature-complete [feature-name]
├── Run tests (/test)
├── Validate design (/vd)
├── Check stage completion (/sv check)
├── Update feature state (NEW)
├── Update branch registry (NEW)
└── Prepare for merge (/fw complete)

# Enhanced chain: safe-commit
/chain safe-commit
├── Existing checks...
├── NEW: Check feature protection
└── NEW: Update branch state
```

#### 4. **State File Integration**

Integrate with existing state management:

```json
// Enhance .claude/state/project-state.json
{
  "existing_fields": "...",
  "features": {
    // NEW: Feature completion tracking
  },
  "branches": {
    // NEW: Active branch management
  }
}
```

#### 5. **PRP/PRD Workflow Integration**

```yaml
# When creating PRP
/create-prp user-authentication
├── Existing: Generate PRP document
├── NEW: Check if feature exists
├── NEW: If enhancing, load previous implementation
└── NEW: Set feature as "in_development"

# When completing PRP
/prp-execute user-auth --level 4
├── Existing: Run validation loops
├── NEW: If all pass, mark feature complete
└── NEW: Update protection status
```

#### 6. **Async Event Integration**

```typescript
// Integrate with event system
import { eventQueue, EVENTS } from '@/lib/events';

// When feature completes
eventQueue.emit(EVENTS.FEATURE_COMPLETED, {
  feature: 'user-auth',
  branch: 'feature/23-auth',
  files: ['components/auth/*']
});

// Non-blocking branch sync
eventQueue.emit(EVENTS.BRANCH_SYNC_NEEDED, {
  branch: 'main',
  age_hours: 48
});
```

### 📋 Revised Implementation Plan

#### Phase 1: Non-Breaking Additions
1. Add state tracking to existing commands
2. Create notification hooks (warnings only)
3. Add optional branch info to `/sr`

#### Phase 2: Workflow Enhancement
1. Enhance `/fw` workflow with protection
2. Add protection checks to chains
3. Integrate with PRP validation

#### Phase 3: Full Integration
1. Update all relevant commands
2. Add to command chains
3. Full documentation update

### 🔧 Configuration Integration

```json
// Add to existing .claude/config.json
{
  "existing_config": "...",
  
  "workflows": {
    "existing_workflows": "...",
    "branch_protection": {
      "enabled": true,
      "mode": "warn",  // warn|block|off
      "integrate_with_prd": true,
      "integrate_with_prp": true,
      "respect_force_flag": true
    }
  }
}
```

### ✅ Answers to Your Questions

1. **Are hooks automatically activated?**
   - Yes, once in `.claude/hooks/pre-tool-use/` and enabled in config.json
   - But my initial implementation had wrong tool names

2. **Do they conflict with other commands/hooks?**
   - Initial version could conflict
   - v2 respects existing modes and workflows
   - Integrates rather than overrides

3. **Integrated into workflow?**
   - v1 was standalone
   - v2 enhances existing commands
   - Works with chains and automation

4. **Follow official documentation?**
   - v1 had incorrect tool names
   - v2 uses correct Anthropic tool names
   - Proper error handling and JSON structure

### 🚀 Better Approach

Instead of separate branch management, integrate into existing flows:

```bash
# Feature lifecycle with protection
/fw start 23          # Creates branch, sets up protection
/create-prp auth      # Knows it's new feature
/prp-execute auth     # Validates implementation
/feature-complete     # Marks as protected
/fw complete 23       # Creates PR with feature state

# Daily workflow with awareness
/sr                   # Shows branch & feature state
/pt auth             # Respects protection
/chain safe-commit   # Checks everything
```

This approach:
- ✅ Enhances without disrupting
- ✅ Uses existing patterns
- ✅ Follows your established workflows
- ✅ Integrates with all systems

Would you like me to implement this improved version that properly integrates with your existing system?
