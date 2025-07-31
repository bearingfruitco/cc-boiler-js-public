# Non-Interactive Mode Guide

Claude Code supports non-interactive execution for automation, CI/CD pipelines, and scripting.

## Overview

Non-interactive mode enables:
- **Automated execution**: No prompts or confirmations
- **Structured output**: JSON format for parsing
- **Exit codes**: Standard codes for success/failure
- **CI/CD integration**: Works in any pipeline
- **Scripting**: Chain commands programmatically

## Basic Usage

### Command Line
```bash
# Run any command non-interactively
claude --non-interactive "/validate-design all"
claude --non-interactive "/stage-validate check 1"
claude --non-interactive "/security-check all"
```

### Environment Variable
```bash
# Set for entire session
export CLAUDE_NON_INTERACTIVE=true
claude "/validate-design all"
```

## Supported Commands

### Validation Commands
| Command | Alias | Description | Exit Codes |
|---------|-------|-------------|------------|
| `/validate-design` | `/vd` | Design system compliance | 0=pass, 1=violations |
| `/stage-validate` | `/sv` | Stage gate validation | 0=complete, 1=incomplete |
| `/prp-execute` | - | PRP validation loops | 0=pass, 1=fail |
| `/security-check` | `/sc` | Security validation | 0=secure, 1=issues |
| `/deps scan` | - | Dependency scanning | 0=clean, 1=vulnerabilities |
| `/test-runner` | `/tr` | Test execution | 0=pass, 1=fail |
| `/validate-async` | - | Async pattern validation | 0=valid, 1=issues |
| `/grade` | - | Implementation grading | 0=pass (>80%), 1=fail |

### Status Commands
| Command | Description | Always Returns |
|---------|-------------|----------------|
| `/work-status` | Project status overview | 0 (informational) |
| `/branch-status` | Branch health info | 0 (informational) |
| `/feature-status` | Feature tracking | 0 (informational) |
| `/agent-health` | Agent system status | 0 (informational) |
| `/chain status` | Chain execution status | 0 (informational) |

## Output Format

All commands return consistent JSON:

### Success Response
```json
{
  "success": true,
  "timestamp": "2025-01-30T12:34:56Z",
  "command": "/validate-design",
  "scope": "all",
  "results": {
    "totalViolations": 0,
    "filesChecked": 42,
    "duration_ms": 1234
  },
  "exitCode": 0
}
```

### Failure Response
```json
{
  "success": false,
  "timestamp": "2025-01-30T12:34:56Z",
  "command": "/security-check",
  "results": {
    "vulnerabilities": 3,
    "critical": 1,
    "high": 2,
    "details": [...]
  },
  "exitCode": 1
}
```

### Error Response
```json
{
  "success": false,
  "timestamp": "2025-01-30T12:34:56Z",
  "error": "Configuration file not found",
  "stack": "Error: ENOENT: no such file or directory...",
  "exitCode": 2
}
```

## Exit Codes

Standard exit codes across all commands:

| Code | Meaning | Example |
|------|---------|---------|
| 0 | Success | All checks passed |
| 1 | Validation failure | Violations or issues found |
| 2 | Configuration error | Missing required files |
| 3 | Tool error | API connection failed |
| 4 | Multiple failures | Several checks failed |

## Command Examples

### Design Validation
```bash
# Check all files
claude --non-interactive "/vd all"

# Parse results
claude --non-interactive "/vd all" | jq '.results.totalViolations'

# Use in conditional
if claude --non-interactive "/vd all"; then
  echo "Design compliant"
else
  echo "Design violations found"
fi
```

### Stage Validation
```bash
# Check current stage
claude --non-interactive "/sv check current"

# Check specific stage
claude --non-interactive "/sv check 2"

# Get progress percentage
claude --non-interactive "/sv status" | jq '.stages[0].progress'
```

### Security Check
```bash
# Full security audit
claude --non-interactive "/sc all"

# Critical only
claude --non-interactive "/sc critical"

# Parse vulnerability count
VULNS=$(claude --non-interactive "/sc all" | jq '.results.vulnerabilities')
```

### Test Execution
```bash
# Run all tests
claude --non-interactive "/tr all"

# Run changed files only
claude --non-interactive "/tr changed"

# Unit tests only
claude --non-interactive "/tr unit"
```

### PRP Validation
```bash
# Validate active PRP at level 1
claude --non-interactive "/prp-execute --level 1"

# Specific PRP
claude --non-interactive "/prp-execute user-auth --level 2"

# With auto-fix
claude --non-interactive "/prp-execute --level 1 --fix"
```

## Scripting Examples

