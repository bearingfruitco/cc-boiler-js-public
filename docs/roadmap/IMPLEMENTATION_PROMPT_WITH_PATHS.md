# Prompt for Next LLM Agent: Claude Code Boilerplate Enhancement Implementation

## Context & Background

You are reviewing an enhancement plan for an advanced Claude Code boilerplate system that already includes:
- 116+ custom commands with PRD-driven development
- 70+ hooks for automated enforcement (design system, security, collaboration)
- Agent OS integration with centralized standards
- Zero context loss between sessions
- Event-driven architecture with async patterns
- Multi-level validation (MCP hooks, Git pre-commit, PRP loops)

## Required Reading - Read These Files First

Please read these documents in order to understand the system and proposed enhancements:

### 1. Enhancement Plans (Read First)
- `/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/docs/roadmap/SYSTEM_ENHANCEMENT_PLAN_2025.md`
- `/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/docs/roadmap/TECHNICAL_IMPLEMENTATION_GUIDE.md`

### 2. Current System Documentation (Read Second)
- `/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/docs/SYSTEM_OVERVIEW.md` - Full system architecture
- `/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/.claude/NEW_CHAT_CONTEXT.md` - Latest features and updates
- `/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/CLAUDE.md` - Core AI agent instructions

### 3. Implementation Examples (Read Third)
Review these files to understand implementation patterns:

**Hook Configuration:**
- `/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/.claude/settings.json` - Current hook setup

**Example Hooks (to understand patterns):**
- `/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/.claude/hooks/pre-tool-use/02-design-check.py` - Pre-tool-use hook example
- `/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/.claude/hooks/post-tool-use/01-state-save.py` - Post-tool-use hook example
- `/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/.claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py` - Auto-approval pattern

**Example Commands (to understand structure):**
- `/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/.claude/commands/smart-resume.md` - Complex command example
- `/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/.claude/commands/create-component.md` - Component creation command
- `/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/.claude/commands/snapshot.md` - (This doesn't exist yet - you'll create it)

### 4. Quick Reference (Optional but Helpful)
- `/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/.claude/QUICK_REFERENCE.md` - All current commands

## Your Task

After reading all the above files:

### 1. Critical Review
- What concerns do you have about the enhancement plan?
- Are the priorities correct? (Snapshot → TypeScript → Parallel Orchestration)
- What implementation risks do you foresee?
- Are there better alternatives to the proposed approaches?

### 2. Architecture Compatibility Check
- Verify all proposed features integrate with existing hook system
- Ensure new commands follow existing patterns
- Check that storage locations don't conflict
- Validate hook format compliance (snake_case, proper returns)

### 3. Implementation Questions to Answer
- Should snapshots use Git's object database instead of file copies?
- Should TypeScript validator use TSC API instead of CLI?
- What's the optimal number of concurrent agents for parallel orchestration?
- How should snapshots handle binary files?
- What happens to snapshots during branch operations?

### 4. Create Proof of Concept

Start with the Snapshot System:

1. **Create the command file:**
   - Path: `/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/.claude/commands/snapshot.md`
   - Follow pattern from `smart-resume.md`

2. **Create the snapshot manager hook:**
   - Path: `/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/.claude/hooks/pre-tool-use/00a-snapshot-manager.py`
   - Follow pattern from `00-auto-approve-safe-ops.py`

3. **Update settings.json:**
   - Add new hook to pre_tool_use section
   - Maintain proper format (snake_case, commands array)

4. **Create storage structure:**
   ```
   /Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/.claude/snapshots/
   ├── manifest.json
   └── .gitignore
   ```

## Testing Requirements

Your implementation should:
- [ ] Create snapshots in < 100ms for typical changes
- [ ] Support rollback in < 5 seconds
- [ ] Not break any existing hooks
- [ ] Follow all existing code patterns
- [ ] Include comprehensive error handling

## Edge Cases to Handle

- What if snapshot creation fails mid-process?
- What if user tries to rollback with uncommitted changes?
- How to handle conflicts between snapshots and git state?
- What's the cleanup strategy for old snapshots?

## Success Criteria

The implementation is successful when:
1. Developers can experiment fearlessly with instant rollback
2. The feature integrates seamlessly with existing workflows
3. No performance degradation for existing features
4. Documentation is complete with examples

## Start Here

1. Read all the files listed above
2. Share your critical review and concerns
3. Propose any alternative approaches
4. Create the snapshot system proof of concept
5. Test with the existing hook system

Remember: The goal is enhancement without complexity. Every new feature should feel like a natural extension of the existing system.

## Note on File Paths

All paths are absolute from: `/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/`

This is the working directory you should use for all file operations.