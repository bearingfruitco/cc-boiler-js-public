---
name: worktree-parallel
aliases: [wt, worktree]
description: Execute tasks in isolated git worktrees for conflict-free parallel development
category: development
---

# Worktree Parallel Execution

This is a wrapper for the full worktree-parallel command located in the worktree subdirectory.

See `/worktree/worktree-parallel` for the complete documentation.

## Quick Usage

```bash
# Three independent features
/worktree-parallel auth-system payment-integration ui-redesign

# Or use aliases
/wt auth payment dashboard
/worktree feat-142 feat-189
```

For full documentation, use: `/help worktree/worktree-parallel`
