# Chain Automation Guide

Smart chains automate complex workflows with conditional execution, prerequisites, and automatic recovery.

## Overview

The enhanced chain system provides:
- **Auto-triggers**: Detect when to suggest running chains
- **Prerequisites**: Ensure conditions are met before execution
- **Context passing**: Share data between steps
- **Success/failure handlers**: Automatic recovery
- **Conditional steps**: Skip based on conditions
- **Checkpointing**: Save progress automatically

## Quick Start

### Check for Triggered Chains
```bash
/chain check
```
This scans all chains and prompts to run any that meet trigger conditions.

### Execute a Specific Chain
```bash
/chain morning-startup
/chain pr-ready
/chain feature-complete
```

### View Available Chains
```bash
/chain list
```

### Check Status
```bash
/chain status
```

## Chain Structure

Chains are defined in `.claude/chains-enhanced.json`:

```json
{
  "chain-name": {
    "description": "What this chain does",
    "triggers": {
      "conditions": { /* when to suggest */ },
      "prompt": "User confirmation message",
      "auto": false  // Never fully automatic
    },
    "prerequisites": {
      "all": [ /* must all be true */ ],
      "any": [ /* at least one true */ ],
      "error": "Message if not met"
    },
    "steps": [
      /* commands or agent tasks */
    ],
    "context": {
      "save": ["variable_names"]
    },
    "checkpoints": ["after:Planning"],
    "on-success": "command to run",
    "on-failure": "recovery command"
  }
}
```

## Condition Expressions

### File System
```json
"conditions": {
  "all": [
    "exists(.claude/)",              // File/dir exists
    "!exists(node_modules/)",        // Doesn't exist
    "fileCount(*.ts) > 10",          // File count
    "file:package.json"              // Same as exists
  ]
}
```

### Time-Based
```json
"conditions": {
  "any": [
    "hoursSinceLastCommand > 8",     // Hours idle
    "daysSinceLastCommand >= 1",     // Days idle
    "isFirstCommandToday === true"   // First today
  ]
}
```

### Command Execution
```json
"conditions": {
  "all": [
    "exec:npm test",                 // Command succeeds
    "exec:git status --porcelain | wc -l | grep -q '^0$'",
    "tests.passing",                 // Shortcut for tests
    "git.clean"                      // Shortcut for git
  ]
}
```

### Logical Operators
```json
"conditions": {
  "all": [ /* AND - all must be true */ ],
  "any": [ /* OR - at least one true */ ],
  "none": [ /* NOT - none can be true */ ]
}
```

## Step Types

### Simple Commands
```json
"steps": [
  "/validate-design",
  "npm test",
  "echo 'Done!'"
]
```

### Agent Tasks
```json
"steps": [
  {
    "agent": "frontend",
    "task": "Build the login component"
  }
]
```

### Conditional Steps
```json
"steps": [
  {
    "command": "/tr unit",
    "condition": "exec:git diff --name-only | grep -q '\\.ts$'"
  }
]
```

### Grouped Steps
```json
"steps": [
  {
    "name": "Planning",
    "commands": ["/prd", "/gt", "/at"]
  },
  {
    "name": "Implementation",
    "commands": ["/orch", "/pt"]
  }
]
```

### Expected Failures
```json
"steps": [
  {
    "command": "npm test",
    "expectFailure": true,  // For TDD red phase
    "reason": "Tests should fail initially"
  }
]
```

## Context Management

### Saving Context
```json
"context": {
  "save": ["deployment_url", "bundle_size", "test_results"]
}
```

### Using Context
Variables are replaced in commands:
```json
"steps": [
  "echo 'Deployed to: ${deployment_url}'",
  "curl ${deployment_url}/health"
]
```

## Checkpointing

### Automatic Checkpoints
```json
"checkpoints": [
  "after:Planning",      // After step named "Planning"
  "after:2",            // After step index 2
  "before:Deploy"       // Before step named "Deploy"
]
```

### Rollback on Failure
```json
"on-failure": "/checkpoint restore latest"
```

## Built-in Chains

### onboard-existing
Detects existing projects without Claude setup:
- Triggers: No .claude/ directory but has code
- Actions: Analyze, migrate design, setup standards

### morning-startup
Comprehensive morning routine:
- Triggers: 8+ hours idle or first command today
- Actions: Load context, check bugs, scan deps, show status

### pr-ready
Ensure quality before pull request:
- Prerequisites: Clean git, passing tests
- Actions: All validations, create PR

### emergency-rollback
Quick recovery from failures:
- Triggers: High error count detected
- Actions: Restore checkpoint, reset git

### feature-complete
End-to-end feature workflow:
- Prerequisites: PRP or PRD exists
- Phases: Planning → Implementation → Testing → Validation
- Checkpoints: After each phase

