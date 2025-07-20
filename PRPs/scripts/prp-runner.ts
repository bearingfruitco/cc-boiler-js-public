#!/usr/bin/env bun
/**
 * PRP Runner - Execute PRPs with validation loops
 * Provides automation capabilities for Product Requirement Prompts
 */

import { parseArgs } from "util";
import { existsSync, readFileSync, writeFileSync, mkdirSync } from "fs";
import { join, dirname } from "path";
import { execSync } from "child_process";

interface PRPMetadata {
  name: string;
  confidence: number;
  created: string;
  validationLevels: {
    level1: string[];
    level2: string[];
    level3: string[];
    level4: string[];
  };
}

interface ExecutionResult {
  success: boolean;
  level: number;
  duration: number;
  output: string;
  errors?: string[];
}

class PRPRunner {
  private prpPath: string;
  private prpContent: string;
  private metadata: PRPMetadata;
  private interactive: boolean;
  private fixMode: boolean;
  private level?: number;

  constructor(prpName: string, options: any) {
    this.prpPath = this.findPRP(prpName);
    this.prpContent = readFileSync(this.prpPath, "utf-8");
    this.metadata = this.extractMetadata();
    this.interactive = options.interactive || false;
    this.fixMode = options.fix || false;
    this.level = options.level;
  }

  private findPRP(name: string): string {
    const locations = [
      `PRPs/active/${name}.md`,
      `PRPs/active/${name}`,
      `PRPs/${name}.md`,
      `PRPs/${name}`,
    ];

    for (const loc of locations) {
      if (existsSync(loc)) {
        return loc;
      }
    }

    throw new Error(`PRP not found: ${name}`);
  }

  private extractMetadata(): PRPMetadata {
    const metadata: PRPMetadata = {
      name: this.prpPath.split("/").pop()?.replace(".md", "") || "unknown",
      confidence: this.extractConfidence(),
      created: new Date().toISOString(),
      validationLevels: this.extractValidationCommands(),
    };

    return metadata;
  }

  private extractConfidence(): number {
    const match = this.prpContent.match(/Confidence.*?(\d+)\/10/i);
    return match ? parseInt(match[1]) : 0;
  }

  private extractValidationCommands(): any {
    const levels: any = {
      level1: [],
      level2: [],
      level3: [],
      level4: [],
    };

    // Extract Level 1 commands
    const level1Match = this.prpContent.match(
      /Level 1:.*?```(?:bash)?\n([\s\S]*?)```/i
    );
    if (level1Match) {
      levels.level1 = level1Match[1]
        .split("\n")
        .filter((cmd) => cmd.trim())
        .map((cmd) => cmd.trim());
    }

    // Similar for other levels
    const level2Match = this.prpContent.match(
      /Level 2:.*?```(?:bash)?\n([\s\S]*?)```/i
    );
    if (level2Match) {
      levels.level2 = level2Match[1]
        .split("\n")
        .filter((cmd) => cmd.trim())
        .map((cmd) => cmd.trim());
    }

    const level3Match = this.prpContent.match(
      /Level 3:.*?```(?:bash)?\n([\s\S]*?)```/i
    );
    if (level3Match) {
      levels.level3 = level3Match[1]
        .split("\n")
        .filter((cmd) => cmd.trim())
        .map((cmd) => cmd.trim());
    }

    const level4Match = this.prpContent.match(
      /Level 4:.*?```(?:bash)?\n([\s\S]*?)```/i
    );
    if (level4Match) {
      levels.level4 = level4Match[1]
        .split("\n")
        .filter((cmd) => cmd.trim())
        .map((cmd) => cmd.trim());
    }

    return levels;
  }

  async execute(): Promise<void> {
    console.log(`🚀 Executing PRP: ${this.metadata.name}`);
    console.log(`📊 Confidence Score: ${this.metadata.confidence}/10`);
    console.log(`🔧 Mode: ${this.interactive ? "Interactive" : "Automated"}`);
    console.log("-".repeat(50));

    const results: ExecutionResult[] = [];

    // Run specified level or all levels
    const levelsToRun = this.level
      ? [this.level]
      : [1, 2, 3, 4];

    for (const level of levelsToRun) {
      const result = await this.runValidationLevel(level);
      results.push(result);

      if (!result.success && this.interactive) {
        const shouldContinue = await this.promptContinue(level);
        if (!shouldContinue) break;
      } else if (!result.success && !this.interactive) {
        break; // Stop on first failure in non-interactive mode
      }
    }

    this.saveResults(results);
    this.printSummary(results);
  }

