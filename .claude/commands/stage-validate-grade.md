# Stage Validate Grade - Enhanced with Requirement Enforcement

Grade implementation against original PRD specifications AND locked requirements using Grove's deliberative alignment concept.

## Arguments:
- $FEATURE: Feature name or current
- $OPTIONS: --verbose --export --against-prd --requirements

## Usage:

```bash
/grade                              # Grade current work
/grade --requirements               # Include locked requirements check
/grade ContactForm --requirements   # Grade specific component
/sv grade --feature auth-system     # Original PRD grading
```

## What It Does:

Analyzes implementation and scores alignment with both PRD and locked requirements:
1. **Locked Requirements Compliance** (CRITICAL)
2. Functional requirements completion
3. Test coverage of acceptance criteria  
4. Design system compliance
5. Performance target achievement
6. Security requirement adherence

## Enhanced Grading Process:

### 1. Check Locked Requirements FIRST
```typescript
interface RequirementCompliance {
  component: string;
  source: { type: string; reference: string; };
  compliance: {
    fields: { required: number; found: number; missing: string[]; };
    features: { required: string[]; implemented: string[]; };
    constraints: ConstraintCheck[];
  };
  score: number; // 0-100, must be 100 to proceed
}
```

### 2. Original PRD Grading
(Original functionality preserved)

### 3. Combined Score
```typescript
interface EnhancedGradeReport {
  requirementCompliance: RequirementCompliance;
  prdAlignment: GradeReport;
  overall: number;
  canProceed: boolean; // false if requirements violated
}
```

## Example Output with Requirements:

```
=== REQUIREMENT COMPLIANCE CHECK ===
Component: ContactForm
Source: Issue #42

❌ REQUIREMENT VIOLATIONS DETECTED
   Required: 13 fields
   Found: 7 fields
   Missing: lastName, phone, address, city, state, zip

   Compliance Score: 0% (BLOCKED)

⚠️  Cannot proceed until requirements are met.
   Run: /pin-requirements 42 ContactForm to see full requirements
   Run: /review-requirements ContactForm for detailed report

=== PRD IMPLEMENTATION GRADE: B+ (87%) ===
[Original grading output continues...]

=== OVERALL ASSESSMENT ===
❌ BLOCKED: Locked requirements not met
   - Fix requirement violations first
   - Then re-run grading
```

## Requirement-Aware Confidence Scoring:

When running `/grade --requirements` before implementation:

```
=== PRE-IMPLEMENTATION CONFIDENCE ===

📊 Requirement Analysis for ContactForm

Source Requirements (Issue #42):
- Fields: 13 required
- Features: Corporate email validation, phone formatting
- Constraints: All fields mandatory except company

Current Plan Analysis:
- Planned fields: 7 (❌ Missing 6)
- Planned features: Basic validation only
- Deviation risk: HIGH

Confidence Scores:
- Requirement Clarity: 9/10 ✓
- Implementation Match: 3/10 ❌
- Deviation Risk: 8/10 ⚠️
- Overall Confidence: 3/10

❌ RECOMMENDATION: Do not proceed
   - Review Issue #42 requirements
   - Update implementation plan
   - Ensure all 13 fields included
```

## Integration with Workflow:

### 1. Pre-Implementation Check
```bash
/fw start 42                      # Start from issue
/pin-requirements 42 ContactForm  # Lock requirements
/prd ContactForm                  # Generate PRD
/grade --requirements             # Check BEFORE coding
# If confidence < 8, revise plan
```

### 2. Post-Implementation Validation
```bash
/cc ContactForm                   # Create component
/grade --requirements             # Validate compliance
# If violations, must fix
/test-requirements ContactForm    # Generate tests
/grade                           # Final PRD alignment
```

### 3. Continuous Monitoring
Every 10 commands, system automatically runs requirement validation

## Enhanced Configuration:

```json
// .claude/config.json
{
  "requirement_enforcement": {
    "enabled": true,
    "strict_mode": true,
    "block_on_violation": true,
    "pre_implementation_check": true,
    "min_confidence": 8
  },
  "grove_enhancements": {
    "implementation_grading": {
      "enabled": true,
      "require_compliance_first": true,
      "min_grade": 85,
      "weights": {
        "requirements": 0.0,  // Pass/fail, not weighted
        "functional": 0.4,
        "testing": 0.25,
        "design": 0.15,
        "performance": 0.1,
        "security": 0.1
      }
    }
  }
}
```

## Requirement Compliance Scoring:

- **100%**: All locked requirements met exactly
- **0%**: Any violation = complete failure
- No partial credit for locked requirements

## Enhanced CLI Integration:

```bash
# Quick requirement check
/grade -r

# Full grading with requirements
/grade --all

# Pre-implementation confidence
/grade ContactForm --pre

# Compare with locked requirements
/grade --against-requirements
```

## Benefits of Enhancement:
- **Prevents requirement drift** before it happens
- **Enforces source of truth** from GitHub issues
- **Early detection** of planning errors
- **Objective compliance** metrics
- **Reduced rework** from misaligned implementations

## Workflow Protection:

The enhanced grading system acts as a gatekeeper:
1. **Before coding**: Warns if plan doesn't match requirements
2. **During coding**: Blocks changes that violate requirements
3. **After coding**: Validates full compliance
4. **Before PR**: Final verification

This ensures Claude Code never loses track of what it's supposed to build.
