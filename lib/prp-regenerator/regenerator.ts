import { promises as fs } from 'fs';
import path from 'path';
import { ArchitectureChangeTracker } from '../architecture-tracker';
import { ArchitectureChange as TrackerChange } from '../architecture-tracker/types';
import { PRPParser } from './parser';
import { PRPGenerator } from './generator';
import { 
  PRPRegenerationTask,
  RegenerationResult,
  ArchitectureChange,
  RegenerationOptions,
  PRPSyncStatus,
  PRPStatus
} from './types';

/**
 * Main class for regenerating PRPs based on architecture changes
 */
export class PRPRegenerator {
  private tracker: ArchitectureChangeTracker;
  private parser: PRPParser;
  private generator: PRPGenerator;
  private prpDirectory: string;
  private backupDirectory: string;

  constructor(projectRoot: string = '.') {
    this.tracker = new ArchitectureChangeTracker(projectRoot);
    this.parser = new PRPParser();
    this.generator = new PRPGenerator(projectRoot);
    this.prpDirectory = path.join(projectRoot, 'PRPs');
    this.backupDirectory = path.join(projectRoot, 'PRPs', '.backups');
  }

  /**
   * Analyze architecture changes and determine which PRPs need updates
   */
  async analyzeImpact(since?: Date): Promise<PRPRegenerationTask[]> {
    // Get recent architecture changes
    const changes = await this.tracker.getChanges(since);
    
    // Group changes by component
    const componentChanges = new Map<string, TrackerChange[]>();
    
    for (const change of changes) {
      for (const component of change.impact.components) {
        if (!componentChanges.has(component)) {
          componentChanges.set(component, []);
        }
        componentChanges.get(component)!.push(change);
      }
    }

    // Create regeneration tasks
    const tasks: PRPRegenerationTask[] = [];
    
    for (const [component, changes] of componentChanges) {
      const prpFile = this.getPRPFileName(component);
      const prpPath = path.join(this.prpDirectory, prpFile);
      
      // Check if PRP exists
      const prpExists = await this.fileExists(prpPath);
      
      if (prpExists) {
        // Analyze if regeneration is needed
        const needsUpdate = await this.needsRegeneration(prpPath, changes);
        
        if (needsUpdate) {
          tasks.push({
            prpFile,
            component,
            architectureChanges: this.convertChanges(changes),
            preserveSections: ['implementation_notes', 'validation_results'],
            priority: this.calculatePriority(changes),
            reason: this.generateReason(changes)
          });
        }
      } else {
        // New component detected - suggest PRP creation
        console.log(`New component detected without PRP: ${component}`);
      }
    }

    return tasks;
  }

  /**
   * Regenerate a single PRP with architecture updates
   */
  async regeneratePRP(
    task: PRPRegenerationTask,
    options: RegenerationOptions = {
      preserveProgress: true,
      preserveCustomSections: true,
      addChangeMarkers: true,
      backupOriginal: true,
      dryRun: false
    }
  ): Promise<RegenerationResult> {
    const prpPath = path.join(this.prpDirectory, task.prpFile);
    
    try {
      // Backup original if requested
      if (options.backupOriginal && !options.dryRun) {
        await this.backupPRP(prpPath);
      }

      // Parse existing PRP
      const existingPRP = await this.parser.parsePRP(prpPath);
      
      // Extract content to preserve
      const preserved = await this.parser.extractPreservedContent(prpPath);
      
      // Generate new PRP content with updates
      const newContent = await this.generator.generatePRP(
        task.component,
        task.architectureChanges,
        preserved,
        options
      );

      // Merge completion status if preserving progress
      let finalContent = newContent;
      if (options.preserveProgress) {
        finalContent = this.parser.mergeCheckboxStatus(newContent, preserved.completionStatus);
      }

      // Add change markers if requested
      if (options.addChangeMarkers) {
        finalContent = this.addChangeMarkers(finalContent, task.architectureChanges);
      }

      // Write updated PRP (unless dry run)
      if (!options.dryRun) {
        await fs.writeFile(prpPath, finalContent, 'utf-8');
      }

      // Calculate what changed
      const changes = this.calculateChanges(existingPRP, finalContent);

      return {
        success: true,
        prpFile: task.prpFile,
        changes,
        preserved,
        warnings: this.generateWarnings(existingPRP, preserved)
      };

    } catch (error) {
      return {
        success: false,
        prpFile: task.prpFile,
        changes: [],
        preserved: {
          completionStatus: { totalTasks: 0, completedTasks: 0, checkboxes: [], lastUpdated: '' },
          customSections: {},
          implementationNotes: []
        },
        errors: [error instanceof Error ? error.message : 'Unknown error']
      };
    }
  }

  /**
   * Sync all PRPs with current architecture
   */
  async syncAllPRPs(options?: RegenerationOptions): Promise<PRPSyncStatus> {
    const tasks = await this.analyzeImpact();
    const results: RegenerationResult[] = [];
    
    for (const task of tasks) {
      const result = await this.regeneratePRP(task, options);
      results.push(result);
    }

    // Get all PRPs
    const allPRPs = await this.getAllPRPs();
    const syncedPRPs = results.filter(r => r.success).map(r => r.prpFile);
    const outdatedPRPs = results.filter(r => !r.success).map(r => r.prpFile);
    
    // Find missing PRPs (components without PRPs)
    const components = await this.getAllComponents();
    const missingPRPs = components
      .filter(comp => !allPRPs.includes(this.getPRPFileName(comp)))
      .map(comp => this.getPRPFileName(comp));

    return {
      totalPRPs: allPRPs.length,
      syncedPRPs: syncedPRPs.length,
      outdatedPRPs,
      missingPRPs,
      lastSync: new Date().toISOString()
    };
  }

