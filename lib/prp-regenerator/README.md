# PRP Regenerator

Automatically synchronizes Project Requirements Plans (PRPs) with architecture changes, ensuring implementation plans stay current as the system evolves.

## Features

- **Automatic Change Detection**: Identifies which PRPs need updates based on architecture changes
- **Smart Regeneration**: Only updates affected sections while preserving progress
- **Progress Preservation**: Maintains completed checkboxes and custom content
- **Change Tracking**: Adds clear markers showing what changed and why
- **Backup System**: Creates backups before modifying PRPs
- **Dry Run Mode**: Preview changes without modifying files

## Installation

```bash
# Install dependencies
npm install commander chalk inquirer table

# Make CLI executable
chmod +x lib/prp-regenerator/cli.ts
```

## Usage

### Check Sync Status

```bash
npx ts-node lib/prp-regenerator/cli.ts status
```

Shows:
- Total PRPs in the system
- How many are synced with architecture
- Which PRPs are outdated
- Which components are missing PRPs

### Analyze Impact

```bash
# Analyze all changes
npx ts-node lib/prp-regenerator/cli.ts analyze

# Analyze changes since a specific date
npx ts-node lib/prp-regenerator/cli.ts analyze --since "2024-01-01"
```

### Update PRPs

Interactive mode (recommended):
```bash
npx ts-node lib/prp-regenerator/cli.ts update --interactive
```

Update all outdated PRPs:
```bash
npx ts-node lib/prp-regenerator/cli.ts update --all
```

Dry run to preview changes:
```bash
npx ts-node lib/prp-regenerator/cli.ts update --all --dry-run
```

### Sync All PRPs

```bash
npx ts-node lib/prp-regenerator/cli.ts sync-all
```

## How It Works

1. **Architecture Change Detection**
   - Monitors changes recorded by the Architecture Tracker
   - Maps changes to affected components
   - Determines which PRPs need updates

2. **Smart Content Preservation**
   - Extracts completion status (checkboxes)
   - Preserves custom sections
   - Maintains implementation notes
   - Keeps validation results

3. **Regeneration Process**
   - Loads current architecture
   - Generates updated sections
   - Merges with preserved content
   - Adds change markers
   - Creates backup before writing

4. **Change Notification**
   - Adds banner showing architecture was updated
   - Lists specific changes affecting the component
   - Marks modified sections with 🔄 emoji
   - Links to architecture changelog

## Example Updated PRP

```markdown
# PRP: Authentication Service

> ⚠️ **Architecture Updated**: 2024-01-15
> - ADDED: OAuth2 integration requirement
> - MODIFIED: Session storage moved to Redis
> - See [architecture changelog](../docs/architecture/CHANGELOG.md)

## Overview
[Updated content reflecting new architecture]

## Technical Context 🔄
[Section updated with new dependencies]

## Implementation Order
- [x] Create directory structure (preserved)
- [x] Define TypeScript types (preserved)
- [ ] Implement OAuth2 integration (new)
```

## Preserved Content

The regenerator preserves:
- ✅ Checkbox completion status
- 📝 Implementation notes
- 🔧 Custom sections
- ✓ Validation results
- 💡 Developer comments

## Integration with Architecture Tracker

The PRP Regenerator works seamlessly with the Architecture Tracker:

```typescript
// When architecture changes are recorded
await architectureTracker.recordChange({
  type: 'component_added',
  component: 'oauth-service',
  // ...
});

// PRPs can be automatically updated
const tasks = await prpRegenerator.analyzeImpact();
await prpRegenerator.regeneratePRP(tasks[0]);
```

## Configuration Options

```typescript
interface RegenerationOptions {
  preserveProgress: boolean;      // Keep checkbox states (default: true)
  preserveCustomSections: boolean; // Keep custom content (default: true)
  addChangeMarkers: boolean;       // Add change indicators (default: true)
  backupOriginal: boolean;         // Create backup (default: true)
  dryRun: boolean;                // Preview only (default: false)
}
```

## Best Practices

1. **Regular Sync Checks**: Run `status` command weekly
2. **Review Before Update**: Use `--dry-run` first
3. **Interactive Updates**: Review each PRP individually
4. **Backup Verification**: Check `.backups` folder
5. **Manual Review**: For completed PRPs

## Troubleshooting

### PRP Not Detected as Outdated
- Check if architecture changes affect the component
- Verify PRP metadata is properly formatted
- Run `analyze` to see detected changes

### Content Not Preserved
- Ensure checkboxes follow standard format: `- [ ]` or `- [x]`
- Custom sections should have unique headers
- Implementation notes should follow the format

### Merge Conflicts
- Backups are in `PRPs/.backups/`
- Compare with backup to resolve
- Use `restore` command if needed

## Future Enhancements

- [ ] Git integration for automatic updates
- [ ] Webhook support for CI/CD
- [ ] Batch processing improvements
- [ ] Visual diff interface
- [ ] Conflict resolution UI
