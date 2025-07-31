---
name: notify-settings
description: Configure smart notification preferences
argument-hint: [show | set <option> <value> | test]
allowed-tools: Read, Write, CreateFile, Bash
aliases: ["notifications", "notify", "alert-settings"]
---

# 🔔 Smart Notification Settings

Managing notification settings: **$ARGUMENTS**

## Processing Command

!`python3 << 'PYTHON'
import json
from pathlib import Path
from datetime import datetime

# Parse arguments
args = """$ARGUMENTS""".strip().split()
command = args[0] if args else "show"

# Settings file
settings_file = Path(".claude/settings.json")

# Load current settings
if settings_file.exists():
    with open(settings_file, 'r') as f:
        settings = json.load(f)
else:
    settings = {}

# Ensure notifications section exists
if 'notifications' not in settings:
    settings['notifications'] = {
        'enabled': True,
        'short_task': 30,
        'medium_task': 60,
        'long_task': 180,
        'quiet_hours_start': 22,
        'quiet_hours_end': 8,
        'channels': {
            'desktop': True,
            'tts': True,
            'slack': False
        },
        'importance_thresholds': {
            'high': 'always',
            'medium': 'long_tasks',
            'low': 'very_long_tasks'
        }
    }

notif_settings = settings['notifications']

if command == "show":
    print("## 🔔 Current Notification Settings\n")
    
    print(f"**Status**: {'✅ Enabled' if notif_settings['enabled'] else '❌ Disabled'}")
    
    print("\n### ⏱️ Task Duration Thresholds")
    print(f"- **Short Tasks**: {notif_settings['short_task']}s")
    print(f"- **Medium Tasks**: {notif_settings['medium_task']}s")
    print(f"- **Long Tasks**: {notif_settings['long_task']}s")
    
    print("\n### 🌙 Quiet Hours")
    print(f"- **Start**: {notif_settings['quiet_hours_start']}:00")
    print(f"- **End**: {notif_settings['quiet_hours_end']}:00")
    
    current_hour = datetime.now().hour
    start = notif_settings['quiet_hours_start']
    end = notif_settings['quiet_hours_end']
    
    in_quiet = False
    if start > end:  # Crosses midnight
        in_quiet = current_hour >= start or current_hour < end
    else:
        in_quiet = start <= current_hour < end
    
    print(f"- **Currently**: {'🌙 In quiet hours' if in_quiet else '☀️ Active hours'}")
    
    print("\n### 📢 Notification Channels")
    channels = notif_settings.get('channels', {})
    for channel, enabled in channels.items():
        status = '✅' if enabled else '❌'
        print(f"- {status} {channel.title()}")
    
    print("\n### 🎯 Importance Handling")
    importance = notif_settings.get('importance_thresholds', {})
    print(f"- **High Priority**: {importance.get('high', 'always')}")
    print(f"- **Medium Priority**: {importance.get('medium', 'long_tasks')}")
    print(f"- **Low Priority**: {importance.get('low', 'very_long_tasks')}")

elif command == "set":
    if len(args) < 3:
        print("❌ Usage: /notify-settings set <option> <value>")
        print("\nAvailable options:")
        print("- enabled: true/false")
        print("- short_task: seconds (default 30)")
        print("- medium_task: seconds (default 60)")
        print("- long_task: seconds (default 180)")
        print("- quiet_hours_start: hour (0-23)")
        print("- quiet_hours_end: hour (0-23)")
        print("- desktop: true/false")
        print("- tts: true/false")
        print("- slack: true/false")
    else:
        option = args[1]
        value = args[2]
        
        # Handle boolean values
        if value.lower() in ['true', 'yes', 'on', '1']:
            value = True
        elif value.lower() in ['false', 'no', 'off', '0']:
            value = False
        else:
            try:
                value = int(value)
            except:
                pass
        
        # Update settings
        if option == 'enabled':
            notif_settings['enabled'] = bool(value)
        elif option in ['short_task', 'medium_task', 'long_task']:
            notif_settings[option] = int(value)
        elif option in ['quiet_hours_start', 'quiet_hours_end']:
            notif_settings[option] = int(value)
        elif option in ['desktop', 'tts', 'slack']:
            if 'channels' not in notif_settings:
                notif_settings['channels'] = {}
            notif_settings['channels'][option] = bool(value)
        else:
            print(f"❌ Unknown option: {option}")
            exit(1)
        
        # Save settings
        settings['notifications'] = notif_settings
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
        
        print(f"✅ Updated {option} to {value}")
        print(f"\n💾 Settings saved to {settings_file}")

elif command == "test":
    print("## 🧪 Testing Notifications\n")
    
    # Test desktop notification
    print("📱 Sending desktop notification...")
    import os
    import sys
    
    platform = sys.platform
    test_message = "Claude Code test notification"
    
    if platform == 'darwin':
        os.system(f'''osascript -e 'display notification "{test_message}" with title "Claude Code" sound name "Glass"' ''')
        print("✅ Desktop notification sent (macOS)")
        
        if notif_settings.get('channels', {}).get('tts', True):
            print("\n🔊 Testing TTS...")
            os.system(f'say "{test_message}"')
            print("✅ TTS test complete")
    
    elif platform.startswith('linux'):
        result = os.system(f'notify-send "Claude Code" "{test_message}"')
        if result == 0:
            print("✅ Desktop notification sent (Linux)")
        else:
            print("❌ notify-send not found. Install libnotify-bin")
        
        if notif_settings.get('channels', {}).get('tts', True):
            print("\n🔊 Testing TTS...")
            if os.system('which espeak > /dev/null 2>&1') == 0:
                os.system(f'espeak "{test_message}" 2>/dev/null')
                print("✅ TTS test complete (espeak)")
            else:
                print("❌ espeak not found. Install espeak for TTS")
    
    else:
        print(f"⚠️  Platform {platform} - using console notification")
        print(f"🔔 {test_message}")
    
    print("\n✅ Notification test complete!")

else:
    print(f"❌ Unknown command: {command}")
    print("Usage: /notify-settings [show|set|test]")

PYTHON`

## Examples

### View current settings
```
/notify-settings show
```

### Enable/disable notifications
```
/notify-settings set enabled false
/notify-settings set enabled true
```

### Adjust thresholds
```
/notify-settings set medium_task 120  # 2 minutes
/notify-settings set long_task 300    # 5 minutes
```

### Configure quiet hours
```
/notify-settings set quiet_hours_start 22  # 10 PM
/notify-settings set quiet_hours_end 7      # 7 AM
```

### Toggle channels
```
/notify-settings set desktop true
/notify-settings set tts false
/notify-settings set slack true
```

### Test notifications
```
/notify-settings test
```

## Next Steps

- Test your settings: `/notify-settings test`
- Run a long task: `/orch "complex feature"`
- Monitor notifications: `tail -f .claude/logs/notifications.log`
- Create notification rules: `/notify-rules`
