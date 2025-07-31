#!/bin/bash
# Create all alias command files from aliases.json

echo "🔧 Creating all alias command files..."

cd /Users/shawnsmith/dev/bfc/boilerplate/.claude

# Read aliases.json and create command files
python3 << 'EOF'
import json
import os

# Read aliases
with open('aliases.json', 'r') as f:
    aliases = json.load(f)

# Change to commands directory
os.chdir('commands')

# Track what we create
created = []
skipped = []

for alias, command in aliases.items():
    # Skip if alias file already exists
    if os.path.exists(f"{alias}.md"):
        skipped.append(alias)
        continue
    
    # Create alias command file
    content = f"""# {alias.upper()} Alias

$ARGUMENTS

This is an alias for /{command.replace(' ', '-')}
"""
    
    # Special handling for subagent commands
    if "use " in command and " subagent to" in command:
        content = f"""# {alias.upper()} Alias

Use the {command}
$ARGUMENTS
"""
    
    with open(f"{alias}.md", 'w') as f:
        f.write(content)
    
    created.append(alias)

print(f"✅ Created {len(created)} alias files")
print(f"⏭️  Skipped {len(skipped)} existing files")

# Show important aliases created
important = ['cti', 'gi', 'ctf', 'sc', 'ws', 'td', 'tb', 'orch', 'spawn', 'ut', 'vp']
print("\nImportant aliases created:")
for alias in important:
    if alias in created:
        print(f"  /{alias} → {aliases[alias]}")
EOF

echo ""
echo "📝 All alias commands created!"
