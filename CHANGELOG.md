# 📝 Changelog

All notable changes to the Claude Code Boilerplate project.

## [2.7.0] - July 2025 (Task Ledger Update)

### 📋 Task Ledger System

This release adds a persistent task tracking system that provides project-wide visibility into all generated and processed tasks.

#### New Features

##### Task Ledger (`.task-ledger.md`)
- **Persistent Task Tracking** - Single source of truth for all tasks
  - Automatically updated by hooks when tasks are created/modified
  - Tracks progress across all features in one file
  - Links tasks directly to GitHub issues
  - Survives session restarts and context switches
  - Included in GitHub gist saves

##### New Command
- `/task-ledger` (`/tl`) - View and manage task ledger
  - `/tl` - View complete ledger
  - `/tl summary` - Quick stats overview
  - `/tl sync` - Sync with all task files
  - `/tl feature [name]` - Focus on specific feature

##### Integration Enhancements
- **Smart Resume** - Shows task ledger summary with progress
- **Task Status** - Now reads from persistent ledger
- **Task Board** - Uses ledger for accurate state
- **Process Tasks** - Updates ledger in real-time
- **Chains** - Updated `daily-startup`, `task-sprint`, and `feature-planning`

##### Hook Added
- `15b-task-ledger-updater.py` - Maintains ledger automatically

#### Benefits
- Never lose task progress between sessions
- See all work in one place
- Better sprint planning with complete visibility
- Perfect for team handoffs
- Complements existing task commands

#### Setup
```bash
# For new projects - automatic
# For existing projects:
./init-task-ledger.sh
/tl sync  # Import existing tasks
```

---

## [2.6.0] - July 2025 (Branch Awareness Update)

### 🌿 Branch Awareness & Feature Protection System

This release adds intelligent branch awareness and feature protection to prevent AI from recreating completed work or creating conflicting branches.

#### New Features

##### Branch Awareness System
- **Feature Protection** - AI now knows what features are already completed
  - Non-blocking awareness when editing completed features
  - Shows helpful context about existing implementations
  - Prevents accidental recreation of working code
  - Progressive enhancement: info → warnings → protection

- **Branch Management** - Intelligent branch hygiene
  - Branch health monitoring and tips
  - Automatic conflict detection
  - Smart branch switching with context preservation
  - Integration with existing workflows

##### New Commands
- `/branch-info` (`/bi`) - Lightweight branch status for automation
- `/branch-status` (`/bs`) - Comprehensive branch overview
- `/feature-status` (`/fs`) - Check feature completion and details
- `/sync-main` (`/sync`) - Safely sync main branch
- `/feature-complete` (`/fc`) - Mark features as completed
- `/branch-clean` (`/bc`) - Clean up merged branches
- `/branch-switch` (`/bsw`) - Smart branch switching

##### Enhanced Integration
- **Smart Resume** - Now shows branch health and feature warnings
- **PRP Integration** - Feature awareness in validation loops
- **Event System** - Branch events through async queue
- **New Chains** - `branch-aware-startup`, `safe-feature-complete`, `branch-maintenance`

##### Hooks Added
- `20-feature-awareness.py` - Shows context when editing completed features
- `branch-health.py` - Periodic branch hygiene notifications

#### Configuration
- New `branch_awareness` section in config.json
- Info-only mode by default (non-blocking)
- Configurable notification frequency
- Optional protection levels

---

## [2.5.0] - June 2025

### 🚀 Major Release: PRP System, TDD Integration, and Master Workflow Guide

This release introduces the Product Requirement Prompt (PRP) methodology for one-pass implementation success, enforced Test-Driven Development, and comprehensive documentation improvements.

#### New Features

##### PRP (Product Requirement Prompt) System
- **One-Pass Implementation** - Complete context for production-ready code on first attempt
  - Combines PRD + codebase intelligence + validation loops
  - AI-optimized documentation for common patterns
  - 4-level validation: Syntax → Components → Integration → Production
  - Automated validation runner with fix mode
  
- **New Commands**
  - `/create-prp` or `/prp` - Generate comprehensive PRP
  - `/prp-execute` or `/prp-exec` - Run validation loops
  - `/prp-execute --fix` - Auto-fix common issues
  - `/prp-execute --level [1-4]` - Run specific validation level
  - `/prd-to-prp` - Convert existing PRD to PRP
  - `/prp-status` - Check PRP progress
  - `/prp-complete` - Mark PRP as done

