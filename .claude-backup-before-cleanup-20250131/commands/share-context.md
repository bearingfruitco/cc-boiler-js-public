---
name: share-context
description: |
  Share context between agents during orchestration.
  Enables complex multi-agent workflows with state preservation.
  MUST BE USED when agents need to pass information.
argument-hint: <action> [from_agent] [to_agent] [context_key]
allowed-tools: Read, Write, CreateFile, DeleteFile, SearchFiles
aliases: ["context", "ctx", "share"]
---

# 🔄 Context Sharing System

Action: **$ARGUMENTS**

## Context Operations

Parse the arguments to determine the operation:
- `store <from_agent> <data>` - Store context from an agent
- `retrieve <to_agent> <context_key>` - Retrieve context for an agent
- `share <from_agent> <to_agent> <data>` - Direct agent-to-agent sharing
- `list` - List all active contexts
- `clean` - Clean up old contexts

## Context Structure

```json
{
  "context_id": "ctx_<timestamp>_<uuid>",
  "session_id": "session_<uuid>",
  "from_agent": "agent_name",
  "to_agent": "agent_name" | "any",
  "timestamp": "ISO-8601",
  "ttl": 3600,
  "data": {
    // Agent-specific data
  },
  "metadata": {
    "workflow": "workflow_name",
    "step": 1,
    "total_steps": 5
  }
}
```

## Implementation

Based on the requested action, I'll perform the appropriate operation:

### 1. Store Context
Create a new context file in `.claude/temp/contexts/`:
```bash
mkdir -p .claude/temp/contexts
echo '{
  "context_id": "ctx_$(date +%s)_$(uuidgen)",
  "from_agent": "$FROM_AGENT",
  "data": $DATA,
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}' > .claude/temp/contexts/context_$CONTEXT_ID.json
```

### 2. Retrieve Context
Search for and return matching context:
```bash
find .claude/temp/contexts -name "*.json" -mmin -60 | while read file; do
  if jq -e ".to_agent == \"$TO_AGENT\" or .to_agent == \"any\"" "$file" > /dev/null; then
    cat "$file"
  fi
done
```

### 3. Direct Sharing
For immediate agent-to-agent context passing:
```bash
CONTEXT_FILE=".claude/temp/contexts/direct_$(date +%s).json"
echo '{
  "from": "$FROM_AGENT",
  "to": "$TO_AGENT", 
  "shared_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "data": $DATA
}' > "$CONTEXT_FILE"
```

### 4. List Active Contexts
Show all contexts less than 1 hour old:
```bash
echo "Active Contexts:"
find .claude/temp/contexts -name "*.json" -mmin -60 -exec basename {} \; | while read file; do
  echo "- $file ($(jq -r .from_agent .claude/temp/contexts/$file) → $(jq -r .to_agent .claude/temp/contexts/$file))"
done
```

### 5. Clean Old Contexts
Remove contexts older than 1 hour:
```bash
find .claude/temp/contexts -name "*.json" -mmin +60 -delete
echo "Cleaned old contexts"
```

## Example Usage Patterns

### Multi-Agent Feature Development
```
1. PM breaks down requirements → context: requirements
2. Schema architect designs → context: data_model  
3. Supabase implements → context: database_schema
4. Backend builds API → context: api_endpoints
5. Frontend creates UI → uses all contexts
```

### Complex Orchestration
```
/orchestrate "Build auth system" →
  → share-context store pm-orchestrator {requirements}
  → share-context retrieve supabase-specialist requirements
  → share-context store supabase-specialist {auth_schema}
  → share-context retrieve backend auth_schema
```

## Context Lifecycle Management

1. **Creation**: Contexts created on demand
2. **TTL**: Default 1 hour, configurable
3. **Cleanup**: Automatic after TTL expires
4. **Persistence**: Can be archived if needed
5. **Security**: Contexts are session-scoped

## Integration with Orchestration

The orchestration command automatically uses context sharing:
- Each agent stores its output as context
- Next agent retrieves relevant contexts
- Final context aggregated for user

!`python3 << 'EOF'
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Example context management
contexts_dir = Path(".claude/temp/contexts")
contexts_dir.mkdir(parents=True, exist_ok=True)

# Create example context
example_context = {
    "context_id": f"ctx_{int(datetime.now().timestamp())}_example",
    "from_agent": "supabase-specialist",
    "to_agent": "orm-specialist",
    "timestamp": datetime.utcnow().isoformat(),
    "ttl": 3600,
    "data": {
        "schema": {
            "users": {
                "id": "uuid primary key",
                "email": "text unique",
                "created_at": "timestamp"
            }
        },
        "rls_policies": [
            "users can only see their own data"
        ]
    }
}

# Save example
example_path = contexts_dir / "example_context.json"
with open(example_path, 'w') as f:
    json.dump(example_context, f, indent=2)

print("📁 Context sharing initialized")
print(f"📍 Context directory: {contexts_dir}")
print(f"📄 Example context created: {example_path}")

# Clean old contexts
for context_file in contexts_dir.glob("*.json"):
    if context_file.stat().st_mtime < (datetime.now() - timedelta(hours=1)).timestamp():
        context_file.unlink()
        print(f"🗑️  Cleaned old context: {context_file.name}")
EOF`

## Best Practices

1. **Keep contexts focused** - Only share necessary data
2. **Use consistent keys** - Standard naming for easy retrieval  
3. **Clean regularly** - Prevent context buildup
4. **Version contexts** - Include schema version in data
5. **Monitor usage** - Track context sharing patterns

Context sharing is now configured and ready for multi-agent orchestration!
