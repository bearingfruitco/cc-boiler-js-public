# Complete New Project Setup Guide with Claude Code

This guide walks you through setting up a new project with all your custom commands, hooks, and boilerplate system.

## Prerequisites

- Claude Code installed
- Git configured
- GitHub CLI (`gh`) installed
- Python 3 installed
- Node.js/npm/pnpm installed

## Step-by-Step Setup Process

### 1. Create Project Directory and Initialize

```bash
# Create and enter project directory
mkdir my-new-project
cd my-new-project

# Initialize git
git init

# Create initial structure
mkdir -p .claude/{commands,hooks,team,scripts,templates}
mkdir -p app components lib hooks stores types docs
```

### 2. Copy Your Boilerplate System

```bash
# Option A: Clone from your boilerplate repo (if you've pushed it)
git clone https://github.com/yourusername/claude-code-boilerplate .claude-temp
cp -r .claude-temp/boilerplate/.claude/* .claude/
cp .claude-temp/boilerplate/package.json .
cp .claude-temp/boilerplate/tailwind.config.js .
cp .claude-temp/boilerplate/*.md .
rm -rf .claude-temp

# Option B: Copy from local boilerplate
cp -r /Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/.claude/* .claude/
cp /Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/package.json .
cp /Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/tailwind.config.js .
cp /Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/*.md .
```

### 3. Initialize Claude Code Settings

```bash
# Create base settings.json if not exists
if [ ! -f .claude/settings.json ]; then
  cat > .claude/settings.json << 'EOF'
{
  "permissions": {
    "file_system": {
      "read": true,
      "write": true,
      "create_directories": true
    },
    "shell": {
      "execute": true,
      "allowed_commands": [
        "npm", "pnpm", "yarn", "npx",
        "git", "gh",
        "node", "tsx",
        "python3", "pip3",
        "prettier", "eslint"
      ]
    },
    "web_browser": {
      "enabled": true
    }
  }
}
EOF
fi
```

### 4. Install Custom Commands

```bash
# Your commands should already be in .claude/commands/ from the copy
# Verify they exist
ls -la .claude/commands/

# Expected files:
# - create-component.md
# - validate-design.md
# - smart-resume.md
# - context-grab.md
# - checkpoint.md
# - feature-workflow.md
# - todo.md
# - work-status.md
# - compact-prepare.md
# - analyze-project.md
# - help.md
# ... and more
```

### 5. Set Up Aliases

```bash
# Create/update aliases.json
cat > .claude/aliases.json << 'EOF'
{
  "cc": "create-component",
  "vd": "validate-design",
  "sr": "smart-resume",
  "cg": "context-grab",
  "cp": "checkpoint",
  "fw": "feature-workflow",
  "ws": "work-status",
  "tr": "test-runner",
  "pm": "performance-monitor",
  "sc": "security-check",
  "er": "error-recovery",
  "?": "help",
  "pp": "pre-pr",
  "qc": "quick-check",
  "dr": "daily-report"
}
EOF
```

### 6. Set Up Command Chains

```bash
# Chains should already be in .claude/chains.json from the copy
# Verify it exists
cat .claude/chains.json
```

### 7. Install Hooks System

```bash
# Run the hooks installer
cd .claude/scripts
chmod +x install-hooks.sh
./install-hooks.sh

# When prompted, enter your name (shawn or nikki)
# This creates .claude/team/config.json with your username
```

### 8. Configure Team Settings

```bash
# If working with Nikki, update team config
cat > .claude/team/config.json << EOF
{
  "current_user": "shawn"
}
EOF

# Initialize team files
cat > .claude/team/registry.json << 'EOF'
{
  "active_work": {},
  "worktrees": {},
  "last_sync": null
}
EOF

cat > .claude/team/knowledge-base.json << 'EOF'
{
  "components": [],
  "solutions": [],
  "command_patterns": {},
  "error_fixes": []
}
EOF
```

### 9. Create Project-Specific Files

```bash
# Create CLAUDE.md (project instructions)
cat > CLAUDE.md << 'EOF'
# Project Instructions for Claude Code

[Copy the CLAUDE.md content from your boilerplate, then customize for this project]

## Project-Specific Rules

### Business Logic
- [Add project-specific business rules]

### API Patterns
- [Add project-specific API patterns]

### Database Schema
- [Add project-specific schema notes]
EOF

# Create PROJECT_CONTEXT.md
cat > PROJECT_CONTEXT.md << 'EOF'
# [Project Name] Context

## Project Type
[Describe what this project is]

## Tech Stack
- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS (with design tokens)
- [Database choice]
- [Auth choice]

## Available Documentation
[List project docs]

## Commands Available
Run `/help` to see all available Claude Code commands
EOF

# Create design rules reminder
cp .claude/DESIGN_RULES.md ./
```