##### TDD Integration
- **Enforced Test-First Development** - Hooks literally block component creation without tests
  - `19-tdd-enforcer.py` - Blocks implementation without tests
  - `06-test-auto-runner.py` - Runs tests automatically on save
  - `17-test-generation-enforcer.py` - Ensures tests from requirements
  
- **Test Automation**
  - Automatic test generation from PRDs and PRPs
  - Tests run on every file save with immediate feedback
  - TDD workflow commands with comprehensive quick reference
  - Integration with stage validation gates

- **New Commands**
  - `/tdd-workflow` - Complete TDD workflow
  - `/prd-tests` - Generate tests from PRD
  - Enhanced `/tr` commands for test running

##### Master Workflow Guide
- **Single Source of Truth** - `MASTER_WORKFLOW_GUIDE.md`
  - Complete command reference (112+ commands)
  - Daily workflow patterns with real examples
  - When to use PRP vs PRD decision tree
  - Context management strategies
  - Common scenarios and solutions
  - Troubleshooting guide
  
- **Documentation Updates**
  - All core docs updated to reference master guide
  - Added `TDD_QUICK_REFERENCE.md`
  - Enhanced `PRPs/README.md` with methodology
  - Updated setup guides with new workflows

#### Technical Improvements

##### Enhanced Hooks
- New hooks for TDD enforcement
- Improved PRP validation hooks
- Better dependency tracking with v2 hooks
- Enhanced response capture for GitHub issues
- More robust error handling

##### Command System
- Added 15+ new commands
- Better command aliases for discovery
- Enhanced help system
- Improved command documentation

##### Project Structure
- New `PRPs/` directory structure
  - `templates/` - PRP templates
  - `ai_docs/` - AI-optimized documentation
  - `scripts/` - Validation runner
  - `active/` - Current PRPs
  - `completed/` - Reference PRPs

#### Breaking Changes
None - all changes are additive

#### Migration Guide
1. Run `./setup-prp.sh` to set up PRP system
2. Read `MASTER_WORKFLOW_GUIDE.md` for new workflows
3. Try `/create-prp` for your next feature
4. Enable TDD with existing `/tdd-workflow` command

#### Documentation
- New guide: `MASTER_WORKFLOW_GUIDE.md`
- New guide: `TDD_QUICK_REFERENCE.md`
- New guide: `docs/workflow/TDD_WORKFLOW_GUIDE.md`
- Updated: All core documentation

