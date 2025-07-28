# UltraThink + Parallel Agents Integration Guide

This guide explains how Ray Fernando's UltraThink workflow has been integrated into the Claude Code boilerplate system.

## What's New

### 1. UltraThink Command (`/ultra-think` or `/ut`)
- Activates extended thinking window (32k+ tokens)
- Automatically spawns parallel agents for complex tasks
- Each agent gets its own context window (128-256k tokens)
- Synthesizes findings into comprehensive plans

### 2. Visual Planning Mode (`/visual-plan` or `/vp`)
- Drag and drop screenshots for analysis
- Iterative "keep planning" workflow
- Automatic design system compliance checking
- Mobile/tablet consideration built-in

### 3. Auto-Parallel Agent Detection
- New hook: `18-auto-parallel-agents.py`
- Automatically detects when to spawn multiple agents
- No manual orchestration needed for complex tasks
- Intelligent agent type selection based on task

## How It Works

### Automatic Triggers

Parallel agents spawn automatically when:
- Using `/ultra-think` or `/ut` commands
- Task mentions "refactor", "architecture", "optimize"
- Working with 5+ files
- Complex debugging scenarios
- Visual planning with screenshots

### Agent Specializations

**UI/UX Tasks:**
- UI Analyst - Reviews layouts and usability
- Pattern Researcher - Finds best practices
- Accessibility Reviewer - Ensures WCAG compliance

**Architecture Tasks:**
- System Analyst - Maps dependencies
- Performance Optimizer - Identifies bottlenecks
- Security Reviewer - Checks vulnerabilities

**Bug Fixing Tasks:**
- Root Cause Analyst - Traces issue origins
- Pattern Reviewer - Identifies anti-patterns
- Solution Researcher - Proposes fixes

**Refactoring Tasks:**
- Dependency Mapper - Traces impacts
- Impact Analyzer - Assesses risks
- Migration Planner - Creates safe strategies

## Workflow Examples

### Example 1: Complex UI Refactoring
```bash
# Start with visual planning
/vp "dashboard layout issues"
# Drag screenshots into interface
# Describe problems

# Claude automatically:
# - Spawns 3 UI-focused agents
# - Analyzes screenshots
# - Checks design system compliance
# - Proposes solutions

# Iterate: "keep planning, ensure mobile works"
# Accept: "looks good, proceed"
```

### Example 2: Architecture Analysis
```bash
# Deep architectural thinking
/ut "plan migration from REST to GraphQL"

# Spawns:
# - API Analyzer (reviews current endpoints)
# - Schema Designer (plans GraphQL schema)
# - Migration Strategist (creates phased approach)

# Each agent works in parallel
# Results synthesized into migration plan
```

### Example 3: Performance Debugging
```bash
# Complex debugging with evidence
/ut "forms are slow on mobile" --visual

# Drag performance screenshots
# Agents analyze:
# - DOM complexity
# - Network waterfalls  
# - Render patterns
# - Bundle sizes

# Comprehensive performance plan generated
```

## Integration with Existing Workflow

### Enhanced PRD Flow
```bash
# 1. Create PRD as normal
/prd "user authentication system"

# 2. Deep analysis with parallel agents
/ut "analyze PRD and identify implementation challenges"

# 3. Generate more accurate tasks
/gt --from-ultrathink

# 4. Higher confidence processing
/pt
```

### Visual Bug Fixing
```bash
# 1. Track bug with screenshot
/bt add "layout broken on iPad" --screenshot

# 2. Visual planning to understand
/vp "analyze iPad layout issue"

# 3. Parallel agents investigate
# 4. Targeted fix generated
```

## Best Practices

1. **Use UltraThink for Uncertainty**
   - When you're not sure how to approach something
   - When multiple valid solutions exist
   - When cross-cutting concerns are involved

2. **Visual Planning for UI**
   - Always include mobile + desktop screenshots
   - Describe what's wrong, not how to fix
   - Let agents propose solutions

3. **Iterate on Plans**
   - Don't accept first plan
   - Add constraints: "keep planning, consider performance"
   - Ensure edge cases are covered

4. **Combine with Existing Tools**
   - UltraThink → PRD → Tasks → Implementation
   - Visual Plan → Component Creation → Validation
   - Bug Report → UltraThink Analysis → Fix

## Configuration

The parallel agent system is controlled by:
- Hook: `.claude/hooks/pre-tool-use/18-auto-parallel-agents.py`
- Commands: `.claude/commands/ultra-think.md`, `visual-plan.md`
- Aliases: Added to `.claude/aliases.json`

## Monitoring

Parallel agent activity is logged to:
- `.claude/logs/parallel-agents.log`
- `.claude/context/agent-prompts.json`

## Tips from Ray Fernando

1. **"YOLO" Mindset**: Sometimes just try things
2. **Plan First**: Get the plan right before coding
3. **Screenshot Everything**: Visual evidence helps
4. **Iterate**: "Keep planning" until satisfied
5. **Trust the Agents**: Let them work independently

## Future Enhancements

- [ ] Auto-screenshot capture on errors
- [ ] Agent specialization customization
- [ ] Visual diff analysis
- [ ] Performance profiling agents
- [ ] Security scanning agents

---

*This integration brings Ray Fernando's powerful UltraThink workflow into your comprehensive boilerplate system, combining the best of both approaches.*
