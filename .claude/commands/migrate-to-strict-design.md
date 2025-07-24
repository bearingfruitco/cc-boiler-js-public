# Migrate to Strict Design System

Analyze and migrate existing codebase to the strict 4-size, 2-weight design system.

## Arguments:
- $MODE: analyze|migrate|force (default: analyze)
- $SCOPE: component|directory|all (default: all)

## Purpose:
- Find all design system violations in existing code
- Generate migration plan
- Optionally auto-migrate with confirmation
- Create report of changes needed/made

## Steps:

### 1. Analysis Phase

```bash
echo "## 🔍 Analyzing Design System Usage"
echo ""

# Find all component files
COMPONENT_FILES=$(find . -name "*.tsx" -o -name "*.jsx" | grep -v node_modules | grep -v .next)
TOTAL_FILES=$(echo "$COMPONENT_FILES" | wc -l)

echo "Found $TOTAL_FILES component files"
echo ""

# Track violations
declare -A VIOLATIONS
VIOLATIONS[font_size]=0
VIOLATIONS[font_weight]=0
VIOLATIONS[spacing]=0
VIOLATIONS[touch_target]=0
```

### 2. Scan for Violations

```typescript
// Violation patterns
const violations = {
  fontSize: {
    forbidden: ['text-xs', 'text-sm', 'text-base', 'text-lg', 'text-xl', 'text-2xl'],
    replacement: {
      'text-xs': 'text-size-4',      // 12px
      'text-sm': 'text-size-4',      // 12px
      'text-base': 'text-size-3',    // 16px
      'text-lg': 'text-size-3',      // 16px
      'text-xl': 'text-size-2',      // 24px
      'text-2xl': 'text-size-1'      // 32px
    }
  },
  fontWeight: {
    forbidden: ['font-light', 'font-normal', 'font-medium', 'font-bold'],
    replacement: {
      'font-light': 'font-regular',
      'font-normal': 'font-regular',
      'font-medium': 'font-semibold',
      'font-bold': 'font-semibold'
    }
  },
  spacing: {
    invalid: [5, 7, 9, 11, 13, 15, 17, 18, 19],
    round: (value) => {
      const valid = [1,2,3,4,6,8,10,12,14,16,20,24,32];
      return valid.reduce((prev, curr) => 
        Math.abs(curr - value) < Math.abs(prev - value) ? curr : prev
      );
    }
  }
};
```

### 3. Generate Violation Report

```bash
cat > .agent-os/DESIGN_MIGRATION_REPORT.md << 'EOF'
# Design System Migration Report

Generated: $(date)

## Summary
- Total Files: $TOTAL_FILES
- Files with Violations: $FILES_WITH_VIOLATIONS
- Total Violations: $TOTAL_VIOLATIONS

## Violations by Type

### Font Size Violations (${VIOLATIONS[font_size]})
EOF

# Add specific violations
for file in $COMPONENT_FILES; do
  # Check each file for violations
  if grep -E "text-(xs|sm|base|lg|xl|2xl)" "$file" > /dev/null; then
    echo "- $file" >> .agent-os/DESIGN_MIGRATION_REPORT.md
    grep -n -E "text-(xs|sm|base|lg|xl|2xl)" "$file" | head -3 >> .agent-os/DESIGN_MIGRATION_REPORT.md
  fi
done
```

### 4. Migration Plan

```typescript
// Generate migration script
const migrationPlan = {
  automatic: [], // Safe to auto-migrate
  review: [],    // Needs human review
  complex: []    // Complex cases needing refactor
};

// Classify each violation
violations.forEach(v => {
  if (v.type === 'fontSize' && v.inButton) {
    // Buttons should use text-size-3
    migrationPlan.automatic.push({
      file: v.file,
      line: v.line,
      from: v.current,
      to: 'text-size-3'
    });
  } else if (v.type === 'spacing' && v.isGrid) {
    // Grid spacing needs review
    migrationPlan.review.push(v);
  }
});
```

### 5. Execute Migration (if requested)

