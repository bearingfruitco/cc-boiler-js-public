#!/bin/bash
# Test different hook formats to find what works

cd /Users/shawnsmith/dev/bfc/boilerplate

echo "Test 1: Current working configuration (no hooks)"
cp .claude/settings-safe-backup.json .claude/settings.json
claude doctor 2>&1 | grep -E "(invalid|error|Cannot assign)" || echo "✅ No errors"

echo -e "\nTest 2: Empty hooks object"
cat > .claude/settings.json << 'EOF'
{
  "permissions": {
    "file_system": {
      "read": true,
      "write": true
    },
    "shell": {
      "execute": true
    }
  },
  "hooks": {}
}
EOF
claude doctor 2>&1 | grep -E "(invalid|error|Cannot assign)" || echo "✅ No errors"

echo -e "\nTest 3: Simple echo hook"
cat > .claude/settings.json << 'EOF'
{
  "permissions": {
    "file_system": {
      "read": true,
      "write": true
    },
    "shell": {
      "execute": true
    }
  },
  "hooks": {
    "preToolUse": [
      {
        "command": "echo test"
      }
    ]
  }
}
EOF
claude doctor 2>&1 | grep -E "(invalid|error|Cannot assign)" || echo "✅ No errors"

echo -e "\nTest 4: Hook with matcher field"
cat > .claude/settings.json << 'EOF'
{
  "permissions": {
    "file_system": {
      "read": true,
      "write": true
    },
    "shell": {
      "execute": true
    }
  },
  "hooks": {
    "preToolUse": [
      {
        "matcher": "",
        "command": "echo test"
      }
    ]
  }
}
EOF
claude doctor 2>&1 | grep -E "(invalid|error|Cannot assign)" || echo "✅ No errors"

# Restore safe config
cp .claude/settings-safe-backup.json .claude/settings.json
echo -e "\n✅ Restored safe configuration"
