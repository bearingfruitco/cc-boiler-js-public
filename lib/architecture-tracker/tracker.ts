import { promises as fs } from 'fs';
import path from 'path';
import { 
  ArchitectureChange, 
  ArchitectureChangeType,
  ChangeCategory,
  ChangeImpact,
  ArchitectureSnapshot
} from './types';

/**
 * Main class for tracking architecture changes
 */
export class ArchitectureChangeTracker {
  private changesPath: string;
  private snapshotsPath: string;
  private changeLogPath: string;

  constructor(basePath: string = '.') {
    this.changesPath = path.join(basePath, 'docs/architecture/changes');
    this.snapshotsPath = path.join(basePath, 'docs/architecture/snapshots');
    this.changeLogPath = path.join(basePath, 'docs/architecture/CHANGELOG.md');
  }

  /**
   * Initialize the architecture tracking system
   */
  async initialize(): Promise<void> {
    // Create necessary directories
    await fs.mkdir(this.changesPath, { recursive: true });
    await fs.mkdir(this.snapshotsPath, { recursive: true });
    
    // Create initial changelog if it doesn't exist
    try {
      await fs.access(this.changeLogPath);
    } catch {
      await this.createInitialChangelog();
    }
  }

  /**
   * Record a new architecture change
   */
  async recordChange(change: Omit<ArchitectureChange, 'id' | 'timestamp'>): Promise<ArchitectureChange> {
    const fullChange: ArchitectureChange = {
      id: this.generateChangeId(),
      timestamp: new Date().toISOString(),
      ...change
    };

    // Save the change record
    const changeFile = path.join(this.changesPath, `${fullChange.id}.json`);
    await fs.writeFile(changeFile, JSON.stringify(fullChange, null, 2));

    // Update the changelog
    await this.updateChangelog(fullChange);

    // Create a snapshot if it's a significant change
    if (this.isSignificantChange(fullChange)) {
      await this.createSnapshot(fullChange);
    }

    return fullChange;
  }

  /**
   * Get all changes within a date range
   */
  async getChanges(since?: Date, until?: Date): Promise<ArchitectureChange[]> {
    const files = await fs.readdir(this.changesPath);
    const changes: ArchitectureChange[] = [];

    for (const file of files) {
      if (file.endsWith('.json')) {
        const content = await fs.readFile(path.join(this.changesPath, file), 'utf-8');
        const change = JSON.parse(content) as ArchitectureChange;
        
        const changeDate = new Date(change.timestamp);
        if ((!since || changeDate >= since) && (!until || changeDate <= until)) {
          changes.push(change);
        }
      }
    }

    return changes.sort((a, b) => 
      new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    );
  }

  /**
   * Get changes by category
   */
  async getChangesByCategory(category: ChangeCategory): Promise<ArchitectureChange[]> {
    const allChanges = await this.getChanges();
    return allChanges.filter(change => change.category === category);
  }

  /**
   * Get changes affecting a specific component
   */
  async getChangesForComponent(componentId: string): Promise<ArchitectureChange[]> {
    const allChanges = await this.getChanges();
    return allChanges.filter(change => 
      change.impact.components.includes(componentId)
    );
  }

  /**
   * Generate an impact report for a proposed change
   */
  async generateImpactReport(change: Omit<ArchitectureChange, 'id' | 'timestamp'>): Promise<ImpactReport> {
    const affectedComponents = new Set<string>(change.impact.components);
    const relatedChanges: ArchitectureChange[] = [];

    // Find all changes that might be related
    const allChanges = await this.getChanges();
    for (const existingChange of allChanges) {
      const hasOverlap = existingChange.impact.components.some(comp => 
        affectedComponents.has(comp)
      );
      if (hasOverlap) {
        relatedChanges.push(existingChange);
      }
    }

    // Analyze potential conflicts
    const conflicts = this.analyzeConflicts(change, relatedChanges);
    
    // Calculate risk score
    const riskScore = this.calculateRiskScore(change, relatedChanges);

    return {
      proposedChange: change,
      affectedComponents: Array.from(affectedComponents),
      relatedChanges,
      conflicts,
      riskScore,
      recommendations: this.generateRecommendations(change, conflicts, riskScore)
    };
  }

