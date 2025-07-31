#!/usr/bin/env node

import { Command } from 'commander';
import { ArchitectureChangeTracker } from './tracker';
import { 
  ArchitectureChangeType, 
  ChangeCategory,
  ChangeImpact 
} from './types';
import chalk from 'chalk';
import inquirer from 'inquirer';
import { table } from 'table';

const program = new Command();
const tracker = new ArchitectureChangeTracker(process.cwd());

program
  .name('architecture-tracker')
  .description('Track and manage architecture changes')
  .version('1.0.0');

// Initialize command
program
  .command('init')
  .description('Initialize architecture tracking in the current project')
  .action(async () => {
    try {
      await tracker.initialize();
      console.log(chalk.green('✓ Architecture tracking initialized successfully'));
    } catch (error) {
      console.error(chalk.red('Error initializing architecture tracking:'), error);
      process.exit(1);
    }
  });

// Record change command
program
  .command('record')
  .description('Record a new architecture change')
  .option('-i, --interactive', 'Use interactive mode')
  .action(async (options) => {
    try {
      let changeData: any = {};

      if (options.interactive) {
        const answers = await inquirer.prompt([
          {
            type: 'list',
            name: 'type',
            message: 'What type of change is this?',
            choices: Object.values(ArchitectureChangeType).map(type => ({
              name: formatChangeType(type),
              value: type
            }))
          },
          {
            type: 'list',
            name: 'category',
            message: 'Which category does this change belong to?',
            choices: Object.values(ChangeCategory)
          },
          {
            type: 'input',
            name: 'description',
            message: 'Provide a brief description of the change:'
          },
          {
            type: 'input',
            name: 'rationale',
            message: 'Why is this change being made?'
          },
          {
            type: 'input',
            name: 'filesAffected',
            message: 'Which files are affected? (comma-separated)'
          },
          {
            type: 'input',
            name: 'components',
            message: 'Which components are impacted? (comma-separated)'
          },
          {
            type: 'list',
            name: 'estimatedEffort',
            message: 'What is the estimated effort?',
            choices: ['low', 'medium', 'high']
          },
          {
            type: 'confirm',
            name: 'breakingChange',
            message: 'Is this a breaking change?',
            default: false
          },
          {
            type: 'confirm',
            name: 'securityImpact',
            message: 'Does this have security implications?',
            default: false
          },
          {
            type: 'input',
            name: 'relatedPRP',
            message: 'Related PRP (optional):'
          }
        ]);

        changeData = {
          type: answers.type,
          category: answers.category,
          description: answers.description,
          filesAffected: answers.filesAffected.split(',').map((f: string) => f.trim()).filter(Boolean),
          relatedPRP: answers.relatedPRP || undefined,
          author: process.env.USER || 'unknown',
          rationale: answers.rationale,
          impact: {
            components: answers.components.split(',').map((c: string) => c.trim()).filter(Boolean),
            estimatedEffort: answers.estimatedEffort,
            breakingChange: answers.breakingChange,
            securityImpact: answers.securityImpact || undefined
          }
        };
      } else {
        console.error(chalk.red('Non-interactive mode not yet implemented. Use --interactive flag.'));
        process.exit(1);
      }

      const change = await tracker.recordChange(changeData);
      console.log(chalk.green(`✓ Architecture change recorded: ${change.id}`));
      
      // Show summary
      console.log('\n' + chalk.bold('Change Summary:'));
      console.log(`Type: ${formatChangeType(change.type)}`);
      console.log(`Category: ${change.category}`);
      console.log(`Description: ${change.description}`);
      console.log(`Impact: ${change.impact.estimatedEffort} effort, affects ${change.impact.components.length} components`);
      
    } catch (error) {
      console.error(chalk.red('Error recording change:'), error);
      process.exit(1);
    }
  });

// List changes command
program
  .command('list')
  .description('List architecture changes')
  .option('-s, --since <date>', 'Show changes since date')
  .option('-u, --until <date>', 'Show changes until date')
  .option('-c, --category <category>', 'Filter by category')
  .option('--component <component>', 'Show changes affecting a component')
  .action(async (options) => {
    try {
      let changes;

      if (options.component) {
        changes = await tracker.getChangesForComponent(options.component);
      } else if (options.category) {
        changes = await tracker.getChangesByCategory(options.category as ChangeCategory);
      } else {
        const since = options.since ? new Date(options.since) : undefined;
        const until = options.until ? new Date(options.until) : undefined;
        changes = await tracker.getChanges(since, until);
      }

      if (changes.length === 0) {
        console.log(chalk.yellow('No changes found matching the criteria.'));
        return;
      }

      // Display changes in a table
      const tableData = [
        ['ID', 'Date', 'Type', 'Category', 'Description', 'Impact']
      ];

      for (const change of changes) {
        tableData.push([
          change.id.substring(0, 20) + '...',
          new Date(change.timestamp).toLocaleDateString(),
          formatChangeType(change.type).substring(0, 20),
          change.category,
          change.description.substring(0, 40) + '...',
          `${change.impact.estimatedEffort} (${change.impact.components.length} components)`
        ]);
      }

      console.log(table(tableData));
      console.log(`\nTotal changes: ${changes.length}`);

    } catch (error) {
      console.error(chalk.red('Error listing changes:'), error);
      process.exit(1);
    }
  });

