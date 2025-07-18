# GitHub Repository Settings Guide

This guide helps you configure recommended GitHub settings for your public repository.

## 🛡️ Branch Protection Rules

After making your repository public, configure these branch protection rules for the `main` branch:

### 1. Navigate to Settings
1. Go to your repository on GitHub
2. Click **Settings** → **Branches**
3. Click **Add rule** or **Add branch protection rule**

### 2. Configure Protection for `main`
Set the following options:

#### ✅ Required Settings
- **Branch name pattern**: `main`
- **Require a pull request before merging**: ✅
  - **Require approvals**: ✅ (at least 1)
  - **Dismiss stale pull request approvals when new commits are pushed**: ✅
- **Require status checks to pass before merging**: ✅
  - Add these checks if available:
    - `CodeRabbit` (automated code review)
    - `build` (if you have CI/CD)
    - `typecheck` (TypeScript validation)
    - `lint` (code style checks)
- **Require branches to be up to date before merging**: ✅
- **Include administrators**: ❌ (optional, but recommended OFF for flexibility)

#### 🔒 Additional Security Options
- **Require signed commits**: ✅ (optional but recommended)
- **Require linear history**: ✅ (keeps git history clean)
- **Require deployments to succeed**: ✅ (if using Vercel/Netlify)
- **Lock branch**: ❌ (keep OFF - too restrictive)

### 3. Save Protection Rules
Click **Create** or **Save changes**

## 📋 Repository Settings

### General Settings
1. **Features** (Settings → General → Features)
   - **Issues**: ✅ Enable
   - **Projects**: ✅ Enable (for kanban boards)
   - **Wiki**: ❌ Disable (use docs in repo instead)
   - **Discussions**: ✅ Enable (for community Q&A)

2. **Pull Requests** (Settings → General → Pull Requests)
   - **Allow merge commits**: ✅
   - **Allow squash merging**: ✅ (recommended default)
   - **Allow rebase merging**: ✅
   - **Automatically delete head branches**: ✅

### Security Settings
1. **Code security and analysis** (Settings → Security & analysis)
   - **Dependency graph**: ✅ Enable
   - **Dependabot alerts**: ✅ Enable
   - **Dependabot security updates**: ✅ Enable
   - **Code scanning**: ✅ Enable (if available)
   - **Secret scanning**: ✅ Enable

2. **Secrets and variables** (Settings → Secrets and variables → Actions)
   - Add any required secrets for GitHub Actions
   - Never commit actual secrets to the repository

## 🤖 GitHub Apps

Ensure these apps are installed on your repository:

1. **CodeRabbit**
   - Real-time code review
   - Design system enforcement
   - Bug detection
   - Install at: https://github.com/marketplace/coderabbit

2. **Claude Code** (if you have access)
   - AI development assistance
   - PRD alignment validation
   - Install at: https://github.com/apps/claude

## 👥 CODEOWNERS

The repository includes a `CODEOWNERS` file that automatically assigns reviewers. Update it with your team members:

```
# Global owners
* @your-username @team-member

# Specific areas
/docs/ @documentation-team
/security/ @security-team
```

## 🏷️ Labels

Create these helpful labels for issues and PRs:

### Priority Labels
- `priority: critical` (color: #FF0000)
- `priority: high` (color: #FF6B6B)
- `priority: medium` (color: #FFE66D)
- `priority: low` (color: #4ECDC4)

### Type Labels
- `type: bug` (color: #EE0701)
- `type: feature` (color: #84B6EB)
- `type: docs` (color: #1D76DB)
- `type: security` (color: #FF0000)
- `type: performance` (color: #F9A825)

### Status Labels
- `status: in-progress` (color: #FEF3C7)
- `status: blocked` (color: #F87171)
- `status: needs-review` (color: #C084FC)

## 📝 Issue Templates

Consider adding issue templates in `.github/ISSUE_TEMPLATE/`:
- Bug report template
- Feature request template
- Security vulnerability template

## 🚀 GitHub Actions

If using GitHub Actions, consider these workflows:
- CI/CD pipeline
- Security scanning
- Dependency updates
- Automated releases

## 💡 Tips

1. **Start with minimal protection** and add more as needed
2. **Document your contribution guidelines** in CONTRIBUTING.md
3. **Use semantic versioning** for releases
4. **Tag releases** for easy reference
5. **Keep your main branch stable** - use feature branches

## 🔗 Useful Links

- [GitHub Docs: Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)
- [GitHub Docs: CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [GitHub Docs: Security Features](https://docs.github.com/en/code-security/getting-started/github-security-features)
