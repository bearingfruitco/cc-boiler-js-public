import { PIIDetector } from './pii-detector';

interface AuditLogEntry {
  id: string;
  timestamp: string;
  action: string;
  userId?: string;
  sessionId: string;
  ipAddress: string;
  userAgent: string;
  resource: string;
  fields?: string[];
  result: 'success' | 'failure' | 'blocked';
  metadata?: Record<string, any>;
  duration?: number;
}

export class AuditLogger {
  private static readonly AUDIT_ACTIONS = {
    // Data access
    VIEW_PII: 'view_pii',
    EXPORT_DATA: 'export_data',
    SEARCH_RECORDS: 'search_records',
    
    // Data modification
    CREATE_RECORD: 'create_record',
    UPDATE_RECORD: 'update_record',
    DELETE_RECORD: 'delete_record',
    
    // Security events
    LOGIN_ATTEMPT: 'login_attempt',
    PERMISSION_CHECK: 'permission_check',
    ENCRYPTION_OPERATION: 'encryption_operation',
    
    // Compliance
    CONSENT_GIVEN: 'consent_given',
    CONSENT_WITHDRAWN: 'consent_withdrawn',
    DATA_RETENTION_CHECK: 'data_retention_check',
  };
  
  /**
   * Log an audit event
   */
  static async log(entry: Omit<AuditLogEntry, 'id' | 'timestamp'>): Promise<void> {
    const auditEntry: AuditLogEntry = {
      id: this.generateAuditId(),
      timestamp: new Date().toISOString(),
      ...entry,
    };
    
    // Ensure no PII in metadata
    if (auditEntry.metadata) {
      auditEntry.metadata = PIIDetector.createSafeObject(auditEntry.metadata);
    }
    
    // In production, send to secure audit log storage
    // For now, we'll structure it for proper storage
    await this.storeAuditLog(auditEntry);
  }
  
  /**
   * Log PII access
   */
  static async logPIIAccess(params: {
    userId?: string;
    sessionId: string;
    ipAddress: string;
    userAgent: string;
    resource: string;
    fields: string[];
    purpose: string;
  }): Promise<void> {
    await this.log({
      action: this.AUDIT_ACTIONS.VIEW_PII,
      userId: params.userId,
      sessionId: params.sessionId,
      ipAddress: params.ipAddress,
      userAgent: params.userAgent,
      resource: params.resource,
      fields: params.fields,
      result: 'success',
      metadata: {
        purpose: params.purpose,
        fieldCount: params.fields.length,
      },
    });
  }
  
  /**
   * Log form submission
   */
  static async logFormSubmission(params: {
    formId: string;
    sessionId: string;
    ipAddress: string;
    userAgent: string;
    fields: string[];
    hasConsent: boolean;
    leadId?: string;
  }): Promise<void> {
    await this.log({
      action: this.AUDIT_ACTIONS.CREATE_RECORD,
      sessionId: params.sessionId,
      ipAddress: params.ipAddress,
      userAgent: params.userAgent,
      resource: `form:${params.formId}`,
      fields: params.fields,
      result: 'success',
      metadata: {
        hasConsent: params.hasConsent,
        leadId: params.leadId,
        fieldCount: params.fields.length,
      },
    });
  }
  
  /**
   * Log consent events
   */
  static async logConsent(params: {
    userId: string;
    sessionId: string;
    ipAddress: string;
    userAgent: string;
    consentType: string;
    granted: boolean;
    version: string;
  }): Promise<void> {
    await this.log({
      action: params.granted 
        ? this.AUDIT_ACTIONS.CONSENT_GIVEN 
        : this.AUDIT_ACTIONS.CONSENT_WITHDRAWN,
      userId: params.userId,
      sessionId: params.sessionId,
      ipAddress: params.ipAddress,
      userAgent: params.userAgent,
      resource: `consent:${params.consentType}`,
      result: 'success',
      metadata: {
        version: params.version,
        timestamp: new Date().toISOString(),
      },
    });
  }
  
  /**
   * Log security events
   */
  static async logSecurityEvent(params: {
    event: 'blocked_pii_in_url' | 'blocked_pii_in_logs' | 'encryption_failure';
    sessionId: string;
    ipAddress: string;
    userAgent: string;
    details: Record<string, any>;
  }): Promise<void> {
    await this.log({
      action: this.AUDIT_ACTIONS.PERMISSION_CHECK,
      sessionId: params.sessionId,
      ipAddress: params.ipAddress,
      userAgent: params.userAgent,
      resource: `security:${params.event}`,
      result: 'blocked',
      metadata: PIIDetector.createSafeObject(params.details),
    });
  }
  
  /**
   * Generate unique audit ID
   */
  private static generateAuditId(): string {
    return `audit_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
  
  /**
   * Store audit log entry
   */
  private static async storeAuditLog(entry: AuditLogEntry): Promise<void> {
    // In production, this would:
    // 1. Encrypt the entry
    // 2. Send to secure audit log storage (not regular DB)
    // 3. Ensure write-once, read-many storage
    // 4. Implement retention policies
    
    // For development, we'll structure it properly
    if (process.env.NODE_ENV === 'development') {
      console.log('[AUDIT]', {
        action: entry.action,
        resource: entry.resource,
        result: entry.result,
        timestamp: entry.timestamp,
      });
    }
    
    // Production would use something like:
    // await auditStorage.write(entry);
  }
  
  /**
   * Query audit logs (with access control)
   */
  static async query(params: {
    startDate: Date;
    endDate: Date;
    action?: string;
    userId?: string;
    resource?: string;
  }): Promise<AuditLogEntry[]> {
    // This would require proper access control
    // Only authorized personnel should query audit logs
    
    throw new Error('Audit log queries must be performed through secure admin interface');
  }
}
