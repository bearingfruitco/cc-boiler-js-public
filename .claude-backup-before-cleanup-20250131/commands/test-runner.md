# Test Runner

Intelligent test execution with context awareness.

## Arguments:
- $SCOPE: current|changed|related|all
- $TYPE: unit|integration|e2e|visual
- $WATCH: true|false

## Usage:
```bash
/test-runner current unit
/test-runner changed all
/test-runner all e2e
/tr changed  # short alias

# Non-interactive mode for CI/CD
claude --non-interactive "/test-runner all unit"
```

## Non-Interactive Mode Support

When running in non-interactive mode, outputs structured JSON:

```json
{
  "scope": "all",
  "type": "unit",
  "status": "failed",
  "summary": {
    "total": 145,
    "passed": 142,
    "failed": 3,
    "skipped": 5,
    "duration": 12.5
  },
  "failures": [
    {
      "file": "components/Button.test.tsx",
      "test": "renders with correct variant",
      "error": "Expected 'primary' but received 'secondary'"
    }
  ],
  "coverage": {
    "statements": 85.2,
    "branches": 78.5,
    "functions": 82.1,
    "lines": 85.8
  },
  "exitCode": 1
}
```

## Enhanced Implementation

!`python3 << 'EOF'
import json
import os
import sys
import subprocess
import time
from pathlib import Path
import re

# Check if running in non-interactive mode
is_non_interactive = os.environ.get('CLAUDE_NON_INTERACTIVE', 'false').lower() == 'true'

# Parse arguments
scope = """$SCOPE""".strip() or "current"
test_type = """$TYPE""".strip() or "unit"
watch = """$WATCH""".strip().lower() == "true"

def get_current_file():
    """Get the current file being worked on"""
    # In real implementation, would read from context
    context_file = Path('.claude/context/current.md')
    if context_file.exists():
        with open(context_file, 'r') as f:
            content = f.read()
            match = re.search(r'Location: ([^\s:]+)', content)
            if match:
                return match.group(1)
    
    # Fallback: most recently modified tsx/jsx file
    files = list(Path('.').glob('**/*.tsx')) + list(Path('.').glob('**/*.jsx'))
    files = [f for f in files if 'node_modules' not in str(f) and '.next' not in str(f)]
    if files:
        return str(max(files, key=lambda f: f.stat().st_mtime))
    
    return None

def find_test_file(source_file):
    """Find test file for a source file"""
    source_path = Path(source_file)
    
    # Common test file patterns
    test_patterns = [
        source_path.with_suffix('.test' + source_path.suffix),
        source_path.with_suffix('.spec' + source_path.suffix),
        Path('__tests__') / source_path.name,
        Path('tests') / source_path.name,
        source_path.parent / '__tests__' / source_path.name,
        source_path.parent / 'tests' / source_path.name
    ]
    
    for pattern in test_patterns:
        if pattern.exists():
            return str(pattern)
    
    return None

def get_changed_files():
    """Get list of changed files from git"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            files = result.stdout.strip().split('\n')
            return [f for f in files if f.endswith(('.tsx', '.jsx', '.ts', '.js'))]
    except:
        pass
    
    return []

def run_tests(test_command, description):
    """Run test command and parse results"""
    start_time = time.time()
    
    try:
        result = subprocess.run(
            test_command,
            shell=True,
            capture_output=True,
            text=True
        )
        
        duration = time.time() - start_time
        
        # Parse test results (simplified - real implementation would parse actual output)
        output = result.stdout + result.stderr
        
        # Extract test counts
        total_match = re.search(r'(\d+) total', output)
        passed_match = re.search(r'(\d+) passed', output)
        failed_match = re.search(r'(\d+) failed', output)
        skipped_match = re.search(r'(\d+) skipped', output)
        
        total = int(total_match.group(1)) if total_match else 0
        passed = int(passed_match.group(1)) if passed_match else 0
        failed = int(failed_match.group(1)) if failed_match else 0
        skipped = int(skipped_match.group(1)) if skipped_match else 0
        
        # Extract failures
        failures = []
        if failed > 0:
            # Simplified failure parsing
            failure_matches = re.findall(r'FAIL\s+([^\s]+)\s+(.+)', output)
            for file, test in failure_matches[:3]:  # First 3 failures
                failures.append({
                    "file": file,
                    "test": test,
                    "error": "Test failed"  # Would extract actual error
                })
        
        # Extract coverage if available
        coverage = {}
        coverage_match = re.search(
            r'Statements\s*:\s*([\d.]+)%.*Branches\s*:\s*([\d.]+)%.*Functions\s*:\s*([\d.]+)%.*Lines\s*:\s*([\d.]+)%',
            output,
            re.DOTALL
        )
        if coverage_match:
            coverage = {
                "statements": float(coverage_match.group(1)),
                "branches": float(coverage_match.group(2)),
                "functions": float(coverage_match.group(3)),
                "lines": float(coverage_match.group(4))
            }
        
        return {
            "success": result.returncode == 0,
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "duration": round(duration, 2),
            "failures": failures,
            "coverage": coverage,
            "output": output if not is_non_interactive else ""
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "duration": 0,
            "failures": [],
            "coverage": {}
        }

def build_test_command(scope, test_type, files=None):
    """Build the appropriate test command"""
    base_cmd = "pnpm test"
    
    # Add test type flags
    if test_type == "unit":
        base_cmd += " --testPathPattern='\\.test\\.(tsx?|jsx?)$'"
    elif test_type == "integration":
        base_cmd += " --testPathPattern='\\.integration\\.(tsx?|jsx?)$'"
    elif test_type == "e2e":
        return "pnpm test:e2e"
    elif test_type == "visual":
        return "pnpm test:visual"
    
    # Add scope
    if scope == "current" and files:
        base_cmd += f" {' '.join(files)}"
    elif scope == "changed" and files:
        base_cmd += f" --findRelatedTests {' '.join(files)}"
    elif scope == "related" and files:
        base_cmd += f" --findRelatedTests {' '.join(files)}"
    
    # Add watch mode if needed
    if watch and not is_non_interactive:
        base_cmd += " --watch"
    
    # Add coverage for non-interactive mode
    if is_non_interactive:
        base_cmd += " --coverage --coverageReporters=text"
    
    return base_cmd

def main():
    files_to_test = []
    
    # Determine which files to test based on scope
    if scope == "current":
        current_file = get_current_file()
        if current_file:
            test_file = find_test_file(current_file)
            if test_file:
                files_to_test = [test_file]
            else:
                # Test the source file itself with --findRelatedTests
                files_to_test = [current_file]
                scope = "related"
        else:
            if not is_non_interactive:
                print("❌ No current file detected")
                sys.exit(1)
    
    elif scope == "changed":
        changed_files = get_changed_files()
        if changed_files:
            # Find test files for changed files
            for file in changed_files:
                test_file = find_test_file(file)
                if test_file:
                    files_to_test.append(test_file)
                else:
                    files_to_test.append(file)
        else:
            if not is_non_interactive:
                print("ℹ️  No changed files detected, running all tests")
            scope = "all"
    
    # Build and run test command
    test_command = build_test_command(scope, test_type, files_to_test)
    
    if not is_non_interactive:
        print(f"🧪 Running {test_type} tests ({scope} scope)")
        print(f"📍 Command: {test_command}\n")
    
    # Run tests
    results = run_tests(test_command, f"{test_type} tests")
    
    # Format output
    if is_non_interactive:
        output = {
            "scope": scope,
            "type": test_type,
            "status": "passed" if results["success"] else "failed",
            "summary": {
                "total": results["total"],
                "passed": results["passed"],
                "failed": results["failed"],
                "skipped": results["skipped"],
                "duration": results["duration"]
            },
            "failures": results["failures"],
            "coverage": results["coverage"],
            "exitCode": 0 if results["success"] else 1
        }
        
        print(json.dumps(output, indent=2))
        sys.exit(output["exitCode"])
    else:
        # Interactive output
        if results.get("error"):
            print(f"❌ Error running tests: {results['error']}")
            sys.exit(1)
        
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS")
        print("=" * 50)
        
        # Summary
        status_icon = "✅" if results["success"] else "❌"
        print(f"{status_icon} Status: {'PASSED' if results['success'] else 'FAILED'}")
        print(f"⏱️  Duration: {results['duration']}s")
        print(f"\n📈 Summary:")
        print(f"  Total: {results['total']}")
        print(f"  ✅ Passed: {results['passed']}")
        if results['failed'] > 0:
            print(f"  ❌ Failed: {results['failed']}")
        if results['skipped'] > 0:
            print(f"  ⏭️  Skipped: {results['skipped']}")
        
        # Failures
        if results['failures']:
            print("\n❌ Failures:")
            for failure in results['failures']:
                print(f"\n  File: {failure['file']}")
                print(f"  Test: {failure['test']}")
                print(f"  Error: {failure['error']}")
        
        # Coverage
        if results['coverage']:
            print("\n📊 Coverage:")
            print(f"  Statements: {results['coverage']['statements']}%")
            print(f"  Branches: {results['coverage']['branches']}%")
            print(f"  Functions: {results['coverage']['functions']}%")
            print(f"  Lines: {results['coverage']['lines']}%")
        
        # Next steps
        if not results["success"]:
            print("\n💡 Next steps:")
            print("  - Fix failing tests")
            print("  - Run: /tr current --watch")
            print("  - Check: /bt add 'Test failures'")

if __name__ == "__main__":
    main()
EOF`

