---
name: analyze-task
description: |
  MUST BE USED to analyze task complexity and suggest appropriate agents.
  Intelligently routes tasks to single agents or multi-agent workflows.
  Use PROACTIVELY when unsure which agent(s) to use for a task.
argument-hint: <detailed task description>
allowed-tools: Read, SearchFiles, Bash
aliases: ["at", "task-analyze", "route"]
---

# 🎯 Task Analysis & Agent Routing

Analyzing task: **$ARGUMENTS**

## 📋 Task Breakdown

Let me analyze this task across multiple dimensions to recommend the best approach:

### 1. Technology Detection
Scanning for technology-specific keywords and patterns...

!`python3 << 'EOF'
import re

task = """$ARGUMENTS"""
task_lower = task.lower()

# Technology detection patterns
tech_patterns = {
    "Supabase": ["supabase", "rls", "row level security", "auth", "authentication", "realtime", "postgres", "edge function"],
    "ORM": ["drizzle", "prisma", "schema", "migration", "database", "relations", "query builder"],
    "Analytics": ["analytics", "tracking", "events", "rudderstack", "bigquery", "dbt", "metrics", "dashboard"],
    "UI/Frontend": ["component", "ui", "shadcn", "tailwind", "animation", "framer", "design system", "accessibility"],
    "Privacy": ["gdpr", "ccpa", "tcpa", "privacy", "consent", "cookies", "pii", "compliance", "tracking pixel"],
    "Events": ["event schema", "taxonomy", "event tracking", "field engineering", "versioning"],
    "Deployment": ["deploy", "vercel", "edge", "ci/cd", "performance", "optimization", "gcp", "cloud"]
}

detected_tech = []
for tech, keywords in tech_patterns.items():
    if any(keyword in task_lower for keyword in keywords):
        detected_tech.append(tech)

print("🔍 Detected Technologies:")
for tech in detected_tech:
    print(f"  • {tech}")

if not detected_tech:
    print("  • No specific technologies detected - will use general agents")
EOF`

### 2. Complexity Assessment

!`python3 << 'EOF'
task = """$ARGUMENTS"""

# Complexity indicators
complexity_score = 0
indicators = []

# Length-based complexity
if len(task) > 200:
    complexity_score += 1
    indicators.append("Detailed requirements")

# Multi-step indicators
multi_step_words = ["then", "after", "next", "also", "additionally", "and then", "finally"]
if any(word in task.lower() for word in multi_step_words):
    complexity_score += 2
    indicators.append("Multi-step process")

# Integration indicators
integration_words = ["integrate", "connect", "combine", "synchronize", "coordinate"]
if any(word in task.lower() for word in integration_words):
    complexity_score += 2
    indicators.append("Integration required")

# Full-stack indicators
if all(tech in task.lower() for tech in ["frontend", "backend"]) or "full stack" in task.lower():
    complexity_score += 3
    indicators.append("Full-stack implementation")

# Determine complexity level
if complexity_score <= 1:
    complexity = "SIMPLE"
    time_estimate = "< 1 hour"
    agent_count = "1 agent"
elif complexity_score <= 3:
    complexity = "MEDIUM"
    time_estimate = "1-4 hours"
    agent_count = "2-3 agents"
else:
    complexity = "COMPLEX"
    time_estimate = "4+ hours"
    agent_count = "4+ agents (workflow recommended)"

print(f"\n📊 Complexity Analysis:")
print(f"  • Level: {complexity}")
print(f"  • Score: {complexity_score}/10")
print(f"  • Estimated Time: {time_estimate}")
print(f"  • Required Resources: {agent_count}")
print(f"  • Indicators: {', '.join(indicators)}")
EOF`

### 3. Agent Recommendations

Based on my analysis, here are the recommended agents:

