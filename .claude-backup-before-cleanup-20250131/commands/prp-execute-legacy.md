# Execute PRP Validation Loops

Run the validation loops defined in a PRP to ensure implementation readiness.

## Arguments: $ARGUMENTS

Expects: PRP name or path (e.g., "user-auth" or "PRPs/user-auth.md")

## What This Does:

Executes all validation loops defined in a PRP to ensure:
- Code quality standards are met
- Design system compliance
- Tests are passing
- Performance benchmarks achieved
- Production readiness confirmed

## Process:

1. **Load PRP**
   - Find and parse the specified PRP
   - Extract validation loops
   - Check for pinned requirements

2. **Pre-Flight Checks**
   - Verify requirements compliance if pinned
   - Check current stage with `/sv check`
   - Ensure environment is ready

3. **Execute Validation Loops**
   
   ### Level 1: Syntax & Standards
   ```bash
   bun run lint:fix
   bun run typecheck
   /vd
   /validate-async
   ```
   
   ### Level 2: Component Testing
   ```bash
   bun run test [component]
   bun run test:components
   ```
   
   ### Level 3: Integration Testing
   ```bash
   bun run test:e2e [feature]
   bun run test:api
   ```
   
   ### Level 4: Production Readiness
   ```bash
   bun run lighthouse
   bun run analyze
   /grade --requirements
   ```

4. **Report Results**
   - Show pass/fail for each level
   - Highlight what needs fixing
   - Suggest remediation commands

## Execution Modes:

### Standard Mode (Default)
- Runs all validations
- Stops on first failure
- Shows detailed error output

### Interactive Mode
```bash
/prp-execute user-auth --interactive
```
- Prompts to continue after failures
- Offers to run auto-fixes
- Allows skipping certain validations

### Fix Mode
```bash
/prp-execute user-auth --fix
```
- Automatically runs fixable commands
- Re-runs validation after fixes
- Reports what was fixed

### CI Mode
```bash
/prp-execute user-auth --ci
```
- Outputs JSON format
- Non-interactive
- Returns proper exit codes

## Integration with Your System:

- **Design Validation**: Uses your `/vd` command
- **Async Checks**: Runs `/validate-async`
- **Stage Gates**: Respects `/sv` requirements
- **Grading**: Includes `/grade` scores
- **Bug Tracking**: Checks known bugs with `/bt`

## Example Output:

```
PRP Validation: user-auth
========================

✅ Level 1: Syntax & Standards
  ✓ bun run lint:fix (312ms)
  ✓ bun run typecheck (1847ms)
  ✓ /vd (89ms)
  ✓ /validate-async (156ms)

✅ Level 2: Component Testing
  ✓ bun run test auth (2341ms)
  ✓ bun run test:components (1823ms)

❌ Level 3: Integration Testing
  ✓ bun run test:api auth (3421ms)
  ✗ bun run test:e2e auth (5123ms)
    Error: Timeout waiting for selector

Cannot proceed to: Production deployment

💡 Fix suggestion:
- Check loading states in auth flow
- Run: /btf auth-login
```

## Options:

- `--level [1-4]` - Run specific level only
- `--skip [names]` - Skip specific validations
- `--fix` - Attempt auto-fixes
- `--interactive` - Interactive mode
- `--json` - JSON output
- `--verbose` - Show all output

## Common Patterns:

### During Development
```bash
# Quick quality check
/prp-execute feature --level 1

# Before committing
/prp-execute feature --level 1,2
```

### Before PR
```bash
# Full validation
/prp-execute feature

# With fixes
/prp-execute feature --fix
```

### CI Integration
```bash
# In GitHub Actions
/prp-execute feature --ci > results.json
```

## Troubleshooting:

### "PRP not found"
- Check PRP exists in `PRPs/` directory
- Try full path: `PRPs/feature.md`

### "Validation keeps failing"
- Run with `--verbose` for details
- Check `/bt list` for known issues
- Try `--fix` mode

### "Takes too long"
- Use `--level` to run specific levels
- Skip slow tests with `--skip e2e`

## Best Practices:

1. **Run Level 1 continuously** during development
2. **Run Level 2 after** each component completion
3. **Run Level 3 before** integration work
4. **Run Level 4 before** creating PR

## Related Commands:

- `/create-prp` - Create a new PRP
- `/prp-validate` - Validate PRP structure
- `/prd-tests` - Generate tests from PRD
- `/grade` - Check implementation quality

The goal is to catch issues early and ensure production-ready code!