# Claude Code Boilerplate Features

> Comprehensive guide to all features in v4.0.0

## 🎯 Core Features

### 1. 31-Agent System
Specialized AI agents for every aspect of development:
- **Technology Specialists**: supabase, playwright, analytics, platform deployment
- **Core Development**: frontend, backend, security, QA, performance
- **Architecture & Planning**: system architect, database architect, PM orchestrator
- **Documentation**: mentor, documentation writer, report generator

[Learn more →](./AGENT_SYSTEM.md)

### 2. Product Requirement Prompts (PRPs)
One-pass implementation system combining:
- Product requirements
- Codebase intelligence
- Validation loops
- AI-optimized documentation

[Learn more →](./PRP_SYSTEM.md)

### 3. Smart Command System (116+ Commands)
Streamlined workflows with intelligent aliases:
- Context management: `/sr`, `/cp`, `/checkpoint`
- Development: `/cc`, `/vd`, `/fw`
- Testing: `/tdd`, `/btf`, `/tr`
- Orchestration: `/orch`, `/spawn`, `/chain`

### 4. Design System Enforcement
Strict 4-size, 2-weight system:
- Font sizes: ONLY text-size-[1-4]
- Font weights: ONLY font-regular, font-semibold
- Spacing: ONLY 4px grid
- Enforced by hooks at write-time and commit-time

### 5. Hook System
Three-layer automated enforcement:
- **Pre-tool-use**: Design, security, dependencies
- **Post-tool-use**: State saving, metrics, suggestions
- **Git pre-commit**: Final validation before commits

### 6. Chain Automation
Intelligent workflows with:
- Auto-triggers based on conditions
- Prerequisite checking
- Context passing between steps
- Parallel execution
- Success/failure handlers

### 7. Next Command Suggestions
Context-aware workflow guidance:
- Analyzes results and suggests next steps
- Time-based hints (morning, end-of-day)
- Orchestration detection
- Learning from patterns

[Learn more →](./NEXT_COMMAND_SUGGESTIONS.md)

### 8. Visual Debugging
Native Claude Code integration:
- `Ctrl+V` for screenshot analysis
- `/vp` for complex visual planning
- Non-interactive mode for CI/CD
- Multi-directory support

### 9. Async Event System
Fire-and-forget architecture:
- Event queue implementation
- Parallel operation detection
- Loading state requirements
- Timeout protection

[Learn more →](./async-event-system.md)

### 10. Context Management
Zero context loss between sessions:
- GitHub gist persistence
- Context profiles
- Bug tracking
- Research management
- Documentation cache

### 11. Security Features
Enterprise-grade protection:
- Field-level encryption
- PII/PHI detection and blocking
- Audit logging
- TCPA/GDPR compliance
- Role-based access control

### 12. Performance Monitoring
Built-in optimization:
- Bundle size tracking
- Lighthouse integration
- Performance budgets
- Loading time analysis
- Resource usage monitoring

## 📚 Feature Categories

### Development Features
- Component creation with validation
- PRD-driven development
- Stage validation gates
- Task management
- Feature workflows

### Testing Features
- TDD workflow automation
- Browser testing integration
- Visual regression testing
- Performance testing
- Accessibility testing

### Collaboration Features
- Multi-agent orchestration
- GitHub integration
- Team handoffs
- Knowledge sharing
- Pattern extraction

### Automation Features
- Smart chains
- Auto-triggers
- Conditional execution
- Parallel processing
- Error recovery

### Quality Features
- 4-level validation
- Design compliance
- Code quality checks
- Security scanning
- Performance budgets

## 🚀 Getting Started with Features

1. **Essential Daily Commands**
   ```bash
   /sr              # Smart resume
   /cp load frontend # Load context
   /bt list         # Check bugs
   /fw start 123    # Start feature
   ```

2. **Creating Components**
   ```bash
   /cc Button       # Create with validation
   /exists Card     # Check before creating
   /deps check Button # Check dependencies
   ```

3. **Using PRPs**
   ```bash
   /create-prp user-auth
   /prp-execute user-auth --level 1
   /prp-execute user-auth --fix
   ```

4. **Orchestrating Agents**
   ```bash
   /orch payment-system
   /spawn security
   /chain architecture-design
   ```

## 📖 Related Documentation

- [System Overview](../SYSTEM_OVERVIEW.md)
- [Workflow Guide](../workflow/README.md)
- [Command Reference](../claude/CLAUDE_CODE_GUIDE.md)
- [Setup Guide](../setup/GETTING_STARTED.md)
