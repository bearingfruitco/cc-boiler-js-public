import { promises as fs } from 'fs';
import path from 'path';
import {
  ParsedComponent,
  APIEndpoint,
  DocumentationSection,
  UpdateType,
  CodeChange,
  ChangeType,
  PropDefinition
} from './types';

/**
 * Generates and updates documentation based on code analysis
 */
export class DocumentationGenerator {
  private templatePath: string;

  constructor(projectRoot: string = '.') {
    this.templatePath = path.join(projectRoot, 'lib/doc-updater/templates');
  }

  /**
   * Generate component documentation
   */
  async generateComponentDoc(component: ParsedComponent): Promise<string> {
    const sections: string[] = [];

    // Title and description
    sections.push(`# ${component.name}`);
    sections.push('');
    if (component.description) {
      sections.push(component.description);
      sections.push('');
    }

    // Import statement
    sections.push('## Import');
    sections.push('');
    sections.push('```typescript');
    sections.push(`import { ${component.name} } from '@/components/${component.name}';`);
    sections.push('```');
    sections.push('');

    // Props
    if (component.props && component.props.length > 0) {
      sections.push('## Props');
      sections.push('');
      sections.push('| Prop | Type | Required | Default | Description |');
      sections.push('|------|------|----------|---------|-------------|');
      
      component.props.forEach(prop => {
        const required = prop.required ? 'Yes' : 'No';
        const defaultVal = prop.defaultValue || '-';
        const desc = prop.description || '-';
        sections.push(`| ${prop.name} | \`${prop.type}\` | ${required} | ${defaultVal} | ${desc} |`);
      });
      sections.push('');
    }

    // Examples
    if (component.examples && component.examples.length > 0) {
      sections.push('## Examples');
      sections.push('');
      component.examples.forEach((example, index) => {
        if (component.examples!.length > 1) {
          sections.push(`### Example ${index + 1}`);
          sections.push('');
        }
        sections.push('```tsx');
        sections.push(example.trim());
        sections.push('```');
        sections.push('');
      });
    } else {
      // Generate basic example
      sections.push('## Basic Usage');
      sections.push('');
      sections.push('```tsx');
      sections.push(this.generateBasicExample(component));
      sections.push('```');
      sections.push('');
    }

    // Component details
    sections.push('## Component Details');
    sections.push('');
    sections.push(`- **Type**: ${component.type} component`);
    sections.push(`- **Export**: ${component.exports.join(', ')}`);
    sections.push('');

    return sections.join('\n');
  }

  /**
   * Generate API documentation
   */
  async generateAPIDoc(endpoints: APIEndpoint[]): Promise<string> {
    const sections: string[] = [];
    const groupedEndpoints = this.groupEndpointsByPath(endpoints);

    // Title
    sections.push('# API Documentation');
    sections.push('');

    // Table of contents
    if (Object.keys(groupedEndpoints).length > 1) {
      sections.push('## Table of Contents');
      sections.push('');
      Object.keys(groupedEndpoints).forEach(path => {
        sections.push(`- [${path}](#${this.pathToAnchor(path)})`);
      });
      sections.push('');
    }

    // Endpoints
    Object.entries(groupedEndpoints).forEach(([path, pathEndpoints]) => {
      sections.push(`## ${path}`);
      sections.push('');

      pathEndpoints.forEach(endpoint => {
        sections.push(`### ${endpoint.method} ${endpoint.path}`);
        sections.push('');
        
        if (endpoint.description) {
          sections.push(endpoint.description);
          sections.push('');
        }

        // Authentication
        if (endpoint.authentication) {
          sections.push('**Authentication Required**: Yes');
          sections.push('');
        }

        // Parameters
        if (endpoint.parameters && endpoint.parameters.length > 0) {
          sections.push('#### Parameters');
          sections.push('');
          sections.push('| Name | Type | In | Required | Description |');
          sections.push('|------|------|----|----------|-------------|');
          
          endpoint.parameters.forEach(param => {
            const required = param.required ? 'Yes' : 'No';
            const desc = param.description || '-';
            sections.push(`| ${param.name} | \`${param.type}\` | ${param.in} | ${required} | ${desc} |`);
          });
          sections.push('');
        }

        // Request body
        if (endpoint.requestBody) {
          sections.push('#### Request Body');
          sections.push('');
          sections.push(`Content-Type: \`${endpoint.requestBody.contentType}\``);
          sections.push('');
          sections.push('```json');
          sections.push(JSON.stringify(endpoint.requestBody.schema, null, 2));
          sections.push('```');
          sections.push('');
        }

        // Responses
        sections.push('#### Responses');
        sections.push('');
        sections.push('| Status | Description |');
        sections.push('|--------|-------------|');
        
        endpoint.responses.forEach(response => {
          sections.push(`| ${response.status} | ${response.description} |`);
        });
        sections.push('');

        // Examples
        if (endpoint.requestBody?.examples) {
          sections.push('#### Example Request');
          sections.push('');
          sections.push('```bash');
          sections.push(this.generateCurlExample(endpoint));
          sections.push('```');
          sections.push('');
        }
      });
    });

    return sections.join('\n');
  }

