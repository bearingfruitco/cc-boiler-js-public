---
name: parallel-execute
description: Execute multiple agents in parallel on the same or different features
args: [feature_name, plan_path, num_agents]
---

# Execute Parallel Development for {{feature_name}}

Launching {{num_agents}} agents to work simultaneously based on {{plan_path}}.

## Execution Process

### 1. Read Implementation Plan
```bash
cat {{plan_path}}
```

### 2. Launch Parallel Agents

You will now coordinate {{num_agents}} sub-agents working in parallel.

For each work tree (1 to {{num_agents}}):

#### Agent {{i}} Instructions:
```
You are Agent {{i}} working in .trees/{{feature_name}}-v{{i}}

1. Change to your work tree:
   cd .trees/{{feature_name}}-v{{i}}

2. Read the plan from {{plan_path}}

3. Implement the feature with your unique approach:
   - You may interpret requirements differently
   - You may use different patterns
   - You may optimize for different aspects
   
4. Write comprehensive tests

5. Document your approach in results.md:
   - What choices you made
   - Why you made them
   - Performance characteristics
   - Test coverage achieved
   
6. Commit your changes:
   git add -A
   git commit -m "feat: {{feature_name}} implementation v{{i}}"
```

### 3. Monitor Progress

Track all agents working simultaneously:
- Agent 1: [Status]
- Agent 2: [Status]
- Agent 3: [Status]

### 4. Collect Results

After all agents complete:

```bash
# Review each implementation
for i in 1..{{num_agents}}; do
  echo "=== Agent $i Results ==="
  cat .trees/{{feature_name}}-v$i/results.md
done
```

### 5. Compare Implementations

Create comparison report:
- Performance metrics
- Test coverage
- Code quality
- Unique approaches
- Recommended best implementation

## Success Criteria
- All {{num_agents}} agents complete
- Each has working implementation
- Tests pass in each work tree
- Results documented
- Ready for selection and merge

## Next Steps
Use `/parallel-merge` to merge the best implementation back to main branch.
