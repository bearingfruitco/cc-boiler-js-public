// Core field registry exports
// Import JSON data with proper TypeScript support

import cookiesData from './cookies.json';
import deviceData from './device.json';
import geographicData from './geographic.json';
import journeyData from './journey.json';
import trackingData from './tracking.json';

// Type definitions for field registry
export interface FieldDefinition {
  type: 'STRING' | 'NUMBER' | 'BOOLEAN' | 'DATE' | 'JSON';
  pii?: boolean;
  phi?: boolean;
  sensitive?: boolean;
  prepopulate?: boolean;
  clientVisible?: boolean;
  auditLog?: boolean;
  encryption?: 'none' | 'transit' | 'field';
  masking?: 'none' | 'partial' | 'full';
  description?: string;
  validation?: any;
}

export interface FieldRegistry {
  [key: string]: FieldDefinition;
}

// Export typed field registries
export const cookiesFields: FieldRegistry = cookiesData as FieldRegistry;
export const deviceFields: FieldRegistry = deviceData as FieldRegistry;
export const geographicFields: FieldRegistry = geographicData as FieldRegistry;
export const journeyFields: FieldRegistry = journeyData as FieldRegistry;
export const trackingFields: FieldRegistry = trackingData as FieldRegistry;

// Combined registry
export const coreFields: FieldRegistry = {
  ...cookiesFields,
  ...deviceFields,
  ...geographicFields,
  ...journeyFields,
  ...trackingFields,
};

// Helper to get field definition
export function getFieldDefinition(fieldName: string): FieldDefinition | undefined {
  return coreFields[fieldName];
}

// Helper to get PII fields
export function getPIIFields(): string[] {
  return Object.entries(coreFields)
    .filter(([_, def]) => def.pii === true)
    .map(([name]) => name);
}

// Helper to get prepopulatable fields
export function getPrepopulatableFields(): string[] {
  return Object.entries(coreFields)
    .filter(([_, def]) => def.prepopulate === true)
    .map(([name]) => name);
}
