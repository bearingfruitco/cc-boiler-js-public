# 🎨 Agency OS Integration Documentation

> **The Operating System for AI Coding Agents** - Centralized standards, drop-in capability, and cross-tool compatibility.

## 📋 Table of Contents
1. [What is Agency OS?](#what-is-agency-os)
2. [Key Features](#key-features)
3. [Quick Start](#quick-start)
4. [Standards System](#standards-system)
5. [Drop-in for Existing Projects](#drop-in-for-existing-projects)
6. [Design System Migration](#design-system-migration)
7. [Cross-Tool Compatibility](#cross-tool-compatibility)
8. [Command Reference](#command-reference)

---

## What is Agency OS?

Agency OS transforms your Claude Code boilerplate into a universal operating system for AI coding agents. It provides:

- **🎯 Centralized Standards**: One source of truth for all development rules
- **🔌 Drop-in Capability**: Works with ANY existing codebase
- **🔄 Cross-Tool Sharing**: Standards work in Claude Code, Cursor, and any AI tool
- **📐 Spec-Driven Development**: Three-layer context (Standards → Product → Specs)

### Three-Layer Architecture
```
.agent-os/
├── standards/          # Global rules (shared across projects)
│   ├── design-system.md
│   ├── tech-stack.md
│   └── best-practices.md
├── product/            # Project-specific context
│   ├── mission.md
│   ├── roadmap.md
│   └── decisions.md
└── specs/              # Feature specifications
    ├── active/
    └── completed/
```

---

## Key Features

### 1. Centralized Standards System
- All design rules in `.agent-os/standards/`
- Single update propagates everywhere
- No more scattered documentation
- Version controlled and shareable

### 2. Drop-in Capability
```bash
# Works with ANY existing project
cd existing-project
/analyze-existing           # Full analysis and setup
/migrate-to-strict-design   # Convert to strict system
```

### 3. Cross-Tool Compatibility
```bash
# Claude Code
/sr  # Loads standards automatically

# Cursor
cat .agent-os/standards/*.md > .cursorrules

# GitHub Copilot
cat .agent-os/standards/*.md > .github/copilot-instructions.md
```

### 4. Automated Migration
- Analyzes existing code patterns
- Generates migration plan
- Auto-converts to strict design system
- Creates backup before changes

---

## Quick Start

### For New Projects
```bash
# Standards are already set up in .agent-os/standards/
/sr                    # Start with standards loaded
/init-project          # Initialize new project
```

### For Existing Projects
```bash
cd existing-project

# Step 1: Analyze
/analyze-existing      # Or /ae

# Step 2: Check design compliance
/migrate-to-strict-design analyze  # Or /mds analyze

# Step 3: Migrate if needed
/migrate-to-strict-design migrate  # Or /mds migrate

# Step 4: Document existing features
/create-prd-from-existing [feature-name]  # Or /prd-existing
```

---

## Standards System

### Design System Standards
Location: `.agent-os/standards/design-system.md`

Key Rules:
- **Typography**: Only text-size-[1-4], font-regular/semibold
- **Spacing**: 4px grid only (p-1, p-2, p-3, p-4, p-6, p-8...)
- **Colors**: 60/30/10 distribution rule
- **Mobile**: Min touch targets 44px (h-11)

### Tech Stack Standards
Location: `.agent-os/standards/tech-stack.md`

Defines:
- Core framework choices
- Approved libraries
- Development tools
- Infrastructure decisions

### Best Practices Standards
Location: `.agent-os/standards/best-practices.md`

Covers:
- Code quality requirements
- Testing standards
- Performance targets
- Security guidelines

---

## Drop-in for Existing Projects

The `/analyze-existing` command provides comprehensive project analysis:

```bash
/ae  # Short alias

# What it does:
1. Detects tech stack and framework
2. Analyzes project structure
3. Identifies existing features
4. Creates mission/roadmap docs
5. Generates migration plan
6. Sets up all boilerplate tools
```

### Generated Documentation
```
.agent-os/product/
├── mission.md      # What you're building
├── roadmap.md      # Phase 0 = existing features
├── tech-stack.md   # Detected technologies
└── decisions.md    # Architectural choices
```

### Example Output
```
🔍 ANALYZING EXISTING PROJECT: my-saas-app

📊 DETECTED STACK:
- Framework: Next.js 14.2.0
- UI: Tailwind CSS + shadcn/ui
- Testing: Jest + React Testing Library

🎨 DESIGN ANALYSIS:
- Using 12 different font sizes (should be 4)
- Using 8 different font weights (should be 2)

✅ CREATED:
- .agent-os/product/mission.md
- .agent-os/product/roadmap.md
- MIGRATION_PLAN.md
```

---

## Design System Migration

The `/migrate-to-strict-design` command handles automated migration:

### Step 1: Analysis
```bash
/mds analyze

# Generates: DESIGN_MIGRATION_REPORT.md
# Shows all violations by type and location
```

### Step 2: Migration
```bash
/mds migrate

# What it does:
1. Creates backup in .agent-os/backups/
2. Updates all font sizes to text-size-[1-4]
3. Updates all font weights to font-regular/semibold
4. Fixes spacing to 4px grid
5. Updates touch targets to minimum 44px
```

### Safe Migration Features
- Automatic backup before changes
- Dry-run mode available
- Incremental migration by category
- Visual regression testing support

---

## Cross-Tool Compatibility

### Share Standards Across Tools

#### Method 1: Direct Reference
```javascript
// In any tool's configuration
const standards = {
  design: fs.readFileSync('.agent-os/standards/design-system.md'),
  tech: fs.readFileSync('.agent-os/standards/tech-stack.md'),
  practices: fs.readFileSync('.agent-os/standards/best-practices.md')
};
```

#### Method 2: Git Submodule
```bash
# Share across multiple projects
git submodule add https://github.com/your-org/agency-standards .agent-os
```

#### Method 3: NPM Package
```bash
npm install @your-org/agency-standards
ln -s node_modules/@your-org/agency-standards .agent-os
```

---

## Command Reference

### Analysis Commands
- `/analyze-existing` (`/ae`) - Analyze and set up existing project
- `/create-prd-from-existing` (`/prd-existing`) - Document existing features

### Migration Commands
- `/migrate-to-strict-design analyze` (`/mds analyze`) - Check compliance
- `/migrate-to-strict-design migrate` (`/mds migrate`) - Auto-migrate

### Workflow Chains
- `/chain analyze-existing-project` - Full project analysis
- `/chain migrate-design-system` - Complete migration
- `/chain onboard-existing` - Full onboarding process
- `/chain standards-sync` - Sync with central standards

### Standards Management
- View: `cat .agent-os/standards/*.md`
- Edit: Direct file editing (changes immediate)
- Validate: `/vd` reads from standards automatically

---

## Integration Benefits

1. **Consistency**: Same rules everywhere, every time
2. **Efficiency**: Drop into any project instantly
3. **Quality**: Automated enforcement at multiple levels
4. **Flexibility**: Standards can evolve with your needs
5. **Collaboration**: Teams share the same source of truth

---

## Next Steps

1. **Customize Standards**: Edit `.agent-os/standards/*.md` to match your preferences
2. **Try Existing Project**: Run `/ae` on any codebase
3. **Test Migration**: Use `/mds` to see the migration process
4. **Share with Team**: Set up centralized standards repository

---

Welcome to the future of AI-assisted development with Agency OS! 🚀