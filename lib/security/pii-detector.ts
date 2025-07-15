import piiFieldsData from '@/field-registry/compliance/pii-fields.json';
import phiFieldsData from '@/field-registry/compliance/phi-fields.json';

interface FieldsData {
  description: string;
  fields: string[];
}

const piiFields = (piiFieldsData as FieldsData).fields;
const phiFields = (phiFieldsData as FieldsData).fields;

interface DetectionResult {
  containsPII: boolean;
  containsPHI: boolean;
  detectedFields: string[];
  patterns: string[];
}

export class PIIDetector {
  private patterns = {
    ssn: /\b\d{3}-\d{2}-\d{4}\b|\b\d{9}\b/,
    creditCard: /\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/,
    email: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/,
    phone: /\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b/,
    dateOfBirth: /\b(0[1-9]|1[0-2])[\/\-](0[1-9]|[12]\d|3[01])[\/\-](19|20)\d{2}\b/,
    ipAddress: /\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b/,
  };

  /**
   * Check if a value contains PII
   */
  containsPII(value: string): boolean {
    if (!value) return false;
    
    const stringValue = String(value).toLowerCase();
    
    // Check against patterns
    for (const pattern of Object.values(this.patterns)) {
      if (pattern.test(stringValue)) {
        return true;
      }
    }
    
    return false;
  }

  /**
   * Detect PII in an object
   */
  detectPII(data: Record<string, any>): DetectionResult {
    const detectedFields: string[] = [];
    const patterns: string[] = [];
    let containsPII = false;
    let containsPHI = false;

    for (const [fieldName, value] of Object.entries(data)) {
      // Check if field is known PII
      if (piiFields.includes(fieldName)) {
        containsPII = true;
        detectedFields.push(fieldName);
      }
      
      // Check if field is PHI
      if (phiFields.includes(fieldName)) {
        containsPHI = true;
        detectedFields.push(fieldName);
      }
      
      // Check value against patterns
      if (value && this.containsPII(String(value))) {
        containsPII = true;
        if (!detectedFields.includes(fieldName)) {
          detectedFields.push(fieldName);
        }
        
        // Identify which pattern matched
        for (const [patternName, pattern] of Object.entries(this.patterns)) {
          if (pattern.test(String(value))) {
            patterns.push(patternName);
          }
        }
      }
    }

    return {
      containsPII,
      containsPHI,
      detectedFields,
      patterns: [...new Set(patterns)],
    };
  }

  /**
   * Create a safe version of an object with PII masked
   */
  createSafeObject(data: Record<string, any>): Record<string, any> {
    const safe: Record<string, any> = {};
    
    for (const [key, value] of Object.entries(data)) {
      if (this.isPIIField(key) || this.containsPII(String(value))) {
        safe[key] = this.maskValue(String(value), key);
      } else {
        safe[key] = value;
      }
    }
    
    return safe;
  }

  /**
   * Check if a field name indicates PII
   */
  private isPIIField(fieldName: string): boolean {
    const field = fieldName.toLowerCase();
    
    // Check against known PII fields
    if (piiFields.includes(fieldName)) {
      return true;
    }
    
    // Check common PII field patterns
    const piiFieldPatterns = [
      'ssn', 'social_security',
      'credit_card', 'card_number',
      'email', 'email_address',
      'phone', 'phone_number',
      'date_of_birth', 'dob', 'birth_date',
      'driver_license', 'license_number',
      'passport', 'account_number',
      'routing_number', 'bank_account'
    ];
    
    return piiFieldPatterns.some(pattern => field.includes(pattern));
  }

  /**
   * Mask a PII value
   */
  private maskValue(value: string, fieldName?: string): string {
    if (!value) return '[EMPTY]';
    
    const len = value.length;
    
    // Email - show domain
    if (this.patterns.email.test(value)) {
      const [local, domain] = value.split('@');
      return `${local.charAt(0)}${'*'.repeat(local.length - 1)}@${domain}`;
    }
    
    // Phone - show area code
    if (this.patterns.phone.test(value)) {
      const cleaned = value.replace(/\D/g, '');
      if (cleaned.length >= 10) {
        return `(${cleaned.substring(0, 3)}) ***-****`;
      }
    }
    
    // SSN - show last 4
    if (this.patterns.ssn.test(value)) {
      const cleaned = value.replace(/\D/g, '');
      if (cleaned.length === 9) {
        return `***-**-${cleaned.substring(5)}`;
      }
    }
    
    // Default masking
    if (len <= 4) {
      return '*'.repeat(len);
    } else if (len <= 8) {
      return value.substring(0, 1) + '*'.repeat(len - 2) + value.substring(len - 1);
    } else {
      return value.substring(0, 2) + '*'.repeat(len - 4) + value.substring(len - 2);
    }
  }
}

