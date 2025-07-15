export const fieldTypes = {
  text: 'string',
  number: 'number',
  boolean: 'boolean',
  date: 'Date',
  array: 'array',
  object: 'object'
};

export type FieldType = keyof typeof fieldTypes;
