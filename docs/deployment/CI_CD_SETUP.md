# CI/CD Setup with Claude Code

This guide shows how to integrate Claude Code's quality gates into your CI/CD pipelines.

## Overview

Claude Code supports non-interactive mode for automation:
- Output: Structured JSON
- Exit codes: 0 (success), 1+ (failure)
- No prompts: All operations automatic
- Parallel execution: Run multiple checks

## Prerequisites

1. **API Key**: Set `ANTHROPIC_API_KEY` in CI secrets
2. **Node.js 18+**: Required for Claude Code
3. **Project Setup**: Claude Code commands configured

## Supported Commands

These commands support non-interactive mode:

### Validation Commands
- `/stage-validate` (`/sv`) - Stage validation
- `/validate-design` (`/vd`) - Design system compliance
- `/prp-execute` - PRP validation loops
- `/deps scan` - Dependency scanning
- `/test-runner` (`/tr`) - Test execution
- `/security-check` (`/sc`) - Security validation
- `/validate-async` - Async pattern checks
- `/grade` - Implementation grading

### Status Commands
- `/work-status` - Project status
- `/branch-status` - Branch health
- `/feature-status` - Feature tracking
- `/agent-health` - Agent system status

## GitHub Actions

### Basic Setup

```yaml
name: Quality Gates
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Claude Code
        run: npm install -g @anthropic-ai/claude-code
        
      - name: Run Validation
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude --non-interactive "/validate-design all"
```

### Complete Example

See `.github/workflows/claude-code-quality-gates.yml` for a comprehensive example that includes:
- Multiple validation steps
- Error handling
- PR comments
- Summary reports
- Artifact uploads

### Matrix Strategy

Run validations in parallel:

```yaml
strategy:
  matrix:
    validation:
      - { cmd: "/vd all", name: "Design" }
      - { cmd: "/sc all", name: "Security" }
      - { cmd: "/deps scan", name: "Dependencies" }
      - { cmd: "/tr all", name: "Tests" }
      
steps:
  - name: Run ${{ matrix.validation.name }}
    run: |
      claude --non-interactive "${{ matrix.validation.cmd }}"
```

## GitLab CI

### Basic Pipeline

```yaml
stages:
  - validate
  - test
  - deploy

variables:
  ANTHROPIC_API_KEY: $ANTHROPIC_API_KEY

before_script:
  - npm install -g @anthropic-ai/claude-code

design-validation:
  stage: validate
  script:
    - claude --non-interactive "/validate-design all"
  artifacts:
    reports:
      junit: design-results.xml
    paths:
      - design-results.json

security-check:
  stage: validate
  script:
    - claude --non-interactive "/security-check all"
  allow_failure: true

stage-validation:
  stage: validate
  script:
    - claude --non-interactive "/stage-validate check current"
  only:
    - merge_requests
```

### Parallel Execution

```yaml
validate:
  stage: validate
  parallel:
    matrix:
      - VALIDATION: [design, security, deps, async]
  script:
    - |
      case $VALIDATION in
        design) claude --non-interactive "/vd all" ;;
        security) claude --non-interactive "/sc all" ;;
        deps) claude --non-interactive "/deps scan" ;;
        async) claude --non-interactive "/validate-async" ;;
      esac
```

## Jenkins

### Jenkinsfile Example

```groovy
pipeline {
    agent any
    
    environment {
        ANTHROPIC_API_KEY = credentials('anthropic-api-key')
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'npm install -g @anthropic-ai/claude-code'
            }
        }
        
        stage('Quality Gates') {
            parallel {
                stage('Design') {
                    steps {
                        sh 'claude --non-interactive "/validate-design all" > design-results.json'
                        publishJSON([
                            json: 'design-results.json',
                            name: 'Design Validation'
                        ])
                    }
                }
                
                stage('Security') {
                    steps {
                        sh 'claude --non-interactive "/security-check all" > security-results.json'
                        publishJSON([
                            json: 'security-results.json',
                            name: 'Security Check'
                        ])
                    }
                }
                
                stage('Tests') {
                    steps {
                        sh 'claude --non-interactive "/test-runner all" > test-results.json'
                        junit 'test-results.xml'
                    }
                }
            }
        }
        
        stage('Grade') {
            when {
                branch 'main'
            }
            steps {
                sh 'claude --non-interactive "/grade --requirements"'
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: '*-results.json', fingerprint: true
        }
        failure {
            emailext (
                subject: "Claude Code validation failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Check the validation results at ${env.BUILD_URL}",
                to: "${env.CHANGE_AUTHOR_EMAIL}"
            )
        }
    }
}
```

## CircleCI

### .circleci/config.yml