### Bash Script
```bash
#!/usr/bin/env bash
# validate-all.sh

set -e  # Exit on first failure

echo "Running quality gates..."

# Design validation
echo -n "Design system: "
if claude --non-interactive "/vd all" > design.json; then
  echo "✓"
else
  echo "✗ ($(jq -r '.results.totalViolations' design.json) violations)"
  exit 1
fi

# Security check
echo -n "Security: "
if claude --non-interactive "/sc all" > security.json; then
  echo "✓"
else
  echo "✗ ($(jq -r '.results.vulnerabilities' security.json) issues)"
  exit 1
fi

# Tests
echo -n "Tests: "
if claude --non-interactive "/tr all" > tests.json; then
  echo "✓"
else
  echo "✗"
  exit 1
fi

echo "All quality gates passed!"
```

### Node.js Script
```javascript
#!/usr/bin/env node
// validate.js

const { execSync } = require('child_process');

async function runValidation(command) {
  try {
    const output = execSync(
      `claude --non-interactive "${command}"`,
      { encoding: 'utf8' }
    );
    return JSON.parse(output);
  } catch (error) {
    // Command failed, parse output from stderr
    const output = error.stdout || error.toString();
    try {
      return JSON.parse(output);
    } catch {
      throw error;
    }
  }
}

async function main() {
  console.log('Running validations...\n');
  
  // Design validation
  const design = await runValidation('/vd all');
  console.log(`Design: ${design.success ? '✓' : '✗'}`);
  if (!design.success) {
    console.log(`  Violations: ${design.results.totalViolations}`);
  }
  
  // Stage validation
  const stage = await runValidation('/sv check current');
  console.log(`Stage: ${stage.results.progress}% complete`);
  
  // Security
  const security = await runValidation('/sc all');
  console.log(`Security: ${security.success ? '✓' : '✗'}`);
  
  // Overall result
  const allPassed = design.success && security.success;
  process.exit(allPassed ? 0 : 1);
}

main().catch(console.error);
```

### Python Script
```python
#!/usr/bin/env python3
# validate.py

import subprocess
import json
import sys

def run_claude_command(command):
    """Run Claude Code command and return JSON result"""
    try:
        result = subprocess.run(
            ['claude', '--non-interactive', command],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        # Parse JSON from stdout even on failure
        if e.stdout:
            return json.loads(e.stdout)
        raise

def main():
    print("Running Claude Code validations...\n")
    
    # Run validations
    validations = [
        ('/vd all', 'Design System'),
        ('/sc all', 'Security'),
        ('/tr all', 'Tests'),
        ('/deps scan', 'Dependencies')
    ]
    
    all_passed = True
    results = []
    
    for command, name in validations:
        result = run_claude_command(command)
        passed = result.get('success', False)
        
        status = '✓' if passed else '✗'
        print(f"{name}: {status}")
        
        if not passed:
            all_passed = False
            # Show details
            if 'totalViolations' in result.get('results', {}):
                print(f"  Violations: {result['results']['totalViolations']}")
            elif 'vulnerabilities' in result.get('results', {}):
                print(f"  Issues: {result['results']['vulnerabilities']}")
        
        results.append(result)
    
    # Save results
    with open('validation-results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    sys.exit(0 if all_passed else 1)

if __name__ == '__main__':
    main()
```

## CI/CD Integration

### Parallel Execution
Run multiple validations simultaneously:

```yaml
# GitHub Actions
strategy:
  matrix:
    check:
      - { cmd: "/vd all", name: "design" }
      - { cmd: "/sc all", name: "security" }
      - { cmd: "/deps scan", name: "deps" }
      - { cmd: "/tr all", name: "tests" }

steps:
  - name: Run ${{ matrix.check.name }}
    run: |
      claude --non-interactive "${{ matrix.check.cmd }}" \
        > ${{ matrix.check.name }}-results.json
```

### Error Handling
```bash
# Capture both stdout and stderr
if ! claude --non-interactive "/vd all" > results.json 2>&1; then
  echo "Validation failed"
  cat results.json
  exit 1
fi
```

### Timeout Handling
```bash
# Add timeout to prevent hanging
timeout 300 claude --non-interactive "/tr all" || {
  echo "Tests timed out after 5 minutes"
  exit 1
}
```

## Parsing Results

### Using jq
```bash
# Get specific values
VIOLATIONS=$(claude --non-interactive "/vd all" | jq -r '.results.totalViolations')
PROGRESS=$(claude --non-interactive "/sv status" | jq -r '.stages[0].progress')

# Check boolean conditions
claude --non-interactive "/sc all" | jq -e '.success' || echo "Security failed"

# Extract arrays
claude --non-interactive "/vd all" | jq -r '.results.files | keys[]'
```

