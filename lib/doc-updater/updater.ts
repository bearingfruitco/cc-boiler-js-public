import { promises as fs } from 'fs';
import path from 'path';
import { CodeAnalyzer } from './analyzer';
import { DocumentationGenerator } from './generator';
import {
  DocumentationUpdate,
  UpdateType,
  UpdateStatus,
  DocumentationMapping,
  UpdateStrategy,
  DocUpdaterConfig,
  FileChange,
  UpdateResult,
  DocumentationChange
} from './types';

/**
 * Main class for automatic documentation updates
 */
export class DocumentationUpdater {
  private analyzer: CodeAnalyzer;
  private generator: DocumentationGenerator;
  private config: DocUpdaterConfig;
  private projectRoot: string;
  private updateQueue: DocumentationUpdate[] = [];

  constructor(projectRoot: string = '.', config?: Partial<DocUpdaterConfig>) {
    this.projectRoot = projectRoot;
    this.analyzer = new CodeAnalyzer();
    this.generator = new DocumentationGenerator(projectRoot);
    this.config = {
      mappings: this.getDefaultMappings(),
      excludePatterns: [
        '**/node_modules/**',
        '**/dist/**',
        '**/build/**',
        '**/*.test.*',
        '**/*.spec.*'
      ],
      customSections: [
        'Notes',
        'FAQ',
        'Troubleshooting',
        'Migration Guide'
      ],
      autoCommit: false,
      commitMessage: 'docs: auto-update documentation',
      ...config
    };
  }

  /**
   * Process file changes and update documentation
   */
  async processFileChanges(changedFiles: string[]): Promise<UpdateResult> {
    const result: UpdateResult = {
      success: true,
      updatedFiles: [],
      changes: [],
      warnings: []
    };

    try {
      // Filter out excluded files
      const filesToProcess = changedFiles.filter(file => 
        !this.isExcluded(file)
      );

      // Analyze changed files
      const fileChanges: FileChange[] = [];
      for (const file of filesToProcess) {
        try {
          const change = await this.analyzer.analyzeFile(file);
          fileChanges.push(change);
        } catch (error) {
          result.warnings?.push(`Failed to analyze ${file}: ${error}`);
        }
      }

      // Group changes by documentation target
      const docUpdates = this.groupChangesByDoc(fileChanges);

      // Process each documentation update
      for (const [docPath, changes] of docUpdates) {
        try {
          const updated = await this.updateDocumentation(docPath, changes);
          if (updated) {
            result.updatedFiles.push(docPath);
            result.changes.push(...updated);
          }
        } catch (error) {
          result.warnings?.push(`Failed to update ${docPath}: ${error}`);
        }
      }

      // Auto-commit if configured
      if (this.config.autoCommit && result.updatedFiles.length > 0) {
        await this.commitChanges(result.updatedFiles);
      }

    } catch (error) {
      result.success = false;
      result.errors = [error instanceof Error ? error.message : 'Unknown error'];
    }

    return result;
  }

  /**
   * Update documentation for specific changes
   */
  private async updateDocumentation(
    docPath: string,
    changes: FileChange[]
  ): Promise<DocumentationChange[]> {
    const fullDocPath = path.join(this.projectRoot, docPath);
    const documentChanges: DocumentationChange[] = [];

    // Find mapping for this documentation
    const mapping = this.config.mappings.find(m => m.targetDoc === docPath);
    if (!mapping) {
      throw new Error(`No mapping found for ${docPath}`);
    }

    // Determine update strategy
    switch (mapping.updateStrategy) {
      case UpdateStrategy.FULL_REGENERATE:
        const newContent = await this.regenerateDocumentation(changes, mapping);
        await fs.writeFile(fullDocPath, newContent);
        documentChanges.push({
          section: 'Full Document',
          type: 'modified',
          content: newContent,
          reason: 'Complete regeneration based on code changes'
        });
        break;

      case UpdateStrategy.SECTION_UPDATE:
        const sectionChanges = await this.updateSections(fullDocPath, changes, mapping);
        documentChanges.push(...sectionChanges);
        break;

      case UpdateStrategy.APPEND_ONLY:
        const appendedContent = await this.appendToDocumentation(fullDocPath, changes, mapping);
        if (appendedContent) {
          documentChanges.push({
            section: 'Appended Content',
            type: 'added',
            content: appendedContent,
            reason: 'New content appended'
          });
        }
        break;

      case UpdateStrategy.MERGE:
        const mergedChanges = await this.mergeDocumentation(fullDocPath, changes, mapping);
        documentChanges.push(...mergedChanges);
        break;
    }

    return documentChanges;
  }

