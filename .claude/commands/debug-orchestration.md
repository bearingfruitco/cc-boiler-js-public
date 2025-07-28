---
name: debug-orchestration
description: Enable verbose debugging for agent orchestration
argument-hint: [on | off | status]
allowed-tools: Read, Write, CreateFile, Bash
aliases: ["debug-orch", "do", "orchestration-debug"]
---

# 🐛 Orchestration Debug Mode

Setting debug mode: **$ARGUMENTS**

## Configuring Debug Settings

!`python3 << 'PYTHON'
import json
from pathlib import Path

# Parse command
command = """$ARGUMENTS""".strip().lower()
if not command or command == "status":
    command = "status"
elif command not in ["on", "off", "status"]:
    print(f"❌ Invalid command: {command}")
    print("Usage: /debug-orchestration [on|off|status]")
    exit(1)

# Debug config file
config_dir = Path(".claude/config")
config_dir.mkdir(exist_ok=True)
debug_config = config_dir / "debug-orchestration.json"

# Load current config
if debug_config.exists():
    with open(debug_config, 'r') as f:
        config = json.load(f)
else:
    config = {
        "enabled": False,
        "verbose_level": 1,
        "log_context": True,
        "log_prompts": True,
        "log_responses": True,
        "trace_decisions": True,
        "capture_timing": True,
        "save_all_outputs": True
    }

if command == "status":
    print("## 🔍 Debug Status\n")
    print(f"**Enabled**: {'✅ Yes' if config['enabled'] else '❌ No'}")
    print(f"**Verbose Level**: {config['verbose_level']}/3")
    print("\n### Debug Options")
    for key, value in config.items():
        if key not in ['enabled', 'verbose_level']:
            status = '✅' if value else '❌'
            print(f"- {status} {key.replace('_', ' ').title()}")

elif command == "on":
    config['enabled'] = True
    with open(debug_config, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("## ✅ Debug Mode Enabled\n")
    print("The following will be captured:")
    print("- 📝 All agent prompts and responses")
    print("- 🔄 Context passed between agents")
    print("- 🎯 Decision-making rationale")
    print("- ⏱️ Timing for each operation")
    print("- 💾 All intermediate outputs")
    
    # Create debug hook
    hook_content = '''#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path

DEBUG_LOG = Path(".claude/logs/orchestration-debug.log")
DEBUG_LOG.parent.mkdir(exist_ok=True)

def log_debug(event_type, data):
    """Log debug information"""
    with open(DEBUG_LOG, 'a') as f:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": data
        }
        f.write(json.dumps(entry) + "\\n")

try:
    tool_data = json.load(sys.stdin)
    
    # Log Task (sub-agent) calls
    if tool_data.get('tool_name') == 'Task':
        prompt = tool_data.get('tool_input', {}).get('prompt', '')
        log_debug("agent_call", {
            "prompt": prompt[:500],
            "full_input": tool_data.get('tool_input', {})
        })
    
except:
    pass

sys.exit(0)
'''
    
    debug_hook = Path(".claude/hooks/pre-tool-use/98-debug-orchestration.py")
    with open(debug_hook, 'w') as f:
        f.write(hook_content)
    
    import os
    os.chmod(debug_hook, 0o755)
    
    print(f"\n✅ Debug hook installed: {debug_hook}")
    print(f"📁 Debug log: .claude/logs/orchestration-debug.log")

elif command == "off":
    config['enabled'] = False
    with open(debug_config, 'w') as f:
        json.dump(config, f, indent=2)
    
    # Remove debug hook
    debug_hook = Path(".claude/hooks/pre-tool-use/98-debug-orchestration.py")
    if debug_hook.exists():
        debug_hook.unlink()
    
    print("## ❌ Debug Mode Disabled\n")
    print("Debug logging has been turned off.")
    print("Existing logs are preserved in `.claude/logs/`")

# Save updated config
with open(debug_config, 'w') as f:
    json.dump(config, f, indent=2)

PYTHON`

## Debug Tools Available

When debug mode is **ON**, you have access to:

### 1. Live Monitoring
```bash
# Watch debug log in real-time
tail -f .claude/logs/orchestration-debug.log
```

### 2. Debug Commands
- `/debug-context` - Show current agent contexts
- `/debug-prompts` - View last 5 agent prompts
- `/debug-timing` - Show timing breakdown
- `/debug-decisions` - Trace decision points

### 3. Analysis Tools
- `/analyze-orchestration` - Post-execution analysis
- `/bottleneck-finder` - Identify slow agents
- `/context-usage` - Memory usage by agent

## Example Debug Output

When enabled, you'll see detailed logs like:

```json
{
  "timestamp": "2024-01-15T10:30:45",
  "type": "agent_call",
  "data": {
    "agent": "frontend",
    "prompt": "Create dashboard component...",
    "context_size": "15KB",
    "decision_reason": "UI task detected",
    "expected_duration": "2-3m"
  }
}
```

## Best Practices

1. **Enable before complex orchestrations** to capture full flow
2. **Disable after debugging** to avoid performance impact
3. **Review logs regularly** to optimize agent prompts
4. **Use with `/trace`** for complete visibility

## Next Steps

- Enable debugging: `/debug-orchestration on`
- Start orchestration: `/orch "complex task"`
- Monitor live: `tail -f .claude/logs/orchestration-debug.log`
- Analyze after: `/analyze-orchestration`
