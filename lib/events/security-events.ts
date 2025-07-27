/**
 * Security Events
 * Track security-related events through the event queue
 */

export const SECURITY_EVENTS = {
  // Rate Limiting Events
  RATE_LIMIT_HIT: 'security.rate_limit.hit',
  RATE_LIMIT_EXCEEDED: 'security.rate_limit.exceeded',
  RATE_LIMIT_WARNING: 'security.rate_limit.warning',
  
  // Authentication Events
  AUTH_SUCCESS: 'security.auth.success',
  AUTH_FAILED: 'security.auth.failed',
  AUTH_SUSPICIOUS: 'security.auth.suspicious',
  AUTH_LOCKOUT: 'security.auth.lockout',
  
  // RLS & Database Events
  RLS_VIOLATION: 'security.rls.violation',
  RLS_POLICY_MISSING: 'security.rls.missing',
  SQL_INJECTION_ATTEMPT: 'security.sql.injection_attempt',
  
  // Input Validation Events
  VALIDATION_FAILED: 'security.validation.failed',
  XSS_ATTEMPT: 'security.xss.attempt',
  MALICIOUS_INPUT: 'security.input.malicious',
  
  // CAPTCHA Events
  CAPTCHA_FAILED: 'security.captcha.failed',
  CAPTCHA_SUCCESS: 'security.captcha.success',
  BOT_DETECTED: 'security.bot.detected',
  
  // API Security Events
  API_SUCCESS: 'security.api.success',
  API_ERROR: 'security.api.error',
  API_ABUSE: 'security.api.abuse',
  CORS_VIOLATION: 'security.cors.violation',
  
  // Dependency Events
  VULNERABLE_DEPENDENCY: 'security.deps.vulnerable',
  OUTDATED_DEPENDENCY: 'security.deps.outdated',
  LICENSE_VIOLATION: 'security.deps.license_violation',
  
  // General Security Events
  SECURITY_SCAN_STARTED: 'security.scan.started',
  SECURITY_SCAN_COMPLETED: 'security.scan.completed',
  SECURITY_ISSUE_FOUND: 'security.issue.found',
  SECURITY_ISSUE_FIXED: 'security.issue.fixed',
};

/**
 * Security event metadata types
 */
export interface SecurityEventMetadata {
  timestamp: number;
  severity?: 'low' | 'medium' | 'high' | 'critical';
  userId?: string;
  ip?: string;
  endpoint?: string;
  method?: string;
  userAgent?: string;
  details?: Record<string, any>;
}

/**
 * Helper to emit security events with consistent metadata
 */
export function emitSecurityEvent(
  eventName: string,
  metadata: Partial<SecurityEventMetadata> = {}
) {
  const { eventQueue } = require('@/lib/events');
  
  eventQueue.emit(eventName, {
    timestamp: Date.now(),
    ...metadata,
  });
}

/**
 * Security event handlers
 * These process security events asynchronously
 */
export const securityEventHandlers = {
  [SECURITY_EVENTS.RATE_LIMIT_EXCEEDED]: async (data: SecurityEventMetadata) => {
    // Log to monitoring service
    console.warn('Rate limit exceeded:', data);
    
    // Could send alert if pattern detected
    // Could temporarily block IP if repeated
  },
  
  [SECURITY_EVENTS.AUTH_FAILED]: async (data: SecurityEventMetadata) => {
    // Track failed attempts
    // Implement account lockout after N attempts
    console.warn('Authentication failed:', data);
  },
  
  [SECURITY_EVENTS.SQL_INJECTION_ATTEMPT]: async (data: SecurityEventMetadata) => {
    // Critical security event
    console.error('SQL injection attempt detected:', data);
    // Send immediate alert
    // Block IP
  },
  
  [SECURITY_EVENTS.VULNERABLE_DEPENDENCY]: async (data: SecurityEventMetadata) => {
    // Create GitHub issue
    // Send notification
    console.error('Vulnerable dependency detected:', data);
  },
};

/**
 * Register security event handlers with the event queue
 */
export function registerSecurityHandlers(eventQueue: any) {
  Object.entries(securityEventHandlers).forEach(([event, handler]) => {
    eventQueue.on(event, handler);
  });
}