  /**
   * Regenerate entire documentation
   */
  private async regenerateDocumentation(
    changes: FileChange[],
    mapping: DocumentationMapping
  ): Promise<string> {
    // Extract all code changes
    const allChanges = changes.flatMap(fc => fc.changes);
    
    // Generate based on type
    if (mapping.targetDoc.includes('/api/')) {
      // API documentation
      const endpoints = allChanges
        .filter(c => c.type.includes('API_ENDPOINT'))
        .map(c => c.metadata as any);
      return await this.generator.generateAPIDoc(endpoints);
    } else if (mapping.targetDoc.includes('/components/')) {
      // Component documentation
      const components = allChanges
        .filter(c => c.type.includes('CLASS'))
        .map(c => ({
          name: c.name,
          description: c.description,
          type: 'function' as const,
          props: c.metadata?.props || [],
          examples: c.examples || [],
          exports: [c.name]
        }));
      
      if (components.length > 0) {
        return await this.generator.generateComponentDoc(components[0]);
      }
    }

    // Default generation
    return await this.generator.updateDocumentation(
      mapping.targetDoc,
      allChanges,
      true
    );
  }

  /**
   * Update specific sections
   */
  private async updateSections(
    docPath: string,
    changes: FileChange[],
    mapping: DocumentationMapping
  ): Promise<DocumentationChange[]> {
    const documentChanges: DocumentationChange[] = [];
    
    try {
      const content = await fs.readFile(docPath, 'utf-8');
      const allChanges = changes.flatMap(fc => fc.changes);
      
      // Update documentation preserving custom sections
      const updatedContent = await this.generator.updateDocumentation(
        docPath,
        allChanges,
        true
      );

      if (updatedContent !== content) {
        await fs.writeFile(docPath, updatedContent);
        documentChanges.push({
          section: 'Multiple Sections',
          type: 'modified',
          content: updatedContent,
          reason: 'Sections updated based on code changes'
        });
      }
    } catch (error) {
      // File doesn't exist, create it
      const allChanges = changes.flatMap(fc => fc.changes);
      const newContent = await this.generator.updateDocumentation(
        docPath,
        allChanges,
        false
      );
      
      await fs.mkdir(path.dirname(docPath), { recursive: true });
      await fs.writeFile(docPath, newContent);
      
      documentChanges.push({
        section: 'New Document',
        type: 'added',
        content: newContent,
        reason: 'Documentation created for new code'
      });
    }

    return documentChanges;
  }

  /**
   * Append to existing documentation
   */
  private async appendToDocumentation(
    docPath: string,
    changes: FileChange[],
    mapping: DocumentationMapping
  ): Promise<string | null> {
    try {
      const existingContent = await fs.readFile(docPath, 'utf-8');
      const allChanges = changes.flatMap(fc => fc.changes);
      
      // Generate content for new items only
      const newItems = allChanges.filter(c => 
        c.type.includes('ADDED') && !existingContent.includes(c.name)
      );

      if (newItems.length === 0) {
        return null;
      }

      // Generate new content
      const newContent = await this.generateAppendContent(newItems);
      
      // Append to file
      const updatedContent = existingContent + '\n\n' + newContent;
      await fs.writeFile(docPath, updatedContent);
      
      return newContent;
    } catch {
      // File doesn't exist, create with full content
      const allChanges = changes.flatMap(fc => fc.changes);
      const content = await this.generator.updateDocumentation(docPath, allChanges, false);
      
      await fs.mkdir(path.dirname(docPath), { recursive: true });
      await fs.writeFile(docPath, content);
      
      return content;
    }
  }

  /**
   * Merge documentation changes
   */
  private async mergeDocumentation(
    docPath: string,
    changes: FileChange[],
    mapping: DocumentationMapping
  ): Promise<DocumentationChange[]> {
    // This would implement intelligent merging
    // For now, use section update strategy
    return this.updateSections(docPath, changes, mapping);
  }

