# Integration Methods Documentation

## 🚀 Quick Reference: All Integration Methods

### Method 1: Complete Workflow (Recommended)
For integrating into an existing project from scratch.

```bash
# 1. Clone boilerplate locally
cd ~/dev/bfc
git clone https://github.com/bearingfruitco/cc-boiler-js-public.git boilerplate-master

# 2. In your project
cd ~/dev/bfc/your-project
git checkout -b integrate-boilerplate

# 3. Run integration
curl -sSL https://raw.githubusercontent.com/bearingfruitco/cc-boiler-js-public/main/scripts/integrate-from-local.sh | bash

# 4. Complete in Claude Code
claude .
# Follow prompts to merge .boilerplate files
```

**Documentation**: See `docs/setup/COMPLETE_INTEGRATION_WORKFLOW.md`

### Method 2: Local Integration Script
When you have the boilerplate cloned locally.

```bash
cd your-project
/path/to/boilerplate/scripts/integrate-from-local.sh full
```

Options:
- `full` - Complete integration
- `commands` - Just Claude commands  
- `design` - Just design system
- `security` - Just security features
- `prps` - Just PRPs

**Documentation**: See `docs/setup/INTEGRATION_GUIDE.md`

### Method 3: Integration Wizard (Interactive)
```bash
curl -sSL https://raw.githubusercontent.com/bearingfruitco/cc-boiler-js-public/main/scripts/integration-wizard.sh > wizard.sh
chmod +x wizard.sh
./wizard.sh
```

**Note**: Download first, then run (avoids stdin issues)

### Method 4: Quick Integration
```bash
curl -sSL https://raw.githubusercontent.com/bearingfruitco/cc-boiler-js-public/main/scripts/quick-integrate.sh | bash
```

## 📋 Integration Checklist

After any integration method:

- [ ] Run `/sr` in Claude Code
- [ ] Run `/help` to see 150+ commands
- [ ] Check design tokens in tailwind.config.js
- [ ] Verify `.claude/` directory structure
- [ ] Test `/agent list` shows 31 agents
- [ ] Merge any `.boilerplate` files
- [ ] Commit on a feature branch
- [ ] Create PR for review

## 🎯 Which Method to Use?

- **New to boilerplate?** → Method 1 (Complete Workflow)
- **Have local boilerplate?** → Method 2 (Local Script)
- **Want step-by-step guidance?** → Method 3 (Wizard)
- **Quick and simple?** → Method 4 (Quick Integration)

## 📚 Key Documentation Files

- `docs/setup/COMPLETE_INTEGRATION_WORKFLOW.md` - Full 30-minute process
- `docs/setup/INTEGRATION_GUIDE.md` - Local integration details
- `docs/setup/EXISTING_PROJECT_INTEGRATION.md` - Original integration guide
- `scripts/integrate-from-local.sh` - Main integration script
- `scripts/integration-wizard.sh` - Interactive wizard
- `scripts/quick-integrate.sh` - Quick download and run

## ⚡ Two-Phase Approach

All methods follow the same pattern:

**Phase 1: Script** (Automated)
- Copies files with backups
- Creates `.boilerplate` markers
- Non-destructive

**Phase 2: Claude Code** (Interactive)
- Reviews conflicts
- Shows diffs
- Merges intelligently
- Verifies everything

## 🔧 Troubleshooting

If integration fails:
1. Check backup directory `.integration-backup/`
2. Reset with `git reset --hard HEAD`
3. Try Method 1 (most reliable)
4. See troubleshooting in `COMPLETE_INTEGRATION_WORKFLOW.md`

## 💡 Pro Tips

1. Always work on a branch
2. Keep boilerplate cloned locally at `~/dev/bfc/boilerplate-master/`
3. Use Claude Code for merge conflicts
4. Test key commands before committing
5. Document any project-specific changes

---

For support, open an issue on GitHub or check the documentation in `/docs/setup/`.
