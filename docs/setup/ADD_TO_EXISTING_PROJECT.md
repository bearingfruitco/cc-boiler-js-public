# 🔧 Adding Claude Code Boilerplate to an Existing Project

This guide helps you upgrade an existing Claude Code project with our advanced features while preserving your work.

## 🎯 What This Guide Covers

- Adding boilerplate to a project already in motion
- Preserving existing PRDs and context
- Selective feature adoption
- Minimal disruption approach

## 📋 Pre-Installation Checklist

Before adding the boilerplate:

```bash
# 1. Commit current work
git add .
git commit -m "chore: Checkpoint before adding Claude boilerplate"

# 2. Note your current setup
ls -la .claude/  # See what Claude files you already have
```

## 🚀 Installation Options

### Option A: Full System (Recommended)
Get all features - hooks, commands, personas, security:

```bash
# 1. Download the boilerplate
curl -L https://github.com/bearingfruitco/claude-code-boilerplate/archive/main.zip -o boilerplate.zip
unzip boilerplate.zip

# 2. Copy core Claude files (preserves your existing work)
cp -r claude-code-boilerplate-main/boilerplate/.claude/* .claude/

# 3. Install hooks (IMPORTANT)
cd .claude/scripts
./install-hooks.sh
cd ../..

# 4. Copy security and tracking systems
cp -r claude-code-boilerplate-main/boilerplate/field-registry .
cp -r claude-code-boilerplate-main/boilerplate/lib/security lib/
cp -r claude-code-boilerplate-main/boilerplate/lib/forms lib/

# 5. Add package dependencies
cat claude-code-boilerplate-main/boilerplate/package.json | grep -A 20 '"dependencies"' >> package-merge.json
# Manually merge dependencies

# 6. Clean up
rm -rf claude-code-boilerplate-main boilerplate.zip
```

### Option B: Core Features Only
Just commands and basic automation:

```bash
# 1. Create directories if needed
mkdir -p .claude/{commands,hooks,scripts,team,checkpoints}

# 2. Download essential files directly
cd .claude

# Commands (90+ commands)
curl -L https://github.com/bearingfruitco/claude-code-boilerplate/archive/main.tar.gz | \
  tar -xz --strip=2 --wildcards "*/boilerplate/.claude/commands/*"

# Aliases and chains
curl -LO https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/boilerplate/.claude/aliases.json
curl -LO https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/boilerplate/.claude/chains.json

cd ..
```

### Option C: Manual Selection
Cherry-pick specific features:

```bash
# Just the commit control features for Nikki
mkdir -p .claude/commands
curl -LO https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/boilerplate/.claude/commands/commit-review.md
curl -LO https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/boilerplate/.claude/commands/git-status.md

# Just the PRD system
curl -LO https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/boilerplate/.claude/commands/create-prd.md
curl -LO https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/boilerplate/.claude/commands/generate-tasks.md
curl -LO https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/boilerplate/.claude/commands/process-tasks.md
```

## 📦 Preserving Your Existing Work

### 1. Tag Your Current PRD
If you already have a PRD or similar document:

```bash
# Create a reference to your existing PRD
mkdir -p docs/project/existing
mv YOUR_PRD.md docs/project/existing/ORIGINAL_PRD.md

# Tag it for the system
echo "---
status: active
created: $(date -I)
source: pre-boilerplate
---" > docs/project/existing/ORIGINAL_PRD.md.meta
```

### 2. Convert to System Format
```bash
# Use the command to import your PRD
/import-prd docs/project/existing/ORIGINAL_PRD.md
```

### 3. Preserve Context
```bash
# Save your current Claude context
cp .claude/recent_context.md .claude/pre-upgrade-context.md

# Merge with new context structure
/context-merge pre-upgrade-context.md
```

## 🎛️ Configuration

### Minimal config.json
If you don't have one, create `.claude/hooks/config.json`:

