# Enhanced Workflow Examples - v2.4.0

## 🎯 Smart Issue Creation from Claude's Analysis

### Scenario: Claude provides implementation plan
```bash
Claude: "Here's how we'll implement the caching system:
1. Add Redis connection to database config
2. Create cache provider with TTL support
3. Implement cache invalidation hooks
4. Add monitoring for cache hit rates"

# Capture this plan to an issue
/capture-to-issue "Implement caching system"

# System responds:
🔍 Analyzing existing issues...

Found related issues:
- #34: "Add caching layer" (75% match)
  Status: Open, Assigned: @teammate
  
Options:
1. Add your plan as comment to #34
2. Create sub-task under #34
3. Create new independent issue

Choose: 2

✅ Created issue #47 "Implement Redis caching"
🔗 Linked to parent #34
📦 Tracking components: CacheProvider, useCache
```

## 🛡️ Preventing Duplicate Work

### Scenario: About to create a component that exists
```bash
# Traditional approach (might create duplicate)
/cc ui Button

# With v2.4.0 (automatic check)
⚠️ Button Already Exists!

📍 Found at: components/ui/Button.tsx
📅 Created: 2024-01-10
📝 Last modified: 2 hours ago by @teammate
📦 Exports: Button (default), ButtonProps

📊 Used in 4 places:
  • components/auth/AuthForm.tsx
  • components/profile/ProfileForm.tsx
  • app/settings/page.tsx

Options:
1. Update existing component (recommended)
2. Create with different name
3. Override (requires confirmation)

To update existing:
  • Open: components/ui/Button.tsx
```

## 📦 Dependency Management in Action

### Scenario: Modifying a shared component
```bash
# Editing Button.tsx that's used by multiple components
[Making changes to Button component...]

# Hook alerts automatically:
📦 Dependency Alert: Button

This component is used by 4 other components:
  • AuthForm
  • ProfileForm
  • SettingsPage
  • ContactForm

Quick Actions:
  • /deps check Button - See full dependency tree
  • /deps breaking Button - Check for breaking changes
  • Continue with caution

# Check for breaking changes
/deps breaking Button

⚠️ Breaking change detected!
Removed prop: 'size'
Used in: AuthForm (line 23), ProfileForm (line 45)

Run: /deps update Button --fix
```

## 🔄 Complete Feature Workflow with Smart Tracking

```bash
# 1. Start feature from issue
/fw start 23

# 2. Claude provides analysis
Claude: "Authentication requires JWT tokens with refresh..."

# 3. Capture analysis to sub-issue
/cti "JWT implementation details"
> Creating sub-issue under #23...

# 4. Create components (with auto-check)
/cc auth LoginForm
> ✅ LoginForm doesn't exist - creating...

# 5. Work on shared component
[editing Button.tsx]
> 📦 Button is used by 3 components...

# 6. Check dependencies before PR
/deps scan
> Updated 5 @used-by comments
> No circular dependencies found

# 7. Complete feature
/fw complete 23
> Creating PR with:
> - Linked issues: #23, #48 (JWT details)
> - Modified components: LoginForm (new), Button (updated)
> - Dependency impacts: 3 components affected
```

## 🎯 Capturing Different Types of Claude Responses

### Implementation Plans
```bash
Claude: "Implementation Plan:
1. Set up database schema
2. Create API endpoints
3. Build UI components"

/cti "Feature implementation plan" --section "Implementation Plan"
```

### Bug Analysis
```bash
Claude: "Root cause analysis shows the issue is..."

/cti "Memory leak investigation" --section "Root cause"
> Links to bug #bug_1234
```

### Architecture Decisions
```bash
Claude: "Recommended architecture:
- Microservices for scalability
- Event-driven communication
- Redis for caching"

/cti "Architecture decision: Microservices"
> Creates ADR and links to PROJECT_PRD.md
```

## 🔍 Smart Dependency Scanning

### Initial Setup
```bash
# Add dependency tracking to existing project
/deps scan

Scanning 47 components...
✅ Added @used-by comments to 23 components
✅ Added @depends-on to 15 components
⚠️ Found 3 potential circular dependencies

Review: .claude/dependencies/manifest.json
```

### Regular Maintenance
```bash
# Weekly dependency check
/deps check --all

Component Health Report:
- Total components: 47
- With dependents: 23
- Highly coupled (>5 deps): 3
- Circular dependencies: 0

Suggestions:
- Button is used by 12 components (consider variants)
- AuthContext has circular dependency with AuthProvider
```

## 💡 Best Practices

### 1. Always Check Before Creating
```bash
# Before any new component/function
/exists MyNewComponent
# Or just try to create - hooks will check automatically
```

### 2. Capture Important Analyses
```bash
# After Claude provides insights
/cti "Performance optimization plan"
# Links to current context automatically
```

### 3. Track Dependencies Early
```bash
# When creating new components
/**
 * @component NewFeature
 * @depends-on Button, useAuth
 * @used-by (none yet)
 */
```

### 4. Review Before Major Changes
```bash
# Before refactoring
/deps check ComponentName
# See impact before proceeding
```

## 🚀 Advanced Workflows

### Multi-Component Update
```bash
# Update all components using old Button API
/deps update Button --migrate-prop size="medium" to variant="primary"

Updating 4 components:
✅ AuthForm - Updated line 23
✅ ProfileForm - Updated line 45
⚠️ SettingsPage - Manual review needed (custom logic)
✅ ContactForm - Updated line 67
```

### Issue Relationship Management
```bash
# Create related issues with smart linking
/cti "Frontend implementation"
> Found parent issue #23 from branch name
> Linking as sub-task...

/cti "Backend API changes"
> Detecting related PRD: user-auth-PRD.md
> Cross-referencing with #23...
```

## 🎯 Result: Zero Duplicate Work

With these enhancements:
- ✅ No more recreating existing components
- ✅ No more duplicate issues
- ✅ Automatic dependency tracking
- ✅ Smart context preservation
- ✅ Clear component relationships
- ✅ Captured analyses become actionable issues

The system now prevents common workflow problems automatically!
