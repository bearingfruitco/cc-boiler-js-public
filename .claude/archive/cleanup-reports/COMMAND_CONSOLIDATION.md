# Command Consolidation Script

This script consolidates duplicate commands and creates proper aliases for Claude Code.

## Issues Found:
1. Multiple versions of smart-resume (3 versions)
2. Multiple versions of other commands (-enhanced, -standards, etc.)
3. Aliases not working in Claude Code

## Solution:
We'll keep the best version of each command and create symlinks for aliases.

## Commands to Consolidate:

### Smart Resume
- smart-resume.md (11.34 KB) - Most comprehensive
- smart-resume-enhanced.md (4.63 KB) - Smaller, likely subset
- smart-resume-standards.md (4.91 KB) - Standards focused

**Decision**: Keep smart-resume.md as primary

### Feature Workflow
- feature-workflow.md (6.51 KB)
- feature-workflow-enhanced.md (5.11 KB)
- feature-workflow-start-enhanced.md (4.52 KB)

**Decision**: Keep feature-workflow.md as primary

### Stage Validate Grade
- stage-validate-grade.md (5.17 KB)
- stage-validate-grade-enhanced.md (5.31 KB)

**Decision**: Keep stage-validate-grade-enhanced.md (newer)

### TDD Workflow
- tdd-workflow.md (3.40 KB)
- tdd-workflow-enhanced.md (7.37 KB)

**Decision**: Keep tdd-workflow-enhanced.md (more complete)

### Init Project
- init-project.md (2.03 KB)
- init-project-enhanced.md (3.86 KB)

**Decision**: Keep init-project-enhanced.md (more features)

### Generate Issues
- generate-issues.md (1.99 KB)
- generate-issues-enhanced.md (4.68 KB)

**Decision**: Keep generate-issues-enhanced.md (more complete)
