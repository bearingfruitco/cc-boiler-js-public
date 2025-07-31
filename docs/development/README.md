# Development Guide

> Essential guides for developing with Claude Code Boilerplate v4.0.0

## 📚 Development Documentation

### [Analytics Setup](./analytics-setup.md)
Complete guide to implementing analytics with our event system.
- Event tracking patterns
- Privacy-compliant implementation
- Performance considerations
- Debug mode setup

### [Authentication Guide](./auth-guide.md) 
Comprehensive authentication implementation guide.
- Auth.js v5 setup
- Supabase authentication
- Protected routes
- Session management
- Role-based access control

### [Project AI Knowledge](./project-ai-knowledge.md)
How to structure project-specific knowledge for AI agents.
- Documentation best practices
- Pattern extraction
- Knowledge management
- AI context optimization

### [Commit Guide](./COMMIT_GUIDE.md)
Git commit conventions and workflow.
- Conventional commits
- Branch naming
- PR templates
- Git hooks usage

### [Troubleshooting Guide](./troubleshooting-guide.md)
Common issues and solutions.
- Command errors
- Integration issues
- Performance problems
- Context management

## 🚀 Quick Start for Developers

### 1. Initial Setup
```bash
# Clone and install
git clone [repo]
cd project
npm install

# Initialize Claude Code
/init
/sr
```

### 2. Daily Workflow
```bash
# Morning routine
/sr                      # Smart resume
/chain morning-setup     # Auto checks
/cp load frontend       # Load context

# Development
/fw start 123           # Start feature
/create-prp feature     # Generate PRP
/cc Component           # Create component
/vd                     # Validate design

# Before committing
git add .
git commit -m "feat: description"
# Pre-commit hooks run automatically
```

### 3. Using AI Agents
```bash
# Single agent
/spawn frontend
"Create user profile component"

# Multi-agent orchestration
/orch payment-system

# Automated workflows
/chain feature-development-v4
```

## 🛠️ Development Best Practices

### Code Organization
```
src/
├── components/
│   ├── ui/           # Reusable UI components
│   ├── forms/        # Form components
│   ├── layout/       # Layout components
│   └── features/     # Feature-specific
├── lib/
│   ├── api/          # API utilities
│   ├── db/           # Database queries
│   ├── security/     # Security utilities
│   └── utils/        # Helpers
├── hooks/            # Custom React hooks
├── stores/           # Zustand stores
└── types/            # TypeScript types
```

### Design System Compliance
- **Font sizes**: ONLY text-size-[1-4]
- **Font weights**: ONLY font-regular, font-semibold  
- **Spacing**: ONLY 4px grid (p-1, p-2, p-3, p-4, p-6, p-8)
- **Colors**: 60% neutral, 30% text/UI, 10% accent
- **Mobile-first**: Always test at 375px width

### Security Requirements
- Never log PII to console
- Use field registry for all data fields
- Implement field-level encryption
- Follow TCPA/GDPR compliance
- Use audit logging for sensitive operations

### Testing Strategy
- **TDD First**: Write tests before implementation
- **Coverage**: Minimum 80% code coverage
- **E2E**: Critical user journeys only
- **Performance**: Test on 3G connection
- **Accessibility**: WCAG AA compliance

## 📋 Development Checklists

### New Feature Checklist
- [ ] Create GitHub issue
- [ ] Generate PRD/PRP
- [ ] Run architecture chain
- [ ] Implement with TDD
- [ ] Validate all 4 levels
- [ ] Update documentation
- [ ] Create PR with context

### Component Creation Checklist
- [ ] Check if exists first
- [ ] Follow design system
- [ ] Add TypeScript types
- [ ] Write tests first
- [ ] Add to exports
- [ ] Update dependencies
- [ ] Document props

### Security Checklist
- [ ] No PII in logs
- [ ] Field encryption enabled
- [ ] Audit logging active
- [ ] Input validation
- [ ] Output encoding
- [ ] Rate limiting
- [ ] CSRF protection

## 🔧 Debugging Tips

### Context Issues
```bash
/sr                    # Restore context
/compress             # Reduce token usage
/checkpoint restore   # Go back to saved state
```

### Performance Issues
```bash
/performance-monitor check
/chain performance-optimization-v4
/validate-async       # Find blocking code
```

### Integration Issues
```bash
/deps scan           # Check dependencies
/error-recovery      # Auto-fix common issues
/help               # Context-aware suggestions
```

## 📚 Additional Resources

### Internal Documentation
- [System Overview](../SYSTEM_OVERVIEW.md)
- [Architecture Guide](../architecture/README.md)
- [Workflow Guide](../workflow/README.md)
- [Features Guide](../features/README.md)

### External Resources
- [Next.js Documentation](https://nextjs.org/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS](https://tailwindcss.com/docs)

## 🤝 Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines on:
- Code style
- Testing requirements  
- PR process
- Documentation standards
