# 🚀 Claude Code Quick Reference Card

## Starting Your Session
```bash
/sr                    # Smart Resume - Start here!
/help                  # Full command reference
/help new              # See latest features
```

## 🛡️ New Safety Features (Automatic)
- **Truth Enforcement** - Prevents changing established values
- **Deletion Guard** - Warns before removing code
- **Hydration Protection** - Catches Next.js SSR errors
- **Import Validation** - Fixes path issues

## Essential Daily Commands

### Before Creating Anything
```bash
/exists Button         # Check if already exists
/facts                 # See established values
/pc Button            # Pre-component check (chain)
```

### Development Flow
```bash
/cc ui Button          # Create component (validated)
/vd                    # Validate design
/chain safe-commit     # Before git commit
```

### PRD → Code Workflow
```bash
/prd feature           # Create PRD
/gt feature            # Generate tasks
/pt feature            # Process tasks
/btf feature           # Browser test
```

### Field Registry
```bash
/ctf ContactForm       # Create tracked form
/fg schemas            # Generate Zod schemas
/fg factories          # Generate test data
```

## 🔥 Quick Chains (New!)
```bash
/chain safe-commit     # Validate before commit
/chain field-sync      # Regenerate field code
/chain pre-component   # Check before creating
```

## 💡 Common Scenarios

### "I need to change an API route"
```bash
/truth-override "API v2 migration"
# Or include "refactor" in task name
```

### "Claude deleted my code!"
```bash
# Deletion guard will warn first
# Use git to restore if needed
```

### "Getting hydration errors"
```bash
# Hook catches automatically
# Shows how to fix with useEffect
```

### "Import paths are wrong"
```bash
# Hook warns and suggests fix
# Use @/ for root imports
```

## 🎯 Key Aliases
- `sr` → smart-resume
- `truth` → facts
- `check` → exists
- `fg` → field-generate
- `sc` → safe-commit (chain)
- `override` → truth-override

## 📊 What's Protected

Run `/facts` to see:
- API routes
- Component names
- Environment variables
- Database schema
- Type definitions

## 🚦 Hook Status Indicators

- 🚫 **Blocked** - Action prevented (must fix)
- ⚠️ **Warning** - Proceed with caution
- ✅ **Allowed** - Intentional change detected
- 📝 **Info** - FYI, no action needed

## 🆘 Quick Help
```bash
/help [command]        # Specific command help
/help workflows        # Complete workflows
/help new             # Latest features
```

Remember: The system prevents mistakes automatically. Focus on building!