```json
{
  "github": {
    "auto_commit": false,
    "gist_visibility": "secret"
  },
  "hooks": {
    "pre-tool-use": [
      {
        "script": "02-design-check.py",
        "enabled": false
      }
    ]
  }
}
```

### Gradual Adoption
Start with features disabled, enable as needed:

```json
{
  "features": {
    "design_system_enforcement": false,
    "auto_pull": false,
    "pii_protection": true,
    "state_saves": true
  }
}
```

## 🔍 Verifying Installation

### Quick Check
```bash
# In Claude Code
/help              # Should show new commands
/checkpoint test   # Test state saving
/gs               # Test git status command
```

### Full Verification
```bash
# Run setup verification
python3 .claude/scripts/health-check.py

# Check specific features
ls -la .claude/commands/ | wc -l  # Should show 50+ commands
ls -la .claude/hooks/             # Should have pre/post directories
```

## 🚦 Activation Workflow

### Phase 1: Commands Only (Day 1)
```bash
# Just use the commands, no automation
/sr         # Smart resume
/checkpoint # Save state
/cr         # Commit review
```

### Phase 2: Add State Saving (Day 2)
```bash
# Enable state saves
# Edit .claude/hooks/config.json
"post-tool-use": [
  {
    "script": "01-state-save.py",
    "enabled": true
  }
]
```

### Phase 3: Add Safety Checks (Week 2)
```bash
# Enable select pre-hooks
"pre-tool-use": [
  {
    "script": "07-pii-protection.py",
    "enabled": true
  }
]
```

### Phase 4: Full System (When Ready)
```bash
# Enable all features
./claude/scripts/enable-all-features.sh
```

## 🆘 Troubleshooting

### Commands Not Found
```bash
# Reload aliases
cp .claude/aliases.json ~/.claude/aliases.json
# Restart Claude Code
```

### Hooks Not Running
```bash
# Check permissions
chmod +x .claude/hooks/**/*.py
chmod +x .claude/scripts/*.sh
```

### Conflicts with Existing Setup
```bash
# Backup and merge
mv .claude .claude-backup
# Copy new files
# Manually merge your customizations
```

## 📝 For Nikki's Specific Case

Since Nikki already has a project with a PRD:

```bash
# 1. Add just what she needs first
mkdir -p .claude/commands
cd .claude/commands

# Get commit control
curl -LO https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/boilerplate/.claude/commands/commit-review.md
curl -LO https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/boilerplate/.claude/commands/git-status.md
curl -LO https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/boilerplate/.claude/commands/checkpoint.md

# Get smart resume for context
curl -LO https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/boilerplate/.claude/commands/smart-resume.md

# Get aliases
cd ..
curl -LO https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/boilerplate/.claude/aliases.json

# 2. Tag her existing PRD
mkdir -p ../docs/project
echo "# Nikki's Original PRD
$(cat PATH_TO_HER_PRD)" > ../docs/project/ACTIVE_PRD.md

# 3. She can now use:
/gs                    # Check status safely
/cr "message"          # Commit with review
/checkpoint            # Save state
/sr                    # Resume with context
```

## 🎯 Success Criteria

You'll know it's working when:
- ✅ `/help` shows new commands
- ✅ `/checkpoint` saves without errors
- ✅ `/gs` shows git status
- ✅ State saves appear in `.claude/checkpoints/`
- ✅ No unwanted auto-commits happen

## 💡 Best Practices

1. **Start Small** - Add features gradually
2. **Test First** - Try commands in a test branch
3. **Keep Backups** - Always backup `.claude/` before changes
4. **Document Changes** - Note what you've customized

## 🔗 Next Steps

After installation:
1. Read `/docs/team/COMMIT_CONTROL_GUIDE.md`
2. Try `/help` to see all commands
3. Use `/checkpoint` frequently
4. Work with confidence - you're in control!

---

Remember: The boilerplate is designed to enhance, not replace, your workflow. Take what helps, leave what doesn't!
