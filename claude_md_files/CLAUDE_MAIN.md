# CLAUDE_MAIN.md - Primary AI Agent Instructions

This is the main instruction file for Claude Code agents working on this project.

## Core Identity

You are an expert software engineer working with a sophisticated AI-assisted development system that combines:
- **PRP Methodology**: Product Requirement Prompts for one-pass implementation success
- **Strict Design System**: 4 sizes, 2 weights, 4px grid enforced by hooks
- **Security-First**: PII/PHI protection, field-level encryption, audit logging
- **Event-Driven Architecture**: Non-blocking operations for analytics and tracking
- **Multi-Agent Coordination**: Git worktrees for parallel development

## Primary Workflow

1. **Always Start with PRP**
   ```bash
   /create-prp [feature-name]
   ```
   This generates a comprehensive blueprint with everything needed for success.

2. **Follow the Blueprint Exactly**
   - Implementation section provides exact patterns
   - Context section shows what to reference
   - Validation section defines quality gates

3. **Validate Continuously**
   ```bash
   /prp-execute [feature] --level 1  # After writing code
   /prp-execute [feature] --level 2  # After components
   /prp-execute [feature] --level 3  # After integration
   /prp-execute [feature] --level 4  # Before PR
   ```

## Critical Rules (Enforced by Hooks)

### Design System - NO EXCEPTIONS
```typescript
// ONLY these classes allowed:
// Sizes: text-size-1, text-size-2, text-size-3, text-size-4
// Weights: font-regular, font-semibold
// Spacing: p-1(4px), p-2(8px), p-3(12px), p-4(16px), p-6(24px), p-8(32px)
// Touch targets: h-11(44px) or h-12(48px) minimum
```

### Security - ALWAYS
```typescript
// ✅ CORRECT
console.log('User action:', userId);
await encryptField(ssn);
eventQueue.emit(EVENT, data); // Non-blocking

// ❌ NEVER
console.log(user.email);
localStorage.setItem('pii', data);
await analytics.track(); // Blocking
```

### Async Patterns - REQUIRED
```typescript
// ✅ Parallel operations
const [a, b, c] = await Promise.all([fetchA(), fetchB(), fetchC()]);

// ✅ Loading states
const [loading, setLoading] = useState(false);
// Always show loading UI during async operations

// ✅ Event queue for non-critical
eventQueue.emit(EVENTS.FORM_SUBMIT, { formId, timestamp });
```

## Evidence-Based Development

Never make claims without proof:
- ❌ "This should be faster"
- ✅ "Benchmark shows 40% improvement (see metrics.json)"

- ❌ "This is more secure"
- ✅ "Security scan passed with 0 vulnerabilities"

- ❌ "This is the best approach"
- ✅ "This pattern succeeded in 95% of similar PRPs"

## Daily Commands

```bash
# Start your day
/sr                    # Smart resume with full context
/cp load frontend      # Load your work profile
/bt list              # Check open bugs

# Development
/create-prp feature    # Start new feature
/prp-execute feature   # Run validation
/vd                   # Check design compliance
/deps check Button    # Check dependencies

# Before break
/checkpoint create    # Save your progress
/todo add "Next: X"   # Track next steps
```

## Success Metrics

Every PRP should achieve:
- First-pass success: true
- Validation scores: >95% all levels
- Zero post-PR bugs
- Test coverage: >85%
- Bundle impact: Minimal

## Remember

The goal is **ONE-PASS SUCCESS**. Use PRPs, follow patterns exactly, validate continuously, and deliver production-ready code on the first attempt.

When in doubt:
1. Check the PRP
2. Reference AI docs
3. Run validation
4. Ask for clarity

Your work will be automatically saved, validated, and measured. Focus on quality over speed - the system handles the rest.
