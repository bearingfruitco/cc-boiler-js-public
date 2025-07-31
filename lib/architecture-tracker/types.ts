/**
 * Architecture Change Tracker
 * Tracks all changes to the system architecture over time
 */

export interface ArchitectureChange {
  id: string;
  timestamp: string;
  type: ArchitectureChangeType;
  category: ChangeCategory;
  description: string;
  filesAffected: string[];
  relatedPRP?: string;
  author: string;
  rationale: string;
  impact: ChangeImpact;
  metadata?: Record<string, any>;
}

export enum ArchitectureChangeType {
  COMPONENT_ADDED = 'component_added',
  COMPONENT_REMOVED = 'component_removed',
  COMPONENT_MODIFIED = 'component_modified',
  API_ADDED = 'api_added',
  API_REMOVED = 'api_removed',
  API_MODIFIED = 'api_modified',
  DATABASE_SCHEMA_CHANGED = 'database_schema_changed',
  SECURITY_POLICY_UPDATED = 'security_policy_updated',
  TECHNOLOGY_STACK_CHANGED = 'technology_stack_changed',
  INTEGRATION_ADDED = 'integration_added',
  INTEGRATION_REMOVED = 'integration_removed',
  ARCHITECTURE_PATTERN_CHANGED = 'architecture_pattern_changed',
}

export enum ChangeCategory {
  FRONTEND = 'frontend',
  BACKEND = 'backend',
  DATABASE = 'database',
  INFRASTRUCTURE = 'infrastructure',
  SECURITY = 'security',
  INTEGRATION = 'integration',
  DEPLOYMENT = 'deployment',
  MONITORING = 'monitoring',
}

export interface ChangeImpact {
  components: string[];
  estimatedEffort: 'low' | 'medium' | 'high';
  breakingChange: boolean;
  securityImpact?: boolean;
  performanceImpact?: 'positive' | 'negative' | 'neutral';
  dependencies?: string[];
}

export interface ArchitectureSnapshot {
  timestamp: string;
  version: string;
  components: ComponentDefinition[];
  apis: APIDefinition[];
  databases: DatabaseDefinition[];
  integrations: IntegrationDefinition[];
  securityPolicies: SecurityPolicy[];
}

export interface ComponentDefinition {
  id: string;
  name: string;
  type: string;
  description: string;
  dependencies: string[];
  status: 'active' | 'deprecated' | 'removed';
  addedDate: string;
  modifiedDate?: string;
  removedDate?: string;
}

export interface APIDefinition {
  id: string;
  path: string;
  method: string;
  description: string;
  authentication: boolean;
  rateLimit?: string;
  status: 'active' | 'deprecated' | 'removed';
}

export interface DatabaseDefinition {
  id: string;
  name: string;
  type: string;
  tables: string[];
  relationships: string[];
  status: 'active' | 'migrating' | 'deprecated';
}

export interface IntegrationDefinition {
  id: string;
  name: string;
  type: string;
  provider: string;
  configuration: Record<string, any>;
  status: 'active' | 'inactive' | 'deprecated';
}

export interface SecurityPolicy {
  id: string;
  name: string;
  type: string;
  rules: string[];
  enforcement: 'required' | 'recommended';
  addedDate: string;
}