!`python3 << 'EOF'
import json

task = """$ARGUMENTS"""
task_lower = task.lower()

# Agent mapping based on task patterns
agent_map = {
    # Technology specialists (v3.0)
    "supabase-specialist": ["supabase", "rls", "auth", "realtime", "postgres function"],
    "orm-specialist": ["drizzle", "prisma", "schema design", "migration", "database model"],
    "analytics-engineer": ["analytics", "tracking", "events", "rudderstack", "bigquery", "metrics"],
    "ui-systems": ["component", "ui design", "shadcn", "animation", "accessibility", "design system"],
    "privacy-compliance": ["gdpr", "ccpa", "privacy", "consent", "compliance", "cookies"],
    "event-schema": ["event schema", "taxonomy", "event design", "field engineering"],
    "platform-deployment": ["deploy", "vercel", "edge", "performance", "optimization"],
    
    # Role-based agents (v2.8.0)
    "pm-orchestrator": ["break down", "plan", "organize", "coordinate", "project"],
    "senior-engineer": ["architecture", "design pattern", "best practice", "system design"],
    "backend": ["api", "endpoint", "server", "backend", "rest", "graphql"],
    "frontend": ["ui", "react", "component", "frontend", "user interface"],
    "qa": ["test", "testing", "quality", "bug", "validation"],
    "security": ["security", "vulnerability", "encryption", "secure"],
    "performance": ["optimize", "performance", "speed", "cache", "fast"],
    "database-architect": ["database design", "normalization", "index", "query optimization"]
}

# Find matching agents
recommended_agents = []
agent_reasons = {}

for agent, keywords in agent_map.items():
    matches = [kw for kw in keywords if kw in task_lower]
    if matches:
        recommended_agents.append(agent)
        agent_reasons[agent] = matches

# Sort by match count
recommended_agents.sort(key=lambda a: len(agent_reasons[a]), reverse=True)

print("\n🤖 Recommended Agents:")
if recommended_agents:
    for i, agent in enumerate(recommended_agents[:5], 1):
        reasons = agent_reasons[agent]
        print(f"\n{i}. **{agent}**")
        print(f"   Matched: {', '.join(reasons[:3])}")
        print(f"   Use for: {agent.replace('-', ' ').title()} tasks")
else:
    print("\nNo specific agent matches - using general purpose agents:")
    print("1. **pm-orchestrator** - For planning and coordination")
    print("2. **senior-engineer** - For technical implementation")
EOF`

### 4. Execution Strategy

!`python3 << 'EOF'
task = """$ARGUMENTS"""

# Determine execution strategy based on complexity and agents
complexity_score = len(task) // 50  # Simple heuristic

print("\n🚀 Recommended Execution Strategy:\n")

if complexity_score <= 2:
    print("**Single Agent Execution**")
    print("```bash")
    print("# Direct agent invocation")
    print("claude -p 'Use the [primary-agent] to: $ARGUMENTS'")
    print("```")
elif complexity_score <= 4:
    print("**Sequential Agent Execution**")
    print("```bash")
    print("# Step 1: Planning")
    print("claude -p 'Use pm-orchestrator to break down: $ARGUMENTS'")
    print("")
    print("# Step 2: Implementation")
    print("claude -p 'Use [primary-agent] to implement the plan'")
    print("")
    print("# Step 3: Validation")
    print("claude -p 'Use qa to validate the implementation'")
    print("```")
else:
    print("**Multi-Agent Workflow**")
    print("```bash")
    print("# Use orchestration for complex coordination")
    print("claude -p '/orchestrate $ARGUMENTS'")
    print("```")
    print("")
    print("This will automatically:")
    print("• Coordinate multiple agents")
    print("• Share context between steps")
    print("• Ensure comprehensive coverage")

print("\n💡 **Pro Tips:**")
print("• For faster results, be specific about requirements")
print("• Use '/orchestrate' for tasks requiring 3+ agents")
print("• Add 'with tests' to include QA validation")
print("• Say 'production-ready' for comprehensive implementation")
EOF`

### 5. Alternative Approaches

Based on your task, you might also consider:

!`python3 << 'EOF'
task = """$ARGUMENTS"""

# Suggest workflow chains
print("📦 **Relevant Workflow Chains:**\n")

chains = {
    "supabase-auth-flow": "Complete authentication system with Supabase",
    "analytics-pipeline": "Event tracking and analytics setup",
    "production-ready-feature": "Full feature with all aspects covered",
    "tech-stack-optimization": "Performance and optimization workflow",
    "feature-complete": "Comprehensive feature implementation",
    "performance-optimization": "System-wide performance improvements"
}

# Simple keyword matching for chain suggestions
suggested_chains = []
for chain, description in chains.items():
    chain_keywords = chain.replace("-", " ").split()
    if any(kw in task.lower() for kw in chain_keywords):
        suggested_chains.append((chain, description))

if suggested_chains:
    for chain, desc in suggested_chains[:3]:
        print(f"• **/chains {chain}**")
        print(f"  {desc}\n")
else:
    print("• **/chains feature-complete** - For comprehensive implementation")
    print("• **/chains production-ready-feature** - For production-grade features")
EOF`

## 📋 Summary

Based on my analysis of your task:

1. **Complexity**: Determined based on requirements
2. **Technologies**: Identified relevant stack components  
3. **Agents**: Recommended specific specialists
4. **Strategy**: Suggested execution approach
5. **Alternatives**: Provided workflow options

### Next Steps:
- Use the recommended agent directly for simple tasks
- Run `/orchestrate` for complex multi-agent tasks
- Execute a workflow chain for standardized processes
- Run `/agent-health` to ensure agents are ready

Need more specific routing? Try:
- `/analyze-task <task> with focus on <technology>`
- `/analyze-task <task> for production deployment`
- `/analyze-task <task> emphasizing performance`

The task analysis is complete. Choose your execution path!
