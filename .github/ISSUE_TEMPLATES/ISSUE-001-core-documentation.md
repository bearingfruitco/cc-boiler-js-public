---
title: Create Missing Core Documentation
labels: documentation, enhancement, priority:high
assignees: ''
---

## 📋 Description

Create essential missing documentation for core features that are currently undocumented or poorly documented.

## 🎯 Acceptance Criteria

- [ ] Hook System documentation is comprehensive and includes all hook types
- [ ] Command Reference includes all 116+ commands with examples
- [ ] API Guide covers Next.js 15 App Router patterns
- [ ] Testing documentation consolidates all testing approaches

## 📝 Tasks

### 1. Create Hook System Documentation
**File**: `/docs/features/HOOK_SYSTEM.md`

- [ ] Document hook types:
  - Pre-tool-use hooks
  - Post-tool-use hooks  
  - Git pre-commit hooks
- [ ] Explain execution order and priorities
- [ ] Include custom hook examples
- [ ] Document configuration options
- [ ] Add troubleshooting section

### 2. Create Command Reference
**File**: `/docs/features/COMMAND_REFERENCE.md`

- [ ] Audit all commands in `.claude/commands/`
- [ ] Categorize commands:
  - Core Commands (sr, cp, checkpoint)
  - Development Commands (cc, vd, fw)
  - Testing Commands (tr, tdd, btf)
  - Orchestration Commands (orch, spawn, chain)
  - Utility Commands (compress, help, metrics)
- [ ] Document each command with:
  - Purpose and description
  - Syntax and parameters
  - Usage examples
  - Aliases
  - Related commands

### 3. Create API Development Guide
**File**: `/docs/development/API_GUIDE.md`

- [ ] Next.js 15 App Router patterns
- [ ] Route handlers vs API routes
- [ ] Validation with Zod schemas
- [ ] Error handling patterns
- [ ] Rate limiting implementation
- [ ] Authentication/authorization
- [ ] CORS configuration
- [ ] Testing API routes

### 4. Create Comprehensive Testing Guide
**File**: `/docs/testing/README.md`

- [ ] Testing philosophy and strategy
- [ ] Test pyramid approach
- [ ] Unit testing with Vitest
- [ ] Component testing
- [ ] Integration testing
- [ ] E2E testing with Playwright
- [ ] Performance testing
- [ ] Test data management
- [ ] CI/CD integration

## 🔗 Resources

- Current hook implementation: `.claude/hooks/`
- Command files: `.claude/commands/`
- Example API routes in boilerplate
- Existing TDD workflow guide

## ⏱️ Time Estimate

4-6 hours

## 🏷️ Labels

- documentation
- enhancement
- priority: high
