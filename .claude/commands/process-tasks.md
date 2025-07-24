Process tasks for feature: $ARGUMENTS

Instructions for systematic task completion with TDD verification:

1. Load the task list from docs/project/features/$ARGUMENTS-tasks.md
2. Find the next uncompleted task
3. Show me the task details
4. Check if tests exist (TDD workflow)
5. Implement ONLY that specific task
6. Run quick verification: tests pass, TypeScript compiles
7. Show the changes made with verification results
8. Wait for my approval before marking complete
9. Update the task with [✓] when approved AND verified
10. Move to the next task

Enhanced TDD Integration:
- Before implementing: Check for existing tests
- If no tests: Suggest creating tests first (/test [component])
- After implementing: Auto-verify tests still pass
- Show verification status with each task

Important:
- Focus on ONE task at a time
- Follow TDD: Red → Green → Refactor
- Ensure tests pass before marking complete
- If verification fails, fix before proceeding
- Save progress after every 3 verified tasks

Task Status Indicators:
[ ] Not started
[~] In progress
[✓] Complete & verified
[✗] Implementation failed verification
[🧪] Tests written, awaiting implementation

Current task format:
"Working on task X.Y: [description]
 TDD Status: [Tests exist/Need tests]
 Verification: [Pending/Passed/Failed]"
