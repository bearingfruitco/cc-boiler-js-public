# Security Standards

## Core Security Principles

1. **Security by Default** - All generators include security features automatically
2. **Defense in Depth** - Multiple layers of security for critical operations
3. **Least Privilege** - Minimal permissions required for functionality
4. **Fail Secure** - Errors default to secure state, not open access

## API Security Requirements

### Rate Limiting (MANDATORY)
Every API route MUST implement rate limiting:

```typescript
import { rateLimit } from '@/lib/security/middleware';

// Standard rate limits
const limits = {
  public: { window: '1m', max: 100 },      // Public APIs
  authenticated: { window: '1m', max: 200 }, // Logged-in users
  sensitive: { window: '1m', max: 10 },     // Login, password reset
  admin: { window: '1m', max: 500 }         // Admin operations
};

export const POST = rateLimit(limits.public)(async (req) => {
  // Handler code
});
```

### Input Validation (MANDATORY)
All inputs MUST be validated with Zod schemas:

```typescript
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  age: z.number().int().positive().max(150)
});

export async function POST(req: Request) {
  const body = await req.json();
  const data = schema.parse(body); // Throws on invalid input
  // Use validated data
}
```

### Authentication & Authorization
Protected routes MUST check authentication:

```typescript
import { withAuth } from '@/lib/auth';

export const GET = withAuth(async (req, { user }) => {
  // user is guaranteed to be authenticated
  // Check additional permissions as needed
  if (!user.permissions.includes('admin')) {
    return new Response('Forbidden', { status: 403 });
  }
});
```

## Database Security

### Row Level Security (RLS)
ALL Supabase tables MUST have RLS policies:

```sql
-- Enable RLS
ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;

-- Users can only see their own data
CREATE POLICY "Users can view own posts" ON public.posts
  FOR SELECT USING (auth.uid() = user_id);

-- Users can only update their own data
CREATE POLICY "Users can update own posts" ON public.posts
  FOR UPDATE USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Admins can see everything
CREATE POLICY "Admins can view all posts" ON public.posts
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM public.profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'admin'
    )
  );
```

### Query Security
- NEVER use string concatenation for SQL
- ALWAYS use parameterized queries
- AVOID using service_role key in client code

## Form Security

### CAPTCHA Integration
Public forms MUST implement CAPTCHA:

```typescript
import { ReCAPTCHA } from '@/components/security/recaptcha';

export function ContactForm() {
  const [captchaToken, setCaptchaToken] = useState('');
  
  const onSubmit = async (data: FormData) => {
    if (!captchaToken) {
      setError('Please complete the CAPTCHA');
      return;
    }
    
    // Include token in submission
    await submitForm({ ...data, captchaToken });
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}
      <ReCAPTCHA
        siteKey={process.env.NEXT_PUBLIC_RECAPTCHA_SITE_KEY}
        onChange={setCaptchaToken}
      />
    </form>
  );
}
```

### CSRF Protection
Next.js App Router provides CSRF protection by default. For custom implementations:

```typescript
// Automatically handled by Next.js App Router
// For API routes, use built-in protections
// For external APIs, implement token validation
```

### Rate Limiting Forms
Implement client-side rate limiting:

```typescript
import { useRateLimit } from '@/hooks/useRateLimit';

export function Form() {
  const { checkLimit, remaining } = useRateLimit('contact-form', {
    max: 3,
    window: '10m'
  });
  
  const onSubmit = async (data) => {
    if (!await checkLimit()) {
      setError(`Too many attempts. ${remaining} attempts remaining.`);
      return;
    }
    // Submit form
  };
}
```

## Dependency Security

### Automated Scanning
Run dependency audits regularly:

```bash
# In package.json scripts
"security:check": "npm audit --audit-level=moderate",
"security:fix": "npm audit fix",
"security:update": "npx npm-check-updates -u"
```

### Version Pinning
Pin dependencies for production:

```json
{
  "dependencies": {
    "next": "15.0.3",        // Exact version
    "react": "^19.0.0",      // Minor updates OK
    "zod": "~3.22.0"         // Patch updates only
  }
}
```

## Security Headers

### Required Headers
Configure in next.config.js:

```javascript
const securityHeaders = [
  {
    key: 'X-DNS-Prefetch-Control',
    value: 'on'
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubDomains; preload'
  },
  {
    key: 'X-Frame-Options',
    value: 'SAMEORIGIN'
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  },
  {
    key: 'Referrer-Policy',
    value: 'strict-origin-when-cross-origin'
  },
  {
    key: 'Content-Security-Policy',
    value: ContentSecurityPolicy.replace(/\s{2,}/g, ' ').trim()
  }
];
```

## WAF Configuration

### Cloudflare Rules (Recommended)
```yaml
# Basic WAF rules
- Block requests with SQL keywords in query strings
- Rate limit by IP (100 req/min)
- Challenge suspicious user agents
- Block known bad IPs
- Enable Bot Fight Mode
```

### Vercel Edge Config
```typescript
// middleware.ts
export const config = {
  matcher: ['/api/:path*', '/auth/:path*']
};

export function middleware(req: NextRequest) {
  // Rate limiting at edge
  // Geo-blocking if needed
  // Bot detection
}
```

## Security Monitoring

### Event Tracking
Track security events via event queue:

```typescript
import { eventQueue, SECURITY_EVENTS } from '@/lib/events';

// Non-blocking security events
eventQueue.emit(SECURITY_EVENTS.RATE_LIMIT_HIT, {
  ip: request.ip,
  endpoint: '/api/contact',
  timestamp: Date.now()
});

// Critical events that need logging
await logSecurityEvent({
  type: 'AUTH_FAILED',
  ip: request.ip,
  attempted_username: username
});
```

### Alerts
Configure alerts for:
- Multiple failed auth attempts
- Rate limit violations
- RLS policy violations
- Dependency vulnerabilities

## Security Checklist

### Pre-Deployment
- [ ] All APIs have rate limiting
- [ ] All forms have validation
- [ ] All inputs are sanitized
- [ ] RLS policies exist for all tables
- [ ] CAPTCHA on public forms
- [ ] Security headers configured
- [ ] Dependencies scanned
- [ ] No secrets in code

### Post-Deployment
- [ ] Monitor rate limit hits
- [ ] Review auth failures
- [ ] Check for vulnerabilities
- [ ] Update dependencies monthly
- [ ] Security audit quarterly

## Enforcement

These standards are enforced via:
1. **Pre-commit hooks** - Block insecure code
2. **CI/CD checks** - Automated security scanning
3. **Code review** - Manual security review
4. **Runtime monitoring** - Track violations

Non-compliance will result in:
- Build failures for critical issues
- Warnings for best practices
- Automated fixes where possible
- Security debt tracking
