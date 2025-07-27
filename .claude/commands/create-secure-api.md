# create-secure-api

Creates a new API route with all security features pre-configured.

## Usage
```bash
create-secure-api <name> [options]
```

## Arguments
- `name` - Name of the API route (e.g., `users`, `posts`, `contacts`)

## Options
- `--auth` - Require authentication (default: true)
- `--rate-limit <config>` - Rate limit config: `strict`, `standard` (default), `relaxed`
- `--methods <methods>` - HTTP methods to implement (default: GET,POST,PUT,DELETE)
- `--rls` - Generate matching RLS policies
- `--tests` - Generate security tests

## Examples
```bash
# Create standard secure API
create-secure-api users

# Create public API with relaxed rate limits
create-secure-api search --auth=false --rate-limit=relaxed

# Create API with RLS policies and tests
create-secure-api posts --rls --tests

# Create read-only API
create-secure-api reports --methods=GET
```

## What it generates

### API Route (`app/api/[name]/route.ts`)
- Rate limiting middleware
- Input validation with Zod
- Authentication checks
- Error handling
- Security event tracking
- Proper TypeScript types

### RLS Policies (if --rls)
- Matching Supabase policies
- Migration file
- Policy tests

### Tests (if --tests)
- Rate limit tests
- Auth tests
- Input validation tests
- Security header tests

## Security Features Included
- ✅ Rate limiting (configurable)
- ✅ Input validation (Zod schemas)
- ✅ Authentication (optional)
- ✅ CORS headers
- ✅ Security headers (CSP, HSTS, etc.)
- ✅ Error sanitization
- ✅ Audit logging
- ✅ SQL injection prevention

## Post-Creation Steps
1. Update the Zod schema for your data model
2. Configure rate limits if needed
3. Add business logic
4. Run security audit: `security-audit api`
