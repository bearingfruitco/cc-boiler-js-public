# 🎯 Complete Command Decision Guide - When to Use What

> Your visual roadmap for choosing the right command at the right time in Claude Code Boilerplate

## 🗺️ Quick Decision Map

```mermaid
graph TD
    Start[Starting Work] --> Q1{New or Existing Project?}
    
    Q1 -->|New Project| NewPath[/init-project]
    Q1 -->|Existing Project| ExistingPath[/ae]
    
    NewPath --> Q2{Have GitHub Issue?}
    ExistingPath --> DesignCheck[/mds analyze]
    
    Q2 -->|Yes| FW[/fw start #123]
    Q2 -->|No| Q3{Clear Requirements?}
    
    DesignCheck --> Q4{Want to Migrate?}
    Q4 -->|Yes| Migrate[/mds migrate]
    Q4 -->|No| Q2
    
    Q3 -->|Yes + Examples| PRP[/create-prp]
    Q3 -->|Yes, No Examples| SimplePRP[/create-prp simple]
    Q3 -->|No, Exploratory| PRD[/prd]
    
    FW --> Q5{Issue Type?}
    Q5 -->|Feature| FeaturePRP[/create-prp]
    Q5 -->|Bug| BugTrack[/bt add]
    Q5 -->|Enhancement| PRD2[/prd]
    
    PRP --> Execute[/prp-execute]
    SimplePRP --> Execute
    PRD --> Tasks[/gt]
    PRD2 --> Tasks
    FeaturePRP --> Execute
    
    Execute --> Process[/pt]
    Tasks --> Process
    BugTrack --> Debug[/ut + /vp]
    
    Process --> Verify[/verify]
    Debug --> Fix[/mt]
    Fix --> Verify
    
    Verify --> Complete[/fw complete]
```

## 📊 Command Categories

### 🚀 Starting Commands

| Scenario | Command | When to Use | Next Steps |
|----------|---------|-------------|------------|
| **New Session** | `/sr` | ALWAYS first command | Load context → Choose workflow |
| **New Project** | `/init-project` | Fresh Next.js project | → `/fw start` or `/gi PROJECT` |
| **Existing Project** | `/ae` | Adding to existing code | → `/mds analyze` → `/chain onboard-existing` |
| **Resume Feature** | `/fw resume` | Continue yesterday's work | → `/pt` to continue tasks |
| **Check Status** | `/work-status` | See what needs doing | → Resume appropriate work |

### 🎨 Creation Commands

```mermaid
graph LR
    Create[Need to Create] --> Type{What Type?}
    
    Type -->|Component| CC[/cc ComponentName]
    Type -->|Form| CTF[/ctf FormName]
    Type -->|API Endpoint| API[/create-api]
    Type -->|Event Handler| EH[/create-event-handler]
    Type -->|Database Schema| DB[/create-schema]
    
    CC --> Validate[/vd]
    CTF --> Security[/audit-form-security]
    API --> Test[/test-api]
    EH --> Async[/validate-async]
    DB --> Migration[/db-migrate]
```

### 🧠 Planning & Analysis Commands

| Command | Best For | Example Use Case | Typical Duration |
|---------|----------|------------------|------------------|
| `/ut` | Complex problems needing deep analysis | "Optimize database queries across system" | 5-10 min thinking |
| `/vp` | UI/UX design with visual feedback | "Redesign mobile navigation" | Iterative 15-30 min |
| `/prd` | Exploratory features | "Add AI chat to app" | 10-15 min |
| `/create-prp` | Clear features with examples | "Add Stripe payment like [example]" | 5 min |
| `/research` | Technical investigation | "Best auth strategy for SaaS" | 20-30 min |

### 🔧 Development Workflow Commands

