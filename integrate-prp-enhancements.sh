#!/bin/bash
# integrate-prp-enhancements.sh
# Run this script to complete the PRP system integration

echo "🚀 Integrating Enhanced PRP System..."
echo "=================================="

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Run this script from your project root directory"
    exit 1
fi

# Create any missing directories
echo "📁 Creating directory structure..."
mkdir -p PRPs/{templates,ai_docs,scripts,active,completed,examples,metrics}
mkdir -p .claude/commands/{PRPs,git-operations,typescript,code-quality,development}
mkdir -p claude_md_files

# Make scripts executable
echo "🔧 Setting script permissions..."
chmod +x PRPs/scripts/*.py
chmod +x .claude/hooks/pre-tool-use/*.py
chmod +x .claude/hooks/post-tool-use/*.py

# Create AI docs index
echo "📚 Creating AI documentation index..."
cat > PRPs/ai_docs/index.md << 'EOF'
# AI Documentation Index

## Available Documentation

### Core Patterns
- `nextjs_15_patterns.md` - Next.js 15 server components, actions, routing
- `supabase_patterns.md` - Auth, real-time, RLS, storage patterns  
- `design_system_rules.md` - Enforced typography, spacing, components
- `security_requirements.md` - PII/PHI protection, encryption, compliance

### Development Guides
- `typescript_gotchas.md` - Common TS pitfalls and solutions
- `async_patterns.md` - Event queue, parallel operations, loading states
- `testing_strategies.md` - Unit, integration, E2E test patterns

### Performance
- `optimization_guide.md` - Bundle size, caching, lazy loading
- `database_performance.md` - Query optimization, indexing

## Usage in PRPs

Reference these docs in your PRP's Required Context section:

```yaml
- doc: PRPs/ai_docs/nextjs_15_patterns.md
  why: Using server components and async patterns
  critical: Form actions pattern (section 4)
```

## Keeping Docs Updated

When you discover new patterns or gotchas:
1. Update the relevant AI doc
2. Add examples from actual code
3. Include "gotcha" warnings
4. Run `/doc-index update` to rebuild
EOF

# Create example PRP
echo "📝 Creating example PRP..."
cat > PRPs/examples/user-profile-example.md << 'EOF'
# PRP: User Profile Management - Example Implementation

> **Example PRP showing complete implementation pattern**
> Reference this for creating new PRPs

## 🎯 Goal

Implement a complete user profile management system with:
- Profile viewing and editing
- Avatar upload
- Settings management
- Real-time updates

## ✅ Success Criteria

- [ ] Users can view their profile
- [ ] Users can edit profile fields
- [ ] Avatar upload with optimization
- [ ] Changes reflected in real-time
- [ ] Mobile-responsive design
- [ ] Accessibility compliant (WCAG 2.1 AA)
- [ ] Performance: < 2s load time
- [ ] Security: All PII encrypted

## 📚 Required Context

### Design System References
```yaml
- doc: PRPs/ai_docs/design_system_rules.md
  why: Building UI components
  critical: Card and form patterns

- doc: PRPs/ai_docs/supabase_patterns.md
  why: Database operations and real-time
  critical: RLS policies for profiles
  
- doc: PRPs/ai_docs/security_requirements.md
  why: Handling PII (email, phone)
  critical: Field encryption patterns
```

### Codebase Patterns
```yaml
- file: components/forms/ContactForm.tsx
  pattern: Form validation with react-hook-form
  lines: 45-89

- file: components/ui/Button.tsx
  pattern: Loading states and disabled handling
  
- file: lib/supabase/client.ts
  pattern: Supabase client setup
```

### Known Gotchas
1. **Avatar upload**: Must validate file type and size client-side
2. **Real-time**: Need to unsubscribe on component unmount
3. **Hydration**: Use useEffect for client-only values

## 🏗️ Implementation Blueprint

[Full implementation details would follow...]

## 🧪 Validation Loops

### Level 1: Syntax & Standards ✓
```bash
bun run lint
bun run typecheck
/vd
```

### Level 2: Component Testing ✓
```bash
bun test Profile.test.tsx
bun test AvatarUpload.test.tsx
```

### Level 3: Integration Testing ✓
```bash
bun test:e2e profile
```

### Level 4: Production Readiness ✓
```bash
/security-scan
/bundle-analyze
/pp
```

## 📊 Success Metrics
```yaml
first_pass_success: true
validation_scores:
  syntax: 100%
  components: 98%
  integration: 95%
  production: 100%
time_to_complete: "3h 15m"
bugs_found_after: 0
test_coverage: 89%
bundle_impact: +12.4kb
```

---
**Status**: Completed ✅
**Lessons Learned**: Real-time subscriptions need careful cleanup
EOF

# Create quick reference
echo "📋 Creating quick reference..."
cat > .claude/PRP_QUICK_REFERENCE.md << 'EOF'
# PRP Quick Reference

## Essential Commands

```bash
# Create new PRP
/create-prp user-authentication
/prp auth-feature              # Short alias

# Execute with validation
/prp-execute auth-feature       # All levels
/prp-exec auth --level 2        # Specific level
/prp-exec auth --fix            # Auto-fix issues

# Chain PRPs
/prp-chain auth → profile → settings

# View metrics
/prp-metrics auth-feature       # Individual
/prp-metrics --summary          # Overall stats
```

## PRP Structure

1. **Goal** - What we're building
2. **Success Criteria** - Measurable outcomes
3. **Required Context** - Docs, files, patterns
4. **Implementation** - Step-by-step blueprint
5. **Validation** - 4-level quality gates
6. **Metrics** - Track success

## Validation Levels

1. **Syntax & Standards** - Lint, types, design
2. **Component Testing** - Unit & component tests  
3. **Integration Testing** - E2E, API tests
4. **Production Readiness** - Security, performance

## Tips

- Reference AI docs for patterns
- Include gotchas upfront
- Be specific in success criteria
- Test each level before proceeding
- Update metrics after completion
EOF

# Final summary
echo ""
echo "✅ PRP Enhancement Integration Complete!"
echo "======================================="
echo ""
echo "📚 What's New:"
echo "  • Enhanced PRP templates in PRPs/templates/"
echo "  • AI documentation in PRPs/ai_docs/"
echo "  • Automated PRP runner: python PRPs/scripts/prp_runner.py"
echo "  • New commands: /prp-chain, /prp-metrics, /create-worktree"
echo "  • Validation hooks: PRP structure and AI docs suggestions"
echo "  • Example PRP: PRPs/examples/user-profile-example.md"
echo ""
echo "🚀 Next Steps:"
echo "  1. Run '/sr' to load the enhanced system"
echo "  2. Try '/create-prp test-feature' to generate your first PRP"
echo "  3. Use '/prp-execute test-feature' to run validation"
echo "  4. Check '/help prp' for all PRP commands"
echo ""
echo "💡 Pro Tips:"
echo "  • Always start with a PRP before coding"
echo "  • Reference AI docs for best practices"
echo "  • Run validation after each implementation phase"
echo "  • Track metrics to improve over time"
echo ""
echo "📖 Documentation:"
echo "  • Quick Reference: .claude/PRP_QUICK_REFERENCE.md"
echo "  • AI Docs Index: PRPs/ai_docs/index.md"
echo "  • Example PRP: PRPs/examples/user-profile-example.md"
echo ""
echo "Happy coding with one-pass success! 🎯"
