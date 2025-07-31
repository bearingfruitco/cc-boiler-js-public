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

# 🎭 Native Agent Orchestration (Fixed)

Orchestrating: **$ARGUMENTS**

## 🎯 Task Analysis

Let me analyze this task and coordinate the appropriate native Claude Code agents...

!`python3 << 'EOF'
import json
import re
from datetime import datetime

task = """$ARGUMENTS"""
task_lower = task.lower()

# Map task patterns to ACTUAL native Claude Code agents
# These are the actual agents that exist in .claude/agents/
native_agent_mappings = {
    "auth_system": [
        ("pm-orchestrator", "Break down authentication requirements"),
        ("supabase-specialist", "Design auth schema and RLS policies"), 
        ("database-architect", "Create user data models"),
        ("backend", "Implement auth API endpoints"),
        ("security", "Review security vulnerabilities"),
        ("qa", "Test authentication flows")
    ],
    "ui_development": [
        ("frontend", "Design user interface components"),
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
        ("frontend", "Build user interface"),
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

agents = native_agent_mappings[selected_type]

print(f"📋 Task Type: {selected_type.replace('_', ' ').title()}")
print(f"🎭 Agents Selected: {len(agents)}")
print("\n📍 Execution Plan:")
for i, (agent, purpose) in enumerate(agents, 1):
    print(f"\n{i}. {agent}")
    print(f"   Purpose: {purpose}")
    print(f"   Command: Use the {agent} agent")
EOF`

## 🚀 Native Agent Execution

Now I'll coordinate these agents using Claude Code's native agent system. 

**IMPORTANT**: Native agents in Claude Code are invoked by stating "Use the [agent-name] agent to [task]" in natural language, not through commands or spawning.

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
Use the frontend agent to build the user interface following our strict design system (4 sizes, 2 weights, 4px grid).

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
└── frontend (UI)
    ↓
qa (testing)
    ↓
documentation-writer (docs)
    ↓
✅ Complete
```

### 💡 Key Differences from Old System

1. **No Custom Spawning**: We use Claude's native "Use the X agent" pattern
2. **Real Agent Names**: Using actual agent files from .claude/agents/
3. **Natural Invocation**: Agents activate through natural language
4. **Better Isolation**: Each agent has its own context
5. **Native Features**: Leverages Claude Code's built-in orchestration

### 🎯 Benefits of Native Orchestration

- **Auto-Activation**: Agents activate based on context
- **Isolated Contexts**: Each agent has clean workspace
- **Better Performance**: Native Claude Code optimization
- **Simplified Flow**: No custom spawning logic needed
- **Maintainable**: Uses official Claude Code patterns

### 📝 Important Notes

1. **Agent Naming**: Always use exact agent names from .claude/agents/ directory
2. **Natural Language**: Invoke with "Use the [agent] agent to..."
3. **No Parameters**: Agents get context from the conversation
4. **Sequential Flow**: Agents work in sequence, not true parallel
5. **Context Passing**: Information flows through the conversation

The orchestration is complete! All native agents have collaborated to deliver your solution.