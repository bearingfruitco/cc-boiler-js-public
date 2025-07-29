# Architecture Phase - Quick Implementation Checklist

## Immediate Actions (Can Do Now)

### 1. For Debt-Tofu-Report Project (Manual Architecture)
```bash
# Use these commands to manually create architecture
/ultrathink complete system architecture for debt relief quiz
/create-prp system architecture design
/create-prp database schema design
/create-prp api architecture design
/create-prp frontend component architecture

# Create architecture docs manually
/write docs/architecture/SYSTEM_DESIGN.md
/write docs/architecture/DATABASE_SCHEMA.md
/write docs/architecture/API_SPECIFICATION.md
/write docs/architecture/FRONTEND_ARCHITECTURE.md
/write docs/architecture/TECHNICAL_ROADMAP.md
```

### 2. Quick Boilerplate Enhancement (Minimal Version)

#### Step 1: Update chains.json
Add this to the chains section:
```json
"architecture-design": {
  "description": "Design system architecture from PRD",
  "commands": [
    "ultrathink system architecture",
    "create-prp database design",
    "create-prp api design", 
    "create-prp frontend design",
    "create-prp integration design"
  ]
}
```

#### Step 2: Create Simple Hook
Create `.claude/hooks/pre-tool-use/17-architecture-check.py`:
```python
#!/usr/bin/env python3
import json
import sys
import os

input_data = json.loads(sys.stdin.read())
tool_name = input_data.get('tool_name', '')
parameters = input_data.get('parameters', {})

# Check if trying to generate issues without architecture
if tool_name == 'execute_command':
    command = parameters.get('command', '')
    if command.startswith('/gi PROJECT'):
        arch_dir = 'docs/architecture'
        if not os.path.exists(arch_dir) or not os.listdir(arch_dir):
            print(json.dumps({
                "action": "block",
                "message": "❌ Architecture not found!\n\nPlease design your system architecture first:\n1. /chain architecture-design\n2. Or manually: /ultrathink system architecture\n\nThis ensures proper technical planning before implementation."
            }))
            sys.exit(0)

# Allow all other operations
sys.exit(0)
```

#### Step 3: Update Command Suggestion
Add to `.claude/hooks/post-tool-use/01a-next-command-suggestions.py`:
```python
# After init-project completion
if 'PROJECT_PRD.md created' in output:
    suggestions.append({
        'command': '/chain architecture-design',
        'reason': 'Design system architecture before creating issues'
    })
```

### 3. Test the Flow

1. In debt-tofu-report:
   ```bash
   /chain architecture-design
   ```

2. Then proceed with:
   ```bash
   /gi PROJECT
   ```

## Full Implementation Plan

### Phase 1: Commands (2 days)
- [ ] Create `/create-architecture` command
- [ ] Add PRD analysis logic
- [ ] Generate architecture templates
- [ ] Create `/arch` alias

### Phase 2: Agent (1 day)
- [ ] Create system-architect agent
- [ ] Add to agent roster
- [ ] Test with sample PRDs

### Phase 3: Integration (2 days)
- [ ] Update chains.json properly
- [ ] Create enforcement hooks
- [ ] Update existing commands
- [ ] Add to workflow guides

### Phase 4: Testing (1 day)
- [ ] Test with debt-tofu-report
- [ ] Test with new project
- [ ] Document findings
- [ ] Create examples

## Benefits Once Implemented

1. **Clear Technical Vision**: No more ad-hoc design decisions
2. **Parallel Development**: Teams can work on separate components
3. **Better Issues**: Issues derived from architecture are more actionable
4. **Reduced Rework**: Catch integration issues before coding
5. **Faster Delivery**: Less time spent on refactoring

## Next Steps

1. **For Your Project**: Use the manual architecture approach above
2. **For Boilerplate**: Implement the quick version first
3. **Long Term**: Follow the full implementation plan

This ensures every project has proper technical design before jumping into code!
