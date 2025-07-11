# Complete New Project Setup Guide with Claude Code

This guide provides alternative methods for setting up a new project with the Claude Code boilerplate.

## Prerequisites

- Claude Code installed (`npm install -g @anthropic-ai/claude-code`)
- Git configured
- GitHub CLI (`gh`) installed and authenticated
- Node.js v22+ / pnpm v9+

## Method 1: GitHub Clone (RECOMMENDED)

```bash
# 1. Clone with your project name
git clone https://github.com/bearingfruitco/claude-code-boilerplate.git my-new-project
cd my-new-project

# 2. Make it yours
rm -rf .git
git init
git add .
git commit -m "Initial commit from Claude Code boilerplate"

# 3. Create GitHub repo
gh repo create my-new-project --private --source=. --remote=origin --push

# 4. Install and setup
pnpm install
chmod +x scripts/*.sh
./scripts/setup-enhanced-boilerplate.sh

# 5. Start building
claude-code .
/init
/init-project
```

## Method 2: GitHub Template

If the repo is set up as a template:

1. Go to https://github.com/bearingfruitco/claude-code-boilerplate
2. Click "Use this template" → "Create a new repository"
3. Name your repo and make it private
4. Clone your new repo:
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
   cd YOUR-REPO
   pnpm install
   ./scripts/setup-enhanced-boilerplate.sh
   ```

## Method 3: Local Copy

If you have the boilerplate locally:

```bash
# 1. Create project
mkdir my-new-project && cd my-new-project

# 2. Copy everything (including hidden files)
cp -r /path/to/claude-code-boilerplate/. .

# 3. Initialize your repo
rm -rf .git
git init
git add .
git commit -m "Initial commit from boilerplate"

# 4. Create GitHub repo
gh repo create my-new-project --private --source=. --remote=origin --push

# 5. Setup
pnpm install
./scripts/setup-enhanced-boilerplate.sh
```

## Method 4: Manual Setup (Advanced)

For selective copying or understanding the structure:

```bash
# 1. Create base structure
mkdir my-new-project && cd my-new-project
git init

# 2. Create directories
mkdir -p .claude/{commands,hooks,personas,scripts,orchestration}
mkdir -p app components lib hooks stores docs/{setup,workflow,technical,claude}
mkdir -p field-registry/{core,verticals,compliance}
mkdir -p scripts templates

# 3. Copy core files
curl -o README.md https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/README.md
curl -o CLAUDE.md https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/CLAUDE.md
curl -o QUICK_REFERENCE.md https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/QUICK_REFERENCE.md
curl -o package.json https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/package.json
curl -o tailwind.config.js https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/tailwind.config.js
curl -o .gitignore https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/.gitignore

# 4. Get the .claude directory (critical)
# This requires cloning or downloading the full repo as there are many files
```

## Post-Setup Configuration

### 1. Environment Variables
```bash
# Create .env.local
cat > .env.local << EOF
# Supabase (if using)
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Analytics (optional)
NEXT_PUBLIC_RUDDERSTACK_KEY=
NEXT_PUBLIC_RUDDERSTACK_URL=
EOF
```

### 2. Project Configuration
```bash
# In Claude Code
/init                      # One-time setup
/init-project             # Define your project
```

### 3. Customize Settings
Edit `.claude/project-config.json`:
```json
{
  "projectName": "my-new-project",
  "projectType": "saas",
  "features": {
    "prdDriven": true,
    "designSystem": true,
    "securityForms": true,
    "multiAgent": true
  }
}
```

## Verification Checklist

Run these to verify setup:

```bash
# Check structure
ls -la .claude/           # Should see commands, hooks, etc.
ls -la docs/             # Should see organized docs

# Check GitHub
gh auth status           # Should be authenticated
git remote -v           # Should show origin

# Check dependencies
node --version          # Should be v22+
pnpm --version         # Should be v9+
claude-code --version  # Should work

# In Claude Code
/help                  # Should show all commands
/sr                    # Should show smart resume
```

## Common Issues

### Missing commands in Claude Code
- Make sure you're in the project root
- Run `/init` to initialize

### GitHub authentication fails
```bash
gh auth login
# Choose: GitHub.com → HTTPS → Yes → Browser
```

### Permission denied on scripts
```bash
chmod +x scripts/*.sh
```

## Next Steps

1. **Define Your Project**
   ```bash
   /init-project      # Interactive project setup
   ```

2. **Generate Structure**
   ```bash
   /gi PROJECT        # Create GitHub issues
   ```

3. **Start Building**
   ```bash
   /fw start 1        # Begin first feature
   ```

## Alternative Approaches

### For Existing Projects
See [ADD_TO_EXISTING_PROJECT.md](./ADD_TO_EXISTING_PROJECT.md)

### For Quick Testing
See [QUICK_START_NEW_PROJECT.md](./QUICK_START_NEW_PROJECT.md)

### For Team Setup
Share this guide and have team members:
1. Clone your repo
2. Run setup scripts
3. Configure their `.claude/team/config.json`

---

Remember: The `.claude/` directory is the heart of the system. Everything else can be customized to your needs.