```bash
if [ "$MODE" = "migrate" ] || [ "$MODE" = "force" ]; then
  echo -e "\n## 🔄 Executing Migration"
  
  # Backup first
  echo "Creating backup..."
  cp -r components components.backup.$(date +%Y%m%d_%H%M%S)
  
  # Apply automatic fixes
  for file in $COMPONENT_FILES; do
    # Font sizes
    sed -i '' 's/text-xs/text-size-4/g' "$file"
    sed -i '' 's/text-sm/text-size-4/g' "$file"
    sed -i '' 's/text-base/text-size-3/g' "$file"
    sed -i '' 's/text-lg/text-size-3/g' "$file"
    sed -i '' 's/text-xl/text-size-2/g' "$file"
    sed -i '' 's/text-2xl/text-size-1/g' "$file"
    
    # Font weights
    sed -i '' 's/font-light/font-regular/g' "$file"
    sed -i '' 's/font-normal/font-regular/g' "$file"
    sed -i '' 's/font-medium/font-semibold/g' "$file"
    sed -i '' 's/font-bold/font-semibold/g' "$file"
    
    # Common spacing fixes
    sed -i '' 's/\bp-5\b/p-4/g' "$file"
    sed -i '' 's/\bp-7\b/p-6/g' "$file"
    sed -i '' 's/\bp-9\b/p-8/g' "$file"
  done
  
  echo "✅ Automatic migration complete"
fi
```

### 6. Create Component Audit

```markdown
# Generate component audit
cat > .agent-os/COMPONENT_AUDIT.md << 'EOF'
# Component Design System Audit

## Components Needing Updates

### High Priority (Core Components)
EOF

# Identify core components
CORE_COMPONENTS=$(find components/ui -name "*.tsx" 2>/dev/null)
for component in $CORE_COMPONENTS; do
  violations=$(grep -c -E "text-(xs|sm|base|lg|xl)|font-(light|normal|medium|bold)" "$component" || echo 0)
  if [ $violations -gt 0 ]; then
    echo "- $(basename $component): $violations violations" >> .agent-os/COMPONENT_AUDIT.md
  fi
done
```

### 7. Update Tailwind Config

```javascript
// Check if using Tailwind v4
if (tailwindVersion >= 4) {
  console.log("✅ Tailwind v4 detected - CSS config recommended");
  
  // Create migration CSS
  fs.writeFileSync('styles/design-system-migration.css', `
    /* Design System Migration - Temporary */
    @layer utilities {
      /* Map old classes to new during migration */
      .text-sm { @apply text-size-4; }
      .text-base { @apply text-size-3; }
      .text-lg { @apply text-size-3; }
      .text-xl { @apply text-size-2; }
      .text-2xl { @apply text-size-1; }
      
      .font-normal { @apply font-regular; }
      .font-medium { @apply font-semibold; }
      .font-bold { @apply font-semibold; }
    }
  `);
}
```

### 8. Integration with Existing Tools

```bash
# Update validate-design to use strict mode
echo "Updating design validation to strict mode..."

# Add to settings
if [ -f ".claude/settings.json" ]; then
  jq '.design_system.strict_mode = true' .claude/settings.json > .claude/settings.json.tmp
  mv .claude/settings.json.tmp .claude/settings.json
fi

# Enable hook if not enabled
if [ ! -f ".claude/hooks/pre-tool-use/02-design-check-simple.py" ]; then
  echo "Enabling design system hook..."
  cp ~/.claude/hooks/pre-tool-use/02-design-check-simple.py .claude/hooks/pre-tool-use/
fi
```

### 9. Final Report

```bash
echo -e "\n## 📊 Migration Summary"
echo ""
echo "### Changes Made:"
echo "- Font sizes standardized to 4-size system"
echo "- Font weights reduced to 2 (regular/semibold)"
echo "- Spacing aligned to 4px grid"
echo "- Touch targets set to minimum 44px"
echo ""
echo "### Files Updated: $MIGRATED_COUNT"
echo "### Backup Location: components.backup.*"
echo ""
echo "### Next Steps:"
echo "1. Review .agent-os/DESIGN_MIGRATION_REPORT.md"
echo "2. Check .agent-os/COMPONENT_AUDIT.md"
echo "3. Run tests: /tr"
echo "4. Visual regression check: /btf"
echo "5. Enable strict validation: /vd"
```

## Chain Integration:

```json
{
  "migrate-existing-project": {
    "description": "Full migration for existing projects",
    "steps": [
      "/analyze-existing",
      "/migrate-to-strict-design analyze",
      "Review migration report",
      "/migrate-to-strict-design migrate",
      "/vd",
      "/tr"
    ]
  }
}
```

## Hook Updates:

This command works with:
- `02-design-check-simple.py` - Will enforce new standards
- `11-truth-enforcer.py` - Protects migrated components
- `14a-creation-guard.py` - Ensures new components follow standards

## Settings Update:

```json
{
  "design_system": {
    "strict_mode": true,
    "migration_complete": false,
    "legacy_mappings": {
      "text-sm": "text-size-4",
      "text-base": "text-size-3"
    }
  }
}
```
