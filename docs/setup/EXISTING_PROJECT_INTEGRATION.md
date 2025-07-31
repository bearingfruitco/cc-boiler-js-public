# Integrating Claude Code Boilerplate into Existing Projects v4.0.0

> Transform your existing codebase with AI-assisted development, automated workflows, and production-ready patterns.

## 🎯 Overview

Two integration approaches based on your project's needs:

1. **Full Integration** (Recommended) - Complete system with Agent OS, all commands, and workflows
2. **Selective Integration** - Choose specific components (just commands, just PRP, just design system)

## 🚀 Full Integration Workflow

### Phase 0: Get the Integration Script

```bash
# From your existing project root:
cd /path/to/your-project

# Option 1: Enhanced v2 Script (Recommended - Never overwrites files!)
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-boilerplate-v2.sh -o integrate-boilerplate-v2.sh
chmod +x integrate-boilerplate-v2.sh
./integrate-boilerplate-v2.sh --mode=full

# Option 2: Original script (overwrites with backups)
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-boilerplate.sh | bash

# Option 3: See what would happen first
./integrate-boilerplate-v2.sh --dry-run
```

### 🆕 Enhanced v2 Script Features
- **Never overwrites your files** - Adds `-boilerplate` suffix instead
- **Clear diffs** for all conflicts
- **Integration wizard** command for guided merging
- **Complete rollback** capability
- **Detailed report** of all changes

### Phase 1: Analysis & Discovery

```bash
# After integration, in Claude Code:
claude .
/sr                    # Load the integrated system
/analyze-existing full # Analyze your codebase
```

This powerful command will:
- 🔍 Detect your tech stack and framework
- 📁 Analyze project structure and patterns
- 🎯 Identify existing features
- 📊 Count components and complexity
- 🏗️ Generate complete documentation

#### What Gets Generated

```
.agent-os/
├── product/
│   ├── mission.md          # Extracted from your codebase
│   ├── roadmap.md          # Phase 0 = what's already built
│   ├── tech-stack.md       # Detected dependencies
│   └── decisions.md        # Ready for your ADRs
└── MIGRATION_GUIDE.md      # Specific to your project
```

### Phase 2: Design System Migration

```bash
# Analyze current design patterns
/migrate-to-strict-design analyze

# Review the report at .agent-os/DESIGN_MIGRATION_REPORT.md
# Shows all violations and suggested fixes

# If you want to proceed with migration
/migrate-to-strict-design migrate

# This will:
# - Backup your components
# - Convert to 4-size, 2-weight system
# - Update spacing to 4px grid
# - Generate migration CSS for Tailwind v4
```

### Phase 3: Documentation Generation

```bash
# For each major existing feature, generate PRDs
/create-prd-from-existing user-authentication
/create-prd-from-existing shopping-cart
/create-prd-from-existing admin-dashboard

# Generate comprehensive architecture
/chain architecture-design

# This creates:
# - Complete system design
# - Database documentation
# - API specifications
# - PRPs for each component
```

### Phase 4: Review Integration Results

The integration script has already handled ALL these files intelligently:

#### Core System Files
```bash
# Your existing CLAUDE.md is preserved
CLAUDE.md                    # Your instructions (kept)
CLAUDE_BOILERPLATE.md       # Our instructions (added)

# .claude directory - intelligent merging
.claude/
├── commands/
│   ├── [your-unique].md    # Your unique commands (kept in place)
│   ├── [conflicting].md    # Conflicts: yours → [name]-project.md
│   └── [our-commands].md   # Our 116+ commands (added)
├── hooks/
│   ├── pre-tool-use/
│   │   ├── 00-your-hook.py # Your hooks (renumbered to run first)
│   │   ├── 10-design-check.py # Our hooks (run after yours)
│   │   └── ...
├── personas/
│   ├── project-personas.json # Your personas (kept)
│   └── agent-personas.json   # Our 31 agents (added)
└── config.json              # Merged configuration
```

#### Standards & Documentation
```bash
.agent-os/                   # Complete standards system
PRPs/                       # One-pass implementation templates
field-registry/             # Security features
QUICK_REFERENCE.md         # Command reference
```

