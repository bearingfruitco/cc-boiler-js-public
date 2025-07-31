# Command Combinations

> Powerful command sequences and combinations for maximum productivity

## 📚 Quick Reference

### Most Used Combinations
- [`/sr && /fw status`](#daily-startup) - Start your day
- [`/cc Button && /vd && /tr`](#component-development) - Create validated component
- [`/create-prp feature && /prp-execute`](#prp-workflow) - One-pass implementation
- [`/bug-track && /btf && /fix`](#bug-fixing) - Debug workflow
- [`/checkpoint create && /fw complete`](#feature-completion) - Finish feature

---

## 🌅 Daily Workflows

### Daily Startup
```bash
# Smart resume with status check
/sr && /fw status && /bt list --open

# Full morning routine
/chain morning-setup
# Runs:
# - Smart resume
# - Dependency check
# - Test status
# - Security scan
# - Open issues review
```

### Context Switch
```bash
# Save current work
/checkpoint create feature-a && /cp save

# Switch to different feature
/cp load feature-b && /sr

# Return later
/cp load feature-a && /checkpoint restore feature-a
```

### End of Day
```bash
# Complete checkpoint
/checkpoint create eod && /fw status && /todo

# With handoff notes
/checkpoint create eod --message="Completed API, UI tomorrow"
```

---

## 🏗️ Component Development

### Basic Component Creation
```bash
# Create, validate, test
/cc Button && /vd && /tr

# With documentation
/cc Button && /vd && /tr && /doc-component Button
```

### Complex Component with PRP
```bash
# Plan first
/create-prp data-table-component

# Execute with validation
/prp-execute data-table --level 1 && \
/cc DataTable --from-prp && \
/prp-execute data-table --level 2

# Full validation
/prp-execute data-table --all-levels
```

### Form Component Workflow
```bash
# Secure form creation
/ctf UserRegistration --compliance=gdpr && \
/afs components/forms/UserRegistration.tsx && \
/tr UserRegistration.test.tsx

# Add to page
/cc pages/register --use=UserRegistration
```

---

## 🔄 PRP Workflows

### Standard PRP Flow
```bash
# Create and execute
/create-prp payment-integration && \
/prp-execute payment-integration --level 1

# Progressive implementation
/prp-execute payment --level 1 && /cc PaymentSchema
/prp-execute payment --level 2 && /cc PaymentAPI  
/prp-execute payment --level 3 && /cc PaymentForm
/prp-execute payment --level 4 && /fw complete
```

### PRP with Orchestration
```bash
# Let agents handle it
/create-prp user-management && \
/orch implement user-management from PRP

# Verify results
/prp-execute user-management --verify-all
```

---

## 🐛 Debugging Workflows

### Visual Debug Flow
```bash
# Capture and analyze
# 1. Take screenshot
# 2. Ctrl+V in Claude Code
# 3. "Fix the alignment issue"

# Then verify
/btf && /pw-screenshot
```

### Systematic Debug
```bash
# Track, reproduce, fix
/bug-track "Login fails on mobile" && \
/btf login --device=mobile && \
/pw-debug && \
/fix-bug mobile-login

# Verify fix
/pw-test login --device=mobile && \
/create-test login-mobile-regression
```

### Performance Debug
```bash
# Baseline, analyze, optimize
/performance-baseline && \
/chain performance-optimization-v4 && \
/performance-compare baseline

# Verify improvements
/lighthouse && /bundle-analyze
```

---

## 🧪 Testing Workflows

### TDD Flow
```bash
# Test first, implement, refactor
/tdd Calculator && \
/tr Calculator.test.tsx && \
/cc Calculator --minimal && \
/tr Calculator.test.tsx && \
/refactor Calculator

# Add edge cases
/enhance-tests Calculator && /tr
```

### Integration Testing
```bash
# Component + API + Database
/test-integration checkout-flow && \
/btf checkout && \
/pw-test checkout.spec.ts

# With coverage
/test --coverage && /coverage-report
```

### Visual Testing
```bash
# Capture baselines
/pw-baseline capture all && \
# ... make changes ... && \
/pw-baseline compare && \
/pw-baseline accept
```

---

## 🚀 Deployment Workflows

### Pre-Deployment Check
```bash
# Full validation
/chain pre-deployment && \
/security-scan && \
/lighthouse && \
/test --all

# Environment check
/env-validate production && \
/deps check --production
```

### Staging Deploy
```bash
# Deploy and test
/deploy staging && \
/smoke-test staging && \
/pw-test --env=staging

# Monitor
/monitor staging --duration=30m
```

---

## 🎭 Multi-Agent Workflows

### Complex Feature
```bash
# Orchestrate specialists
/orch implement real-time chat feature && \
/deps check --new && \
/test-integration chat

# Parallel development
(/spawn frontend & /spawn backend) && \
/wait && /merge-work
```

### Architecture Planning
```bash
# Multi-perspective design
/chain architecture-design && \
/visualize-architecture && \
/validate-architecture

# Generate implementation
/architecture-to-prps && \
/prp-status --all
```

---

## 📊 Analysis Workflows

### Codebase Analysis
```bash
# Full analysis
/analyze-existing full && \
/deps scan && \
/metrics report

# Specific analysis
/analyze components --unused && \
/analyze api --performance
```

### Dependency Analysis
```bash
# Check before changes
/deps check Button && \
/cc Button --safe && \
/deps verify Button

# Circular dependency check
/deps scan --circular && \
/deps visualize
```

---

## 🔒 Security Workflows

### Security Audit
```bash
# Full security check
/security-scan && \
/audit-forms --all && \
/check-pii-exposure

# Fix issues
/security-fix --auto && \
/security-scan --verify
```

### Compliance Check
```bash
# GDPR compliance
/gdpr-check && \
/audit-data-retention && \
/generate-privacy-policy

# TCPA compliance
/tcpa-check forms && \
/audit-consent-collection
```

---

## ⚡ Performance Workflows

### Optimization Flow
```bash
# Analyze, optimize, verify
/bundle-analyze && \
/optimize-bundle && \
/lighthouse compare

# Component optimization
/analyze Button --performance && \
/optimize-component Button && \
/performance-test Button
```

### Load Testing
```bash
# Baseline, test, analyze
/performance-baseline prod && \
/load-test --users=1000 && \
/performance-report

# Fix bottlenecks
/analyze-slow-queries && \
/optimize-database
```

---

## 🎨 Design System Workflows

### Migration Flow
```bash
# Analyze violations
/migrate-to-strict-design analyze && \
/vd --report

# Fix with backup
/migrate-to-strict-design migrate && \
/vd --verify

# Rollback if needed
/migrate-rollback design
```

### Component Library
```bash
# Build library
/chain component-library && \
/generate-component-docs && \
/storybook build

# Publish
/publish-components --version=patch
```

---

## 💡 Advanced Combinations

### Conditional Chains
```bash
# If tests pass, deploy
/test --all && /deploy staging || /debug failed-tests

# Progressive deployment
/test && /deploy staging && /smoke-test && /deploy production
```

### Parallel Execution
```bash
# Run multiple validations
(/vd & /test & /lint & /typecheck) && echo "All validations passed"

# Parallel feature work
(/cc Header & /cc Footer & /cc Sidebar) && /cc Layout --compose
```

### Loop Workflows
```bash
# Process multiple PRPs
for prp in $(ls PRPs/active/*.md); do
  /prp-execute $(basename $prp .md) --level 1
done

# Bulk component updates
for comp in Button Card Modal; do
  /cc $comp --update && /vd && /tr
done
```

---

## 🏆 Power User Tips

### Command Aliases in Chains
```bash
# Short and sweet
/sr && /fw s && /bt l -o && /vd

# Equals
/smart-resume && /feature-workflow status && /bug-track list --open && /validate-design
```

### Custom Chains
Add to `.claude/config/chains.json`:
```json
{
  "my-daily": {
    "description": "My custom daily workflow",
    "commands": [
      "/sr",
      "/fw status",
      "/bt list --open",
      "/test changed",
      "/coffee make ☕"
    ]
  }
}
```

### Pipe Results
```bash
# Use output from one command
/analyze components --unused | /cc --remove

# Chain with processing
/deps check Button | grep "Used by" | wc -l
```

---

## 📚 Command Categories

### Essential Daily
- `/sr` - Smart Resume
- `/fw` - Feature Workflow  
- `/bt` - Bug Tracking
- `/checkpoint` - Save Progress

### Development
- `/cc` - Create Component
- `/create-prp` - Create PRP
- `/prp-execute` - Execute PRP
- `/vd` - Validate Design

### Testing
- `/tr` - Test Runner
- `/tdd` - Test-Driven Dev
- `/btf` - Browser Test Flow
- `/test` - Run All Tests

### Analysis
- `/deps` - Dependencies
- `/analyze` - Code Analysis
- `/metrics` - Metrics Report
- `/performance` - Performance

### Multi-Agent
- `/orch` - Orchestrate
- `/spawn` - Spawn Agent
- `/chain` - Run Chain
- `/merge-work` - Merge Results

---

**Remember**: Commands are composable! Start simple, then combine for powerful workflows. The system tracks everything, so experiment freely!
