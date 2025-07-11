import { piiFields } from '@/field-registry/compliance/pii-fields.json';
import { phiFields } from '@/field-registry/compliance/phi-fields.json';

export class PIIDetector {
  // Common PII patterns
  private static patterns = {
    ssn: /\b\d{3}-?\d{2}-?\d{4}\b/,
    email: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/,
    phone: /\b(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b/,
    creditCard: /\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/,
    ipAddress: /\b(?:\d{1,3}\.){3}\d{1,3}\b/,
    dateOfBirth: /\b(0[1-9]|1[0-2])[-\/](0[1-9]|[12]\d|3[01])[-\/](19|20)\d{2}\b/,
    // PHI patterns
    medicalRecordNumber: /\b(MRN|mrn)[\s:#-]?\d{6,10}\b/i,
    healthPlanNumber: /\b(HPN|hpn)[\s:#-]?\d{8,12}\b/i,
    diagnosisCode: /\b[A-Z]\d{2}\.?\d{1,2}\b/, // ICD-10 format
    procedureCode: /\b\d{5}\b/, // CPT code format
    npi: /\b\d{10}\b/, // National Provider Identifier
  };
  
  /**
   * Detect PII in a string value
   */
  static detectPII(value: string): {
    hasPII: boolean;
    types: string[];
    matches: Array<{ type: string; value: string }>;
  } {
    const results = {
      hasPII: false,
      types: [] as string[],
      matches: [] as Array<{ type: string; value: string }>,
    };
    
    // Check against patterns
    for (const [type, pattern] of Object.entries(this.patterns)) {
      const matches = value.match(pattern);
      if (matches) {
        results.hasPII = true;
        results.types.push(type);
        results.matches.push({ type, value: matches[0] });
      }
    }
    
    return results;
  }
  
  /**
   * Check if a field name is PII
   */
  static isPIIField(fieldName: string): boolean {
    // Check all PII categories
    for (const category of Object.values(piiFields.categories)) {
      if (category.fields.includes(fieldName)) {
        return true;
      }
    }
    
    // Check PHI categories for HIPAA
    for (const category of Object.values(phiFields.categories)) {
      if (category.fields.includes(fieldName)) {
        return true;
      }
    }
    
    // Check common PII field name patterns
    const piiFieldPatterns = [
      /ssn/i,
      /social.*security/i,
      /email/i,
      /phone/i,
      /address/i,
      /birth.*date/i,
      /dob/i,
      /credit.*card/i,
      /bank.*account/i,
      /driver.*license/i,
      /passport/i,
      // PHI patterns
      /patient/i,
      /medical/i,
      /diagnosis/i,
      /treatment/i,
      /prescription/i,
      /health/i,
      /clinical/i,
      /lab.*result/i,
      /procedure/i,
      /medication/i,
    ];
    
    return piiFieldPatterns.some(pattern => pattern.test(fieldName));
  }
  
  /**
   * Scan an object for PII
   */
  static scanObject(obj: any, path = ''): Array<{
    path: string;
    field: string;
    reason: string;
    value?: any;
  }> {
    const issues: Array<{
      path: string;
      field: string;
      reason: string;
      value?: any;
    }> = [];
    
    if (!obj || typeof obj !== 'object') {
      return issues;
    }
    
    for (const [key, value] of Object.entries(obj)) {
      const currentPath = path ? `${path}.${key}` : key;
      
      // Check if field name indicates PII
      if (this.isPIIField(key)) {
        issues.push({
          path: currentPath,
          field: key,
          reason: 'PII field name detected',
          value: this.maskValue(value),
        });
      }
      
      // Check string values for PII patterns
      if (typeof value === 'string') {
        const detection = this.detectPII(value);
        if (detection.hasPII) {
          issues.push({
            path: currentPath,
            field: key,
            reason: `PII pattern detected: ${detection.types.join(', ')}`,
            value: this.maskValue(value),
          });
        }
      }
      
      // Recurse into nested objects
      if (typeof value === 'object' && value !== null) {
        issues.push(...this.scanObject(value, currentPath));
      }
    }
    
    return issues;
  }
  
  /**
   * Mask PII value for logging
   */
  static maskValue(value: any): string {
    if (!value) return '[empty]';
    
    const str = String(value);
    
    // Apply specific masking patterns
    if (this.patterns.ssn.test(str)) {
      return str.replace(/\d{3}-?\d{2}/, 'XXX-XX');
    }
    
    if (this.patterns.email.test(str)) {
      return str.replace(/^([^@]{1,3})[^@]*(@.+)$/, '$1***$2');
    }
    
    if (this.patterns.phone.test(str)) {
      return str.replace(/\d{3}([-.\s]?)\d{4}$/, 'XXX$1XXXX');
    }
    
    if (this.patterns.creditCard.test(str)) {
      return str.replace(/\d{4}[\s-]?\d{4}[\s-]?\d{4}/, 'XXXX-XXXX-XXXX');
    }
    
    // Generic masking for other values
    if (str.length > 4) {
      return str.substring(0, 2) + '*'.repeat(Math.min(str.length - 4, 10)) + str.slice(-2);
    }
    
    return '*'.repeat(str.length);
  }
  
  /**
   * Create safe version of object for logging
   */
  static createSafeObject(obj: any): any {
    if (!obj || typeof obj !== 'object') {
      return obj;
    }
    
    const safe: any = Array.isArray(obj) ? [] : {};
    
    for (const [key, value] of Object.entries(obj)) {
      if (this.isPIIField(key)) {
        safe[key] = '[REDACTED-PII]';
      } else if (typeof value === 'string') {
        const detection = this.detectPII(value);
        safe[key] = detection.hasPII ? this.maskValue(value) : value;
      } else if (typeof value === 'object' && value !== null) {
        safe[key] = this.createSafeObject(value);
      } else {
        safe[key] = value;
      }
    }
    
    return safe;
  }
}
