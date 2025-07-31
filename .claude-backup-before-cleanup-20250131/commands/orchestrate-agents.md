Orchestrate sub-agents with specialized personas to work on tasks in parallel: $ARGUMENTS

Parse arguments:
- Feature name or task file path
- --strategy=feature|security|performance|data|full (default: auto)
- --agents=auto|2-8 (default: auto-detect based on tasks)
- --personas=frontend,backend,security (override auto-selection)

## Persona-Based Sub-Agent Orchestration

### 1. Load Available Personas
Read from: .claude/personas/agent-personas.json

Available personas:
- **frontend**: UI/UX specialist with design system expertise
- **backend**: Server architect with API and database skills  
- **security**: Security analyst for compliance and protection
- **qa**: Quality engineer for comprehensive testing
- **architect**: System designer for architecture decisions
- **performance**: Optimization expert for speed improvements
- **integrator**: Integration specialist for connecting systems
- **data**: Database engineer for schema and migrations

### 2. Analyze Tasks and Match Personas

```typescript
function matchPersonaToTask(task: Task): Persona {
  // Keywords to persona mapping
  const patterns = {
    frontend: /component|ui|form|button|layout|style|responsive/i,
    backend: /api|endpoint|database|server|auth|middleware/i,
    security: /encrypt|pii|audit|compliance|hipaa|gdpr/i,
    qa: /test|spec|e2e|unit|coverage|regression/i,
    data: /migration|schema|table|index|query/i,
    performance: /optimize|cache|speed|bundle|lazy/i,
    integrator: /webhook|external|third-party|sync/i,
    architect: /design|pattern|structure|architecture/i
  };
  
  // Match task description to best persona
  return findBestMatch(task.description, patterns);
}
```

### 3. Coordination Protocol

#### Handoff Points
- Backend completes API → Frontend can start integration
- Frontend completes form → Test agent can write tests
- All agents complete → Integration agent validates

#### Communication
- Shared checkpoint file for progress
- Clear interfaces between components
- Status updates after each task

### 4. Implementation

```typescript
// .claude/orchestration/task-assignments.json
{
  "session_id": "orch_123456",
  "feature": "user-authentication",
  "agents": {
    "frontend": {
      "id": "agent_fe_001",
      "tasks": ["2.1", "2.2", "2.3"],
      "status": "working",
      "current_task": "2.1",
      "completed": [],
      "context": {
        "focus": "UI components",
        "dependencies": ["1.3", "1.4"],
        "output_contracts": {
          "LoginForm": "components/auth/LoginForm.tsx",
          "RegisterForm": "components/auth/RegisterForm.tsx"
        }
      }
    },
    "backend": {
      "id": "agent_be_001",
      "tasks": ["1.1", "1.2", "1.3", "1.4"],
      "status": "working",
      "current_task": "1.2",
      "completed": ["1.1"],
      "context": {
        "focus": "API and database",
        "dependencies": [],
        "output_contracts": {
          "auth_routes": "app/api/auth/*/route.ts",
          "user_schema": "lib/db/schemas/user.ts"
        }
      }
    }
  }
}
```

### 5. Sub-Agent Instructions

Each sub-agent receives:
```markdown
## You are BACKEND_AGENT for feature: user-authentication

### Your Tasks:
1.1 [✓] Create user database schema
1.2 [ ] Set up auth API routes
1.3 [ ] Implement JWT tokens
1.4 [ ] Add rate limiting

### Your Context:
- Focus: API and database only
- Do NOT work on UI components
- Output locations:
  - API routes: app/api/auth/*/route.ts
  - Schemas: lib/db/schemas/*.ts
  - Utils: lib/auth/*.ts

### Dependencies:
- None (you're first in the chain)

### Handoff Contract:
When you complete tasks 1.3 and 1.4, notify FRONTEND_AGENT with:
- API endpoint URLs
- Request/response formats
- Auth header requirements

### Communication:
- Update .claude/orchestration/progress/backend.json after each task
- Check .claude/orchestration/messages.json for updates
- Signal completion with: /agent-complete backend
```

### 6. Progress Tracking

Real-time dashboard:
```
=== SUB-AGENT STATUS ===
Feature: user-authentication

BACKEND_AGENT    [██████░░░░] 60%  - Working on: JWT implementation
FRONTEND_AGENT   [██░░░░░░░░] 20%  - Waiting for: API endpoints
SECURITY_AGENT   [░░░░░░░░░░] 0%   - Waiting for: Components
TEST_AGENT       [░░░░░░░░░░] 0%   - Waiting for: All implementation

Messages:
- [BACKEND → FRONTEND]: Auth endpoints ready at /api/auth/login
- [FRONTEND → TEST]: LoginForm component ready for testing

Next Handoff: 1.3 completion unlocks frontend tasks
```

### 7. Conflict Prevention

Each agent has exclusive file ownership:
```json
{
  "file_ownership": {
    "components/auth/*": "frontend",
    "app/api/auth/*": "backend",
    "lib/db/*": "backend",
    "lib/security/*": "security",
    "tests/*": "test"
  }
}
```

### 8. Smart Orchestration Mode

Automatically determines:
- Number of agents needed (2-5)
- Task dependencies and optimal order
- Handoff points between agents
- File ownership boundaries

### 9. Checkpoint Integration

Sub-agents automatically:
- Save progress every 2 tasks
- Create handoff documentation
- Update the main context file
- Leave breadcrumbs for debugging

### 10. Benefits

- **3-5x faster** for multi-aspect features
- **Better quality** through specialization
- **Clear boundaries** prevent conflicts
- **Natural documentation** from handoffs
- **Easy debugging** with clear ownership

## Example Usage:

```bash
# Start orchestration for a feature
/orchestrate auth --agents=3

# This creates:
# - 3 specialized sub-agents
# - Task assignments based on type
# - Coordination protocol
# - Progress tracking
# - Automatic handoffs
```

## Sub-Agent Lifecycle:

1. **Spawn**: Main agent creates sub-agents with specific contexts
2. **Assign**: Tasks distributed based on expertise
3. **Execute**: Each agent works independently
4. **Communicate**: Updates via shared state
5. **Handoff**: Clear contracts between agents
6. **Merge**: Results combined by orchestrator
7. **Complete**: Main agent validates and closes
