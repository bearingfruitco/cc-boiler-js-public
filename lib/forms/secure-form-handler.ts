import { trackingFields } from '@/field-registry/core/tracking.json';
import { cookieFields } from '@/field-registry/core/cookies.json';
import { deviceFields } from '@/field-registry/core/device.json';
import { geographicFields } from '@/field-registry/core/geographic.json';
import { journeyFields } from '@/field-registry/core/journey.json';
import { PIIDetector } from '@/lib/security/pii-detector';
import { FieldEncryptor } from '@/lib/security/field-encryptor';
import { AuditLogger } from '@/lib/security/audit-logger';
import { cookies } from 'next/headers';

interface FormSubmission {
  formData: Record<string, any>;
  metadata: {
    formId: string;
    sessionId: string;
    ipAddress: string;
    userAgent: string;
  };
}

export class SecureFormHandler {
  // Whitelist of fields that can be prepopulated from URL
  private static readonly PREPOP_WHITELIST = [
    'utm_source',
    'utm_medium',
    'utm_campaign',
    'utm_term',
    'utm_content',
    'gclid',
    'fbclid',
    'ttclid',
    'wbraid',
    'gbraid',
    'partner_id',
    'campaign_id',
    'source_id',
    'ad_id',
    'placement_id',
  ];
  
  /**
   * Parse and validate prepopulation parameters
   */
  static parseSecureParams(url: URL): Record<string, string> {
    const params: Record<string, string> = {};
    
    for (const [key, value] of url.searchParams) {
      // Only allow whitelisted fields
      if (!this.PREPOP_WHITELIST.includes(key)) {
        continue;
      }
      
      // Validate value doesn't contain PII
      const piiCheck = PIIDetector.detectPII(value);
      if (piiCheck.hasPII) {
        console.warn(`[SECURITY] Blocked PII in URL param: ${key}`);
        await AuditLogger.logSecurityEvent({
          event: 'blocked_pii_in_url',
          sessionId: 'unknown',
          ipAddress: 'unknown',
          userAgent: 'unknown',
          details: { key, piiTypes: piiCheck.types },
        });
        continue;
      }
      
      // Sanitize value
      params[key] = this.sanitizeValue(value);
    }
    
    return params;
  }
  
  /**
   * Capture all tracking data automatically
   */
  private static async captureTrackingData(url: URL): Promise<Record<string, any>> {
    const tracking: Record<string, any> = {};
    
    // Get URL parameters
    for (const field of Object.keys(trackingFields.fields)) {
      const value = url.searchParams.get(field);
      if (value) {
        tracking[field] = this.sanitizeValue(value);
      }
    }
    
    return tracking;
  }
  
  /**
   * Capture device information
   */
  private static captureDeviceData(userAgent: string): Record<string, any> {
    // In production, use a proper user agent parser
    return {
      user_agent: userAgent,
      browser_name: 'Chrome', // Parse from UA
      browser_version: '120.0', // Parse from UA
      os_name: 'Windows', // Parse from UA
      os_version: '11', // Parse from UA
      device_type: 'desktop', // Detect from UA
      screen_width: 1920, // Get from client
      screen_height: 1080, // Get from client
      viewport_width: 1920, // Get from client
      viewport_height: 980, // Get from client
    };
  }
  
  /**
   * Capture cookie data (server-side only)
   */
  private static async captureCookies(): Promise<Record<string, any>> {
    const cookieStore = cookies();
    const cookieData: Record<string, any> = {};
    
    // Capture marketing cookies
    const cookiesToCapture = ['_ga', '_fbp', '_fbc', '_gcl_aw', '_ttp'];
    
    for (const cookieName of cookiesToCapture) {
      const cookie = cookieStore.get(cookieName);
      if (cookie) {
        cookieData[`cookie_${cookieName.replace('_', '')}`] = cookie.value;
      }
    }
    
    // Extract client ID from GA cookie
    if (cookieData.cookie_ga) {
      const parts = cookieData.cookie_ga.split('.');
      if (parts.length >= 4) {
        cookieData.client_id = `${parts[2]}.${parts[3]}`;
      }
    }
    
    return cookieData;
  }
  