### 10. Install npm Dependencies

```bash
# Install base dependencies
pnpm install next@latest react@latest react-dom@latest
pnpm install -D typescript @types/react @types/node tailwindcss
pnpm install lucide-react framer-motion
pnpm install zod react-hook-form @hookform/resolvers

# If using Supabase
pnpm install @supabase/supabase-js

# Development tools
pnpm install -D prettier eslint @typescript-eslint/parser
```

### 11. Create Base Configuration Files

```bash
# TypeScript config
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{"name": "next"}],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
EOF

# Next.js config
cat > next.config.js << 'EOF'
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Your config here
}

module.exports = nextConfig
EOF

# Prettier config
cat > .prettierrc << 'EOF'
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
EOF
```

### 12. Create Initial Project Structure

```bash
# Create app directory structure
mkdir -p app/api
mkdir -p app/\(public\)
mkdir -p app/\(protected\)

# Create root layout
cat > app/layout.tsx << 'EOF'
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Your App',
  description: 'Your app description',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
EOF

# Create globals.css with Tailwind
cat > app/globals.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  /* Your design tokens will be added by Tailwind config */
}
EOF
```

### 13. Set Up Git and GitHub

```bash
# Create .gitignore
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/

# Next.js
.next/
out/

# Production
build/
dist/

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env*.local
.env

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts

# Claude Code
.claude/team/registry.json
.claude/team/metrics/
.claude/team/logs/
.claude/team/handoffs/
EOF

# Initial commit
git add .
git commit -m "Initial project setup with Claude Code boilerplate"

# Create GitHub repo and push
gh repo create my-new-project --private
git push -u origin main
```

### 14. Test Your Setup

```bash
# Start Claude Code in the project directory
claude-code .

# Test commands (in Claude Code terminal):
/help              # Should show all your commands
/sr                # Should run smart resume
/cc ui Button      # Should create a component with validation
/vd                # Should validate design system
/checkpoint create # Should create a checkpoint

# Test hooks by trying to:
# 1. Create a file with forbidden CSS classes
# 2. Make a claim like "this should work"
# 3. Check if auto-save to GitHub gists is working
```

### 15. Project-Specific Configuration

```bash
# Add any project-specific configuration
# For example, if using Supabase:

cat > .env.local << 'EOF'
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-key
EOF

# Add to .gitignore if not already there
echo ".env.local" >> .gitignore
```

## Troubleshooting

### Commands Not Found
```bash
# Check commands directory
ls -la .claude/commands/

# Check aliases
cat .claude/aliases.json

# Restart Claude Code
```

### Hooks Not Running
```bash
# Check Python
python3 --version

# Check hooks are executable
chmod +x .claude/hooks/**/*.py

# Check settings.json has hooks section
cat .claude/settings.json | grep -A 20 "hooks"

# Restart Claude Code after changes
```

### Team Features Not Working
```bash
# Check GitHub CLI
gh auth status

# Check team config
cat .claude/team/config.json

# Ensure git is initialized
git status
```

## Quick Setup Script

Save this as `setup-new-project.sh` for future use:

```bash
#!/bin/bash
# setup-new-project.sh - Quick setup for new Claude Code projects

PROJECT_NAME=$1
BOILERPLATE_PATH="/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate"

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./setup-new-project.sh <project-name>"
    exit 1
fi

echo "🚀 Setting up new project: $PROJECT_NAME"

# Create and enter directory
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Initialize git
git init

# Copy boilerplate
cp -r "$BOILERPLATE_PATH/.claude" .
cp "$BOILERPLATE_PATH/package.json" .
cp "$BOILERPLATE_PATH/tailwind.config.js" .
cp "$BOILERPLATE_PATH"/*.md .

# Create project structure
mkdir -p app/{api,\(public\),\(protected\)} components lib hooks stores types docs

# Run hooks installer
cd .claude/scripts
chmod +x install-hooks.sh
./install-hooks.sh

cd ../..

# Install dependencies
pnpm install

# Initial commit
git add .
git commit -m "Initial setup with Claude Code boilerplate"

echo "✅ Project setup complete!"
echo "Next steps:"
echo "1. cd $PROJECT_NAME"
echo "2. Update CLAUDE.md with project-specific instructions"
echo "3. Run: claude-code ."
echo "4. Test with: /help"
```

## Summary

This setup gives you:
1. ✅ All custom commands (/cc, /vd, /sr, etc.)
2. ✅ Command chains (morning-setup, pre-pr, etc.)
3. ✅ Hooks system (design enforcement, team sync, etc.)
4. ✅ Team collaboration features
5. ✅ GitHub integration
6. ✅ Design system enforcement
7. ✅ Project structure
8. ✅ Configuration files

After setup, you can immediately start using all your productivity features in the new project!
