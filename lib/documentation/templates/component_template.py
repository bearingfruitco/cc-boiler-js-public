"""
Component Documentation Template
"""

COMPONENT_TEMPLATE = """# {component_name}

<!-- GENERATED: component-overview -->
{overview}
<!-- END GENERATED -->

## Installation

```bash
import {{ {component_name} }} from '@/components/{component_path}'
```

## API Reference

<!-- GENERATED: props-table -->
### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
{props_table}
<!-- END GENERATED -->

<!-- GENERATED: methods-table -->
### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
{methods_table}
<!-- END GENERATED -->

## Usage Examples

<!-- GENERATED: examples -->
### Basic Usage

```tsx
{basic_example}
```

### Advanced Usage

```tsx
{advanced_example}
```
<!-- END GENERATED -->

<!-- MANUAL: custom-notes -->
## Notes

Add any custom notes here. This section is preserved during updates.
<!-- END MANUAL -->

<!-- GENERATED: metadata -->
---
*Last updated: {timestamp}*
*Auto-generated from: {source_file}*
<!-- END GENERATED -->
"""