```yaml
version: 2.1

orbs:
  node: circleci/node@5.0

jobs:
  validate:
    docker:
      - image: cimg/node:18.0
    steps:
      - checkout
      - run:
          name: Install Claude Code
          command: npm install -g @anthropic-ai/claude-code
      - run:
          name: Design Validation
          command: |
            claude --non-interactive "/validate-design all" | tee design-results.json
            echo "Design violations: $(jq -r '.totalViolations' design-results.json)"
      - run:
          name: Security Check
          command: claude --non-interactive "/security-check all"
      - run:
          name: Stage Validation
          command: claude --non-interactive "/stage-validate check current"
      - store_artifacts:
          path: ./*-results.json
      - store_test_results:
          path: ./test-results

workflows:
  quality-gates:
    jobs:
      - validate:
          context: claude-code-credentials
```

## Exit Codes

Standard exit codes for automation:

| Code | Meaning | Example |
|------|---------|---------|
| 0 | Success | All validations passed |
| 1 | Validation failure | Design violations found |
| 2 | Configuration error | Missing required files |
| 3 | Tool error | API connection failed |
| 4 | Multiple failures | Several checks failed |

## JSON Output Format

All commands output consistent JSON:

```json
{
  "success": true,
  "timestamp": "2025-01-30T12:34:56Z",
  "command": "/validate-design",
  "results": {
    // Command-specific results
  },
  "duration_ms": 1234,
  "exitCode": 0
}
```

## Best Practices

### 1. Fail Fast
Run critical validations first:
```yaml
- claude --non-interactive "/security-check critical" || exit 1
- claude --non-interactive "/validate-design all" || exit 1
- claude --non-interactive "/test-runner smoke" || exit 1
```

### 2. Parallel Execution
Run independent checks simultaneously:
```yaml
parallel:
  - claude --non-interactive "/vd all" > design.json &
  - claude --non-interactive "/sc all" > security.json &
  - claude --non-interactive "/deps scan" > deps.json &
wait
```

### 3. Cache Dependencies
Speed up builds by caching:
```yaml
- name: Cache Claude Code
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-claude-code-${{ hashFiles('**/package-lock.json') }}
```

### 4. Progressive Validation
Different checks for different stages:

```yaml
# PR validation - quick checks
on: pull_request
  run: |
    claude --non-interactive "/vd current"
    claude --non-interactive "/tr changed"

# Main branch - comprehensive
on:
  push:
    branches: [main]
  run: |
    claude --non-interactive "/vd all"
    claude --non-interactive "/sc all"
    claude --non-interactive "/grade"
```

### 5. Error Reporting
Parse JSON for detailed reports:

```bash
# Extract specific errors
VIOLATIONS=$(jq -r '.files | to_entries[] | "\(.key): \(.value | join(", "))"' design-results.json)

# Create summary
if [ $(jq -r '.totalViolations' design-results.json) -gt 0 ]; then
  echo "::error::Design violations found: $VIOLATIONS"
fi
```

## Debugging

### Enable Verbose Output
```bash
CLAUDE_DEBUG=true claude --non-interactive "/vd all"
```

### Test Locally
```bash
# Simulate CI environment
export CLAUDE_NON_INTERACTIVE=true
claude "/validate-design all"
```

### Common Issues

1. **API Key not found**
   ```bash
   Error: ANTHROPIC_API_KEY environment variable not set
   Solution: Add to CI secrets and expose in job
   ```

2. **Command not found**
   ```bash
   Error: Command '/vd' not found
   Solution: Ensure .claude/ directory is in repo
   ```

3. **Timeout**
   ```bash
   Error: Command timed out after 300s
   Solution: Increase timeout or run fewer files
   ```

## Advanced Usage

### Custom Quality Gates
Create composite validations:

```bash
#!/bin/bash
# quality-gate.sh

echo "Running comprehensive quality gates..."

# Required gates (must pass)
claude --non-interactive "/vd all" || exit 1
claude --non-interactive "/sc critical" || exit 1
claude --non-interactive "/tr smoke" || exit 1

# Advisory gates (warn only)
claude --non-interactive "/deps scan" || echo "::warning::Dependency issues found"
claude --non-interactive "/grade" || echo "::warning::Implementation below threshold"

echo "Quality gates passed!"
```

### Integration with Other Tools

Combine with traditional tools:

```yaml
- name: Traditional Linting
  run: npm run lint
  
- name: Claude Design Validation
  run: claude --non-interactive "/vd all"
  
- name: Traditional Tests
  run: npm test
  
- name: Claude Security Check
  run: claude --non-interactive "/sc all"
```

### Monitoring Trends

Track quality over time:

```bash
# Save results with timestamp
DATE=$(date +%Y%m%d-%H%M%S)
claude --non-interactive "/vd all" > "reports/design-$DATE.json"

# Generate trend report
claude --non-interactive "/show-metrics trends" > "reports/trends-$DATE.json"
```

## Examples

See these files for working examples:
- `.github/workflows/claude-code-quality-gates.yml` - GitHub Actions
- `scripts/ci-validate.sh` - Shell script wrapper
- `docs/ci-cd/` - Platform-specific guides

## Support

- Claude Code Docs: https://docs.anthropic.com/claude-code
- GitHub Issues: Report CI/CD specific issues
- Discord: #claude-code-automation channel