  /**
   * Generate content to append
   */
  private async generateAppendContent(changes: any[]): Promise<string> {
    const sections: string[] = [];
    const date = new Date().toISOString().split('T')[0];
    
    sections.push(`## Updates - ${date}`);
    sections.push('');

    // Group by type
    const functions = changes.filter(c => c.type.includes('FUNCTION'));
    const components = changes.filter(c => c.type.includes('CLASS'));
    const types = changes.filter(c => c.type.includes('TYPE'));

    if (functions.length > 0) {
      sections.push('### New Functions');
      sections.push('');
      functions.forEach(func => {
        sections.push(`#### ${func.name}`);
        sections.push('');
        if (func.signature) {
          sections.push('```typescript');
          sections.push(func.signature);
          sections.push('```');
          sections.push('');
        }
        if (func.description) {
          sections.push(func.description);
          sections.push('');
        }
      });
    }

    if (components.length > 0) {
      sections.push('### New Components');
      sections.push('');
      components.forEach(comp => {
        sections.push(`#### ${comp.name}`);
        sections.push('');
        if (comp.description) {
          sections.push(comp.description);
          sections.push('');
        }
      });
    }

    if (types.length > 0) {
      sections.push('### New Types');
      sections.push('');
      types.forEach(type => {
        sections.push(`#### ${type.name}`);
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
   * Group file changes by target documentation
   */
  private groupChangesByDoc(changes: FileChange[]): Map<string, FileChange[]> {
    const grouped = new Map<string, FileChange[]>();

    changes.forEach(change => {
      const mapping = this.findMapping(change.path);
      if (mapping) {
        if (!grouped.has(mapping.targetDoc)) {
          grouped.set(mapping.targetDoc, []);
        }
        grouped.get(mapping.targetDoc)!.push(change);
      }
    });

    return grouped;
  }

  /**
   * Find documentation mapping for a source file
   */
  private findMapping(filePath: string): DocumentationMapping | null {
    return this.config.mappings.find(mapping => {
      const pattern = new RegExp(mapping.sourcePattern);
      return pattern.test(filePath);
    }) || null;
  }

  /**
   * Check if file is excluded
   */
  private isExcluded(filePath: string): boolean {
    return this.config.excludePatterns.some(pattern => {
      const regex = new RegExp(pattern.replace(/\*/g, '.*'));
      return regex.test(filePath);
    });
  }

  /**
   * Commit documentation changes
   */
  private async commitChanges(files: string[]): Promise<void> {
    // This would use git commands to commit
    // For now, just log
    console.log(`Would commit ${files.length} documentation files`);
  }

  /**
   * Get default documentation mappings
   */
  private getDefaultMappings(): DocumentationMapping[] {
    return [
      {
        sourcePattern: 'components/.*\\.tsx?$',
        targetDoc: 'docs/components/${name}.md',
        updateStrategy: UpdateStrategy.SECTION_UPDATE,
        sections: [
          {
            sectionName: 'Props',
            sourceType: 'typescript' as any,
            preserveCustom: true
          },
          {
            sectionName: 'Examples',
            sourceType: 'jsdoc' as any,
            preserveCustom: true
          }
        ]
      },
      {
        sourcePattern: 'app/api/.*/route\\.ts$',
        targetDoc: 'docs/api/${path}.md',
        updateStrategy: UpdateStrategy.FULL_REGENERATE,
        sections: [
          {
            sectionName: 'Endpoints',
            sourceType: 'api_route' as any,
            preserveCustom: false
          }
        ]
      },
      {
        sourcePattern: 'lib/.*\\.ts$',
        targetDoc: 'docs/lib/${name}.md',
        updateStrategy: UpdateStrategy.MERGE,
        sections: [
          {
            sectionName: 'Functions',
            sourceType: 'typescript' as any,
            preserveCustom: true
          }
        ]
      },
      {
        sourcePattern: 'types/.*\\.ts$',
        targetDoc: 'docs/types.md',
        updateStrategy: UpdateStrategy.APPEND_ONLY,
        sections: [
          {
            sectionName: 'Type Definitions',
            sourceType: 'typescript' as any,
            preserveCustom: true
          }
        ]
      }
    ];
  }
}
