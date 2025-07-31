import { ArchitectureChangeTracker } from './tracker';
import { 
  ArchitectureChangeType, 
  ChangeCategory,
  ArchitectureChange 
} from './types';

/**
 * Integration hooks for connecting the Architecture Tracker
 * with existing project systems
 */

export class ArchitectureTrackerHooks {
  private tracker: ArchitectureChangeTracker;

  constructor(projectRoot: string = '.') {
    this.tracker = new ArchitectureChangeTracker(projectRoot);
  }

  /**
   * Hook for PRP generation - records architecture changes when new PRPs are created
   */
  async onPRPCreated(prp: {
    id: string;
    title: string;
    description: string;
    components: string[];
    type: string;
  }): Promise<void> {
    // Determine change type based on PRP
    const changeType = this.inferChangeType(prp);
    const category = this.inferCategory(prp);

    await this.tracker.recordChange({
      type: changeType,
      category: category,
      description: `PRP Created: ${prp.title}`,
      filesAffected: [`PRPs/${prp.id}.md`],
      relatedPRP: prp.id,
      author: process.env.USER || 'system',
      rationale: prp.description,
      impact: {
        components: prp.components,
        estimatedEffort: 'medium', // Could be inferred from PRP
        breakingChange: false,
      }
    });
  }

  /**
   * Hook for component creation/modification
   */
  async onComponentChange(change: {
    componentId: string;
    action: 'created' | 'modified' | 'removed';
    description: string;
    files: string[];
    relatedPRP?: string;
  }): Promise<void> {
    const typeMap = {
      created: ArchitectureChangeType.COMPONENT_ADDED,
      modified: ArchitectureChangeType.COMPONENT_MODIFIED,
      removed: ArchitectureChangeType.COMPONENT_REMOVED,
    };

    await this.tracker.recordChange({
      type: typeMap[change.action],
      category: ChangeCategory.BACKEND, // Could be determined from component
      description: `Component ${change.action}: ${change.componentId}`,
      filesAffected: change.files,
      relatedPRP: change.relatedPRP,
      author: process.env.USER || 'system',
      rationale: change.description,
      impact: {
        components: [change.componentId],
        estimatedEffort: change.action === 'removed' ? 'high' : 'medium',
        breakingChange: change.action === 'removed',
      }
    });
  }

  /**
   * Hook for API endpoint changes
   */
  async onAPIChange(change: {
    endpoint: string;
    method: string;
    action: 'added' | 'modified' | 'removed';
    description: string;
    breakingChange?: boolean;
  }): Promise<void> {
    const typeMap = {
      added: ArchitectureChangeType.API_ADDED,
      modified: ArchitectureChangeType.API_MODIFIED,
      removed: ArchitectureChangeType.API_REMOVED,
    };

    await this.tracker.recordChange({
      type: typeMap[change.action],
      category: ChangeCategory.BACKEND,
      description: `API ${change.action}: ${change.method} ${change.endpoint}`,
      filesAffected: [`app/api/${change.endpoint}/route.ts`],
      author: process.env.USER || 'system',
      rationale: change.description,
      impact: {
        components: ['api-gateway'],
        estimatedEffort: 'low',
        breakingChange: change.breakingChange || change.action === 'removed',
      }
    });
  }

  /**
   * Hook for database schema changes
   */
  async onDatabaseChange(change: {
    tables: string[];
    action: string;
    migration: string;
    description: string;
  }): Promise<void> {
    await this.tracker.recordChange({
      type: ArchitectureChangeType.DATABASE_SCHEMA_CHANGED,
      category: ChangeCategory.DATABASE,
      description: `Database ${change.action}: ${change.tables.join(', ')}`,
      filesAffected: [`migrations/${change.migration}`],
      author: process.env.USER || 'system',
      rationale: change.description,
      impact: {
        components: ['database', ...change.tables],
        estimatedEffort: 'high',
        breakingChange: true,
      }
    });
  }

  /**
   * Hook for security policy updates
   */
  async onSecurityPolicyChange(change: {
    policy: string;
    action: string;
    description: string;
    components: string[];
  }): Promise<void> {
    await this.tracker.recordChange({
      type: ArchitectureChangeType.SECURITY_POLICY_UPDATED,
      category: ChangeCategory.SECURITY,
      description: `Security policy ${change.action}: ${change.policy}`,
      filesAffected: ['docs/SECURITY.md'],
      author: process.env.USER || 'system',
      rationale: change.description,
      impact: {
        components: change.components,
        estimatedEffort: 'medium',
        breakingChange: false,
        securityImpact: true,
      }
    });
  }

