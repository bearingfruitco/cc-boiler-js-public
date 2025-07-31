# Smart Integration System for Existing Projects

## The Challenge

When integrating the boilerplate into existing projects, we need to handle:

1. **Existing CLAUDE.md files** - They may have project-specific instructions
2. **Existing .claude directories** - May contain custom commands, hooks, personas
3. **Root-level files** - package.json, configs, etc. that shouldn't be overwritten
4. **Git configuration** - Existing .gitignore, .husky hooks
5. **Documentation** - Existing docs that should be preserved

## Smart Integration Approach

### Phase 1: Discovery & Analysis

```bash
# Enhanced analyze-existing command should:
/analyze-existing --integration-check

# This will create a conflict report:
.claude-integration/
├── CONFLICT_REPORT.md      # What exists vs what we want to add
├── MERGE_PLAN.md          # How we'll handle each conflict
├── backup/                # Backup of their existing files
└── staged/                # Our files ready to integrate
```

### Phase 2: Intelligent Merging

#### For CLAUDE.md
```markdown
# If they have CLAUDE.md, we create CLAUDE_BOILERPLATE.md
# Then suggest a merged approach:

<!-- Their existing CLAUDE.md -->
# Project-Specific Claude Instructions

[Their content...]

## Boilerplate System Integration

For boilerplate commands and workflows, see CLAUDE_BOILERPLATE.md

<!-- End of their file -->
```

#### For .claude Directory
```bash
.claude/
├── commands/
│   ├── project/          # Their existing commands (moved)
│   ├── boilerplate/      # Our commands (namespaced)
│   └── [our commands]    # Non-conflicting commands
├── hooks/
│   ├── project/          # Their hooks (preserved)
│   ├── pre-tool-use/
│   │   ├── 00-their-hook.py
│   │   ├── 01-our-hook.py   # Numbered to run after theirs
│   └── post-tool-use/
├── personas/
│   ├── project-personas.json  # Their personas
│   └── agent-personas.json    # Our personas
└── chains.json           # Intelligently merged
```

#### For Root Files
```yaml
# Integration manifest
.claude-integration/manifest.yml:
  
preserve:
  - CLAUDE.md          # Their AI instructions
  - package.json       # Their dependencies
  - .env.example       # Their environment template
  - README.md          # Their documentation

merge:
  - .gitignore        # Add our patterns to theirs
  - .coderabbit.yaml  # Merge configurations
  - tsconfig.json     # Merge compiler options

add_new:
  - .claude/          # With conflict resolution
  - .agent-os/        # New directory
  - PRPs/             # New directory
  - field-registry/   # If not exists

rename_ours:
  - CLAUDE.md → CLAUDE_BOILERPLATE.md
  - README.md → README_BOILERPLATE.md
```

### Phase 3: Integration Options

#### Option A: Full Integration with Preservation
```bash
/integrate-boilerplate --mode=full --preserve-existing

# Results in:
.claude/
├── commands/
│   ├── _project/     # Their commands preserved
│   └── [all our commands with conflict resolution]
├── project-config.json
└── integration-config.json  # Tracks what came from where
```

#### Option B: Selective Integration
```bash
/integrate-boilerplate --select

# Interactive menu:
? What would you like to integrate?
  ◯ Commands & Automation (.claude)
  ◯ Design System Enforcement
  ◯ PRP System (one-pass implementation)
  ◯ Agent OS Standards
  ◯ Security Features (field-registry)
  ◯ Git Hooks (pre-commit validation)
  ◯ Event System (async patterns)
```

#### Option C: Side-by-Side Installation
```bash
/integrate-boilerplate --mode=sidecar

# Installs as:
.claude-boilerplate/    # Our complete system
.claude/                # Their existing system

# With a router command:
/bb [command]          # Use boilerplate command
/project [command]     # Use their command
```

## Enhanced Integration Command

