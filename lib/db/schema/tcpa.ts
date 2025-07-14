/**
 * TCPA Compliance Database Schema
 * Tables for storing certificates, consents, and verifications
 */

import { pgTable, text, timestamp, boolean, jsonb, integer } from 'drizzle-orm/pg-core';
import { createInsertSchema, createSelectSchema } from 'drizzle-zod';
import { z } from 'zod';

// TCPA Certificates table
export const tcpaCertificates = pgTable('tcpa_certificates', {
  id: text('id').primaryKey().$defaultFn(() => crypto.randomUUID()),
  leadId: text('lead_id').notNull(),
  certUrl: text('cert_url').notNull(),
  certType: text('cert_type').notNull().$type<'trustedform' | 'jornaya'>(),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  expiresAt: timestamp('expires_at').notNull(),
  verified: boolean('verified').default(false),
  verificationData: jsonb('verification_data'),
  
  // Audit fields
  ipAddress: text('ip_address'),
  userAgent: text('user_agent'),
  pageUrl: text('page_url'),
});

// TCPA Consents table
export const tcpaConsents = pgTable('tcpa_consents', {
  id: text('id').primaryKey().$defaultFn(() => crypto.randomUUID()),
  leadId: text('lead_id').notNull(),
  consentText: text('consent_text').notNull(),
  consentedAt: timestamp('consented_at').notNull(),
  ipAddress: text('ip_address').notNull(),
  userAgent: text('user_agent'),
  pageUrl: text('page_url').notNull(),
  
  // Link to certificate if available
  certificateId: text('certificate_id').references(() => tcpaCertificates.id),
  
  // Additional tracking
  sessionId: text('session_id'),
  formId: text('form_id'),
});

// TCPA Verifications table
export const tcpaVerifications = pgTable('tcpa_verifications', {
  id: text('id').primaryKey().$defaultFn(() => crypto.randomUUID()),
  certificateId: text('certificate_id').notNull(),
  verifiedAt: timestamp('verified_at').notNull().defaultNow(),
  valid: boolean('valid').notNull(),
  provider: text('provider').notNull().$type<'trustedform' | 'jornaya'>(),
  responseData: jsonb('response_data').notNull(),
  errorMessage: text('error_message'),
  
  // API tracking
  apiVersion: text('api_version'),
  responseTime: integer('response_time'), // milliseconds
});

// Zod schemas for validation
export const insertTCPACertificateSchema = createInsertSchema(tcpaCertificates, {
  certType: z.enum(['trustedform', 'jornaya']),
  certUrl: z.string().url(),
  leadId: z.string().min(1),
});

export const insertTCPAConsentSchema = createInsertSchema(tcpaConsents, {
  consentText: z.string().min(10),
  ipAddress: z.string().ip(),
  pageUrl: z.string().url(),
});

export const insertTCPAVerificationSchema = createInsertSchema(tcpaVerifications, {
  provider: z.enum(['trustedform', 'jornaya']),
  valid: z.boolean(),
});

// Select schemas
export const selectTCPACertificateSchema = createSelectSchema(tcpaCertificates);
export const selectTCPAConsentSchema = createSelectSchema(tcpaConsents);
export const selectTCPAVerificationSchema = createSelectSchema(tcpaVerifications);

// Types
export type TCPACertificate = z.infer<typeof selectTCPACertificateSchema>;
export type TCPAConsent = z.infer<typeof selectTCPAConsentSchema>;
export type TCPAVerification = z.infer<typeof selectTCPAVerificationSchema>;
export type InsertTCPACertificate = z.infer<typeof insertTCPACertificateSchema>;
export type InsertTCPAConsent = z.infer<typeof insertTCPAConsentSchema>;
export type InsertTCPAVerification = z.infer<typeof insertTCPAVerificationSchema>;