See [GitHub Issue #17](https://github.com/bearingfruitco/claude-code-boilerplate/issues/17) for release announcement.

---

## [2.3.5] - January 2025

### 📚 Research Management System (RMS)

Introduced intelligent organization and updating of internal research/planning documents to prevent version proliferation.

#### New Features
- **Smart Document Updates** - Detects and merges updates instead of creating duplicates
  - Document type-aware merging (analysis, planning, decisions)
  - Version history preserved
  - Single source of truth per topic
  - No more auth-v1, auth-v2, auth-final versions

- **Automatic Organization** - Research docs organized, not scattered
  - Hook detects research documents automatically
  - Organizes in `.claude/research/` structure
  - Links to features based on git branch
  - Searchable index for finding past research

- **Context-Aware Loading** - Prevents context overload
  - Manual inclusion by default (`auto_include: false`)
  - Max 2 docs, 10KB total limits
  - Summaries only unless requested
  - Feature-specific loading

#### New Commands
- `/research review` - Organize pending documents
- `/research update` - Update existing research
- `/research search` - Find past analysis
- `/research context` - Manage research in context
- `/research history` - View version history

#### Documentation
- New guide: `docs/guides/research-management-guide.md`
- Updated CLAUDE.md with research workflow
- Enhanced command references

See [v2.3.5 Release Notes](docs/releases/v2.3.5.md) for full details.

## [2.3.4] - January 2025

### 🐰 CodeRabbit IDE Integration

Introduced seamless integration with CodeRabbit IDE extension for real-time code review in Cursor/VSCode.

#### New Features
- **Dual-AI Workflow** - Claude generates, CodeRabbit reviews in real-time
  - 95% bug catch rate before commit
  - Design system enforcement as you type
  - Educational feedback improves skills
  - One-click fixes for simple issues

- **PR Feedback Command** - Quick status checks
  - `/pr-feedback` shows PR status summary
  - Complements real-time IDE review
  - Lightweight final check before merge

- **Enhanced Configuration** - CodeRabbit-aware settings
  - IDE extension mode in config
  - Custom `.coderabbit.yaml` template
  - Design system rules for CodeRabbit

#### Documentation Updates
- New integration guide: `/docs/guides/coderabbit-integration.md`
- Updated Day 1 setup guide with IDE instructions
- Enhanced QUICK_REFERENCE.md with new workflow
- CLAUDE.md includes CodeRabbit best practices

#### Files Modified
- `.claude/config.json` - Added CodeRabbit integration settings
- `.claude/commands/pr-feedback.md` - New command
- `package.json` - Version bump to 2.3.4
- Multiple documentation files updated

See [RELEASE_NOTES_v2.3.4.md](RELEASE_NOTES_v2.3.4.md) for full details.

## [2.3.3] - January 2025

### 🪝 Hook System Enhancements

Added three powerful enhancements based on advanced patterns from the Claude hooks ecosystem.

#### New Features
- **PreCompact Hook Support** - Preserves context during conversation compaction
  - Automatically saves critical files before compaction
  - Integrates with `/sr` for seamless restoration
  - Solves "4-hour session amnesia" problem

- **Command Suggestion Engine** - Educational corrections for design violations
  - Maps violations to specific corrections
  - Tracks patterns and shows common mistakes
  - Categories: typography, spacing, accessibility, color

- **Structured Command Logging** - Queryable command history
  - Logs all commands with timing and results
  - `/query-logs` command for analytics
  - Shows usage statistics and performance insights

- **Implementation Guide Hook** - Prevents common AI mistakes
  - Detects potential duplicate files before creation
  - Identifies overlapping functionality with existing systems
  - Suggests better approaches and required updates
  - Embodies "analyze, recommend, revise" pattern

#### New Commands
- `/query-logs` - Query command history and analytics
- `/check-work` - Quick implementation quality check

#### Files Added
- `.claude/hooks/notification/01-precompact-handler.py`
- `.claude/utils/suggestion_engine.py`
- `.claude/hooks/post-tool-use/03-command-logger.py`
- `.claude/hooks/pre-tool-use/15-implementation-guide.py`
- `.claude/commands/query-logs`
- `.claude/commands/check-work.md`

See [RELEASE_NOTES_v2.3.3.md](RELEASE_NOTES_v2.3.3.md) for full details.

## [2.3.2] - January 2025

### 🤖 GitHub Apps Integration

Added comprehensive AI-powered code review capabilities through GitHub Apps integration.

#### New Features
- **CodeRabbit Integration** - AI code reviews that catch 95%+ of bugs
  - Automatic PR reviews within 2-3 minutes
  - Line-by-line suggestions with one-click fixes
  - Learns from team corrections and adapts
  - $24/developer/month Pro plan

- **Claude Code GitHub App** - PRD alignment and AI assistance
  - Validates implementation against PRDs
  - Included with Claude Max plan ($200/month)
  - Deep integration with existing commands
  - No additional API costs

- **Smart Repository Setup** - Prevents common configuration errors
  - New `scripts/quick-setup.sh` automates repo configuration
  - Enhanced `/init-project` verifies correct repository
  - Enhanced `/gi` prevents creating issues in boilerplate repo
  - Clear error messages guide proper setup

#### New Files
- `.coderabbit.yaml` - CodeRabbit configuration with design system rules
- `scripts/quick-setup.sh` - Automated repository setup
- `scripts/add-to-existing.sh` - Add to existing projects
- `docs/setup/DAY_1_COMPLETE_GUIDE.md` - Comprehensive setup with GitHub Apps
- `docs/updates/GITHUB_APPS_INTEGRATION.md` - Integration documentation

#### Enhanced Commands
- `/init-project` - Now checks repository configuration and GitHub Apps
- `/gi` - Verifies target repository before creating issues

#### Configuration
- `.claude/project-config.json` - Tracks repository and GitHub Apps status
- Custom CodeRabbit rules enforce design system automatically

#### Benefits
- 86% faster code delivery (Anthropic case study)
- 60% reduction in code review issues
- Automated bug detection before PR merge
- Continuous learning from team practices

## [2.3.0] - January 2025

### 🌟 Grove-Inspired Enhancements

Based on Sean Grove's "The New Code" talk from OpenAI, treating specifications as primary artifacts:

#### New Features
- **PRD Clarity Linter** - Automatically detects ambiguous language
  - Catches terms like "fast", "secure", "optimal"
  - Suggests specific, measurable alternatives
  - Context-aware (stricter in requirements sections)
  - Non-blocking warnings by default

- **Specification Pattern Library** (`/specs`)
  - Extract patterns from successful implementations
  - Auto-tags by type (auth, forms, API, etc.)
  - Track success metrics
  - Apply patterns to new features

- **PRD Test Generation** (`/prd-tests`)
  - Convert acceptance criteria to executable tests
  - Generate unit, integration, and E2E tests
  - Link tests back to PRD sections
  - Track coverage of requirements

- **Implementation Grading** (`/grade`)
  - Score code alignment with PRD (0-100%)
  - Breakdown by category (functional, testing, design)
  - Track improvement over time
  - Export detailed reports

#### Philosophy
- **80-90% of value is communication, not code**
- **Specifications are the "source code"**
- **Code is a "lossy projection" of intent**
- **Clear communication = effective programming**

#### Configuration
All Grove enhancements configurable in `.claude/config.json` under `grove_enhancements`

## [2.2.0] - January 2025

### 🎯 Context Management & Workflow Enhancements

Based on analysis of advanced context engineering workflows:

#### New Commands
- **`/bug-track` (bt)** - Persistent bug tracking across sessions
  - Automatically syncs to GitHub gists
  - Links bugs to specific files and lines
  - Tracks resolution history
  - Integrated with error detection hooks

- **`/context-profile` (cp)** - Manage focused context profiles
  - Create work-specific profiles (frontend, backend, debug)
  - Switch contexts without losing work
  - Presets for common workflows
  - Shows context window usage

- **`/doc-cache` (dc)** - Cache external documentation locally
  - Works with `/research-docs` to cache results
  - Offline access to documentation
  - Searchable index of cached content
  - Auto-cleanup of stale docs

- **`/stage-validate` (sv)** - Enforce stage completion gates
  - Automated validation of PRD phases
  - Blocks progression until criteria met
  - Integration with task system
  - Override with documented reasons

#### Enhanced PRD System
- **Stage Gates**: Each PRD phase now has exit criteria
- **Context Management Plan**: PRDs suggest context profiles
- **Documentation Requirements**: Auto-cache relevant docs

#### Why These Changes
- **Never lose bugs**: Persistent tracking across all sessions
- **Focused work**: Context profiles prevent overload
- **Work offline**: Cached documentation always available
- **Quality gates**: Ensure each phase is complete before moving on

### 📁 New Directory Structure
```
.claude/
  ├── bugs/            # Bug tracking persistence
  ├── profiles/        # Context profile storage
  │   └── presets/     # Built-in profiles
  └── doc-cache/       # Cached documentation
      └── sources/     # Original doc sources
```

### 📚 Documentation
- Added [NEW_FEATURES_SETUP.md](docs/setup/NEW_FEATURES_SETUP.md)
- Updated help command with new features
- Enhanced QUICK_REFERENCE.md
- Updated PRD template with stage gates

## [2.1.0] - January 2025

### 🎨 UI Design Enhancements

Based on analysis of SuperDesign and modern UI generation approaches:

#### New Commands
- **Enhanced `/create-component`**:
  - `--wireframe` flag: Start with ASCII wireframe for rapid layout validation
  - `--animate` flag: Plan micro-interactions before implementation
  - `--style=ref` flag: Use extracted style references
  
- **New `/extract-style` command**:
  - Extract design tokens from reference images/URLs
  - Automatically maps to our 4-size, 2-weight design system
  - Maintains 60/30/10 color distribution
  - Saves themes as version-controlled JSON

#### Design Workflow Improvements
- **Flow Engineering**: Layout → Style → Animation → Implementation
- **ASCII Wireframing**: 1-second layout validation before coding
- **Style Extraction**: From Dribbble, Behance, or any website
- **Animation Planning**: Define keyframes and triggers upfront

#### Why These Changes
- Prevents "AI-ish UI" through better design planning
- Maintains our strict design system enforcement
- Adds speed without compromising quality
- Optional enhancements - use only when helpful

### 📚 Documentation
- Updated `/create-component.md` with wireframe flow
- Added `/extract-style.md` command documentation
- Enhanced `NEW_CHAT_CONTEXT.md` with UI design workflow
- Updated `INITIAL.md` with design recommendations

## [2.0.0] - January 2025

### 🚀 Major Package Updates

#### Based on 2025 Ecosystem Research
- Comprehensive analysis of NPM downloads, GitHub activity, and community adoption
- See [PACKAGE_UPDATES_JAN_2025.md](./docs/technical/PACKAGE_UPDATES_JAN_2025.md) for detailed research

#### Performance Improvements
- **Added Turbopack**: `next dev --turbopack` for 76.7% faster development
- **Already using Biome**: 15x faster than ESLint
- **SWC**: Default compiler, 17x faster than Babel

#### New Dependencies
- **Authentication**:
  - `next-auth@^5.0.0-beta.25` - Auth.js v5 (1.4M weekly downloads)
  - `jose@^5.10.0` - JWT token handling
  
- **UI Components** (Radix UI primitives):
  - `@radix-ui/react-dialog@^1.1.0`
  - `@radix-ui/react-dropdown-menu@^2.1.0`
  - `@radix-ui/react-toast@^1.2.0`
  - `@radix-ui/react-select@^2.1.0`
  - `@radix-ui/react-checkbox@^1.1.0`
  - `@radix-ui/react-switch@^1.1.0`

- **Date Handling**:
  - `date-fns@^4.0.0` - Updated to v4 (34M weekly downloads)
  - `@date-fns/tz@^1.0.0` - Timezone support

- **Testing**:
  - `msw@^2.7.0` - API mocking (2.5M weekly downloads)
  - `@faker-js/faker@^9.9.0` - Test data generation

- **Developer Experience**:
  - `concurrently@^8.2.0` - Run multiple commands
  - `tsx@^4.19.0` - Execute TypeScript directly
  - `uuid@^11.0.0` - Updated to v11

#### Version Updates
- `drizzle-kit@^0.32.0` - Updated from 0.31.4
- `@biomejs/biome@2.1.1` - Fixed exact version
- `@testing-library/jest-dom@^6.6.3` - Fixed version
- `vitest@^3.2.4` - Updated to v3

### 📚 Documentation Updates

#### New Documentation
- [DEPENDENCY_MANAGEMENT.md](./docs/technical/DEPENDENCY_MANAGEMENT.md) - Complete dependency tracking
- [PACKAGE_UPDATES_JAN_2025.md](./docs/technical/PACKAGE_UPDATES_JAN_2025.md) - 2025 ecosystem research
- [PACKAGE_RECOMMENDATIONS.md](./docs/technical/PACKAGE_RECOMMENDATIONS.md) - Additional package options
- [COMMIT_CONTROL_GUIDE.md](./docs/team/COMMIT_CONTROL_GUIDE.md) - No auto-commit clarification
- [ADD_TO_EXISTING_PROJECT.md](./docs/setup/ADD_TO_EXISTING_PROJECT.md) - Add to existing projects

#### Updated Documentation
- README.md - Updated tech stack section
- SYSTEM_OVERVIEW.md - Comprehensive tech stack update
- NEW_CHAT_CONTEXT.md - Latest package information
- DAY_1_COMPLETE_GUIDE.md - Clarified no auto-commits

### 🛠️ New Features

#### Commands
- `/check-deps` - Check and update dependencies
- `/commit-review` - Safe commit with review
- `/git-status` - Check changes without risk
- `/facts` - View protected project values
- `/exists` - Check before creating
- `/field-generate` - Generate from field registry

#### Scripts
- `scripts/check-dependencies.ts` - Dependency version checker
- `scripts/add-to-existing.sh` - Add boilerplate to existing projects

#### Hooks
- `10-hydration-guard.py` - Prevent Next.js SSR errors
- `11-truth-enforcer.py` - Protect established values
- `12-deletion-guard.py` - Warn before deletions
- `13-import-validator.py` - Fix import paths

### 🔧 Configuration Updates
- `biome.json` - Updated schema for v2.1.1
- `.mcp.json` - Added development tool servers
- `package.json` - Major dependency overhaul

### 🎯 Philosophy Updates
- Lean boilerplate principle - only essential packages
- Evidence-based decisions using real NPM data
- Performance-first with Rust-based tooling
- Security by default with PII protection

## [1.0.0] - December 2024

### Initial Release
- PRD-driven development system
- 90+ custom commands
- Design system enforcement
- Context preservation
- Multi-agent orchestration
- Field registry for security
- Comprehensive documentation

---

## Version History

- **2.0.0** - January 2025: Major ecosystem update
- **1.0.0** - December 2024: Initial release
