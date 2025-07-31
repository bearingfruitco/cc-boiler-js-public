#!/usr/bin/env python3
"""
Comprehensive Security Validator Hook
Consolidates PII protection, TCPA compliance, and general security validation
"""

import json
import sys
import re
from pathlib import Path

class SecurityValidator:
    """Comprehensive security validation hook"""
    
    # PII Protection patterns
    PII_FIELDS = [
        'email', 'phone', 'ssn', 'social_security',
        'first_name', 'last_name', 'full_name', 'name',
        'address', 'street', 'city', 'state', 'zip', 'postal',
        'date_of_birth', 'dob', 'birthdate',
        'credit_card', 'card_number', 'cvv', 'expiry',
        'bank_account', 'routing_number', 'iban',
        'drivers_license', 'passport', 'national_id',
        'ip_address', 'user_id', 'customer_id',
        'password', 'secret', 'api_key', 'token'
    ]
    
    # TCPA messaging keywords
    MESSAGING_KEYWORDS = [
        'sendSMS', 'sendMessage', 'sendText', 
        'twilio', 'sendgrid', 'messagebird', 'nexmo',
        'sms', 'text message', 'notification',
        'phone', 'mobile', 'cellular'
    ]
    
    # Security patterns
    SECURITY_PATTERNS = {
        'console_log': r'console\.(log|debug|info)\s*\(',
        'hardcoded_secret': r'(api[_-]?key|secret|password|token)\s*[:=]\s*["\'][^"\']+["\']',
        'eval_usage': r'\beval\s*\(',
        'innerHTML': r'\.innerHTML\s*=',
        'dangerouslySetInnerHTML': r'dangerouslySetInnerHTML',
        'sql_injection': r'(SELECT|INSERT|UPDATE|DELETE).+\+.*["\']',
    }
    
    def __init__(self):
        self.violations = []
        self.warnings = []
    
    def validate(self, operation):
        """Main validation entry point"""
        content = operation.get('content', '')
        file_path = operation.get('path', '')
        tool = operation.get('tool', '')
        
        # Run all security checks
        self.check_pii_protection(content, file_path)
        self.check_tcpa_compliance(content, file_path)
        self.check_general_security(content, file_path, tool)
        
        # Return results
        if self.violations:
            return self.format_response(False)
        elif self.warnings:
            return self.format_response(True, warnings=True)
        else:
            return {'approved': True}
    
    def check_pii_protection(self, content, file_path):
        """Check for PII exposure risks"""
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_lower = line.lower()
            
            # Check console.log with PII
            if 'console.' in line:
                for pii_field in self.PII_FIELDS:
                    if pii_field in line_lower and not self.is_safe_log(line):
                        self.violations.append({
                            'type': 'pii_in_console',
                            'line': line_num,
                            'field': pii_field,
                            'message': f'Potential PII ({pii_field}) in console.log',
                            'severity': 'high'
                        })
            
            # Check URL parameters with PII
            if any(pattern in line for pattern in ['?', '&', 'searchParams', 'URLSearchParams']):
                for pii_field in self.PII_FIELDS:
                    if pii_field in line_lower and self.is_url_param(line):
                        self.violations.append({
                            'type': 'pii_in_url',
                            'line': line_num,
                            'field': pii_field,
                            'message': f'PII ({pii_field}) exposed in URL parameters',
                            'severity': 'high'
                        })
            
            # Check localStorage/sessionStorage
            if any(storage in line for storage in ['localStorage', 'sessionStorage']):
                for pii_field in self.PII_FIELDS:
                    if pii_field in line_lower:
                        self.violations.append({
                            'type': 'pii_in_storage',
                            'line': line_num,
                            'field': pii_field,
                            'message': f'PII ({pii_field}) stored in browser storage',
                            'severity': 'critical'
                        })
            
            # Check form fields for proper masking
            if 'type="text"' in line and any(pii in line_lower for pii in ['ssn', 'social', 'credit', 'card']):
                self.warnings.append({
                    'type': 'unmasked_sensitive_field',
                    'line': line_num,
                    'message': 'Sensitive field should use type="password" or masking',
                    'severity': 'medium'
                })
    
    def check_tcpa_compliance(self, content, file_path):
        """Check for TCPA compliance in messaging"""
        content_lower = content.lower()
        
        # Check if this contains messaging functionality
        is_messaging = any(keyword in content_lower for keyword in self.MESSAGING_KEYWORDS)
        if not is_messaging:
            return
        
        # Required TCPA elements
        has_consent_check = any(term in content_lower for term in [
            'consent', 'opt-in', 'optin', 'permission', 'subscribe'
        ])
        
        has_opt_out = any(term in content_lower for term in [
            'opt-out', 'optout', 'unsubscribe', 'stop', 'cancel'
        ])
        
        has_time_restriction = any(term in content_lower for term in [
            'business hours', 'time restriction', 'allowed hours',
            'quiet hours', 'do not disturb'
        ])
        
        # Check for violations
        if not has_consent_check:
            self.violations.append({
                'type': 'tcpa_missing_consent',
                'message': 'Messaging feature missing consent verification',
                'severity': 'critical',
                'fix': 'Add consent check: if (!user.smsConsent) throw new Error("User has not consented to SMS");'
            })
        
        if not has_opt_out:
            self.violations.append({
                'type': 'tcpa_missing_optout',
                'message': 'Messaging feature missing opt-out mechanism',
                'severity': 'high',
                'fix': 'Add opt-out handling: if (message.includes("STOP")) { await unsubscribeUser(phoneNumber); }'
            })
        
        if not has_time_restriction:
            self.warnings.append({
                'type': 'tcpa_no_time_check',
                'message': 'Consider adding time restrictions for messaging',
                'severity': 'medium',
                'fix': 'Check time before sending: if (!isBusinessHours()) { await queueForLater(message); }'
            })
    
    def check_general_security(self, content, file_path, tool):
        """General security checks"""
        
        # API route security
        if '/api/' in file_path and file_path.endswith('.ts'):
            self.check_api_security(content)
        
        # Form security
        if '<form' in content or 'Form' in content:
            self.check_form_security(content)
        
        # General patterns
        for pattern_name, pattern in self.SECURITY_PATTERNS.items():
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                
                if pattern_name == 'console_log' and 'production' not in content[:match.start()]:
                    self.warnings.append({
                        'type': 'console_in_production',
                        'line': line_num,
                        'message': 'Console.log should be removed in production',
                        'severity': 'low'
                    })
                elif pattern_name == 'hardcoded_secret':
                    self.violations.append({
                        'type': 'hardcoded_secret',
                        'line': line_num,
                        'message': 'Hardcoded secret detected',
                        'severity': 'critical'
                    })
                elif pattern_name in ['eval_usage', 'innerHTML', 'dangerouslySetInnerHTML']:
                    self.violations.append({
                        'type': 'dangerous_operation',
                        'line': line_num,
                        'message': f'Dangerous operation: {pattern_name}',
                        'severity': 'high'
                    })
                elif pattern_name == 'sql_injection':
                    self.violations.append({
                        'type': 'sql_injection_risk',
                        'line': line_num,
                        'message': 'Potential SQL injection vulnerability',
                        'severity': 'critical'
                    })
    
    def check_api_security(self, content):
        """Check API route security"""
        # Rate limiting
        if 'rateLimit' not in content and any(method in content for method in ['POST', 'PUT', 'DELETE']):
            self.violations.append({
                'type': 'missing_rate_limit',
                'message': 'API route missing rate limiting',
                'severity': 'high',
                'fix': 'import { rateLimit } from "@/lib/security/middleware";'
            })
        
        # Input validation
        if 'parse(' not in content and 'validate(' not in content:
            self.warnings.append({
                'type': 'missing_validation',
                'message': 'API route missing input validation',
                'severity': 'medium',
                'fix': 'Use Zod schema: const data = schema.parse(await req.json());'
            })
        
        # Authentication
        if 'auth' not in content.lower() and 'session' not in content.lower():
            self.warnings.append({
                'type': 'missing_auth_check',
                'message': 'API route may need authentication',
                'severity': 'medium'
            })
    
    def check_form_security(self, content):
        """Check form security"""
        # CSRF protection
        if 'csrf' not in content.lower() and 'action="' in content:
            self.warnings.append({
                'type': 'missing_csrf',
                'message': 'Form missing CSRF protection',
                'severity': 'medium'
            })
        
        # Validation
        if 'validate' not in content and 'schema' not in content:
            self.warnings.append({
                'type': 'form_validation',
                'message': 'Form missing client-side validation',
                'severity': 'low'
            })
    
    def is_safe_log(self, line):
        """Check if console.log is safe (e.g., in development only)"""
        return any(safe in line for safe in [
            'process.env.NODE_ENV',
            'development',
            'debug',
            '// TODO: Remove'
        ])
    
    def is_url_param(self, line):
        """Check if line contains URL parameter assignment"""
        return any(pattern in line for pattern in [
            '.set(',
            '.append(',
            '?',
            '&',
            'searchParams'
        ])
    
    def format_response(self, approved, warnings=False):
        """Format the validation response"""
        if not approved:
            return {
                'approved': False,
                'message': 'Security violations detected',
                'violations': self.violations,
                'fix_required': True
            }
        elif warnings:
            return {
                'approved': True,
                'message': 'Approved with warnings',
                'warnings': self.warnings,
                'continue': True
            }
        else:
            return {'approved': True}

# Hook entry point
def main():
    operation = json.loads(sys.stdin.read())
    validator = SecurityValidator()
    result = validator.validate(operation)
    print(json.dumps(result))

if __name__ == '__main__':
    main()
