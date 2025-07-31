---
name: chain
description: |
  Execute smart chains with auto-triggers, prerequisites, and context passing.
  Chains can detect conditions and suggest running automatically.
argument-hint: <chain-name|check|list> [options]
aliases: ["chains", "workflow"]
---

# Smart Chain Execution

**Action**: $ARGUMENTS

## 🔗 Smart Chain System

This enhanced chain system supports:
- **Auto-triggers**: Detect when chains should run
- **Prerequisites**: Ensure conditions are met
- **Context passing**: Share data between steps
- **Success/failure handlers**: Automatic recovery
- **Checkpointing**: Save progress automatically

!`node << 'EOF'
const SmartChainSystem = require('./.claude/utils/smart-chains.js');
const readline = require('readline');

const system = new SmartChainSystem();
const args = process.argv.slice(2);
const action = args[0] || 'check';

async function promptUser(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  return new Promise((resolve) => {
    rl.question(question + ' ', (answer) => {
      rl.close();
      resolve(answer);
    });
  });
}

async function main() {
  switch (action) {
    case 'check':
      // Check for triggered chains
      const triggered = system.checkTriggers();
      
      if (triggered.length === 0) {
        console.log('No chains triggered based on current conditions.');
        return;
      }
      
      console.log('\n🔗 Smart Chain Triggers Detected:\n');
      for (const trigger of triggered) {
        console.log(`📌 ${trigger.name}`);
        console.log(`   ${trigger.chain.description}`);
        console.log(`   Conditions met for auto-trigger\n`);
        
        const answer = await promptUser(trigger.prompt);
        if (answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes') {
          console.log(`\nExecuting chain: ${trigger.name}\n`);
          const result = await system.executeChain(trigger.name);
          
          if (result.success) {
            console.log(`\n✅ Chain completed successfully!`);
          } else {
            console.log(`\n❌ Chain failed: ${result.error}`);
          }
        }
      }
      break;
      
    case 'list':
      // List all available chains
      console.log('\n📚 Available Smart Chains:\n');
      
      const chains = system.chains.chains;
      for (const [name, chain] of Object.entries(chains)) {
        console.log(`📌 ${name}`);
        console.log(`   ${chain.description}`);
        
        if (chain.triggers) {
          console.log('   🔍 Auto-triggers when conditions are met');
        }
        
        if (chain.prerequisites) {
          console.log('   ✓ Has prerequisites that must be met');
        }
        
        console.log('');
      }
      
      // Show status
      const status = system.getStatus();
      console.log('📊 Chain Status:');
      console.log(`   Running: ${status.running}`);
      console.log(`   Completed: ${status.completed}`);
      console.log(`   Failed: ${status.failed}`);
      break;
      
    case 'status':
      // Show detailed status
      const detailedStatus = system.getStatus();
      
      console.log('\n📊 Chain Execution Status:\n');
      
      if (Object.keys(detailedStatus.chains.running).length > 0) {
        console.log('🏃 Currently Running:');
        for (const [name, info] of Object.entries(detailedStatus.chains.running)) {
          const duration = Date.now() - info.startTime;
          console.log(`   ${name} - Step ${info.currentStep} (${Math.round(duration / 1000)}s)`);
        }
        console.log('');
      }
      
      if (Object.keys(detailedStatus.chains.completed).length > 0) {
        console.log('✅ Recently Completed:');
        const completed = Object.entries(detailedStatus.chains.completed)
          .sort((a, b) => b[1].completedAt - a[1].completedAt)
          .slice(0, 5);
          
        for (const [name, info] of completed) {
          const when = new Date(info.completedAt).toLocaleString();
          console.log(`   ${name} - ${when} (${Math.round(info.duration / 1000)}s)`);
        }
        console.log('');
      }
      
      if (Object.keys(detailedStatus.chains.failed).length > 0) {
        console.log('❌ Recent Failures:');
        const failed = Object.entries(detailedStatus.chains.failed)
          .sort((a, b) => b[1].failedAt - a[1].failedAt)
          .slice(0, 5);
          
        for (const [name, info] of failed) {
          const when = new Date(info.failedAt).toLocaleString();
          console.log(`   ${name} - ${when}`);
          console.log(`     Error: ${info.error}`);
        }
      }
      break;
      
    default:
      // Execute a specific chain
      const chainName = action;
      
      if (!system.chains.chains[chainName]) {
        console.log(`❌ Chain '${chainName}' not found.`);
        console.log('\nAvailable chains:');
        for (const name of Object.keys(system.chains.chains)) {
          console.log(`  - ${name}`);
        }
        return;
      }
      
      // Check prerequisites
      const prereqCheck = system.checkPrerequisites(chainName);
      if (!prereqCheck.passed) {
        console.log(`\n⚠️  Prerequisites not met for '${chainName}':`);
        console.log(`   ${prereqCheck.error}`);
        console.log('\nPlease resolve these issues and try again.');
        return;
      }
      
      console.log(`\n🔗 Executing chain: ${chainName}\n`);
      const result = await system.executeChain(chainName);
      
      if (result.success) {
        console.log(`\n✅ Chain '${chainName}' completed successfully!`);
      } else {
        console.log(`\n❌ Chain '${chainName}' failed: ${result.error}`);
      }
  }
}

main().catch(console.error);
EOF`

