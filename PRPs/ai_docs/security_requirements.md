# Security Requirements - AI Reference

## Core Security Principles

1. **Never Trust Client Input** - Always validate server-side
2. **Encrypt Sensitive Data** - PII/PHI must be encrypted at rest
3. **Audit Everything** - Log access to sensitive data
4. **Principle of Least Privilege** - Minimal access by default
5. **Defense in Depth** - Multiple layers of security

## PII/PHI Protection

### Identifying PII/PHI
```typescript
// Common PII fields (enforced by field registry)
const PII_FIELDS = [
  'ssn', 'social_security_number',
  'email', 'email_address',
  'phone', 'phone_number',
  'date_of_birth', 'dob',
  'driver_license',
  'passport_number',
  'credit_card', 'card_number',
  'bank_account',
  'ip_address',
  'full_name', 'legal_name'
];

// PHI fields (HIPAA)
const PHI_FIELDS = [
  'medical_record_number', 'mrn',
  'health_insurance_number',
  'diagnosis', 'treatment',
  'prescription',
  'lab_results',
  'mental_health_notes'
];
```

### Field-Level Encryption
```typescript
// ✅ CORRECT - Encrypt before storage
import { encryptField, decryptField } from '@/lib/security/encryption';

// Storing PII
const encryptedSSN = await encryptField(ssn, 'ssn');
await db.insert({
  ssn: encryptedSSN,
  // Other fields
});

// Retrieving PII
const user = await db.findOne({ id });
const decryptedSSN = await decryptField(user.ssn, 'ssn');

// ❌ WRONG - Storing PII in plain text
await db.insert({
  ssn: ssn, // Never store PII unencrypted!
});
```

### Secure Logging
```typescript
// ✅ CORRECT - No PII in logs
logger.info('User action', {
  userId: user.id,
  action: 'profile_update',
  timestamp: new Date()
});

// ✅ CORRECT - Masked PII if needed
logger.info('Phone validation', {
  phone: maskPhone(phone), // ***-***-1234
  valid: isValid
});

// ❌ WRONG - PII in logs
console.log('User data:', user); // Contains email, phone, etc
logger.error('Failed login', { email, password }); // Never log passwords!
```

### Client-Side Security
```typescript
// ❌ NEVER store PII client-side
localStorage.setItem('user', JSON.stringify(userData));
sessionStorage.setItem('ssn', ssn);
document.cookie = `email=${email}`;

// ❌ NEVER put PII in URLs
router.push(`/user?email=${email}`);
window.location.href = `/verify?ssn=${ssn}`;

// ✅ CORRECT - Use server-side sessions
// Store only non-sensitive identifiers client-side
localStorage.setItem('sessionId', sessionId);
router.push(`/user/${userId}`); // Use opaque IDs
```

## Authentication Patterns

### Password Requirements
```typescript
// Password validation schema
const PasswordSchema = z.string()
  .min(12, 'Password must be at least 12 characters')
  .regex(/[A-Z]/, 'Password must contain uppercase letter')
  .regex(/[a-z]/, 'Password must contain lowercase letter')
  .regex(/[0-9]/, 'Password must contain number')
  .regex(/[^A-Za-z0-9]/, 'Password must contain special character');

// ✅ NEVER store passwords - use hashing
import bcrypt from 'bcryptjs';

const hashedPassword = await bcrypt.hash(password, 12);
// Store hashedPassword, never the original
```

### Session Management
```typescript
// ✅ Secure session configuration
export const authOptions = {
  session: {
    strategy: 'jwt',
    maxAge: 30 * 60, // 30 minutes
  },
  cookies: {
    sessionToken: {
      name: 'session-token',
      options: {
        httpOnly: true,
        sameSite: 'lax',
        path: '/',
        secure: process.env.NODE_ENV === 'production'
      }
    }
  }
};

// ✅ Session validation on every request
export async function validateSession(req: Request) {
  const session = await getServerSession(authOptions);
  
  if (!session) {
    throw new UnauthorizedError('No session');
  }
  
  // Additional checks
  if (isExpired(session)) {
    throw new UnauthorizedError('Session expired');
  }
  
  return session;
}
```

### API Security
```typescript
// ✅ API route protection
export async function POST(req: Request) {
  // 1. Validate session
  const session = await validateSession(req);
  
  // 2. Check permissions
  if (!hasPermission(session.user, 'write')) {
    return Response.json({ error: 'Forbidden' }, { status: 403 });
  }
  
  // 3. Validate input
  const body = await req.json();
  const validated = InputSchema.parse(body);
  
  // 4. Rate limiting
  const rateLimitOk = await checkRateLimit(session.user.id);
  if (!rateLimitOk) {
    return Response.json({ error: 'Too many requests' }, { status: 429 });
  }
  
  // 5. Process request
  // ...
}
```

