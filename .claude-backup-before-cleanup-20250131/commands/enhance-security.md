# enhance-security

Adds security features to existing code without breaking functionality.

## Usage
```bash
enhance-security <target> [options]
```

## Arguments
- `target` - What to enhance: `api`, `form`, `all`, or specific file path

## Options
- `--level` - Security level: `basic`, `standard` (default), `strict`
- `--fix` - Automatically apply fixes (default: false)
- `--spawn` - Use security-enhancer sub-agent for deep analysis

## Examples
```bash
# Enhance security of all APIs
enhance-security api

# Add security to specific file
enhance-security app/api/users/route.ts

# Auto-fix with strict security
enhance-security all --level=strict --fix

# Use sub-agent for enhancement
enhance-security form --spawn
```

## What it does

### For APIs
- Adds rate limiting middleware
- Generates Zod validation schemas
- Adds authentication checks
- Implements proper error handling
- Adds security headers

### For Forms
- Adds input validation
- Integrates CAPTCHA
- Implements rate limiting
- Adds honeypot fields
- Ensures CSRF protection

### For Database
- Suggests RLS policies
- Adds parameterized queries
- Implements soft deletes
- Adds audit trails

## Enhancement Levels

### Basic
- Input validation
- Basic rate limiting
- Error sanitization

### Standard (Default)
- Everything in Basic
- Authentication checks
- CAPTCHA for public forms
- Security headers
- Event tracking

### Strict
- Everything in Standard
- Aggressive rate limiting
- IP-based blocking
- Advanced validation
- Audit logging

## Example Enhancements

### Before (Insecure API)
```typescript
export async function POST(req: Request) {
  const data = await req.json();
  const result = await db.insert(users).values(data);
  return Response.json(result);
}
```

### After (Enhanced)
```typescript
import { rateLimit, validateInput } from '@/lib/security/middleware';
import { userSchema } from './schema';

export const POST = rateLimit({ window: '1m', max: 10 })(
  validateInput(userSchema)(
    async (req: Request) => {
      const data = req.validated;
      const result = await db.insert(users).values(data);
      return Response.json({ success: true, id: result.id });
    }
  )
);
```

## Sub-Agent Mode
When using `--spawn`, the security-enhancer sub-agent will:
1. Analyze code structure
2. Identify security gaps
3. Apply appropriate patterns
4. Generate tests
5. Validate changes

## Integration
- Works with existing code
- Preserves functionality
- Follows design system
- Generates tests
- Updates documentation
