---
name: prd-to-prp
description: Convert PRD to implementation-ready PRPs with context discovery
---

# PRD to PRP Conversion (Context-Aware)

Convert Product Requirements Document into actionable Product Requirement Prompts with automatic context discovery and safety checks.

## Usage

```bash
/prd-to-prp [feature-name]
/prd-to-prp --safe  # Extra safety checks
```

## Process

### Phase 1: Gather All Documentation & Context

```bash
echo "=== 📚 Gathering Documentation ==="

# Core documents
test -f "docs/project/PROJECT_PRD.md" && echo "✓ PRD found"
test -d ".agent-os" && echo "✓ Analysis found"
test -d "docs/architecture" && echo "✓ Architecture docs found"

# Existing implementations
echo -e "\n=== 🔍 Discovering Existing Implementations ==="
```

### Phase 2: Context Discovery for Each PRP

For each potential PRP, I'll automatically:

#### 1. Search for Related Files
```javascript
function discoverPRPContext(prpName) {
  const patterns = {
    'refactor': ['**/components/**/*.tsx', '**/*.test.ts'],
    'supabase': ['**/supabase/**', '**/db/**', '**/*schema*'],
    'rudderstack': ['**/analytics/**', '**/tracking/**', '**/gtm/**'],
    'sentry': ['sentry.*.ts', '**/error**', '**/monitoring/**'],
    'bigquery': ['**/bigquery/**', '**/warehouse/**', 'docs/*BIGQUERY*'],
    'test': ['**/*.test.*', '**/*.spec.*', 'jest.config.*', 'vitest.config.*']
  };
  
  const files = findMatchingFiles(patterns[prpName]);
  return analyzeFiles(files);
}
```

#### 2. Check Working Systems
```javascript
function checkWorkingSystems(prpName) {
  const checks = {
    'supabase': [
      'grep -r "createClient" --include="*.ts"',
      'test -f "src/lib/supabase/client.ts"',
      'find . -name "*.sql" | head -5'
    ],
    'rudderstack': [
      'grep -r "rudderAnalytics.track" --include="*.ts"',
      'test -f "src/lib/analytics/rudderstack.ts"',
      'grep -r "GTM-" --include="*.tsx"'  // Check GTM overlap
    ],
    'sentry': [
      'test -f "sentry.client.config.ts"',
      'grep -r "Sentry.captureException" --include="*.ts"'
    ]
  };
  
  return runChecks(checks[prpName]);
}
```

#### 3. Verify Database Schema
```javascript
function verifyDatabaseSchema() {
  // Find schema definitions
  const schemaFiles = [
    'supabase/migrations/*.sql',
    'prisma/schema.prisma',
    'src/types/database.ts',
    'src/lib/db/schema.ts'
  ];
  
  // Extract table and field definitions
  const schema = parseSchemaFiles(schemaFiles);
  
  // Check for conflicts
  return {
    tables: schema.tables,
    fields: schema.fields,
    relationships: schema.relationships,
    warning: detectSchemaConflicts(schema)
  };
}
```

### Phase 3: Generate Context-Aware PRPs

Each PRP will include:

```markdown
# [Feature Name] PRP

## 🔍 Context Discovery Results

### Existing Implementation
\`\`\`yaml
Status:
  ${feature}: ${status}
  Files Found: ${fileCount}
  Working: ${isWorking}
  Coverage: ${coverage}%
\`\`\`

### Related Files (Review Before Modifying)
${contextFiles.map(f => `- \`${f.path}\`: ${f.description}`)}