#### Configuration Files
```bash
# Merged (manual step needed):
tailwind.config.js         # Add design tokens from backup
tsconfig.json             # Add path aliases from backup

# Added if didn't exist:
biome.json                # Linting/formatting
components.json           # shadcn/ui config
.coderabbit.yaml         # AI code reviews
playwright.config.ts     # E2E testing

# Skipped if you have DB setup:
drizzle.config.ts        # Only added if no DB config exists
```

#### Code Structure
```bash
# Smart directory merging:
components/
├── ui/                    # Added if not exists
├── forms/                 # Added if not exists
└── [your-components]/     # Untouched

lib/
├── events/                # Async event system (added)
├── validation/            # Zod schemas (added)
├── api/                   # API utilities (added)
├── db/                    # Only if no DB exists
└── [your-code]/           # Untouched

# Added if not exist:
hooks/                     # Custom React hooks
stores/                    # Zustand stores
types/                     # TypeScript types
templates/                 # Component templates
```

#### What's NOT Touched
```bash
# Sacred files - never modified:
app/                       # Your routes
package.json              # Your dependencies
middleware.ts             # Your middleware
.env*                     # Your secrets
public/                   # Your assets
tests/                    # Your tests
```

📖 **Full details**: See [INTEGRATION_FILE_MANIFEST.md](./INTEGRATION_FILE_MANIFEST.md) for complete file handling

#### Handling Conflicts

**Existing Commands?**
```bash
# Critical commands (like /sr, /cc, /vd):
Your version: /cc → /cc-project
Our version: /cc (takes precedence)

# Non-critical commands:
Your version: /deploy (kept)
Our version: /deploy-bp (renamed)

# Access both:
/cc              # Boilerplate version
/cc-project      # Your original
```

**Existing Hooks?**
```bash
# Execution order via numbering:
00-09: Your critical hooks
10-19: Our critical hooks
20-29: Your feature hooks
30-39: Our feature hooks

# Both run, yours first!
```

**Existing CLAUDE.md?**
```bash
# Yours remains primary
# Ours added as CLAUDE_BOILERPLATE.md
# Your file gets a note about the integration
```

**Existing Sub-Agents?**
```bash
# Separate files, no conflicts
your-agents.json     # Kept
agent-personas.json  # Added
```

### Phase 5: Complete Integration

#### Install Missing Dependencies

The script will list dependencies to add:

```bash
# Core dependencies your project might need
pnpm add @supabase/supabase-js framer-motion lucide-react zustand
pnpm add react-hook-form @hookform/resolvers zod

# Dev dependencies
pnpm add -D @biomejs/biome drizzle-kit @playwright/test
```

#### Manual Config Merges

If you had existing configs, merge these additions:

**tailwind.config.js** - Add to theme.extend:
```javascript
fontSize: {
  'size-1': ['32px', { lineHeight: '1.25' }],
  'size-2': ['24px', { lineHeight: '1.375' }],
  'size-3': ['16px', { lineHeight: '1.5' }],
  'size-4': ['12px', { lineHeight: '1.5' }],
},
fontWeight: {
  regular: '400',
  semibold: '600',
},
spacing: {
  '11': '44px', // min touch target
  '12': '48px', // preferred touch target
}
```

**tsconfig.json** - Add to compilerOptions.paths:
```json
"paths": {
  "@/*": ["./*"],
  "@/components/*": ["./components/*"],
  "@/lib/*": ["./lib/*"],
  "@/hooks/*": ["./hooks/*"]
}
```

#### Configure Project

```bash
# In Claude Code
/config set repository.owner YOUR_GITHUB_USERNAME
/config set repository.name YOUR_REPO_NAME
/config set project.name "Your Project Name"

# Or edit .claude/project-config.json directly
```

### Phase 6: Verification

```bash
# Test the integration
/sr                    # Smart resume - loads everything
/deps scan             # Scan existing dependencies
/vd                    # Validate design compliance
/test                  # Run your existing tests
/chain list           # See available workflows
```

## 🔧 Selective Integration Options

### Three Integration Modes