  private async runValidationLevel(level: number): Promise<ExecutionResult> {
    const levelKey = `level${level}` as keyof typeof this.metadata.validationLevels;
    const commands = this.metadata.validationLevels[levelKey];

    if (!commands || commands.length === 0) {
      return {
        success: true,
        level,
        duration: 0,
        output: "No commands defined for this level",
      };
    }

    console.log(`\n🔍 Running Level ${level} Validation...`);
    const startTime = Date.now();
    const errors: string[] = [];
    let allPassed = true;

    for (const command of commands) {
      console.log(`  $ ${command}`);
      
      try {
        const output = execSync(command, { encoding: "utf-8" });
        console.log("  ✅ Passed");
        
        if (this.fixMode && command.includes("--fix")) {
          console.log("  🔧 Applied fixes");
        }
      } catch (error: any) {
        console.log("  ❌ Failed");
        errors.push(`${command}: ${error.message}`);
        allPassed = false;
        
        if (this.fixMode && this.canAutoFix(command)) {
          const fixed = await this.attemptAutoFix(command);
          if (fixed) {
            console.log("  🔧 Auto-fixed and retrying...");
            try {
              execSync(command, { encoding: "utf-8" });
              console.log("  ✅ Passed after fix");
              allPassed = true;
            } catch {
              allPassed = false;
            }
          }
        }
      }
    }

    const duration = Date.now() - startTime;

    return {
      success: allPassed,
      level,
      duration,
      output: allPassed ? "All validations passed" : "Some validations failed",
      errors: errors.length > 0 ? errors : undefined,
    };
  }

  private canAutoFix(command: string): boolean {
    return command.includes("lint") || 
           command.includes("format") || 
           command.includes("typecheck");
  }

  private async attemptAutoFix(command: string): Promise<boolean> {
    const fixCommands: Record<string, string> = {
      "bun run lint": "bun run lint:fix",
      "bun run typecheck": "bun run typecheck --fix",
      "bun run format": "bun run format:fix",
    };

    const fixCommand = fixCommands[command];
    if (!fixCommand) return false;

    try {
      execSync(fixCommand, { encoding: "utf-8" });
      return true;
    } catch {
      return false;
    }
  }

  private async promptContinue(level: number): Promise<boolean> {
    console.log(`\n⚠️  Level ${level} validation failed.`);
    console.log("Continue to next level? (y/n): ");
    
    // In Bun, we can use prompt
    const answer = prompt("") || "n";
    return answer.toLowerCase() === "y";
  }

  private saveResults(results: ExecutionResult[]): void {
    const logsDir = "PRPs/execution_logs";
    if (!existsSync(logsDir)) {
      mkdirSync(logsDir, { recursive: true });
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
    const logFile = join(logsDir, `${this.metadata.name}_${timestamp}.json`);

    const logData = {
      prp: this.metadata.name,
      confidence: this.metadata.confidence,
      executed: new Date().toISOString(),
      mode: this.interactive ? "interactive" : "automated",
      results,
      totalDuration: results.reduce((sum, r) => sum + r.duration, 0),
      success: results.every((r) => r.success),
    };

    writeFileSync(logFile, JSON.stringify(logData, null, 2));
    console.log(`\n📁 Execution log saved: ${logFile}`);
  }

  private printSummary(results: ExecutionResult[]): void {
    console.log("\n" + "=".repeat(50));
    console.log("📊 EXECUTION SUMMARY");
    console.log("=".repeat(50));

    for (const result of results) {
      const status = result.success ? "✅" : "❌";
      console.log(`${status} Level ${result.level}: ${result.output} (${result.duration}ms)`);
      
      if (result.errors) {
        for (const error of result.errors) {
          console.log(`   └─ ${error}`);
        }
      }
    }

    const totalDuration = results.reduce((sum, r) => sum + r.duration, 0);
    const allPassed = results.every((r) => r.success);

    console.log("\n" + "-".repeat(50));
    console.log(`Total Duration: ${totalDuration}ms`);
    console.log(`Overall Result: ${allPassed ? "✅ PASSED" : "❌ FAILED"}`);
    
    if (!allPassed) {
      console.log("\n💡 Suggestions:");
      console.log("- Review the failed validations");
      console.log("- Run with --fix flag to attempt auto-fixes");
      console.log("- Check /prp-status for detailed progress");
    }
  }
}

// Main execution
async function main() {
  const { values, positionals } = parseArgs({
    args: Bun.argv,
    options: {
      prp: {
        type: "string",
      },
      interactive: {
        type: "boolean",
        default: false,
      },
      fix: {
        type: "boolean",
        default: false,
      },
      level: {
        type: "string",
      },
      help: {
        type: "boolean",
        default: false,
      },
    },
    strict: true,
    allowPositionals: true,
  });

  if (values.help || !values.prp) {
    console.log(`
PRP Runner - Execute Product Requirement Prompts with validation

Usage: bun run prp-runner.ts --prp <name> [options]

Options:
  --prp <name>      Name of the PRP to execute (required)
  --interactive     Run in interactive mode with prompts
  --fix             Attempt to auto-fix validation failures
  --level <n>       Run specific validation level (1-4)
  --help            Show this help message

Examples:
  bun run prp-runner.ts --prp user-auth
  bun run prp-runner.ts --prp payment --level 1 --fix
  bun run prp-runner.ts --prp checkout --interactive
    `);
    process.exit(values.help ? 0 : 1);
  }

  try {
    const runner = new PRPRunner(values.prp, {
      interactive: values.interactive,
      fix: values.fix,
      level: values.level ? parseInt(values.level) : undefined,
    });

    await runner.execute();
  } catch (error: any) {
    console.error(`\n❌ Error: ${error.message}`);
    process.exit(1);
  }
}

// Run if executed directly
if (import.meta.main) {
  main();
}