## Why This Command:
- Run only relevant tests
- Track test coverage per feature
- Integrate with TODO system
- Maintain test context

## Steps:

### Scope: CURRENT
Test only current file/feature:

```bash
# Detect current file
CURRENT_FILE=$(grep "Location:" .claude/context/current.md | \
  head -1 | cut -d' ' -f2 | cut -d':' -f1)

# Find related test
TEST_FILE=$(echo $CURRENT_FILE | \
  sed 's/\.tsx$/.test.tsx/' | \
  sed 's|components/|__tests__/components/|')

# Run test
if [ -f "$TEST_FILE" ]; then
  npm test -- $TEST_FILE
else
  echo "❌ No test found for $CURRENT_FILE"
  echo "Create: $TEST_FILE"
  
  # Generate test template
  /create-component test ${CURRENT_FILE}
fi
```

### Scope: CHANGED
Test all modified files:

```bash
# Get changed files
CHANGED=$(git diff --name-only HEAD | grep -E '\.(tsx?|jsx?)$')

# Find their tests
for FILE in $CHANGED; do
  TEST_FILE=$(find-test $FILE)
  npm test -- $TEST_FILE
done
```

### Scope: RELATED
Test current component and all that use it:

```bash
# Get current component
COMPONENT=$(basename $CURRENT_FILE .tsx)

# Find all files using it
RELATED=$(grep -r "import.*$COMPONENT" --include="*.tsx" . | \
  cut -d: -f1 | sort -u)

# Run their tests
npm test -- --findRelatedTests $RELATED
```

