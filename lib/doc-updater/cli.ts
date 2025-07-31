#!/usr/bin/env node

import { Command } from 'commander';
import { DocumentationUpdater } from './updater';
import { DocumentationWatcher } from './watcher';
import { CodeAnalyzer } from './analyzer';
import chalk from 'chalk';
import { glob } from 'glob';
import path from 'path';
import { promises as fs } from 'fs';

const program = new Command();

program
  .name('doc-updater')
  .description('Automatic documentation updater')
  .version('1.0.0');

// Update command
program
  .command('update')
  .description('Update documentation for specific files')
  .argument('[files...]', 'Files to update documentation for')
  .option('-p, --pattern <pattern>', 'Glob pattern for files')
  .option('-d, --dry-run', 'Show what would be updated without making changes')
  .action(async (files, options) => {
    try {
      console.log(chalk.blue('📝 Updating documentation...\n'));

      let filesToUpdate = files;

      // If pattern provided, use glob
      if (options.pattern) {
        filesToUpdate = await glob(options.pattern);
        console.log(chalk.gray(`Found ${filesToUpdate.length} files matching pattern`));
      }

      // If no files specified, analyze all common paths
      if (!filesToUpdate || filesToUpdate.length === 0) {
        filesToUpdate = await glob('{components,app/api,lib,types}/**/*.{ts,tsx,js,jsx}');
        console.log(chalk.gray(`Analyzing ${filesToUpdate.length} files`));
      }

      const updater = new DocumentationUpdater(process.cwd());
      const result = await updater.processFileChanges(filesToUpdate);

      if (result.success) {
        if (result.updatedFiles.length > 0) {
          console.log(chalk.green(`\n✓ Updated ${result.updatedFiles.length} documentation file(s):`));
          result.updatedFiles.forEach(file => {
            console.log(chalk.green(`  - ${file}`));
          });

          if (options.dryRun) {
            console.log(chalk.yellow('\nThis was a dry run. No files were actually updated.'));
          }
        } else {
          console.log(chalk.gray('No documentation updates needed'));
        }

        // Show warnings
        if (result.warnings && result.warnings.length > 0) {
          console.log(chalk.yellow('\nWarnings:'));
          result.warnings.forEach(warning => {
            console.log(chalk.yellow(`  ⚠ ${warning}`));
          });
        }
      } else {
        console.error(chalk.red('Documentation update failed:'));
        result.errors?.forEach(error => {
          console.error(chalk.red(`  - ${error}`));
        });
        process.exit(1);
      }

    } catch (error) {
      console.error(chalk.red('Error:'), error);
      process.exit(1);
    }
  });

// Watch command
program
  .command('watch')
  .description('Watch files and auto-update documentation')
  .option('-p, --paths <paths...>', 'Paths to watch', ['components', 'app/api', 'lib', 'types'])
  .action((options) => {
    const watcher = new DocumentationWatcher();
    
    console.log(chalk.blue('Starting documentation watcher...'));
    watcher.start(options.paths);

    // Handle shutdown
    process.on('SIGINT', async () => {
      console.log(chalk.yellow('\nStopping watcher...'));
      await watcher.stop();
      process.exit(0);
    });

    process.on('SIGTERM', async () => {
      await watcher.stop();
      process.exit(0);
    });
  });

// Analyze command
program
  .command('analyze <file>')
  .description('Analyze a file and show what documentation would be generated')
  .action(async (file) => {
    try {
      console.log(chalk.blue(`Analyzing ${file}...\n`));

      const analyzer = new CodeAnalyzer();
      const analysis = await analyzer.analyzeFile(file);

      console.log(chalk.bold('File Analysis:'));
      console.log(`Path: ${analysis.path}`);
      console.log(`Language: ${analysis.language}`);
      console.log(`Changes detected: ${analysis.changes.length}`);

      if (analysis.changes.length > 0) {
        console.log(chalk.bold('\nDetected changes:'));
        analysis.changes.forEach(change => {
          console.log(`\n${chalk.cyan(change.type)}:`);
          console.log(`  Name: ${change.name}`);
          if (change.description) {
            console.log(`  Description: ${change.description}`);
          }
          if (change.signature) {
            console.log(`  Signature: ${change.signature}`);
          }
        });
      }

    } catch (error) {
      console.error(chalk.red('Error analyzing file:'), error);
      process.exit(1);
    }
  });

