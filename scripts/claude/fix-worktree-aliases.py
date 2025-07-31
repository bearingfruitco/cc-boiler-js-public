#!/usr/bin/env python3
"""Fix worktree-parallel aliases"""

import json
from pathlib import Path

CLAUDE_DIR = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude")

def fix_worktree_aliases():
    """Update aliases to point to correct worktree command location"""
    
    aliases_path = CLAUDE_DIR / "aliases.json"
    with open(aliases_path) as f:
        aliases = json.load(f)
    
    # The worktree-parallel command is in a subdirectory
    # We need to update the aliases but Claude Code doesn't support subdirectory paths in aliases
    # So we'll create a symlink or wrapper command
    
    # Remove the broken aliases for now
    if "wt" in aliases:
        del aliases["wt"]
    if "worktree" in aliases:
        del aliases["worktree"]
    
    # Save updated aliases
    with open(aliases_path, 'w') as f:
        json.dump(aliases, f, indent=2)
    
    print("✅ Removed broken worktree aliases")
    
    # Create a wrapper command at the root level
    wrapper_content = """---
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
"""
    
    wrapper_path = CLAUDE_DIR / "commands" / "worktree-parallel.md"
    wrapper_path.write_text(wrapper_content)
    
    print("✅ Created worktree-parallel wrapper command")
    
    # Re-add the aliases pointing to the wrapper
    with open(aliases_path) as f:
        aliases = json.load(f)
    
    aliases["wt"] = "worktree-parallel"
    aliases["worktree"] = "worktree-parallel"
    
    with open(aliases_path, 'w') as f:
        json.dump(aliases, f, indent=2)
    
    print("✅ Re-added aliases pointing to wrapper command")

if __name__ == "__main__":
    fix_worktree_aliases()
