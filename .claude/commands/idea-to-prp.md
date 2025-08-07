---
name: idea-to-prp
description: Convert a rough idea into a structured PRP with research
aliases: [idea, explore-idea, prp-from-idea]
---

# Convert Idea to PRP

Turn a rough idea or feature request into a well-researched, actionable PRP.

## Usage

```bash
/idea-to-prp "I want better analytics tracking"
/idea "Add user segmentation to RudderStack"
/explore-idea "Set up BigQuery for data warehouse"
```

## Process

### Phase 1: Idea Exploration

I'll explore your idea by:

```javascript
function exploreIdea(userIdea) {
  // 1. Extract key concepts
  const concepts = extractConcepts(userIdea);
  // Examples: ["analytics", "tracking", "rudderstack", "bigquery"]
  
  // 2. Map to systems
  const systems = mapToSystems(concepts);
  // Examples: ["rudderstack", "bigquery", "analytics"]
  
  // 3. Check current state
  const currentState = analyzeCurrentState(systems);
  
  // 4. Identify gaps
  const gaps = findGaps(currentState, userIdea);
  
  // 5. Generate recommendations
  return {
    interpretation: "I understand you want to...",
    currentState: "You currently have...",
    gaps: "What's missing...",
    recommendations: "I suggest..."
  };
}
```

### Phase 2: Research & Discovery

```bash
echo "🔍 Researching: ${userIdea}"

# Check existing implementations
echo "📊 Current State:"
- RudderStack: ${checkRudderStack()}
- BigQuery: ${checkBigQuery()}
- Tracking Events: ${countTrackingEvents()}

# Find relevant documentation
echo "📚 Relevant Docs:"
- Internal: ${findInternalDocs()}
- Patterns: ${findPatterns()}
- Examples: ${findExamples()}

# Identify requirements
echo "📋 Requirements:"
- Technical: ${technicalRequirements}
- Business: ${businessRequirements}
- Compliance: ${complianceRequirements}
```

### Phase 3: Structured Proposal

Based on the research, I'll create:

```markdown
# Idea Exploration: ${userIdea}

## 📊 Research Summary

### Your Idea
"${userIdea}"

### My Understanding
${interpretation}

### Current Situation
- **What exists**: ${currentImplementations}
- **What works**: ${workingFeatures}
- **What's missing**: ${gaps}

### Recommended Approach
${recommendations}

## 🎯 Proposed PRP

### Option 1: Quick Win (${quickWinEffort})
${quickWinDescription}
- Effort: ${quickWinDays} days
- Impact: ${quickWinImpact}

### Option 2: Full Solution (${fullSolutionEffort})
${fullSolutionDescription}
- Effort: ${fullSolutionDays} days
- Impact: ${fullSolutionImpact}

### Option 3: Phased Approach
Phase 1: ${phase1Description} (${phase1Days} days)
Phase 2: ${phase2Description} (${phase2Days} days)
Phase 3: ${phase3Description} (${phase3Days} days)

## 📝 Next Steps

Would you like me to create a PRP for:
1. Option 1 (Quick Win)
2. Option 2 (Full Solution)
3. Option 3 (Phased)
4. Custom approach

Run: /create-prp "${selectedOption}"
```

## Example Interactions

### Example 1: Vague Idea

```bash
/idea "better analytics"

🔍 Researching: "better analytics"

📊 Current State:
- RudderStack: ✅ Basic tracking implemented
- Events tracked: 12 (form submissions, page views)
- Destinations: Google Analytics only
- Missing: User traits, conversion tracking, BigQuery

📚 My Understanding:
You want to improve analytics capabilities. Based on your setup:

Recommended Approach:
1. Add user identification (1 day)
2. Implement conversion tracking (2 days)
3. Set up BigQuery warehouse (3 days)
4. Create dashboards (2 days)

Would you like a PRP for any of these?
```

### Example 2: Specific Feature

```bash
/idea "Track user sessions with RudderStack and store in BigQuery"

🔍 Researching: Session tracking + BigQuery storage

📊 Current State:
- RudderStack: ✅ Configured
- Session tracking: ❌ Not implemented
- BigQuery: ⚠️ Credentials exist, not connected

📝 I'll create a comprehensive PRP for:
"Session Tracking with BigQuery Pipeline"

This will include:
- Session management logic
- RudderStack session events
- BigQuery destination setup
- Data schema design
- Real-time streaming

Creating PRP...
✅ Created: PRPs/active/session-tracking-bigquery-prp.md
```

### Example 3: Integration Request

```bash
/idea "Connect RudderStack to our data warehouse"

🔍 Researching: Data warehouse integration

📊 Discovery:
- RudderStack: Active
- BigQuery mentioned in: docs/RUDDERSTACK_BIGQUERY_CONFIG.md
- Warehouse destination: Not configured

Options found:
1. BigQuery (recommended - docs exist)
2. Snowflake (alternative)
3. Redshift (alternative)

Based on existing docs, recommending BigQuery.

Would you like me to create:
/create-prp "rudderstack-bigquery-integration"
```

## Smart Features

### Auto-Detection
- Recognizes system names (RudderStack, Supabase, Sentry)
- Maps generic terms to specific implementations
- Checks for existing documentation

### Context Awareness
- Searches for related implementations
- Checks environment variables
- Finds configuration files
- Reviews documentation

### Recommendation Engine
- Suggests feasible approaches
- Estimates effort
- Identifies dependencies
- Proposes phasing

## Workflow Integration

```mermaid
graph LR
    A[Rough Idea] --> B[/idea-to-prp]
    B --> C[Research & Discovery]
    C --> D[Structured Options]
    D --> E[/create-prp]
    E --> F[Detailed PRP]
    F --> G[/prp-to-issues]
    G --> H[GitHub Issue]
    H --> I[/fw start]
```

This gives you a complete path from idea to implementation!
