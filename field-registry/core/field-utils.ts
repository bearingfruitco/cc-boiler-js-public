import { isPIIField } from './pii-fields';
import { cookiesFields } from './cookies-fields';

export interface FieldDefinition {
  name: string;
  type: string;
  required: boolean;
  validation?: any;
  sensitive?: boolean;
  pii?: boolean;
}

export function getFieldDefinition(fieldName: string): FieldDefinition {
  return {
    name: fieldName,
    type: 'string',
    required: false,
    sensitive: isPIIField(fieldName),
    pii: isPIIField(fieldName)
  };
}

export function getPIIFields(): string[] {
  return [
    'email', 'phone', 'ssn', 'first_name', 'last_name',
    'date_of_birth', 'address', 'credit_card', 'bank_account'
  ];
}

export function getPrepopulatableFields(): string[] {
  const prepopulatable = [
    ...cookiesFields.tracking,
    ...cookiesFields.device,
    ...cookiesFields.geographic,
    'state', 'zip_code', 'source', 'medium'
  ];
  return [...new Set(prepopulatable)];
}
