# Enhanced PRD with PRP Validation Loops

This template combines your existing PRD structure with PRP's validation loop methodology.
It maintains all your existing features while adding one-pass implementation success.

## 1. Feature Overview
- What is this feature?
- Why are we building it?
- Who will use it?

## 2. Goal & Success Criteria
### Goal
[One sentence: What must be achieved]

### Success Criteria (Checkboxes for tracking)
- [ ] [Specific, measurable criterion]
- [ ] [Another measurable criterion]
- [ ] [Performance metric: e.g., loads < 3s]
- [ ] [Business metric: e.g., 20% conversion]

## 3. User Stories
Generate 3-5 user stories in format:
"As a [type of user], I want to [action] so that [benefit]"

## 4. Functional Requirements
### Must Have (MVP)
- Feature 1: [description]
- Feature 2: [description]

### Nice to Have
- Enhancement 1: [description]

### Out of Scope (v1)
- Future feature: [description]

## 5. UI/UX Requirements
- Key screens/components needed
- User flow description
- Mobile considerations (min 44px touch targets)
- Design system compliance (text-size-[1-4], font-regular/semibold)

## 6. Technical Requirements
### Architecture
- API endpoints needed
- Database changes
- Performance requirements
- Security considerations

### Async Requirements (if applicable)
Run `/prd-async $FEATURE` after creating this PRD

## 7. All Needed Context (PRP Enhancement)
### Documentation & References
```yaml
# Format: Include specific reasons why each resource is needed
- url: https://nextjs.org/docs/app/building-your-application/data-fetching
  why: Using server components for initial data load
  critical: Parallel data fetching pattern in section 3.2

- file: components/forms/ContactForm.tsx
  why: Follow same validation pattern and error handling
  gotcha: Note the async validation on line 127

- doc: https://supabase.com/docs/guides/auth/row-level-security
  section: "Policies with security definer functions"
  why: Need to implement user-scoped data access

- pattern: lib/api/client.ts
  why: Standard error handling and retry logic
```

### Known Gotchas & Critical Warnings
```markdown
# CRITICAL: Always validate on server before database operations
# CRITICAL: PII fields must use field-registry encryption
# CRITICAL: All async operations need loading states
# WARNING: This API has 100 req/min rate limit
# NOTE: Mobile Safari requires special handling for [specific feature]
```

### Code Patterns to Follow
```typescript
// Standard form pattern from our system
const form = useForm<FormData>({
  resolver: zodResolver(schema),
  defaultValues: { /* ... */ }
});

// Event tracking pattern (non-blocking)
eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, data);
```

## 8. Implementation Blueprint (Step-by-Step)
### Phase 1: Foundation
1. Create database schema
   ```sql
   -- Migrations go here
   ```
2. Set up API routes following our pattern
3. Implement core business logic with tests

### Phase 2: UI Implementation
1. Create components using design system
2. Implement forms with validation
3. Add loading states for all async ops
4. Mobile responsive implementation

### Phase 3: Integration & Polish
1. Connect frontend to API
2. Add error boundaries
3. Implement analytics events
4. Performance optimization

## 9. Validation Loops (PRP Core Feature)

### 🔴 Level 1: Syntax & Standards (Run continuously)
```bash
# Runs automatically, but can be triggered manually
bun run lint:fix           # Fix style issues
bun run typecheck          # TypeScript validation
bun run validate-design    # Design system check
```
**Must Pass Before**: Writing any component code

### 🟡 Level 2: Component Testing (After each component)
```bash
# Unit tests for individual components
bun run test $FEATURE.test.ts

# Specific validation commands
bun run test:components    # Component tests only
bun run test:hooks        # Custom hooks
```
**Must Pass Before**: Integration work

### 🟢 Level 3: Integration Testing (After integration)
```bash
# API integration tests
bun run test:api $FEATURE

# Full feature flow
bun run test:e2e $FEATURE

# Accessibility audit
bun run test:a11y
```
**Must Pass Before**: Stage completion

### 🔵 Level 4: Production Validation (Before PR)
```bash
# Performance check
bun run lighthouse $FEATURE_URL

# Security audit
bun run security:check

# Bundle size check
bun run analyze

# Full validation suite
/sv check 3
/grade --requirements
```
**Must Pass Before**: Creating PR

### Validation Automation
```yaml
# These run automatically via hooks:
- Design system validation (pre-commit)
- Type checking (pre-commit)
- Test relevant files (pre-push)
- Requirements compliance (/pin-requirements)
```

## 10. Error Handling & Edge Cases
### Edge Cases
- Network timeout during submission
- Concurrent user modifications
- Invalid data from external API
- Rate limit exceeded

### Error Recovery
```typescript
// Standard error handling pattern
try {
  await apiCall();
} catch (error) {
  if (error instanceof ApiError) {
    // Specific handling
  } else {
    // Generic fallback
  }
}
```

## 11. Testing Strategy
### Test Generation
After PRD approval, run:
```bash
/prd-tests $FEATURE              # Generate test suite
/test-requirements $ISSUE_NUMBER  # Generate from requirements
```

### Test Coverage Requirements
- Unit tests: 80% coverage minimum
- Integration tests: All API endpoints
- E2E tests: Critical user paths
- Performance tests: Must meet SLAs

## 12. Documentation Requirements
### Code Documentation
- JSDoc for all public APIs
- README for complex features
- Architecture decisions in ADRs

### User Documentation
- Feature announcement
- Help documentation
- API documentation (if applicable)

## 13. Rollout Strategy
### Feature Flags
```typescript
if (flags.isEnabled('$FEATURE')) {
  // New implementation
}
```

### Monitoring
- Error rate monitoring
- Performance metrics
- User engagement analytics
- Business metrics tracking

## 14. Implementation Checklist
### Pre-Development
- [ ] PRD reviewed and approved
- [ ] `/pin-requirements $ISSUE $FEATURE` run
- [ ] `/prd-async $FEATURE` completed (if needed)
- [ ] `/prd-tests $FEATURE` generated
- [ ] Technical design reviewed

### During Development  
- [ ] Level 1 validation passing
- [ ] Level 2 validation passing
- [ ] Stage 1 complete (`/sv check 1`)
- [ ] Stage 2 complete (`/sv check 2`)
- [ ] All tests passing

### Pre-Deployment
- [ ] Level 3 validation passing
- [ ] Level 4 validation passing
- [ ] `/grade --requirements` > 85%
- [ ] Security review complete
- [ ] Documentation complete

## 15. Success Metrics & Monitoring
### Technical Metrics
- Page load time < 3s
- API response time < 500ms (p95)
- Error rate < 0.1%
- Test coverage > 80%

### Business Metrics
- [Feature-specific metric]
- [User engagement metric]
- [Conversion metric]

### Tracking Implementation
```typescript
// Event tracking for metrics
eventQueue.emit('feature.used', {
  feature: '$FEATURE',
  action: 'complete',
  value: measuredValue
});
```

---

## Quick Validation Commands

```bash
# During development
/vd                    # Validate design
/validate-async        # Check async patterns
/exists Component      # Before creating

# Testing
/prd-tests generate    # Create tests from PRD
/btf                   # Browser test flow
/test-requirements     # Test against requirements

# Completion
/sv check             # Validate current stage
/grade                # Check PRD alignment
/fw complete          # Create PR with context
```

## Notes
- This PRD will be validated against pinned requirements if set
- All code must pass design system validation
- Tests will be auto-generated from success criteria
- Validation loops ensure first-pass success
