import { promises as fs } from 'fs';
import path from 'path';
import { 
  PRPContent, 
  CheckboxStatus, 
  CompletionStatus,
  PRPSection,
  SectionType,
  PRPMetadata,
  PRPStatus,
  PreservedContent
} from './types';

/**
 * Parser for existing PRP files to extract content and progress
 */
export class PRPParser {
  /**
   * Parse a PRP markdown file into structured content
   */
  async parsePRP(prpPath: string): Promise<PRPContent> {
    const content = await fs.readFile(prpPath, 'utf-8');
    
    const metadata = this.extractMetadata(content);
    const sections = this.extractSections(content);
    const completionStatus = this.extractCompletionStatus(content);
    const customContent = this.extractCustomContent(content, sections);

    return {
      metadata,
      sections,
      completionStatus,
      customContent
    };
  }

  /**
   * Extract metadata from PRP frontmatter
   */
  private extractMetadata(content: string): PRPMetadata {
    const metadataMatch = content.match(/^---\n([\s\S]*?)\n---/);
    
    if (!metadataMatch) {
      // Create default metadata if none exists
      return {
        id: 'unknown',
        component: 'unknown',
        version: '1.0.0',
        lastGenerated: new Date().toISOString(),
        architectureVersion: 'unknown',
        status: PRPStatus.DRAFT
      };
    }

    const metadataText = metadataMatch[1];
    const metadata: any = {};

    // Parse YAML-like frontmatter
    metadataText.split('\n').forEach(line => {
      const [key, ...valueParts] = line.split(':');
      if (key && valueParts.length > 0) {
        metadata[key.trim()] = valueParts.join(':').trim();
      }
    });

    return {
      id: metadata.id || 'unknown',
      component: metadata.component || 'unknown',
      version: metadata.version || '1.0.0',
      lastGenerated: metadata.lastGenerated || new Date().toISOString(),
      architectureVersion: metadata.architectureVersion || 'unknown',
      status: metadata.status || PRPStatus.DRAFT,
      customSections: metadata.customSections?.split(',').map((s: string) => s.trim())
    };
  }

