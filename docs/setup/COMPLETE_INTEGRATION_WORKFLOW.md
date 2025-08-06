# Complete Boilerplate Integration Workflow - From Zero to Hero

## 📋 Prerequisites
- An existing project that needs the boilerplate
- Claude Code installed
- Git access to both repos

## 🚀 Complete Integration Process

### Phase 1: Initial Setup (5 minutes)

#### Step 1: Clone Your Project
```bash
# Go to your development directory
cd ~/dev/bfc

# Clone your existing project (if not already local)
git clone [your-project-repo] my-project
cd my-project
```

#### Step 2: Clone the Boilerplate Locally
```bash
# Go back to your bfc directory
cd ~/dev/bfc

# Clone the boilerplate for reference
git clone https://github.com/bearingfruitco/cc-boiler-js-public.git boilerplate-master

# This gives you a permanent local copy at ~/dev/bfc/boilerplate-master
```

#### Step 3: Create Integration Branch
```bash
# Go back to your project
cd ~/dev/bfc/my-project

# Create a new branch for integration
git checkout -b integrate-boilerplate

# Verify you're on the new branch
git branch
```

### Phase 2: Initial Integration Script (2 minutes)

#### Step 4: Download Integration Script
```bash
# Get the integration script from boilerplate
cp ~/dev/bfc/boilerplate-master/scripts/integrate-from-local.sh ./integrate-boilerplate.sh
chmod +x ./integrate-boilerplate.sh

# Or create it directly:
cat > integrate-boilerplate.sh << 'EOF'
#!/bin/bash
set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

BOILERPLATE_DIR="$HOME/dev/bfc/boilerplate-master"
BACKUP_DIR=".integration-backup/$(date +%Y%m%d_%H%M%S)"

echo -e "${CYAN}Starting Boilerplate Integration${NC}"
echo "Source: $BOILERPLATE_DIR"
echo "Target: $(pwd)"
echo ""

# Create backup
mkdir -p "$BACKUP_DIR"

# Backup existing files
for file in .claude CLAUDE.md tailwind.config.js tsconfig.json biome.json; do
  if [ -e "$file" ]; then
    cp -r "$file" "$BACKUP_DIR/"
    echo "Backed up: $file"
  fi
done

# Copy .claude directory
if [ -d "$BOILERPLATE_DIR/.claude" ]; then
  if [ -d ".claude" ]; then
    rsync -av --backup --suffix="-original" "$BOILERPLATE_DIR/.claude/" ".claude/"
  else
    cp -r "$BOILERPLATE_DIR/.claude" .
  fi
  echo -e "${GREEN}✓ Integrated .claude directory${NC}"
fi

# Copy other essential directories
for dir in PRPs field-registry; do
  if [ ! -d "$dir" ] && [ -d "$BOILERPLATE_DIR/$dir" ]; then
    cp -r "$BOILERPLATE_DIR/$dir" .
    echo -e "${GREEN}✓ Added $dir${NC}"
  fi
done

# Create .boilerplate versions for configs
for file in CLAUDE.md tailwind.config.js tsconfig.json biome.json; do
  if [ -f "$BOILERPLATE_DIR/$file" ]; then
    if [ -f "$file" ]; then
      cp "$BOILERPLATE_DIR/$file" "${file}.boilerplate"
      echo -e "${YELLOW}Created ${file}.boilerplate for review${NC}"
    else
      cp "$BOILERPLATE_DIR/$file" "$file"
      echo -e "${GREEN}✓ Added $file${NC}"
    fi
  fi
done

echo ""
echo -e "${GREEN}Initial integration complete!${NC}"
echo "Backups saved to: $BACKUP_DIR"
echo ""
echo "Next: Open Claude Code to complete the merge"
EOF

chmod +x integrate-boilerplate.sh
```

#### Step 5: Run Initial Integration
```bash
# Run the script
./integrate-boilerplate.sh

# Check what was created
ls -la *.boilerplate
ls -la .claude
ls -la PRPs
```

### Phase 3: Open Claude Code for Smart Merging (10-15 minutes)

#### Step 6: Start Claude Code
```bash
# In your project directory
claude .
```

#### Step 7: Give Claude Code the Integration Task

In Claude Code, paste this instruction:

```
I need to complete the integration of Claude Code Boilerplate v4.0.0 into this project.

Current situation:
1. The boilerplate source is at: ~/dev/bfc/boilerplate-master/
2. I have .boilerplate files that need intelligent merging
3. The .claude directory has been initially copied but may need updates

Please help me:

STEP 1: Analyze what needs merging
- List all .boilerplate files
- Show me the count of commands, agents, and hooks currently present
- Compare with what's in the source boilerplate

STEP 2: For each .boilerplate file, show me:
- A diff between the current file and the .boilerplate version
- Your recommendation for merging (keep current, use boilerplate, or combine)
- The proposed merged result

STEP 3: Handle special merges:
- CLAUDE.md: Combine project-specific + boilerplate instructions
- tailwind.config.js: Ensure design tokens are added (text-size-1 through 4)
- tsconfig.json: Ensure path aliases are present
- biome.json: Use working version (probably current)

STEP 4: Verify nothing is missing:
- Check all commands from boilerplate are present
- Check all agents are copied
- Check hooks are properly installed
- Check config files in .claude/config/

STEP 5: Create verification tests

Show me each step and wait for my approval before making changes.
```

