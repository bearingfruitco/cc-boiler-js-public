#!/usr/bin/env node

import { Command } from 'commander';
import { PRPRegenerator } from './regenerator';
import chalk from 'chalk';
import inquirer from 'inquirer';
import { table } from 'table';
import { RegenerationOptions } from './types';

const program = new Command();
const regenerator = new PRPRegenerator(process.cwd());

program
  .name('prp-sync')
  .description('Synchronize PRPs with architecture changes')
  .version('1.0.0');

// Check status command
program
  .command('status')
  .description('Check PRP synchronization status')
  .action(async () => {
    try {
      console.log(chalk.blue('Checking PRP synchronization status...\n'));
      
      const status = await regenerator.checkSyncStatus();
      
      // Display summary
      console.log(chalk.bold('PRP Sync Status'));
      console.log('='.repeat(50));
      console.log(`Total PRPs: ${status.totalPRPs}`);
      console.log(`Synced: ${chalk.green(status.syncedPRPs)}`);
      console.log(`Outdated: ${chalk.yellow(status.outdatedPRPs.length)}`);
      console.log(`Missing: ${chalk.red(status.missingPRPs.length)}`);
      
      // Show outdated PRPs
      if (status.outdatedPRPs.length > 0) {
        console.log('\n' + chalk.yellow('Outdated PRPs:'));
        status.outdatedPRPs.forEach(prp => {
          console.log(`  - ${prp}`);
        });
      }
      
      // Show missing PRPs
      if (status.missingPRPs.length > 0) {
        console.log('\n' + chalk.red('Missing PRPs (new components):'));
        status.missingPRPs.forEach(prp => {
          console.log(`  - ${prp}`);
        });
      }
      
      if (status.outdatedPRPs.length > 0) {
        console.log('\n' + chalk.cyan('Run "prp-sync update" to synchronize outdated PRPs'));
      }
      
    } catch (error) {
      console.error(chalk.red('Error checking status:'), error);
      process.exit(1);
    }
  });

// Analyze command
program
  .command('analyze')
  .description('Analyze which PRPs need updates based on architecture changes')
  .option('-s, --since <date>', 'Analyze changes since date')
  .action(async (options) => {
    try {
      const since = options.since ? new Date(options.since) : undefined;
      
      console.log(chalk.blue('Analyzing architecture changes...\n'));
      
      const tasks = await regenerator.analyzeImpact(since);
      
      if (tasks.length === 0) {
        console.log(chalk.green('✓ All PRPs are up to date!'));
        return;
      }
      
      // Display tasks in table
      const tableData = [
        ['PRP', 'Component', 'Priority', 'Reason']
      ];
      
      tasks.forEach(task => {
        const priorityColor = task.priority === 'high' ? chalk.red : 
                            task.priority === 'medium' ? chalk.yellow : 
                            chalk.green;
        
        tableData.push([
          task.prpFile,
          task.component,
          priorityColor(task.priority.toUpperCase()),
          task.reason.substring(0, 50) + '...'
        ]);
      });
      
      console.log(table(tableData));
      console.log(`\nFound ${tasks.length} PRPs requiring updates`);
      
      // Show architecture changes
      console.log('\n' + chalk.bold('Architecture Changes Detected:'));
      tasks.forEach(task => {
        console.log(`\n${chalk.underline(task.component)}:`);
        task.architectureChanges.forEach(change => {
          const symbol = change.type === 'added' ? '+' : 
                        change.type === 'removed' ? '-' : '~';
          const color = change.type === 'added' ? chalk.green : 
                       change.type === 'removed' ? chalk.red : chalk.yellow;
          console.log(color(`  ${symbol} ${change.description}`));
        });
      });
      
    } catch (error) {
      console.error(chalk.red('Error analyzing impact:'), error);
      process.exit(1);
    }
  });

