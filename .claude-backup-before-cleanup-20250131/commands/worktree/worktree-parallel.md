---
name: worktree-parallel
aliases: [wt, worktree]
description: Execute tasks in isolated git worktrees for conflict-free parallel development
category: development
---

# Worktree Parallel Execution

Execute multiple features in completely isolated git worktrees, enabling true parallel development without file conflicts. This complements `/orchestrate-agents` by adding filesystem isolation.

## Arguments
- $FEATURES: Space-separated list of features to develop in parallel
- --tasks: Specify task for each worktree  
- --from-prd: Generate worktrees from PRD tasks
- --from-issues: Create worktrees from GitHub issues
- --no-merge: Don't auto-merge when complete
- --base: Base branch (default: main)

## When to Use vs. Regular Orchestration

### Use Worktrees When:
- Multiple features modify the same files
- Testing different approaches to the same problem  
- Building truly independent features
- Need clean git history per feature
- Want to preserve work if one feature fails

### Use Regular Orchestration When:
- Features work on different parts of codebase
- Tasks are interdependent  
- Quick iterations needed
- Working within single feature branch

## Usage Examples

### Basic Parallel Features
```bash
# Three independent features
/wt auth-system payment-integration ui-redesign

# With specific tasks
/wt auth payment --tasks "implement JWT auth" "add Stripe integration"
```

### From PRD Workflow
```bash
# Generate PRD
/prd multi-tenant-system

# Generate tasks  
/gt multi-tenant

# Execute in parallel worktrees
/wt --from-prd multi-tenant
# Creates worktrees for each major task group
```

### From GitHub Issues
```bash
# Create worktrees from open issues
/wt --from-issues 142 156 189
# Each issue gets its own worktree and branch
```

## Integration with Existing System

### 1. Preserves All Current Workflows
- PRD/PRP system works unchanged
- All hooks run independently per worktree
- Design validation per worktree
- Metrics tracked separately

### 2. Enhanced Orchestration
```bash
# Old way (shared filesystem)
/orchestrate-agents "build auth, payments, and dashboard"
# Risk: File conflicts if they touch same components

# New way (isolated filesystems)
/wt auth payments dashboard --orchestrate
# Each agent works in complete isolation
```

### 3. Automatic Configuration
Each worktree receives:
- Full `.claude` directory copy
- Context for specific feature
- Isolated git branch
- Independent hook state
- Separate metrics tracking

## Worktree Lifecycle

### 1. Setup Phase
```bash
# For each feature, creates:
git worktree add -b feature/[name] .worktrees/[name] main

# Copies configuration
cp -r .claude .worktrees/[name]/

# Creates context
echo "[task description]" > .worktrees/[name]/.claude/context/task.md
```

### 2. Execution Phase
```bash
# Each worktree can be worked on:
cd .worktrees/auth-system
/sr  # Smart resume works normally
/cc LoginForm  # All commands work
/pt auth-tasks  # Process tasks independently
```

### 3. Review Phase
```bash
# Review changes in isolation
/wt-review auth-system

# Or trigger multi-perspective review
/chain multi-perspective-review --worktree auth-system
```

### 4. Merge Phase
```bash
# Create PR for each feature
/wt-pr auth-system

# Or merge directly
/wt-merge auth-system

# Clean up
/wt-clean auth-system
```

## Worktree Management Commands

### Status and Monitoring
```bash
/wt-status              # Show all active worktrees
/wt-health              # Check worktree health
/wt-progress            # Show progress per worktree
```

### Navigation
```bash
/wt-switch auth-system  # Switch to worktree directory
/wt-return              # Return to main directory
```

### Review and Merge
```bash
/wt-review [name]       # Review changes in worktree
/wt-pr [name]          # Create PR from worktree
/wt-merge [name]       # Merge worktree to base
/wt-abandon [name]     # Abandon worktree (keeps branch)
```

### Cleanup
```bash
/wt-clean [name]       # Remove specific worktree
/wt-clean --merged     # Remove all merged worktrees
/wt-clean --all        # Remove all worktrees
```

## Best Practices

### 1. One Feature Per Worktree
Keep changes focused and reviewable

### 2. Clear Naming
Use descriptive names that match your tickets:
```bash
/wt feat/auth-142 fix/payment-189 refactor/ui-205
```

### 3. Regular Syncing
Keep worktrees updated with main:
```bash
/wt-sync auth-system  # Pull latest main changes
/wt-sync --all        # Update all worktrees
```

### 4. Clean Up Regularly
```bash
# After merging features
/wt-clean --merged

# Weekly cleanup
/wt-status --stale    # Shows worktrees older than 7 days
```

## Performance Considerations

### Disk Space
- Each worktree is a full checkout (~100-500MB typically)
- Recommended: Max 5-10 active worktrees
- Use `/wt-status --size` to monitor

### Memory
- Each parallel agent uses separate memory
- Limit concurrent agents to CPU cores - 1

### Best Performance Pattern
```bash
# Morning setup
/wt feat-auth feat-payment feat-dashboard
/wt-orchestrate --morning-tasks

# Work on features
/wt-switch feat-auth
/pt auth-tasks

# Evening cleanup  
/wt-status
/wt-clean --completed
```

## Integration with Chains

Add to your chains for automated workflows:

```json
{
  "chains": {
    "parallel-features": {
      "description": "Develop multiple features in isolation",
      "commands": [
        "checkpoint create pre-parallel",
        "worktree-parallel {features}",
        "worktree-orchestrate",
        "worktree-status --watch"
      ]
    }
  }
}
```

## Troubleshooting

### Worktree Conflicts
```bash
# If worktree gets stuck
/wt-repair [name]

# Force removal if needed
git worktree remove .worktrees/[name] --force
```

### Finding Lost Work
```bash
# All work is preserved in branches
git branch -a | grep feature/

# Recover abandoned worktree
git checkout -b recovered feature/abandoned-feature
```

## Notes

- Requires git 2.5+
- Each worktree maintains independent state
- Perfect for experiment-heavy development
- Complements, doesn't replace, normal workflow
