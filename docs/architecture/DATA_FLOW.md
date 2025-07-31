# Data Flow Architecture

> How data moves through the Claude Code Boilerplate system

## 🌊 Data Flow Overview

The system processes data through multiple layers, each adding value and validation while maintaining performance and security.

## 📍 Primary Data Flows

### 1. Command Execution Flow

```
User Input → Command Resolution → Parameter Validation → Execution
     ↓              ↓                    ↓                  ↓
   Terminal    Alias Mapping      Type Checking      Core Logic
                    ↓                    ↓                  ↓
              Command Cache        Schema Valid      File System
                                                           ↓
                                                    Response Format
                                                           ↓
                                                    User Response
```

**Example: Creating a Component**
```bash
/cc Button primary
     ↓
Resolve: create-component
     ↓
Validate: name="Button", variant="primary"
     ↓
Pre-hooks: Design validation
     ↓
Execute: Generate component code
     ↓
Post-hooks: Update indexes, emit events
     ↓
Response: "✅ Created Button component"
```

### 2. Multi-Agent Data Flow

```
Task Input → Task Analysis → Agent Selection → Work Distribution
     ↓             ↓               ↓                  ↓
  User Goal   Requirements    Best Match      Parallel Tasks
                   ↓               ↓                  ↓
              Complexity      Load Agents      Individual Work
                                   ↓                  ↓
                            Agent Context      Results Stream
                                                      ↓
                                              Result Synthesis
                                                      ↓
                                              Combined Output
```

**Example: Full Feature Implementation**
```
"Build user authentication" 
           ↓
Orchestrator Analysis:
- Needs: API, UI, Database, Tests
           ↓
Spawn Agents:
- Backend: API + Database
- Frontend: UI Components  
- QA: Test Suite
           ↓
Parallel Execution:
┌──────────────┬───────────────┬──────────────┐
│   Backend    │   Frontend    │      QA      │
│ • API routes │ • Login form  │ • API tests  │
│ • JWT logic  │ • User menu   │ • UI tests   │
│ • DB schema  │ • Auth hook   │ • E2E flows  │
└──────────────┴───────────────┴──────────────┘
           ↓
Synthesis & Integration
```

### 3. State Management Flow

```
Operation → State Capture → Storage → Compression → Retrieval
     ↓            ↓            ↓          ↓            ↓
  Any Action   Current     .claude/    Optimize     /sr Load
               Context      state/      for LLM
                  ↓            ↓          ↓            ↓
              Changes     Version    Prioritize    Full Context
                          Control     Important
```

**State Data Structure**
```json
{
  "session": {
    "id": "session-123",
    "started": "2025-07-30T10:00:00Z",
    "context": {
      "working_on": "user authentication",
      "last_command": "/cc LoginForm",
      "current_files": ["components/LoginForm.tsx"],
      "active_branch": "feature/auth"
    }
  },
  "history": [
    {
      "command": "/create-prp auth-system",
      "timestamp": "2025-07-30T10:05:00Z",
      "result": "success",
      "output": "Created auth-system.prp.md"
    }
  ],
  "cache": {
    "validations": {},
    "resolutions": {}
  }
}
```

### 4. Event System Data Flow

```
Source → Event Creation → Event Bus → Handlers → Side Effects
   ↓           ↓             ↓          ↓            ↓
Action    Structured      Publish   Subscribe    Execute
          Message                    Process     Actions
             ↓               ↓          ↓            ↓
          Metadata      Queue/Route  Transform   Update UI
                                                Database
                                                Trigger Chains
```

**Event Example**
```typescript
// Component created event
{
  type: 'component.created',
  timestamp: Date.now(),
  data: {
    name: 'Button',
    path: 'components/ui/Button.tsx',
    variant: 'primary',
    creator: 'create-component'
  },
  metadata: {
    session: 'session-123',
    user: 'developer',
    triggered_by: 'command'
  }
}

// Triggers:
→ Update component index
→ Run design validation
→ Generate documentation
→ Notify other systems
```

### 5. Validation Data Flow

```
Input → Level 1 → Level 2 → Level 3 → Level 4 → Result
  ↓        ↓         ↓         ↓         ↓        ↓
Code    Syntax   Semantic  Design    Quality   Pass/Fail
         Check    Rules    System    Metrics   + Report
           ↓         ↓         ↓         ↓        ↓
        Parse    Logic    Tokens    Best      Actions
                 Valid    Match    Practice
```

