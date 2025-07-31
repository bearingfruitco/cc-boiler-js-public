---
name: orchestrate
description: |
  Coordinates multiple native Claude Code agents to work on complex tasks.
  Automatically selects appropriate agents based on task requirements.
  Use for tasks requiring 3+ agents or multiple specialized skills.
argument-hint: <complex task description>
allowed-tools: Read, Write, CreateFile, SearchFiles, Bash
aliases: ["orch", "coordinate", "multi-agent"]
---

# 🎭 Native Agent Orchestration

Orchestrating: **$ARGUMENTS**

## 🎯 Task Analysis

Let me analyze this task and coordinate the appropriate native agents...

!`python3 << 'EOF'
import json
import re
from datetime import datetime

task = """$ARGUMENTS"""
task_lower = task.lower()

# Map task patterns to native agents
agent_mappings = {
    "auth_system": [
        ("pm-orchestrator", "Break down authentication requirements"),
        ("supabase-specialist", "Design auth schema and RLS policies"),
        ("database-architect", "Create user data models"),
        ("backend", "Implement auth API endpoints"),
        ("security-threat-analyst", "Review security vulnerabilities"),
        ("qa", "Test authentication flows")
    ],
    "ui_development": [
        ("frontend-ux-specialist", "Design user interface components"),
        ("ui-systems", "Create design system components"),
        ("form-builder-specialist", "Implement form interactions"),
        ("qa", "Test UI functionality")
    ],
    "database_work": [
        ("database-architect", "Design database schema"),
        ("orm-specialist", "Optimize queries and patterns"),
        ("migration-specialist", "Create migration scripts"),
        ("supabase-specialist", "Configure Supabase features")
    ],
    "performance": [
        ("performance", "Analyze performance bottlenecks"),
        ("analyzer", "Deep dive into specific issues"),
        ("refactoring-expert", "Optimize code structure"),
        ("qa", "Validate improvements")
    ],
    "full_feature": [
        ("pm-orchestrator", "Feature planning and breakdown"),
        ("system-architect", "Design technical architecture"),
        ("database-architect", "Design data models"),
        ("backend", "Implement server logic"),
        ("frontend-ux-specialist", "Build user interface"),
        ("qa", "Comprehensive testing"),
        ("documentation-writer", "Create documentation")
    ]
}

# Detect task type and select agents
selected_type = "full_feature"  # default

if any(word in task_lower for word in ["auth", "login", "user", "session", "jwt"]):
    selected_type = "auth_system"
elif any(word in task_lower for word in ["ui", "component", "frontend", "design", "layout"]):
    selected_type = "ui_development"
elif any(word in task_lower for word in ["database", "schema", "migration", "query"]):
    selected_type = "database_work"
elif any(word in task_lower for word in ["performance", "optimize", "slow", "speed"]):
    selected_type = "performance"

agents = agent_mappings[selected_type]

print(f"📋 Task Type: {selected_type.replace('_', ' ').title()}")
print(f"🎭 Agents Selected: {len(agents)}")
print("\n📍 Execution Plan:")
for i, (agent, purpose) in enumerate(agents, 1):
    print(f"\n{i}. {agent}")
    print(f"   Purpose: {purpose}")
EOF`

## 🚀 Native Agent Execution

Now I'll coordinate these agents using Claude Code's native agent system:

### Step 1: Requirements Analysis

Use the pm-orchestrator agent to break down the requirements for: $ARGUMENTS

*The PM agent will analyze the task and create a structured plan that other agents can follow.*

### Step 2: Technical Architecture

Based on the requirements, use the system-architect agent to design the technical approach.

*The architect will define the system structure, integration points, and technical decisions.*

### Step 3: Implementation

Now I'll coordinate the implementation agents:

#### Database Layer
Use the database-architect agent to design the data models and relationships.

#### Backend Implementation  
Use the backend agent to implement the server-side logic and API endpoints.

#### Frontend Development
Use the frontend-ux-specialist agent to build the user interface following our strict design system (4 sizes, 2 weights, 4px grid).

### Step 4: Quality Assurance

Use the qa agent to test all implemented features and ensure quality standards are met.

### Step 5: Documentation

Use the documentation-writer agent to create comprehensive documentation for the implemented features.

## 📊 Orchestration Summary

The native agents have been coordinated to complete your task. Each agent operated in their specialized domain with their own context window, ensuring:

- **Clear Separation**: Each agent focused on their expertise
- **Context Isolation**: No pollution between different concerns  
- **Optimal Performance**: Native agent features utilized
- **Quality Output**: Specialized knowledge applied

### 🔄 Agent Coordination Flow

```
Task Analysis
    ↓
pm-orchestrator (requirements)
    ↓
system-architect (design)
    ↓
[Parallel Execution]
├── database-architect (data layer)
├── backend (server logic)
└── frontend-ux-specialist (UI)
    ↓
qa (testing)
    ↓
documentation-writer (docs)
    ↓
✅ Complete
```

### 💡 Next Steps

1. **Review Output**: Check the work from each agent
2. **Run Validation**: `/vd` for design compliance
3. **Test Features**: `/tr` to run tests
4. **Create PR**: `/fw complete` when ready

### 🎯 Benefits of Native Orchestration

- **Auto-Activation**: Agents activate based on context
- **Isolated Contexts**: Each agent has clean workspace
- **Better Performance**: Native Claude Code optimization
- **Simplified Flow**: No custom spawning logic needed

The orchestration is complete! All native agents have collaborated to deliver your solution.