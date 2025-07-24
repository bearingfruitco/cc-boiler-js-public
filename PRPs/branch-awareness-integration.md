# PRP Integration for Branch Awareness

Integrates branch and feature awareness into the PRP workflow.

## Integration Points

### 1. PRP Creation Enhancement

When creating a PRP, check for related completed features:

```typescript
// In /create-prp command enhancement
async function createPRPWithAwareness(featureName: string) {
  // Check if enhancing existing feature
  const existingFeature = await checkExistingFeature(featureName);
  
  if (existingFeature && existingFeature.status === 'completed') {
    // Add to PRP context
    const prpContext = {
      enhancing_feature: existingFeature.name,
      existing_implementation: existingFeature.working_implementation,
      preserve_functionality: existingFeature.key_functions,
      protected_files: existingFeature.files
    };
    
    // Include in PRP template
    return generatePRPWithContext(featureName, prpContext);
  }
  
  // Standard PRP creation
  return generateStandardPRP(featureName);
}
```

### 2. PRP Validation Enhancement

Add branch awareness to validation loops:

```yaml
# In PRP validation level 1 (syntax & standards)
validation_checks:
  - existing: lint, typecheck, design
  - NEW: feature_preservation_check
  
feature_preservation_check:
  - Verify no protected functionality removed
  - Ensure enhancement builds on existing
  - Check branch is appropriate for changes
```

### 3. PRP Execution Integration

```bash
# Enhanced /prp-execute
/prp-execute auth-enhancement --level 4

# Additional checks at each level:
Level 1: Check not breaking existing auth
Level 2: Verify auth tests still pass
Level 3: Ensure integration with existing auth works
Level 4: Validate performance not degraded
```

### 4. AI Documentation Enhancement

Update AI docs to include feature state:

```markdown
# In PRPs/ai_docs/[feature].md

## Existing Implementation Context
- Current status: Completed
- Key functions: login, logout, validateToken
- Test coverage: 92%
- Performance baseline: <100ms validation

## Enhancement Guidelines
- Preserve all existing functionality
- Build on current implementation
- Maintain backward compatibility
- Don't recreate working parts
```

## Command Integration

### Enhanced PRP Commands

```bash
# Check before creating PRP
/feature-status auth
> Shows existing implementation

# Create enhancement PRP
/create-prp auth-mfa
> Automatically includes existing auth context
> Marks as enhancement, not new feature

# Execute with preservation checks
/prp-execute auth-mfa
> Validates against existing implementation
> Ensures no regression
```

## State Integration

PRP state includes feature awareness:

```json
// In .claude/state/active-prp.json
{
  "name": "auth-mfa",
  "type": "enhancement",
  "enhancing_feature": "user-authentication",
  "protected_files": [
    "components/auth/LoginForm.tsx",
    "lib/auth/jwt.ts"
  ],
  "preservation_requirements": [
    "Maintain JWT token structure",
    "Keep existing login flow",
    "Preserve session management"
  ]
}
```

## Workflow Benefits

1. **Context Preservation** - PRP knows what exists
2. **Protection Integration** - Validation ensures no regression
3. **Clear Enhancement Path** - Builds on working code
4. **Automated Checks** - Each level validates preservation

This integrates branch/feature awareness directly into your PRP methodology without disrupting the flow.
