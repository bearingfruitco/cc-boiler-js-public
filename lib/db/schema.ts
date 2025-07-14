import { pgTable, text, timestamp, uuid, boolean, integer, jsonb } from 'drizzle-orm/pg-core';
import { sql } from 'drizzle-orm';
import { createInsertSchema, createSelectSchema } from 'drizzle-zod';
import { z } from 'zod';

// Users table
export const users = pgTable('users', {
  id: uuid('id').default(sql`gen_random_uuid()`).primaryKey(),
  email: text('email').unique().notNull(),
  name: text('name'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
});

// Form submissions table (for tracked forms)
export const formSubmissions = pgTable('form_submissions', {
  id: uuid('id').default(sql`gen_random_uuid()`).primaryKey(),
  formName: text('form_name').notNull(),
  data: jsonb('data').notNull(),
  userId: uuid('user_id').references(() => users.id),
  ip: text('ip'),
  userAgent: text('user_agent'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

// Audit logs table (for PII access tracking)
export const auditLogs = pgTable('audit_logs', {
  id: uuid('id').default(sql`gen_random_uuid()`).primaryKey(),
  userId: uuid('user_id').references(() => users.id),
  action: text('action').notNull(),
  resource: text('resource').notNull(),
  metadata: jsonb('metadata'),
  ip: text('ip'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

// Type inference helpers
export type User = typeof users.$inferSelect;
export type NewUser = typeof users.$inferInsert;
export type FormSubmission = typeof formSubmissions.$inferSelect;
export type NewFormSubmission = typeof formSubmissions.$inferInsert;
export type AuditLog = typeof auditLogs.$inferSelect;
export type NewAuditLog = typeof auditLogs.$inferInsert;

// Zod schemas for validation
export const insertUserSchema = createInsertSchema(users);
export const selectUserSchema = createSelectSchema(users);
export const insertFormSubmissionSchema = createInsertSchema(formSubmissions);
export const selectFormSubmissionSchema = createSelectSchema(formSubmissions);
export const insertAuditLogSchema = createInsertSchema(auditLogs);
export const selectAuditLogSchema = createSelectSchema(auditLogs);