// Export singleton instance
export const piiDetector = new PIIDetector();

// Add missing static methods
export class PIIDetectorExtensions {
  static createSafeObject(obj: any): any {
    const safe: any = {};
    for (const [key, value] of Object.entries(obj)) {
      if (!PIIDetector.isPII(key) && !PIIDetector.containsPII(String(value))) {
        safe[key] = value;
      }
    }
    return safe;
  }

  static detectPII(data: any): string[] {
    const piiFields: string[] = [];
    for (const [key, value] of Object.entries(data)) {
      if (PIIDetector.isPII(key) || PIIDetector.containsPII(String(value))) {
        piiFields.push(key);
      }
    }
    return piiFields;
  }
}

// Extend PIIDetector
Object.assign(PIIDetector, PIIDetectorExtensions);

// Static method implementations
PIIDetector.isPII = function(fieldName: string): boolean {
  const piiFieldsList = [
    'email', 'phone', 'ssn', 'social_security_number',
    'first_name', 'last_name', 'date_of_birth', 'address',
    'credit_card', 'bank_account', 'driver_license'
  ];
  return piiFieldsList.includes(fieldName.toLowerCase());
};

PIIDetector.containsPII = function(value: string): boolean {
  if (!value) return false;
  // Check for SSN pattern
  if (/\b\d{3}-\d{2}-\d{4}\b/.test(value)) return true;
  // Check for credit card pattern
  if (/\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/.test(value)) return true;
  // Check for phone pattern
  if (/\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/.test(value)) return true;
  return false;
};

PIIDetector.createSafeObject = function(obj: any): any {
  const safe: any = {};
  for (const [key, value] of Object.entries(obj)) {
    if (!PIIDetector.isPII(key) && !PIIDetector.containsPII(String(value))) {
      safe[key] = value;
    }
  }
  return safe;
};

PIIDetector.detectPII = function(data: any): string[] {
  const piiFields: string[] = [];
  for (const [key, value] of Object.entries(data)) {
    if (PIIDetector.isPII(key) || PIIDetector.containsPII(String(value))) {
      piiFields.push(key);
    }
  }
  return piiFields;
};

// Declare static methods on the class
declare module './pii-detector' {
  interface PIIDetectorConstructor {
    isPII(fieldName: string): boolean;
    containsPII(value: string): boolean;
    createSafeObject(obj: any): any;
    detectPII(data: any): string[];
  }
}

interface PIIDetectorConstructor {
  new(): PIIDetector;
  isPII(fieldName: string): boolean;
  containsPII(value: string): boolean;
  createSafeObject(obj: any): any;
  detectPII(data: any): string[];
}

const PIIDetectorClass = PIIDetector as any as PIIDetectorConstructor;

// Add methods to the class
PIIDetectorClass.isPII = function(fieldName: string): boolean {
  const piiFieldsList = [
    'email', 'phone', 'ssn', 'social_security_number',
    'first_name', 'last_name', 'date_of_birth', 'address',
    'credit_card', 'bank_account', 'driver_license'
  ];
  return piiFieldsList.includes(fieldName.toLowerCase());
};

PIIDetectorClass.containsPII = function(value: string): boolean {
  if (!value) return false;
  if (/\b\d{3}-\d{2}-\d{4}\b/.test(value)) return true;
  if (/\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/.test(value)) return true;
  if (/\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/.test(value)) return true;
  return false;
};

PIIDetectorClass.createSafeObject = function(obj: any): any {
  const safe: any = {};
  for (const [key, value] of Object.entries(obj)) {
    if (!PIIDetectorClass.isPII(key) && !PIIDetectorClass.containsPII(String(value))) {
      safe[key] = value;
    }
  }
  return safe;
};

PIIDetectorClass.detectPII = function(data: any): string[] {
  const piiFields: string[] = [];
  for (const [key, value] of Object.entries(data)) {
    if (PIIDetectorClass.isPII(key) || PIIDetectorClass.containsPII(String(value))) {
      piiFields.push(key);
    }
  }
  return piiFields;
};
