# Quick Reference: GitHub Clone → Boilerplate Integration

## 🎯 The Complete Process (5 Minutes)

```bash
# 1. Go to your dev directory
cd ~/dev  # or /Users/yourname/dev

# 2. Clone the project you want to work on
git clone https://github.com/[user]/[project].git
cd [project]

# 3. Download and run integration script FROM THE INTERNET
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-existing.sh | bash

# 4. Open in Claude Code
claude .

# 5. Use boilerplate commands (they exist now!)
/sr
/analyze-existing full
/fw start
```

## 🔑 The Key Understanding

**You DON'T need to:**
- ❌ Clone the boilerplate separately
- ❌ Have the integration script beforehand  
- ❌ Manually merge folders
- ❌ Download anything else

**The curl command does EVERYTHING:**
1. Downloads the script from GitHub
2. Script downloads the boilerplate
3. Script installs it into YOUR project
4. Script cleans up
5. Done!

## 📊 What Really Happens

```
Your Computer:
~/dev/
│
├── your-project/  (after git clone)
│   └── Just your project files
│
├── Run curl command
│   ├── Downloads script from internet
│   ├── Script gets boilerplate
│   ├── Script adds to your-project/
│   └── Script cleans up
│
└── your-project/  (after script)
    ├── .claude/        ← Added
    ├── .agent-os/      ← Added
    ├── PRPs/          ← Added
    └── [your files]    ← Untouched
```

## 🚀 Real Example

```bash
# Starting in your dev directory
cd /Users/shawnsmith/dev/bfc

# Clone debt-funnel project
git clone https://github.com/bearingfruitco/debt-funnel.git
cd debt-funnel

# Get boilerplate (downloads script from internet and runs it)
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-existing.sh | bash

# Now use Claude Code
claude .
/sr  # Works because boilerplate is installed!
```

## 🔧 Script Options

### See What It Does First
```bash
# Download script
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-existing.sh -o integrate.sh

# Look at it
cat integrate.sh

# Run it
chmod +x integrate.sh
./integrate.sh
```

### Preview Mode
```bash
./integrate.sh --dry-run  # See what would happen
./integrate.sh            # Actually do it
```

### Other Modes
```bash
./integrate.sh --mode=selective  # Choose what to install
./integrate.sh --mode=sidecar   # Install as .claude-boilerplate/
```

## ❓ Common Issues

| Problem | Solution |
|---------|----------|
| No curl | Use `wget -qO- [url] \| bash` |
| Permission denied | Download first, then `chmod +x` |
| /sr not found | Script didn't finish - check `.claude/` exists |
| Already have boilerplate | Script detects and handles it |

## 📝 What Gets Added

```
your-project/
├── .claude/           # 150+ commands
│   ├── commands/     # All the commands
│   ├── agents/       # 31 AI agents
│   └── hooks/        # Automation
├── .agent-os/        # Standards
├── field-registry/   # Security
├── PRPs/            # Templates
├── templates/       # Components
└── CLAUDE_BOILERPLATE.md  # If you have CLAUDE.md
```

## 🛡️ Safety

- **Automatic backup** → `.claude-integration/backup/`
- **Never overwrites** → Your files are safe
- **Conflict handling** → Renames with `-project` suffix
- **Dry run mode** → Preview before changes

## 💡 Remember

1. **Clone your project first**
2. **Run the curl command** (downloads and runs script)
3. **Script does everything else**
4. **Open Claude Code and go!**

The integration script is downloaded FROM THE INTERNET - you don't need it beforehand!

---

**Script URL**: `https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-existing.sh`  
**Version**: 4.0.0 | **Updated**: January 2025
