# Claude Code Boilerplate Integration Guide

## 🎯 Smart Integration from Local Boilerplate

You have the complete boilerplate at: `/Users/shawnsmith/dev/bfc/boilerplate/`
And a fresh copy at: `/Users/shawnsmith/dev/bfc/boilerplate-latest/`

## Integration Strategy for Existing Projects

When asked to integrate the boilerplate into an existing project, follow this systematic approach:

### Phase 1: Analysis
```bash
# 1. Analyze what the project already has
ls -la .claude 2>/dev/null || echo "No .claude directory"
ls -la CLAUDE.md 2>/dev/null || echo "No CLAUDE.md"
grep -l "text-size-" **/*.tsx 2>/dev/null | head -5 || echo "No design system detected"
```

### Phase 2: Core Integration (Always Do This)
```bash
# 1. Copy .claude directory (merge if exists)
if [ -d ".claude" ]; then
  rsync -av --backup --suffix="-backup" /Users/shawnsmith/dev/bfc/boilerplate/.claude/ .claude/
else
  cp -r /Users/shawnsmith/dev/bfc/boilerplate/.claude .
fi

# 2. Copy CLAUDE.md (backup if exists)
if [ -f "CLAUDE.md" ]; then
  cp CLAUDE.md CLAUDE.md.backup
fi
cp /Users/shawnsmith/dev/bfc/boilerplate/CLAUDE.md .

# 3. Copy PRPs directory
cp -r /Users/shawnsmith/dev/bfc/boilerplate/PRPs .

# 4. Copy field-registry
cp -r /Users/shawnsmith/dev/bfc/boilerplate/field-registry .
```

### Phase 3: Configuration Merging
```bash
# 1. Handle tailwind.config.js
if [ -f "tailwind.config.js" ]; then
  cp /Users/shawnsmith/dev/bfc/boilerplate/tailwind.config.js tailwind.config.boilerplate.js
  echo "⚠️ Manual merge needed: tailwind.config.boilerplate.js → tailwind.config.js"
else
  cp /Users/shawnsmith/dev/bfc/boilerplate/tailwind.config.js .
fi

# 2. Handle tsconfig.json
if [ -f "tsconfig.json" ]; then
  cp /Users/shawnsmith/dev/bfc/boilerplate/tsconfig.json tsconfig.boilerplate.json
  echo "⚠️ Manual merge needed: tsconfig.boilerplate.json → tsconfig.json"
else
  cp /Users/shawnsmith/dev/bfc/boilerplate/tsconfig.json .
fi

# 3. Handle biome.json
if [ -f "biome.json" ]; then
  cp /Users/shawnsmith/dev/bfc/boilerplate/biome.json biome.boilerplate.json
  echo "⚠️ Manual merge needed: biome.boilerplate.json → biome.json"
else
  cp /Users/shawnsmith/dev/bfc/boilerplate/biome.json .
fi
```

### Phase 4: Selective Component Integration
Based on what's missing in the project:

```bash
# If no components/ui directory
if [ ! -d "components/ui" ]; then
  cp -r /Users/shawnsmith/dev/bfc/boilerplate/components/ui components/
fi

# If no lib/utils
if [ ! -f "lib/utils.ts" ]; then
  mkdir -p lib
  cp /Users/shawnsmith/dev/bfc/boilerplate/lib/utils.ts lib/
fi

# If no hooks directory
if [ ! -d "hooks" ]; then
  cp -r /Users/shawnsmith/dev/bfc/boilerplate/hooks .
fi
```

### Phase 5: Scripts Integration
```bash
# Copy useful scripts
mkdir -p scripts
cp /Users/shawnsmith/dev/bfc/boilerplate/scripts/setup-hooks.sh scripts/
cp /Users/shawnsmith/dev/bfc/boilerplate/scripts/quick-setup.sh scripts/
chmod +x scripts/*.sh
```

### Phase 6: Git Hooks Setup
```bash
# Set up git hooks if .husky doesn't exist
if [ ! -d ".husky" ]; then
  cp -r /Users/shawnsmith/dev/bfc/boilerplate/.husky .
fi
```

## Smart Selective Integration

For specific features:

### Just Commands & Agents
```bash
cp -r /Users/shawnsmith/dev/bfc/boilerplate/.claude .
cp /Users/shawnsmith/dev/bfc/boilerplate/CLAUDE.md .
```

### Just Design System
```bash
cp /Users/shawnsmith/dev/bfc/boilerplate/tailwind.config.js tailwind.config.boilerplate.js
# Then manually merge the design tokens
```

### Just Security Features
```bash
cp -r /Users/shawnsmith/dev/bfc/boilerplate/field-registry .
cp -r /Users/shawnsmith/dev/bfc/boilerplate/lib/security lib/
```

### Just PRPs
```bash
cp -r /Users/shawnsmith/dev/bfc/boilerplate/PRPs .
```

## Post-Integration Checklist

After integration, verify:
- [ ] `/sr` command works in Claude Code
- [ ] `/help` shows all commands
- [ ] Design system tokens in tailwind.config.js
- [ ] No TypeScript errors
- [ ] Biome configuration valid

## Manual Merge Requirements

Always need manual merging for:
1. `package.json` - dependencies
2. `tailwind.config.js` - merge design tokens
3. `tsconfig.json` - merge path aliases
4. `.env.example` - merge environment variables

## Quick Test
```bash
# In Claude Code
/sr
/analyze-existing full
/help
```
