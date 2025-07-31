import { promises as fs } from 'fs';
import path from 'path';
import { 
  ArchitectureChange,
  PreservedContent,
  RegenerationOptions,
  PRPSection,
  SectionType,
  PRPStatus
} from './types';

/**
 * Generates PRP content based on architecture and preserved content
 */
export class PRPGenerator {
  private projectRoot: string;
  private architecturePath: string;

  constructor(projectRoot: string = '.') {
    this.projectRoot = projectRoot;
    this.architecturePath = path.join(projectRoot, 'docs/architecture');
  }

  /**
   * Generate updated PRP content
   */
  async generatePRP(
    component: string,
    architectureChanges: ArchitectureChange[],
    preserved: PreservedContent,
    options: RegenerationOptions
  ): Promise<string> {
    // Load current architecture
    const architecture = await this.loadArchitecture();
    
    // Generate sections
    const sections: PRPSection[] = [
      this.generateMetadata(component, architectureChanges),
      this.generateOverview(component, architecture),
      this.generateTechnicalContext(component, architecture, architectureChanges),
      this.generateArchitectureChanges(architectureChanges),
      this.generateSchemaDefinitions(component, architecture),
      this.generateFileStructure(component),
      this.generateImplementationOrder(component, architecture),
      this.generateValidationCheckpoints(component),
    ];

    // Add preserved custom sections
    if (options.preserveCustomSections && preserved.customSections) {
      Object.entries(preserved.customSections).forEach(([id, content]) => {
        sections.push({
          id,
          title: this.formatTitle(id),
          content,
          type: SectionType.CUSTOM,
          required: false,
          order: 100, // Put custom sections at the end
          isCustom: true
        });
      });
    }

    // Sort sections by order
    sections.sort((a, b) => a.order - b.order);

    // Build markdown content
    return this.buildMarkdown(sections, preserved, options);
  }

  private generateMetadata(component: string, changes: ArchitectureChange[]): PRPSection {
    const metadata = {
      id: `${component}-prp`,
      component: component,
      version: '2.0.0', // Increment version due to architecture update
      lastGenerated: new Date().toISOString(),
      architectureVersion: 'latest',
      status: changes.length > 0 ? PRPStatus.OUTDATED : PRPStatus.DRAFT,
      regeneratedDue: changes.map(c => c.description).join(', ')
    };

    const content = `---
${Object.entries(metadata).map(([key, value]) => `${key}: ${value}`).join('\n')}
---`;

    return {
      id: 'metadata',
      title: 'Metadata',
      content,
      type: SectionType.CUSTOM,
      required: true,
      order: 0
    };
  }

  private generateOverview(component: string, architecture: any): PRPSection {
    const content = `
## Overview

This Project Requirements Plan (PRP) defines the implementation requirements for the **${component}** component.

${architecture.components?.[component]?.description || 'Component description will be added here.'}

### Recent Architecture Updates

This PRP has been regenerated to reflect recent architecture changes. Please review the changes in the Architecture Changes section below.

### Component Purpose
${architecture.components?.[component]?.purpose || '- Primary responsibility of this component'}

### Key Features
${architecture.components?.[component]?.features?.map((f: string) => `- ${f}`).join('\n') || '- Feature 1\n- Feature 2'}
`;

    return {
      id: 'overview',
      title: 'Overview',
      content: content.trim(),
      type: SectionType.OVERVIEW,
      required: true,
      order: 1
    };
  }

  private generateTechnicalContext(
    component: string, 
    architecture: any, 
    changes: ArchitectureChange[]
  ): PRPSection {
    const dependencies = architecture.components?.[component]?.dependencies || [];
    const integrations = architecture.components?.[component]?.integrations || [];

    const content = `
## Technical Context

### Dependencies
${dependencies.length > 0 ? dependencies.map((d: string) => `- ${d}`).join('\n') : '- No external dependencies'}

### Integrations
${integrations.length > 0 ? integrations.map((i: string) => `- ${i}`).join('\n') : '- No integrations required'}

### Technology Stack
- **Language**: ${architecture.stack?.language || 'TypeScript'}
- **Framework**: ${architecture.stack?.framework || 'Next.js'}
- **Database**: ${architecture.stack?.database || 'PostgreSQL'}
- **Cache**: ${architecture.stack?.cache || 'Redis'}

### Architecture Patterns
${architecture.patterns?.map((p: string) => `- ${p}`).join('\n') || '- Repository pattern\n- Service layer\n- Event-driven'}

${changes.some(c => c.type === 'modified') ? `
### Technical Considerations
Due to recent architecture changes, please ensure:
- Compatibility with updated dependencies
- Migration of existing data if schema changed
- Update integration points as needed` : ''}
`;

    return {
      id: 'technical-context',
      title: 'Technical Context',
      content: content.trim(),
      type: SectionType.TECHNICAL_CONTEXT,
      required: true,
      order: 2
    };
  }