#### 1. Full Mode (Recommended)
```bash
# Download and run the integration script
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-boilerplate.sh -o integrate.sh
chmod +x integrate.sh
./integrate.sh --mode=full

# What happens:
# - Intelligent merging of everything
# - Your work preserved and accessible
# - Conflicts resolved by renaming
# - Full boilerplate power available
```

#### 2. Selective Mode
```bash
./integrate.sh --mode=selective

# Interactive menu appears:
# 1) Commands & Automation (.claude/)
# 2) Design System Enforcement  
# 3) PRP System (PRPs/)
# 4) Agent OS Standards (.agent-os/)
# 5) Security Features (field-registry/)
# 6) Git Hooks (.husky/)
# 7) Documentation (CLAUDE.md, guides)
# 8) Config Files (.coderabbit.yaml, etc)
#
# Enter: 1,3,5  (to select specific items)

# Perfect for:
# - Projects with extensive Claude setups
# - Teams wanting specific features only
# - Gradual adoption
```

#### 3. Sidecar Mode
```bash
./integrate.sh --mode=sidecar

# Creates parallel installation:
.claude/              # Your existing setup (untouched)
.claude-boilerplate/  # Our complete system

# Then in Claude Code:
# Access boilerplate commands by using them from .claude-boilerplate/
# No conflicts, complete separation

# Perfect for:
# - Testing without commitment
# - Very customized existing setups
# - Comparing approaches
```

### Manual Integration (If Scripts Don't Work)

If you prefer manual control or the scripts have issues:

```bash
# 1. Clone boilerplate to a temporary location
git clone https://github.com/bearingfruitco/claude-code-boilerplate.git /tmp/boilerplate

# 2. From your project root, manually copy what you need:

# If you DON'T have .claude yet:
cp -r /tmp/boilerplate/.claude .

# If you DO have .claude:
mkdir -p .claude-backup
cp -r .claude/* .claude-backup/
# Then manually merge, being careful with conflicts

# Copy other directories as needed:
cp -r /tmp/boilerplate/.agent-os .     # Standards system
cp -r /tmp/boilerplate/PRPs .          # PRP templates
cp -r /tmp/boilerplate/field-registry . # Security features

# Handle CLAUDE.md
if [ -f "CLAUDE.md" ]; then
  cp /tmp/boilerplate/CLAUDE.md CLAUDE_BOILERPLATE.md
else
  cp /tmp/boilerplate/CLAUDE.md .
fi

# Clean up
rm -rf /tmp/boilerplate
```

## 🔄 Integration Workflow Examples

### Starting Fresh Development

After integration, new features follow the modern workflow:

```bash
# Start new feature
/fw start new-feature

# Generate implementation guide
/create-prp payment-integration

# Orchestrate specialists
/orch payment-integration

# Validate continuously
/prp-execute payment-integration --level 1  # Syntax
/prp-execute payment-integration --level 2  # Components
/prp-execute payment-integration --level 3  # Integration
/prp-execute payment-integration --level 4  # Production

# Complete
/fw complete
```

### Enhancing Existing Features

```bash
# Analyze what exists
/deps check ShoppingCart
/exists CartItem

# Generate enhancement PRP
/create-prp cart-performance-optimization

# Use analyzer agent
/spawn analyzer
"Trace through cart checkout flow"

# Apply optimizations with validation
/validate-async  # Check for blocking operations
/vd              # Ensure design compliance
```

### Refactoring with Safety

```bash
# Before refactoring
/checkpoint create pre-refactor
/deps scan  # Know what depends on your changes

# During refactoring
/chain refactoring-chain

# Agents will:
# - Analyze code
# - Create refactoring plan
# - Ensure test coverage
# - Execute refactoring
# - Verify functionality
```

## 📊 What to Expect

### Immediate Benefits (Day 1)
- ✅ Smart context management (`/sr`)
- ✅ Command shortcuts for everything
- ✅ Automated design validation
- ✅ Bug tracking across sessions
- ✅ GitHub integration

### Short Term (Week 1)
- ✅ Faster feature development with PRPs
- ✅ Consistent code quality
- ✅ Reduced context switching
- ✅ Better test coverage
- ✅ Cleaner commits

