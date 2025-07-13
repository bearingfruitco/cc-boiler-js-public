# New Chat Context - Claude Code Boilerplate v2.3.2

## 🆕 What's New in v2.3.2

### GitHub Apps Integration
- **CodeRabbit**: AI code reviews on every PR (catches 95%+ bugs)
- **Claude Code App**: PRD alignment validation (included with Max plan)
- **Smart Setup**: New `scripts/quick-setup.sh` prevents repo confusion
- **Enhanced Commands**: `/init-project` and `/gi` now verify correct repository

## 🚀 Quick Start

You're working with an advanced AI-assisted development system that treats specifications (PRDs) as the primary development artifact. This follows Sean Grove's "The New Code" philosophy.

### First Commands
```bash
/sr                    # Smart Resume - restores full context
/help new              # See latest features
/cp load [profile]     # Load focused context
```

## 🌟 Latest Features

### GitHub Apps Integration (v2.3.2)
- **CodeRabbit + Claude Code** for comprehensive AI reviews
- **Repository safety** - can't accidentally pollute boilerplate repo
- **Automated setup** - one script configures everything
- **Design enforcement** - AI learns and enforces your rules

### Workflow Enhancement (v2.3.1)
- **Smart Auto-Approval** - No more "Can I edit this file?" interruptions!
  - Read operations proceed automatically
  - Test file edits auto-approved
  - Safe commands (lint, test) run without prompts
  - Production code still protected

### Grove-Inspired Enhancements (v2.3.0)
1. **PRD Clarity Linter** - Catches ambiguous language automatically
2. **Specification Patterns** - Extract/reuse successful implementations (`/specs`)
3. **Test Generation** - PRD acceptance criteria → tests (`/prd-tests`)
4. **Implementation Grading** - Score alignment with PRD (`/grade`)

### Context Management (v2.2.0)
- **Context Profiles** - Focused work modes (`/cp`)
- **Bug Tracking** - Persistent across sessions (`/bt`)
- **Doc Cache** - Offline documentation (`/dc`)
- **Stage Gates** - Enforce completion (`/sv`)

## 🎯 Core Workflow

```
IDEA → /init-project → /prd → /gt → /pt → /grade → /fw complete
```

1. **Define** specifications clearly (PRD)
2. **Generate** tests from acceptance criteria
3. **Implement** through micro-tasks
4. **Grade** alignment with original intent
5. **Extract** patterns for future reuse

## 📋 Essential Commands

### Daily Development
```bash
/sr                    # Resume where you left off
/fw start [#]          # Start GitHub issue
/prd [name]            # Create specification
/prd-tests [name]      # Generate test suite
/gt [name]             # Generate tasks
/pt [name]             # Process tasks
/grade                 # Check alignment
/specs extract         # Save successful pattern
```

### Quality & Safety
```bash
/vd                    # Validate design
/sv check              # Stage validation
/facts                 # Protected values
/exists [name]         # Check before creating
/bt add "bug"          # Track bugs
```

## 🛡️ Automatic Protections

The system automatically:
- **Approves** safe operations (no more waiting!)
- **Blocks** design violations (wrong CSS classes)
- **Warns** about ambiguous PRD language
- **Saves** context every 60 seconds
- **Prevents** PII exposure
- **Tracks** bugs persistently
- **Grades** implementation quality

## 💡 Key Principles

1. **Specifications are primary** - PRDs drive everything
2. **Clear communication** - Ambiguity is the enemy
3. **Automated enforcement** - Hooks handle compliance
4. **Pattern learning** - Success builds on success
5. **Objective quality** - Measurable alignment

## 🔑 Quick Reference

```
SPECIFICATIONS          DEVELOPMENT            QUALITY
/prd    - create       /cc  - component       /grade  - alignment
/specs  - patterns     /vd  - design check    /sv     - stages
/prd-tests - tests     /bt  - bug track       /btf    - browser

CONTEXT                COLLABORATION          HELP
/sr     - resume       /fw  - workflow        /help new
/cp     - profiles     /orch - agents         /help [cmd]
/dc     - doc cache    /team - status         /?
```

## 📁 Key Files

- `CLAUDE.md` - AI agent instructions
- `QUICK_REFERENCE.md` - All commands
- `docs/updates/GROVE_ENHANCEMENTS.md` - New features
- `.claude/config.json` - System configuration

## 🎨 Design System

**Enforced automatically:**
- Font sizes: `text-size-1` through `text-size-4` only
- Font weights: `font-regular`, `font-semibold` only
- Spacing: 4px grid (p-1, p-2, p-3, p-4, p-6, p-8)
- Colors: 60% neutral, 30% primary, 10% accent

## 🚦 Getting Help

```bash
/help              # Context-aware help
/help new          # Latest features
/help workflows    # Common patterns
/help [command]    # Specific command
```

## 💭 Philosophy

> "The person who communicates most effectively is the most valuable programmer." - Sean Grove

This system helps you:
- Write clear specifications
- Generate code from intent
- Measure alignment objectively
- Learn from successes
- Collaborate seamlessly

Ready to start? Try `/init-project` or `/sr` to resume existing work!