```mermaid
flowchart TD
    Start[Development Start] --> Choice{Workflow Type?}
    
    Choice -->|PRD-Driven| PRDFlow
    Choice -->|PRP-Driven| PRPFlow
    Choice -->|TDD| TDDFlow
    Choice -->|Debug| DebugFlow
    
    subgraph PRDFlow[PRD Workflow]
        P1[/prd feature] --> P2[/prd-async]
        P2 --> P3[/gt feature]
        P3 --> P4[/pt feature]
        P4 --> P5[/grade]
    end
    
    subgraph PRPFlow[PRP Workflow]
        R1[/create-prp feature] --> R2[/prp-validate]
        R2 --> R3[/prp-execute --level 1]
        R3 --> R4[/prp-execute --level 2]
        R4 --> R5[/prp-complete]
    end
    
    subgraph TDDFlow[TDD Workflow]
        T1[/tdd-workflow feature] --> T2[Write Test]
        T2 --> T3[Run Test - Fail]
        T3 --> T4[Implement]
        T4 --> T5[Run Test - Pass]
        T5 --> T6[/verify --tdd]
    end
    
    subgraph DebugFlow[Debug Workflow]
        D1[/bt add "bug"] --> D2[/ut "analyze bug"]
        D2 --> D3[/vp "visualize issue"]
        D3 --> D4[/mt "fix"]
        D4 --> D5[/bt resolve]
    end
```

### 🧪 Validation & Testing Commands

| Stage | Commands | Purpose | Success Criteria |
|-------|----------|---------|------------------|
| **Code Quality** | `/vd`, `/lint`, `/typecheck` | Instant validation | Zero violations |
| **Component Testing** | `/tr current`, `/tr:components` | Unit tests | 100% pass |
| **Integration** | `/btf`, `/test:e2e` | Browser testing | All flows work |
| **Performance** | `/lighthouse`, `/perf-monitor` | Speed check | Score >90 |
| **Security** | `/sc all`, `/audit-form-security` | Security scan | No vulnerabilities |
| **Completion** | `/verify --full`, `/grade` | Final check | >80% PRD alignment |

### 🚀 Advanced Orchestration

```mermaid
graph TD
    Complex[Complex Feature] --> Analyze{Can Parallelize?}
    
    Analyze -->|Yes| Orchestrate[/orch feature]
    Analyze -->|No| Sequential[/pt feature]
    
    Orchestrate --> Agents{Spawn Agents}
    Agents --> A1[Agent 1: API]
    Agents --> A2[Agent 2: UI]
    Agents --> A3[Agent 3: Tests]
    
    A1 --> Monitor[/sas - Monitor]
    A2 --> Monitor
    A3 --> Monitor
    
    Monitor --> Sync[/ov - Overview]
    Sequential --> SingleAgent[Process Tasks]
    
    Sync --> Merge[Merge Work]
    SingleAgent --> Complete[/fw complete]
    Merge --> Complete
```

## 🎯 Scenario-Based Decision Trees

### Scenario 1: "I need to add user authentication"

```mermaid
flowchart LR
    Auth[Add Authentication] --> Exist{Existing Auth?}
    
    Exist -->|No| FromScratch
    Exist -->|Yes| Enhance
    
    subgraph FromScratch[Build New]
        FS1[/ut "auth strategy"] --> FS2[/prd authentication]
        FS2 --> FS3[/gt authentication]
        FS3 --> FS4[/orch authentication]
    end
    
    subgraph Enhance[Enhance Existing]
        E1[/ae] --> E2[/research auth-improvements]
        E2 --> E3[/create-prp add-oauth]
        E3 --> E4[/prp-execute]
    end
```

### Scenario 2: "The form submission is failing"

```mermaid
flowchart TD
    Bug[Form Failing] --> Track[/bt add "form submission fails"]
    
    Track --> Investigate{Investigation}
    
    Investigate --> I1[/ut "analyze form failure"]
    Investigate --> I2[/vp "show form issue"]
    Investigate --> I3[/validate-async]
    
    I1 --> Root[Identify Root Cause]
    I2 --> Root
    I3 --> Root
    
    Root --> Fix{Fix Type?}
    
    Fix -->|Async Issue| FA[/create-event-handler]
    Fix -->|Validation| FV[/ctf FormName --fix]
    Fix -->|API| FAPI[/debug-api]
    
    FA --> Test[/btf]
    FV --> Test
    FAPI --> Test
    
    Test --> Resolve[/bt resolve 1]
```

### Scenario 3: "I need to improve performance"

