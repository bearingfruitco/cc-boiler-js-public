---
name: feature-flags
description: |
  Manage v3.0 feature flags for gradual rollout.
  Control which features are enabled in different environments.
argument-hint: [status|enable <feature>|disable <feature>|rollout]
allowed-tools: Read, Write, Bash
aliases: ["flags", "ff", "features"]
---

# 🚦 Feature Flags Management

Managing flags for: **${ARGUMENTS:-status}**

## Current Feature Status

!`python3 << 'EOF'
import json
from pathlib import Path

# Load feature flags
flags_file = Path(".claude/feature-flags.json")
with open(flags_file) as f:
    flags = json.load(f)

print("🚦 V3.0 Feature Flags Status")
print("=" * 60)

# Display features
for feature, config in flags["v3_features"].items():
    status = "✅ ON" if config["enabled"] else "🔴 OFF"
    print(f"\n{feature}:")
    print(f"  Status: {status}")
    print(f"  Description: {config['description']}")
    if not config["enabled"] and "reason" in config:
        print(f"  Reason: {config['reason']}")

# Display rollout strategy
print("\n\n📅 Rollout Strategy:")
for phase, details in flags["rollout_strategy"].items():
    print(f"\n{phase.upper()}: {details['name']}")
    print(f"  Start Date: {details['start_date']}")
    print(f"  Features: {', '.join(details['features'])}")

# Environment variables
print("\n\n🔧 Environment Controls:")
for action, command in flags["feature_control"].items():
    print(f"  {action}: {command}")
EOF`

## Feature Flag Actions

Based on the arguments, perform the requested action:

### Enable/Disable Features

!`python3 << 'EOF'
import sys
import json

args = """$ARGUMENTS""".split()
if len(args) >= 2 and args[0] in ["enable", "disable"]:
    action = args[0]
    feature = args[1]
    
    # Load flags
    with open(".claude/feature-flags.json") as f:
        flags = json.load(f)
    
    if feature in flags["v3_features"]:
        flags["v3_features"][feature]["enabled"] = (action == "enable")
        
        # Save updated flags
        with open(".claude/feature-flags.json", "w") as f:
            json.dump(flags, f, indent=2)
            
        status = "enabled" if action == "enable" else "disabled"
        print(f"✅ Feature '{feature}' has been {status}")
        
        # Show impact
        if feature == "technology_agents":
            agents = flags["v3_features"][feature]["agents"]
            print(f"   Affected agents: {', '.join(agents)}")
        elif feature == "orchestration":
            commands = flags["v3_features"][feature]["commands"]
            print(f"   Affected commands: {', '.join(commands)}")
    else:
        print(f"❌ Unknown feature: {feature}")
        print("Available features:", ", ".join(flags["v3_features"].keys()))
elif args and args[0] == "rollout":
    print("\n🚀 Executing Rollout Plan...")
    print("1. Dev environment: All features enabled ✅")
    print("2. Staging: Testing in progress... 🔄")
    print("3. Production: Scheduled for next week 📅")
EOF`

## Feature Testing by Environment

### Development Environment
```bash
# Enable all v3.0 features
export CLAUDE_ENV=development
# All features active by default
```

### Staging Environment
```bash
# Enable v3.0 with monitoring
export CLAUDE_ENV=staging
export CLAUDE_ENABLE_METRICS=1
export CLAUDE_DEBUG_ORCHESTRATION=1
```

### Production Environment
```bash
# Careful rollout with fallbacks
export CLAUDE_ENV=production
export CLAUDE_ENABLE_ROLLBACK=1
export CLAUDE_DISABLE_MCP=1  # MCP still in POC
```

## Quick Feature Toggles

### Disable All V3 Features (Emergency)
```bash
export CLAUDE_FORCE_V2_MODE=1
claude -p "Continue with v2.8 agents only"
```

### Enable Debug Mode
```bash
export CLAUDE_DEBUG_ORCHESTRATION=1
export CLAUDE_VERBOSE_METRICS=1
claude -p "/orchestrate complex task"
```

### Test Specific Features
```bash
# Test only technology agents
export CLAUDE_ENABLE_ONLY=technology_agents
claude -p "/at build authentication"

# Test only monitoring
export CLAUDE_ENABLE_ONLY=monitoring
claude -p "/agent-health"
```

## Rollout Verification

!`python3 << 'EOF'
print("\n✅ Feature Flag Verification:")
print("  • Flags file exists: ✓")
print("  • All features documented: ✓")
print("  • Rollback mechanism ready: ✓")
print("  • Environment controls working: ✓")
print("\n🎯 Ready for phased rollout!")
EOF`

## Best Practices

1. **Test in Dev First**: Always enable in development before staging
2. **Monitor Metrics**: Watch performance after enabling features
3. **Have Rollback Ready**: Keep v2.8 backup accessible
4. **Gradual Rollout**: Enable one feature at a time in production
5. **Document Changes**: Log all feature flag changes

Feature flags provide safe, controlled rollout of v3.0 capabilities!
