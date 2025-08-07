---
name: prd-to-prp-safe
description: Convert PRD to PRPs with extensive safety checks and context discovery
aliases: [safe-prp, prp-safe]
---

# Safe PRP Generation with Context Discovery

Convert PRD to PRPs while discovering and preserving existing implementations.

## Process

### Phase 1: Discovery & Analysis

Before creating any PRP, I'll perform extensive discovery:

```bash
echo "=== 🔍 Discovering Existing Implementations ==="

# Check Supabase implementation
echo "📊 Supabase Status:"
grep -r "createClient" --include="*.ts" --include="*.tsx" 2>/dev/null | head -5
test -f "src/lib/supabase/client.ts" && echo "✓ Supabase client exists"
test -f "supabase/migrations/*.sql" && echo "✓ Migrations exist"

# Check database schema
echo "📊 Database Schema:"
find . -name "*.sql" -o -name "schema.prisma" -o -name "*schema*.ts" 2>/dev/null

# Check RudderStack implementation
echo "📊 RudderStack Status:"
test -f "src/lib/analytics/rudderstack.ts" && cat src/lib/analytics/rudderstack.ts | grep -E "(track|identify|page)" | head -5
grep -r "rudderAnalytics" --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l | xargs echo "RudderStack calls found:"

# Check Google Tag Manager
echo "📊 GTM Status:"
grep -r "GTM-" --include="*.tsx" --include="*.html" 2>/dev/null
grep -r "dataLayer" --include="*.ts" --include="*.tsx" 2>/dev/null | head -3

# Check Sentry implementation
echo "📊 Sentry Status:"
test -f "sentry.client.config.ts" && echo "✓ Client config exists"
test -f "sentry.server.config.ts" && echo "✓ Server config exists"
test -f "sentry.edge.config.ts" && echo "✓ Edge config exists"
grep -r "Sentry.captureException" --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l | xargs echo "Sentry captures found:"

# Check existing tables/fields
echo "📊 Database Fields:"
grep -r "CREATE TABLE\|ALTER TABLE" --include="*.sql" 2>/dev/null
grep -r "interface.*Lead\|type.*Lead" --include="*.ts" 2>/dev/null | head -5

# Check environment variables in use
echo "📊 Environment Variables in Use:"
grep -r "process.env.NEXT_PUBLIC_" --include="*.ts" --include="*.tsx" 2>/dev/null | cut -d: -f2 | sort -u | head -10
```

### Phase 2: Context File Discovery

For each PRP topic, I'll find related files:

```javascript
function discoverContextFiles(prpTopic) {
  const contextPatterns = {
    'supabase': [
      '**/supabase/**/*.{ts,sql}',
      '**/lib/supabase/**/*.ts',
      '**/db/**/*.{ts,sql}',
      '**/*schema*.{ts,prisma}',
      '**/migrations/*.sql'
    ],
    'rudderstack': [
      '**/analytics/**/*.ts',
      '**/lib/tracking/**/*.ts',
      '**/*track*.ts',
      '**/*analytics*.ts',
      '**/gtm/**/*.{ts,tsx}'
    ],
    'sentry': [
      'sentry.*.config.ts',
      '**/error*.{ts,tsx}',
      '**/lib/monitoring/**/*.ts',
      '**/*error-boundary*.tsx'
    ],
    'bigquery': [
      '**/bigquery/**/*.{ts,sql}',
      '**/warehouse/**/*.ts',
      '**/*pipeline*.ts',
      'docs/*BIGQUERY*.md'
    ],
    'database': [
      '**/schema*.{ts,prisma,sql}',
      '**/migrations/*.sql',
      '**/models/**/*.ts',
      '**/types/**/*.ts'
    ]
  };
  
  return findFiles(contextPatterns[prpTopic]);
}
```

### Phase 3: Working System Detection

Before modifying anything, check what's working:

```javascript
function detectWorkingSystems() {
  const working = {
    supabase: {
      client: fileExists('src/lib/supabase/client.ts'),
      auth: grepExists('supabase.auth.signIn'),
      database: grepExists('supabase.from('),
      realtime: grepExists('supabase.channel('),
      tables: findSupabaseTables(),
      migrations: countFiles('supabase/migrations/*.sql')
    },
    rudderstack: {
      initialized: grepExists('rudderAnalytics.load('),
      tracking: grepExists('rudderAnalytics.track('),
      identify: grepExists('rudderAnalytics.identify('),
      destinations: checkRudderDestinations(),
      gtmIntegration: grepExists('dataLayer.push(')
    },
    sentry: {
      configured: fileExists('sentry.client.config.ts'),
      capturing: grepExists('Sentry.captureException('),
      performance: grepExists('Sentry.startTransaction('),
      contexts: grepExists('Sentry.setContext(')
    },
    database: {
      tables: findDatabaseTables(),
      fields: findTableFields(),
      relationships: findRelationships(),
      indexes: findIndexes()
    }
  };
  
  return working;
}
```

