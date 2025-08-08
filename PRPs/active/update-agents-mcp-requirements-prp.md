# PRP: Update All Agents with MCP Requirements

> **Add MCP requirement declarations to all 30+ agents so they can access needed services**

## 🎯 Goal
Update every agent file to declare which MCPs they need, with proper permissions and configuration.

## 🔑 Why This Matters
- **User Value**: Agents know what tools they can use
- **Business Value**: Clear service dependencies
- **Technical Value**: Automatic permission management

## ✅ Success Criteria
- [ ] All 30+ agents updated with MCP requirements
- [ ] Permissions properly scoped per agent
- [ ] `/mcp-status` shows all agents configured
- [ ] No conflicts in permission requests
- [ ] Documentation in each agent file

## 📚 Required Context

### Source Files
- `.claude/config/mcp-registry.json` - MCP mappings
- `.claude/agents/*.md` - Agent files to update

### Update Pattern
```yaml
---
name: agent-name
mcp_requirements:
  required:
    - mcp-name  # Why needed
  optional:
    - mcp-name  # Why helpful
mcp_permissions:
  mcp-name:
    - permission:scope
---
```

## 🏗️ Implementation Tasks

### Task 1: Update Core Development Agents
```yaml
# senior-engineer.md
mcp_requirements:
  required:
    - github-mcp      # Repository operations
    - supabase-mcp    # Database access
    - sentry-mcp      # Error tracking

# frontend.md
mcp_requirements:
  required:
    - stagehand-mcp   # UI automation
  optional:
    - playwright-mcp  # E2E testing

# backend.md
mcp_requirements:
  required:
    - supabase-mcp    # Database/API
  optional:
    - redis-mcp       # Caching
```

### Task 2: Update Database Agents
```yaml
# database-architect.md - ALREADY DONE
# orm-specialist.md
# migration-specialist.md
```

### Task 3: Update Testing Agents
```yaml
# qa.md
# playwright-specialist.md
# tdd-engineer.md
```

### Task 4: Update Analytics Agents
```yaml
# analytics-engineer.md
# event-schema.md
# report-generator.md
```

### Task 5: Update Specialized Agents
```yaml
# integration-specialist.md
# supabase-specialist.md
# security-auditor.md
# pii-guardian.md
# automation-workflow-engineer.md
# researcher.md
# documentation-writer.md
```

## 🧪 Validation
- [ ] Each agent has correct MCPs listed
- [ ] Permissions match registry
- [ ] No syntax errors in YAML
- [ ] `/mcp-status` shows all configured

## 📊 Success Metrics
- **Coverage**: 30/30 agents updated
- **Accuracy**: 100% match with registry
- **Validation**: All agents pass MCP check