### Using grep/awk
```bash
# Simple success check
claude --non-interactive "/vd all" | grep -q '"success": true'

# Extract values
claude --non-interactive "/sv check 1" | awk -F'"progress": ' '{print $2}' | awk -F',' '{print $1}'
```

## Advanced Usage

### Custom Output Processing
```bash
#!/usr/bin/env bash
# process-results.sh

# Run validation and process results
claude --non-interactive "/vd all" | {
  read -r json
  
  # Parse with native bash
  if [[ "$json" =~ \"success\":\ true ]]; then
    echo "✅ Design validation passed"
  else
    # Extract violation count
    if [[ "$json" =~ \"totalViolations\":\ ([0-9]+) ]]; then
      count="${BASH_REMATCH[1]}"
      echo "❌ Design validation failed: $count violations"
    fi
  fi
  
  # Save for later
  echo "$json" > design-validation.json
}
```

### Conditional Execution
```bash
# Only run expensive checks if quick ones pass
if claude --non-interactive "/vd current"; then
  echo "Current file valid, checking all..."
  claude --non-interactive "/vd all"
fi
```

### Result Aggregation
```bash
# Aggregate results from multiple commands
{
  echo '{"validations": ['
  
  # Run each validation and collect results
  first=true
  for cmd in "/vd all" "/sc all" "/tr all" "/deps scan"; do
    if [ "$first" = true ]; then
      first=false
    else
      echo ','
    fi
    
    claude --non-interactive "$cmd" | tr -d '\n'
  done
  
  echo ']}'
} > all-results.json

# Process aggregated results
jq '.validations | map({command: .command, success: .success}) | group_by(.success)' all-results.json
```

### Retry Logic
```bash
# Retry failed commands with backoff
retry_command() {
  local cmd=$1
  local max_attempts=3
  local attempt=1
  
  while [ $attempt -le $max_attempts ]; do
    if claude --non-interactive "$cmd"; then
      return 0
    fi
    
    echo "Attempt $attempt failed, retrying..."
    sleep $((attempt * 2))
    ((attempt++))
  done
  
  return 1
}

# Use with any command
retry_command "/deps scan"
```

## Debugging

### Enable Debug Output
```bash
# Set debug environment variable
CLAUDE_DEBUG=true claude --non-interactive "/vd all"

# Verbose output
CLAUDE_VERBOSE=true claude --non-interactive "/sc all"
```

### Test Locally
```bash
# Simulate CI environment
export CLAUDE_NON_INTERACTIVE=true
export CI=true

# Run commands as they would in CI
claude "/validate-design all"
```

### Common Issues

#### 1. No JSON Output
```bash
# Ensure command supports non-interactive mode
claude --non-interactive "/help" 2>&1 | head -20

# Check if command exists
claude --non-interactive "/invalid-command" 2>&1
```

#### 2. Parsing Errors
```bash
# Validate JSON output
claude --non-interactive "/vd all" | jq . > /dev/null || echo "Invalid JSON"

# Pretty print for debugging
claude --non-interactive "/vd all" | jq .
```

#### 3. Exit Code Mismatch
```bash
# Check actual exit code
claude --non-interactive "/vd all"
echo "Exit code: $?"

# Compare with JSON
claude --non-interactive "/vd all" | jq -r '.exitCode'
```

## Performance Tips

### 1. Scope Appropriately
```bash
# Check current file first (fast)
if ! claude --non-interactive "/vd current"; then
  # Only run full check if current fails
  claude --non-interactive "/vd all"
fi
```

### 2. Cache Results
```bash
# Cache validation results
CACHE_FILE=".validation-cache.json"
CACHE_AGE=300  # 5 minutes

if [ -f "$CACHE_FILE" ]; then
  age=$(($(date +%s) - $(stat -f %m "$CACHE_FILE" 2>/dev/null || stat -c %Y "$CACHE_FILE")))
  if [ $age -lt $CACHE_AGE ]; then
    cat "$CACHE_FILE"
    exit 0
  fi
fi

# Run validation and cache
claude --non-interactive "/vd all" | tee "$CACHE_FILE"
```

### 3. Parallel Execution
```bash
# Run validations in parallel
(
  claude --non-interactive "/vd all" > design.json &
  claude --non-interactive "/sc all" > security.json &
  claude --non-interactive "/deps scan" > deps.json &
  wait
)

# Process results
for file in design.json security.json deps.json; do
  if ! jq -e '.success' "$file" > /dev/null; then
    echo "$file validation failed"
    exit 1
  fi
done
```

## Integration Patterns

### Pre-commit Hook
```bash
#!/usr/bin/env bash
# .git/hooks/pre-commit

echo "Running pre-commit validations..."

# Only check changed files
changed_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(tsx?|jsx?)$')

if [ -n "$changed_files" ]; then
  if ! claude --non-interactive "/vd current"; then
    echo "Design validation failed. Run '/vd fix' to auto-fix."
    exit 1
  fi
fi

if ! claude --non-interactive "/tr changed"; then
  echo "Tests failed. Fix before committing."
  exit 1
fi
```