  /**
   * Create an Architecture Decision Record (ADR) from a change
   */
  async createADR(changeId: string): Promise<string> {
    const changes = await this.getChanges();
    const change = changes.find(c => c.id === changeId);
    
    if (!change) {
      throw new Error(`Change ${changeId} not found`);
    }

    const adrContent = this.generateADRContent(change);
    const adrPath = path.join(
      this.changesPath, 
      '..',
      'decisions',
      `ADR-${change.id}.md`
    );

    await fs.mkdir(path.dirname(adrPath), { recursive: true });
    await fs.writeFile(adrPath, adrContent);

    return adrPath;
  }

  /**
   * Generate a visual diff between two architecture snapshots
   */
  async generateDiff(fromDate: Date, toDate: Date): Promise<ArchitectureDiff> {
    const fromSnapshot = await this.getSnapshotNearDate(fromDate);
    const toSnapshot = await this.getSnapshotNearDate(toDate);

    if (!fromSnapshot || !toSnapshot) {
      throw new Error('Could not find snapshots for the specified dates');
    }

    return {
      from: fromSnapshot,
      to: toSnapshot,
      componentChanges: this.diffComponents(fromSnapshot, toSnapshot),
      apiChanges: this.diffAPIs(fromSnapshot, toSnapshot),
      databaseChanges: this.diffDatabases(fromSnapshot, toSnapshot),
      integrationChanges: this.diffIntegrations(fromSnapshot, toSnapshot),
      securityChanges: this.diffSecurityPolicies(fromSnapshot, toSnapshot)
    };
  }

  // Private helper methods

  private generateChangeId(): string {
    const date = new Date();
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const random = Math.random().toString(36).substring(7);
    return `arch-change-${year}${month}${day}-${random}`;
  }

  private async createInitialChangelog(): Promise<void> {
    const content = `# Architecture Changelog

This file tracks all significant changes to the system architecture.

## Format

Each entry follows this format:
- **Date**: When the change was made
- **Type**: The type of change
- **Impact**: Components affected and effort required
- **Description**: What changed and why

---

`;
    await fs.writeFile(this.changeLogPath, content);
  }

  private async updateChangelog(change: ArchitectureChange): Promise<void> {
    const existingContent = await fs.readFile(this.changeLogPath, 'utf-8');
    
    const changeEntry = `
## [${new Date(change.timestamp).toISOString().split('T')[0]}] ${change.description}
- **Type**: ${this.formatChangeType(change.type)}
- **Category**: ${change.category}
- **Impact**: ${change.impact.estimatedEffort} effort, affects ${change.impact.components.join(', ')}
- **Breaking Change**: ${change.impact.breakingChange ? 'Yes' : 'No'}
- **Author**: ${change.author}
- **Rationale**: ${change.rationale}
${change.relatedPRP ? `- **Related PRP**: ${change.relatedPRP}` : ''}

### Changes
${change.filesAffected.map(file => `- Modified: \`${file}\``).join('\n')}