### Current Database Schema
\`\`\`sql
-- Tables in use (DO NOT DROP)
${existingTables}
\`\`\`

### Environment Variables
\`\`\`bash
# Already configured
${existingEnvVars}

# Needed (add to .env)
${missingEnvVars}
\`\`\`

## ⚠️ Safety Warnings
${warnings.map(w => `- ⚠️ ${w}`)}

## 🎯 Requirements (from PRD)
${requirements}

## 🔧 Implementation Approach

### Preserve (DO NOT MODIFY)
${workingFeatures.map(f => `- ✅ ${f}`)}

### Extend (SAFE TO ADD)
${newFeatures.map(f => `- ➕ ${f}`)}

### Fix (BROKEN/MISSING)
${brokenFeatures.map(f => `- 🔧 ${f}`)}

## 📋 Implementation Steps

### Step 1: Verify Current State
\`\`\`bash
# Test existing functionality first
${testCommands}
\`\`\`

### Step 2: Safe Implementation
${implementationSteps}

### Step 3: Regression Testing
\`\`\`bash
# Ensure nothing broke
${regressionTests}
\`\`\`

## 🧪 Testing Strategy
${testingApproach}

## ✅ Success Criteria
${successCriteria}

## 🔗 Dependencies
- Files: ${contextFiles.map(f => f.path)}
- PRPs: ${dependentPRPs}
- External: ${externalDeps}
```

### Phase 4: Special Checks

#### Google Tag Manager vs RudderStack
```javascript
function determineTrackingStrategy() {
  const hasGTM = checkForGTM();
  const hasRudderStack = checkForRudderStack();
  const rudderDestinations = getRudderDestinations();
  
  if (hasGTM && hasRudderStack) {
    return {
      strategy: 'DUAL',
      recommendation: 'Migrate GTM events to RudderStack',
      reason: 'RudderStack can send to GTM as destination'
    };
  }
  
  if (hasRudderStack && rudderDestinations.includes('Google Analytics')) {
    return {
      strategy: 'RUDDERSTACK_ONLY',
      recommendation: 'No GTM needed',
      reason: 'RudderStack handles all tracking'
    };
  }
  
  return analyzeNeeds();
}
```

#### Supabase Table Alignment
```javascript
function checkSupabaseAlignment() {
  const localTypes = findTypeDefinitions();
  const migrations = findMigrations();
  const supabaseSchema = parseSupabaseSchema();
  
  return {
    aligned: compareSchemas(localTypes, supabaseSchema),
    conflicts: findConflicts(),
    migrations_needed: generateMigrations()
  };
}
```

### Phase 5: Output Summary

After generating PRPs:

```
📊 PRP Generation Complete

Created 7 PRPs with context:

1. debt-form-refactor-prp.md
   - Context Files: 15
   - Warnings: Component has revenue-critical logic
   - Safety: Preserves all tracking events

2. supabase-integration-prp.md  
   - Context Files: 8
   - Status: Partially implemented
   - Action: Extend, don't replace

3. rudderstack-analytics-prp.md
   - Context Files: 12
   - GTM Check: Not needed (RudderStack handles)
   - Action: Add BigQuery destination only

4. sentry-monitoring-prp.md
   - Context Files: 6
   - Status: Working, needs enhancement
   - Action: Add features, preserve existing

⚠️ IMPORTANT WARNINGS:
- Database has existing schema - migrations must be additive
- RudderStack is tracking revenue - preserve all events
- Supabase client exists - extend, don't recreate

Next: Review PRPs before converting to issues
```

## Safety Features

1. **Automatic Context Discovery** - Finds all related files
2. **Working System Detection** - Identifies what not to break
3. **Schema Verification** - Checks database alignment
4. **Dependency Mapping** - Shows interconnections
5. **GTM vs RudderStack Analysis** - Determines tracking strategy
6. **Regression Test Generation** - Ensures nothing breaks

## Usage Examples

### Standard Generation
```bash
/prd-to-prp
# Generates PRPs with basic context
```

### Safe Mode
```bash
/prd-to-prp --safe
# Extra verification, more conservative approach
```

### Single Feature
```bash
/prd-to-prp supabase-integration
# Generates one PRP with deep context
```

This ensures PRPs are always context-aware and won't break existing systems!