  /**
   * Extract sections from PRP content
   */
  private extractSections(content: string): PRPSection[] {
    const sections: PRPSection[] = [];
    
    // Remove frontmatter if present
    const mainContent = content.replace(/^---\n[\s\S]*?\n---\n/, '');
    
    // Split by headers
    const sectionRegex = /^(#{1,3})\s+(.+)$/gm;
    let match;
    let lastIndex = 0;
    let sectionOrder = 0;

    while ((match = sectionRegex.exec(mainContent)) !== null) {
      if (lastIndex > 0) {
        // Add previous section content
        const prevSection = sections[sections.length - 1];
        if (prevSection) {
          prevSection.content = mainContent.substring(lastIndex, match.index).trim();
        }
      }

      const level = match[1].length;
      const title = match[2];
      const sectionType = this.inferSectionType(title);
      
      sections.push({
        id: this.generateSectionId(title),
        title,
        content: '', // Will be filled on next iteration
        type: sectionType,
        required: this.isSectionRequired(sectionType),
        order: sectionOrder++,
        isCustom: sectionType === SectionType.CUSTOM
      });

      lastIndex = match.index + match[0].length;
    }

    // Add content for last section
    if (sections.length > 0 && lastIndex < mainContent.length) {
      sections[sections.length - 1].content = mainContent.substring(lastIndex).trim();
    }

    return sections;
  }

  /**
   * Extract completion status from checkboxes
   */
  private extractCompletionStatus(content: string): CompletionStatus {
    const checkboxes: CheckboxStatus[] = [];
    const lines = content.split('\n');
    
    lines.forEach((line, index) => {
      const checkboxMatch = line.match(/^(\s*)-\s+\[([ x])\]\s+(.+)$/);
      if (checkboxMatch) {
        const checked = checkboxMatch[2].toLowerCase() === 'x';
        const text = checkboxMatch[3];
        
        // Find which section this checkbox belongs to
        const section = this.findSectionForLine(lines, index);
        
        checkboxes.push({
          id: `checkbox-${index}`,
          text,
          checked,
          section,
          lineNumber: index + 1
        });
      }
    });

    const completedTasks = checkboxes.filter(cb => cb.checked).length;
    
    return {
      totalTasks: checkboxes.length,
      completedTasks,
      checkboxes,
      lastUpdated: new Date().toISOString()
    };
  }

  /**
   * Extract custom content that doesn't fit standard sections
   */
  private extractCustomContent(content: string, sections: PRPSection[]): Record<string, string> {
    const customContent: Record<string, string> = {};
    
    // Look for sections marked as custom
    sections.forEach(section => {
      if (section.isCustom || section.type === SectionType.CUSTOM) {
        customContent[section.id] = section.content;
      }
    });

    // Look for implementation notes
    const notesMatch = content.match(/## Implementation Notes\n([\s\S]*?)(?=\n##|$)/);
    if (notesMatch) {
      customContent['implementation_notes'] = notesMatch[1].trim();
    }

    // Look for validation results
    const validationMatch = content.match(/## Validation Results\n([\s\S]*?)(?=\n##|$)/);
    if (validationMatch) {
      customContent['validation_results'] = validationMatch[1].trim();
    }

    return customContent;
  }

  /**
   * Extract preserved content for regeneration
   */
  async extractPreservedContent(prpPath: string): Promise<PreservedContent> {
    const prpContent = await this.parsePRP(prpPath);
    
    // Extract implementation notes from custom content
    const implementationNotes: string[] = [];
    if (prpContent.customContent['implementation_notes']) {
      implementationNotes.push(prpContent.customContent['implementation_notes']);
    }

    // Look for inline notes marked with specific patterns
    prpContent.sections.forEach(section => {
      const noteMatches = section.content.matchAll(/> \*\*Implementation Note\*\*: (.+)/g);
      for (const match of noteMatches) {
        implementationNotes.push(match[1]);
      }
    });

    return {
      completionStatus: prpContent.completionStatus,
      customSections: prpContent.customContent,
      implementationNotes,
      validationResults: prpContent.customContent['validation_results']
    };
  }

  /**
   * Helper methods
   */
  
  private inferSectionType(title: string): SectionType {
    const titleLower = title.toLowerCase();
    
    if (titleLower.includes('overview')) return SectionType.OVERVIEW;
    if (titleLower.includes('technical') && titleLower.includes('context')) return SectionType.TECHNICAL_CONTEXT;
    if (titleLower.includes('architecture') && titleLower.includes('change')) return SectionType.ARCHITECTURE_CHANGES;
    if (titleLower.includes('schema')) return SectionType.SCHEMA_DEFINITIONS;
    if (titleLower.includes('file') && titleLower.includes('structure')) return SectionType.FILE_STRUCTURE;
    if (titleLower.includes('validation')) return SectionType.VALIDATION_CHECKPOINTS;
    if (titleLower.includes('implementation') && titleLower.includes('order')) return SectionType.IMPLEMENTATION_ORDER;
    if (titleLower.includes('migration')) return SectionType.MIGRATION_NOTES;
    
    return SectionType.CUSTOM;
  }

  private isSectionRequired(type: SectionType): boolean {
    const requiredSections = [
      SectionType.OVERVIEW,
      SectionType.TECHNICAL_CONTEXT,
      SectionType.FILE_STRUCTURE,
      SectionType.VALIDATION_CHECKPOINTS,
      SectionType.IMPLEMENTATION_ORDER
    ];
    
    return requiredSections.includes(type);
  }

  private generateSectionId(title: string): string {
    return title
      .toLowerCase()
      .replace(/[^a-z0-9]/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '');
  }

  private findSectionForLine(lines: string[], lineIndex: number): string {
    // Search backwards for the nearest header
    for (let i = lineIndex - 1; i >= 0; i--) {
      const headerMatch = lines[i].match(/^#{1,3}\s+(.+)$/);
      if (headerMatch) {
        return headerMatch[1];
      }
    }
    return 'Unknown Section';
  }

  /**
   * Merge checkbox status from old PRP to new content
   */
  mergeCheckboxStatus(newContent: string, oldStatus: CompletionStatus): string {
    const lines = newContent.split('\n');
    const updatedLines: string[] = [];
    
    lines.forEach((line, index) => {
      const checkboxMatch = line.match(/^(\s*)-\s+\[\s*\]\s+(.+)$/);
      if (checkboxMatch) {
        const indent = checkboxMatch[1];
        const text = checkboxMatch[2];
        
        // Find matching checkbox from old status
        const oldCheckbox = oldStatus.checkboxes.find(cb => 
          this.normalizeText(cb.text) === this.normalizeText(text)
        );
        
        if (oldCheckbox && oldCheckbox.checked) {
          // Preserve checked status
          updatedLines.push(`${indent}- [x] ${text}`);
        } else {
          updatedLines.push(line);
        }
      } else {
        updatedLines.push(line);
      }
    });
    
    return updatedLines.join('\n');
  }

  private normalizeText(text: string): string {
    return text.toLowerCase().replace(/[^a-z0-9]/g, '');
  }
}
