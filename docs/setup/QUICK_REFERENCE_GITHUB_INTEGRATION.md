# Quick Reference: GitHub Clone → Boilerplate Integration

## 🚀 5-Minute Integration

```bash
# 1. Clone any GitHub repository
git clone https://github.com/[user]/[repo].git
cd [repo]
git checkout -b add-boilerplate

# 2. Open in Claude Code
claude .

# 3. Run these commands in Claude Code:
/analyze-existing full      # Understand project (30 sec)
/boilerplate-version        # Check for old version (5 sec)
/integrate-boilerplate      # Add boilerplate (2 min)
/sr                        # Load everything (10 sec)

# 4. Install dependencies (if needed)
pnpm install

# Done! Start building with:
/fw start
```

## 🎯 Integration Modes

### Full Integration (Most Common)
```bash
/integrate-boilerplate --mode=full
```
✅ Everything integrated  
✅ Conflicts auto-resolved  
✅ Your code untouched  

### Selective Integration
```bash
/integrate-boilerplate --mode=selective
# Pick what you want from menu
```
✅ Choose specific features  
✅ Minimal footprint  
✅ Gradual adoption  

### Sidecar Mode (Testing)
```bash
/integrate-boilerplate --mode=sidecar
# Access with /bb prefix
```
✅ Zero conflicts  
✅ Parallel installation  
✅ Easy removal  

## 📊 Version Handling

### Check Version
```bash
/boilerplate-version
```

### Upgrade from Old Version
```bash
/upgrade-boilerplate        # Auto-detects version
/upgrade-boilerplate --from-version=2.0  # Specify version
```

### Supported Upgrade Paths
- v1.0 → v4.0 ✅
- v2.0 → v4.0 ✅
- v3.0 → v4.0 ✅
- v3.5 → v4.0 ✅

## 🛡️ What's Protected

**Never Touched:**
- `app/` - Your app code
- `components/` - Your components
- `lib/` - Your libraries
- `package.json` - Your deps
- `.env*` - Your secrets

**Smart Handling:**
- Commands → Conflicts renamed with `-project`
- Hooks → Yours run first (00-09)
- CLAUDE.md → Yours stays primary

## 🔄 Safety Features

### Preview Changes
```bash
/integrate-boilerplate --dry-run
```

### Automatic Backup
```
.claude-integration/backup/[timestamp]/
```

### Instant Rollback
```bash
/integration-rollback
```

## 📋 Common Scenarios

### Next.js Project
```bash
git clone [nextjs-repo]
cd [project]
claude .
/analyze-existing full
/integrate-boilerplate
/migrate-to-strict-design  # Optional
```

### React SPA
```bash
git clone [react-repo]
cd [project]
claude .
/analyze-existing full
/integrate-boilerplate --mode=selective
# Choose: 1,3,5 (skip design if using MUI)
```

### Monorepo
```bash
git clone [monorepo]
cd [monorepo]
claude .
/analyze-existing full
/config set project.type monorepo
/integrate-boilerplate
```

### Project with Old Boilerplate
```bash
git clone [old-boilerplate-project]
cd [project]
claude .
/boilerplate-version        # Check version
/upgrade-boilerplate        # Upgrade to v4.0
```

## ❓ Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Command not found | `/search integrate` or re-install |
| Conflicts detected | Normal - handled automatically |
| Version mismatch | `/upgrade-boilerplate` |
| Dependencies fail | `rm -rf node_modules && pnpm install` |
| Need to rollback | `/integration-rollback` |

## 📚 Full Documentation

- **Complete Guide**: [GITHUB_CLONE_INTEGRATION.md](./GITHUB_CLONE_INTEGRATION.md)
- **Existing Projects**: [EXISTING_PROJECT_INTEGRATION.md](./EXISTING_PROJECT_INTEGRATION.md)
- **New Projects**: [GETTING_STARTED.md](./GETTING_STARTED.md)
- **Workflows**: [SYSTEM_WORKFLOWS.md](./SYSTEM_WORKFLOWS.md)

## 💡 Pro Tips

1. **Always branch first**: `git checkout -b add-boilerplate`
2. **Use dry-run**: See changes before making them
3. **Check version first**: Might already have old boilerplate
4. **Selective for custom setups**: Don't force everything
5. **Sidecar for testing**: Try without commitment

---

**Version**: 4.0.0 | **Updated**: January 2025
