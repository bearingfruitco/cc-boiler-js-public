# Create PRP (Product Requirement Prompt)

Generate a comprehensive PRP that ensures one-pass implementation success.

## Arguments: $ARGUMENTS

## What This Does:

Creates a Product Requirement Prompt (PRP) which is:
- PRD + Curated Codebase Intelligence + Validation Loops
- Everything needed for production-ready code on first attempt
- Integrated with your existing requirement enforcement system

## Process:

1. **Analyze Request**
   - Understand the feature/component to build
   - Identify similar patterns in codebase
   - Check for existing implementations

2. **Gather Context**
   - Find relevant code examples
   - Identify design patterns to follow
   - Collect known gotchas and warnings

3. **Create PRP Structure**
   - Clear goal and success criteria
   - All needed documentation references
   - Step-by-step implementation blueprint
   - Multi-level validation loops

4. **Integration Points**
   - Links to pinned requirements if applicable
   - Connects to existing PRDs
   - References team patterns and decisions

## Template Selection:

Based on the request, I'll choose the appropriate template:
- **prp_base.md** - General features with full validation
- **prp_typescript.md** - React/TypeScript components
- **prp_enhanced.md** - Complex features with stage gates

## Generated PRP Will Include:

### 1. Goal & Success Criteria
- Clear, measurable objectives
- Checkboxes for tracking progress
- Performance and quality metrics

### 2. Context Section
```yaml
- url: [documentation link]
  why: [specific reason needed]
  critical: [key section or warning]
  
- file: [codebase example]
  pattern: [what to follow]
  gotcha: [what to avoid]
```

### 3. Implementation Blueprint
- Phase-by-phase approach
- Exact code patterns to follow
- Design system compliance built-in

### 4. Validation Loops
- Level 1: Syntax & Standards (continuous)
- Level 2: Component Testing (after each part)
- Level 3: Integration Testing (after connecting)
- Level 4: Production Readiness (before PR)

### 5. Integration with Your System
- Uses your design system rules
- Incorporates pinned requirements
- Leverages existing patterns
- Connects to bug tracking

## Example Usage:

```bash
/create-prp user authentication with JWT
/create-prp responsive data table component
/create-prp checkout flow with Stripe
```

## After Creation:

1. Review and adjust the PRP if needed
2. Run `/prp-validate` to check completeness
3. Use `/prp-execute` to run validation loops
4. Begin implementation following the blueprint

## Benefits:

- **One-Pass Success**: Everything needed upfront
- **Prevents Violations**: Design system rules embedded
- **Reduces Bugs**: Known gotchas documented
- **Faster Development**: No searching for patterns
- **Quality Assured**: Validation at every step

## Output Location:

The PRP will be saved to:
- `PRPs/[feature-name].md` - Active PRP
- Linked to any related GitHub issues
- Referenced in your context management

## Tips:

1. **Be Specific**: "user auth" → "JWT auth with refresh tokens"
2. **Include Context**: Mention similar features to reference
3. **State Constraints**: Note performance requirements
4. **Identify Complexity**: Mention if async operations involved

The PRP ensures you have everything needed before writing a single line of code!