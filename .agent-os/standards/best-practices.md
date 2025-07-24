# Development Best Practices

## Core Principles

### 1. TDD (Test-Driven Development)
- **Always** write tests before implementation
- Red → Green → Refactor cycle
- Tests document expected behavior
- Use `/tdd-workflow` command to enforce

### 2. "Actually Works" Protocol
- Never claim completion without verification
- Run tests before marking tasks complete
- Use `/verify` command to validate claims
- Evidence-based development

### 3. Specification-First Development
- PRDs drive all development
- PRPs provide implementation context
- Grade implementation against specs
- Use `/grade` to measure alignment

## Code Organization

### File Structure
```
components/
  ui/        - Reusable UI components
  forms/     - Form-specific components
  layout/    - Layout components
  features/  - Feature-specific components
lib/
  api/       - API client and utilities
  db/        - Database queries and schemas
  events/    - Event system
  utils/     - Helper functions
hooks/       - Custom React hooks
types/       - TypeScript type definitions
```

### Import Order
1. React/Next.js imports
2. Third-party libraries
3. Absolute imports from @/
4. Relative imports
5. Types

### Component Patterns
- Functional components only (no classes)
- Props interfaces for all components
- Composition over inheritance
- Co-locate related files

## Async Development

### Event-Driven Architecture
```typescript
// Critical path - await required
await api.submitForm(data);

// Non-critical - fire and forget
eventQueue.emit(LEAD_EVENTS.PIXEL_FIRE, data);
```

### Required Patterns
- Loading states for ALL async operations
- Error boundaries for graceful failures
- Timeout protection (5s default)
- Retry logic for network operations

### Parallel Operations
```typescript
// ✅ Good - parallel execution
const [user, prefs, perms] = await Promise.all([
  fetchUser(),
  fetchPreferences(),
  fetchPermissions()
]);

// ❌ Bad - sequential awaits
const user = await fetchUser();
const prefs = await fetchPreferences();
const perms = await fetchPermissions();
```

## Error Handling

### API Errors
```typescript
try {
  const data = await apiClient('/endpoint');
} catch (error) {
  if (error instanceof ApiError) {
    setError(error.message);
  } else {
    setError('Something went wrong');
  }
}
```

### Form Validation
- Client-side validation with Zod
- Display field-level errors
- Prevent submission with invalid data
- Clear error messages

## Git Workflow

### Branch Strategy
- `main` - production ready
- `feat/*` - new features
- `fix/*` - bug fixes
- `chore/*` - maintenance

### Commit Messages
Follow Conventional Commits:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `style:` formatting
- `refactor:` code restructuring
- `test:` test changes
- `chore:` maintenance

### Pre-Commit Checks
Automated via Husky:
1. Design system validation
2. TypeScript checking
3. Test execution
4. Linting

## Security Practices

### PII Protection
- Never log sensitive data
- Use field-level encryption
- Implement audit trails
- Follow TCPA compliance

### API Security
- Validate all inputs
- Use parameterized queries
- Implement rate limiting
- Sanitize outputs

### Authentication
- Use Supabase Auth (when needed)
- Secure session management
- Implement proper RBAC
- No hardcoded credentials

## Performance Guidelines

### Loading Performance
- Lazy load components
- Optimize images with Next.js
- Use React Server Components
- Implement code splitting

### Runtime Performance
- Memoize expensive operations
- Use React.memo sparingly
- Optimize re-renders
- Profile with React DevTools

## Documentation

### Code Comments
- Explain WHY, not WHAT
- Document complex logic
- Use TSDoc for functions
- Keep comments updated

### Component Documentation
```typescript
/**
 * Button component with loading state
 * @param loading - Shows spinner when true
 * @param variant - Visual style variant
 */
```

### README Files
- Feature-level documentation
- Setup instructions
- API documentation
- Troubleshooting guides

## Team Collaboration

### Code Reviews
- Check design system compliance
- Verify test coverage
- Ensure error handling
- Review performance impact

### Knowledge Sharing
- Document patterns in specs/
- Update best practices regularly
- Share learnings in team meetings
- Maintain decision logs

## Continuous Improvement

### Pattern Extraction
- Use `/specs extract` for successful patterns
- Document in pattern library
- Share across team
- Reuse in future PRPs

### Metrics Tracking
- Implementation grading scores
- Bug frequency by component
- Performance metrics
- User feedback

### Regular Reviews
- Weekly pattern reviews
- Monthly best practice updates
- Quarterly architecture reviews
- Annual tech debt assessment
