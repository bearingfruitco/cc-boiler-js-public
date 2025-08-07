---
name: analyze-for-prps
description: Analyze project and create a PRP gameplan without creating the actual PRPs
aliases: [prp-analysis, prp-plan, analyze-prps]
---

# Analyze for PRPs - Create the Gameplan

Analyze the entire project to determine what PRPs are needed, without creating them yet.

## Usage

```bash
/analyze-for-prps
/prp-plan  # alias
```

## Process

### Phase 1: Comprehensive Analysis

I'll analyze:

1. **Documentation Review**
   ```bash
   # Check all documentation sources
   - .agent-os/product/roadmap.md (phases)
   - .agent-os/product/tech-stack.md (technology)
   - .agent-os/ANALYSIS_SUMMARY.md (findings)
   - docs/architecture/*.md (system design)
   - *IMPROVEMENTS.md (priority items)
   - docs/project/PROJECT_PRD.md (requirements)
   ```

2. **Current State Discovery**
   ```bash
   # Find what's implemented
   - Component sizes (lines of code)
   - Test coverage percentage
   - Configured services (env vars)
   - Partial implementations
   - Working features
   - Database schema
   ```

3. **Gap Analysis**
   ```bash
   # Identify what's needed
   - Architectural debt
   - Missing features
   - Incomplete integrations
   - Performance issues
   - Test coverage gaps
   ```

### Phase 2: Generate PRP Gameplan

I'll create a structured plan:

```markdown
# PRP Generation Gameplan

## 📊 Analysis Summary
- Components analyzed: X
- Services checked: Y
- Issues found: Z

## 🎯 Recommended PRPs (Prioritized)

### Priority 0 (Critical - Do First)
1. **debt-form-refactor**
   - Problem: 3,053-line monolithic component
   - Impact: Blocking maintainability
   - Effort: 5-7 days
   - Dependencies: None

2. **test-infrastructure**
   - Problem: 0% test coverage
   - Impact: No safety net for changes
   - Effort: 3-4 days
   - Dependencies: None

### Priority 1 (Important - Do Next)
3. **supabase-integration**
   - Problem: Configured but not implemented
   - Current: Env vars set, no client usage
   - Effort: 3-5 days
   - Dependencies: None

4. **rudderstack-bigquery**
   - Problem: Missing data warehouse
   - Current: RudderStack works, no BigQuery
   - Effort: 2-3 days
   - Dependencies: RudderStack working

### Priority 2 (Enhancement - Do Later)
5. **sentry-enhancement**
   - Problem: Basic implementation only
   - Current: Configured, minimal usage
   - Effort: 2 days
   - Dependencies: None

## 📁 Context Files for Each PRP

### For debt-form-refactor:
- src/app/[domain]/optin/[funnel]/components/debt/DebtForm.tsx
- src/lib/analytics/rudderstack.ts (preserve tracking)
- All child components already extracted

### For test-infrastructure:
- package.json (test dependencies)
- vitest.config.* or jest.config.*
- Any existing *.test.ts files

### For supabase-integration:
- .env.example (configured vars)
- src/lib/supabase/* (if exists)
- supabase/migrations/* (if exists)

[etc...]

## ⚠️ Warnings & Considerations

- **Revenue Critical**: DebtForm handles all lead generation
- **Preserve Tracking**: RudderStack events must not change
- **Database Schema**: Must be additive only
- **GTM Not Needed**: RudderStack handles GA already

## 📋 Recommended Approach

1. Create PRPs in this order (one at a time)
2. Each PRP should take 10-15 minutes to generate
3. Review each PRP before creating the next
4. Convert to issues only after all PRPs created

## 🚀 Next Command

To create these PRPs one by one, run:
```
/prp-gameplan-execute
```

This will create each PRP with full context and safety checks.
```

### Phase 3: Output Format

The gameplan will be saved as:
- `PRPs/gameplan/prp-gameplan.md`
- Includes priority, effort, dependencies
- Lists all context files needed
- Shows what to preserve

## Next Steps

After analysis, you'll have:
1. Clear list of needed PRPs
2. Priority order for creation
3. Context files identified
4. Warnings about critical code
5. Ready to execute the plan

Run `/prp-gameplan-execute` to create them one by one.
