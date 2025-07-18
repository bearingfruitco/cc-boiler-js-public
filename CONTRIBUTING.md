# Contributing to Claude Code Boilerplate

Thank you for your interest in contributing! This boilerplate evolves with community usage and feedback.

## 🤝 How to Contribute

### 1. Report Issues
- Use GitHub Issues to report bugs
- Include reproduction steps
- Mention your environment (OS, Node version, etc.)

### 2. Suggest Features
- Open a GitHub Issue with the `feature` label
- Describe the use case
- Include examples if possible

### 3. Submit Pull Requests
- Fork the repository
- Create a feature branch (`git checkout -b feature/amazing-feature`)
- Commit your changes (`git commit -m 'Add amazing feature'`)
- Push to the branch (`git push origin feature/amazing-feature`)
- Open a Pull Request

## 📋 Contribution Guidelines

### Code Style
- Follow the existing design system (4 sizes, 2 weights, 4px grid)
- Use TypeScript with strict mode
- Run `/vd` to validate design compliance
- Ensure all tests pass

### Commits
- Use conventional commits:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation
  - `chore:` for maintenance
  - `refactor:` for code improvements

### Documentation
- Update relevant documentation
- Add examples for new features
- Keep the QUICK_REFERENCE.md updated

### Testing
- Add tests for new functionality
- Ensure existing tests pass
- Test with `/btf` for UI changes

## 🎯 Areas We Need Help

### 1. Custom Commands
Share your custom commands that improve workflow

### 2. PRP Templates
Create templates for common use cases

### 3. Documentation
- Improve existing guides
- Add video tutorials
- Translate to other languages

### 4. Integrations
- Additional MCP servers
- Third-party service integrations
- CI/CD workflows

### 5. Performance
- Optimize command execution
- Reduce token usage
- Improve build times

## 🏗️ Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/claude-code-boilerplate.git
cd claude-code-boilerplate

# Install dependencies
pnpm install

# Create .env.local
cp .env.example .env.local

# Start development
pnpm dev
```

## 🧪 Testing

```bash
# Run all tests
pnpm test

# Type checking
pnpm typecheck

# Linting
pnpm lint

# Design validation
/vd
```

## 📝 Pull Request Process

1. Update documentation
2. Add tests if applicable
3. Ensure CI passes
4. Request review from maintainers
5. Address feedback
6. Celebrate when merged! 🎉

## 🌟 Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

## 💬 Questions?

- Open a GitHub Discussion
- Check existing issues
- Read the documentation

## 📜 Code of Conduct

Be respectful, inclusive, and constructive. We're all here to build better tools together.

---

Thank you for helping make Claude Code Boilerplate better for everyone! 🚀