  /**
   * Check sync status without making changes
   */
  async checkSyncStatus(): Promise<PRPSyncStatus> {
    const tasks = await this.analyzeImpact();
    const allPRPs = await this.getAllPRPs();
    const components = await this.getAllComponents();
    
    const outdatedPRPs = tasks.map(t => t.prpFile);
    const missingPRPs = components
      .filter(comp => !allPRPs.includes(this.getPRPFileName(comp)))
      .map(comp => this.getPRPFileName(comp));

    return {
      totalPRPs: allPRPs.length,
      syncedPRPs: allPRPs.length - outdatedPRPs.length,
      outdatedPRPs,
      missingPRPs,
      lastSync: new Date().toISOString()
    };
  }

  // Private helper methods

  private async fileExists(path: string): Promise<boolean> {
    try {
      await fs.access(path);
      return true;
    } catch {
      return false;
    }
  }

  private getPRPFileName(component: string): string {
    return `${component.toLowerCase().replace(/\s+/g, '-')}-prp.md`;
  }

  private async needsRegeneration(prpPath: string, changes: TrackerChange[]): Promise<boolean> {
    // Check if any changes are significant enough to warrant regeneration
    const significantChanges = changes.some(change => 
      change.impact.breakingChange ||
      change.type.includes('REMOVED') ||
      change.type.includes('SCHEMA_CHANGED') ||
      change.type === 'ARCHITECTURE_PATTERN_CHANGED'
    );

    if (significantChanges) return true;

    // Check if PRP is marked as outdated
    try {
      const prp = await this.parser.parsePRP(prpPath);
      return prp.metadata.status === PRPStatus.OUTDATED;
    } catch {
      return true; // If we can't parse it, regenerate it
    }
  }

  private convertChanges(trackerChanges: TrackerChange[]): ArchitectureChange[] {
    return trackerChanges.map(change => ({
      type: this.mapChangeType(change.type),
      component: change.impact.components[0] || 'unknown',
      description: change.description,
      impact: change.impact.components,
      requiresPRPUpdate: true
    }));
  }

  private mapChangeType(trackerType: string): 'added' | 'modified' | 'removed' {
    if (trackerType.includes('ADDED')) return 'added';
    if (trackerType.includes('REMOVED')) return 'removed';
    return 'modified';
  }

  private calculatePriority(changes: TrackerChange[]): 'high' | 'medium' | 'low' {
    if (changes.some(c => c.impact.breakingChange)) return 'high';
    if (changes.some(c => c.impact.estimatedEffort === 'high')) return 'high';
    if (changes.some(c => c.impact.securityImpact)) return 'high';
    if (changes.length > 3) return 'medium';
    return 'low';
  }

  private generateReason(changes: TrackerChange[]): string {
    const reasons: string[] = [];
    
    if (changes.some(c => c.impact.breakingChange)) {
      reasons.push('Breaking changes detected');
    }
    
    const types = new Set(changes.map(c => c.type));
    reasons.push(`Architecture changes: ${Array.from(types).join(', ')}`);
    
    return reasons.join('. ');
  }

  private async backupPRP(prpPath: string): Promise<void> {
    await fs.mkdir(this.backupDirectory, { recursive: true });
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = path.basename(prpPath);
    const backupPath = path.join(this.backupDirectory, `${filename}.${timestamp}`);
    
    await fs.copyFile(prpPath, backupPath);
  }

  private addChangeMarkers(content: string, changes: ArchitectureChange[]): string {
    const changeNotice = `
> ⚠️ **Architecture Updated**: ${new Date().toISOString().split('T')[0]}
${changes.map(c => `> - ${c.type.toUpperCase()}: ${c.description}`).join('\n')}
> - See [architecture changelog](../docs/architecture/CHANGELOG.md)

`;

    // Add after title
    const lines = content.split('\n');
    const titleIndex = lines.findIndex(line => line.startsWith('# '));
    
    if (titleIndex !== -1) {
      lines.splice(titleIndex + 1, 0, changeNotice);
    }

    // Mark changed sections
    changes.forEach(change => {
      const sectionRegex = new RegExp(`^(##.*${change.component}.*$)`, 'gmi');
      content = content.replace(sectionRegex, '$1 🔄');
    });

    return lines.join('\n');
  }

  private calculateChanges(existingPRP: any, newContent: string): any[] {
    // This would do a detailed diff - simplified for now
    return [
      {
        section: 'Architecture Changes',
        type: 'added',
        description: 'Added architecture change notifications'
      }
    ];
  }

  private generateWarnings(existingPRP: any, preserved: any): string[] {
    const warnings: string[] = [];
    
    if (existingPRP.metadata.status === PRPStatus.COMPLETED) {
      warnings.push('PRP was marked as completed - manual review recommended');
    }
    
    if (preserved.completionStatus.completedTasks > 0) {
      warnings.push(`${preserved.completionStatus.completedTasks} tasks already completed`);
    }
    
    return warnings;
  }

  private async getAllPRPs(): Promise<string[]> {
    try {
      const files = await fs.readdir(this.prpDirectory);
      return files.filter(f => f.endsWith('-prp.md'));
    } catch {
      return [];
    }
  }

  private async getAllComponents(): Promise<string[]> {
    // This would extract from architecture docs - simplified for now
    return [
      'authentication-service',
      'user-management',
      'api-gateway',
      'database-service'
    ];
  }
}
