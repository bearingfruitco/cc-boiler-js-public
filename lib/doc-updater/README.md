# Documentation Updater

Automatically updates documentation as code changes, ensuring documentation stays in sync with implementation.

## Features

- **Automatic Code Analysis**: Parses TypeScript/JavaScript to extract documentation
- **Smart Updates**: Only updates changed sections, preserves custom content
- **Multiple Strategies**: Full regeneration, section updates, append-only, or merge
- **File Watching**: Real-time documentation updates as you code
- **JSDoc Support**: Extracts comments, examples, and type information
- **Component Documentation**: Generates prop tables and usage examples
- **API Documentation**: Creates endpoint documentation with examples
- **Type Documentation**: Documents interfaces and type definitions

## Installation

```bash
# Install dependencies
npm install typescript chokidar commander chalk glob lodash

# Make CLI executable
chmod +x lib/doc-updater/cli.ts
```

## Usage

### Initialize Documentation Structure

```bash
npx ts-node lib/doc-updater/cli.ts init
```

Creates the documentation directory structure:
```
docs/
├── components/     # React component docs
├── api/           # API endpoint docs
├── lib/           # Library function docs
├── types/         # Type definition docs
├── architecture/  # Architecture docs
└── guides/        # User guides
```

### Update Documentation

Update all documentation:
```bash
npx ts-node lib/doc-updater/cli.ts update
```

Update specific files:
```bash
npx ts-node lib/doc-updater/cli.ts update components/Button.tsx lib/utils.ts
```

Update with pattern:
```bash
npx ts-node lib/doc-updater/cli.ts update --pattern "components/**/*.tsx"
```

Dry run to preview changes:
```bash
npx ts-node lib/doc-updater/cli.ts update --dry-run
```

### Watch Mode

Enable automatic updates:
```bash
npx ts-node lib/doc-updater/cli.ts watch
```

Watch specific paths:
```bash
npx ts-node lib/doc-updater/cli.ts watch --paths components lib
```

### Check Documentation Status

```bash
npx ts-node lib/doc-updater/cli.ts check
```

Shows:
- Total source files
- Documentation coverage
- Missing documentation files

### Analyze Files

```bash
npx ts-node lib/doc-updater/cli.ts analyze components/Button.tsx
```

Shows what would be extracted from a file.

## Documentation Mapping

The system uses configurable mappings to determine how source files map to documentation:

```typescript
{
  // Component files → Individual component docs
  sourcePattern: 'components/.*\\.tsx?$',
  targetDoc: 'docs/components/${name}.md',
  updateStrategy: UpdateStrategy.SECTION_UPDATE,
  
  // API routes → API documentation
  sourcePattern: 'app/api/.*/route\\.ts$',
  targetDoc: 'docs/api/${path}.md',
  updateStrategy: UpdateStrategy.FULL_REGENERATE,
  
  // Library files → Library docs
  sourcePattern: 'lib/.*\\.ts$',
  targetDoc: 'docs/lib/${name}.md',
  updateStrategy: UpdateStrategy.MERGE,
  
  // Type definitions → Consolidated type docs
  sourcePattern: 'types/.*\\.ts$',
  targetDoc: 'docs/types.md',
  updateStrategy: UpdateStrategy.APPEND_ONLY
}
```

## Update Strategies

### Full Regenerate
Completely regenerates documentation from source. Best for:
- API documentation
- Auto-generated references
- Documentation that shouldn't have manual edits

### Section Update
Updates specific sections while preserving others. Best for:
- Component documentation
- Mixed auto/manual content
- Preserving examples and notes

### Append Only
Only adds new content, never modifies existing. Best for:
- Type definitions
- Changelog-style documentation
- Historical records

### Merge
Intelligently merges changes with existing content. Best for:
- Complex documentation
- Multi-source documentation
- Collaborative docs

## Writing Code for Better Documentation

### JSDoc Comments

Add comprehensive JSDoc comments:

```typescript
/**
 * Button component for user interactions
 * 
 * @description
 * A flexible button component that supports multiple variants and sizes.
 * Handles loading states and can be used as a link.
 * 
 * @example
 * ```tsx
 * <Button variant="primary" size="large" onClick={handleSubmit}>
 *   Submit Form
 * </Button>
 * ```
 * 
 * @example
 * ```tsx
 * // As a link
 * <Button as="a" href="/home" variant="secondary">
 *   Go Home
 * </Button>
 * ```
 */
export function Button({
  variant = 'primary',
  size = 'medium',
  loading = false,
  disabled = false,
  children,
  onClick,
  ...props
}: ButtonProps) {
  // Implementation
}
```

