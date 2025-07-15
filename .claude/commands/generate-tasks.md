Generate a detailed task list from PRD with domain analysis: $ARGUMENTS

Read docs/project/features/$ARGUMENTS-PRD.md and create an enhanced task list with:

## Task List for $ARGUMENTS

### Task Generation Guidelines:
1. Each task should be completable in 5-15 minutes
2. Each task should produce verifiable output  
3. Tasks should be independent when possible
4. Include task dependencies where needed
5. Tag each task with relevant domains
6. Identify parallel work opportunities

### Domain Tagging:
Tag each task with one or more domains:
- `frontend` - UI components, styling, client-side logic
- `backend` - APIs, server logic, authentication
- `data` - Database schema, migrations, queries
- `security` - Auth, encryption, compliance
- `qa` - Testing, validation, quality checks
- `performance` - Optimization, caching, profiling
- `integration` - External APIs, webhooks
- `devops` - Deployment, monitoring, infrastructure

### Task Format:
```markdown
## Task X.Y: [Task Name] [domains: domain1, domain2]
**Complexity**: Low/Medium/High
**Estimated time**: 5-30 minutes
**Dependencies**: Task A.B, Task C.D (if any)
**Enables**: Task M.N (if any)

Description of what needs to be done.

**Acceptance Criteria**:
- [ ] Specific measurable outcome
- [ ] Another verifiable result
```

### Generate Task Structure:

#### Phase 1: Foundation (Backend/Data)
Analyze PRD for database needs, data models, core infrastructure.

Example tasks:
```markdown
## Task 1.1: Design user database schema [domains: data, backend]
**Complexity**: Medium
**Estimated time**: 15 minutes
**Dependencies**: None
**Enables**: Tasks 1.2, 2.1

Design the user table with all required fields from PRD.

**Acceptance Criteria**:
- [ ] Schema includes all PRD-specified fields
- [ ] Proper indexes defined
- [ ] Migration file created
```

#### Phase 2: Core Backend Logic
API endpoints, business logic, server-side validation.

#### Phase 3: Frontend Components  
UI components, forms, client-side logic.

#### Phase 4: Integration & Testing
Connect systems, end-to-end flows, comprehensive testing.

#### Phase 5: Performance & Polish
Optimization, accessibility, final touches.

### Orchestration Analysis Section:

After generating all tasks, add:

```markdown
## 🤖 Orchestration Analysis

### Domain Distribution:
- Frontend: X tasks
- Backend: Y tasks  
- Data: Z tasks
- [etc...]

### Parallel Work Opportunities:
1. **Phase 1**: Tasks 1.1, 1.2, 1.3 can run in parallel (different domains)
2. **Phase 3**: Frontend work can start once APIs are defined
3. **Phase 4**: Testing can begin per component as completed

### Complexity Assessment:
- Total tasks: [count]
- High complexity: [count]
- Dependencies: [critical path length]
- Estimated total time: [sum of estimates]

### Orchestration Recommendation:
[One of the following]

✅ **Multi-agent orchestration recommended**
- 4+ domains with significant work
- Multiple parallel opportunities identified
- Estimated 50-70% time savings

**Suggested command**:
```bash
/orch $ARGUMENTS --agents=[count] --strategy=[type]
```

OR

⚡ **Single agent sufficient**
- Limited domain overlap
- Mostly sequential work
- Low complexity

**Suggested command**:
```bash
/pt $ARGUMENTS
```
```

### Additional Enhancements:

1. **Dependency Graph**: Show which tasks block others
2. **Critical Path**: Identify the longest dependency chain
3. **Resource Allocation**: Suggest which persona for each task
4. **Risk Assessment**: Flag high-complexity or high-risk tasks

Save the enhanced task list as: docs/project/features/$ARGUMENTS-tasks.md

The auto-orchestration hook will analyze this file and provide intelligent suggestions!