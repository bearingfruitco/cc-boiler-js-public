# Day 1 Complete Setup Guide

This guide walks you through the complete setup process for a new project using the Claude Code Boilerplate, including all GitHub integrations.

## Prerequisites

- Claude Code installed (claude.ai/code)
- GitHub account
- Node.js 22+ and pnpm
- Git configured

## Step 1: Create Your New Repository

### Option A: Create Empty GitHub Repo First (Recommended)
```bash
# 1. Go to github.com and create new repository
# 2. Name it (e.g., "my-awesome-app")
# 3. DON'T initialize with README
# 4. Copy the repository URL
```

### Option B: Create Locally First
```bash
# We'll create on GitHub later
mkdir my-awesome-app
cd my-awesome-app
```

## Step 2: Clone and Setup Boilerplate

```bash
# Clone boilerplate to temporary directory
git clone https://github.com/bearingfruitco/claude-code-boilerplate.git temp-boilerplate

# Copy everything except .git
cp -r temp-boilerplate/* .
cp -r temp-boilerplate/.* . 2>/dev/null || true

# Clean up
rm -rf temp-boilerplate
rm -rf .git

# Initialize fresh git
git init
```

## Step 3: Connect to YOUR Repository (Critical!)

```bash
# If you created repo on GitHub (Option A):
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# If you didn't create on GitHub yet (Option B):
# Use GitHub CLI
gh repo create YOUR_REPO_NAME --private --source=.

# Or create manually on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

## Step 4: Install GitHub Apps (NEW!)

### 4.1 Install CodeRabbit
1. Go to [github.com/marketplace/coderabbit](https://github.com/marketplace/coderabbit)
2. Click "Set up a plan" → Choose Pro ($24/dev/month)
3. Select "Only select repositories" → Choose YOUR new repo
4. Grant permissions and complete setup

### 4.2 Install Claude Code GitHub App
1. Go to [github.com/apps/claude](https://github.com/apps/claude)
2. Click "Install"
3. Select "Only select repositories" → Choose YOUR new repo
4. Grant permissions (code read/write, issues, PRs)

### 4.3 Configure CodeRabbit (Optional but Recommended)
Create `.coderabbit.yaml` in your repo root:

```yaml
# .coderabbit.yaml
reviews:
  auto_review:
    enabled: true
  
  # Respect our design system
  custom_patterns:
    - pattern: "text-sm|text-lg|text-xl|font-bold|font-medium"
      message: "Use design tokens: text-size-[1-4], font-regular/semibold"
      level: error
    
    - pattern: "p-5|m-7|gap-5|space-x-5|space-y-5"
      message: "Use 4px grid: p-4, p-6, p-8"
      level: error
    
    - pattern: "console\\.log.*email|console\\.log.*phone|console\\.log.*ssn"
      message: "Never log PII to console"
      level: error

  # Don't review generated files
  path_filters:
    - "!pnpm-lock.yaml"
    - "!*.generated.ts"
    - "!*.d.ts"
```

## Step 5: Initial Setup and Commit

```bash
# Install dependencies
pnpm install

# Setup git hooks
pnpm prepare

# Create .env.local from example
cp .env.example .env.local

# Initial commit to YOUR repo
git add .
git commit -m "Initial commit with Claude Code Boilerplate"
git push -u origin main
```

## Step 6: Update Project Configuration

### 6.1 Fix Repository References
Edit `.claude/project-config.json`:

```json
{
  "repository": {
    "owner": "YOUR_GITHUB_USERNAME",
    "name": "YOUR_REPO_NAME",
    "branch": "main"
  },
  "project": {
    "name": "Your Project Name",
    "type": "Next.js Application"
  }
}
```

### 6.2 Update package.json
```json
{
  "name": "your-project-name",
  "version": "0.1.0",
  // ... rest stays the same
}
```

## Step 7: Start Claude Code and Initialize

```bash
# Open in Claude Code
claude .

# OR open in VSCode/Cursor with Claude Code extension
code .
```

In Claude Code, run these commands:

```bash
# 1. Initialize the system
/init

# 2. Initialize your PROJECT (not boilerplate!)
/init-project

# Answer questions about YOUR project:
# - What are you building?
# - Who is your target user?
# - What problem does it solve?
# - MVP scope?
# - Tech preferences?
```

## Step 8: Generate GitHub Issues in YOUR Repo

```bash
# This will create issues in YOUR repo, not the boilerplate
/gi PROJECT

# Verify by checking:
# https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/issues
```

## Step 9: Verify Everything Works

### 9.1 Test CodeRabbit
```bash
# Create a test branch
git checkout -b test/coderabbit

# Make a small change with a design violation
echo '<div className="text-sm font-bold">Test</div>' > components/Test.tsx

# Commit and push
git add .
git commit -m "Test CodeRabbit"
git push origin test/coderabbit

# Create PR on GitHub
# CodeRabbit should comment within 2-3 minutes!
```

### 9.2 Test Claude Code Integration
```bash
# In your PR, you should see:
# - CodeRabbit review comments
# - Claude Code bot able to create issues/PRs
# - Status checks from both
```

## Step 10: Configure Branch Protection (Optional)

Go to Settings → Branches → Add rule:
- Branch name pattern: `main`
- Require PR reviews: ✓
- Require status checks: ✓
  - CodeRabbit
  - Claude Code (if using Actions)
- Require branches to be up to date: ✓

## Common Issues and Fixes

### Issue: Commands create issues in boilerplate repo
**Fix**: Update `.claude/project-config.json` with YOUR repo details

### Issue: CodeRabbit not reviewing
**Fix**: 
1. Check it's installed on YOUR repo (not boilerplate)
2. Wait 2-3 minutes (initial setup)
3. Check GitHub Apps settings

### Issue: Permission errors
**Fix**: Ensure both apps have write access to code, issues, and PRs

## Daily Workflow After Setup

```bash
# Start each day
/sr                    # Smart resume
/bt list               # Check bugs

# Work on features
/fw start 1            # Start issue #1
/prd feature-name      # Create PRD
/gt feature-name       # Generate tasks
/pt feature-name       # Process tasks

# Push changes
git add .
git commit -m "feat: implement feature"
git push

# Create PR
/fw complete 1         # Or manually on GitHub

# Both CodeRabbit and Claude Code will review automatically!
```

## Success Checklist

- [ ] Created YOUR repository (not using boilerplate repo)
- [ ] Updated `.claude/project-config.json` with YOUR repo
- [ ] Installed CodeRabbit on YOUR repo
- [ ] Installed Claude Code GitHub App on YOUR repo
- [ ] Created `.coderabbit.yaml` configuration
- [ ] Ran `/init-project` and created PROJECT_PRD
- [ ] Generated issues with `/gi PROJECT` in YOUR repo
- [ ] Tested PR creation and saw both bots respond
- [ ] No references to boilerplate repo remain

## Next Steps

1. Start with your first feature: `/fw start 1`
2. Create detailed PRD: `/prd feature-name`
3. Let the system guide you through implementation
4. Watch as both AI systems ensure quality!

---

Remember: The boilerplate is just a template. Once copied, everything should reference YOUR repository, not the boilerplate origin.
