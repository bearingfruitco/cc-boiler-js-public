#!/usr/bin/env python3
import json
import os
from pathlib import Path

# Read aliases
with open('/Users/shawnsmith/dev/bfc/boilerplate/.claude/aliases.json', 'r') as f:
    aliases = json.load(f)

# Get all command files
commands_dir = Path('/Users/shawnsmith/dev/bfc/boilerplate/.claude/commands')
all_files = list(commands_dir.glob('*.md'))

# Separate aliases from actual commands
alias_files = []
actual_commands = []
unknown_aliases = []

for file in all_files:
    filename = file.stem  # filename without .md
    if filename in aliases:
        alias_files.append(filename)
    else:
        actual_commands.append(filename)

# Find aliases that don't have files
for alias in aliases:
    if alias not in [f.stem for f in all_files]:
        unknown_aliases.append(alias)

print(f"📊 Command Analysis:")
print(f"Total .md files in commands dir: {len(all_files)}")
print(f"Alias command files: {len(alias_files)}")
print(f"Actual command files: {len(actual_commands)}")
print(f"Total aliases defined: {len(aliases)}")
print(f"Missing alias files: {len(unknown_aliases)}")

print(f"\n📁 Breakdown:")
print(f"- Unique actual commands: {len(actual_commands)}")
print(f"- Alias shortcuts created: {len(alias_files)}")
print(f"- Total available commands: {len(all_files)}")

# Show some actual commands
print(f"\n📝 Sample actual commands (first 20):")
for cmd in sorted(actual_commands)[:20]:
    print(f"  /{cmd}")

# Show if any aliases are missing
if unknown_aliases:
    print(f"\n⚠️  Aliases without files:")
    for alias in unknown_aliases[:10]:
        print(f"  {alias} → {aliases[alias]}")
