# Maintenance Scripts

This directory contains scripts for maintaining and analyzing the Claude Code Boilerplate system.

## Scripts

### analyze-alias-duplication.py
Analyzes command aliases to find duplicates and excessive aliasing.

**Usage:**
```bash
python analyze-alias-duplication.py
```

**Output:**
- Commands with 3+ aliases
- Recommendations for which aliases to keep/remove
- Summary statistics

### analyze-commands.py
Analyzes the command structure and finds issues like duplicates or missing files.

**Usage:**
```bash
python analyze-commands.py
```

### clean-aliases.sh
Creates a recommended set of aliases with only 1-2 aliases per command.

**Usage:**
```bash
./clean-aliases.sh
```

**Output:**
- Creates `aliases-recommended.json` with cleaned aliases
- Shows reduction statistics

### create-all-aliases.sh
Generates all command aliases from the command files.

**Usage:**
```bash
./create-all-aliases.sh
```

### fix-commands.sh
Fixes common issues in command files like missing aliases or incorrect formatting.

**Usage:**
```bash
./fix-commands.sh
```

## Best Practices

1. **Run analysis before cleanup**: Always run the analyze scripts first to understand the current state
2. **Backup before changes**: The scripts create backups, but verify them
3. **Test after changes**: Run `/help` in Claude Code to ensure commands still work
4. **Document changes**: Update the changelog when making significant changes

## Maintenance Schedule

Recommended maintenance tasks:
- **Weekly**: Run alias analysis to check for drift
- **Monthly**: Clean up excessive aliases
- **Quarterly**: Full command structure review
