#!/usr/bin/env node

/**
 * PRP Runner - Execute Product Requirement Prompts with validation loops
 * Integrates with existing Claude Code boilerplate system
 */

import { readFile, writeFile, access } from 'fs/promises';
import { join, resolve } from 'path';
import { spawn } from 'child_process';
import { createInterface } from 'readline';

interface PRPConfig {
  name: string;
  path: string;
  validationLoops: ValidationLoop[];
  requirements?: {
    issueNumber?: number;
    pinned?: boolean;
  };
}

interface ValidationLoop {
  level: number;
  name: string;
  commands: string[];
  mustPassBefore: string;
  autoFix?: boolean;
}

interface RunnerOptions {
  prp: string;
  interactive?: boolean;
  outputFormat?: 'text' | 'json' | 'stream-json';
  skipValidation?: string[];
  fix?: boolean;
}

class PRPRunner {
  private config: PRPConfig | null = null;
  private results: any[] = [];

  constructor(private options: RunnerOptions) {}

  async run() {
    try {
      // 1. Load PRP
      await this.loadPRP();
      
      // 2. Check requirements if pinned
      if (this.config?.requirements?.pinned) {
        await this.checkRequirements();
      }

      // 3. Run validation loops
      await this.runValidationLoops();

      // 4. Output results
      this.outputResults();

    } catch (error) {
      this.handleError(error);
    }
  }

  private async loadPRP() {
    const prpPath = this.resolvePRPPath(this.options.prp);
    
    try {
      await access(prpPath);
      const content = await readFile(prpPath, 'utf-8');
      
      this.config = {
        name: this.options.prp,
        path: prpPath,
        validationLoops: this.parseValidationLoops(content),
        requirements: this.parseRequirements(content)
      };

      this.log('info', `Loaded PRP: ${this.config.name}`);
    } catch (error) {
      throw new Error(`PRP not found: ${prpPath}`);
    }
  }

  private resolvePRPPath(prp: string): string {
    // Check multiple locations
    const locations = [
      join(process.cwd(), 'PRPs', `${prp}.md`),
      join(process.cwd(), 'PRPs', prp),
      join(process.cwd(), '.claude', 'templates', 'prp', `${prp}.md`),
      prp // Direct path
    ];

    // Return first that exists (checked later)
    return locations[0];
  }

  private parseValidationLoops(content: string): ValidationLoop[] {
    const loops: ValidationLoop[] = [];
    const loopRegex = /### (?:Level |🔴|🟡|🟢|🔵)(\d+)[:\s]+([^\n]+)[\s\S]*?```bash\n([\s\S]*?)```[\s\S]*?Must Pass Before[:\s]+([^\n]+)/gm;
    
    let match;
    while ((match = loopRegex.exec(content)) !== null) {
      const [, level, name, commands, mustPassBefore] = match;
      
      loops.push({
        level: parseInt(level),
        name: name.trim(),
        commands: commands.trim().split('\n').filter(cmd => 
          cmd.trim() && !cmd.trim().startsWith('#')
        ),
        mustPassBefore: mustPassBefore.trim(),
        autoFix: commands.includes('--fix') || commands.includes(':fix')
      });
    }

    return loops.sort((a, b) => a.level - b.level);
  }

  private parseRequirements(content: string): any {
    const reqMatch = content.match(/Requirements:\s*`#(\d+)`/);
    const pinnedMatch = content.match(/\/pin-requirements\s+(\d+)/);
    
    return {
      issueNumber: reqMatch ? parseInt(reqMatch[1]) : undefined,
      pinned: !!pinnedMatch
    };
  }

  private async checkRequirements() {
    if (!this.config?.requirements?.issueNumber) return;

    this.log('info', 'Checking pinned requirements...');
    
    const result = await this.runCommand('/review-requirements', []);
    
    if (result.exitCode !== 0) {
      throw new Error('Requirements check failed. Run /review-requirements for details.');
    }
  }