// Update command
program
  .command('update')
  .description('Update PRPs based on architecture changes')
  .option('-i, --interactive', 'Interactive mode to select PRPs')
  .option('-a, --all', 'Update all outdated PRPs')
  .option('-d, --dry-run', 'Show what would be updated without making changes')
  .option('--no-backup', 'Skip creating backups')
  .option('--no-preserve', 'Don\'t preserve completion status')
  .action(async (options) => {
    try {
      const tasks = await regenerator.analyzeImpact();
      
      if (tasks.length === 0) {
        console.log(chalk.green('✓ All PRPs are up to date!'));
        return;
      }
      
      let selectedTasks = tasks;
      
      // Interactive selection
      if (options.interactive && !options.all) {
        const choices = tasks.map(task => ({
          name: `${task.prpFile} (${task.priority}) - ${task.reason}`,
          value: task,
          checked: task.priority === 'high'
        }));
        
        const answers = await inquirer.prompt([
          {
            type: 'checkbox',
            name: 'selectedTasks',
            message: 'Select PRPs to update:',
            choices,
            validate: (input) => input.length > 0 || 'Please select at least one PRP'
          }
        ]);
        
        selectedTasks = answers.selectedTasks;
      }
      
      // Confirm update
      if (!options.dryRun) {
        const confirm = await inquirer.prompt([
          {
            type: 'confirm',
            name: 'proceed',
            message: `Update ${selectedTasks.length} PRP(s)?`,
            default: true
          }
        ]);
        
        if (!confirm.proceed) {
          console.log('Update cancelled');
          return;
        }
      }
      
      // Prepare options
      const regenerationOptions: RegenerationOptions = {
        preserveProgress: options.preserve !== false,
        preserveCustomSections: true,
        addChangeMarkers: true,
        backupOriginal: options.backup !== false,
        dryRun: options.dryRun || false
      };
      
      // Update PRPs
      console.log('\n' + chalk.blue('Updating PRPs...'));
      
      for (const task of selectedTasks) {
        console.log(`\n${chalk.bold(task.prpFile)}:`);
        
        const result = await regenerator.regeneratePRP(task, regenerationOptions);
        
        if (result.success) {
          console.log(chalk.green('✓ Updated successfully'));
          
          // Show changes
          if (result.changes.length > 0) {
            console.log('Changes:');
            result.changes.forEach(change => {
              const symbol = change.type === 'added' ? '+' : 
                           change.type === 'removed' ? '-' : '~';
              console.log(`  ${symbol} ${change.section}: ${change.description}`);
            });
          }
          
          // Show preserved content
          if (result.preserved.completionStatus.completedTasks > 0) {
            console.log(chalk.cyan(`  Preserved: ${result.preserved.completionStatus.completedTasks} completed tasks`));
          }
          
          // Show warnings
          if (result.warnings && result.warnings.length > 0) {
            console.log(chalk.yellow('  Warnings:'));
            result.warnings.forEach(warning => {
              console.log(`    - ${warning}`);
            });
          }
        } else {
          console.log(chalk.red('✗ Update failed'));
          if (result.errors) {
            result.errors.forEach(error => {
              console.log(chalk.red(`  Error: ${error}`));
            });
          }
        }
      }
      
      if (options.dryRun) {
        console.log('\n' + chalk.yellow('This was a dry run. No files were modified.'));
      } else {
        console.log('\n' + chalk.green(`✓ Updated ${selectedTasks.length} PRPs`));
      }
      
    } catch (error) {
      console.error(chalk.red('Error updating PRPs:'), error);
      process.exit(1);
    }
  });

// Sync all command
program
  .command('sync-all')
  .description('Synchronize all PRPs with current architecture')
  .option('-d, --dry-run', 'Show what would be updated without making changes')
  .action(async (options) => {
    try {
      const confirm = await inquirer.prompt([
        {
          type: 'confirm',
          name: 'proceed',
          message: 'This will update ALL outdated PRPs. Continue?',
          default: false
        }
      ]);
      
      if (!confirm.proceed) {
        console.log('Sync cancelled');
        return;
      }
      
      console.log(chalk.blue('Synchronizing all PRPs...\n'));
      
      const regenerationOptions: RegenerationOptions = {
        preserveProgress: true,
        preserveCustomSections: true,
        addChangeMarkers: true,
        backupOriginal: true,
        dryRun: options.dryRun || false
      };
      
      const status = await regenerator.syncAllPRPs(regenerationOptions);
      
      console.log('\n' + chalk.bold('Sync Complete'));
      console.log('='.repeat(50));
      console.log(`Total PRPs: ${status.totalPRPs}`);
      console.log(`Successfully synced: ${chalk.green(status.syncedPRPs)}`);
      console.log(`Failed: ${chalk.red(status.outdatedPRPs.length)}`);
      console.log(`Missing PRPs: ${chalk.yellow(status.missingPRPs.length)}`);
      
      if (options.dryRun) {
        console.log('\n' + chalk.yellow('This was a dry run. No files were modified.'));
      }
      
    } catch (error) {
      console.error(chalk.red('Error syncing PRPs:'), error);
      process.exit(1);
    }
  });

// Restore command
program
  .command('restore <prpFile>')
  .description('Restore a PRP from backup')
  .action(async (prpFile) => {
    try {
      // This would list available backups and restore
      console.log(chalk.yellow('Restore functionality not yet implemented'));
    } catch (error) {
      console.error(chalk.red('Error restoring PRP:'), error);
      process.exit(1);
    }
  });

program.parse();
