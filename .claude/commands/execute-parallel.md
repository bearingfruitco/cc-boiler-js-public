---
name: execute-parallel
description: Execute multiple agents in parallel on the same feature for competitive implementation
args: [feature_name, plan_path, num_agents]
---

# Execute Parallel Agent Development

Launching {{num_agents}} agents to implement: {{feature_name}}

## Preparation

### 1. Read Implementation Plan
```bash
# Read the plan that all agents will follow
cat {{plan_path}}
```

### 2. Verify Work Trees Ready
```bash
git worktree list | grep {{feature_name}}
```

## Parallel Execution

### Launch Sub-Agents

For each work tree (1 to {{num_agents}}):

#### Agent {{i}} Instructions:
```markdown
You are Agent {{i}} of {{num_agents}} working on {{feature_name}}.

WORKSPACE: .trees/{{feature_name}}-v{{i}}

YOUR MISSION:
1. Change to your workspace
2. Read the implementation plan
3. Implement the feature YOUR way
4. Follow our design system and patterns
5. Write tests (invoke tdd-engineer if needed)
6. Validate your implementation
7. Create results summary

IMPORTANT:
- You work independently
- Make your own design decisions
- Optimize for your interpretation
- Document your approach
```

### 3. Monitor Progress

Track all agents:
- Agent 1: Working in .trees/{{feature_name}}-v1
- Agent 2: Working in .trees/{{feature_name}}-v2  
- Agent 3: Working in .trees/{{feature_name}}-v3

### 4. Collect Results

Each agent should create:
```markdown
# .trees/{{feature_name}}-v{{i}}/RESULTS.md

## Implementation Summary
- Approach: [Description]
- Key Decisions: [List]
- Trade-offs: [List]
- Performance: [Metrics]
- Test Coverage: [Percentage]
```

## Post-Execution Analysis

### 1. Compare Implementations
```bash
# Check each implementation
for i in 1 2 3; do
  echo "=== Implementation v$i ==="
  cd .trees/{{feature_name}}-v$i
  npm test
  npm run build
  cat RESULTS.md
  cd -
done
```

### 2. Performance Comparison
```markdown
| Metric | v1 | v2 | v3 |
|--------|----|----|----| 
| Tests Passing | ✅ | ✅ | ✅ |
| Build Time | 2.3s | 2.1s | 2.5s |
| Bundle Size | 245KB | 238KB | 251KB |
| Coverage | 85% | 88% | 82% |
```

### 3. Recommendation
```markdown
## Recommended Implementation: v{{best}}

Reasons:
- Best performance metrics
- Cleanest code structure
- Highest test coverage
- Most maintainable

Next Step: /merge-best {{feature_name}} {{best}}
```

## Important Rules

1. **Isolation**: Each agent works independently
2. **Quality**: All must pass tests
3. **Documentation**: Each must document approach
4. **Comparison**: Objective metrics for selection
5. **No Interference**: Agents don't see each other's work

## Success Criteria

- All {{num_agents}} implementations complete
- All pass our test suite
- Clear winner identified
- Ready for merge to main