### Scope: ALL
Run entire test suite:

```bash
npm test -- --coverage
```

## Type Options:

### UNIT Tests
```bash
npm test -- --testPathPattern='\.test\.(tsx?|jsx?)$'
```

### INTEGRATION Tests
```bash
npm test -- --testPathPattern='\.integration\.(tsx?|jsx?)$'
```

### E2E Tests
```bash
npm run test:e2e
```

### VISUAL Tests
```bash
npm run test:visual
```

## Watch Mode:

Continuous testing during development:

```bash
# Watch current file
/test-runner current unit --watch

# Watch changed files
/test-runner changed all --watch
```

## Integration:

### With TODO System
```typescript
// Marks TODO when test fails
interface TestResult {
  file: string;
  status: 'pass' | 'fail';
  todos: string[];
}

// Updates .task-ledger.md
if (testResult.status === 'fail') {
  addTodo(`Fix test: ${testResult.file}`);
}
```

### With Context System
```bash
# Saves test results to context
echo "Last test run: $SCOPE $TYPE" >> .claude/context/test-history.md
echo "Coverage: $COVERAGE%" >> .claude/context/test-history.md
```

## Output Format:

```
🧪 Running unit tests (changed scope)

✅ components/Button.test.tsx (5/5)
✅ components/Card.test.tsx (3/3)
❌ components/Modal.test.tsx (2/3)
   ↳ ❌ should close on escape key

📊 Coverage Summary:
   Statements: 85.2%
   Branches: 78.5%
   Functions: 82.1%
   Lines: 85.8%

💡 Next steps:
   - Fix failing test in Modal.test.tsx
   - Coverage below 80% in: utils/validation.ts
```

## CI/CD Integration:

### GitHub Actions
```yaml
- name: Run Unit Tests
  env:
    CLAUDE_NON_INTERACTIVE: true
  run: |
    claude --non-interactive "/test-runner all unit"
    
- name: Run Integration Tests
  env:
    CLAUDE_NON_INTERACTIVE: true
  run: |
    claude --non-interactive "/test-runner all integration"
    
- name: Check Coverage
  run: |
    COVERAGE=$(claude --non-interactive "/test-runner all unit" | jq -r '.coverage.statements')
    if (( $(echo "$COVERAGE < 80" | bc -l) )); then
      echo "Coverage too low: $COVERAGE%"
      exit 1
    fi
```

### Pre-commit Hook
```bash
# Run tests for changed files
claude --non-interactive "/test-runner changed unit"
```

## Benefits:
- Focused testing saves time
- Automatic test discovery
- Coverage tracking
- TODO integration
- Watch mode for TDD
- CI/CD ready