# pin-config

Pin custom configuration data (JSON, lists, constants) as immutable requirements.

## Usage
```
/pin-config [name] [type] < content
/pin-json brands < {"approved": ["Nike", "Adidas", "Puma"]}
/pin-list colors < ["#FF0000", "#00FF00", "#0000FF"]
```

## What It Does

1. **Creates Locked Configuration** - Saves your data as immutable
2. **Enforces Via Hooks** - Same drift detection as requirements
3. **Validates Changes** - Blocks any code that violates config
4. **Anchors Context** - Adds to every prompt

## Examples

### Pin Brand Names
```bash
/pin-config approved-brands json
{
  "approved": ["Nike", "Adidas", "Puma", "New Balance"],
  "forbidden": ["Fake Brand", "Knockoff Co"],
  "premium": ["Nike", "Adidas"]
}
```

### Pin Color Palette
```bash
/pin-config design-colors json
{
  "primary": "#1E40AF",
  "secondary": "#DB2777", 
  "neutral": {
    "50": "#FAFAFA",
    "900": "#111827"
  }
}
```

### Pin API Endpoints
```bash
/pin-config api-endpoints json
{
  "production": "https://api.company.com",
  "staging": "https://staging-api.company.com",
  "version": "v2"
}
```

### Pin Allowed Values
```bash
/pin-config form-options json
{
  "states": ["CA", "NY", "TX", "FL"],
  "countries": ["US", "CA", "MX"],
  "industries": ["Tech", "Healthcare", "Finance"]
}
```

## How It Works

1. Saves to `.claude/requirements/config/[name].json`
2. Hooks monitor for violations
3. Blocks changes that don't match pinned values
4. Survives all sessions

## Integration with Code

Once pinned, the hooks will:

```typescript
// ❌ BLOCKED - Uses non-approved brand
const brands = ["Nike", "Reebok"]; // Reebok not in approved list

// ✅ ALLOWED - Only approved brands
const brands = ["Nike", "Adidas"];

// ❌ BLOCKED - Wrong color
const primaryColor = "#0000FF"; // Not the pinned primary

// ✅ ALLOWED - Matches pinned config
const primaryColor = "#1E40AF";
```

## Viewing Pinned Configs
```bash
/pin-config --list

PINNED CONFIGURATIONS
====================
📌 approved-brands (json) - 4 brands approved
📌 design-colors (json) - Color palette locked
📌 api-endpoints (json) - API URLs fixed
```

## Updating Configs
```bash
# Must explicitly unlock first
/unpin-config approved-brands --reason="Adding new partner brand"
/pin-config approved-brands json < new-brands.json
```

## Best Practices

1. **Pin Early** - Lock configs before development starts
2. **Be Specific** - Include all valid values
3. **Document Why** - Add description when pinning
4. **Version Control** - Configs are tracked in git
