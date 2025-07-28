# Agent Tool Specifications Guide

## Tool Access Patterns

### 1. Full Access Agents (Omit tools field)
These agents need access to all tools including future MCPs:

```yaml
---
name: product-manager-orchestrator
description: |
  [description]
color: gold
---
```

**Agents needing full access:**
- product-manager-orchestrator (coordinates everything)
- senior-software-engineer (implements features)
- backend-reliability-engineer (manages systems)
- migration-specialist (complex transitions)
- automation-workflow-engineer (n8n integrations)

### 2. Read-Only Analysis Agents
These agents only need to read and analyze:

```yaml
---
name: security-threat-analyst
description: |
  [description]
tools: read_file, search_files, list_directory, web_search
color: purple
---
```

**Agents with read-only access:**
- security-threat-analyst
- code-analyzer-debugger
- performance-optimizer (mostly reads, some writes)
- deep-research-specialist
- financial-analyst

### 3. Implementation Agents
These agents need read/write for specific purposes:

```yaml
---
name: frontend-ux-specialist
description: |
  [description]
tools: read_file, write_file, create_file, edit_file, search_files, list_directory
color: green
---
```

**Agents with implementation access:**
- frontend-ux-specialist
- systems-architect (for ADRs)
- qa-test-engineer
- smart-form-builder
- refactoring-expert
- database-architect

### 4. Validation/Guardian Agents
These agents need minimal access:

```yaml
---
name: production-code-validator
description: |
  [description]
tools: read_file, search_files, list_directory
color: red
---
```

**Agents with validation access:**
- production-code-validator
- pii-guardian
- technical-mentor-guide (mostly reads)

### 5. Documentation/Reporting Agents
These agents need specific access patterns:

```yaml
---
name: report-generator
description: |
  [description]
tools: read_file, write_file, create_file, search_files, web_search
color: gold
---
```

**Agents with documentation access:**
- report-generator
- prd-writer (enhances existing PRDs)
- technical-mentor-guide

## With MCP Integrations

When you add the MCPs, update these agents:

### Semgrep MCP
```yaml
---
name: security-threat-analyst
description: |
  [description]
tools: read_file, search_files, list_directory, web_search, semgrep_scan, semgrep_rules
color: purple
---
```

### Exa AI MCP
```yaml
---
name: deep-research-specialist
description: |
  [description]
tools: read_file, search_files, web_search, exa_search, exa_analyze
color: teal
---
```

### Supabase MCP
```yaml
---
name: database-architect
description: |
  [description]
tools: read_file, write_file, search_files, supabase_query, supabase_migrate, supabase_schema
color: navy
---
```

### n8n MCP (if available)
```yaml
---
name: automation-workflow-engineer
description: |
  [description]
tools: read_file, write_file, web_search, n8n_create_workflow, n8n_execute, n8n_schedule
color: amber
---
```

## Quick Reference Table

| Agent | Tool Access | Reason |
|-------|-------------|---------|
| product-manager-orchestrator | Full (omit) | Needs everything for coordination |
| systems-architect | Implementation | Creates ADRs, reads all |
| senior-software-engineer | Full (omit) | Implements everything |
| frontend-ux-specialist | Implementation | UI file creation |
| backend-reliability-engineer | Full (omit) | System management |
| security-threat-analyst | Read-only + Semgrep | Analysis only |
| qa-test-engineer | Implementation | Test creation |
| performance-optimizer | Read-only + | Mostly analysis |
| code-analyzer-debugger | Read-only | Investigation only |
| technical-mentor-guide | Read-only | Documentation |
| deep-research-specialist | Read-only + Exa | Research |
| production-code-validator | Read-only | Validation |
| prd-writer | Implementation | Enhances PRDs |
| database-architect | Implementation + Supabase | Schema management |
| automation-workflow-engineer | Full (omit) | Complex integrations |
| refactoring-expert | Implementation | Code modification |
| smart-form-builder | Implementation | Component creation |
| migration-specialist | Full (omit) | Complex operations |
| pii-guardian | Read-only | Scanning only |
| report-generator | Implementation | Report creation |
| financial-analyst | Read-only | Analysis |
| supabase-specialist | Full (omit) | Supabase ecosystem management |
| orm-specialist | Implementation | Database schema and migrations |
| analytics-engineer | Implementation + Web | Analytics pipeline setup |
| ui-systems | Implementation | Advanced UI components |
| privacy-compliance | Implementation + Web | Compliance implementation |
| event-schema | Implementation | Event architecture design |
| platform-deployment | Full (omit) | Deployment and infrastructure |

## General Rules

1. **When in doubt**: Start with minimal access and expand if needed
2. **Orchestrators**: Always get full access (omit tools)
3. **Analyzers**: Usually read-only + search
4. **Implementers**: Need write access to specific file types
5. **Validators**: Minimal read access only
6. **With MCPs**: Add specific MCP tools to the list

## Future MCP Considerations

As you add more MCPs, update agents that would benefit:
- Logger/monitoring MCPs → performance-optimizer
- Testing MCPs → qa-test-engineer  
- Documentation MCPs → technical-mentor-guide
- Cloud provider MCPs → backend-reliability-engineer
