/**
 * Bridge between event queue and analytics providers
 * Ensures all events flow through existing analytics infrastructure
 */

import { eventQueue } from '@/lib/events/event-queue';
import { LEAD_EVENTS } from '@/lib/events/lead-events';
import { ANALYTICS_EVENTS } from '@/lib/events/analytics-events';
import { trackEvent, identifyUser, pageView } from '@/lib/analytics/rudderstack';

/**
 * Initialize analytics bridge
 * This connects the event queue to Rudderstack and other providers
 */
export function initAnalyticsBridge() {
  // Bridge all lead events to Rudderstack
  eventQueue.on('lead.*', async (event: any) => {
    // Map internal events to Rudderstack event names
    const eventMapping: Record<string, string> = {
      [LEAD_EVENTS.FORM_VIEW]: 'Form Viewed',
      [LEAD_EVENTS.FORM_START]: 'Form Started',
      [LEAD_EVENTS.FIELD_CHANGE]: 'Form Field Changed',
      [LEAD_EVENTS.FORM_SUBMIT]: 'Form Submitted',
      [LEAD_EVENTS.SUBMISSION_SUCCESS]: 'Lead Captured',
      [LEAD_EVENTS.SUBMISSION_ERROR]: 'Form Submit Error',
      [LEAD_EVENTS.CONSENT_ACCEPTED]: 'Consent Given',
    };

    const rudderEventName = eventMapping[event.type] || event.type;
    
    // Send to Rudderstack with proper formatting
    trackEvent(rudderEventName, {
      formId: event.formId,
      sessionId: event.sessionId,
      ...event.data,
      // Include tracking parameters
      ...(event.tracking || {}),
      // Metadata
      timestamp: event.timestamp,
      source: event.source,
    });
  });

  // Bridge analytics events
  eventQueue.on('analytics.*', async (event: any) => {
    const eventType = event.type.replace('analytics.', '');
    
    switch (eventType) {
      case 'page.view':
        pageView(event.title, {
          url: event.url,
          path: event.path,
          referrer: event.referrer,
          ...event.query,
        });
        break;
        
      case 'user.action':
        trackEvent(`${event.category} - ${event.action}`, {
          label: event.label,
          value: event.value,
        });
        break;
        
      case 'conversion':
        trackEvent('Conversion', {
          type: event.metadata?.type,
          value: event.metadata?.value,
          ...event.metadata,
        });
        break;
        
      default:
        // Pass through other events
        trackEvent(eventType, event);
    }
  });

  // Bridge pixel fire events for debugging
  eventQueue.on(LEAD_EVENTS.PIXEL_FIRE, async (event: any) => {
    // Log pixel fires to Rudderstack for monitoring
    trackEvent('Tracking Pixel Fired', {
      platform: event.platform,
      eventName: event.eventName,
      success: event.success,
      duration: event.duration,
      error: event.error,
    });
  });

  // Bridge webhook events for monitoring
  eventQueue.on(LEAD_EVENTS.WEBHOOK_SEND, async (event: any) => {
    trackEvent('Webhook Sent', {
      url: event.webhookUrl,
      success: event.success,
      attempts: event.attempts,
      error: event.error,
    });
  });

  // Handle user identification
  eventQueue.on('user.identify', async (event: any) => {
    identifyUser(event.userId, event.traits);
  });
}

/**
 * Track form conversion with proper attribution
 */
export function trackFormConversion(
  formId: string,
  leadId: string,
  data: Record<string, any>
) {
  // Extract attribution data
  const attribution = {
    utm_source: data.utm_source,
    utm_medium: data.utm_medium,
    utm_campaign: data.utm_campaign,
    utm_term: data.utm_term,
    utm_content: data.utm_content,
    gclid: data.gclid,
    fbclid: data.fbclid,
    ttclid: data.ttclid,
  };

  // Track the conversion
  trackEvent('Lead Form Conversion', {
    formId,
    leadId,
    ...attribution,
    // Include form-specific data (non-PII)
    vertical: data.vertical,
    form_type: data.form_type,
  });
}

/**
 * Enhanced page tracking with form context
 */
export function trackFormPage(formId: string, step?: string) {
  pageView(`Form - ${formId}${step ? ` - ${step}` : ''}`, {
    formId,
    step,
  });
}

/**
 * Track form abandonment
 */
export function trackFormAbandonment(
  formId: string,
  lastField: string,
  timeSpent: number
) {
  trackEvent('Form Abandoned', {
    formId,
    lastField,
    timeSpent,
    abandonmentPoint: lastField,
  });
}