### Merge Request Pipeline
```yaml
# .gitlab-ci.yml
validation:
  stage: test
  script:
    - npm install -g @anthropic-ai/claude-code
    - |
      failed=0
      
      # Run all validations, track failures
      claude --non-interactive "/vd all" || ((failed++))
      claude --non-interactive "/sc all" || ((failed++))
      claude --non-interactive "/deps scan" || ((failed++))
      claude --non-interactive "/tr all" || ((failed++))
      
      # Report summary
      if [ $failed -eq 0 ]; then
        echo "All validations passed!"
      else
        echo "$failed validation(s) failed"
        exit 1
      fi
  artifacts:
    reports:
      junit: test-results.xml
    paths:
      - "*-results.json"
```

### Scheduled Audits
```yaml
# GitHub Actions - daily security audit
name: Daily Security Audit
on:
  schedule:
    - cron: '0 9 * * *'  # 9 AM daily

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Security Audit
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          npm install -g @anthropic-ai/claude-code
          
          # Run comprehensive audit
          claude --non-interactive "/sc all" > security-audit.json
          claude --non-interactive "/deps scan --production" > deps-audit.json
          
          # Create issue if problems found
          if ! jq -e '.success' security-audit.json > /dev/null; then
            gh issue create \
              --title "Security Audit Failed - $(date +%Y-%m-%d)" \
              --body "$(jq -r '.results' security-audit.json)"
          fi
```

## Best Practices

### 1. Always Check Exit Codes
```bash
# Good
if claude --non-interactive "/vd all"; then
  echo "Validation passed"
fi

# Better - capture output too
if output=$(claude --non-interactive "/vd all"); then
  echo "Validation passed"
  echo "$output" > validation-success.json
else
  echo "Validation failed"
  echo "$output" > validation-failure.json
  exit 1
fi
```

### 2. Handle Missing Commands
```bash
# Check if command exists
if ! claude --non-interactive "/help" | grep -q "validate-design"; then
  echo "Warning: validate-design command not available"
  exit 0  # Don't fail CI for missing optional commands
fi
```

### 3. Set Appropriate Timeouts
```bash
# Add timeouts for long-running commands
timeout 300 claude --non-interactive "/tr all" || {
  echo "Tests timed out after 5 minutes"
  exit 1
}
```

### 4. Parse Safely
```bash
# Safe JSON parsing with defaults
get_json_value() {
  local json=$1
  local key=$2
  local default=$3
  
  echo "$json" | jq -r ".$key // \"$default\"" 2>/dev/null || echo "$default"
}

result=$(claude --non-interactive "/vd all")
violations=$(get_json_value "$result" "results.totalViolations" "0")
```

### 5. Log for Debugging
```bash
# Save all outputs for debugging
LOG_DIR="ci-logs/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$LOG_DIR"

claude --non-interactive "/vd all" 2>&1 | tee "$LOG_DIR/design-validation.log"
```

## Migration Guide

### From Interactive Commands
```bash
# Before (interactive)
claude "/validate-design all"
# Prompts for confirmation, shows progress

# After (non-interactive)
claude --non-interactive "/validate-design all"
# No prompts, returns JSON
```

### From Shell Scripts
```bash
# Before
#!/bin/bash
echo "y" | claude "/stage-validate check 1"  # Risky!

# After
#!/bin/bash
claude --non-interactive "/stage-validate check 1"  # Safe
```

### From Manual Testing
```bash
# Before: Run each command manually
# After: Automated script
#!/usr/bin/env bash

validations=(
  "/vd all:Design System"
  "/sc all:Security"
  "/deps scan:Dependencies"
  "/tr all:Tests"
)

for item in "${validations[@]}"; do
  cmd="${item%%:*}"
  name="${item#*:}"
  
  printf "%-20s" "$name:"
  if claude --non-interactive "$cmd" > /dev/null 2>&1; then
    echo "✅"
  else
    echo "❌"
  fi
done
```

## Summary

Non-interactive mode enables:
- ✅ CI/CD automation
- ✅ Scripted workflows
- ✅ Parallel execution
- ✅ Result parsing
- ✅ Error handling

Key points:
1. Use `--non-interactive` flag or `CLAUDE_NON_INTERACTIVE=true`
2. Parse JSON output for detailed results
3. Check exit codes for success/failure
4. Handle timeouts and retries
5. Log outputs for debugging

With non-interactive mode, Claude Code becomes a powerful automation tool for maintaining code quality in any development workflow!
