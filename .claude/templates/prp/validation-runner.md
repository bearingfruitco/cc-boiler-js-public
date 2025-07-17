# PRP Validation Loop Runner

A TypeScript implementation of the PRP validation loop system that integrates
with your existing commands and provides automated validation execution.

## Implementation

```typescript
// lib/prp/validation-runner.ts

import { execSync } from 'child_process';
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import chalk from 'chalk';

export interface ValidationLevel {
  level: number;
  name: string;
  description: string;
  commands: Array<{
    cmd: string;
    required: boolean;
    continueOnError?: boolean;
  }>;
  mustPassBefore: string;
}

export interface ValidationResult {
  level: number;
  passed: boolean;
  results: Array<{
    command: string;
    success: boolean;
    output?: string;
    error?: string;
  }>;
  duration: number;
}

export class PRPValidationRunner {
  private validationLevels: ValidationLevel[] = [
    {
      level: 1,
      name: 'Syntax & Standards',
      description: 'Code quality and design system compliance',
      commands: [
        { cmd: 'bun run lint:fix', required: true },
        { cmd: 'bun run typecheck', required: true },
        { cmd: 'bun run validate-design', required: true }
      ],
      mustPassBefore: 'Writing any component code'
    },
    {
      level: 2,
      name: 'Component Testing',
      description: 'Unit tests for components and hooks',
      commands: [
        { cmd: 'bun run test:components', required: true },
        { cmd: 'bun run test:hooks', required: false, continueOnError: true }
      ],
      mustPassBefore: 'Integration work'
    },
    {
      level: 3,
      name: 'Integration Testing',
      description: 'API and E2E testing',
      commands: [
        { cmd: 'bun run test:api', required: true },
        { cmd: 'bun run test:e2e', required: true },
        { cmd: 'bun run test:a11y', required: false }
      ],
      mustPassBefore: 'Stage completion'
    },
    {
      level: 4,
      name: 'Production Validation',
      description: 'Performance, security, and final checks',
      commands: [
        { cmd: 'bun run analyze', required: true },
        { cmd: 'bun run security:check', required: true },
        { cmd: 'bun run lighthouse', required: false, continueOnError: true }
      ],
      mustPassBefore: 'Creating PR'
    }
  ];

  constructor(private feature?: string) {}

  /**
   * Run validation for a specific level
   */
  async runLevel(level: number): Promise<ValidationResult> {
    const validationLevel = this.validationLevels.find(v => v.level === level);
    if (!validationLevel) {
      throw new Error(`Validation level ${level} not found`);
    }

    console.log(chalk.blue(`\n🔄 Running Level ${level}: ${validationLevel.name}`));
    console.log(chalk.gray(validationLevel.description));
    console.log(chalk.gray(`Must pass before: ${validationLevel.mustPassBefore}\n`));

    const startTime = Date.now();
    const results = [];
    let allPassed = true;

    for (const { cmd, required, continueOnError } of validationLevel.commands) {
      const fullCmd = this.feature ? cmd.replace('$FEATURE', this.feature) : cmd;
      
      console.log(chalk.gray(`Running: ${fullCmd}`));
      
      try {
        const output = execSync(fullCmd, { 
          encoding: 'utf8',
          stdio: 'pipe'
        });
        
        results.push({
          command: fullCmd,
          success: true,
          output: output.trim()
        });
        
        console.log(chalk.green('✓ Passed'));
      } catch (error: any) {
        const success = continueOnError || false;
        
        results.push({
          command: fullCmd,
          success,
          error: error.message || error.toString()
        });
        
        if (required && !continueOnError) {
          allPassed = false;
          console.log(chalk.red('✗ Failed (required)'));
        } else {
          console.log(chalk.yellow('⚠ Failed (optional)'));
        }
      }
    }

    const duration = Date.now() - startTime;

    return {
      level,
      passed: allPassed,
      results,
      duration
    };
  }

  /**
   * Run all validation levels up to a specified level
   */
  async runUpToLevel(maxLevel: number): Promise<ValidationResult[]> {
    const results: ValidationResult[] = [];
    
    for (let level = 1; level <= maxLevel; level++) {
      const result = await this.runLevel(level);
      results.push(result);
      
      if (!result.passed) {
        console.log(chalk.red(`\n❌ Validation failed at level ${level}`));
        console.log(chalk.yellow('Fix the issues above before proceeding.'));
        break;
      }
    }
    
    return results;
  }

  /**
   * Run validation and check if we can proceed to next stage
   */
  async canProceed(fromLevel: number): Promise<boolean> {
    const result = await this.runLevel(fromLevel);
    
    if (result.passed) {
      console.log(chalk.green(`\n✅ Level ${fromLevel} validation passed!`));
      console.log(chalk.blue(`You can now proceed to: ${this.getNextStage(fromLevel)}`));
      return true;
    } else {
      console.log(chalk.red(`\n❌ Level ${fromLevel} validation failed!`));
      console.log(chalk.yellow('Fix the issues above before proceeding.'));
      return false;
    }
  }

  /**
   * Get validation summary for a PRP
   */
  async getValidationSummary(): Promise<string> {
    const results = await this.runUpToLevel(4);
    
    let summary = '# PRP Validation Summary\n\n';
    
    for (const result of results) {
      const level = this.validationLevels.find(v => v.level === result.level)!;
      const status = result.passed ? '✅' : '❌';
      
      summary += `## Level ${result.level}: ${level.name} ${status}\n`;
      summary += `Duration: ${(result.duration / 1000).toFixed(2)}s\n\n`;
      
      for (const test of result.results) {
        const testStatus = test.success ? '✓' : '✗';
        summary += `- ${testStatus} ${test.command}\n`;
        if (test.error) {
          summary += `  Error: ${test.error.split('\n')[0]}\n`;
        }
      }
      summary += '\n';
    }
    
    const allPassed = results.every(r => r.passed);
    if (allPassed) {
      summary += '## 🎉 All validations passed! Ready for PR.\n';
    } else {
      const failedLevel = results.find(r => !r.passed)?.level || 0;
      summary += `## ⚠️ Validation stopped at level ${failedLevel}. Fix issues before proceeding.\n`;
    }
    
    return summary;
  }

  private getNextStage(level: number): string {
    switch (level) {
      case 1: return 'Component implementation';
      case 2: return 'Integration and API connection';
      case 3: return 'Final polish and optimization';
      case 4: return 'Create PR and deploy';
      default: return 'Next stage';
    }
  }
}

