# 🔒 Comprehensive Security Integration Plan for Claude Code Boilerplate

> **Version**: 1.0  
> **Date**: January 2025  
> **Status**: Planning Phase  
> **Impact**: Major enhancement to existing system

## Executive Summary

This plan integrates production-grade security features into the Claude Code Boilerplate system while maintaining its core philosophy of spec-driven development. The implementation leverages the official Claude Code hooks API and the new sub-agents feature for specialized security tasks.

## Table of Contents

1. [Current State Analysis](#current-state-analysis)
2. [Security Requirements](#security-requirements)
3. [Hooks Integration Strategy](#hooks-integration-strategy)
4. [Sub-Agents Architecture](#sub-agents-architecture)
5. [Implementation Phases](#implementation-phases)
6. [Technical Specifications](#technical-specifications)
7. [Migration Path](#migration-path)
8. [Success Metrics](#success-metrics)

---

## Current State Analysis

### Existing Security Features
- Basic secret scanning via `/sc` command
- PII protection hooks
- Form validation with Zod
- Event tracking for compliance
- Git hooks for pre-commit checks

### Critical Gaps
1. **No Rate Limiting** - APIs vulnerable to abuse
2. **No RLS Templates** - Manual Supabase security
3. **No CAPTCHA** - Forms vulnerable to bots
4. **No WAF Guidance** - Missing edge protection
5. **Limited Dependency Scanning** - No automated vulnerability checks
6. **No Security Sub-Agents** - Security is reactive, not proactive

### System Strengths to Leverage
- Robust hooks architecture already in place
- Event queue for non-blocking operations
- PRD/PRP workflow for requirements tracking
- Command chaining for complex workflows
- New sub-agents API for specialized tasks

---

## Security Requirements

### Core Security Features Needed

#### 1. Rate Limiting
- **API Routes**: Sliding window rate limits
- **Form Submissions**: Throttle by IP/user
- **Authentication**: Prevent brute force
- **Integration**: Upstash Redis or in-memory

#### 2. Row Level Security (RLS)
- **Supabase Policies**: Auto-generated templates
- **Testing**: RLS policy validation
- **Documentation**: Policy intent tracking
- **Monitoring**: Violation detection

#### 3. CAPTCHA Integration
- **reCAPTCHA v3**: Score-based protection
- **Fallback**: Challenge for low scores
- **Analytics**: Bot detection metrics
- **Accessibility**: Alternative options

#### 4. WAF Configuration
- **Cloudflare/Vercel**: Rule templates
- **DDoS Protection**: Rate limit rules
- **Geographic**: Country-based access
- **Bot Management**: Good bot allowlist

#### 5. Dependency Security
- **Scanning**: npm audit integration
- **Updates**: Automated PR creation
- **Policies**: Version pinning rules
- **SBOM**: Software bill of materials

#### 6. Input Validation & Sanitization
- **XSS Prevention**: Output encoding
- **SQL Injection**: Parameterized queries
- **CSRF**: Token validation
- **File Upload**: Type/size validation

---

## Hooks Integration Strategy

### Hook Architecture (Per Official Docs)

```json
{
  "hooks": [
    {
      "type": "pre-command",
      "command": "python3 .claude/hooks/security-pre-command.py",
      "matcher": {
        "command": ["create-component", "create-api", "create-tracked-form"]
      }
    },
    {
      "type": "post-command",
      "command": "python3 .claude/hooks/security-post-command.py",
      "output_stream": "stdout",
      "timeout": 5000
    },
    {
      "type": "pre-write-file",
      "command": "python3 .claude/hooks/security-pre-write.py",
      "matcher": {
        "path_pattern": "**/api/**/*.ts"
      }
    }
  ]
}
```

### Security Hooks Specification

#### 1. Pre-Command Security Hook
```python
# .claude/hooks/security-pre-command.py
import json
import sys

def handle_pre_command(event):
    command = event.get('command', '')
    args = event.get('args', {})
    
    # Security requirements based on command
    security_requirements = {
        'create-api': {
            'rate_limit': True,
            'auth_required': True,
            'input_validation': True,
            'suggest_rls': True
        },
        'create-tracked-form': {
            'captcha': True,
            'rate_limit': True,
            'csrf_token': True,
            'honeypot': True
        }
    }
    
    if command in security_requirements:
        return {
            "status": "continue",
            "message": f"🔒 Security requirements applied: {security_requirements[command]}",
            "metadata": {
                "security_config": security_requirements[command]
            }
        }
    
    return {"status": "continue"}
```

#### 2. Pre-Write Security Validator
```python
# .claude/hooks/security-pre-write.py
import json
import re

def validate_api_security(content):
    issues = []
    
    # Check for rate limiting
    if 'rateLimit' not in content and '/api/' in event.get('path', ''):
        issues.append({
            'type': 'missing_rate_limit',
            'severity': 'high',
            'fix': 'import { rateLimit } from "@/lib/security/middleware"'
        })
    
    # Check for input validation
    if 'parse(' not in content and ('POST' in content or 'PUT' in content):
        issues.append({
            'type': 'missing_validation',
            'severity': 'high',
            'fix': 'Add zod schema validation'
        })
    
    if issues:
        return {
            "status": "warning",
            "message": f"⚠️ Security issues detected: {len(issues)} problems found",
            "auto_fix_available": True,
            "issues": issues
        }
    
    return {"status": "continue"}
```

#### 3. Post-Command Security Analyzer
```python
# .claude/hooks/security-post-command.py
def analyze_security_posture(event):
    # Run after file creation to suggest improvements
    if event.get('command') in ['create-api', 'create-component']:
        suggestions = []
        
        # Analyze created files
        if 'api' in event.get('created_files', []):
            suggestions.append("Consider adding rate limiting: /enhance-api security")
            suggestions.append("Add RLS policies: /generate-rls")
        
        return {
            "suggestions": suggestions,
            "next_commands": ["security-audit", "test-security"]
        }
```

---

## Sub-Agents Architecture

### Security Sub-Agents Design

Using the new sub-agents API, we'll create specialized security agents:

#### 1. Security Auditor Agent
```typescript
// .claude/sub-agents/security-auditor.ts
export const securityAuditorConfig = {
  id: "security-auditor",
  name: "Security Auditor",
  description: "Performs comprehensive security audits",
  instructions: `You are a security expert focused on:
    - OWASP Top 10 vulnerabilities
    - Dependency vulnerability scanning
    - Code security patterns
    - Infrastructure security
    
    When spawned, automatically:
    1. Scan for security vulnerabilities
    2. Check dependencies
    3. Validate security configurations
    4. Generate security report`,
  
  tools: [
    "run-command",
    "read-file",
    "write-file"
  ],
  
  workflow: {
    auto_execute: [
      "npm audit",
      "validate-security all",
      "check-rls-policies",
      "scan-secrets"
    ]
  }
};
```

#### 2. RLS Policy Generator Agent
```typescript
// .claude/sub-agents/rls-generator.ts
export const rlsGeneratorConfig = {
  id: "rls-generator",
  name: "RLS Policy Generator",
  description: "Creates Supabase RLS policies from requirements",
  instructions: `You generate Row Level Security policies.
    
    Given a data model and access requirements:
    1. Create comprehensive RLS policies
    2. Generate test cases for policies
    3. Document policy intent
    4. Create migration files`,
  
  context_from_parent: ["database_schema", "user_roles", "access_matrix"]
};
```

#### 3. Security Enhancement Agent
```typescript
// .claude/sub-agents/security-enhancer.ts
export const securityEnhancerConfig = {
  id: "security-enhancer",
  name: "Security Enhancer",
  description: "Enhances existing code with security features",
  instructions: `You add security features to existing code:
    - Add rate limiting to APIs
    - Implement CAPTCHA in forms
    - Add input validation
    - Configure security headers
    
    Maintain existing functionality while adding security layers.`,
  
  templates: {
    rate_limit: "templates/security/rate-limit.ts",
    captcha: "templates/security/captcha.tsx",
    validation: "templates/security/validation.ts"
  }
};
```

### Sub-Agent Integration with Main Workflow

```typescript
// Enhanced command with sub-agent spawning
export const enhancedCommands = {
  'create-secure-api': async (name: string) => {
    // 1. Main agent creates basic API
    await createAPI(name);
    
    // 2. Spawn security enhancer
    const enhancer = await spawnSubAgent('security-enhancer', {
      task: `Add security to ${name} API`,
      context: { apiPath: `app/api/${name}/route.ts` }
    });
    
    // 3. Wait for enhancement
    await enhancer.complete();
    
    // 4. Spawn auditor for validation
    const auditor = await spawnSubAgent('security-auditor', {
      task: 'Validate security implementation',
      context: { focusPath: `app/api/${name}` }
    });
    
    return auditor.getReport();
  }
};
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Update `.claude/settings.json` with new hook configurations
- [ ] Create base security hooks following official API
- [ ] Implement security boilerplate templates
- [ ] Update command aliases for security variants

### Phase 2: Core Security Features (Week 2)
- [ ] Implement rate limiting middleware templates
- [ ] Create RLS policy generators
- [ ] Add CAPTCHA integration patterns
- [ ] Build input validation enhancers

### Phase 3: Sub-Agent Integration (Week 3)
- [ ] Implement security sub-agents
- [ ] Create sub-agent workflows
- [ ] Integrate with existing commands
- [ ] Add orchestration patterns

### Phase 4: Monitoring & Compliance (Week 4)
- [ ] Security dashboard in `/sr`
- [ ] Compliance reporting
- [ ] Vulnerability tracking
- [ ] Auto-remediation workflows

---

## Technical Specifications

### Security Middleware Stack
```typescript
// lib/security/middleware-stack.ts
export const securityStack = {
  // Rate Limiting
  rateLimit: {
    provider: 'upstash' | 'memory',
    config: {
      window: '1m',
      max: 100,
      keyGenerator: (req) => req.ip || 'anonymous'
    }
  },
  
  // Input Validation
  validation: {
    schemas: 'zod',
    sanitization: 'dompurify',
    encoding: 'he'
  },
  
  // CAPTCHA
  captcha: {
    provider: 'recaptcha-v3',
    threshold: 0.5,
    actions: ['submit_form', 'create_account']
  },
  
  // Security Headers
  headers: {
    csp: "default-src 'self'",
    hsts: 'max-age=31536000',
    xfo: 'DENY',
    referrer: 'strict-origin-when-cross-origin'
  }
};
```

### RLS Template System
```sql
-- templates/rls/user-owned-data.sql
CREATE POLICY "Users can view own {{table_name}}"
  ON public.{{table_name}}
  FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can update own {{table_name}}"
  ON public.{{table_name}}
  FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);
```

### Security Event Types
```typescript
// lib/events/security-events.ts
export const SECURITY_EVENTS = {
  // Rate Limiting
  RATE_LIMIT_EXCEEDED: 'security.rate_limit.exceeded',
  RATE_LIMIT_WARNING: 'security.rate_limit.warning',
  
  // Authentication
  AUTH_FAILED: 'security.auth.failed',
  AUTH_SUSPICIOUS: 'security.auth.suspicious',
  
  // RLS
  RLS_VIOLATION: 'security.rls.violation',
  RLS_POLICY_MISSING: 'security.rls.missing',
  
  // Input Validation
  VALIDATION_FAILED: 'security.validation.failed',
  XSS_ATTEMPT: 'security.xss.attempt',
  SQL_INJECTION_ATTEMPT: 'security.sql.attempt',
  
  // Dependencies
  VULNERABLE_DEPENDENCY: 'security.deps.vulnerable',
  OUTDATED_DEPENDENCY: 'security.deps.outdated'
};
```

---

## Migration Path

### For Existing Projects Using Boilerplate

1. **Run Security Audit**
   ```bash
   /chain security-baseline-audit
   ```

2. **Apply Security Patches**
   ```bash
   /spawn security-enhancer --task "Apply security to all APIs"
   ```

3. **Generate Missing Policies**
   ```bash
   /spawn rls-generator --analyze-models
   ```

4. **Update Monitoring**
   ```bash
   /security-events configure
   ```

### For New Projects

Security features will be included by default in:
- All API generators
- Form creators
- Database schemas
- Deployment configs

---

## Success Metrics

### Security Coverage
- 100% of APIs have rate limiting
- 100% of forms have CAPTCHA option
- 100% of database tables have RLS
- 0 high/critical vulnerabilities in dependencies

### Developer Experience
- Security adds < 5% to development time
- 90% of security issues auto-fixed
- Security status visible in daily workflow
- Clear security requirements in PRDs

### Production Metrics
- 50% reduction in bot traffic
- 90% reduction in API abuse
- 0 security incidents from missing validations
- 100% compliance with security checklist

---

## Integration with Existing System

### PRD Template Update
```markdown
## Security Requirements (Auto-Generated)
Based on features described above:
- [ ] APIs require rate limiting (100 req/min)
- [ ] Forms require CAPTCHA (score > 0.5)
- [ ] User data requires RLS policies
- [ ] All inputs must be validated
- [ ] Dependencies must be scanned
```

### Command Enhancement
```bash
# Existing commands get security flags
/cc Button --secure          # Adds XSS protection
/ctf ContactForm --captcha   # Includes reCAPTCHA
/create-api users --rls      # Generates with RLS

# New security commands
/security-audit              # Run full audit
/spawn security-auditor      # Deep security analysis
/enhance-security [target]   # Add security to existing code
```

### Workflow Integration
```json
{
  "chains": {
    "secure-feature-complete": {
      "extends": "feature-complete",
      "add_before_complete": [
        "spawn security-auditor --quick",
        "validate-security all",
        "check-dependencies"
      ]
    }
  }
}
```

---

## Next Steps

1. **Review & Approve** this plan
2. **Create Security Standards** document in `.agent-os/standards/security.md`
3. **Implement Phase 1** hooks following official API
4. **Test with Example Project** to validate approach
5. **Document Security Patterns** for team use

---

## Appendix: Security Boilerplate Examples

### Secure API Route
```typescript
// app/api/users/route.ts
import { rateLimit } from '@/lib/security/middleware';
import { apiSchema } from './schema';
import { withAuth } from '@/lib/auth';

export const POST = withAuth(
  rateLimit({
    window: '1m',
    max: 10,
    message: 'Too many requests'
  })(
    async (req) => {
      // Input validation
      const body = await req.json();
      const validated = apiSchema.parse(body);
      
      // Business logic with validated data
      // ...
    }
  )
);
```

### Secure Form Component
```tsx
// components/forms/ContactForm.tsx
import { ReCAPTCHA } from '@/components/security/recaptcha';
import { useRateLimit } from '@/hooks/useRateLimit';
import { contactSchema } from './schema';

export function ContactForm() {
  const { checkLimit } = useRateLimit('contact-form', {
    max: 3,
    window: '10m'
  });
  
  const onSubmit = async (data: FormData) => {
    // Rate limit check
    if (!await checkLimit()) {
      return { error: 'Too many submissions' };
    }
    
    // Validation
    const validated = contactSchema.parse(data);
    
    // CAPTCHA included in form
    // CSRF handled by framework
    // Honeypot field hidden
  };
}
```

---

This plan provides a comprehensive approach to integrating security into your Claude Code Boilerplate system while maintaining its philosophy and leveraging new features like sub-agents. The phased approach allows for gradual implementation without disrupting existing workflows.