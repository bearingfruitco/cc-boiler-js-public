#!/usr/bin/env python3
import json
from collections import defaultdict

# Read aliases
with open('/Users/shawnsmith/dev/bfc/boilerplate/.claude/aliases.json', 'r') as f:
    aliases = json.load(f)

# Group by command to see duplicates
command_to_aliases = defaultdict(list)
for alias, command in aliases.items():
    command_to_aliases[command].append(alias)

# Find commands with too many aliases
print("🔍 Commands with excessive aliases:\n")
excessive = []
for command, alias_list in sorted(command_to_aliases.items(), key=lambda x: len(x[1]), reverse=True):
    if len(alias_list) >= 3:  # 3 or more aliases
        excessive.append((command, alias_list))

# Show worst offenders first
for cmd, alias_list in excessive[:15]:
    print(f"❌ '{cmd}' has {len(alias_list)} aliases:")
    print(f"   Aliases: /{', /'.join(sorted(alias_list))}")
    
    # Suggest which to keep
    short_aliases = [a for a in alias_list if len(a) <= 3]
    medium_aliases = [a for a in alias_list if 3 < len(a) <= 6]
    
    if short_aliases:
        print(f"   ✅ Keep: /{short_aliases[0]}")
        if len(short_aliases) > 1:
            print(f"   ⚠️  Remove: {', '.join(['/' + a for a in short_aliases[1:]])}")
    elif medium_aliases:
        print(f"   ✅ Keep: /{medium_aliases[0]}")
    
    if len(alias_list) > len(short_aliases):
        remove = [a for a in alias_list if a not in short_aliases[:1]]
        if short_aliases:
            remove = [a for a in alias_list if a != short_aliases[0]]
        elif medium_aliases:
            remove = [a for a in alias_list if a != medium_aliases[0]]
        if len(remove) > 0 and len(remove) < len(alias_list):
            print(f"   🗑️  Remove: /{', /'.join(remove)}")
    print()

# Summary stats
total_aliases = len(aliases)
unique_commands = len(command_to_aliases)
commands_with_3plus = len([c for c, a in command_to_aliases.items() if len(a) >= 3])
commands_with_4plus = len([c for c, a in command_to_aliases.items() if len(a) >= 4])

print(f"\n📊 Summary:")
print(f"Total aliases: {total_aliases}")
print(f"Unique commands: {unique_commands}")
print(f"Commands with 3+ aliases: {commands_with_3plus}")
print(f"Commands with 4+ aliases: {commands_with_4plus}")
print(f"Average aliases per command: {total_aliases/unique_commands:.1f}")

# Recommend reduction
recommended_aliases = 0
for cmd, alias_list in command_to_aliases.items():
    if len(alias_list) == 1:
        recommended_aliases += 1
    else:
        recommended_aliases += min(2, len(alias_list))  # Max 2 aliases per command

print(f"\n💡 Recommendation:")
print(f"Reduce from {total_aliases} to ~{recommended_aliases} aliases")
print(f"That's a {((total_aliases - recommended_aliases) / total_aliases * 100):.0f}% reduction!")
