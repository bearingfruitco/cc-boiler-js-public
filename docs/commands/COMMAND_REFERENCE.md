# Claude Code Boilerplate Command Reference v4.0.0

> Complete reference for all 116+ commands in the Claude Code Boilerplate system.

## ? Table of Contents

1. [Quick Reference](#quick-reference)
2. [Core Commands](#core-commands)
3. [Development Commands](#development-commands)
4. [Testing Commands](#testing-commands)
5. [PRP/PRD Commands](#prpprd-commands)
6. [Agent & Orchestration](#agent--orchestration)
7. [Design System](#design-system)
8. [Security Commands](#security-commands)
9. [Git & Version Control](#git--version-control)
10. [Utility Commands](#utility-commands)
11. [Analytics & Monitoring](#analytics--monitoring)
12. [Documentation](#documentation)
13. [Deployment](#deployment)
14. [Troubleshooting](#troubleshooting)

## Quick Reference

### Most Used Commands

| Command | Alias | Purpose |
|---------|-------|---------|
| `/smart-resume` | `/sr` | Resume work with full context |
| `/create-component` | `/cc` | Create component with TDD |
| `/validate-design` | `/vd` | Check design compliance |
| `/test-runner` | `/tr` | Run tests |
| `/feature-workflow` | `/fw` | Manage feature development |
| `/orchestrate` | `/orch` | Coordinate multiple agents |
| `/chain` | - | Run automated workflows |
| `/checkpoint` | `/cp` | Save/restore work state |
| `/process-tasks` | `/pt` | Work through tasks |
| `/help` | `/h` | Get contextual help |

### Command Patterns

- **Aliases**: Most commands have short aliases (e.g., `/sr` for `/smart-resume`)
- **Arguments**: Use `$ARGUMENTS` in commands (e.g., `/cc Button --animate`)
- **Options**: Many commands support flags (e.g., `--fix`, `--verbose`, `--dry-run`)
- **Chaining**: Commands can be chained with `/chain [workflow-name]`

## Core Commands

### `/smart-resume` (alias: `/sr`)
**Purpose**: Intelligently resume work with full context awareness

**Syntax**: `/sr [quick|full|auto]`

**Options**:
- `quick` - Fast resume for short breaks (<1 hour)
- `full` - Complete context restoration
- `auto` - Automatically determine (default)

**Example**:
```bash
/sr              # Auto-detect what you need
/sr quick        # Just show current location
/sr full         # Search everywhere, rebuild context
```

**Features**:
- Detects current branch and issue
- Restores from GitHub gists
- Shows recent activity
- Suggests next actions
- TDD status check
- Branch awareness

---

### `/checkpoint` (alias: `/cp`)
**Purpose**: Create and manage work checkpoints

**Syntax**: `/checkpoint [create|restore|list] [name]`

**Commands**:
- `create [name]` - Save current state
- `restore [name]` - Restore to checkpoint
- `list` - Show all checkpoints
- `save` - Quick save with auto-name
- `load [profile]` - Load a context profile

**Example**:
```bash
/checkpoint create pre-refactor
/checkpoint restore pre-refactor
/checkpoint list
/cp save "working on auth"
```

---

### `/context-profile` (alias: `/cp` when used with profiles)
**Purpose**: Manage focused work contexts

**Syntax**: `/cp [create|load|save] [profile-name]`

**Profiles**:
- `frontend` - UI/UX focused context
- `backend` - API/server context
- `fullstack` - Complete context
- `debug` - Troubleshooting context
- Custom profiles

**Example**:
```bash
/cp load frontend       # Load frontend profile
/cp create payment-api  # Create custom profile
/cp save               # Save current to active profile
```

---

### `/help` (alias: `/h`, `/?`)
**Purpose**: Get contextual help and guidance

**Syntax**: `/help [topic|command]`

**Topics**:
- Commands
- Workflows
- Design system
- Testing
- Security
- Deployment

**Example**:
```bash
/help              # General help
/help tdd          # TDD workflow help
/help /cc          # Help for specific command
/?                 # Quick help
```

## Development Commands

### `/create-component` (alias: `/cc`)
**Purpose**: Create components with TDD and browser verification

**Syntax**: `/cc [type] [name] [options]`

**Types**:
- `ui` - UI components
- `form` - Form components
- `feature` - Feature components
- `layout` - Layout components

**Options**:
- `--wireframe` - Start with ASCII wireframe
- `--animate` - Include animations
- `--no-tdd` - Skip tests (not recommended)
- `--no-browser` - Skip browser tests
- `--browser-only` - Only browser tests

**Example**:
```bash
/cc ui Button
/cc form LoginForm --animate
/cc feature Dashboard --wireframe
```

**Workflow**:
1. Generates tests first (TDD)
2. Creates browser tests
3. Implements component
4. Verifies in browser
5. Captures screenshot

---

### `/validate-design` (alias: `/vd`)
**Purpose**: Check design system compliance

**Syntax**: `/vd [scope] [options]`

**Scopes**:
- `current` - Current file only
- `all` - All component files
- `staged` - Staged files only
- `[file]` - Specific file

**Options**:
- `--fix` - Auto-fix violations
- `--strict` - Strictest checking
- `--report` - Generate report

**Example**:
```bash
/vd                    # Current context
/vd all --fix          # Fix all violations
/vd components/Button  # Specific file
```

**Checks**:
- Font sizes (text-size-[1-4])
- Font weights (regular, semibold)
- Spacing (4px grid)
- Touch targets (44px min)
- Color distribution (60/30/10)

---

### `/generate-tasks` (alias: `/gt`)
**Purpose**: Break down features into micro-tasks

**Syntax**: `/gt [feature|issue]`

**Example**:
```bash
/gt authentication     # From feature name
/gt "#123"            # From issue number
/gt                   # From current context
```

**Output**:
- Numbered task list
- Time estimates
- Dependencies
- Suggested order

---

### `/process-tasks` (alias: `/pt`)
**Purpose**: Work through tasks systematically

**Syntax**: `/pt [feature] [options]`

**Options**:
- `--continue` - Resume from last
- `--task=[n]` - Specific task
- `--verify` - Verify each step

**Example**:
```bash
/pt authentication
/pt --continue
/pt --task=3 --verify
```

## Testing Commands

### `/test-runner` (alias: `/tr`)
**Purpose**: Run tests with intelligent detection

**Syntax**: `/tr [scope] [options]`

**Scopes**:
- `all` - All tests
- `current` - Current file's tests
- `changed` - Changed files only
- `failed` - Previously failed
- `[pattern]` - Match pattern

**Options**:
- `--watch` - Watch mode
- `--coverage` - With coverage
- `--update` - Update snapshots
- `--bail` - Stop on first fail

**Example**:
```bash
/tr                    # Smart detection
/tr all --coverage     # Full test suite
/tr Button            # Specific component
/tr changed           # Only changes
```

---

### `/tdd` (alias: `/test`)
**Purpose**: Test-driven development workflow

**Syntax**: `/tdd [component] [options]`

**Commands**:
- `/tdd [name]` - Generate tests for component
- `/tdd-dashboard` - View TDD metrics
- `/tdd-workflow` - Full TDD guide
- `/tdd-status` - Current TDD status

**Example**:
```bash
/tdd Button           # Generate Button tests
/tdd-dashboard       # See TDD progress
/tdds                # Quick status
```

**Workflow**:
1. Write failing tests
2. Implement minimal code
3. Make tests pass
4. Refactor safely

---

### `/browser-test-flow` (alias: `/btf`)
**Purpose**: Browser-based testing workflow

**Syntax**: `/btf [component] [options]`

**Commands**:
- `/pw-verify` - Verify in browser
- `/pw-console` - Check console
- `/pw-screenshot` - Capture screenshot
- `/pw-a11y` - Accessibility test

**Example**:
```bash
/btf LoginForm        # Full browser test
/pw-verify           # Quick verification
/pw-console          # Console errors
```

## PRP/PRD Commands

### `/create-prp`
**Purpose**: Create Product Requirement Prompt for one-pass implementation

**Syntax**: `/create-prp [feature] [options]`

**Options**:
- `--from-prd` - Convert from PRD
- `--template=[type]` - Use template
- `--ai-docs` - Include AI docs

**Example**:
```bash
/create-prp user-authentication
/create-prp --from-prd="#123"
/prp-create payment-flow --template=typescript
```

**Output**:
- Complete implementation guide
- Code patterns from codebase
- Database schemas
- API endpoints
- UI components
- Test scenarios

---

### `/prp-execute` (alias: `/prp-exec`)
**Purpose**: Execute PRP validation at different levels

**Syntax**: `/prp-execute [name] --level=[1-4] [options]`

**Levels**:
1. **Syntax & Standards** - Lint, TypeScript, design
2. **Component Testing** - Unit tests, hooks
3. **Integration Testing** - E2E, API, database
4. **Production Readiness** - Performance, security

**Options**:
- `--fix` - Auto-fix issues
- `--verbose` - Detailed output
- `--stop-on-error` - Halt on first error

**Example**:
```bash
/prp-execute auth --level=1        # Quick validation
/prp-execute auth --level=4 --fix  # Full validation with fixes
```

---

### `/create-prd`
**Purpose**: Create Product Requirement Document

**Syntax**: `/prd [feature] [options]`

**Options**:
- `--from-issue=[#]` - From GitHub issue
- `--template=[type]` - Use template
- `--async` - Include async requirements

**Example**:
```bash
/prd user-profile
/prd --from-issue=45
/prd-async notification-system
```

---

### `/prd-to-prp`
**Purpose**: Convert PRD to executable PRP

**Syntax**: `/prd-to-prp [prd-name]`

**Example**:
```bash
/prd-to-prp user-authentication
/convert-to-prp payment-flow
```

## Agent & Orchestration

### `/orchestrate` (alias: `/orch`)
**Purpose**: Coordinate multiple AI agents for complex tasks

**Syntax**: `/orch [task-description]`

**Agent Types**:
- Frontend specialists
- Backend engineers
- Security analysts
- Database architects
- QA engineers
- Performance experts

**Example**:
```bash
/orch implement complete authentication system
/orch optimize database performance
/orch security audit for payment flow
```

**Workflow**:
1. Analyzes task requirements
2. Selects appropriate agents
3. Coordinates execution
4. Synthesizes results

---

### `/spawn` (deprecated - use native agents)
**Purpose**: Legacy agent spawning (replaced by native agents)

**Migration**:
```bash
# Old way:
/spawn frontend

# New way:
Use the frontend agent to build the UI
```

---

### `/chain`
**Purpose**: Run automated workflow chains

**Syntax**: `/chain [workflow-name] [options]`

**Common Chains**:
- `morning-setup` - Daily startup routine
- `pre-pr` - Pre-PR validation
- `feature-complete` - Complete feature workflow
- `safe-commit` - Safe commit checks
- `architecture-design` - Full architecture
- `performance-optimization-v4` - Performance tuning

**Example**:
```bash
/chain morning-setup
/chain pre-pr
/chain feature-development-v4 --feature="shopping-cart"
```

---

### `/multi-agent` (alias: `/multi-review`)
**Purpose**: Get multiple agent perspectives simultaneously

**Syntax**: `/multi-agent [task]`

**Example**:
```bash
/multi-agent review authentication implementation
/multi-perspective-review
```

## Design System

### `/dmoff` / `/dmon`
**Purpose**: Toggle design system enforcement

**Syntax**: 
- `/dmoff` - Disable enforcement
- `/dmon` - Enable enforcement

**Example**:
```bash
/dmoff         # Temporarily disable
# ... work with any Tailwind classes ...
/dmon          # Re-enable strict mode
```

---

### `/strict-design`
**Purpose**: Enforce strictest design compliance

**Syntax**: `/strict-design [enable|disable]`

**Example**:
```bash
/strict-design enable
/migrate-to-strict-design analyze
```

---

### `/extract-style`
**Purpose**: Extract design patterns from existing code

**Syntax**: `/extract-style [component]`

**Example**:
```bash
/extract-style Button
/extract-style all --save
```

## Security Commands

### `/security-check` (alias: `/sc`)
**Purpose**: Run security validations

**Syntax**: `/security-check [scope] [options]`

**Scopes**:
- `all` - Complete check
- `api` - API endpoints
- `auth` - Authentication
- `deps` - Dependencies
- `form` - Form security

**Example**:
```bash
/security-check all
/sc api --fix
/security-audit
```

---

### `/create-secure-api` (alias: `/csa`)
**Purpose**: Create API with security built-in

**Syntax**: `/csa [endpoint-name]`

**Features**:
- Input validation
- Rate limiting
- Authentication
- CORS configuration
- Error handling

**Example**:
```bash
/csa user-profile
/create-secure-api payment
```

---

### `/generate-rls` (alias: `/rls`)
**Purpose**: Generate Row Level Security policies

**Syntax**: `/rls [table|all]`

**Example**:
```bash
/rls users
/rls all
/gen-rls --supabase
```

---

### `/pii`
**Purpose**: Manage PII field protection

**Syntax**: `/pii [scan|protect|audit]`

**Example**:
```bash
/pii scan              # Find PII fields
/pii protect email     # Protect field
/pii audit            # Full audit
```

## Git & Version Control

### `/feature-workflow` (alias: `/fw`)
**Purpose**: Manage feature development lifecycle

**Syntax**: `/fw [start|status|complete] [issue#]`

**Commands**:
- `start [#]` - Start new feature
- `status` - Current status
- `validate` - Run validations
- `complete` - Create PR

**Example**:
```bash
/fw start 123
/fw status
/fw complete
```

---

### `/branch-status` (alias: `/bs`)
**Purpose**: Smart branch management

**Syntax**: `/branch-status [options]`

**Features**:
- Active branches
- File conflicts
- Main sync status
- Protected features

**Example**:
```bash
/branch-status
/bs --clean
/branch-switch feature-123
```

---

### `/sync-main`
**Purpose**: Sync with main branch safely

**Syntax**: `/sync-main [options]`

**Options**:
- `--check` - Check only
- `--merge` - Auto-merge
- `--rebase` - Use rebase

**Example**:
```bash
/sync-main --check
/pull-main
```

## Utility Commands

### `/compress` (alias: `/compress-context`)
**Purpose**: Compress context when token limit approached

**Syntax**: `/compress [aggressive|smart|manual]`

**Example**:
```bash
/compress           # Smart compression
/compress aggressive # Maximum compression
/ctx-compress      # Alias
```

---

### `/todo`
**Purpose**: Manage TODO items

**Syntax**: `/todo [list|add|complete] [item]`

**Example**:
```bash
/todo list
/todo add "Fix auth bug"
/todo complete 3
```

---

### `/metrics`
**Purpose**: View productivity metrics

**Syntax**: `/metrics [report|dashboard|export]`

**Reports**:
- Commands used
- Time saved
- Code quality
- Test coverage
- Agent usage

**Example**:
```bash
/metrics dashboard
/show-metrics
/metrics export
```

---

### `/deps`
**Purpose**: Dependency management

**Syntax**: `/deps [check|scan|update] [component]`

**Features**:
- Find dependencies
- Check for issues
- Update tracking
- Circular detection

**Example**:
```bash
/deps check Button
/deps scan
/dependency-scan --production
```

## Analytics & Monitoring

### `/analytics`
**Purpose**: Analytics implementation and tracking

**Syntax**: `/analytics [setup|track|report]`

**Example**:
```bash
/analytics setup rudderstack
/analytics track event-name
/analytics report
```

---

### `/performance-monitor` (alias: `/pm`)
**Purpose**: Performance monitoring

**Syntax**: `/pm [check|baseline|compare]`

**Metrics**:
- Bundle size
- Load time
- Runtime performance
- Memory usage

**Example**:
```bash
/pm baseline          # Set baseline
/pm check            # Current metrics
/pm compare baseline # Compare to baseline
```

---

### `/monitor-v3`
**Purpose**: Real-time monitoring setup

**Syntax**: `/monitor-v3 [feature]`

**Example**:
```bash
/monitor-v3 enable
/release-monitor
```

## Documentation

### `/generate-docs` (alias: `/doc`)
**Purpose**: Generate documentation

**Syntax**: `/doc [scope] [options]`

**Scopes**:
- `api` - API documentation
- `components` - Component docs
- `architecture` - System docs
- `readme` - README files

**Example**:
```bash
/doc api
/generate-docs components
/api-doc
```

---

### `/research`
**Purpose**: Manage research documents

**Syntax**: `/research [create|update|list] [topic]`

**Example**:
```bash
/research create authentication-analysis
/research update
/research list
```

## Deployment

### `/deploy`
**Purpose**: Deployment management

**Syntax**: `/deploy [staging|production] [options]`

**Checks**:
- Environment variables
- Tests passing
- Security cleared
- Performance baseline

**Example**:
```bash
/deploy staging
/deploy-staging
/deploy production --dry-run
```

---

### `/env-validate`
**Purpose**: Validate environment configuration

**Syntax**: `/env-validate [environment]`

**Example**:
```bash
/env-validate
/env-switch production
/env-status
```

---

### `/vercel`
**Purpose**: Vercel-specific deployment

**Syntax**: `/vercel [deploy|preview|promote]`

**Example**:
```bash
/vercel preview
/vercel deploy
/production-preview
```

## Troubleshooting

### `/error-recovery` (alias: `/er`)
**Purpose**: Recover from errors

**Syntax**: `/er [deps|build|test]`

**Example**:
```bash
/error-recovery deps
/er build
```

---

### `/debug`
**Purpose**: Debug assistance

**Syntax**: `/debug [issue-description]`

**Features**:
- Stack trace analysis
- Variable inspection
- Performance profiling
- Memory leaks

**Example**:
```bash
/debug "button not clicking"
/analyze-deep error
```

---

### `/facts`
**Purpose**: Show protected facts/truths

**Syntax**: `/facts [category|all]`

**Categories**:
- `components` - UI components
- `api` - API endpoints
- `config` - Configuration
- `constants` - Constants

**Example**:
```bash
/facts all
/facts components
/truth
```

## Command Combinations

### Common Workflows

**Morning Start**:
```bash
/sr ? /chain morning-setup ? /fw status
```

**New Feature**:
```bash
/fw start 123 ? /create-prp ? /gt ? /pt
```

**Component Creation**:
```bash
/cc ui Button ? /vd ? /test ? /btf
```

**Pre-Commit**:
```bash
/chain pre-pr ? /fw complete
```

**Debugging**:
```bash
/debug ? /deps check ? /error-recovery
```

## Advanced Usage

### Command Flags

Most commands support common flags:
- `--dry-run` - Preview without changes
- `--verbose` - Detailed output
- `--quiet` - Minimal output
- `--fix` - Auto-fix issues
- `--force` - Skip confirmations

### Command Piping

Some commands can be piped:
```bash
/analyze | /create-prp | /prp-execute
```

### Batch Operations

Run multiple commands:
```bash
/chain "custom" --commands="sr,test,vd,fw complete"
```

## Getting Help

### Interactive Help
```bash
/help              # General help
/help [command]    # Command-specific help
/? [topic]        # Quick help
```

### Command Discovery
```bash
/chain list        # Available chains
/agent-health      # Agent status
/v4-status        # System status
```

### Examples
Most commands show examples when run without arguments:
```bash
/cc               # Shows usage examples
/chain            # Lists available chains
/metrics          # Shows available reports
```

## Best Practices

1. **Start with `/sr`** - Always resume context first
2. **Use aliases** - Faster workflow with shortcuts
3. **Chain commands** - Automate repetitive tasks
4. **Validate often** - `/vd` and `/test` frequently
5. **Create checkpoints** - Before major changes
6. **Use profiles** - Focused contexts for different work
7. **Trust automation** - Let hooks handle enforcement
8. **Document as you go** - `/research` for decisions

## Version Notes

This reference covers Claude Code Boilerplate v4.0.0 with:
- 116+ commands
- 31 specialized agents
- Multiple automation chains
- Comprehensive hook system
- Native Claude Code integration

For updates, run:
```bash
/boilerplate-sync
/v4-status
```

---

**Quick Start**: `/sr` ? `/help` ? Start coding!
**Need Help?**: `/help [topic]` or `/?`
**Report Issues**: `/capture-to-issue`