## Data Validation

### Input Sanitization
```typescript
import DOMPurify from 'isomorphic-dompurify';

// ✅ Sanitize HTML content
const sanitizedHTML = DOMPurify.sanitize(userInput, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
  ALLOWED_ATTR: ['href']
});

// ✅ SQL injection prevention (use parameterized queries)
const { data } = await supabase
  .from('users')
  .select('*')
  .eq('email', email); // Parameterized, not concatenated

// ❌ NEVER concatenate user input
const query = `SELECT * FROM users WHERE email = '${email}'`; // SQL injection!
```

### File Upload Security
```typescript
// ✅ Validate file uploads
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const MAX_SIZE = 5 * 1024 * 1024; // 5MB

function validateFile(file: File): string | null {
  if (!ALLOWED_TYPES.includes(file.type)) {
    return 'Invalid file type';
  }
  
  if (file.size > MAX_SIZE) {
    return 'File too large';
  }
  
  // Additional checks
  const ext = file.name.split('.').pop()?.toLowerCase();
  if (!['jpg', 'jpeg', 'png', 'webp'].includes(ext || '')) {
    return 'Invalid file extension';
  }
  
  return null;
}

// ✅ Scan for malware (if available)
const isSafe = await scanFile(file);
if (!isSafe) {
  throw new Error('File failed security scan');
}
```

## CORS & CSP Configuration

### CORS Settings
```typescript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: process.env.ALLOWED_ORIGIN },
          { key: 'Access-Control-Allow-Methods', value: 'GET,POST,PUT,DELETE,OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'Content-Type, Authorization' },
          { key: 'Access-Control-Max-Age', value: '86400' },
        ],
      },
    ];
  },
};
```

### Content Security Policy
```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const response = NextResponse.next();
  
  // Set security headers
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-XSS-Protection', '1; mode=block');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  
  // Content Security Policy
  response.headers.set(
    'Content-Security-Policy',
    "default-src 'self'; " +
    "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; " +
    "style-src 'self' 'unsafe-inline'; " +
    "img-src 'self' data: https:; " +
    "font-src 'self'; " +
    "connect-src 'self' https://api.supabase.io wss://api.supabase.io; " +
    "frame-ancestors 'none';"
  );
  
  return response;
}
```

## Compliance Requirements

### GDPR Compliance
```typescript
// ✅ Right to be forgotten
export async function deleteUserData(userId: string) {
  // Start transaction
  await db.transaction(async (tx) => {
    // Delete or anonymize all user data
    await tx.update(users).set({
      email: `deleted-${userId}@example.com`,
      name: 'Deleted User',
      phone: null,
      // Keep ID for referential integrity
    }).where(eq(users.id, userId));
    
    // Log the deletion
    await auditLog.create({
      action: 'user_data_deletion',
      userId,
      timestamp: new Date(),
      reason: 'GDPR request'
    });
  });
}

// ✅ Data export
export async function exportUserData(userId: string) {
  const userData = await collectAllUserData(userId);
  
  // Audit the export
  await auditLog.create({
    action: 'user_data_export',
    userId,
    timestamp: new Date()
  });
  
  return userData;
}
```

### TCPA Compliance (US)
```typescript
// ✅ Consent required for marketing communications
interface ConsentRecord {
  userId: string;
  consentType: 'sms' | 'email' | 'calls';
  granted: boolean;
  timestamp: Date;
  ipAddress: string;
  userAgent: string;
}

// Always get explicit consent
const consentCheckbox = (
  <label>
    <input
      type="checkbox"
      required
      onChange={(e) => setConsent(e.target.checked)}
    />
    I agree to receive marketing communications
  </label>
);
```

## Security Checklist

Before deploying:
- [ ] All PII fields encrypted
- [ ] No sensitive data in logs
- [ ] No PII in URLs or client storage
- [ ] Authentication required for sensitive routes
- [ ] Input validation on all endpoints
- [ ] Rate limiting implemented
- [ ] CORS properly configured
- [ ] CSP headers set
- [ ] Security headers enabled
- [ ] Audit logging active
- [ ] GDPR compliance verified
- [ ] TCPA consent flows implemented

Remember: Security is not optional. These patterns are enforced by hooks and will block non-compliant code.
