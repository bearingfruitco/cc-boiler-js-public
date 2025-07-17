# Create Git Worktree for Parallel Development

Enable multiple agents to work on different features simultaneously using Git worktrees.

## Usage
```bash
/create-worktree feature-auth
/create-worktree feature-api backend-agent
/create-worktree bugfix-123 qa-agent
```

## Arguments: $ARGUMENTS

## What It Does

1. **Creates New Git Worktree**
   - Parallel development branch
   - Isolated working directory
   - Linked to main repository

2. **Sets Up Environment**
   - Copies necessary configs
   - Installs dependencies
   - Prepares for agent work

3. **Configures for Agent**
   - Sets agent-specific context
   - Loads appropriate profile
   - Establishes boundaries

4. **Maintains Synchronization**
   - Tracks parent branch
   - Handles merge conflicts
   - Coordinates with main

## Process

1. Check if worktree name is available
2. Create worktree from current branch
3. Set up directory structure:
   ```
   ../project-auth/          # New worktree
   ├── .claude/             # Copied configs
   ├── PRPs/active/         # Active PRPs
   └── [all project files]  # Full codebase
   ```
4. Initialize agent context
5. Create tracking metadata

## Multi-Agent Workflow Example

```bash
# Terminal 1 - Frontend Agent
cd ..
/create-worktree feature-auth frontend-agent
cd project-auth
/persona frontend
/prp-execute auth-ui

# Terminal 2 - Backend Agent  
cd ..
/create-worktree feature-api backend-agent
cd project-api
/persona backend
/prp-execute auth-api

# Terminal 3 - Integration Agent
cd ..
/create-worktree feature-integration integrator
cd project-integration
/orchestrate-merge auth-ui auth-api
```

## Worktree Structure

```
project/                    # Main repository
├── .git/                  # Git directory
└── ...                    # Main branch files

../project-auth/           # Frontend worktree
├── .git                   # Link to main .git
└── ...                    # feature-auth branch

../project-api/            # Backend worktree
├── .git                   # Link to main .git
└── ...                    # feature-api branch
```

## Agent Assignment

Each worktree can be assigned to a specific agent:

```yaml
worktree: feature-auth
agent: frontend
context:
  - Focus on UI components
  - Use design system strictly
  - No backend modifications
  - Test with Playwright

worktree: feature-api  
agent: backend
context:
  - API endpoints only
  - Database schema changes allowed
  - Security validation required
  - Test with Vitest
```

## Synchronization Commands

```bash
# Check worktree status
/worktree-status

# Sync with main branch
/worktree-sync feature-auth

# Merge worktrees
/worktree-merge feature-auth feature-api

# Clean up worktree
/cleanup-worktree feature-auth
```

## Safety Features

1. **Conflict Prevention**
   - Checks for file conflicts before creation
   - Warns about overlapping work
   - Suggests coordination

2. **Boundary Enforcement**
   - Agents can't modify outside their scope
   - Automatic validation of changes
   - Clear error messages

3. **Progress Tracking**
   - Visual status of all worktrees
   - Completion percentages
   - Dependency tracking

## Example Output

```
🌳 Creating worktree: feature-auth
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Worktree created at: ../project-auth
✓ Branch: feature-auth
✓ Based on: main (a4f2c89)
✓ Agent assigned: frontend

📁 Structure ready:
   ../project-auth/
   ├── .claude/
   ├── PRPs/active/auth-ui.md
   └── [project files]

🚀 Next steps:
   cd ../project-auth
   /persona frontend
   /prp-execute auth-ui

💡 Other active worktrees:
   - feature-api (backend-agent)
   - bugfix-123 (qa-agent)
```

## Best Practices

1. **One Feature Per Worktree**
   - Keep worktrees focused
   - Easier to merge
   - Clear boundaries

2. **Regular Synchronization**
   - Sync with main daily
   - Resolve conflicts early
   - Communicate with team

3. **Clean Up After Merge**
   - Remove completed worktrees
   - Archive PRP results
   - Update documentation

## Troubleshooting

### Common Issues

1. **"Worktree already exists"**
   - Use different name
   - Or cleanup existing: `/cleanup-worktree [name]`

2. **"Cannot create worktree"**
   - Ensure git is initialized
   - Check disk space
   - Verify permissions

3. **"Conflicts detected"**
   - Sync with main first
   - Resolve conflicts
   - Then create worktree

## Integration with PRPs

Worktrees work seamlessly with PRPs:

```bash
# In worktree
/create-prp auth-feature
/prp-execute auth-feature
# Work is isolated to this worktree
```

## Tips

1. Name worktrees descriptively
2. Assign appropriate agents
3. Document handoff points
4. Test before merging
5. Communicate progress regularly
