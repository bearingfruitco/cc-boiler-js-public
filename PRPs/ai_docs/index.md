# AI Documentation Index

## Available Documentation

### Core Patterns
- `nextjs_15_patterns.md` - Next.js 15 server components, actions, routing
- `supabase_patterns.md` - Auth, real-time, RLS, storage patterns  
- `design_system_rules.md` - Enforced typography, spacing, components
- `security_requirements.md` - PII/PHI protection, encryption, compliance

### Development Guides
- `typescript_gotchas.md` - Common TS pitfalls and solutions
- `async_patterns.md` - Event queue, parallel operations, loading states
- `testing_strategies.md` - Unit, integration, E2E test patterns

### Performance
- `optimization_guide.md` - Bundle size, caching, lazy loading
- `database_performance.md` - Query optimization, indexing

## Usage in PRPs

Reference these docs in your PRP's Required Context section:

```yaml
- doc: PRPs/ai_docs/nextjs_15_patterns.md
  why: Using server components and async patterns
  critical: Form actions pattern (section 4)
```

## Keeping Docs Updated

When you discover new patterns or gotchas:
1. Update the relevant AI doc
2. Add examples from actual code
3. Include "gotcha" warnings
4. Run `/doc-index update` to rebuild
