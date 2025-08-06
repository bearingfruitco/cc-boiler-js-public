# GitHub Clone to Boilerplate Integration Guide

> **The Complete Guide**: Clone any GitHub repository and safely integrate the Claude Code Boilerplate v4.0.0 without breaking anything.

## 🎯 Quick Start - The Real Process (5 Minutes)

```bash
# 1. Go to your dev directory
cd ~/dev  # or wherever you keep projects

# 2. Clone the project you want to work on
git clone https://github.com/[user]/[project].git
cd [project]

# 3. Download and run the integration script FROM THE INTERNET
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-existing.sh | bash

# 4. Open in Claude Code
claude .

# 5. Start using boilerplate commands (they exist now!)
/sr                        # Load everything
/analyze-existing full     # Understand project
/fw start                  # Start building!
```

## 📍 Understanding the Process

### Starting Point
You have:
- Your development directory (e.g., `~/dev` or `/Users/yourname/dev`)
- A GitHub project URL you want to work on
- No boilerplate installed yet

### What Actually Happens

**Step 1: Get Your Project**
```bash
cd ~/dev
git clone https://github.com/user/some-project.git
cd some-project
```
Now you have the project on your computer at `~/dev/some-project`

**Step 2: Get and Run the Integration Script**
```bash
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-existing.sh | bash
```
This command:
- Downloads the script FROM THE INTERNET (from GitHub)
- Runs it immediately
- The script then downloads the boilerplate and installs it INTO your project

**Step 3: Use Claude Code**
```bash
claude .
/sr  # These commands work now because the boilerplate is installed!
```

## 🔑 Key Points to Understand

### You DON'T Need To:
- ❌ Clone the boilerplate repository yourself
- ❌ Have the integration script beforehand
- ❌ Manually copy or merge folders
- ❌ Download the boilerplate separately

### The Script Does Everything:
1. Downloads the boilerplate to a temp folder
2. Copies boilerplate files INTO your project
3. Handles any conflicts intelligently
4. Cleans up temp files
5. Reports what was done

### Why This Works:
- The integration script lives on GitHub
- `curl` can download files from any URL
- The script knows how to get the boilerplate and install it

## 📊 Visual Flow

```
Your Computer:
~/dev/
│
├── Step 1: Clone project from GitHub
│   └── some-project/  (just the project, no boilerplate)
│
├── Step 2: Run curl command
│   ├── Downloads script from GitHub
│   ├── Script downloads boilerplate to /tmp/
│   ├── Script copies boilerplate INTO some-project/
│   └── Script cleans up /tmp/
│
└── Result: some-project/  (now has boilerplate!)
    ├── .claude/        (150+ commands) ← Added by script
    ├── .agent-os/      (standards)     ← Added by script
    ├── field-registry/ (security)      ← Added by script
    ├── PRPs/          (templates)      ← Added by script
    └── [original project files]        ← Untouched
```

## 🚀 Complete Real-World Example

Let's say you want to work on a Next.js project called "debt-funnel":

```bash
# 1. Go to your development directory
cd /Users/shawnsmith/dev/bfc

# 2. Clone the debt-funnel project
git clone https://github.com/bearingfruitco/debt-funnel.git
cd debt-funnel

# 3. Get and run the integration script from the internet
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-existing.sh | bash

# The script will output:
# ✓ Downloading boilerplate...
# ✓ Creating backup...
# ✓ Integrating .claude directory...
# ✓ Installing Agent OS...
# ✓ Integration complete!

# 4. Open in Claude Code
claude .

# 5. Now these commands work:
/sr
/analyze-existing full
/fw start
```

## 🔧 Integration Methods Explained

### Method 1: Direct Run (Simplest)
```bash
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-existing.sh | bash
```
Downloads and runs immediately.

### Method 2: Download First (Safer)
```bash
# Download the script so you can see it
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-existing.sh -o integrate.sh

# Look at what it does
cat integrate.sh

# Run it
chmod +x integrate.sh
./integrate.sh
```
Lets you review the script before running.