```mermaid
flowchart LR
    Perf[Performance Issue] --> Measure[/lighthouse]
    
    Measure --> Analyze[/perf-monitor]
    
    Analyze --> Type{Issue Type?}
    
    Type -->|Bundle Size| Bundle[/analyze-bundle]
    Type -->|Database| DB[/ut "optimize queries"]
    Type -->|Rendering| Render[/vp "identify renders"]
    
    Bundle --> Optimize[/refactor --performance]
    DB --> Optimize
    Render --> Optimize
    
    Optimize --> Verify[/lighthouse --compare]
```

## 🔄 Daily Workflow Patterns

### Morning Startup
```bash
/sr                    # Load everything
/work-status           # See active work
/bt list --open        # Check bugs
/todo                  # Review TODOs
/cp load [context]     # Load appropriate context
```

### Feature Development
```bash
/fw start 123          # Start from issue
/create-prp feature    # Define clear spec
/prp-execute --level 1 # Validate approach
/pt feature            # Process tasks
/verify --full         # Ensure complete
/fw complete           # Create PR
```

### Bug Fixing
```bash
/bt list               # See all bugs
/bt start 5            # Start bug #5
/ut "analyze bug"      # Deep analysis
/vp "show issue"       # Visual debugging
/mt "implement fix"    # Micro-task fix
/verify --full         # Validate fix
/bt resolve 5          # Mark complete
```

### Code Review Prep
```bash
/lint:fix              # Fix style issues
/vd                    # Validate design
/test:all              # Run all tests
/sc all                # Security check
/grade                 # Check PRD alignment
/pr-feedback           # Get AI review
```

## 💡 Command Combination Patterns

### Pattern 1: Full Feature Implementation
```bash
/chain feature-complete
# Runs: /fw start → /create-prp → /prp-execute → /pt → /verify → /fw complete
```

### Pattern 2: Quick Component
```bash
/cc Button && /vd && /tr Button
# Create → Validate → Test
```

### Pattern 3: Performance Optimization
```bash
/chain performance-optimize
# Runs: /lighthouse → /perf-monitor → /ut → /refactor → /lighthouse
```

### Pattern 4: Existing Project Onboarding
```bash
/chain onboard-existing
# Runs: /ae → /mds analyze → /create-prd-from-existing → /task-ledger sync → /sr
```

## 🚨 Red Flags - Wrong Command Usage

| ❌ Don't Do This | ✅ Do This Instead | Why |
|------------------|-------------------|-----|
| Jump straight to `/pt` | Start with `/sr` | Lost context = wasted time |
| `/cc` without checking | `/exists Button` first | Avoid duplicates |
| `/prd` for simple features | `/create-prp` with examples | Faster with clear specs |
| Manual design fixes | `/mds migrate` | Automated = consistent |
| `/fw complete` without `/verify` | Always `/verify --full` first | Catches issues early |
| Sequential `/mt` for parallel work | `/orch` for multi-part features | 3x faster completion |

## 📈 Efficiency Tips

### Use Chains for Common Workflows
```bash
/chain daily-startup    # Morning routine
/chain safe-deploy      # Pre-deployment checks
/chain quick-fix        # Bug fix workflow
```

### Let Auto-Enhancement Work
- Complex tasks auto-trigger `/ut`
- Multi-file changes auto-suggest `/orch`
- Design violations auto-run `/vd`

### Trust the Suggestions
After each command, follow the "Next steps" suggestions - they're based on successful patterns from 50+ projects.

### Parallel by Default
For features with 3+ tasks, always check:
```bash
/orch feature --preview
# Shows time saved with parallel execution
```

## 🎯 Quick Reference Card

```
Starting Work:
  Always: /sr
  New Project: /init-project  
  Existing: /ae → /mds analyze

Creating:
  Component: /cc
  Form: /ctf
  API: /create-api

Planning:
  Complex: /ut
  Visual: /vp
  Exploratory: /prd
  Clear: /create-prp

Development:
  Tasks: /pt
  Tests: /tdd-workflow
  Debug: /bt → /ut → /mt

Validation:
  Design: /vd
  Tests: /tr
  Security: /sc
  Complete: /verify --full

Completion:
  Grade: /grade
  PR: /fw complete
```

---

**Remember**: The commands are designed to guide you. When in doubt, use `/help [what you want to do]` for context-aware suggestions!