### Phase 4: Claude Code Integration Process

Claude Code will now:

#### Step 8: Analysis Phase
```bash
# Claude will run something like:
echo "=== Current State ==="
echo "Commands: $(ls .claude/commands/*.md 2>/dev/null | wc -l)"
echo "Agents: $(ls .claude/agents/*.md 2>/dev/null | wc -l)"
echo "Hooks: $(find .claude/hooks -name "*.py" 2>/dev/null | wc -l)"

echo -e "\n=== Boilerplate Has ==="
echo "Commands: $(ls ~/dev/bfc/boilerplate-master/.claude/commands/*.md | wc -l)"
echo "Agents: $(ls ~/dev/bfc/boilerplate-master/.claude/agents/*.md | wc -l)"

echo -e "\n=== Files to Merge ==="
ls -la *.boilerplate
```

#### Step 9: Diff Review Phase
Claude will show you diffs like:
```bash
# For CLAUDE.md
diff -u CLAUDE.md CLAUDE.md.boilerplate | head -50

# For tailwind.config.js
diff -u tailwind.config.js tailwind.config.js.boilerplate | grep -A 10 -B 10 "fontSize"
```

#### Step 10: Merge Execution Phase
After your approval, Claude will:
```bash
# Merge CLAUDE.md
cat > CLAUDE.md << 'EOF'
[Combined content with both project-specific and boilerplate sections]
EOF

# Add design tokens to tailwind.config.js
# Add path aliases to tsconfig.json
# etc.
```

#### Step 11: Verification Phase
```bash
# Test critical commands
for cmd in sr help agent chain prp fw; do
  test -f ".claude/commands/$cmd.md" && echo "✓ /$cmd present" || echo "✗ /$cmd missing"
done

# Test in Claude Code
/sr
/help
/analyze-existing
```

### Phase 5: Finalization (5 minutes)

#### Step 12: Clean Up
```bash
# After verification, remove .boilerplate files
rm -f *.boilerplate

# Remove any backup files if everything works
rm -f .claude/**/*-original

# Check git status
git status
```

#### Step 13: Commit Integration
```bash
# Stage all changes
git add -A

# Commit with detailed message
git commit -m "feat: integrate Claude Code Boilerplate v4.0.0

- Added 150+ Claude commands
- Added 31 specialized AI agents  
- Integrated hooks system for automation
- Added PRPs for one-pass implementation
- Integrated design system (4 sizes, 2 weights)
- Added field registry for security
- Merged configuration files
- Combined CLAUDE.md instructions"

# Push the branch
git push origin integrate-boilerplate
```

#### Step 14: Create PR
```bash
# Create a pull request for review
gh pr create --title "Integrate Claude Code Boilerplate v4.0.0" \
  --body "This PR integrates the complete Claude Code Boilerplate system into the project.

## Changes
- Added .claude directory with commands, agents, hooks
- Integrated PRPs and field-registry
- Updated configuration files with design tokens
- Merged CLAUDE.md instructions

## Testing
- [x] /sr command works
- [x] /help shows 150+ commands
- [x] Design tokens present in tailwind
- [x] All agents accessible
- [x] Hooks functioning

## Notes
All existing functionality preserved. Boilerplate additions are non-destructive."
```

### Phase 6: Post-Integration Testing

#### Step 15: Test Everything
In Claude Code:
```
/sr                    # Load context
/help                  # View all commands
/agent list           # See all agents
/chain                # View chains
/analyze-existing full # Analyze the integrated project
```

## 📊 Time Estimate

- Phase 1 (Setup): 5 minutes
- Phase 2 (Initial Script): 2 minutes  
- Phase 3-4 (Claude Code): 10-15 minutes
- Phase 5 (Finalization): 5 minutes
- **Total: ~30 minutes**

## 🎯 Success Criteria

After completion, you should have:
- ✅ 150+ working commands in Claude Code
- ✅ 31 specialized agents available
- ✅ Hooks system operational
- ✅ PRPs directory for structured development
- ✅ Design system integrated (text-size-1 through 4)
- ✅ Combined CLAUDE.md with all instructions
- ✅ Clean git history with PR ready
- ✅ No broken functionality
- ✅ Full boilerplate features available

## 🔥 Pro Tips

1. **Always work on a branch** - Never integrate directly on main
2. **Run the script first** - Gets 80% done automatically
3. **Let Claude Code handle merges** - It can show diffs and merge intelligently
4. **Test before committing** - Verify key commands work
5. **Keep the boilerplate-master** - Local reference is always useful

## 🆘 Troubleshooting

If something goes wrong:
```bash
# Restore from backup
cp -r .integration-backup/[date]/* .

# Or reset to branch start
git reset --hard HEAD

# Or checkout original files
git checkout main -- CLAUDE.md tailwind.config.js
```

This is the complete, professional way to integrate the boilerplate into any existing project!