---
`;

    // Insert the new entry after the header
    const lines = existingContent.split('\n');
    const insertIndex = lines.findIndex(line => line.startsWith('---')) + 2;
    lines.splice(insertIndex, 0, changeEntry);
    
    await fs.writeFile(this.changeLogPath, lines.join('\n'));
  }

  private formatChangeType(type: ArchitectureChangeType): string {
    return type.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    ).join(' ');
  }

  private isSignificantChange(change: ArchitectureChange): boolean {
    return change.impact.breakingChange || 
           change.impact.estimatedEffort === 'high' ||
           change.type === ArchitectureChangeType.ARCHITECTURE_PATTERN_CHANGED ||
           change.type === ArchitectureChangeType.TECHNOLOGY_STACK_CHANGED;
  }

  private async createSnapshot(change: ArchitectureChange): Promise<void> {
    // This would create a full snapshot of the current architecture
    // For now, we'll create a placeholder
    const snapshot: ArchitectureSnapshot = {
      timestamp: change.timestamp,
      version: `snapshot-${change.id}`,
      components: [], // Would be populated from actual architecture docs
      apis: [],
      databases: [],
      integrations: [],
      securityPolicies: []
    };

    const snapshotFile = path.join(this.snapshotsPath, `${snapshot.version}.json`);
    await fs.writeFile(snapshotFile, JSON.stringify(snapshot, null, 2));
  }

  private analyzeConflicts(
    proposedChange: Omit<ArchitectureChange, 'id' | 'timestamp'>, 
    relatedChanges: ArchitectureChange[]
  ): Conflict[] {
    const conflicts: Conflict[] = [];

    for (const related of relatedChanges) {
      // Check for file conflicts
      const fileOverlap = proposedChange.filesAffected.filter(file =>
        related.filesAffected.includes(file)
      );

      if (fileOverlap.length > 0) {
        conflicts.push({
          type: 'file_conflict',
          severity: 'medium',
          description: `Conflicts with change ${related.id} on files: ${fileOverlap.join(', ')}`,
          relatedChangeId: related.id
        });
      }

      // Check for component conflicts
      const componentOverlap = proposedChange.impact.components.filter(comp =>
        related.impact.components.includes(comp)
      );

      if (componentOverlap.length > 0 && this.areConflictingChangeTypes(proposedChange.type, related.type)) {
        conflicts.push({
          type: 'component_conflict',
          severity: 'high',
          description: `Conflicting changes to components: ${componentOverlap.join(', ')}`,
          relatedChangeId: related.id
        });
      }
    }

    return conflicts;
  }

  private areConflictingChangeTypes(type1: ArchitectureChangeType, type2: ArchitectureChangeType): boolean {
    const conflictMap: Record<ArchitectureChangeType, ArchitectureChangeType[]> = {
      [ArchitectureChangeType.COMPONENT_REMOVED]: [
        ArchitectureChangeType.COMPONENT_MODIFIED,
        ArchitectureChangeType.API_ADDED
      ],
      [ArchitectureChangeType.API_REMOVED]: [
        ArchitectureChangeType.API_MODIFIED
      ],
      // Add more conflict rules as needed
    } as any;

    return conflictMap[type1]?.includes(type2) || conflictMap[type2]?.includes(type1) || false;
  }

  private calculateRiskScore(
    change: Omit<ArchitectureChange, 'id' | 'timestamp'>,
    relatedChanges: ArchitectureChange[]
  ): number {
    let score = 0;

    // Base risk from change type
    const typeRiskMap: Partial<Record<ArchitectureChangeType, number>> = {
      [ArchitectureChangeType.COMPONENT_REMOVED]: 8,
      [ArchitectureChangeType.API_REMOVED]: 7,
      [ArchitectureChangeType.DATABASE_SCHEMA_CHANGED]: 9,
      [ArchitectureChangeType.SECURITY_POLICY_UPDATED]: 6,
      [ArchitectureChangeType.ARCHITECTURE_PATTERN_CHANGED]: 10,
    };
    score += typeRiskMap[change.type] || 5;

    // Risk from impact
    if (change.impact.breakingChange) score += 5;
    if (change.impact.securityImpact) score += 3;
    if (change.impact.estimatedEffort === 'high') score += 2;
    
    // Risk from number of affected components
    score += Math.min(change.impact.components.length, 5);

    // Risk from recent related changes
    const recentRelatedChanges = relatedChanges.filter(rc => {
      const daysSince = (Date.now() - new Date(rc.timestamp).getTime()) / (1000 * 60 * 60 * 24);
      return daysSince < 30;
    });
    score += Math.min(recentRelatedChanges.length * 2, 10);

    return Math.min(score, 30); // Cap at 30
  }

  private generateRecommendations(
    change: Omit<ArchitectureChange, 'id' | 'timestamp'>,
    conflicts: Conflict[],
    riskScore: number
  ): string[] {
    const recommendations: string[] = [];

    if (riskScore > 20) {
      recommendations.push('Consider breaking this change into smaller, incremental changes');
      recommendations.push('Schedule a architecture review meeting before proceeding');
    }

    if (change.impact.breakingChange) {
      recommendations.push('Create a migration guide for affected components');
      recommendations.push('Plan for a phased rollout with feature flags');
    }

    if (conflicts.some(c => c.severity === 'high')) {
      recommendations.push('Resolve high-severity conflicts before implementation');
      recommendations.push('Coordinate with teams owning conflicting changes');
    }

    if (change.impact.securityImpact) {
      recommendations.push('Conduct security review before implementation');
      recommendations.push('Update security documentation and policies');
    }

    if (change.impact.estimatedEffort === 'high') {
      recommendations.push('Consider creating a dedicated project team');
      recommendations.push('Break down into multiple PRPs for better tracking');
    }

    return recommendations;
  }

  private generateADRContent(change: ArchitectureChange): string {
    return `# Architecture Decision Record: ${change.description}

## Status
Implemented

## Context
${change.rationale}

## Decision
${change.description}

### Change Type
${this.formatChangeType(change.type)}

