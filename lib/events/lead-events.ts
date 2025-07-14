/**
 * Lead generation specific events and handlers
 */

import { z } from 'zod';
import { eventQueue } from './event-queue';
import { BaseEventSchema } from './event-types';

// Lead event data schema
export const LeadEventSchema = BaseEventSchema.extend({
  formId: z.string(),
  leadId: z.string().optional(),
  sessionId: z.string(),
  data: z.record(z.any()),
  tracking: z.object({
    source: z.string().optional(),
    medium: z.string().optional(),
    campaign: z.string().optional(),
    term: z.string().optional(),
    content: z.string().optional(),
    gclid: z.string().optional(),
    fbclid: z.string().optional(),
  }).optional(),
});

export type LeadEvent = z.infer<typeof LeadEventSchema>;

// Lead event types
export const LEAD_EVENTS = {
  // User interaction events
  FORM_VIEW: 'lead.form.view',
  FORM_START: 'lead.form.start',
  FIELD_FOCUS: 'lead.field.focus',
  FIELD_BLUR: 'lead.field.blur',
  FIELD_CHANGE: 'lead.field.change',
  FORM_ABANDON: 'lead.form.abandon',
  
  // Submission events
  FORM_SUBMIT: 'lead.form.submit',
  FORM_VALIDATE: 'lead.form.validate',
  SUBMISSION_START: 'lead.submission.start',
  SUBMISSION_SUCCESS: 'lead.submission.success',
  SUBMISSION_ERROR: 'lead.submission.error',
  
  // Tracking events
  PIXEL_FIRE: 'lead.pixel.fire',
  WEBHOOK_SEND: 'lead.webhook.send',
  ANALYTICS_TRACK: 'lead.analytics.track',
  CRM_SYNC: 'lead.crm.sync',
  EMAIL_SEND: 'lead.email.send',
  
  // Consent events
  CONSENT_SHOWN: 'lead.consent.shown',
  CONSENT_ACCEPTED: 'lead.consent.accepted',
  CONSENT_DECLINED: 'lead.consent.declined',
  TCPA_ACCEPTED: 'lead.tcpa.accepted',
  
  // Error events
  VALIDATION_ERROR: 'lead.validation.error',
  NETWORK_ERROR: 'lead.network.error',
  INTEGRATION_ERROR: 'lead.integration.error',
} as const;

export type LeadEventType = typeof LEAD_EVENTS[keyof typeof LEAD_EVENTS];

// Field change event
export interface FieldChangeEvent extends LeadEvent {
  fieldName: string;
  oldValue: any;
  newValue: any;
  isValid: boolean;
}

// Submission event
export interface SubmissionEvent extends LeadEvent {
  success: boolean;
  errors?: Record<string, string>;
  duration: number;
}

// Tracking event
export interface TrackingEvent extends LeadEvent {
  platform: 'google' | 'facebook' | 'tiktok' | 'custom';
  eventName: string;
  success: boolean;
}

/**
 * Create a lead event with proper structure
 */
export function createLeadEvent(
  type: LeadEventType,
  formId: string,
  data: Partial<LeadEvent>
): LeadEvent {
  return {
    timestamp: new Date().toISOString(),
    source: 'lead-form',
    version: '1.0',
    formId,
    sessionId: data.sessionId || generateSessionId(),
    data: data.data || {},
    ...data,
  };
}

/**
 * Generate a session ID if not provided
 */
