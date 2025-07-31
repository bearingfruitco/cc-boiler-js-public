# Component Architecture

> Detailed component structure and relationships in Claude Code Boilerplate v4.0.0

## 🧩 Component Overview

The system is organized into logical components that work together to provide a comprehensive development environment.

## 📦 Core Components

### 1. Command Components (`/.claude/commands/`)

```
commands/
├── core/                    # Essential commands
│   ├── smart-resume.md     # Context management
│   ├── help.md            # Help system
│   └── config.md          # Configuration
├── creation/              # Creation commands
│   ├── create-component.md
│   ├── create-prp.md
│   └── create-hook.md
├── validation/            # Validation commands
│   ├── validate-design.md
│   ├── test-runner.md
│   └── grade.md
└── orchestration/         # Multi-agent commands
    ├── orchestrate.md
    ├── spawn.md
    └── ultra-think.md
```

**Key Relationships**:
- Commands can trigger other commands
- Commands emit events for hooks
- Commands can spawn agents

### 2. Agent Components (`/.claude/personas/`)

```
personas/
├── agent-personas.json     # 31 specialized agents
├── orchestrator.json      # Master coordinator
└── specialist-configs/    # Domain-specific configs
```

**Agent Categories**:
1. **Frontend Specialists** (5 agents)
   - UI/UX Expert
   - React Specialist
   - Animation Expert
   - Accessibility Specialist
   - Performance Optimizer

2. **Backend Specialists** (5 agents)
   - API Architect
   - Database Expert
   - Security Specialist
   - Infrastructure Engineer
   - Integration Specialist

3. **Quality Assurance** (4 agents)
   - Test Engineer
   - QA Automation
   - Performance Tester
   - Security Auditor

4. **Architecture & Design** (4 agents)
   - System Architect
   - Solution Designer
   - Tech Lead
   - Code Reviewer

5. **Specialized Domains** (13 agents)
   - Mobile Developer
   - DevOps Engineer
   - Data Scientist
   - And more...

### 3. Hook Components (`/.claude/hooks/`)

```
hooks/
├── pre-tool-use/
│   ├── 01-state-capture.py
│   ├── 02-design-check.py
│   ├── 03-security-scan.py
│   └── ...
├── post-tool-use/
│   ├── 10-validation.py
│   ├── 11-event-emit.py
│   ├── 12-chain-trigger.py
│   └── ...
└── on-error/
    ├── 20-error-handler.py
    └── 21-recovery.py
```

**Hook Flow**:
```
File Operation Request
       ↓
[Pre-Tool-Use Hooks]
  01 → 02 → 03 → ...
       ↓
  Operation Execution
       ↓
[Post-Tool-Use Hooks]
  10 → 11 → 12 → ...
       ↓
    Response
```

### 4. Event System Components (`/lib/events/`)

```
events/
├── event-emitter.ts       # Core event bus
├── event-handlers/        # Event processors
│   ├── file-change.ts
│   ├── command-complete.ts
│   └── validation-result.ts
├── event-queue.ts         # Async queue
└── event-types.ts         # Type definitions
```

**Event Flow**:
```
Component A → Emit Event → Event Bus → Handlers → Component B
                              ↓
                         Event Queue
                              ↓
                      Async Processing
```

### 5. Validation Components (`/lib/validation/`)

```
validation/
├── design-validator.ts    # Design system rules
├── code-validator.ts      # Code quality checks
├── security-validator.ts  # Security scanning
├── accessibility.ts       # A11y validation
└── performance.ts         # Performance checks
```

**Validation Levels**:
1. **Syntax**: Basic correctness
2. **Semantic**: Logic and patterns
3. **Design**: System compliance
4. **Quality**: Best practices

### 6. State Management Components

```
.claude/
├── state/
│   ├── context.json      # Current context
│   ├── history.json      # Command history
│   └── sessions/         # Session data
├── cache/
│   ├── validations/      # Validation results
│   └── resolutions/      # Command lookups
└── config.json           # Configuration
```

## 🔗 Component Interactions

### 1. Command → Agent Flow
```
/orchestrate "Build user dashboard"
         ↓
    Orchestrator
         ↓
  [Analyze Task]
         ↓
 Spawn: Frontend, Backend, QA
         ↓
 [Parallel Execution]
         ↓
   Synthesize Results
```

### 2. Hook → Validation Flow
```
File Change → Pre-Hook → Design Check → Validation
                ↓             ↓              ↓
             Continue?    Load Rules    Pass/Fail
                              ↓
                         Apply Fixes
```

### 3. Event → Chain Flow
```
Component Created → Event: "component.created"
                           ↓
                    Chain Trigger Check
                           ↓
                    Execute Chain Steps
```

## 🏗️ Component Patterns

### 1. **Command Pattern**
```markdown
---
command: component-name
aliases: [cn, comp-name]
category: creation
description: Creates a new component
parameters:
  name: Component name
  type: Component type
---

# Execution logic here
```

### 2. **Agent Pattern**
```json
{
  "name": "Frontend Specialist",
  "expertise": ["React", "UI/UX", "Performance"],
  "personality": "Detail-oriented and user-focused",
  "tools": ["create-component", "validate-design"],
  "prompts": {
    "analyze": "Analyze this from a frontend perspective...",
    "implement": "Implement with React best practices..."
  }
}
```

### 3. **Hook Pattern**
```python
# Pre-tool-use hook
def process(event):
    if event.tool == "write_file":
        if is_component_file(event.path):
            validate_design_system(event.content)
    return event
```

## 📊 Component Dependencies

### Direct Dependencies
```
Commands ──depends on──> Hooks
         ──depends on──> Validation
         ──depends on──> State

Agents ──depends on──> Commands
       ──depends on──> Context

Chains ──depends on──> Commands
       ──depends on──> Events
```

### Indirect Dependencies
```
UI Components ──validated by──> Design System
              ──tested by────> Test Framework
              ──documented──> Auto-docs

API Endpoints ──secured by──> Security Rules
              ──cached by──> Cache Layer
              ──logged by──> Monitoring
```

## 🔄 Component Lifecycle

### 1. **Initialization**
1. Load core configuration
2. Register commands
3. Initialize hooks
4. Setup event listeners
5. Restore state

### 2. **Runtime**
1. Accept user input
2. Resolve command
3. Execute pre-hooks
4. Perform operation
5. Execute post-hooks
6. Emit events
7. Update state

### 3. **Shutdown**
1. Save current state
2. Flush event queue
3. Clean up resources
4. Write session data

## 🚀 Extension Points

### Adding New Components

1. **New Command**:
   - Create markdown file in `/commands/`
   - Add metadata and logic
   - Register aliases

2. **New Agent**:
   - Add to `agent-personas.json`
   - Define expertise and tools
   - Create specialized prompts

3. **New Hook**:
   - Add to appropriate hook directory
   - Follow naming convention (XX-name)
   - Implement process function

4. **New Validator**:
   - Add to `/lib/validation/`
   - Implement validation interface
   - Register with validation engine

---

*Component Architecture v4.0.0*  
*Last Updated: 2025-07-30*
