# 📝 Changelog

All notable changes to the Claude Code Boilerplate project.

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
