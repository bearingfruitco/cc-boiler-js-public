---
command: design-mode
aliases: [dm, design-system, ds]
description: Toggle or configure the design system enforcement
category: customization
---

# Design Mode Management

Quickly toggle between strict design system and flexible modes.

## Usage

```bash
/design-mode           # Show current status
/design-mode off       # Disable enforcement (full flexibility)  
/design-mode on        # Enable strict enforcement
/design-mode custom    # Open customization options
/design-mode shadcn    # Switch to shadcn/ui mode
/design-mode status    # Check current settings
```

## Quick Actions

### Disable for Creative Freedom
```bash
/dm off

# Now you can use:
# - Any Tailwind classes (text-sm, font-bold, etc.)
# - Any spacing (p-5, m-10, etc.)
# - Custom CSS values (text-[58px], p-[37px])
# - External UI libraries
```

### Enable for Consistency  
```bash
/dm on

# Enforces:
# - 4 font sizes only (text-size-[1-4])
# - 2 font weights only (font-regular, font-semibold)  
# - 4px spacing grid
# - Minimum touch targets
```

### Custom Configuration
```bash
/dm custom

# Opens config editor to set:
# - Your own allowed sizes
# - Your own spacing grid
# - Partial enforcement
# - Path-specific rules
```

## Examples

### Working on a Landing Page
```bash
# Need to match a specific design
/dm off
# ... implement landing page with full flexibility
/dm on  
# Back to strict mode for app components
```

### Using shadcn/ui
```bash
/dm shadcn
# Sets up for shadcn/ui components
# Updates AI instructions
# Disables conflicting rules
```

### Hybrid Approach
```bash
/dm custom
# Set flexible rules for /app/marketing/
# Keep strict rules for /components/ui/
```

## Configuration Options

When using `/dm custom`, you can configure:

```json
{
  "design_system": {
    "enforce": true,              // Master switch
    "auto_fix": false,           // Just warn, don't fix
    "strict_paths": [            // Enforce in these paths
      "components/ui/",
      "app/(app)/"  
    ],
    "flexible_paths": [          // No enforcement here
      "app/marketing/",
      "app/landing/"
    ],
    "allowed_font_sizes": [      // Your allowed sizes
      "text-sm", "text-base", "text-lg", "text-xl",
      "text-[32px]", "text-[48px]"  // Custom values
    ],
    "allowed_font_weights": [    // Your weights
      "font-normal", "font-medium", "font-semibold", "font-bold"
    ],
    "spacing_grid": null,        // null = no grid enforcement
    "min_touch_target": 44       // Mobile touch target size
  }
}
```

## Integration with Other Tools

### With CodeRabbit
- Design rules automatically sync
- `/dm off` also updates .coderabbit.yaml
- Custom rules propagate to PR reviews

### With Figma
```bash
# Import Figma tokens
/dm import-figma [tokens.json]
# Automatically configures design system
```

### With Tailwind UI
```bash
/dm off
# Full access to all Tailwind UI components
# No class restrictions
```

## Best Practices

1. **Start Strict** - Use strict mode by default
2. **Go Flexible for Special Cases** - Landing pages, marketing
3. **Document Exceptions** - Note why you disabled rules
4. **Re-enable After** - Return to strict mode when done

## Related Commands

- `/vd` - Validate design compliance
- `/cc` - Create component (respects current mode)
- `/analyze-design` - Extract design patterns from images

## Notes

- Settings persist across sessions
- Team members are notified of mode changes
- All changes are logged for accountability

For detailed customization guide, see: `docs/design/DESIGN_SYSTEM_CUSTOMIZATION.md`
