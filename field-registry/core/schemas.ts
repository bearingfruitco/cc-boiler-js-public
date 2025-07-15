import { z } from 'zod';

export const fieldSchema = z.object({
  name: z.string(),
  type: z.string(),
  required: z.boolean(),
  validation: z.any().optional(),
});

export const categorySchema = z.object({
  name: z.string(),
  description: z.string(),
  fields: z.array(z.string()),
});