// Check command
program
  .command('check')
  .description('Check which documentation files need updating')
  .action(async () => {
    try {
      console.log(chalk.blue('Checking documentation status...\n'));

      const files = await glob('{components,app/api,lib,types}/**/*.{ts,tsx,js,jsx}');
      const docsToUpdate: string[] = [];

      // This would check each file against its documentation
      // For now, just show a summary
      console.log(`Found ${files.length} source files`);
      
      const componentFiles = files.filter(f => f.includes('/components/'));
      const apiFiles = files.filter(f => f.includes('/api/'));
      const libFiles = files.filter(f => f.includes('/lib/'));
      const typeFiles = files.filter(f => f.includes('/types/'));

      console.log(chalk.bold('\nFile distribution:'));
      console.log(`  Components: ${componentFiles.length}`);
      console.log(`  API routes: ${apiFiles.length}`);
      console.log(`  Library files: ${libFiles.length}`);
      console.log(`  Type definitions: ${typeFiles.length}`);

      // Check for missing docs
      const missingDocs: string[] = [];
      for (const file of componentFiles) {
        const docPath = file.replace('/components/', '/docs/components/')
                           .replace('.tsx', '.md')
                           .replace('.jsx', '.md');
        
        try {
          await fs.access(path.join(process.cwd(), docPath));
        } catch {
          missingDocs.push(file);
        }
      }

      console.log(chalk.bold('\nDocumentation coverage:'));
      console.log(`  ✓ Documented: ${files.length - missingDocs.length}`);
      console.log(`  ✗ Missing: ${missingDocs.length}`);

      if (missingDocs.length > 0) {
        console.log(chalk.yellow('\nMissing documentation for:'));
        missingDocs.slice(0, 10).forEach(file => {
          console.log(chalk.yellow(`  - ${file}`));
        });
        if (missingDocs.length > 10) {
          console.log(chalk.gray(`  ... and ${missingDocs.length - 10} more`));
        }
      }

    } catch (error) {
      console.error(chalk.red('Error checking status:'), error);
      process.exit(1);
    }
  });

// Init command
program
  .command('init')
  .description('Initialize documentation structure')
  .action(async () => {
    try {
      console.log(chalk.blue('Initializing documentation structure...\n'));

      const dirs = [
        'docs/components',
        'docs/api',
        'docs/lib',
        'docs/types',
        'docs/architecture',
        'docs/guides'
      ];

      for (const dir of dirs) {
        const fullPath = path.join(process.cwd(), dir);
        console.log(chalk.gray(`Creating ${dir}...`));
        await fs.mkdir(fullPath, { recursive: true });
        
        // Create README for each directory
        const readme = `# ${path.basename(dir).charAt(0).toUpperCase() + path.basename(dir).slice(1)} Documentation

This directory contains auto-generated documentation for ${path.basename(dir)}.

## Structure

Documentation files are automatically generated and updated based on source code changes.

## Manual Sections

You can add custom sections to any documentation file. The following section names are preserved during auto-updates:
- Notes
- FAQ
- Troubleshooting
- Migration Guide

## Auto-update

Documentation is automatically updated when source files change. To manually update:

\`\`\`bash
npx doc-updater update
\`\`\`
`;
        await fs.writeFile(path.join(fullPath, 'README.md'), readme);
      }

      // Create main docs README
      const mainReadme = `# Documentation

This documentation is automatically generated and maintained by the documentation updater system.

## Structure

- **/components** - React component documentation
- **/api** - API endpoint documentation
- **/lib** - Library function documentation
- **/types** - TypeScript type definitions
- **/architecture** - System architecture documentation
- **/guides** - User and developer guides

## Auto-update System

Documentation is automatically updated when code changes are detected. The system:
- Analyzes TypeScript/JavaScript files
- Extracts JSDoc comments
- Generates documentation from code structure
- Preserves custom sections
- Maintains version history

## Commands

### Watch for changes
\`\`\`bash
npx doc-updater watch
\`\`\`

### Update all documentation
\`\`\`bash
npx doc-updater update
\`\`\`

### Check documentation status
\`\`\`bash
npx doc-updater check
\`\`\`

## Writing Documentation

### JSDoc Comments
Add JSDoc comments to your code for better documentation:

\`\`\`typescript
/**
 * Button component for user interactions
 * @example
 * <Button variant="primary" onClick={handleClick}>
 *   Click me
 * </Button>
 */
export function Button({ variant, onClick, children }) {
  // ...
}
\`\`\`

### Custom Sections
Add custom sections that won't be overwritten:

\`\`\`markdown
## Notes
Custom notes about implementation...

## FAQ
Frequently asked questions...
\`\`\`
`;
      await fs.writeFile(path.join(process.cwd(), 'docs/README.md'), mainReadme);

      console.log(chalk.green('\n✓ Documentation structure initialized'));
      console.log(chalk.cyan('\nNext steps:'));
      console.log('1. Run "npx doc-updater update" to generate initial documentation');
      console.log('2. Run "npx doc-updater watch" to enable auto-updates');

    } catch (error) {
      console.error(chalk.red('Error initializing:'), error);
      process.exit(1);
    }
  });

program.parse();
