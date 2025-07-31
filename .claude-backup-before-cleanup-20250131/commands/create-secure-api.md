# /create-secure-api

Create a new API endpoint with mandatory security controls, following security-first development principles.

## Usage
```
/create-secure-api <endpoint-name> [options]
```

## Options
- `--method <GET|POST|PUT|DELETE>` - HTTP method (default: GET)
- `--auth-required` - Require authentication (default: true)
- `--rate-limit <number>` - Requests per minute (default: 60)
- `--no-security` - Skip security (requires confirmation)

## What This Command Does

1. **Security Analysis**
   - Analyzes endpoint requirements
   - Identifies data access patterns
   - Determines authentication needs
   - Generates threat model

2. **RLS Policy Generation**
   - Creates Row Level Security policies
   - Generates permission matrix
   - Sets up role-based access
   - Creates audit policies

3. **Security Tests**
   - Authentication tests
   - Authorization tests
   - Input validation tests
   - Rate limiting tests
   - OWASP Top 10 checks

4. **API Implementation**
   - Secure endpoint boilerplate
   - Input validation schemas
   - Error handling
   - Rate limiting middleware
   - CORS configuration

5. **Documentation**
   - Security requirements
   - API documentation
   - Permission matrix
   - Threat model

## Example

```bash
/create-secure-api user-profile --method GET --rate-limit 100
```

This generates:
```
app/api/user-profile/
├── route.ts              # Secure API endpoint
├── security.ts           # Security middleware
├── validation.ts         # Input validation
├── rate-limit.ts        # Rate limiting
└── tests/
    ├── auth.test.ts     # Authentication tests
    ├── authz.test.ts    # Authorization tests
    └── security.test.ts # Security tests

.claude/security/
├── policies/user-profile.sql    # RLS policies
├── rules/user-profile.json      # Permission matrix
└── threats/user-profile.md      # Threat model
```

## Security Controls Applied

### 1. Authentication
```typescript
// Automatic auth check
const session = await getServerSession();
if (!session && authRequired) {
  return new Response('Unauthorized', { status: 401 });
}
```

### 2. Authorization
```typescript
// Role-based access control
const hasPermission = await checkPermission(
  session.user.id,
  resource,
  action
);
```

### 3. Input Validation
```typescript
// Zod schema validation
const validated = schema.parse(await request.json());
```

### 4. Rate Limiting
```typescript
// Per-user rate limiting
const { success } = await rateLimit.check(session.user.id);
if (!success) {
  return new Response('Too Many Requests', { status: 429 });
}
```

### 5. Security Headers
```typescript
// Security headers
headers.set('X-Content-Type-Options', 'nosniff');
headers.set('X-Frame-Options', 'DENY');
headers.set('X-XSS-Protection', '1; mode=block');
```

## Generated RLS Example

```sql
-- Policy: user_profile_select
CREATE POLICY "user_profile_select" ON profiles
FOR SELECT
USING (
  auth.uid() IS NOT NULL
  AND (
    auth.uid() = user_id
    OR is_public = true
  )
);

-- Policy: user_profile_update
CREATE POLICY "user_profile_update" ON profiles
FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);
```

## Security Test Example

```typescript
describe('Security: user-profile API', () => {
  test('requires authentication', async () => {
    const response = await fetch('/api/user-profile', {
      headers: { /* no auth */ }
    });
    expect(response.status).toBe(401);
  });
  
  test('prevents access to other users data', async () => {
    const response = await authenticatedFetch(
      '/api/user-profile?userId=other-user'
    );
    expect(response.status).toBe(403);
  });
  
  test('validates input', async () => {
    const response = await authenticatedFetch('/api/user-profile', {
      method: 'POST',
      body: { invalid: 'data' }
    });
    expect(response.status).toBe(400);
  });
});
```

## Skipping Security (Not Recommended)

If you must skip security:
```bash
/create-secure-api public-health-check --no-security
```

You'll be prompted to provide justification, which is logged for audit purposes.

## Post-Creation Workflow

1. **Review Generated Security**
   - Check RLS policies
   - Verify permission matrix
   - Review threat model

2. **Run Security Tests**
   ```bash
   pnpm test:security user-profile
   ```

3. **Deploy RLS Policies**
   ```bash
   pnpm supabase:deploy
   ```

4. **Security Audit**
   ```bash
   /spawn-agent security-auditor audit-api user-profile
   ```

## Related Commands
- `/spawn-agent security-auditor` - Run security audit
- `/generate-rls` - Generate RLS policies
- `/security-check api` - Check API security
- `/threat-model` - Generate threat model