```typescript
// New /integrate-boilerplate command

interface IntegrationOptions {
  mode: 'full' | 'selective' | 'sidecar';
  preserveExisting: boolean;
  backupFirst: boolean;
  mergeStrategy: {
    commands: 'merge' | 'namespace' | 'replace';
    hooks: 'append' | 'prepend' | 'merge';
    config: 'merge' | 'separate';
  };
}

async function integrateBoilerplate(options: IntegrationOptions) {
  // 1. Scan existing project
  const conflicts = await scanForConflicts();
  
  // 2. Create integration plan
  const plan = await createIntegrationPlan(conflicts, options);
  
  // 3. Show plan to user
  await showIntegrationPlan(plan);
  
  // 4. Get confirmation
  if (!await confirmIntegration()) return;
  
  // 5. Backup existing files
  if (options.backupFirst) {
    await backupExistingFiles(conflicts);
  }
  
  // 6. Execute integration
  await executeIntegration(plan);
  
  // 7. Verify integration
  await verifyIntegration();
  
  // 8. Generate report
  await generateIntegrationReport();
}
```

## Conflict Resolution Rules

### Commands
```javascript
// If their command exists with same name:
if (existingCommands[commandName]) {
  if (isBoilerplateCore(commandName)) {
    // Critical commands like /sr, /cc, /vd
    moveExisting(`${commandName}` → `${commandName}-project`);
    installOurs(commandName);
  } else {
    // Non-critical commands
    installOurs(`${commandName}-bp`);
    keepTheirs(commandName);
  }
}
```

### Hooks
```python
# Numbering system for execution order:
# 00-09: Their critical hooks (security, auth)
# 10-19: Our critical hooks (design system)
# 20-29: Their feature hooks  
# 30-39: Our feature hooks
# 40-49: Their utility hooks
# 50-59: Our utility hooks
```

### Configuration Files
```json
// Their .claude/config.json
{
  "project": "their-settings",
  "custom": "their-values"
}

// Becomes:
{
  "project": "their-settings",
  "custom": "their-values",
  "boilerplate": {
    "version": "4.0.0",
    "design_system": { ... },
    "features": { ... }
  }
}
```

## Integration Manifest

After integration, we create:

```yaml
# .claude-integration/MANIFEST.yml
integration:
  date: 2025-07-30
  boilerplate_version: 4.0.0
  mode: full
  
preserved:
  - path: CLAUDE.md
    reason: "Existing project AI instructions"
  - path: .claude/commands/deploy.md
    reason: "Project-specific deployment"
    
merged:
  - path: .gitignore
    strategy: append
    additions: [".claude/state", "PRPs/active"]
    
conflicts_resolved:
  - original: .claude/commands/cc.md
    resolution: "moved to cc-project.md"
    our_version: "cc.md"
    
added:
  - .agent-os/
  - PRPs/
  - field-registry/
  - .husky/pre-commit
  
commands:
  from_project: 12
  from_boilerplate: 116
  conflicts: 3
  namespaced: 3
```

## Safe Integration Checklist

Before integration:
- [ ] Backup entire .claude directory
- [ ] Backup CLAUDE.md
- [ ] Backup any custom configurations
- [ ] Check for Git uncommitted changes
- [ ] Document custom commands/hooks

During integration:
- [ ] Review conflict report
- [ ] Approve merge strategy
- [ ] Test critical commands
- [ ] Verify hooks execution order
- [ ] Check design system compatibility

After integration:
- [ ] Original commands still work
- [ ] New commands available
- [ ] No broken workflows
- [ ] Git hooks functioning
- [ ] Documentation accessible

## Rollback Plan

If issues arise:
```bash
/integration-rollback

# This will:
1. Restore from .claude-integration/backup/
2. Remove added directories
3. Revert merged files
4. Restore original configurations
5. Clean up integration artifacts
```

## The Smart Integration Promise

Our integration system:
- **Never breaks existing workflows**
- **Preserves all custom work**
- **Adds power without disruption**
- **Provides clear rollback path**
- **Documents every change**

This ensures teams can adopt the boilerplate incrementally with zero risk to their existing Claude Code setup.
