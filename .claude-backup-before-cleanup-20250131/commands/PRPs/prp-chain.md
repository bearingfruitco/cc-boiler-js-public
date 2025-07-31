# Chain PRPs Together

Link multiple PRPs for complex features with dependencies.

## Usage
```bash
/prp-chain auth-prp.md → profile-prp.md → settings-prp.md
```

## Arguments: $ARGUMENTS

## What It Does

1. **Validates Dependency Order**
   - Ensures PRPs are in correct sequence
   - Checks that dependencies are satisfied
   - Prevents circular dependencies

2. **Checks Completion Status**
   - Verifies previous PRPs are complete
   - Validates success metrics
   - Ensures handoff points are documented

3. **Passes Outputs Between PRPs**
   - Extracts outputs from completed PRPs
   - Injects as inputs to next PRP
   - Maintains context throughout chain

4. **Tracks Overall Progress**
   - Shows visual progress indicator
   - Logs time per PRP
   - Calculates total chain metrics

## Process

1. Parse the chain specification
2. Load each PRP and validate structure
3. Check dependency graph
4. For each PRP in sequence:
   - Verify prerequisites met
   - Extract outputs from previous
   - Update inputs for current
   - Track execution metrics
5. Generate chain summary report

## Example Chain Definition

```yaml
chain:
  name: "User Management System"
  prps:
    - id: auth-prp
      outputs: [user_session, jwt_token]
    - id: profile-prp
      inputs: [user_session]
      outputs: [profile_data]
    - id: settings-prp
      inputs: [user_session, profile_data]
      outputs: [preferences]
```

## Handoff Points

Each PRP must declare its inputs/outputs:

```markdown
## Inputs
- user_session: Session object from auth-prp
- profile_data: User profile from profile-prp

## Outputs
- preferences: User preference object
- theme_settings: UI theme configuration
```

## Validation

Before chaining:
- All PRPs must exist
- Dependencies must be valid
- No circular references
- Handoff points documented

## Example Output

```
🔗 PRP Chain: User Management System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[✓] auth-prp.md
    └─> Outputs: user_session, jwt_token
    
[→] profile-prp.md (current)
    └─> Inputs: user_session ✓
    └─> Progress: 45%
    
[ ] settings-prp.md
    └─> Waiting for: profile_data

Overall Progress: ████████░░░░░░░░ 33%
Time Elapsed: 1h 23m
```

## Tips

1. Keep chains focused (3-5 PRPs max)
2. Document handoff points clearly
3. Test outputs before chaining
4. Use for related features only
5. Review chain before starting
