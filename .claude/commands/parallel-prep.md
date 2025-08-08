---
name: parallel-prep
description: Prepare parallel work trees for multiple agents to work simultaneously
args: [feature_name, num_agents]
---

# Prepare Parallel Development for {{feature_name}}

Creating {{num_agents}} parallel work trees for feature development.

## Setup Process

### 1. Create Directory Structure
```bash
mkdir -p .trees
echo ".trees/" >> .gitignore
```

### 2. Create Branches and Work Trees
For each agent (1 to {{num_agents}}):

```bash
# Create feature branch
git checkout -b feature/{{feature_name}}-v${i}

# Add work tree
git worktree add .trees/{{feature_name}}-v${i} feature/{{feature_name}}-v${i}

# Verify setup
cd .trees/{{feature_name}}-v${i}
pwd
git status
cd ../..
```

### 3. List All Work Trees
```bash
git worktree list
```

### 4. Report Status
Confirm {{num_agents}} work trees are ready for parallel execution:
- Each has its own branch
- Each is isolated in .trees/
- No conflicts possible
- Ready for parallel development

## Output
```
✅ Work tree 1: .trees/{{feature_name}}-v1 (branch: feature/{{feature_name}}-v1)
✅ Work tree 2: .trees/{{feature_name}}-v2 (branch: feature/{{feature_name}}-v2)
✅ Work tree 3: .trees/{{feature_name}}-v3 (branch: feature/{{feature_name}}-v3)
...
Ready for parallel execution with /parallel-execute
```
