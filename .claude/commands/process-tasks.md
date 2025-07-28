Process tasks for feature: $ARGUMENTS

🔴 **TDD MANDATORY**: Every task must have tests BEFORE implementation!

Instructions for systematic task completion with ENFORCED TDD:

1. Load the task list from docs/project/features/$ARGUMENTS-tasks.md
2. Find the next uncompleted task
3. Show me the task details
4. **MANDATORY TDD CHECK**:
   ```bash
   # Check if tests exist for this task
   if [ ! -f "*test*" ]; then
     echo "🧪 No tests found! Generating tests..."
     # Auto-spawn TDD engineer
     /spawn tdd-engineer "Generate tests for: $TASK_DESCRIPTION"
     # WAIT for test generation to complete
     echo "⏳ Waiting for tests... (2-3 minutes)"
   fi
   ```
5. **Run tests first (RED phase)**:
   ```bash
   /test
   # EXPECT FAILURE - this is good!
   # Shows what needs to be implemented
   ```
6. Implement ONLY that specific task (GREEN phase)
7. Run verification until tests pass:
   ```bash
   /test  # Must pass!
   /tc    # TypeScript check
   ```
8. Show the changes with test results
9. Wait for approval (tests must be GREEN)
10. Update task with [✓] when tests pass
11. Move to next task

**ENFORCED TDD Workflow**:
- 🚫 **NO IMPLEMENTATION WITHOUT TESTS**
- Tests are generated automatically if missing
- Implementation blocked until tests exist
- Must see RED before writing code
- Must see GREEN before marking complete
- Coverage must stay above 80%

**Critical Rules**:
- 🔴 ONE task at a time
- 🔴 Tests MUST exist before coding
- 🔴 See failing tests first (RED)
- 🟢 Make tests pass (GREEN)
- 🔵 Refactor if needed (tests stay GREEN)
- 📊 Coverage must not drop below 80%
- 💾 Save after each completed task

**Task Status Indicators**:
[ ] Not started
[🧪] Tests being generated
[🔴] Tests written, failing (RED)
[~] Implementation in progress
[🟡] Tests passing, needs refactor
[🟢] Complete & all tests passing (GREEN)
[✗] Failed - fix required
[📊] Coverage check failed

**Current Task Display**:
```
Task X.Y: [description]
🧪 TDD Status: [Auto-generating|Ready|Failed]
🔴 Test Status: [8/10 failing]
🟢 Coverage: [87.5%]
⏱️ Time: [2m 34s]
```

**Example Workflow**:
```bash
/pt user-auth

# Output:
Task 2.1: Create login form component
🧪 TDD Status: No tests found!
→ Auto-spawning TDD engineer...
→ Generating LoginForm.test.tsx...
✅ Tests created!

🔴 Running tests... 0/12 passing (RED - this is expected!)

Now implement LoginForm.tsx to make tests pass...
```
