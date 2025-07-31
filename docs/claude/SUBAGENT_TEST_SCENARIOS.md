# Sub-Agent Test Scenarios

## 🧪 Testing Guide for Each Agent

### 1. Frontend UX Specialist (`fe`)
**Test Scenario**: Create a responsive user profile card
```bash
fe create a responsive user profile card with avatar, name, bio, and social links following our design system

# Expected: Component using text-size-[1-4], 4px grid spacing, proper mobile sizing
```

### 2. Backend Reliability Engineer (`be`)
**Test Scenario**: Create a secure API endpoint
```bash
be create a POST /api/users endpoint with validation, error handling, and rate limiting

# Expected: Robust API with try-catch, validation, proper status codes
```

### 3. QA Test Engineer (`qa`)
**Test Scenario**: Generate tests for authentication
```bash
qa create comprehensive test suite for user authentication including unit, integration, and e2e tests

# Expected: Test files with multiple test cases, edge cases, error scenarios
```

### 4. Security Threat Analyst (`sec`)
**Test Scenario**: Audit authentication system
```bash
sec perform security audit on authentication system checking for OWASP vulnerabilities

# Expected: Detailed security report with findings and recommendations
```

### 5. TDD Engineer (`tdd`)
**Test Scenario**: Implement feature with TDD
```bash
tdd implement password reset feature using test-driven development

# Expected: Tests written first (red), then implementation (green), then refactor
```

### 6. Code Reviewer (`cr`)
**Test Scenario**: Review recent changes
```bash
cr review the authentication implementation for best practices and security

# Expected: Detailed review with strengths, issues, and suggestions
```

### 7. Documentation Writer (`doc`)
**Test Scenario**: Document API endpoints
```bash
doc create comprehensive API documentation for the user management endpoints

# Expected: Clear docs with examples, request/response formats, error codes
```

### 8. PM Orchestrator (`pm`)
**Test Scenario**: Coordinate feature development
```bash
pm orchestrate development of user profile feature with edit capabilities

# Expected: Coordination plan using multiple agents in logical sequence
```

### 9. Systems Architect (`arch`)
**Test Scenario**: Design system architecture
```bash
arch design architecture for real-time notification system

# Expected: Technical design with diagrams, technology choices, ADRs
```

### 10. Database Architect (`db`)
**Test Scenario**: Design database schema
```bash
db design schema for user profiles with posts and comments

# Expected: Optimized schema with relationships, indexes, constraints
```

### 11. Performance Optimizer (`perf`)
**Test Scenario**: Optimize slow component
```bash
perf analyze and optimize the dashboard component that's rendering slowly

# Expected: Performance analysis with specific optimization recommendations
```

### 12. Migration Specialist (`migrate`)
**Test Scenario**: Plan database migration
```bash
migrate create migration plan for adding user roles and permissions

# Expected: Migration scripts with rollback procedures
```

### 13. Refactoring Expert (`refactor`)
**Test Scenario**: Refactor legacy code
```bash
refactor improve the user service module to follow SOLID principles

# Expected: Refactoring plan with step-by-step improvements
```

### 14. Form Builder Specialist (`form`)
**Test Scenario**: Create dynamic form
```bash
form create a multi-step registration form with validation and progress tracking

# Expected: Advanced form with validation, state management, UX features
```

### 15. PII Guardian (`pii`)
**Test Scenario**: Scan for PII exposure
```bash
pii scan codebase for exposed personal information and suggest remediation

# Expected: PII audit report with compliance recommendations
```

## 🔄 Workflow Chain Tests

### Security Audit Chain
```bash
chain security-audit-chain

# Expected: 
# 1. Security analysis by security-threat-analyst
# 2. Code path tracing by code-analyzer-debugger
# 3. API fixes by backend-reliability-engineer
# 4. Documentation by documentation-writer
```

### Feature Development Chain
```bash
chain feature-development-chain

# Expected:
# 1. Planning phase with PM, architect, QA
# 2. Implementation with TDD, frontend, backend
# 3. Review with code-reviewer, security, performance
```

## 🎯 Integration Tests

### Test 1: File Context Suggestions
1. Create a file: `components/UserCard.tsx`
2. Edit the file
3. **Expected**: System suggests `fe` (frontend-ux-specialist)

### Test 2: Security File Detection
1. Create a file: `api/auth/login.ts`
2. Edit the file
3. **Expected**: System suggests `sec` (security-threat-analyst)

### Test 3: Workflow Transition
1. Use: `qa create tests for checkout`
2. Complete the agent task
3. **Expected**: System suggests `tdd` for implementation

### Test 4: Alias Usage
```bash
# Test each primary alias
fe build navbar
be create user API
qa test checkout
sec audit auth
tdd implement search
cr review changes
doc update README
pm coordinate feature
```

## ✅ Success Criteria

Each agent should:
1. Understand its domain expertise
2. Follow system conventions
3. Produce high-quality output
4. Integrate with other agents
5. Respect design system rules

## 📋 Test Results Template

```markdown
## Agent Test Results

### Agent: [Name]
- **Test**: [Scenario]
- **Command**: [Exact command used]
- **Result**: ✅ PASS / ❌ FAIL
- **Output Quality**: ⭐⭐⭐⭐⭐
- **Notes**: [Any observations]

### Integration
- **File Suggestions**: ✅ Working
- **Workflow Transitions**: ✅ Working
- **Alias Commands**: ✅ Working
- **Chain Execution**: ✅ Working
```

## 🚀 Quick Test Script

```bash
# Run this to test all agents quickly
echo "Testing all agents..."

# Test primary agents
fe create test component
be create test endpoint
qa create test suite
sec perform quick audit
tdd implement test feature
cr review test code
doc create test docs
pm orchestrate test workflow

echo "✅ Basic agent tests complete"
```
