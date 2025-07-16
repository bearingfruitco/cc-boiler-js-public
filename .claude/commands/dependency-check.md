# Dependency Tracking Commands

Track component dependencies using simple @used-by comments.

## Arguments:
- $ACTION: check|scan|update|breaking
- $COMPONENT: Component name to check

## Actions:

### CHECK - See what uses a component
```bash
/deps check Button
/deps check useAuth
```

Shows:
```
📦 Dependency Check: Button

Used by (3 components):
  ✓ AuthForm (components/auth/AuthForm.tsx)
  ✓ ProfileForm (components/profile/ProfileForm.tsx) 
  ✓ SettingsPage (app/settings/page.tsx)

Last modified: 2 hours ago
Breaking changes: None detected

Quick actions:
  • /deps update Button - Update all imports
  • /deps breaking Button - Check for breaking changes
```

### SCAN - Update all @used-by comments
```bash
/deps scan
```

Scans entire codebase and updates dependency comments:
```typescript
/**
 * @component Button
 * @used-by AuthForm, ProfileForm, SettingsPage
 * @depends-on Icon, cn
 * @last-scan 2024-01-16
 */
```

### UPDATE - Update all components using a dependency
```bash
/deps update Button
```

Updates:
1. Import statements
2. Props if interface changed
3. Re-runs type checking

### BREAKING - Check if changes break dependents
```bash
/deps breaking Button
```

Analyzes:
- Removed props
- Changed prop types  
- Renamed exports
- Breaking behavior changes

## Comment Format:

Add to component files:
```typescript
/**
 * @component ComponentName
 * @used-by Component1, Component2, Component3
 * @depends-on Dependency1, Dependency2
 * @last-scan 2024-01-16
 */
```

## How It Works:

### 1. Lightweight Tracking
- No complex manifest files
- Comments live with code
- Git tracks changes naturally

### 2. Smart Detection
```typescript
// When you modify Button.tsx
function detectDependents(file) {
  // 1. Read @used-by comment
  const usedBy = parseUsedByComment(file);
  
  // 2. Verify with actual imports
  const actualUsers = findImports('Button');
  
  // 3. Alert if mismatch
  if (difference(usedBy, actualUsers)) {
    suggest('/deps scan');
  }
}
```

### 3. Integration with Hooks
Pre-commit hook alerts when modifying components with dependents:
```
⚠️  Button.tsx is used by 3 components
Run: /deps check Button
```

## Examples:

### Before Making Changes:
```bash
# About to modify Button
/deps check Button
> Used by: AuthForm, ProfileForm, SettingsPage
> Safe to modify: Yes (no breaking changes detected)
```

### After Making Changes:
```bash
# Changed Button props
/deps breaking Button
> ⚠️  Breaking change detected!
> Removed prop: 'size'
> Used in: AuthForm (line 23), ProfileForm (line 45)
> 
> Run: /deps update Button --fix
```

### Regular Maintenance:
```bash
# Weekly scan
/deps scan
> Scanning 47 components...
> Updated 12 @used-by comments
> Found 3 missing dependencies
> Run: /deps check --missing
```

## Configuration:

In `.claude/config.json`:
```json
{
  "dependencies": {
    "auto_scan": true,
    "scan_on_commit": true,
    "track_hooks": true,
    "track_utils": true,
    "alert_threshold": 3
  }
}
```

## Smart Features:

### Circular Dependency Detection:
```bash
/deps check --circular
> ⚠️  Circular dependency found:
> AuthForm → useAuth → AuthContext → AuthForm
```

### Missing Dependency Detection:
```bash
/deps scan --missing
> Missing @depends-on:
> • Button uses Icon but doesn't declare it
> • AuthForm uses z from zod but doesn't declare it
```

### Visual Output (Optional):
```bash
/deps check Button --visual

Button
  ├── used by:
  │   ├── AuthForm
  │   ├── ProfileForm  
  │   └── SettingsPage
  └── depends on:
      ├── Icon
      └── cn (utils)
```

## Best Practices:

1. **Run scan weekly**: `/deps scan`
2. **Check before refactoring**: `/deps check Component`
3. **Update after changes**: `/deps update Component`
4. **Add to PR checklist**: "Ran /deps check on modified components"

## Minimal Overhead:

- Just comments in code
- No runtime cost
- No complex graphs
- Git-friendly tracking
- Clear, actionable alerts