// Export for use in commands
export async function runValidation(
  level?: number,
  feature?: string
): Promise<void> {
  const runner = new PRPValidationRunner(feature);
  
  if (level) {
    await runner.canProceed(level);
  } else {
    const summary = await runner.getValidationSummary();
    console.log(summary);
  }
}
```

## Integration with Commands

```typescript
// .claude/commands/prp-validate.md

# PRP Validation Runner

Run validation loops defined in your PRP.

## Arguments:
- $LEVEL: Validation level (1-4) or 'all'
- $FEATURE: Feature name (optional)

## Examples:
```bash
/prp-validate 1              # Run level 1 validation
/prp-validate 2 auth-system  # Run level 2 for auth-system
/prp-validate all            # Run all levels
```

## Implementation:

```typescript
import { runValidation } from '@/lib/prp/validation-runner';

const args = '$ARGUMENTS'.split(' ');
const level = args[0] === 'all' ? undefined : parseInt(args[0]);
const feature = args[1];

await runValidation(level, feature);
```

## What it does:

1. Runs the validation commands for the specified level
2. Reports pass/fail for each command
3. Stops on required failures
4. Provides clear next steps
5. Integrates with your stage validation system

## Validation Levels:

1️⃣ **Syntax & Standards** (Continuous)
   - Linting
   - Type checking  
   - Design system validation

2️⃣ **Component Testing** (After components)
   - Unit tests
   - Component tests
   - Hook tests

3️⃣ **Integration Testing** (After integration)
   - API tests
   - E2E tests
   - Accessibility tests

4️⃣ **Production Validation** (Before PR)
   - Bundle analysis
   - Security audit
   - Performance checks

## Integration with existing commands:

- Works with `/sv check` for stage validation
- Complements `/grade` for requirement scoring
- Can be triggered by `/pt` after tasks
- Results feed into `/fw complete`
```

## Usage in PRPs

In your PRP documents, reference the validation runner:

```markdown
## Validation Loops

Run validations with: `/prp-validate [level] [feature-name]`

### 🔴 Level 1: Syntax & Standards
```bash
/prp-validate 1 auth-system
```

### 🟡 Level 2: Component Testing  
```bash
/prp-validate 2 auth-system
```

### 🟢 Level 3: Integration Testing
```bash
/prp-validate 3 auth-system
```

### 🔵 Level 4: Production Validation
```bash
/prp-validate 4 auth-system
```

### Run all validations:
```bash
/prp-validate all auth-system
```
```

## Benefits

1. **Automated validation execution** - No manual command running
2. **Clear pass/fail criteria** - Know exactly what needs fixing
3. **Progressive validation** - Can't skip ahead without passing earlier levels
4. **Integration with existing system** - Works with your current commands
5. **Actionable feedback** - Clear next steps after each validation