  /**
   * Update existing documentation
   */
  async updateDocumentation(
    docPath: string,
    changes: CodeChange[],
    preserveCustom: boolean = true
  ): Promise<string> {
    let content = '';
    
    try {
      content = await fs.readFile(docPath, 'utf-8');
    } catch {
      // File doesn't exist, create new
      return this.generateNewDocumentation(changes);
    }

    const sections = this.parseDocumentSections(content);
    const updatedSections = this.updateSections(sections, changes);

    if (preserveCustom) {
      // Preserve custom sections
      const customSections = sections.filter(s => s.isCustom);
      updatedSections.push(...customSections);
    }

    // Sort sections by order
    updatedSections.sort((a, b) => a.order - b.order);

    // Build updated content
    return updatedSections.map(s => s.content).join('\n\n');
  }

  /**
   * Generate documentation for a new file
   */
  private generateNewDocumentation(changes: CodeChange[]): string {
    const sections: string[] = [];
    const components = changes.filter(c => c.type === ChangeType.CLASS_ADDED);
    const functions = changes.filter(c => c.type === ChangeType.FUNCTION_ADDED);
    const types = changes.filter(c => c.type === ChangeType.TYPE_ADDED);

    // Title
    sections.push('# Documentation');
    sections.push('');
    sections.push('> Auto-generated documentation');
    sections.push('');

    // Components
    if (components.length > 0) {
      sections.push('## Components');
      sections.push('');
      components.forEach(comp => {
        sections.push(`### ${comp.name}`);
        sections.push('');
        if (comp.description) {
          sections.push(comp.description);
          sections.push('');
        }
      });
    }

    // Functions
    if (functions.length > 0) {
      sections.push('## Functions');
      sections.push('');
      functions.forEach(func => {
        sections.push(`### ${func.name}`);
        sections.push('');
        sections.push('```typescript');
        sections.push(func.signature || `function ${func.name}()`);
        sections.push('```');
        sections.push('');
        if (func.description) {
          sections.push(func.description);
          sections.push('');
        }
      });
    }

    // Types
    if (types.length > 0) {
      sections.push('## Types');
      sections.push('');
      types.forEach(type => {
        sections.push(`### ${type.name}`);
        sections.push('');
        if (type.description) {
          sections.push(type.description);
          sections.push('');
        }
      });
    }

    return sections.join('\n');
  }