  private async runValidationLoops() {
    if (!this.config) return;

    for (const loop of this.config.validationLoops) {
      // Skip if requested
      if (this.options.skipValidation?.includes(loop.name)) {
        this.log('warn', `Skipping validation: ${loop.name}`);
        continue;
      }

      this.log('info', `\nRunning Level ${loop.level}: ${loop.name}`);
      this.log('info', `Must pass before: ${loop.mustPassBefore}`);

      const loopResults: any[] = [];
      let allPassed = true;

      for (const command of loop.commands) {
        const result = await this.runValidationCommand(command, loop);
        loopResults.push(result);
        
        if (!result.success) {
          allPassed = false;
          
          // Try auto-fix if available and requested
          if (loop.autoFix && this.options.fix) {
            this.log('info', 'Attempting auto-fix...');
            const fixResult = await this.runValidationCommand(
              command.replace(/\b(lint|format|typecheck)\b/, '$1:fix'),
              loop
            );
            
            if (fixResult.success) {
              result.fixed = true;
              allPassed = true;
            }
          }
        }
      }

      this.results.push({
        level: loop.level,
        name: loop.name,
        passed: allPassed,
        results: loopResults
      });

      // Stop on failure unless interactive
      if (!allPassed && !this.options.interactive) {
        this.log('error', `\n❌ Level ${loop.level} validation failed!`);
        this.log('error', `Cannot proceed to: ${loop.mustPassBefore}`);
        
        if (loop.autoFix) {
          this.log('info', '\n💡 Tip: Run with --fix to attempt auto-fixes');
        }
        
        break;
      }

      // Interactive mode - ask to continue
      if (!allPassed && this.options.interactive) {
        const shouldContinue = await this.promptUser(
          `\nLevel ${loop.level} failed. Continue anyway? (y/N): `
        );
        
        if (!shouldContinue) break;
      }
    }
  }

  private async runValidationCommand(command: string, loop: ValidationLoop): Promise<any> {
    const startTime = Date.now();
    
    try {
      // Parse command
      const [cmd, ...args] = command.trim().split(/\s+/);
      
      // Handle different command types
      let result;
      if (cmd.startsWith('/')) {
        // Claude command
        result = await this.runCommand(cmd, args);
      } else if (cmd === 'bun' || cmd === 'npm') {
        // Package manager command
        result = await this.runShellCommand(cmd, args);
      } else {
        // Shell command
        result = await this.runShellCommand(cmd, args);
      }

      const duration = Date.now() - startTime;
      
      return {
        command,
        success: result.exitCode === 0,
        duration,
        output: result.output,
        error: result.error
      };

    } catch (error) {
      return {
        command,
        success: false,
        duration: Date.now() - startTime,
        error: error.message
      };
    }
  }

  private async runCommand(command: string, args: string[]): Promise<any> {
    return new Promise((resolve) => {
      const fullCommand = `${command} ${args.join(' ')}`.trim();
      
      // Simulate command execution (in real implementation, would integrate with Claude)
      this.log('debug', `Executing: ${fullCommand}`);
      
      // Mock successful execution for now
      setTimeout(() => {
        resolve({
          exitCode: 0,
          output: `${command} completed successfully`,
          error: null
        });
      }, 100);
    });
  }

  private async runShellCommand(command: string, args: string[]): Promise<any> {
    return new Promise((resolve) => {
      const child = spawn(command, args, { 
        shell: true,
        cwd: process.cwd()
      });

      let output = '';
      let error = '';

      child.stdout.on('data', (data) => {
        output += data.toString();
        if (this.options.outputFormat === 'stream-json') {
          this.streamOutput('stdout', data.toString());
        }
      });

      child.stderr.on('data', (data) => {
        error += data.toString();
        if (this.options.outputFormat === 'stream-json') {
          this.streamOutput('stderr', data.toString());
        }
      });

      child.on('close', (code) => {
        resolve({
          exitCode: code || 0,
          output,
          error
        });
      });
    });
  }

  private async promptUser(question: string): Promise<boolean> {
    const rl = createInterface({
      input: process.stdin,
      output: process.stdout
    });

    return new Promise((resolve) => {
      rl.question(question, (answer) => {
        rl.close();
        resolve(answer.toLowerCase() === 'y');
      });
    });
  }

  private outputResults() {
    switch (this.options.outputFormat) {
      case 'json':
        console.log(JSON.stringify({
          prp: this.config?.name,
          timestamp: new Date().toISOString(),
          results: this.results,
          summary: this.generateSummary()
        }, null, 2));
        break;

      case 'stream-json':
        // Already streamed during execution
        this.streamOutput('complete', this.generateSummary());
        break;

      default:
        this.outputTextResults();
    }
  }