### TypeScript Interfaces

Document your types:

```typescript
/**
 * Props for the Button component
 */
export interface ButtonProps {
  /** Visual style variant */
  variant?: 'primary' | 'secondary' | 'danger';
  
  /** Button size */
  size?: 'small' | 'medium' | 'large';
  
  /** Shows loading spinner and disables interaction */
  loading?: boolean;
  
  /** Disables the button */
  disabled?: boolean;
  
  /** Button content */
  children: React.ReactNode;
  
  /** Click handler */
  onClick?: () => void;
}
```

### API Routes

Document your endpoints:

```typescript
/**
 * Get user by ID
 * 
 * @description Retrieves a single user by their ID
 * @authenticated Required
 * @param {string} id - User ID (path parameter)
 * @returns {200} User object
 * @returns {404} User not found
 * @returns {401} Unauthorized
 */
export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  // Implementation
}
```

## Preserved Sections

The following section names are preserved during auto-updates:
- **Notes**: Implementation notes
- **FAQ**: Frequently asked questions
- **Troubleshooting**: Common issues and solutions
- **Migration Guide**: Version migration instructions
- **Examples**: Additional examples (beyond auto-generated)
- **See Also**: Related documentation links

## Generated Documentation Examples

### Component Documentation

```markdown
# Button

A flexible button component that supports multiple variants and sizes.

## Import

```typescript
import { Button } from '@/components/Button';
```

## Props

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| variant | `'primary' \| 'secondary' \| 'danger'` | No | 'primary' | Visual style variant |
| size | `'small' \| 'medium' \| 'large'` | No | 'medium' | Button size |
| loading | `boolean` | No | false | Shows loading spinner |
| children | `React.ReactNode` | Yes | - | Button content |
| onClick | `() => void` | No | - | Click handler |

## Examples

### Basic Usage
```tsx
<Button variant="primary" onClick={handleClick}>
  Click me
</Button>
```

### Loading State
```tsx
<Button loading={isSubmitting}>
  Submit Form
</Button>
```
```

### API Documentation

```markdown
# API Documentation

## /api/users/[id]

### GET /api/users/[id]

Retrieves a single user by their ID

**Authentication Required**: Yes

#### Parameters

| Name | Type | In | Required | Description |
|------|------|----|----------|-------------|
| id | `string` | path | Yes | User ID |

#### Responses

| Status | Description |
|--------|-------------|
| 200 | User object |
| 404 | User not found |
| 401 | Unauthorized |

#### Example Request

```bash
curl -X GET \
  'http://localhost:3000/api/users/123' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```
```

## Integration with Development Workflow

### Git Hooks

Add to `.husky/pre-commit`:
```bash
#!/bin/sh
npx doc-updater update --dry-run
```

### CI/CD

Add to your CI pipeline:
```yaml
- name: Check documentation
  run: npx doc-updater check
  
- name: Update documentation
  run: npx doc-updater update
```

### VS Code Integration

Add to `.vscode/tasks.json`:
```json
{
  "label": "Watch Documentation",
  "type": "shell",
  "command": "npx doc-updater watch",
  "isBackground": true,
  "runOptions": {
    "runOn": "folderOpen"
  }
}
```

## Best Practices

1. **Write JSDoc Comments**: The better your comments, the better the documentation
2. **Use TypeScript**: Type information enhances documentation
3. **Provide Examples**: Include @example tags in JSDoc
4. **Document Props**: Add descriptions to interface properties
5. **Keep Custom Sections**: Use preserved section names for manual content
6. **Regular Updates**: Run documentation updates before commits
7. **Review Generated Docs**: Check auto-generated content for accuracy

## Troubleshooting

### Documentation Not Updating
- Check file patterns in mappings
- Verify JSDoc comments are properly formatted
- Ensure TypeScript compiles without errors

### Custom Content Lost
- Use preserved section names
- Check update strategy (use SECTION_UPDATE or MERGE)
- Verify section headers match exactly

### Missing Documentation
- Run `check` command to identify gaps
- Ensure source files have appropriate comments
- Check mapping configuration

## Future Enhancements

- [ ] Markdown table of contents generation
- [ ] Cross-reference linking
- [ ] Documentation versioning
- [ ] API playground generation
- [ ] Component playground integration
- [ ] Documentation search index
