export interface FieldDefinition {
  name: string;
  type: string;
  required: boolean;
  validation?: any;
  sensitive?: boolean;
  pii?: boolean;
}

export interface FieldCategory {
  name: string;
  description: string;
  fields: string[];
}
