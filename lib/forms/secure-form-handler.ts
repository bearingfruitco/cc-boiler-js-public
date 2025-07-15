import { trackingFields, cookiesFields, deviceFields, geographicFields, journeyFields } from '@/field-registry/core';
import { PIIDetector } from '@/lib/security/pii-detector';
import { FieldEncryptor } from '@/lib/security/field-encryptor';
import { AuditLogger } from '@/lib/security/audit-logger';
import { cookies } from 'next/headers';
import { eventQueue, LEAD_EVENTS } from '@/lib/events';

interface FormSubmission {
  formData: Record<string, any>;
  metadata: {
    formId: string;
    sessionId: string;
    ipAddress: string;
    userAgent: string;
  };
}

interface ValidationResult {
  isValid: boolean;
  errors: Record<string, string>;
  warnings: string[];
}

interface ProcessedFormData {
  data: Record<string, any>;
  encrypted: Record<string, string>;
  attribution: Record<string, any>;
  device: Record<string, any>;
  journey: Record<string, any>;
}

export class SecureFormHandler {
  private static instance: SecureFormHandler;
  private piiDetector: PIIDetector;
  private fieldEncryptor: FieldEncryptor;
  private auditLogger: AuditLogger;

  constructor() {
    this.piiDetector = new PIIDetector();
    this.fieldEncryptor = new FieldEncryptor();
    this.auditLogger = new AuditLogger();
  }

  static getInstance(): SecureFormHandler {
    if (!SecureFormHandler.instance) {
      SecureFormHandler.instance = new SecureFormHandler();
    }
    return SecureFormHandler.instance;
  }

  /**
   * Validate form data before processing
   */
  async validateFormData(
    formData: Record<string, any>,
    formId: string
  ): Promise<ValidationResult> {
    const errors: Record<string, string> = {};
    const warnings: string[] = [];

    // Check for PII in non-secure fields
    for (const [field, value] of Object.entries(formData)) {
      if (this.piiDetector.containsPII(String(value))) {
        const fieldConfig = this.getFieldConfig(field);
        if (!fieldConfig?.pii) {
          warnings.push(`Field "${field}" contains PII but is not marked as PII field`);
        }
      }
    }

    // Validate required fields based on form type
    const requiredFields = this.getRequiredFields(formId);
    for (const field of requiredFields) {
      if (!formData[field]) {
        errors[field] = `${field} is required`;
      }
    }

    return {
      isValid: Object.keys(errors).length === 0,
      errors,
      warnings,
    };
  }

  /**
   * Process tracking fields from URL and cookies
   */
  async processTrackingData(request: Request): Promise<Record<string, any>> {
    const url = new URL(request.url);
    const trackingData: Record<string, any> = {};

    // Extract URL parameters
    for (const field of Object.keys(trackingFields)) {
      const value = url.searchParams.get(field);
      if (value && this.canPrepopulateField(field)) {
        trackingData[field] = this.sanitizeValue(value);
      }
    }

    // Extract cookie data
    const cookieStore = cookies();
    for (const field of Object.keys(cookiesFields)) {
      const value = cookieStore.get(field)?.value;
      if (value) {
        trackingData[field] = this.sanitizeValue(value);
      }
    }

    return trackingData;
  }

  /**
   * Process form submission securely
   */
  async processFormSubmission(
    submission: FormSubmission
  ): Promise<ProcessedFormData> {
    const { formData, metadata } = submission;

    // Audit the submission attempt
    await this.auditLogger.logFormSubmission({
      formId: metadata.formId,
      sessionId: metadata.sessionId,
      ipAddress: metadata.ipAddress,
      fields: Object.keys(formData),
    });

    // Separate PII and non-PII data
    const piiData: Record<string, any> = {};
    const nonPiiData: Record<string, any> = {};
    const encryptedData: Record<string, string> = {};

    for (const [field, value] of Object.entries(formData)) {
      const fieldConfig = this.getFieldConfig(field);
      
      if (fieldConfig?.pii) {
        // Encrypt PII fields
        const encrypted = await this.fieldEncryptor.encryptField(field, value);
        encryptedData[field] = encrypted;
        piiData[field] = value; // Keep original for server-side processing
      } else {
        nonPiiData[field] = value;
      }
    }

    // Extract attribution data
    const attribution = this.extractAttribution(formData);
    
    // Extract device data
    const device = await this.extractDeviceData(metadata.userAgent);
    
    // Extract journey data
    const journey = this.extractJourneyData(metadata.sessionId);

    // Emit form submission event
    eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, {
      formId: metadata.formId,
      sessionId: metadata.sessionId,
      fieldCount: Object.keys(formData).length,
      hasPII: Object.keys(piiData).length > 0,
    });

