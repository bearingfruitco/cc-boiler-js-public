---
name: prd-to-prp
description: Convert PRD to implementation-ready PRPs using all available documentation
---

# PRD to PRP Conversion (Enhanced)

Convert Product Requirements Document into actionable Product Requirement Prompts, incorporating all architectural analysis and roadmap documentation.

## Usage

```bash
/prd-to-prp [feature-name]
```

## Process

I'll analyze your PRD along with all architectural documentation to create comprehensive PRPs.

### Phase 1: Gather All Documentation

First, I'll collect and analyze all relevant documentation:

```bash
# Check for all documentation sources
echo "=== Gathering Documentation Sources ==="

# 1. Core PRD
if [ -f "docs/project/PROJECT_PRD.md" ]; then
  echo "✓ Found PROJECT_PRD.md"
else
  echo "⚠️ No PRD found - run /prd-from-existing first"
fi

# 2. Agent-OS Analysis
if [ -d ".agent-os" ]; then
  echo "✓ Found .agent-os/ analysis:"
  ls -la .agent-os/product/*.md 2>/dev/null | grep -c ".md" | xargs echo "  - Product docs:"
  ls -la .agent-os/*.md 2>/dev/null | grep -c ".md" | xargs echo "  - Analysis docs:"
fi

# 3. Architecture Documentation
if [ -d "docs/architecture" ]; then
  echo "✓ Found architecture docs:"
  ls -la docs/architecture/*.md 2>/dev/null | grep -c ".md" | xargs echo "  - Architecture files:"
fi

# 4. Improvement Plans
if [ -f "*IMPROVEMENTS.md" ]; then
  echo "✓ Found improvement plans"
fi
```

### Phase 2: Analyze Documentation

I'll read and incorporate:

#### From `.agent-os/` (if exists):
- **product/mission.md** - Product vision and goals
- **product/roadmap.md** - Phased development plan
- **product/tech-stack.md** - Technology decisions
- **product/decisions.md** - Architecture Decision Records (ADRs)
- **ANALYSIS_SUMMARY.md** - Executive summary of current state

#### From `docs/architecture/` (if exists):
- **SYSTEM_ARCHITECTURE.md** - Component overview
- **DATA_FLOW.md** - Data pipeline design
- **INTEGRATION_ARCHITECTURE.md** - External services
- **INFRASTRUCTURE.md** - Deployment architecture
- **SECURITY_ARCHITECTURE.md** - Security controls

#### From Analysis Results:
- **Architectural Debt** - Components needing refactoring
- **Performance Issues** - Optimization opportunities
- **Missing Coverage** - Tests, monitoring, documentation
- **Priority Items** - P0/P1/P2 categorization

### Phase 3: Generate Contextual PRPs

Based on ALL documentation, I'll create PRPs that address:

#### 1. Immediate Architectural Debt
If architectural analysis found issues like:
- Monolithic components (>1000 lines)
- Missing test coverage (<80%)
- Performance bottlenecks
- Security vulnerabilities

I'll create PRPs like:
- `refactor-[component]-prp.md`
- `test-infrastructure-prp.md`
- `performance-optimization-prp.md`
- `security-hardening-prp.md`

#### 2. Roadmap Phase Items
From `.agent-os/product/roadmap.md` phases:
- **Phase 1 (0-30 days)**: Immediate improvements
- **Phase 2 (30-60 days)**: Feature enhancements
- **Phase 3 (60-90 days)**: Scale preparations
- **Phase 4 (90+ days)**: Innovation items

#### 3. Feature-Specific PRPs
For each major feature in the PRD:
```markdown
# PRP Structure
1. Context (from architecture docs)
2. Current State (from analysis)
3. Requirements (from PRD)
4. Technical Approach (from tech-stack)
5. Implementation Steps
6. Testing Strategy
7. Success Metrics
```

### Phase 4: PRP Generation Output

For each identified need, I'll create:

```markdown
# [Feature/Fix Name] PRP

## Context
- Current Architecture: [from docs/architecture/]
- Identified Issues: [from analysis]
- Priority: [P0/P1/P2]
- Phase: [1/2/3/4 from roadmap]

## Requirements
[From PRD and analysis]

## Technical Implementation
[Based on tech-stack and architecture]

## Steps
[Detailed implementation plan]

## Dependencies
[From architecture docs]

## Testing Requirements
[Based on gaps identified]

## Success Criteria
[Measurable outcomes]
```

### Phase 5: Priority Ordering

PRPs will be generated in priority order:

1. **P0 - Critical** (Blocking/Broken)
   - Test infrastructure (if missing)
   - Security vulnerabilities
   - Performance crisis
   - Monolithic refactoring

2. **P1 - Important** (Phase 1 roadmap)
   - Core feature improvements
   - User experience fixes
   - Performance optimization
   - Monitoring setup

3. **P2 - Enhancement** (Phase 2+ roadmap)
   - New features
   - Advanced capabilities
   - Nice-to-have improvements

## Integration with Existing Documentation

This command now:
- ✅ Reads `.agent-os/` analysis results
- ✅ Incorporates `docs/architecture/` findings
- ✅ Uses roadmap phases for prioritization
- ✅ Addresses architectural debt identified
- ✅ Creates actionable, specific PRPs
- ✅ Links PRPs to concrete problems found

## Example Output

After running `/prd-to-prp`, you'll see:

```
📊 Documentation Analysis Complete
Found:
- ✓ PRD with 5 major features
- ✓ Architecture docs (5 files)
- ✓ Roadmap with 4 phases
- ✓ 3 P0 architectural issues
- ✓ 8 P1 improvements identified

🎯 Generating PRPs:

P0 - Critical (Must Fix):
1. Creating: debt-form-refactor-prp.md (3,053 lines → 10 components)
2. Creating: test-infrastructure-prp.md (0% → 80% coverage)
3. Creating: performance-optimization-prp.md (<250ms target)

P1 - Phase 1 (Next 30 days):
4. Creating: monitoring-setup-prp.md
5. Creating: ci-cd-pipeline-prp.md
6. Creating: documentation-system-prp.md

P2 - Enhancements:
7. Creating: ml-scoring-prp.md
8. Creating: advanced-analytics-prp.md

✅ Created 8 PRPs in PRPs/active/
```

## Next Steps

After PRP generation:
1. Review generated PRPs: `/prp list`
2. Convert to issues: `/prp-to-issues`
3. Start implementation: `/fw start [issue-number]`

## Note

This enhanced version ensures PRPs are based on:
- Real architectural analysis
- Actual problems identified
- Roadmap priorities
- Technical debt findings
- Not just theoretical features
