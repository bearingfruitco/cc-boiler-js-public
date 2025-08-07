---
name: prp-to-issues
description: Convert PRPs to GitHub issues with full context awareness
aliases: [prp2i, ptoi]
---

# PRP to GitHub Issues Converter

Convert Product Requirement Prompts (PRPs) into actionable GitHub issues with full architectural context.

## Usage

```bash
/prp-to-issues              # Convert all active PRPs
/prp-to-issues [prp-name]   # Convert specific PRP
/ptoi                       # Short alias
```

## Process

### Phase 1: Discover PRPs

I'll scan for PRPs and their context:

```bash
# Check for active PRPs
echo "=== Scanning for PRPs ==="
ls -la PRPs/active/*.md 2>/dev/null || echo "No active PRPs found"

# Check for architectural context
echo "=== Checking Context ==="
test -d ".agent-os" && echo "✓ Analysis context available"
test -d "docs/architecture" && echo "✓ Architecture docs available"
test -f "docs/project/PROJECT_PRD.md" && echo "✓ PRD available"
```

### Phase 2: Analyze Each PRP

For each PRP, I'll extract:

1. **Core Requirements**
   - Feature description
   - Technical requirements
   - Success criteria

2. **Architectural Context**
   - Related components (from architecture docs)
   - Dependencies (from tech-stack)
   - Integration points

3. **Priority & Phasing**
   - P0/P1/P2 classification
   - Roadmap phase (1-4)
   - Estimated effort

4. **Technical Debt**
   - If PRP addresses debt (e.g., refactoring)
   - Current issues (lines of code, missing tests)
   - Target improvements

### Phase 3: Generate Smart Issues

Each issue will include:

```markdown
## 🎯 [PRP Title]

### 📊 Context
- **Priority**: P0/P1/P2
- **Phase**: [1-4] from roadmap
- **Type**: Feature/Refactor/Infrastructure/Testing
- **Effort**: S/M/L/XL

### 🏗️ Current State
[From architectural analysis]
- Component: [e.g., DebtForm - 3,053 lines]
- Coverage: [e.g., 0% tests]
- Performance: [e.g., <250ms target]

### ✅ Acceptance Criteria
[From PRP success criteria]
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### 🔧 Technical Requirements
[From architecture docs]
- Framework: [Next.js 15, React 19]
- Dependencies: [Required packages]
- Integration: [External services]

### 📋 Implementation Tasks
- [ ] Task 1: [Specific action]
- [ ] Task 2: [Specific action]
- [ ] Task 3: [Specific action]

### 🧪 Testing Requirements
- [ ] Unit tests: [Coverage target]
- [ ] Integration tests: [Key flows]
- [ ] E2E tests: [Critical paths]

### 📚 Documentation
- [ ] Update API docs
- [ ] Update component docs
- [ ] Update architecture diagrams

### 🔗 Related
- PRP: `PRPs/active/[name].md`
- Architecture: `docs/architecture/[relevant].md`
- Roadmap Phase: [Link to phase]
```

### Phase 4: Issue Creation Strategy

#### For Refactoring PRPs (e.g., monolithic component):
```markdown
# Main Issue: Refactor DebtForm Component

## Sub-issues (automatically created):
1. Extract validation logic → separate module
2. Create FormSection components (10 components)
3. Implement state management (Zustand/Context)
4. Add comprehensive tests (80% coverage)
5. Update documentation
```

#### For Feature PRPs:
```markdown
# Main Issue: [Feature Name]

## Sub-issues (if complex):
1. Backend API implementation
2. Frontend UI components
3. Integration & testing
4. Documentation & deployment
```

#### For Infrastructure PRPs:
```markdown
# Main Issue: [Infrastructure Item]

## Checklist approach (single issue):
- [ ] Set up testing framework
- [ ] Configure CI/CD
- [ ] Add monitoring
- [ ] Document setup
```

### Phase 5: Smart Batching

Based on PRP analysis:

1. **Group Related PRPs**
   - Refactoring + Testing = Single epic
   - Related features = Linked issues

2. **Order by Dependencies**
   - Infrastructure first
   - Refactoring before features
   - Testing parallel to development

3. **Respect Phases**
   - Phase 1 (0-30 days): P0 + immediate fixes
   - Phase 2 (30-60 days): Features + enhancements
   - Phase 3+: Scale + innovation

## Example Output

```bash
/prp-to-issues

📊 Found 5 Active PRPs:
1. debt-form-refactor-prp.md (P0 - Refactoring)
2. test-infrastructure-prp.md (P0 - Infrastructure)
3. performance-optimization-prp.md (P1 - Performance)
4. monitoring-setup-prp.md (P1 - Infrastructure)
5. ml-scoring-prp.md (P2 - Feature)

🔍 Analyzing Context:
- Architectural debt: 3,053-line component
- Test coverage: 0%
- Performance target: <250ms

📝 Creating Issues:

Epic #1: Critical Refactoring & Testing
├── Issue #23: Refactor DebtForm Component (P0)
│   └── 5 sub-tasks created
├── Issue #24: Implement Test Infrastructure (P0)
│   └── Single issue with checklist
└── Issue #25: Performance Optimization (P1)
    └── 3 sub-tasks created

Feature Issues:
├── Issue #26: Monitoring & Observability (P1)
└── Issue #27: ML Scoring System (P2)

✅ Created 5 main issues + 8 sub-issues
📁 Updated: docs/project/ISSUE_MAP.md
🔗 Repository: shawnsmith/debt-funnel
```

## Integration with Workflow

After running this command:

1. **Review Issues**: Check GitHub for created issues
2. **Start Development**: `/fw start [issue-number]`
3. **Track Progress**: `/issue-kanban`
4. **Update PRPs**: Move completed PRPs to `PRPs/completed/`

## Smart Features

### Detects Issue Type:
- **Monolithic refactor** → Creates sub-issues for each component
- **Test setup** → Single issue with comprehensive checklist
- **Feature** → Evaluates complexity for sub-issue creation
- **Bug fix** → Simple issue with clear criteria

### Uses All Documentation:
- `.agent-os/product/roadmap.md` → Phases and timeline
- `docs/architecture/*.md` → Technical context
- `*IMPROVEMENTS.md` → Priority classification
- PRP content → Requirements and tasks

### Prevents Duplicates:
- Checks existing issues before creating
- Links related issues
- Updates rather than duplicates

## Next Steps

After issue creation:
```bash
/issue-kanban          # View issue board
/fw start [issue#]     # Start TDD workflow
/track-progress        # Monitor completion
```

This ensures your GitHub issues have full context from:
- PRP requirements
- Architectural analysis
- Roadmap phases
- Technical debt findings
- Not just generic tasks!
