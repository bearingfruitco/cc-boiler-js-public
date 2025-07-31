/**
 * Documentation Updater Types
 * Defines structures for automatic documentation updates
 */

export interface DocumentationUpdate {
  id: string;
  type: UpdateType;
  targetFile: string;
  sourceFiles: string[];
  changes: DocumentationChange[];
  timestamp: string;
  status: UpdateStatus;
}

export enum UpdateType {
  COMPONENT_ADDED = 'component_added',
  COMPONENT_MODIFIED = 'component_modified',
  API_ADDED = 'api_added',
  API_MODIFIED = 'api_modified',
  SCHEMA_CHANGED = 'schema_changed',
  TYPE_MODIFIED = 'type_modified',
  EXAMPLE_UPDATED = 'example_updated',
  ARCHITECTURE_CHANGED = 'architecture_changed'
}

export enum UpdateStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed',
  SKIPPED = 'skipped'
}

export interface DocumentationChange {
  section: string;
  type: 'added' | 'modified' | 'removed';
  content: string;
  reason: string;
}

export interface FileChange {
  path: string;
  type: 'added' | 'modified' | 'removed';
  language: string;
  changes: CodeChange[];
}

export interface CodeChange {
  type: ChangeType;
  name: string;
  signature?: string;
  description?: string;
  examples?: string[];
  metadata?: Record<string, any>;
}

export enum ChangeType {
  FUNCTION_ADDED = 'function_added',
  FUNCTION_MODIFIED = 'function_modified',
  FUNCTION_REMOVED = 'function_removed',
  CLASS_ADDED = 'class_added',
  CLASS_MODIFIED = 'class_modified',
  TYPE_ADDED = 'type_added',
  TYPE_MODIFIED = 'type_modified',
  EXPORT_ADDED = 'export_added',
  EXPORT_MODIFIED = 'export_modified',
  API_ENDPOINT_ADDED = 'api_endpoint_added',
  API_ENDPOINT_MODIFIED = 'api_endpoint_modified',
  SCHEMA_FIELD_ADDED = 'schema_field_added',
  SCHEMA_FIELD_MODIFIED = 'schema_field_modified'
}

export interface DocumentationMapping {
  sourcePattern: string;
  targetDoc: string;
  updateStrategy: UpdateStrategy;
  sections: SectionMapping[];
}

export interface SectionMapping {
  sectionName: string;
  sourceType: SourceType;
  template?: string;
  preserveCustom: boolean;
}

export enum SourceType {
  JSDOC = 'jsdoc',
  TYPESCRIPT = 'typescript',
  API_ROUTE = 'api_route',
  SCHEMA = 'schema',
  COMPONENT = 'component',
  HOOK = 'hook'
}

export enum UpdateStrategy {
  FULL_REGENERATE = 'full_regenerate',
  SECTION_UPDATE = 'section_update',
  APPEND_ONLY = 'append_only',
  MERGE = 'merge'
}

export interface DocUpdaterConfig {
  mappings: DocumentationMapping[];
  excludePatterns: string[];
  customSections: string[];
  autoCommit: boolean;
  commitMessage: string;
}

export interface ParsedComponent {
  name: string;
  type: 'function' | 'class' | 'const';
  props?: PropDefinition[];
  methods?: MethodDefinition[];
  description?: string;
  examples?: string[];
  exports: string[];
}

export interface PropDefinition {
  name: string;
  type: string;
  required: boolean;
  defaultValue?: string;
  description?: string;
}

export interface MethodDefinition {
  name: string;
  signature: string;
  description?: string;
  parameters: ParameterDefinition[];
  returnType: string;
}

export interface ParameterDefinition {
  name: string;
  type: string;
  description?: string;
  optional: boolean;
}

export interface APIEndpoint {
  path: string;
  method: string;
  description?: string;
  parameters: APIParameter[];
  requestBody?: RequestBody;
  responses: APIResponse[];
  authentication?: boolean;
}

export interface APIParameter {
  name: string;
  in: 'path' | 'query' | 'header';
  type: string;
  required: boolean;
  description?: string;
}

export interface RequestBody {
  contentType: string;
  schema: any;
  examples?: Record<string, any>;
}

export interface APIResponse {
  status: number;
  description: string;
  schema?: any;
  examples?: Record<string, any>;
}

export interface DocumentationSection {
  id: string;
  title: string;
  content: string;
  order: number;
  isCustom: boolean;
  lastUpdated: string;
  sourceFiles?: string[];
}

export interface UpdateResult {
  success: boolean;
  updatedFiles: string[];
  changes: DocumentationChange[];
  errors?: string[];
  warnings?: string[];
}