// Impact analysis command
program
  .command('impact')
  .description('Analyze the impact of a proposed change')
  .option('-i, --interactive', 'Use interactive mode')
  .action(async (options) => {
    try {
      if (!options.interactive) {
        console.error(chalk.red('Impact analysis requires interactive mode. Use --interactive flag.'));
        process.exit(1);
      }

      // Collect change information
      const answers = await inquirer.prompt([
        {
          type: 'list',
          name: 'type',
          message: 'What type of change are you proposing?',
          choices: Object.values(ArchitectureChangeType).map(type => ({
            name: formatChangeType(type),
            value: type
          }))
        },
        {
          type: 'list',
          name: 'category',
          message: 'Which category?',
          choices: Object.values(ChangeCategory)
        },
        {
          type: 'input',
          name: 'description',
          message: 'Describe the proposed change:'
        },
        {
          type: 'input',
          name: 'components',
          message: 'Which components would be affected? (comma-separated)'
        },
        {
          type: 'list',
          name: 'estimatedEffort',
          message: 'Estimated effort?',
          choices: ['low', 'medium', 'high']
        },
        {
          type: 'confirm',
          name: 'breakingChange',
          message: 'Would this be a breaking change?'
        }
      ]);

      const proposedChange = {
        type: answers.type,
        category: answers.category,
        description: answers.description,
        filesAffected: [],
        author: process.env.USER || 'unknown',
        rationale: '',
        impact: {
          components: answers.components.split(',').map((c: string) => c.trim()).filter(Boolean),
          estimatedEffort: answers.estimatedEffort as 'low' | 'medium' | 'high',
          breakingChange: answers.breakingChange
        }
      };

      const report = await tracker.generateImpactReport(proposedChange);

      // Display impact report
      console.log('\n' + chalk.bold('Impact Analysis Report'));
      console.log('='.repeat(50));
      
      console.log(chalk.bold('\nProposed Change:'));
      console.log(`Type: ${formatChangeType(proposedChange.type)}`);
      console.log(`Description: ${proposedChange.description}`);
      
      console.log(chalk.bold('\nRisk Assessment:'));
      const riskColor = report.riskScore > 20 ? chalk.red : report.riskScore > 10 ? chalk.yellow : chalk.green;
      console.log(`Risk Score: ${riskColor(report.riskScore + '/30')}`);
      
      console.log(chalk.bold('\nAffected Components:'));
      report.affectedComponents.forEach(comp => console.log(`  - ${comp}`));
      
      if (report.conflicts.length > 0) {
        console.log(chalk.bold('\n⚠️  Conflicts Detected:'));
        report.conflicts.forEach(conflict => {
          const color = conflict.severity === 'high' ? chalk.red : conflict.severity === 'medium' ? chalk.yellow : chalk.white;
          console.log(color(`  - [${conflict.severity.toUpperCase()}] ${conflict.description}`));
        });
      }
      
      if (report.relatedChanges.length > 0) {
        console.log(chalk.bold('\nRelated Recent Changes:'));
        report.relatedChanges.slice(0, 5).forEach(change => {
          console.log(`  - ${change.id}: ${change.description}`);
        });
      }
      
      console.log(chalk.bold('\nRecommendations:'));
      report.recommendations.forEach(rec => console.log(`  • ${rec}`));

    } catch (error) {
      console.error(chalk.red('Error generating impact report:'), error);
      process.exit(1);
    }
  });

// Generate ADR command
program
  .command('adr <changeId>')
  .description('Generate an Architecture Decision Record for a change')
  .action(async (changeId) => {
    try {
      const adrPath = await tracker.createADR(changeId);
      console.log(chalk.green(`✓ ADR created: ${adrPath}`));
    } catch (error) {
      console.error(chalk.red('Error creating ADR:'), error);
      process.exit(1);
    }
  });

// Diff command
program
  .command('diff')
  .description('Show architecture differences between two dates')
  .requiredOption('-f, --from <date>', 'From date')
  .requiredOption('-t, --to <date>', 'To date')
  .action(async (options) => {
    try {
      const fromDate = new Date(options.from);
      const toDate = new Date(options.to);
      
      const diff = await tracker.generateDiff(fromDate, toDate);
      
      console.log(chalk.bold(`\nArchitecture Changes from ${fromDate.toLocaleDateString()} to ${toDate.toLocaleDateString()}`));
      console.log('='.repeat(70));
      
      // Component changes
      if (diff.componentChanges.length > 0) {
        console.log(chalk.bold('\nComponent Changes:'));
        diff.componentChanges.forEach(change => {
          const symbol = change.type === 'added' ? '+' : change.type === 'removed' ? '-' : '~';
          const color = change.type === 'added' ? chalk.green : change.type === 'removed' ? chalk.red : chalk.yellow;
          console.log(color(`  ${symbol} ${change.component.name}`));
        });
      }
      
      // API changes
      if (diff.apiChanges.length > 0) {
        console.log(chalk.bold('\nAPI Changes:'));
        diff.apiChanges.forEach(change => {
          const symbol = change.type === 'added' ? '+' : change.type === 'removed' ? '-' : '~';
          const color = change.type === 'added' ? chalk.green : change.type === 'removed' ? chalk.red : chalk.yellow;
          console.log(color(`  ${symbol} ${change.api.method} ${change.api.path}`));
        });
      }
      
      // Add more diff sections as needed
      
    } catch (error) {
      console.error(chalk.red('Error generating diff:'), error);
      process.exit(1);
    }
  });

// Helper function to format change types
function formatChangeType(type: ArchitectureChangeType): string {
  return type.split('_').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
  ).join(' ');
}

program.parse();
