# Boilerplate Sync

Synchronize your project with the latest boilerplate updates.

## Usage

```bash
/boilerplate-sync [--check-only] [--since=commit]
/bp-sync          # alias
```

## Options

- `--check-only`: Just show what would be updated, don't apply
- `--since=commit`: Show changes since specific commit
- `--selective`: Choose which updates to apply

## What This Does

1. **Identifies Boilerplate Updates**
   - Checks for new commands
   - Finds updated agents
   - Detects new hooks and scripts
   - Shows architecture enhancements

2. **Generates Update Report**
   - Lists all changes since last sync
   - Categorizes by type
   - Shows migration impact

3. **Selective Application**
   - Choose which updates to apply
   - Preserves project-specific changes
   - Handles conflicts gracefully

## Update Process

### Step 1: Check for Updates

```bash
/boilerplate-sync --check-only
```

Output:
```
Boilerplate Update Report
========================
Current Project Version: abc123
Latest Boilerplate Version: def456

New Commands Available:
- /create-architecture
- /validate-architecture
- /architecture-viz
- /generate-component-prps

New Agents:
- prp-writer

Updated Hooks:
- architecture-suggester.py

Continue with sync? (y/n)
```

### Step 2: Review Changes

The command will show:
- Commit history since last sync
- Files that will be updated
- Any potential conflicts

### Step 3: Apply Updates

Choose your update strategy:

#### Safe Update (Recommended)
```bash
# Only adds new files, doesn't overwrite
/boilerplate-sync --safe
```

#### Selective Update
```bash
# Choose specific components
/boilerplate-sync --selective
> [ ] Commands (5 new)
> [x] Agents (1 new)
> [x] Hooks (3 updated)
> [ ] Scripts
```

#### Full Sync (Caution!)
```bash
# Overwrites all boilerplate files
/boilerplate-sync --full
```

## Integration with debt-tofu-report

For the debt-tofu-report project specifically:

```bash
cd /path/to/debt-tofu-report

# Check what's new since project started
/boilerplate-sync --check-only --since=2024-01-01

# Apply architecture updates
/boilerplate-sync --selective
> [x] Architecture commands
> [x] PRP generation
> [ ] Other updates

# After sync, set up architecture
/create-architecture    # Now available!
/validate-architecture
/generate-component-prps
```

## Version Tracking

The system maintains version tracking in:
- `.claude/boilerplate-version.json` - Current version
- `.claude/last-sync.json` - Last sync details
- `BOILERPLATE_CHANGELOG.md` - Human-readable changes

## Manual Update Methods

If you prefer manual control:

### Cherry-pick Specific Commits
```bash
# Add boilerplate as remote
git remote add boilerplate https://github.com/[boilerplate-repo]
git fetch boilerplate

# Cherry-pick specific updates
git log boilerplate/main --oneline
git cherry-pick abc123  # Architecture update
git cherry-pick def456  # PRP writer agent
```

### Copy Specific Files
```bash
# Just copy what you need
cp ../boilerplate/.claude/commands/create-architecture.md .claude/commands/
cp ../boilerplate/scripts/validate-architecture.py scripts/
```

### Using rsync for Selective Sync
```bash
# Sync only commands
rsync -av ../boilerplate/.claude/commands/ .claude/commands/

# Sync everything except project-specific files
rsync -av --exclude='project-specific/*' ../boilerplate/.claude/ .claude/
```

## Best Practices

1. **Always Check First**
   ```bash
   /boilerplate-sync --check-only
   ```

2. **Backup Before Major Updates**
   ```bash
   cp -r .claude .claude.backup
   ```

3. **Test After Updates**
   ```bash
   /health-check
   /validate-commands
   ```

4. **Document Project-Specific Changes**
   Keep a `PROJECT_CUSTOMIZATIONS.md` to track your modifications

## Conflict Resolution

If you've modified boilerplate files:

1. **Automatic Detection**
   - System detects modified files
   - Shows diff before overwriting
   - Offers merge options

2. **Manual Resolution**
   ```bash
   # See what changed
   diff .claude/commands/example.md ../boilerplate/.claude/commands/example.md
   
   # Merge manually if needed
   git merge-file .claude/commands/example.md
   ```

## Recommended Workflow for debt-tofu-report

Since debt-tofu-report is already underway:

```bash
# 1. Check updates
/boilerplate-sync --check-only

# 2. Apply architecture system (highly recommended)
/boilerplate-sync --selective
Select: Architecture commands, PRP generation

# 3. Generate architecture from existing code
/analyze-existing              # Understand current structure
/create-architecture --from-existing  # Generate architecture docs
/validate-architecture        # Ensure completeness

# 4. Generate PRPs for remaining work
/generate-component-prps      # Create PRPs for unbuilt components

# 5. Continue development with new workflow
/fw start [next-component]    # Now with architecture guidance!
```

This way, debt-tofu-report gets the benefits of architecture-driven development without disrupting ongoing work!
