/**
 * Requirement Locking Schema
 * Defines the structure for locked requirements to prevent drift
 */

export interface ValidationRule {
  type: 'exact_count' | 'minimum' | 'maximum' | 'includes' | 'pattern';
  field: string;
  value: any;
  errorMessage: string;
}

export interface LockedRequirement {
  id: string;
  source: {
    type: 'github_issue' | 'prd' | 'manual';
    reference: string; // Issue #42, PRD name, etc.
    url?: string;
  };
  component: string;
  requirements: {
    fields?: { 
      count: number; 
      names: string[];
      required: string[];
      optional?: string[];
    };
    features?: string[];
    constraints?: string[];
    validations?: ValidationRule[];
    ui?: {
      minHeight?: string;
      maxFields?: number;
      layout?: 'vertical' | 'horizontal' | 'grid';
    };
  };
  locked: boolean;
  lockedAt: Date;
  lockedBy: string;
  version: number;
  description?: string;
  testRequirements?: {
    coverage: number;
    e2e: boolean;
    accessibility: boolean;
  };
}

export interface RequirementViolation {
  component: string;
  requirement: string;
  expected: any;
  actual: any;
  severity: 'critical' | 'high' | 'medium' | 'low';
  suggestion: string;
}

export interface ContextAnchor {
  id: string;
  text: string;
  priority: 'critical' | 'high' | 'normal';
  source: string;
  createdAt: Date;
  immutable: boolean;
  expiresAt?: Date;
}