  private generateArchitectureChanges(changes: ArchitectureChange[]): PRPSection {
    if (changes.length === 0) {
      return {
        id: 'architecture-changes',
        title: 'Architecture Changes',
        content: '## Architecture Changes\n\nNo architecture changes detected.',
        type: SectionType.ARCHITECTURE_CHANGES,
        required: false,
        order: 3
      };
    }

    const content = `
## Architecture Changes 🔄

The following architecture changes affect this component:

${changes.map(change => `
### ${this.formatChangeType(change.type)}: ${change.component}

**Description**: ${change.description}

**Impact**: 
${change.impact.map(i => `- ${i}`).join('\n')}

**Action Required**: ${this.getActionRequired(change)}
`).join('\n')}

### Migration Notes
${this.generateMigrationNotes(changes)}
`;

    return {
      id: 'architecture-changes',
      title: 'Architecture Changes',
      content: content.trim(),
      type: SectionType.ARCHITECTURE_CHANGES,
      required: true,
      order: 3
    };
  }

  private generateSchemaDefinitions(component: string, architecture: any): PRPSection {
    const schemas = architecture.schemas?.[component] || {};
    
    const content = `
## Schema Definitions

### Database Schema
${schemas.database ? this.formatDatabaseSchema(schemas.database) : 'No database schema required for this component.'}

### API Schema
${schemas.api ? this.formatAPISchema(schemas.api) : 'No API schema defined yet.'}

### Event Schema
${schemas.events ? this.formatEventSchema(schemas.events) : 'No events emitted by this component.'}
`;

    return {
      id: 'schema-definitions',
      title: 'Schema Definitions',
      content: content.trim(),
      type: SectionType.SCHEMA_DEFINITIONS,
      required: true,
      order: 4
    };
  }

  private generateFileStructure(component: string): PRPSection {
    const content = `
## File Structure

\`\`\`
${component}/
├── index.ts              # Main entry point
├── types.ts              # TypeScript type definitions
├── ${component}.service.ts    # Core service logic
├── ${component}.controller.ts # API endpoints
├── ${component}.repository.ts # Data access layer
├── schemas/
│   ├── database.ts       # Database schema
│   └── validation.ts     # Input validation schemas
├── tests/
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
└── README.md            # Component documentation
\`\`\`

### Key Files

- **index.ts**: Exports public API of the component
- **types.ts**: All TypeScript interfaces and types
- **${component}.service.ts**: Business logic implementation
- **${component}.controller.ts**: HTTP request handling
- **${component}.repository.ts**: Database operations
`;

    return {
      id: 'file-structure',
      title: 'File Structure',
      content: content.trim(),
      type: SectionType.FILE_STRUCTURE,
      required: true,
      order: 5
    };
  }

  private generateImplementationOrder(component: string, architecture: any): PRPSection {
    const content = `
## Implementation Order

Follow this sequence for implementing the ${component}:

### Phase 1: Foundation
- [ ] Create directory structure
- [ ] Define TypeScript types and interfaces
- [ ] Set up basic module structure
- [ ] Configure dependency injection

### Phase 2: Core Logic
- [ ] Implement repository layer
- [ ] Create service classes
- [ ] Add business logic
- [ ] Handle error cases

### Phase 3: API Layer
- [ ] Define API routes
- [ ] Implement controllers
- [ ] Add request validation
- [ ] Create response DTOs

### Phase 4: Integration
- [ ] Connect to external services
- [ ] Implement event handlers
- [ ] Add monitoring/logging
- [ ] Configure authentication

### Phase 5: Testing
- [ ] Write unit tests
- [ ] Create integration tests
- [ ] Add performance tests
- [ ] Validate error handling

### Phase 6: Documentation
- [ ] Update API documentation
- [ ] Create usage examples
- [ ] Document configuration
- [ ] Add troubleshooting guide
`;

    return {
      id: 'implementation-order',
      title: 'Implementation Order',
      content: content.trim(),
      type: SectionType.IMPLEMENTATION_ORDER,
      required: true,
      order: 6
    };
  }

