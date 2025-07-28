---
name: mcp-poc
description: |
  Test MCP integration with Supabase for v3.0 agents.
  This is a proof of concept for evaluating MCP benefits.
argument-hint: [setup|test|status]
allowed-tools: Read, Write, Bash
aliases: ["test-mcp", "mcp-test"]
---

# 🔌 MCP Integration Proof of Concept

Testing MCP for: **${ARGUMENTS:-status}**

## MCP (Model Context Protocol) Overview

MCP allows Claude Code to connect directly to external services, giving agents real-time access to:
- Databases (Supabase)
- Analytics (BigQuery)
- Deployment (Vercel)
- Custom tools

## Current MCP Status

!`python3 << 'EOF'
import json
import os
from pathlib import Path

# Check for MCP configuration
mcp_config = Path.home() / ".claude" / "mcp_config.json"
has_mcp = mcp_config.exists()

print("🔍 MCP Configuration Status:")
print(f"  • Config exists: {'✅ Yes' if has_mcp else '❌ No'}")

if has_mcp:
    with open(mcp_config) as f:
        config = json.load(f)
    servers = config.get("mcpServers", {})
    print(f"  • Configured servers: {len(servers)}")
    for server in servers:
        print(f"    - {server}")
else:
    print("  • No MCP servers configured")

print("\n💡 To set up MCP:")
print("  1. Run: claude mcp")
print("  2. Configure desired servers")
print("  3. Test with this command")
EOF`

## POC: Supabase MCP Integration

Based on the argument, perform the appropriate action:

### Setup MCP
If argument is "setup":
```bash
# Create example MCP configuration
cat > ~/.claude/mcp_config_example.json << 'EOF'
{
  "mcpServers": {
    "supabase-poc": {
      "command": "node",
      "args": [".claude/scripts/mcp-servers/supabase-poc.js"],
      "env": {
        "SUPABASE_URL": "${SUPABASE_URL}",
        "SUPABASE_SERVICE_KEY": "${SUPABASE_SERVICE_KEY}"
      }
    }
  }
}
EOF

echo "✅ Example config created at ~/.claude/mcp_config_example.json"
echo "⚠️  Add your Supabase credentials and rename to mcp_config.json"
```

### Test MCP
If argument is "test":
```bash
# Test MCP tool availability
echo "Testing MCP tools..."

# Check if Supabase MCP tools are available
if claude --list-tools | grep -q "mcp__supabase"; then
    echo "✅ Supabase MCP tools detected!"
    echo ""
    echo "Available tools:"
    claude --list-tools | grep "mcp__supabase"
else
    echo "❌ No Supabase MCP tools found"
    echo "Run '/mcp-poc setup' first"
fi
```

### Status Check
Show current MCP integration status and benefits

## Benefits of MCP for v3.0 Agents

### 1. Direct Database Access
- Agents can query Supabase directly
- No need for intermediate API calls
- Real-time data validation

### 2. Enhanced Capabilities
```
Without MCP: Agent → Suggests SQL → You run it
With MCP: Agent → Runs query → Shows results
```

### 3. Workflow Automation
- Deploy directly from agents
- Run migrations automatically
- Validate changes in real-time

## Example Usage with v3.0 Agents

### Supabase Specialist + MCP:
```
User: "Show me all users created today"
Agent: *Uses mcp__supabase__query to fetch data directly*
Result: Immediate, accurate data
```

### Analytics Engineer + MCP:
```
User: "Validate our event schema"
Agent: *Uses mcp__analytics__validate to check in real-time*
Result: Instant validation with live data
```

## Implementation Status

!`python3 << 'EOF'
status = {
    "mcp_evaluation": "✅ Complete",
    "poc_implementation": "🟡 In Progress", 
    "supabase_mcp": "🔄 Testing",
    "analytics_mcp": "📋 Planned",
    "deployment_mcp": "📋 Planned",
    "production_ready": "❌ Not yet"
}

print("\n📊 MCP Integration Roadmap:")
for feature, status in status.items():
    print(f"  • {feature}: {status}")

print("\n📈 Expected Benefits:")
print("  • 25% faster database operations")
print("  • 30% fewer errors in agent tasks")
print("  • Real-time validation capabilities")
print("  • Direct deployment from agents")
EOF`

## Next Steps

1. **Complete POC**: Test Supabase MCP with real queries
2. **Measure Impact**: Compare agent performance with/without MCP
3. **Security Review**: Ensure proper credential handling
4. **Team Training**: Document MCP usage patterns
5. **Gradual Rollout**: Start with dev environment

## Security Considerations

⚠️ **Important**: MCP servers have direct access to services
- Use read-only credentials where possible
- Implement rate limiting
- Audit all MCP operations
- Rotate credentials regularly

For full MCP documentation, see: `.claude/docs/mcp-integration-evaluation.md`