    return {
      data: { ...nonPiiData, ...piiData },
      encrypted: encryptedData,
      attribution,
      device,
      journey,
    };
  }

  /**
   * Check if a field can be prepopulated from URL
   */
  private canPrepopulateField(field: string): boolean {
    const fieldConfig = this.getFieldConfig(field);
    return fieldConfig?.prepopulate === true && !fieldConfig?.pii;
  }

  /**
   * Sanitize input values
   */
  private sanitizeValue(value: string): string {
    return value
      .trim()
      .replace(/<script[^>]*>.*?<\/script>/gi, '')
      .replace(/<[^>]+>/g, '')
      .slice(0, 1000); // Limit length
  }

  /**
   * Get field configuration
   */
  private getFieldConfig(field: string): any {
    const allFields = {
      ...trackingFields,
      ...cookiesFields,
      ...deviceFields,
      ...geographicFields,
      ...journeyFields,
    };
    return allFields[field];
  }

  /**
   * Get required fields for a form
   */
  private getRequiredFields(formId: string): string[] {
    // Define required fields per form type
    const requiredFieldsMap: Record<string, string[]> = {
      'lead-form': ['name', 'email', 'phone'],
      'contact-form': ['name', 'email', 'message'],
      'quiz-form': ['email'],
    };

    return requiredFieldsMap[formId] || [];
  }

  /**
   * Extract attribution data
   */
  private extractAttribution(formData: Record<string, any>): Record<string, any> {
    const attribution: Record<string, any> = {};
    const attributionFields = [
      'utm_source',
      'utm_medium',
      'utm_campaign',
      'utm_term',
      'utm_content',
      'gclid',
      'fbclid',
      'ttclid',
    ];

    for (const field of attributionFields) {
      if (formData[field]) {
        attribution[field] = formData[field];
      }
    }

    return attribution;
  }

  /**
   * Extract device data from user agent
   */
  private async extractDeviceData(userAgent: string): Promise<Record<string, any>> {
    // Simple device detection (you might want to use a library like ua-parser-js)
    const isMobile = /mobile|android|iphone/i.test(userAgent);
    const isTablet = /tablet|ipad/i.test(userAgent);
    
    return {
      device_type: isTablet ? 'tablet' : isMobile ? 'mobile' : 'desktop',
      user_agent: userAgent,
      screen_resolution: 'unknown', // Would be set client-side
      browser: this.detectBrowser(userAgent),
    };
  }

  /**
   * Detect browser from user agent
   */
  private detectBrowser(userAgent: string): string {
    if (userAgent.includes('Chrome')) return 'Chrome';
    if (userAgent.includes('Firefox')) return 'Firefox';
    if (userAgent.includes('Safari')) return 'Safari';
    if (userAgent.includes('Edge')) return 'Edge';
    return 'Other';
  }

  /**
   * Extract journey data
   */
  private extractJourneyData(sessionId: string): Record<string, any> {
    return {
      session_id: sessionId,
      form_started_at: new Date().toISOString(),
      form_submitted_at: new Date().toISOString(),
    };
  }

  /**
   * Parse secure parameters from URL
   */
  static parseSecureParams(url: URL): Record<string, string> {
    const params: Record<string, string> = {};
    const allowedParams = [
      'utm_source',
      'utm_medium',
      'utm_campaign',
      'utm_term',
      'utm_content',
      'gclid',
      'fbclid',
      'ttclid',
      'partner_id',
      'campaign_id',
    ];

    for (const param of allowedParams) {
      const value = url.searchParams.get(param);
      if (value) {
        params[param] = value;
      }
    }

    return params;
  }
}

// Export singleton instance
export const secureFormHandler = SecureFormHandler.getInstance();

// Add missing static method
export class SecureFormHandlerExtensions {
  static async processFormSubmission(data: any): Promise<any> {
    // Implementation
    return SecureFormHandler.processFormData(data);
  }
}

// Extend SecureFormHandler
Object.assign(SecureFormHandler, SecureFormHandlerExtensions);

// Add processFormData method if missing
SecureFormHandler.processFormData = SecureFormHandler.processFormData || function(data: any) {
  return SecureFormHandler.sanitizeData(data);
};

// Add processFormSubmission
SecureFormHandler.processFormSubmission = async function(data: any) {
  return SecureFormHandler.processFormData(data);
};

// Add static methods
declare module './secure-form-handler' {
  interface SecureFormHandlerConstructor {
    processFormData(data: any): any;
    sanitizeData(data: any): any;
    processFormSubmission(data: any): Promise<any>;
  }
}

interface SecureFormHandlerConstructor {
  new(): SecureFormHandler;
  processFormData(data: any): any;
  sanitizeData(data: any): any;
  processFormSubmission(data: any): Promise<any>;
  parseSecureParams(url: URL): any;
}

const SecureFormHandlerClass = SecureFormHandler as any as SecureFormHandlerConstructor;

// Add methods
SecureFormHandlerClass.processFormData = function(data: any) {
  // Remove PII from logs
  return PIIDetectorClass.createSafeObject(data);
};

SecureFormHandlerClass.sanitizeData = function(data: any) {
  return SecureFormHandlerClass.processFormData(data);
};

SecureFormHandlerClass.processFormSubmission = async function(data: any) {
  return SecureFormHandlerClass.processFormData(data);
};
