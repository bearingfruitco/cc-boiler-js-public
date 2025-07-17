# PRP: User Profile Management - Example Implementation

> **Example PRP showing complete implementation pattern**
> Reference this for creating new PRPs

## 🎯 Goal

Implement a complete user profile management system with:
- Profile viewing and editing
- Avatar upload
- Settings management
- Real-time updates

## ✅ Success Criteria

- [ ] Users can view their profile
- [ ] Users can edit profile fields
- [ ] Avatar upload with optimization
- [ ] Changes reflected in real-time
- [ ] Mobile-responsive design
- [ ] Accessibility compliant (WCAG 2.1 AA)
- [ ] Performance: < 2s load time
- [ ] Security: All PII encrypted

## 📚 Required Context

### Design System References
```yaml
- doc: PRPs/ai_docs/design_system_rules.md
  why: Building UI components
  critical: Card and form patterns

- doc: PRPs/ai_docs/supabase_patterns.md
  why: Database operations and real-time
  critical: RLS policies for profiles
  
- doc: PRPs/ai_docs/security_requirements.md
  why: Handling PII (email, phone)
  critical: Field encryption patterns
```

### Codebase Patterns
```yaml
- file: components/forms/ContactForm.tsx
  pattern: Form validation with react-hook-form
  lines: 45-89

- file: components/ui/Button.tsx
  pattern: Loading states and disabled handling
  
- file: lib/supabase/client.ts
  pattern: Supabase client setup
```

### Known Gotchas
1. **Avatar upload**: Must validate file type and size client-side
2. **Real-time**: Need to unsubscribe on component unmount
3. **Hydration**: Use useEffect for client-only values

## 🏗️ Implementation Blueprint

[Full implementation details would follow...]

## 🧪 Validation Loops

### Level 1: Syntax & Standards ✓
```bash
bun run lint
bun run typecheck
/vd
```

### Level 2: Component Testing ✓
```bash
bun test Profile.test.tsx
bun test AvatarUpload.test.tsx
```

### Level 3: Integration Testing ✓
```bash
bun test:e2e profile
```

### Level 4: Production Readiness ✓
```bash
/security-scan
/bundle-analyze
/pp
```

## 📊 Success Metrics
```yaml
first_pass_success: true
validation_scores:
  syntax: 100%
  components: 98%
  integration: 95%
  production: 100%
time_to_complete: "3h 15m"
bugs_found_after: 0
test_coverage: 89%
bundle_impact: +12.4kb
```

---
**Status**: Completed ✅
**Lessons Learned**: Real-time subscriptions need careful cleanup