## 📋 Available Actions

### Check for Triggers
```bash
/chain check
```
Scans all chains and prompts to run any that meet trigger conditions.

### List All Chains
```bash
/chain list
```
Shows all available chains with their features.

### View Status
```bash
/chain status
```
Shows currently running, completed, and failed chains.

### Execute Specific Chain
```bash
/chain onboard-existing
/chain morning-startup
/chain pr-ready
```

## 🎯 Smart Chain Features

### 1. Auto-Triggers
Chains can detect conditions and suggest running:
```json
"triggers": {
  "conditions": {
    "any": [
      "hoursSinceLastCommand > 8",
      "isFirstCommandToday === true"
    ]
  },
  "prompt": "Welcome back! Run morning setup? (y/n)"
}
```

### 2. Prerequisites
Ensure conditions are met before running:
```json
"prerequisites": {
  "all": [
    "tests.passing",
    "git.clean"
  ],
  "error": "Tests must pass and git must be clean"
}
```

### 3. Context Passing
Share data between steps:
```json
"context": {
  "save": ["deployment_url", "bundle_size"]
}
```

### 4. Conditional Steps
Skip steps based on conditions:
```json
{
  "command": "/tr unit",
  "condition": "exec:git diff --name-only | grep -q '\\.ts$'"
}
```

### 5. Success/Failure Handlers
Automatic recovery or cleanup:
```json
"on-success": "/checkpoint create success",
"on-failure": "/rollback && /checkpoint restore"
```

## 🔍 Condition Expressions

### File Checks
- `exists(path)` - File or directory exists
- `!exists(path)` - File doesn't exist
- `file:path` - Same as exists
- `fileCount(pattern) > n` - Count files matching pattern

### Time-Based
- `hoursSinceLastCommand > n` - Hours since last command
- `daysSinceLastCommand >= n` - Days since last command
- `isFirstCommandToday === true` - First command today

### Command Execution
- `exec:command` - Run command, true if exit code 0
- `tests.passing` - Tests pass
- `git.clean` - No uncommitted changes

### Logical Operators
- `all: [...]` - All conditions must be true (AND)
- `any: [...]` - At least one must be true (OR)
- `none: [...]` - None can be true (NOT)

## 📚 Example Chains

### Morning Routine
Automatically suggests running when you start work:
```bash
/chain check
# Detects: First command of the day
# Runs: Smart resume, bug list, dependency scan, etc.
```

### PR Readiness
Ensures everything is ready for a pull request:
```bash
/chain pr-ready
# Checks: Clean git, passing tests
# Runs: All validations, creates PR
```

### Emergency Rollback
Triggers when multiple failures detected:
```bash
/chain check
# Detects: High error count
# Offers: Rollback to last known good state
```

## 🔧 Creating Custom Chains

Add to `.claude/chains-enhanced.json`:
```json
{
  "my-workflow": {
    "description": "My custom workflow",
    "triggers": {
      "conditions": { ... },
      "prompt": "Run my workflow?"
    },
    "prerequisites": { ... },
    "steps": [ ... ],
    "on-success": "...",
    "on-failure": "..."
  }
}
```

## 💡 Tips

1. **Morning Routine**: Run `/chain check` when you start work
2. **Before PR**: Always run `/chain pr-ready`
3. **After Errors**: Check if `/chain check` suggests fixes
4. **Custom Workflows**: Create chains for repetitive tasks
5. **Monitor Progress**: Use `/chain status` to track execution

## 🔄 Integration

Chains integrate with:
- `/checkpoint` - Automatic progress saving
- `/orchestrate` - Multi-agent coordination
- `/grade` - Validation steps
- `/capture-to-issue` - Results documentation

The smart chain system makes complex workflows simple and reliable!