### Category
${change.category}

## Consequences

### Positive
- ${change.rationale}

### Negative
- Effort: ${change.impact.estimatedEffort}
- Breaking change: ${change.impact.breakingChange ? 'Yes' : 'No'}
${change.impact.securityImpact ? '- Security impact requires review' : ''}

### Affected Components
${change.impact.components.map(comp => `- ${comp}`).join('\n')}

## Implementation
- Date: ${new Date(change.timestamp).toISOString().split('T')[0]}
- Author: ${change.author}
${change.relatedPRP ? `- Related PRP: ${change.relatedPRP}` : ''}

### Files Modified
${change.filesAffected.map(file => `- ${file}`).join('\n')}

## References
- [Architecture Changelog](../CHANGELOG.md)
${change.relatedPRP ? `- [Project Requirements Plan](../../PRPs/${change.relatedPRP}.md)` : ''}
`;
  }

  private async getSnapshotNearDate(date: Date): Promise<ArchitectureSnapshot | null> {
    const files = await fs.readdir(this.snapshotsPath);
    let closestSnapshot: ArchitectureSnapshot | null = null;
    let closestDiff = Infinity;

    for (const file of files) {
      if (file.endsWith('.json')) {
        const content = await fs.readFile(path.join(this.snapshotsPath, file), 'utf-8');
        const snapshot = JSON.parse(content) as ArchitectureSnapshot;
        const snapshotDate = new Date(snapshot.timestamp);
        const diff = Math.abs(date.getTime() - snapshotDate.getTime());
        
        if (diff < closestDiff) {
          closestDiff = diff;
          closestSnapshot = snapshot;
        }
      }
    }

    return closestSnapshot;
  }

  private diffComponents(from: ArchitectureSnapshot, to: ArchitectureSnapshot): ComponentDiff[] {
    // Implementation would compare components between snapshots
    return [];
  }

  private diffAPIs(from: ArchitectureSnapshot, to: ArchitectureSnapshot): APIDiff[] {
    // Implementation would compare APIs between snapshots
    return [];
  }

  private diffDatabases(from: ArchitectureSnapshot, to: ArchitectureSnapshot): DatabaseDiff[] {
    // Implementation would compare databases between snapshots
    return [];
  }

  private diffIntegrations(from: ArchitectureSnapshot, to: ArchitectureSnapshot): IntegrationDiff[] {
    // Implementation would compare integrations between snapshots
    return [];
  }

  private diffSecurityPolicies(from: ArchitectureSnapshot, to: ArchitectureSnapshot): SecurityPolicyDiff[] {
    // Implementation would compare security policies between snapshots
    return [];
  }
}

// Additional type definitions

interface ImpactReport {
  proposedChange: Omit<ArchitectureChange, 'id' | 'timestamp'>;
  affectedComponents: string[];
  relatedChanges: ArchitectureChange[];
  conflicts: Conflict[];
  riskScore: number;
  recommendations: string[];
}

interface Conflict {
  type: 'file_conflict' | 'component_conflict' | 'dependency_conflict';
  severity: 'low' | 'medium' | 'high';
  description: string;
  relatedChangeId: string;
}

interface ArchitectureDiff {
  from: ArchitectureSnapshot;
  to: ArchitectureSnapshot;
  componentChanges: ComponentDiff[];
  apiChanges: APIDiff[];
  databaseChanges: DatabaseDiff[];
  integrationChanges: IntegrationDiff[];
  securityChanges: SecurityPolicyDiff[];
}

interface ComponentDiff {
  type: 'added' | 'removed' | 'modified';
  component: ComponentDefinition;
  changes?: string[];
}

interface APIDiff {
  type: 'added' | 'removed' | 'modified';
  api: APIDefinition;
  changes?: string[];
}

interface DatabaseDiff {
  type: 'added' | 'removed' | 'modified';
  database: DatabaseDefinition;
  changes?: string[];
}

interface IntegrationDiff {
  type: 'added' | 'removed' | 'modified';
  integration: IntegrationDefinition;
  changes?: string[];
}

interface SecurityPolicyDiff {
  type: 'added' | 'removed' | 'modified';
  policy: SecurityPolicy;
  changes?: string[];
}

// Re-export types
export type {
  ImpactReport,
  Conflict,
  ArchitectureDiff,
  ComponentDiff,
  APIDiff,
  DatabaseDiff,
  IntegrationDiff,
  SecurityPolicyDiff
};