### smart-test
Run tests based on changes:
- Conditional: Only runs relevant test suites
- Optimized: Skips unchanged areas

### daily-standup
Generate standup report:
- Triggers: 9-10 AM on first command
- Actions: Yesterday's commits, today's tasks, blockers

### weekly-cleanup
Maintenance tasks:
- Triggers: Monday morning
- Actions: Clean branches, update deps, prune

## Creating Custom Chains

### 1. Basic Chain
```json
{
  "my-deploy": {
    "description": "Deploy to production",
    "steps": [
      "/test-runner all",
      "/build",
      "/deploy prod"
    ]
  }
}
```

### 2. With Prerequisites
```json
{
  "safe-migrate": {
    "description": "Safe database migration",
    "prerequisites": {
      "all": [
        "tests.passing",
        "exists(migrations/*.sql)"
      ],
      "error": "Tests must pass and migrations must exist"
    },
    "steps": [
      "/checkpoint create pre-migration",
      "/db:migrate",
      "/test-runner integration"
    ],
    "on-failure": "/db:rollback"
  }
}
```

### 3. With Auto-Triggers
```json
{
  "fix-lint": {
    "description": "Auto-fix linting errors",
    "triggers": {
      "conditions": {
        "any": [
          "exec:npm run lint 2>&1 | grep -q 'error'"
        ]
      },
      "prompt": "Linting errors detected. Fix? (y/n)"
    },
    "steps": [
      "npm run lint:fix",
      "/vd fix"
    ]
  }
}
```

### 4. Complex Workflow
```json
{
  "release": {
    "description": "Full release workflow",
    "prerequisites": {
      "all": [
        "git.clean",
        "tests.passing",
        "exec:git branch --show-current | grep -q '^main$'"
      ]
    },
    "steps": [
      {
        "name": "Version",
        "commands": ["npm version patch"]
      },
      {
        "name": "Build",
        "commands": ["npm run build", "npm run test:prod"]
      },
      {
        "name": "Deploy",
        "commands": ["/deploy prod"],
        "condition": "tests.passing"
      }
    ],
    "checkpoints": ["after:Build"],
    "on-success": "git push --tags",
    "on-failure": "git reset --hard HEAD~1"
  }
}
```

## Best Practices

### 1. Always Confirm
Never make chains fully automatic:
```json
"triggers": {
  "auto": false,  // Always false
  "prompt": "Clear question? (y/n)"
}
```

### 2. Clear Prerequisites
Be explicit about requirements:
```json
"prerequisites": {
  "all": ["tests.passing", "git.clean"],
  "error": "Cannot proceed: uncommitted changes or failing tests"
}
```

### 3. Use Checkpoints
Save progress for long chains:
```json
"checkpoints": ["after:Build", "after:Test"],
"on-failure": "/checkpoint restore latest"
```

### 4. Handle Failures
Always provide recovery:
```json
"on-failure": "echo 'Failed! Run /debug for details'"
```

### 5. Test Conditions
Verify condition expressions:
```bash
# Test a condition
exec:git status --porcelain | wc -l | grep -q '^0$'
echo $?  # Should be 0 if true
```

## Debugging

### Check Why Not Triggered
```bash
# Manually test conditions
/chain check --verbose
```

### View Execution Log
```bash
# Check state file
cat .claude/state/chain-state.json
```

### Test Individual Steps
```bash
# Run steps manually to debug
/validate-design
echo $?  # Check exit code
```

## Integration

Chains work with:
- **Commands**: Any Claude Code command
- **Agents**: Native agent invocation
- **Scripts**: Shell commands
- **Checkpoints**: Progress saving
- **Issues**: Result capture

## Examples

### Development Flow
```bash
# Morning
/chain check
> "Welcome back! Run morning setup? (y/n)" y

# Before lunch
/chain feature-complete

# Before PR
/chain pr-ready

# End of day
/chain check
> "Create end-of-day checkpoint? (y/n)" y
```

### CI/CD Integration
```yaml
# In GitHub Actions
- name: Run PR validation chain
  run: |
    claude --non-interactive "/chain pr-ready"
```

## Troubleshooting

### Chain Not Found
```bash
/chain list  # See available chains
```

### Prerequisites Failed
Check the specific error and resolve:
```bash
npm test  # Fix failing tests
git add . && git commit  # Clean git status
```

### Step Failed
Check which step and why:
```bash
/chain status  # See failed chains
cat .claude/state/chain-state.json  # Detailed info
```

### Condition Not Working
Test conditions individually:
```bash
# Test file existence
ls .claude/ && echo "exists" || echo "not exists"

# Test command
npm test && echo "passing" || echo "failing"
```

## Summary

Smart chains turn complex multi-step workflows into single commands with:
- Intelligent triggering
- Safety prerequisites  
- Progress tracking
- Automatic recovery
- Conditional execution

Start with `/chain check` and let the system guide you!