### Method 3: Preview Mode
```bash
# Download script
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-existing.sh -o integrate.sh
chmod +x integrate.sh

# See what it would do without making changes
./integrate.sh --dry-run

# If happy, run for real
./integrate.sh
```

## 📋 What the Integration Script Does

1. **Checks Prerequisites**
   - Verifies git is installed
   - Checks if you're in a git repo
   - Warns if anything is missing

2. **Detects Existing Boilerplate**
   - Looks for `.claude/VERSION`
   - Detects v1.0, v2.0, v3.0, v3.5, or v4.0
   - Skips if already v4.0

3. **Downloads Boilerplate**
   - Clones boilerplate to `/tmp/claude-boilerplate-[random]`
   - Gets latest v4.0.0 from GitHub

4. **Creates Backup**
   - Saves existing files to `.claude-integration/backup/[timestamp]`
   - Preserves your customizations

5. **Integrates Intelligently**
   - **Your files**: Never overwritten
   - **Your commands**: Renamed with `-project` suffix
   - **Your CLAUDE.md**: Kept, ours becomes `CLAUDE_BOILERPLATE.md`
   - **New directories**: Added (`.claude/`, `.agent-os/`, etc.)

6. **Cleans Up**
   - Removes temp files
   - Generates report
   - Shows next steps

## 🛡️ Safety Features

### Automatic Backup
```bash
.claude-integration/
└── backup/
    └── 20250206_143022/  # Timestamp
        ├── .claude/      # Your original files
        ├── CLAUDE.md
        └── metadata.json
```

### Dry Run Mode
```bash
./integrate.sh --dry-run
# Shows what would happen without making changes
```

### Rollback
```bash
# If something goes wrong
cp -r .claude-integration/backup/[latest]/* .
```

## ❓ Common Questions

### Q: Where does the integration script come from?
**A:** It's downloaded from GitHub using curl. The script lives at:
`https://github.com/bearingfruitco/claude-code-boilerplate/blob/main/scripts/integrate-existing.sh`

### Q: Do I need to clone the boilerplate repo?
**A:** No! The script does that for you automatically in a temp folder.

### Q: What if I don't have curl?
**A:** Use wget instead:
```bash
wget -qO- https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-existing.sh | bash
```

### Q: What if the script fails?
**A:** Check:
- Internet connection (to download from GitHub)
- Git is installed (`git --version`)
- You're in the right directory (`pwd`)
- Permissions (`ls -la`)

### Q: Can I run it multiple times?
**A:** Yes! It detects existing installations and handles them properly.

## 🔄 Handling Existing Versions

If your project already has an older boilerplate:

```bash
# The script detects the version automatically
# After integration, in Claude Code:
/boilerplate-version    # Check what you have
/upgrade-boilerplate    # Upgrade to v4.0 if needed
```

## 📊 Integration Modes

### Full Mode (Default)
```bash
./integrate.sh --mode=full
```
Integrates everything with smart conflict resolution.

### Selective Mode
```bash
./integrate.sh --mode=selective
```
Choose specific components to integrate.

### Sidecar Mode
```bash
./integrate.sh --mode=sidecar
```
Installs as `.claude-boilerplate/` (no conflicts).

## 🎯 Next Steps After Integration

1. **Verify Installation**
   ```bash
   claude .
   /sr                  # Should work
   /help               # Shows 150+ commands
   ```

2. **Configure Project**
   ```bash
   /config set project.name "Your Project"
   /analyze-existing full
   ```

3. **Start Building**
   ```bash
   /fw start feature
   /create-prp implementation
   ```

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| "curl: command not found" | Use `wget -qO-` instead |
| "Permission denied" | Use `chmod +x integrate.sh` |
| "/sr command not found" | Script didn't complete - check `.claude/` exists |
| "Already have v4.0" | You're good! Use `/upgrade-boilerplate` to refresh |
| Script fails | Check internet connection, try downloading manually |

## 📚 The Key Insight

**You don't need the boilerplate or its scripts beforehand!**

The curl command downloads the integration script FROM THE INTERNET, and that script handles everything else. It's all automatic!

---

*Last Updated: January 2025 | Version 4.0.0*
