# UltraThink - Extended Deep Thinking with Parallel Agents

Activate Claude's extended thinking window (32k+ tokens) with automatic parallel agent orchestration for complex tasks.

## Usage
```bash
/ultra-think [task description]
/ut [task]  # Short alias
```

## Options
- `--parallel` - Force parallel agents (auto-detected by default)
- `--agents [n]` - Specify number of agents (default: auto 3-5)
- `--visual` - Include screenshot analysis capability
- `--no-code` - Planning only, no implementation

## Examples

### Complex UI Refactoring
```bash
/ut "refactor the dashboard layout for better mobile UX" --visual
# Spawns: UI analyst, pattern researcher, implementation planner
```

### Architecture Planning
```bash
/ut "plan migration from REST to GraphQL"
# Spawns: API analyzer, schema designer, migration strategist
```

### Bug Investigation
```bash
/ut "diagnose why forms are slow on mobile"
# Spawns: performance analyst, code reviewer, solution researcher
```

## How It Works

1. **Triggers Extended Thinking**
   - Activates 32k+ token thinking window
   - Enables deeper analysis and planning

2. **Auto-Spawns Parallel Agents**
   - Detects task complexity
   - Assigns specialized agents
   - Each gets own context window (128-256k)

3. **Orchestrated Planning**
   - Agents work simultaneously
   - Report findings back
   - Main agent synthesizes plan

4. **Iterative Refinement**
   - Review proposed plans
   - "Keep planning" to refine
   - Grade alignment with requirements

## Integration with Existing Commands

```bash
# Start with PRD
/prd "user dashboard"

# Deep think the implementation
/ut "analyze PRD and plan optimal implementation"

# Generate refined tasks
/gt --from-ultrathink

# Process with confidence
/pt
```

## Parallel Agent Types

### Auto-Selected Based on Context:

**UI/UX Tasks:**
- Visual Design Analyst
- Component Pattern Researcher  
- Accessibility Reviewer

**Architecture Tasks:**
- System Design Analyst
- Performance Optimizer
- Security Reviewer

**Refactoring Tasks:**
- Dependency Mapper
- Impact Analyzer
- Migration Planner

**Bug Fixing Tasks:**
- Root Cause Analyst
- Code Pattern Reviewer
- Solution Researcher

## Visual Planning Mode

When `--visual` flag used:
1. Drag screenshots into planning
2. Agents analyze visual elements
3. Compare with design system
4. Suggest improvements

## Planning Iteration

The command supports iterative planning:
```
Plan proposed. Options:
1. Accept and continue
2. "Keep planning" - refine further
3. Add constraints
4. Change approach
```

## Auto-Detection Triggers

UltraThink automatically activates for:
- PRDs with 5+ user stories
- Tasks mentioning "architecture"
- Multi-file refactoring (5+ files)
- Performance optimization
- Security reviews
- Complex UI changes

## Output Format

```markdown
# UltraThink Analysis

## Task Understanding
[Main agent's interpretation]

## Parallel Agent Reports

### Agent 1: [Specialization]
- Key findings
- Recommendations
- Concerns

### Agent 2: [Specialization]
- Key findings
- Recommendations
- Concerns

### Agent 3: [Specialization]
- Key findings
- Recommendations
- Concerns

## Synthesized Plan
1. Step-by-step approach
2. Risk mitigation
3. Success criteria

## Implementation Strategy
[If not --no-code]
```

## Integration Points

- **PRD Workflow**: Enhances `/prd` with deep analysis
- **Task Generation**: Improves `/gt` accuracy
- **Bug Tracking**: Enhances `/bt` root cause analysis
- **Architecture**: New depth for system design
- **Refactoring**: Safer large-scale changes

## Tips

1. **Use for Uncertainty**: When you're not sure how to approach something
2. **Complex Decisions**: When multiple valid approaches exist
3. **Cross-Cutting Concerns**: When changes affect multiple systems
4. **Learning**: To understand existing code deeply

## Related Commands
- `/orchestrate-agents` - Manual agent control
- `/think-through` - Sequential deep thinking
- `/prd` - Requirements definition
- `/analyze-project` - Static analysis
