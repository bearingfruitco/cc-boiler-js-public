import { watch } from 'chokidar';
import { DocumentationUpdater } from './updater';
import { debounce } from 'lodash';
import chalk from 'chalk';

/**
 * File watcher that triggers documentation updates on code changes
 */
export class DocumentationWatcher {
  private updater: DocumentationUpdater;
  private watcher: any;
  private pendingChanges: Set<string> = new Set();
  private updateDebounced: () => void;

  constructor(projectRoot: string = '.') {
    this.updater = new DocumentationUpdater(projectRoot);
    
    // Debounce updates to avoid too many rapid updates
    this.updateDebounced = debounce(() => {
      this.processPendingChanges();
    }, 2000); // Wait 2 seconds after last change
  }

  /**
   * Start watching for file changes
   */
  start(watchPaths: string[] = ['components', 'app/api', 'lib', 'types']): void {
    console.log(chalk.blue('🔍 Starting documentation watcher...'));

    this.watcher = watch(watchPaths, {
      ignored: [
        '**/node_modules/**',
        '**/.git/**',
        '**/dist/**',
        '**/build/**',
        '**/*.test.*',
        '**/*.spec.*',
        '**/docs/**' // Don't watch documentation files
      ],
      persistent: true,
      ignoreInitial: true
    });

    // Handle file changes
    this.watcher
      .on('add', (path: string) => this.handleFileChange(path, 'added'))
      .on('change', (path: string) => this.handleFileChange(path, 'changed'))
      .on('unlink', (path: string) => this.handleFileChange(path, 'removed'))
      .on('error', (error: Error) => console.error(chalk.red('Watcher error:'), error));

    console.log(chalk.green('✓ Documentation watcher started'));
    console.log(chalk.gray('Watching paths:'), watchPaths.join(', '));
  }

  /**
   * Stop watching
   */
  async stop(): Promise<void> {
    if (this.watcher) {
      await this.watcher.close();
      console.log(chalk.yellow('Documentation watcher stopped'));
    }
  }

  /**
   * Handle file change event
   */
  private handleFileChange(path: string, event: string): void {
    console.log(chalk.gray(`File ${event}: ${path}`));
    
    // Skip if it's a documentation file
    if (path.includes('/docs/')) {
      return;
    }

    // Add to pending changes
    this.pendingChanges.add(path);
    
    // Trigger debounced update
    this.updateDebounced();
  }

  /**
   * Process all pending file changes
   */
  private async processPendingChanges(): Promise<void> {
    if (this.pendingChanges.size === 0) {
      return;
    }

    const files = Array.from(this.pendingChanges);
    this.pendingChanges.clear();

    console.log(chalk.blue(`\n📝 Updating documentation for ${files.length} file(s)...`));

    try {
      const result = await this.updater.processFileChanges(files);

      if (result.success) {
        if (result.updatedFiles.length > 0) {
          console.log(chalk.green(`✓ Updated ${result.updatedFiles.length} documentation file(s):`));
          result.updatedFiles.forEach(file => {
            console.log(chalk.green(`  - ${file}`));
          });

          // Show changes summary
          if (result.changes.length > 0) {
            console.log(chalk.cyan('\nChanges made:'));
            result.changes.forEach(change => {
              const symbol = change.type === 'added' ? '+' : 
                           change.type === 'removed' ? '-' : '~';
              const color = change.type === 'added' ? chalk.green : 
                          change.type === 'removed' ? chalk.red : chalk.yellow;
              console.log(color(`  ${symbol} ${change.section}: ${change.reason}`));
            });
          }
        } else {
          console.log(chalk.gray('No documentation updates needed'));
        }

        // Show warnings if any
        if (result.warnings && result.warnings.length > 0) {
          console.log(chalk.yellow('\nWarnings:'));
          result.warnings.forEach(warning => {
            console.log(chalk.yellow(`  ⚠ ${warning}`));
          });
        }
      } else {
        console.error(chalk.red('✗ Documentation update failed:'));
        result.errors?.forEach(error => {
          console.error(chalk.red(`  - ${error}`));
        });
      }
    } catch (error) {
      console.error(chalk.red('Error updating documentation:'), error);
    }
  }
}

// CLI usage
if (require.main === module) {
  const watcher = new DocumentationWatcher();
  
  // Start watching
  watcher.start();

  // Handle shutdown
  process.on('SIGINT', async () => {
    console.log(chalk.yellow('\nShutting down...'));
    await watcher.stop();
    process.exit(0);
  });

  process.on('SIGTERM', async () => {
    await watcher.stop();
    process.exit(0);
  });

  // Keep process running
  console.log(chalk.cyan('Press Ctrl+C to stop watching\n'));
}
