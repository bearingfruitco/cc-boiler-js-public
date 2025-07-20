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

## PRP Integration: --from-prp

When generating tasks from a PRP instead of PRD:

```bash
/gt auth --from-prp
```

This mode:
1. **Loads PRP Implementation Blueprint**
   - Uses detailed task breakdown from PRP
   - Maintains task dependencies
   - Includes validation gates

2. **Enriches Tasks with Context**
   ```yaml
   Task: Implement JWT utilities
   Context:
     - Pattern: Use existing src/utils/crypto.py
     - Gotcha: Token expiry must be configurable
     - Validation: Must pass test_jwt_security.py
   ```

3. **Adds Validation Checkpoints**
   - After each task group
   - Links to PRP validation levels
   - Auto-triggers `/prp-execute --level N`

4. **Maintains PRP Linkage**
   - Tasks reference PRP sections
   - Progress updates PRP status
   - Validation results tracked

## Example Output with --from-prp:

```markdown
## Tasks for: user-authentication (from PRP)

### Phase 1: Data Models (3 tasks)
- [ ] TASK-001: Create user model with required fields
  - Context: See PRPs/active/auth.md#data-models
  - Pattern: Extend BaseModel from src/models/base.py
  - Validate: /prp-execute auth --level 1

- [ ] TASK-002: Add password hashing utilities  
  - Gotcha: Use bcrypt with min rounds=12
  - Ref: PRPs/ai_docs/security_patterns.md

[Checkpoint: Run Level 1 validation]

### Phase 2: Core Logic (4 tasks)
...
```

## Differences from Standard Mode:

| Aspect | Standard (/gt) | PRP Mode (/gt --from-prp) |
|--------|---------------|---------------------------|
| Source | PRD document | PRP blueprint |
| Detail | High-level tasks | Detailed implementation |
| Context | Basic | Rich with patterns/gotchas |
| Validation | Manual | Automated checkpoints |
| Tracking | Simple | Integrated with PRP status |