---
name: prep-parallel
description: Prepare parallel work trees for multiple agents to work simultaneously
args: [feature_name, num_agents]
---

# Prepare Parallel Development Environment

Setting up {{num_agents}} parallel work trees for feature: {{feature_name}}

## Process

### 1. Validate Prerequisites
```bash
# Ensure we're on main/master branch
git status
# Ensure no uncommitted changes
git stash push -m "prep-parallel-{{feature_name}}"
```

### 2. Create Feature Branches
For each agent (1 to {{num_agents}}):
```bash
git checkout -b feature/{{feature_name}}-v{{i}}
git checkout main
```

### 3. Setup Work Trees
```bash
# Create work trees directory if not exists
mkdir -p .trees

# Create work tree for each agent
git worktree add .trees/{{feature_name}}-v1 feature/{{feature_name}}-v1
git worktree add .trees/{{feature_name}}-v2 feature/{{feature_name}}-v2
# ... repeat for all agents
```

### 4. Verify Setup
```bash
# List all work trees
git worktree list

# Verify each tree
for tree in .trees/{{feature_name}}-v*; do
  echo "Checking $tree"
  cd $tree && pwd && git branch --show-current
  cd -
done
```

### 5. Prepare Each Environment
For each work tree:
```bash
cd .trees/{{feature_name}}-v{{i}}
# Copy environment files if needed
cp ../../.env .env
# Install dependencies if needed
npm install
cd -
```

### 6. Report Ready Status
```markdown
## Parallel Environment Ready

Feature: {{feature_name}}
Agents: {{num_agents}}

Work Trees Created:
- .trees/{{feature_name}}-v1 → feature/{{feature_name}}-v1
- .trees/{{feature_name}}-v2 → feature/{{feature_name}}-v2
- .trees/{{feature_name}}-v3 → feature/{{feature_name}}-v3

Ready for: /execute-parallel {{feature_name}} [plan_file] {{num_agents}}
```

## Important Notes
- Each agent will work in complete isolation
- No conflicts between parallel development
- Main branch remains untouched
- Choose best implementation after completion
