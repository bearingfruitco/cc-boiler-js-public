# Issue #15: Populate All Empty Agent Files

## Overview
Critical issue discovered - most agent files in `.claude/agents/` are empty (0 bytes). These need to be populated with proper Claude Code sub-agent format following official documentation.

## Problem Statement
We have 31 agents referenced in the system, but most are empty files. This means:
- Agents cannot be invoked properly
- System functionality is severely limited
- Orchestration features won't work
- Team collaboration is broken

## Empty Agent Files Found
1. analytics-engineer.md
2. analyzer.md
3. automation-workflow-engineer.md
4. backend.md
5. code-reviewer.md
6. database-architect.md (partially created)
7. documentation-writer.md
8. event-schema.md
9. financial-analyst.md
10. form-builder-specialist.md
11. frontend.md
12. integration-specialist.md
13. mentor.md
14. migration-specialist.md
15. orm-specialist.md
16. performance.md
17. pii-guardian.md
18. platform-deployment.md
19. pm-orchestrator.md
20. prd-writer.md
21. privacy-compliance.md
22. production-code-validator.md
23. progress-logger.md
24. prp-writer.md
25. qa.md
26. refactoring-expert.md
27. report-generator.md
28. researcher.md
29. senior-engineer.md
30. supabase-specialist.md
31. tdd-engineer.md
32. ui-systems.md

## Requirements

### Agent File Format
Each agent must follow the Claude Code sub-agent format:
```markdown
---
name: agent-name
description: Clear description of when this agent should be used. Include "Use PROACTIVELY" for automatic invocation.
tools: Read, Write, Edit, Bash, [other specific tools]
---

[System prompt with detailed instructions]
```

### Content Requirements
1. **Clear Purpose**: Single responsibility principle
2. **Detailed Instructions**: Step-by-step processes
3. **Tool Access**: Only necessary tools
4. **Output Formats**: Structured templates
5. **Best Practices**: Domain-specific guidance
6. **Examples**: Concrete code/output examples

## Priority Order

### Critical Agents (Do First)
1. **frontend** - UI/React development
2. **backend** - API development
3. **qa** - Testing and quality
4. **database-architect** - Database design
5. **supabase-specialist** - Supabase integration
6. **tdd-engineer** - Test-driven development
7. **security** - Security implementation
8. **pm-orchestrator** - Project coordination

### Important Agents (Do Second)
9. **analyzer** - Code analysis
10. **code-reviewer** - Code review
11. **performance** - Performance optimization
12. **orm-specialist** - ORM optimization
13. **ui-systems** - UI/UX systems
14. **documentation-writer** - Documentation
15. **refactoring-expert** - Code refactoring
16. **senior-engineer** - Complex problems

### Specialized Agents (Do Third)
17. **analytics-engineer** - Analytics implementation
18. **event-schema** - Event design
19. **form-builder-specialist** - Form creation
20. **integration-specialist** - Third-party integration
21. **migration-specialist** - Data migration
22. **pii-guardian** - PII protection
23. **privacy-compliance** - Privacy laws
24. **automation-workflow-engineer** - Automation

### Utility Agents (Do Last)
25. **mentor** - Teaching/guidance
26. **prd-writer** - PRD creation
27. **prp-writer** - PRP creation
28. **progress-logger** - Progress tracking
29. **report-generator** - Report creation
30. **researcher** - Research tasks
31. **production-code-validator** - Code validation
32. **financial-analyst** - Cost analysis

## Implementation Plan

### Phase 1: Critical Agents (Today)
- Create 8 critical agents with full content
- Test basic invocation
- Verify tool access

### Phase 2: Important Agents (Tomorrow)
- Create 8 important agents
- Test orchestration between agents
- Verify workflows

### Phase 3: Specialized Agents (Day 3)
- Create 8 specialized agents
- Test domain-specific functionality
- Integrate with commands

### Phase 4: Utility Agents (Day 4)
- Create remaining utility agents
- Complete testing
- Update documentation

## Success Criteria
- [ ] All 31 agents have complete content
- [ ] Each agent follows official format
- [ ] Agents can be invoked with `/agents`
- [ ] Tool access is properly configured
- [ ] Orchestration works between agents
- [ ] Documentation is updated

## Resources
- Official docs: https://docs.anthropic.com/en/docs/claude-code/sub-agents
- Existing examples: playwright-specialist.md, security-auditor.md
- System chains that use agents: chains.json

## Priority: CRITICAL 🔴
This blocks core system functionality. Without agents, the orchestration and multi-agent features cannot work.