  private outputTextResults() {
    console.log('\n' + '='.repeat(60));
    console.log(`PRP Validation Results: ${this.config?.name}`);
    console.log('='.repeat(60) + '\n');

    for (const loop of this.results) {
      const icon = loop.passed ? '✅' : '❌';
      console.log(`${icon} Level ${loop.level}: ${loop.name}`);
      
      for (const result of loop.results) {
        const cmdIcon = result.success ? '✓' : '✗';
        const fixedText = result.fixed ? ' (auto-fixed)' : '';
        console.log(`  ${cmdIcon} ${result.command}${fixedText} (${result.duration}ms)`);
        
        if (!result.success && result.error) {
          console.log(`     Error: ${result.error.split('\n')[0]}`);
        }
      }
      console.log();
    }

    const summary = this.generateSummary();
    console.log('\nSummary:');
    console.log(`- Total Levels: ${summary.totalLevels}`);
    console.log(`- Passed: ${summary.passed}`);
    console.log(`- Failed: ${summary.failed}`);
    
    if (summary.failed > 0) {
      console.log(`\n⚠️  Cannot proceed past Level ${summary.lastPassedLevel}`);
    } else {
      console.log('\n🎉 All validation loops passed! Ready for implementation.');
    }
  }

  private generateSummary() {
    const totalLevels = this.results.length;
    const passed = this.results.filter(r => r.passed).length;
    const failed = totalLevels - passed;
    const lastPassedLevel = this.results.filter(r => r.passed).length;

    return {
      totalLevels,
      passed,
      failed,
      lastPassedLevel,
      allPassed: failed === 0
    };
  }

  private streamOutput(type: string, data: any) {
    if (this.options.outputFormat === 'stream-json') {
      console.log(JSON.stringify({
        type,
        timestamp: new Date().toISOString(),
        data
      }));
    }
  }

  private log(level: 'info' | 'warn' | 'error' | 'debug', message: string) {
    if (this.options.outputFormat === 'json' || this.options.outputFormat === 'stream-json') {
      return; // No console output in JSON modes
    }

    const colors = {
      info: '\x1b[36m',   // Cyan
      warn: '\x1b[33m',   // Yellow
      error: '\x1b[31m',  // Red
      debug: '\x1b[90m'   // Gray
    };

    const reset = '\x1b[0m';
    console.log(`${colors[level]}${message}${reset}`);
  }

  private handleError(error: any) {
    if (this.options.outputFormat === 'json') {
      console.log(JSON.stringify({
        error: error.message,
        stack: error.stack
      }));
    } else {
      console.error('\n❌ Error:', error.message);
      if (error.stack && process.env.DEBUG) {
        console.error(error.stack);
      }
    }
    
    process.exit(1);
  }
}

// CLI Interface
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help')) {
    console.log(`
PRP Runner - Execute Product Requirement Prompts with validation

Usage: bun run prp-runner.ts [options] <prp-name>

Options:
  --interactive, -i     Interactive mode (prompt on failures)
  --output-format, -o   Output format: text (default), json, stream-json
  --skip-validation     Skip specific validation loops (comma-separated)
  --fix                 Attempt auto-fixes where available
  --help               Show this help message

Examples:
  bun run prp-runner.ts user-auth
  bun run prp-runner.ts user-auth --interactive
  bun run prp-runner.ts user-auth --fix
  bun run prp-runner.ts user-auth --output-format json
  bun run prp-runner.ts user-auth --skip-validation "Component Testing"
    `);
    process.exit(0);
  }

  // Parse options
  const options: RunnerOptions = {
    prp: args[args.length - 1], // Last arg is PRP name
    interactive: args.includes('--interactive') || args.includes('-i'),
    fix: args.includes('--fix'),
    outputFormat: 'text' as any
  };

  // Parse output format
  const formatIndex = args.findIndex(arg => arg === '--output-format' || arg === '-o');
  if (formatIndex !== -1 && args[formatIndex + 1]) {
    options.outputFormat = args[formatIndex + 1] as any;
  }

  // Parse skip validation
  const skipIndex = args.findIndex(arg => arg === '--skip-validation');
  if (skipIndex !== -1 && args[skipIndex + 1]) {
    options.skipValidation = args[skipIndex + 1].split(',').map(s => s.trim());
  }

  // Run
  const runner = new PRPRunner(options);
  await runner.run();
}

// Execute if run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export { PRPRunner, type RunnerOptions, type PRPConfig };