  /**
   * Parse document into sections
   */
  private parseDocumentSections(content: string): DocumentationSection[] {
    const sections: DocumentationSection[] = [];
    const lines = content.split('\n');
    let currentSection: DocumentationSection | null = null;
    let sectionContent: string[] = [];
    let order = 0;

    lines.forEach((line, index) => {
      if (line.startsWith('#')) {
        // Save previous section
        if (currentSection) {
          currentSection.content = sectionContent.join('\n').trim();
          sections.push(currentSection);
        }

        // Start new section
        const title = line.replace(/^#+\s*/, '');
        currentSection = {
          id: this.titleToId(title),
          title,
          content: '',
          order: order++,
          isCustom: this.isCustomSection(title),
          lastUpdated: new Date().toISOString()
        };
        sectionContent = [line];
      } else if (currentSection) {
        sectionContent.push(line);
      }
    });

    // Save last section
    if (currentSection) {
      currentSection.content = sectionContent.join('\n').trim();
      sections.push(currentSection);
    }

    return sections;
  }

  /**
   * Update sections based on changes
   */
  private updateSections(
    sections: DocumentationSection[],
    changes: CodeChange[]
  ): DocumentationSection[] {
    const updatedSections = [...sections];

    // Group changes by type
    const components = changes.filter(c => c.type === ChangeType.CLASS_ADDED || c.type === ChangeType.CLASS_MODIFIED);
    const functions = changes.filter(c => c.type === ChangeType.FUNCTION_ADDED || c.type === ChangeType.FUNCTION_MODIFIED);

    // Update component sections
    if (components.length > 0) {
      const componentSection = updatedSections.find(s => s.id === 'components');
      if (componentSection) {
        // Update existing section
        componentSection.content = this.updateComponentSection(componentSection.content, components);
        componentSection.lastUpdated = new Date().toISOString();
      } else {
        // Add new section
        updatedSections.push({
          id: 'components',
          title: 'Components',
          content: this.generateComponentSection(components),
          order: 10,
          isCustom: false,
          lastUpdated: new Date().toISOString()
        });
      }
    }

    return updatedSections;
  }

  /**
   * Helper methods
   */

  private generateBasicExample(component: ParsedComponent): string {
    if (component.props && component.props.length > 0) {
      const requiredProps = component.props
        .filter(p => p.required)
        .map(p => `  ${p.name}={${this.getExampleValue(p)}}`)
        .join('\n');
      
      if (requiredProps) {
        return `<${component.name}\n${requiredProps}\n/>`;
      }
    }
    return `<${component.name} />`;
  }

  private getExampleValue(prop: PropDefinition): string {
    switch (prop.type) {
      case 'string':
        return `"example"`;
      case 'number':
        return '42';
      case 'boolean':
        return 'true';
      case 'function':
        return '() => {}';
      default:
        return '{}';
    }
  }

  private groupEndpointsByPath(endpoints: APIEndpoint[]): Record<string, APIEndpoint[]> {
    const grouped: Record<string, APIEndpoint[]> = {};
    
    endpoints.forEach(endpoint => {
      const basePath = endpoint.path.split('/').slice(0, 3).join('/');
      if (!grouped[basePath]) {
        grouped[basePath] = [];
      }
      grouped[basePath].push(endpoint);
    });

    return grouped;
  }

  private pathToAnchor(path: string): string {
    return path.toLowerCase().replace(/[^a-z0-9]/g, '-');
  }

  private generateCurlExample(endpoint: APIEndpoint): string {
    const lines = [`curl -X ${endpoint.method} \\`];
    lines.push(`  'http://localhost:3000${endpoint.path}' \\`);
    
    if (endpoint.authentication) {
      lines.push(`  -H 'Authorization: Bearer YOUR_TOKEN' \\`);
    }
    
    if (endpoint.requestBody) {
      lines.push(`  -H 'Content-Type: ${endpoint.requestBody.contentType}' \\`);
      const exampleData = endpoint.requestBody.examples?.default || endpoint.requestBody.schema;
      lines.push(`  -d '${JSON.stringify(exampleData)}'`);
    } else {
      // Remove trailing backslash from last line
      lines[lines.length - 1] = lines[lines.length - 1].replace(' \\', '');
    }

    return lines.join('\n  ');
  }

  private titleToId(title: string): string {
    return title.toLowerCase().replace(/[^a-z0-9]/g, '-');
  }

  private isCustomSection(title: string): boolean {
    const standardSections = [
      'components', 'props', 'examples', 'api', 'functions',
      'types', 'import', 'usage', 'parameters', 'returns'
    ];
    const titleLower = title.toLowerCase();
    return !standardSections.some(section => titleLower.includes(section));
  }

  private updateComponentSection(content: string, components: CodeChange[]): string {
    // This would intelligently merge new component info with existing
    // For now, just append
    const newComponents = components
      .filter(c => !content.includes(c.name))
      .map(c => `### ${c.name}\n\n${c.description || 'No description available.'}`)
      .join('\n\n');

    if (newComponents) {
      return content + '\n\n' + newComponents;
    }

    return content;
  }

  private generateComponentSection(components: CodeChange[]): string {
    const sections = ['## Components', ''];
    
    components.forEach(comp => {
      sections.push(`### ${comp.name}`);
      sections.push('');
      if (comp.description) {
        sections.push(comp.description);
        sections.push('');
      }
    });

    return sections.join('\n');
  }
}