  /**
   * Hook for integration changes
   */
  async onIntegrationChange(change: {
    service: string;
    action: 'added' | 'removed' | 'modified';
    description: string;
    configFiles: string[];
  }): Promise<void> {
    const typeMap = {
      added: ArchitectureChangeType.INTEGRATION_ADDED,
      removed: ArchitectureChangeType.INTEGRATION_REMOVED,
      modified: ArchitectureChangeType.INTEGRATION_ADDED, // No specific type for modified
    };

    await this.tracker.recordChange({
      type: typeMap[change.action],
      category: ChangeCategory.INTEGRATION,
      description: `Integration ${change.action}: ${change.service}`,
      filesAffected: change.configFiles,
      author: process.env.USER || 'system',
      rationale: change.description,
      impact: {
        components: ['integrations', change.service],
        estimatedEffort: change.action === 'added' ? 'high' : 'medium',
        breakingChange: change.action === 'removed',
      }
    });
  }

  /**
   * Git hook for detecting architecture changes from commits
   */
  async onGitCommit(commit: {
    hash: string;
    message: string;
    files: string[];
    author: string;
  }): Promise<void> {
    // Check if any architecture files were modified
    const archFiles = commit.files.filter(f => 
      f.includes('docs/architecture/') ||
      f.includes('SYSTEM_DESIGN.md') ||
      f.includes('TECHNICAL_ROADMAP.md')
    );

    if (archFiles.length === 0) return;

    // Try to parse change type from commit message
    const changeInfo = this.parseCommitMessage(commit.message);
    
    if (changeInfo) {
      await this.tracker.recordChange({
        type: changeInfo.type,
        category: changeInfo.category,
        description: changeInfo.description,
        filesAffected: archFiles,
        author: commit.author,
        rationale: commit.message,
        impact: changeInfo.impact,
      });
    }
  }

  /**
   * Validation hook - checks if proposed changes conflict
   */
  async validateProposedChange(change: Omit<ArchitectureChange, 'id' | 'timestamp'>): Promise<{
    valid: boolean;
    conflicts: any[];
    recommendations: string[];
  }> {
    const report = await this.tracker.generateImpactReport(change);
    
    return {
      valid: report.riskScore < 20 && report.conflicts.filter(c => c.severity === 'high').length === 0,
      conflicts: report.conflicts,
      recommendations: report.recommendations,
    };
  }

  // Helper methods

  private inferChangeType(prp: any): ArchitectureChangeType {
    // Simple inference based on PRP type/title
    if (prp.type === 'feature' || prp.title.toLowerCase().includes('add')) {
      return ArchitectureChangeType.COMPONENT_ADDED;
    } else if (prp.title.toLowerCase().includes('remove') || prp.title.toLowerCase().includes('deprecate')) {
      return ArchitectureChangeType.COMPONENT_REMOVED;
    } else if (prp.title.toLowerCase().includes('api')) {
      return ArchitectureChangeType.API_ADDED;
    } else if (prp.title.toLowerCase().includes('database') || prp.title.toLowerCase().includes('schema')) {
      return ArchitectureChangeType.DATABASE_SCHEMA_CHANGED;
    }
    return ArchitectureChangeType.COMPONENT_MODIFIED;
  }

  private inferCategory(prp: any): ChangeCategory {
    // Simple inference based on components
    if (prp.components.some((c: string) => c.includes('ui') || c.includes('frontend'))) {
      return ChangeCategory.FRONTEND;
    } else if (prp.components.some((c: string) => c.includes('db') || c.includes('database'))) {
      return ChangeCategory.DATABASE;
    } else if (prp.components.some((c: string) => c.includes('api') || c.includes('backend'))) {
      return ChangeCategory.BACKEND;
    }
    return ChangeCategory.BACKEND;
  }

  private parseCommitMessage(message: string): any | null {
    // Parse conventional commit format or specific patterns
    const patterns = [
      /^feat\(arch\): (.+)$/,
      /^architecture: (.+)$/,
      /^arch-change: (.+)$/,
    ];

    for (const pattern of patterns) {
      const match = message.match(pattern);
      if (match) {
        return {
          type: ArchitectureChangeType.COMPONENT_MODIFIED,
          category: ChangeCategory.BACKEND,
          description: match[1],
          impact: {
            components: [],
            estimatedEffort: 'medium',
            breakingChange: false,
          }
        };
      }
    }

    return null;
  }
}

// Export singleton instance
export const architectureHooks = new ArchitectureTrackerHooks();