**Validation Pipeline**
```javascript
// Design validation flow
validateComponent(component) {
  // Level 1: Syntax
  const syntaxValid = checkJSXSyntax(component);
  
  // Level 2: Semantic
  const propsValid = checkPropTypes(component);
  const hooksValid = checkHookRules(component);
  
  // Level 3: Design System
  const tokensValid = checkDesignTokens(component);
  const spacingValid = checkSpacingRules(component);
  
  // Level 4: Quality
  const a11yValid = checkAccessibility(component);
  const perfValid = checkPerformance(component);
  
  return {
    valid: all([syntaxValid, propsValid, ...]),
    report: generateReport(allChecks),
    fixes: suggestFixes(failures)
  };
}
```

## 🔄 Async Data Patterns

### 1. Event Queue Processing
```
Events → Queue → Batch → Process → Complete
   ↓       ↓       ↓        ↓         ↓
Emit    FIFO    Group   Handle    Cleanup
        Order   Similar  Async    Confirm
```

### 2. File Operation Pipeline
```
Request → Lock → Read → Transform → Write → Unlock → Event
   ↓        ↓      ↓        ↓         ↓       ↓       ↓
Check    Acquire  Load   Modify    Save   Release  Notify
Access   Mutex    File   Content   Atomic  Lock    System
```

### 3. Context Streaming
```
Large Context → Chunk → Stream → Process → Reassemble
      ↓           ↓        ↓         ↓          ↓
   Detect      Split    Send     Handle     Combine
   Size        Smart    Parts    Each       Results
```

## 🛡️ Security Data Flow

### 1. Input Sanitization
```
User Input → Sanitize → Validate → Execute
     ↓           ↓          ↓         ↓
Raw Data    Clean HTML   Schema    Safe Op
            Escape SQL    Check     
            Strip XSS     Types
```

### 2. PII Detection Flow
```
Content → Scan → Detect → Flag → Handle
   ↓        ↓       ↓       ↓       ↓
Text     Patterns  PII   Mark    Redact
Data     Regex    Found  Fields  Store
         ML/AI                   Encrypt
```

### 3. Authentication Flow
```
Request → Token → Verify → Authorize → Execute
   ↓        ↓        ↓         ↓          ↓
Headers   JWT     Decode    Check      Proceed
         Extract  Valid?    Perms      Or Deny
```

## 📊 Performance Optimization Flows

### 1. Caching Strategy
```
Request → Cache Check → Miss? → Compute → Store → Return
   ↓          ↓          ↓        ↓        ↓       ↓
Query     Hit/Miss    Fetch    Process   Cache   Response
           ↓                               Update
         Return                            TTL
         Cached
```

### 2. Lazy Loading Flow
```
Initialize → Minimal Load → On Demand → Full Load
     ↓            ↓            ↓           ↓
  Start      Core Only    User Action   Load Module
  Fast       Commands     Need Agent?   Agent Data
```

### 3. Parallel Processing
```
Task → Split → Distribute → Process → Merge
  ↓      ↓         ↓          ↓        ↓
Large  Chunks   Workers    Parallel  Combine
Job    Smart    Assign     Execute   Results
```

## 🔌 Integration Data Flows

### 1. GitHub Integration
```
Local → Git → GitHub API → Webhooks → Local
  ↓      ↓        ↓           ↓         ↓
Code   Commit   Push       Trigger   Update
Change  Stage   Create PR   Actions   Status
```

### 2. Database Operations
```
Query → ORM → Connection → Execute → Transform → Return
  ↓      ↓        ↓          ↓          ↓         ↓
Build  Drizzle  Pool      Database   Format    Model
SQL    Prisma   Manage    Process    Results   Object
```

### 3. External Services
```
Request → Auth → API Call → Response → Process → Store
   ↓       ↓        ↓          ↓         ↓        ↓
Build   Add Key  HTTP/S     Parse     Extract   Cache
Call    Headers  Request    JSON      Data      Local
```

## 🎯 Data Flow Best Practices

### 1. **Immutability**
- Never mutate data directly
- Create new objects for changes
- Use functional transformations

### 2. **Error Boundaries**
- Catch errors at each layer
- Provide fallback flows
- Log for debugging

### 3. **Data Validation**
- Validate at entry points
- Use schema validation
- Type check thoroughly

### 4. **Performance**
- Stream large data
- Cache expensive operations
- Use async patterns

### 5. **Security**
- Sanitize all inputs
- Encrypt sensitive data
- Audit data access

---

*Data Flow Architecture v4.0.0*  
*Last Updated: 2025-07-30*