  /**
   * Process form submission with full security
   */
  static async processFormSubmission(
    submission: FormSubmission,
    encryptionKey: string
  ): Promise<{
    success: boolean;
    data?: Record<string, any>;
    errors?: string[];
  }> {
    const errors: string[] = [];
    
    try {
      // 1. Validate no PII in places it shouldn't be
      const formDataScan = PIIDetector.scanObject(submission.formData);
      for (const issue of formDataScan) {
        if (issue.path.includes('utm_') || issue.path.includes('gclid')) {
          errors.push(`PII detected in tracking field: ${issue.path}`);
        }
      }
      
      if (errors.length > 0) {
        return { success: false, errors };
      }
      
      // 2. Capture all tracking data
      const url = new URL(submission.metadata.formId); // In production, get actual URL
      const tracking = await this.captureTrackingData(url);
      const device = this.captureDeviceData(submission.metadata.userAgent);
      const cookieData = await this.captureCookies();
      
      // 3. Generate IDs
      const journeyId = this.generateJourneyId();
      const sessionId = submission.metadata.sessionId || this.generateSessionId();
      
      // 4. Merge all data
      const completeSubmission = {
        // Form data
        ...submission.formData,
        
        // Tracking data
        ...tracking,
        
        // Journey data
        journey_id: journeyId,
        session_id: sessionId,
        form_submit_time: new Date().toISOString(),
        
        // Metadata
        eventtime_created_at: new Date().toISOString(),
        ip_address: submission.metadata.ipAddress,
        
        // Related tables data
        dim_device: device,
        dim_cookie: cookieData,
      };
      
      // 5. Encrypt PII fields
      const encryptedData = await FieldEncryptor.encryptFields(
        completeSubmission,
        encryptionKey
      );
      
      // 6. Log the submission
      await AuditLogger.logFormSubmission({
        formId: submission.metadata.formId,
        sessionId: sessionId,
        ipAddress: submission.metadata.ipAddress,
        userAgent: submission.metadata.userAgent,
        fields: Object.keys(submission.formData),
        hasConsent: !!submission.formData.consent_tcpa,
        leadId: encryptedData.id,
      });
      
      return {
        success: true,
        data: encryptedData,
      };
      
    } catch (error) {
      console.error('[SecureFormHandler] Error:', error);
      errors.push('Internal processing error');
      return { success: false, errors };
    }
  }
  
  /**
   * Sanitize input value
   */
  private static sanitizeValue(value: string): string {
    return value
      .trim()
      .replace(/[<>]/g, '') // Remove potential HTML
      .substring(0, 500); // Limit length
  }
  
  /**
   * Generate unique journey ID
   */
  private static generateJourneyId(): string {
    return `journey_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
  
  /**
   * Generate session ID
   */
  private static generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
  
  /**
   * Validate form data against field registry
   */
  static async validateFormData(
    formData: Record<string, any>,
    vertical?: string
  ): Promise<{
    valid: boolean;
    errors: Record<string, string>;
  }> {
    const errors: Record<string, string> = {};
    
    // Load field definitions based on vertical
    const fieldDefs = await this.loadFieldDefinitions(vertical);
    
    for (const [fieldName, fieldDef] of Object.entries(fieldDefs)) {
      const value = formData[fieldName];
      
      // Check required fields
      if (fieldDef.mode === 'REQUIRED' && !value) {
        errors[fieldName] = `${fieldName} is required`;
        continue;
      }
      
      // Validate based on type
      if (value && fieldDef.validation) {
        const validation = fieldDef.validation;
        
        // Pattern validation
        if (validation.pattern) {
          const pattern = new RegExp(validation.pattern);
          if (!pattern.test(String(value))) {
            errors[fieldName] = validation.message || `Invalid format for ${fieldName}`;
          }
        }
        
        // Length validation
        if (validation.minLength && String(value).length < validation.minLength) {
          errors[fieldName] = `${fieldName} must be at least ${validation.minLength} characters`;
        }
        
        if (validation.maxLength && String(value).length > validation.maxLength) {
          errors[fieldName] = `${fieldName} must be no more than ${validation.maxLength} characters`;
        }
        
        // Numeric validation
        if (fieldDef.type === 'INTEGER' || fieldDef.type === 'FLOAT') {
          const numValue = Number(value);
          if (isNaN(numValue)) {
            errors[fieldName] = `${fieldName} must be a number`;
          } else {
            if (validation.min !== undefined && numValue < validation.min) {
              errors[fieldName] = `${fieldName} must be at least ${validation.min}`;
            }
            if (validation.max !== undefined && numValue > validation.max) {
              errors[fieldName] = `${fieldName} must be no more than ${validation.max}`;
            }
          }
        }
        
        // Enum validation
        if (validation.enum && !validation.enum.includes(value)) {
          errors[fieldName] = `${fieldName} must be one of: ${validation.enum.join(', ')}`;
        }
      }
    }
    
    return {
      valid: Object.keys(errors).length === 0,
      errors,
    };
  }
  
  /**
   * Load field definitions for a vertical
   */
  private static async loadFieldDefinitions(vertical?: string): Promise<Record<string, any>> {
    // Load core fields
    const core = {
      ...trackingFields.fields,
      ...journeyFields.fields,
    };
    
    // Load vertical-specific fields if specified
    if (vertical) {
      try {
        const verticalFields = await import(`@/field-registry/verticals/${vertical}.json`);
        return { ...core, ...verticalFields.fields };
      } catch (error) {
        console.warn(`No field definitions found for vertical: ${vertical}`);
      }
    }
    
    return core;
  }
}