  private generateValidationCheckpoints(component: string): PRPSection {
    const content = `
## Validation Checkpoints

### Code Quality
- [ ] All tests passing (unit and integration)
- [ ] Code coverage >80%
- [ ] No linting errors
- [ ] TypeScript strict mode compliance

### Architecture Compliance
- [ ] Follows defined patterns
- [ ] Dependency rules enforced
- [ ] API contracts match specification
- [ ] Database schema validated

### Security
- [ ] Input validation implemented
- [ ] Authentication/authorization in place
- [ ] Sensitive data encrypted
- [ ] Security headers configured

### Performance
- [ ] Response times <200ms (p95)
- [ ] Memory usage within limits
- [ ] Database queries optimized
- [ ] Caching strategy implemented

### Documentation
- [ ] API documentation complete
- [ ] Code comments added
- [ ] README updated
- [ ] Architecture diagrams current

### Deployment Readiness
- [ ] Environment variables documented
- [ ] Health checks implemented
- [ ] Monitoring configured
- [ ] Rollback plan defined
`;

    return {
      id: 'validation-checkpoints',
      title: 'Validation Checkpoints',
      content: content.trim(),
      type: SectionType.VALIDATION_CHECKPOINTS,
      required: true,
      order: 7
    };
  }

  // Helper methods

  private async loadArchitecture(): Promise<any> {
    // Load architecture from various sources
    // This is simplified - would load from actual architecture files
    return {
      components: {
        'authentication-service': {
          description: 'Handles user authentication and session management',
          purpose: 'Secure user authentication',
          features: ['Login/logout', 'Session management', 'OAuth integration'],
          dependencies: ['bcrypt', 'jsonwebtoken'],
          integrations: ['user-service', 'api-gateway']
        }
      },
      stack: {
        language: 'TypeScript',
        framework: 'Next.js',
        database: 'PostgreSQL',
        cache: 'Redis'
      },
      patterns: ['Repository pattern', 'Service layer', 'Event-driven']
    };
  }

  private buildMarkdown(
    sections: PRPSection[], 
    preserved: PreservedContent,
    options: RegenerationOptions
  ): string {
    const parts: string[] = [];

    // Add metadata if present
    const metadata = sections.find(s => s.id === 'metadata');
    if (metadata) {
      parts.push(metadata.content);
      parts.push(''); // Empty line after metadata
    }

    // Add title
    const component = sections.find(s => s.type === SectionType.OVERVIEW)?.content.match(/\*\*(.+?)\*\*/)?.[1] || 'Component';
    parts.push(`# PRP: ${component}`);
    parts.push('');

    // Add sections (skip metadata)
    sections.filter(s => s.id !== 'metadata').forEach(section => {
      if (section.content) {
        parts.push(section.content);
        parts.push(''); // Empty line between sections
      }
    });

    // Add preserved implementation notes if any
    if (options.preserveCustomSections && preserved.implementationNotes.length > 0) {
      parts.push('## Implementation Notes');
      parts.push('');
      preserved.implementationNotes.forEach(note => {
        parts.push(`> **Implementation Note**: ${note}`);
        parts.push('');
      });
    }

    return parts.join('\n');
  }

  private formatTitle(id: string): string {
    return id
      .split(/[-_]/)
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }

  private formatChangeType(type: 'added' | 'modified' | 'removed'): string {
    const typeMap = {
      added: '➕ Added',
      modified: '🔄 Modified',
      removed: '❌ Removed'
    };
    return typeMap[type];
  }

  private getActionRequired(change: ArchitectureChange): string {
    switch (change.type) {
      case 'added':
        return 'Implement new functionality to support this addition';
      case 'modified':
        return 'Update existing implementation to match new requirements';
      case 'removed':
        return 'Remove deprecated code and update dependencies';
      default:
        return 'Review and update as needed';
    }
  }

  private generateMigrationNotes(changes: ArchitectureChange[]): string {
    const notes: string[] = [];

    if (changes.some(c => c.type === 'removed')) {
      notes.push('- Plan deprecation strategy for removed components');
      notes.push('- Update all references to removed functionality');
    }

    if (changes.some(c => c.type === 'modified')) {
      notes.push('- Review and update integration points');
      notes.push('- Test backward compatibility');
    }

    if (changes.some(c => c.type === 'added')) {
      notes.push('- Implement new integration points');
      notes.push('- Update documentation for new features');
    }

    return notes.join('\n') || 'No specific migration steps required.';
  }

  private formatDatabaseSchema(schema: any): string {
    // Format database schema - simplified
    return '```sql\n-- Database schema will be generated from architecture\n```';
  }

  private formatAPISchema(schema: any): string {
    // Format API schema - simplified
    return '```typescript\n// API schema will be generated from architecture\n```';
  }

  private formatEventSchema(schema: any): string {
    // Format event schema - simplified
    return '```typescript\n// Event schema will be generated from architecture\n```';
  }
}