function generateSessionId(): string {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Fire multiple tracking pixels in parallel
 */
export async function fireTrackingPixels(event: LeadEvent): Promise<void> {
  const pixelPromises = [];

  // Google Analytics
  if (typeof window !== 'undefined' && (window as any).gtag) {
    pixelPromises.push(
      fireGooglePixel(event).catch(err => 
        console.error('Google pixel error:', err)
      )
    );
  }

  // Facebook Pixel
  if (typeof window !== 'undefined' && (window as any).fbq) {
    pixelPromises.push(
      fireFacebookPixel(event).catch(err => 
        console.error('Facebook pixel error:', err)
      )
    );
  }

  // TikTok Pixel
  if (typeof window !== 'undefined' && (window as any).ttq) {
    pixelPromises.push(
      fireTikTokPixel(event).catch(err => 
        console.error('TikTok pixel error:', err)
      )
    );
  }

  await Promise.allSettled(pixelPromises);
}

/**
 * Fire Google Analytics event
 */
async function fireGooglePixel(event: LeadEvent): Promise<void> {
  const startTime = Date.now();
  
  try {
    (window as any).gtag('event', 'generate_lead', {
      event_category: 'engagement',
      event_label: event.formId,
      value: 1,
      ...event.tracking,
    });

    eventQueue.emit(LEAD_EVENTS.PIXEL_FIRE, {
      ...event,
      platform: 'google',
      eventName: 'generate_lead',
      success: true,
      duration: Date.now() - startTime,
    } as TrackingEvent);
  } catch (error) {
    eventQueue.emit(LEAD_EVENTS.PIXEL_FIRE, {
      ...event,
      platform: 'google',
      eventName: 'generate_lead',
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    } as TrackingEvent);
    throw error;
  }
}

/**
 * Fire Facebook Pixel event
 */
async function fireFacebookPixel(event: LeadEvent): Promise<void> {
  const startTime = Date.now();
  
  try {
    (window as any).fbq('track', 'Lead', {
      content_name: event.formId,
      content_category: 'Lead Form',
      ...event.tracking,
    });

    eventQueue.emit(LEAD_EVENTS.PIXEL_FIRE, {
      ...event,
      platform: 'facebook',
      eventName: 'Lead',
      success: true,
      duration: Date.now() - startTime,
    } as TrackingEvent);
  } catch (error) {
    eventQueue.emit(LEAD_EVENTS.PIXEL_FIRE, {
      ...event,
      platform: 'facebook',
      eventName: 'Lead',
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    } as TrackingEvent);
    throw error;
  }
}

/**
 * Fire TikTok Pixel event
 */
async function fireTikTokPixel(event: LeadEvent): Promise<void> {
  const startTime = Date.now();
  
  try {
    (window as any).ttq.track('SubmitForm', {
      content_name: event.formId,
      content_type: 'lead_form',
      ...event.tracking,
    });

    eventQueue.emit(LEAD_EVENTS.PIXEL_FIRE, {
      ...event,
      platform: 'tiktok',
      eventName: 'SubmitForm',
      success: true,
      duration: Date.now() - startTime,
    } as TrackingEvent);
  } catch (error) {
    eventQueue.emit(LEAD_EVENTS.PIXEL_FIRE, {
      ...event,
      platform: 'tiktok',
      eventName: 'SubmitForm',
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    } as TrackingEvent);
    throw error;
  }
}

/**
 * Send webhook notification
 */
export async function sendWebhook(
  url: string,
  event: LeadEvent,
  options: { timeout?: number; retries?: number } = {}
): Promise<void> {
  const { timeout = 5000, retries = 3 } = options;
  let lastError: Error | null = null;

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeout);

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Event-Type': event.source,
          'X-Event-ID': event.id || 'unknown',
        },
        body: JSON.stringify(event),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`Webhook failed: ${response.statusText}`);
      }

      eventQueue.emit(LEAD_EVENTS.WEBHOOK_SEND, {
        ...event,
        webhookUrl: url,
        success: true,
        attempt,
      });

      return;
    } catch (error) {
      lastError = error instanceof Error ? error : new Error('Unknown error');
      
      if (attempt === retries) {
        eventQueue.emit(LEAD_EVENTS.WEBHOOK_SEND, {
          ...event,
          webhookUrl: url,
          success: false,
          error: lastError.message,
          attempts: retries,
        });
        throw lastError;
      }

      // Exponential backoff
      await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
    }
  }
}

// Register default handlers for critical events
eventQueue.on(LEAD_EVENTS.FORM_SUBMIT, async (event: LeadEvent) => {
  // Log submission for monitoring
  console.log('[Lead Event] Form submitted:', event.formId);
});

eventQueue.on(LEAD_EVENTS.SUBMISSION_SUCCESS, async (event: LeadEvent) => {
  // Send webhooks if configured
  const webhookUrl = process.env.NEXT_PUBLIC_LEAD_WEBHOOK_URL;
  if (webhookUrl) {
    sendWebhook(webhookUrl, event).catch(err =>
      console.error('Webhook error:', err)
    );
  }
});
