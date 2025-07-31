# Architecture Change Tracker

A comprehensive system for tracking and managing changes to software architecture over time.

## Features

- **Change Recording**: Log all architecture modifications with full context
- **Impact Analysis**: Analyze the impact of proposed changes before implementation
- **Change History**: Maintain a searchable history of all architecture decisions
- **Conflict Detection**: Identify potential conflicts between changes
- **ADR Generation**: Automatically create Architecture Decision Records
- **Visual Diffs**: Compare architecture snapshots between different dates
- **Risk Assessment**: Calculate risk scores for proposed changes

## Installation

```bash
# Install dependencies
npm install commander chalk inquirer table

# Make CLI executable
chmod +x lib/architecture-tracker/cli.ts
```

## Usage

### Initialize Tracking

```bash
npx ts-node lib/architecture-tracker/cli.ts init
```

This creates the necessary directory structure and initial changelog.

### Record a Change

Interactive mode (recommended):
```bash
npx ts-node lib/architecture-tracker/cli.ts record --interactive
```

### List Changes

```bash
# List all changes
npx ts-node lib/architecture-tracker/cli.ts list

# List changes since a date
npx ts-node lib/architecture-tracker/cli.ts list --since "2024-01-01"

# List changes by category
npx ts-node lib/architecture-tracker/cli.ts list --category backend

# List changes affecting a component
npx ts-node lib/architecture-tracker/cli.ts list --component api-gateway
```

### Impact Analysis

Analyze the impact of a proposed change:
```bash
npx ts-node lib/architecture-tracker/cli.ts impact --interactive
```

### Generate ADR

Create an Architecture Decision Record from a change:
```bash
npx ts-node lib/architecture-tracker/cli.ts adr <change-id>
```

### Compare Architecture Versions

```bash
npx ts-node lib/architecture-tracker/cli.ts diff --from "2024-01-01" --to "2024-02-01"
```

## Change Types

- **Component Added/Removed/Modified**: Changes to system components
- **API Added/Removed/Modified**: API endpoint changes
- **Database Schema Changed**: Database structure modifications
- **Security Policy Updated**: Security-related changes
- **Technology Stack Changed**: Major technology decisions
- **Integration Added/Removed**: External service integrations
- **Architecture Pattern Changed**: Fundamental architecture changes

## Change Categories

- **Frontend**: UI/UX related changes
- **Backend**: Server-side logic changes
- **Database**: Data storage changes
- **Infrastructure**: Deployment and hosting changes
- **Security**: Security-related modifications
- **Integration**: Third-party service changes
- **Deployment**: CI/CD and deployment changes
- **Monitoring**: Observability changes

## Directory Structure

```
docs/architecture/
├── changes/           # Individual change records (JSON)
├── snapshots/         # Architecture snapshots
├── decisions/         # Architecture Decision Records (ADRs)
└── CHANGELOG.md       # Human-readable changelog
```

## Integration with Existing Commands

The architecture tracker can be integrated with existing commands:

### With PRP Generation
When generating a new PRP, record the architecture change:
```typescript
const change = await tracker.recordChange({
  type: ArchitectureChangeType.COMPONENT_ADDED,
  category: ChangeCategory.BACKEND,
  description: 'Added caching service',
  relatedPRP: prpId,
  // ... other fields
});
```

### With Architecture Validation
Before making changes, run impact analysis:
```typescript
const report = await tracker.generateImpactReport(proposedChange);
if (report.riskScore > 20) {
  console.warn('High risk change detected. Review recommendations.');
}
```

## Example Change Record

```json
{
  "id": "arch-change-20240115-a7x9k",
  "timestamp": "2024-01-15T10:30:00Z",
  "type": "component_added",
  "category": "backend",
  "description": "Added Redis caching layer",
  "filesAffected": [
    "docs/architecture/SYSTEM_DESIGN.md",
    "docs/architecture/TECHNICAL_ROADMAP.md"
  ],
  "relatedPRP": "cache-service-prp",
  "author": "john.doe",
  "rationale": "Improve API response times and reduce database load",
  "impact": {
    "components": ["api-gateway", "database-service"],
    "estimatedEffort": "medium",
    "breakingChange": false,
    "performanceImpact": "positive"
  }
}
```

## Best Practices

1. **Record Changes Immediately**: Don't wait - record architecture changes as they happen
2. **Be Descriptive**: Provide clear descriptions and rationale
3. **Link to PRPs**: Always link architecture changes to their driving PRPs
4. **Review Impact**: Run impact analysis before major changes
5. **Generate ADRs**: Create ADRs for significant decisions
6. **Regular Reviews**: Periodically review the architecture changelog

## Future Enhancements

- [ ] Web UI for visualizing architecture evolution
- [ ] Automated change detection from git commits
- [ ] Integration with diagram generation tools
- [ ] Metrics dashboard for architecture health
- [ ] Automated architecture documentation updates