### Phase 4: Safe PRP Generation

Each PRP will include:

```markdown
# [Feature] PRP

## ⚠️ EXISTING IMPLEMENTATION STATUS
${discoveredImplementation}

## 🔒 DO NOT MODIFY (Working Systems)
${workingSystems.map(sys => `- ✅ ${sys}: Already working, preserve as-is`)}

## 📁 CONTEXT FILES TO REVIEW
${contextFiles.map(file => `- ${file}: ${fileDescription}`)}

## 🗄️ CURRENT DATABASE SCHEMA
\`\`\`typescript
// Existing tables and fields (DO NOT CHANGE WITHOUT MIGRATION)
${currentSchema}
\`\`\`

## 🔧 SAFE IMPLEMENTATION APPROACH

### What Already Works:
${existingFeatures}

### What Needs Addition (not replacement):
${gaps}

### Migration Strategy (if needed):
${migrationSteps}

## 📋 VALIDATION BEFORE STARTING
- [ ] Review all context files listed above
- [ ] Confirm existing features still work
- [ ] Check current database schema matches
- [ ] Verify environment variables exist
- [ ] Test current implementation first

## ⚡ IMPLEMENTATION STEPS

### Step 1: Preserve Existing
\`\`\`bash
# Backup current working files
cp ${workingFiles} ${backupLocation}

# Test current functionality
npm test -- ${existingTests}
\`\`\`

### Step 2: Extend (Don't Replace)
${extensionSteps}

### Step 3: Add New Tables/Fields (if needed)
\`\`\`sql
-- Only ADD, never DROP or ALTER existing
ALTER TABLE leads ADD COLUMN IF NOT EXISTS new_field TYPE;
\`\`\`

## 🧪 REGRESSION TESTING
- [ ] All existing features still work
- [ ] No breaking changes to API
- [ ] Database migrations are additive only
- [ ] Environment variables unchanged
```

### Phase 5: Google Tag Manager Check

```javascript
function checkGTMvsRudderstack() {
  // Determine if GTM is needed or if RudderStack handles everything
  const gtmImplemented = grepExists('GTM-');
  const rudderDestinations = getRudderDestinations();
  
  if (rudderDestinations.includes('Google Analytics')) {
    return "RudderStack handles GA - no GTM needed";
  }
  
  if (gtmImplemented && !rudderDestinations.includes('Google Tag Manager')) {
    return "GTM exists - add as RudderStack destination";
  }
  
  return analyzeTrackingNeeds();
}
```

### Phase 6: Supabase Table Verification

```javascript
async function verifySupabaseTables() {
  // Check actual Supabase schema
  const localSchema = parseLocalSchema();
  const supabaseSchema = await fetchSupabaseSchema(); // If possible
  
  const comparison = {
    matching: [],
    localOnly: [],
    supabaseOnly: [],
    typeMismatches: []
  };
  
  // Compare and report
  return generateSchemaReport(comparison);
}
```

## Enhanced PRP Command

Use this safer version:

```bash
/prd-to-prp-safe

Please create SAFE PRPs that:
1. DISCOVER what already exists
2. PRESERVE working functionality  
3. EXTEND rather than replace
4. INCLUDE all context files
5. VERIFY database schemas
6. CHECK environment variables

For each system (Supabase, RudderStack, Sentry, BigQuery):
- List what's already implemented
- Identify what's actually missing
- Provide safe extension path
- Include regression tests

CRITICAL CHECKS:
- Supabase: Check existing tables/fields before creating new ones
- RudderStack: Verify if GTM is needed or if RudderStack handles it
- Sentry: Preserve existing error tracking
- Database: Only additive changes, no breaking modifications

Include these sections in each PRP:
1. "DO NOT MODIFY" - Working features to preserve
2. "CONTEXT FILES" - All related files to review
3. "CURRENT SCHEMA" - Existing database structure
4. "SAFE ADDITIONS" - Non-breaking enhancements
5. "REGRESSION TESTS" - Ensure nothing breaks
```

## Output Format

Each PRP will show:

```yaml
Status Check:
  Supabase:
    ✅ Client initialized
    ✅ Auth configured
    ⚠️ Real-time not set up
    ❌ RLS policies missing
    
  RudderStack:
    ✅ Client initialized
    ✅ Basic tracking working
    ✅ GA destination configured
    ❓ GTM needed? No - RudderStack handles it
    ❌ BigQuery destination not configured
    
  Database:
    Tables Found:
      - leads (15 fields)
      - funnels (8 fields)
      - analytics_events (12 fields)
    
Context Files:
  - src/lib/supabase/client.ts (review before modifying)
  - src/lib/analytics/rudderstack.ts (extend, don't replace)
  - supabase/migrations/001_initial.sql (current schema)
  - .env.example (required variables)
```

This ensures PRPs don't break working systems!