### Long Term (Month 1)
- ✅ 70% faster development
- ✅ 90% fewer inconsistencies
- ✅ Accumulated patterns library
- ✅ Team knowledge sharing
- ✅ Reduced technical debt

## 🚨 Common Integration Scenarios

### Scenario: Different Testing Framework

Your project uses Jest, boilerplate uses Vitest:

```bash
# Option 1: Keep Jest
/config set testing.framework jest
/config set testing.runner "npm test"

# Option 2: Migrate to Vitest (recommended)
/chain migrate-to-vitest
```

### Scenario: Different State Management

Your project uses Redux, boilerplate uses Zustand:

```bash
# Keep both - they can coexist
# New features use Zustand
# Existing features keep Redux
# Gradual migration possible
```

### Scenario: Monorepo Structure

```bash
# Install at monorepo root
cd /monorepo-root
/analyze-existing full

# Configure for monorepo
/config set project.type monorepo
/config set project.packages ["web", "api", "shared"]
```

### Scenario: Custom Build System

```bash
# Configure commands to use your build
/config set build.command "your-build-command"
/config set test.command "your-test-command"
/config set dev.command "your-dev-command"
```

## 🛡️ Safety Measures

### Automatic Backups

The `/integrate-boilerplate` command automatically:

```bash
# Creates timestamped backup
.claude-integration/
├── backup/
│   └── 20250730_143022/
│       ├── .claude/          # Your complete .claude directory
│       ├── CLAUDE.md        # Your AI instructions
│       └── .husky/          # Your Git hooks
├── CONFLICT_REPORT.md     # What conflicts were found
├── MERGE_PLAN.md         # How they were resolved
└── INTEGRATION_COMPLETE.md # What was added/changed
```

### Dry Run Mode

```bash
# See what would happen without changes
/integrate-boilerplate --dry-run

# Shows:
# - What conflicts exist
# - How they'd be resolved  
# - What would be added
# - No actual changes made
```

### Instant Rollback

```bash
# If something goes wrong
/integration-rollback

# Or manually:
rm -rf .claude
cp -r .claude-integration/backup/[latest]/.claude .
rm -f CLAUDE_BOILERPLATE.md

# You're back to pre-integration state!
```

### Gradual Adoption

Start small:
```bash
# Week 1: Just use commands
/sr, /cc, /vd

# Week 2: Try PRPs for new features
/create-prp, /prp-execute

# Week 3: Enable hooks
Design validation, security checks

# Week 4: Full workflow
Orchestration, chains, agents
```

### Rollback Options

```bash
# Rollback commands
/checkpoint restore pre-integration

# Rollback design migration
mv components.backup.* components

# Remove integration
rm -rf .claude .agent-os .husky PRPs
```

## 📚 After Integration

### Recommended Reading
1. [SYSTEM_WORKFLOWS.md](./SYSTEM_WORKFLOWS.md) - How to use the system
2. [docs/workflow/](../workflow/) - Specific workflow guides
3. [PRPs/README.md](../../PRPs/README.md) - PRP methodology

### Training Your Team

```bash
# Generate team onboarding
/chain team-onboarding

# This creates:
# - Custom guide for your codebase
# - Common patterns document
# - Quick reference card
# - Video script (if needed)
```

### Continuous Improvement

```bash
# Weekly pattern extraction
/specs extract

# Monthly metrics review
/metrics report

# Quarterly system update
/update-boilerplate
```

## ❓ FAQ

**Q: Will this break my existing code?**  
A: No. The system is additive. Your code continues working, with new tools available.

**Q: Can I remove it if needed?**  
A: Yes. Clean removal is simple - delete added directories.

**Q: How long does integration take?**  
A: Basic: 15 minutes. Full integration with migration: 2-4 hours.

**Q: Will my team need training?**  
A: Basic commands are intuitive. Advanced features have built-in help.

**Q: Can I customize everything?**  
A: Yes. All commands, hooks, and agents are customizable.

---

**Support**: [Your support channels]  
**Version**: 4.0.0 - "Automation & Intelligence"  
**License**: [Your license]
