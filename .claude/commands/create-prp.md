---
name: create-prp
description: Create a PRP for a specific feature or idea with full context discovery
aliases: [prp-new, new-prp, prp]
---

# Create PRP for Feature/Idea

Create a focused PRP for a specific feature, integration, or improvement idea.

## Usage

```bash
/create-prp rudderstack-enhanced-tracking
/create-prp "Add BigQuery destination to RudderStack"
/prp "Implement A/B testing with RudderStack"
```

## Process

### Phase 1: Understand the Request

I'll analyze your feature request to determine:
- Type (feature/integration/refactor/infrastructure)
- Priority (P0/P1/P2)
- Dependencies
- Context needed

### Phase 2: Discover Existing Context

Based on your feature, I'll search for:

```javascript
function discoverFeatureContext(featureName) {
  const contexts = {
    'rudderstack': {
      patterns: [
        'src/lib/analytics/**',
        'src/lib/tracking/**',
        'docs/*RUDDER*.md',
        '.env.example'
      ],
      check: [
        'Current implementation status',
        'Existing tracking events',
        'Configured destinations',
        'Environment variables'
      ]
    },
    'supabase': {
      patterns: [
        'src/lib/supabase/**',
        'supabase/**',
        'docs/*SUPABASE*.md',
        '.env.example'
      ],
      check: [
        'Client configuration',
        'Database schema',
        'Auth implementation',
        'RLS policies'
      ]
    },
    'bigquery': {
      patterns: [
        'docs/*BIGQUERY*.md',
        'src/lib/warehouse/**',
        'scripts/bigquery/**'
      ],
      check: [
        'Service account setup',
        'Dataset configuration',
        'Pipeline implementation'
      ]
    },
    'testing': {
      patterns: [
        '**/*.test.*',
        '**/*.spec.*',
        'jest.config.*',
        'vitest.config.*'
      ],
      check: [
        'Test framework',
        'Coverage configuration',
        'Existing tests'
      ]
    }
  };
  
  // Find which context applies
  const relevantContext = detectRelevantContext(featureName);
  return gatherContext(contexts[relevantContext]);
}
```

### Phase 3: Generate Validator-Compliant PRP

```markdown
# PRP: ${featureName} - One-Pass Implementation Guide

> **PRP = PRD + Curated Codebase Intelligence + Validation Loops**
> Feature requested by user: "${userDescription}"

## 🎯 Goal
${generateGoal(featureName, context)}

## 🔑 Why This Matters
- **User Value**: ${userValue}
- **Business Value**: ${businessValue}  
- **Technical Value**: ${technicalValue}

## ✅ Success Criteria (Measurable)
${generateSuccessCriteria(featureName)}

## 📚 Required Context

### Current Implementation Status
\`\`\`yaml
${currentStatus}
\`\`\`

### Documentation & References
\`\`\`yaml
${discoveredFiles.map(f => formatReference(f))}
\`\`\`

### Known Gotchas & Critical Warnings
\`\`\`markdown
${generateWarnings(featureName, context)}
\`\`\`

### Required Patterns From Codebase
\`\`\`typescript
${extractPatterns(context)}
\`\`\`

## 🏗️ Implementation Blueprint

${generateImplementationPlan(featureName, context)}

## 🧪 Validation Loops

${generateValidationLoops(featureName)}

## 🚫 Common Mistakes to Avoid
${generateMistakes(featureName)}

## 📊 Success Metrics
${generateMetrics(featureName)}
```

## Examples

### Example 1: RudderStack Enhancement

```bash
/create-prp "Enhanced RudderStack tracking with user traits and BigQuery"

I'll create a PRP for enhanced RudderStack tracking.

🔍 Discovering current implementation...
✓ Found: src/lib/analytics/rudderstack.ts
✓ Status: Basic tracking implemented
✓ Missing: User traits, BigQuery destination

📝 Creating PRP with:
- Goal: Enhance tracking with user identification and warehouse
- Context: 5 files found
- Implementation: 3 phases
- Validation: 4 loops

✅ Created: PRPs/active/rudderstack-enhanced-tracking-prp.md
```

### Example 2: New Feature

```bash
/create-prp "A/B testing framework using RudderStack"

I'll create a PRP for A/B testing.

🔍 Discovering context...
✓ RudderStack configured
✓ No existing A/B testing
✓ Can leverage track() for experiments

📝 Creating PRP with:
- Goal: Implement A/B testing with variant tracking
- Context: Existing analytics setup
- Implementation: Experiment engine + tracking
- Validation: Statistical significance testing

✅ Created: PRPs/active/ab-testing-framework-prp.md
```

## Special Features for Common Requests

### RudderStack PRPs
When creating RudderStack PRPs, I'll check:
- Current tracking implementation
- Events being tracked
- Destinations configured
- BigQuery connection status
- GTM overlap
- User identification setup

### Supabase PRPs
When creating Supabase PRPs, I'll check:
- Database schema
- Auth configuration
- RLS policies
- Real-time subscriptions
- Edge functions

### Testing PRPs
When creating testing PRPs, I'll check:
- Current coverage
- Test framework
- CI/CD setup
- Missing test types

## Integration with Workflow

After creating a PRP:

```bash
# 1. Review the PRP
cat PRPs/active/[feature-name]-prp.md

# 2. Convert to GitHub issue
/prp-to-issues [feature-name]

# 3. Start development
/fw start [issue-number]
```

## Smart Context Discovery

The command will:
1. Parse your feature description
2. Identify related systems
3. Find existing implementations
4. Check for conflicts
5. Gather relevant patterns
6. Create comprehensive PRP

This ensures your PRP has everything needed for implementation!
