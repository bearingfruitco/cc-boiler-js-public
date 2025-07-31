/**
 * PRP Regenerator Types
 * Defines the structure for PRP regeneration based on architecture changes
 */

export interface PRPMetadata {
  id: string;
  component: string;
  version: string;
  lastGenerated: string;
  architectureVersion: string;
  status: PRPStatus;
  customSections?: string[];
}

export enum PRPStatus {
  DRAFT = 'draft',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  OUTDATED = 'outdated',
  ARCHIVED = 'archived'
}

export interface PRPContent {
  metadata: PRPMetadata;
  sections: PRPSection[];
  completionStatus: CompletionStatus;
  customContent: Record<string, string>;
}

export interface PRPSection {
  id: string;
  title: string;
  content: string;
  type: SectionType;
  required: boolean;
  order: number;
  lastModified?: string;
  isCustom?: boolean;
}

export enum SectionType {
  OVERVIEW = 'overview',
  TECHNICAL_CONTEXT = 'technical_context',
  ARCHITECTURE_CHANGES = 'architecture_changes',
  SCHEMA_DEFINITIONS = 'schema_definitions',
  FILE_STRUCTURE = 'file_structure',
  VALIDATION_CHECKPOINTS = 'validation_checkpoints',
  IMPLEMENTATION_ORDER = 'implementation_order',
  MIGRATION_NOTES = 'migration_notes',
  CUSTOM = 'custom'
}

export interface CompletionStatus {
  totalTasks: number;
  completedTasks: number;
  checkboxes: CheckboxStatus[];
  lastUpdated: string;
}

export interface CheckboxStatus {
  id: string;
  text: string;
  checked: boolean;
  section: string;
  lineNumber: number;
}

export interface ArchitectureChange {
  type: 'added' | 'modified' | 'removed';
  component: string;
  description: string;
  impact: string[];
  requiresPRPUpdate: boolean;
}

export interface PRPRegenerationTask {
  prpFile: string;
  component: string;
  architectureChanges: ArchitectureChange[];
  preserveSections: string[];
  priority: 'high' | 'medium' | 'low';
  reason: string;
}

export interface RegenerationResult {
  success: boolean;
  prpFile: string;
  changes: PRPChange[];
  preserved: PreservedContent;
  warnings?: string[];
  errors?: string[];
}

export interface PRPChange {
  section: string;
  type: 'added' | 'modified' | 'removed';
  description: string;
  diff?: string;
}

export interface PreservedContent {
  completionStatus: CompletionStatus;
  customSections: Record<string, string>;
  implementationNotes: string[];
  validationResults?: any;
}

export interface PRPSyncStatus {
  totalPRPs: number;
  syncedPRPs: number;
  outdatedPRPs: string[];
  missingPRPs: string[];
  lastSync: string;
}

export interface RegenerationOptions {
  preserveProgress: boolean;
  preserveCustomSections: boolean;
  addChangeMarkers: boolean;
  backupOriginal: boolean;
  dryRun: boolean;
}
