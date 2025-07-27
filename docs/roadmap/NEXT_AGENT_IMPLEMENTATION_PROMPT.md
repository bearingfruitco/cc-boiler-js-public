# Prompt for Next LLM Agent: Claude Code Boilerplate Enhancement Implementation

## Context & Background

You are reviewing an enhancement plan for an advanced Claude Code boilerplate system that already includes:
- 116+ custom commands with PRD-driven development
- 70+ hooks for automated enforcement (design system, security, collaboration)
- Agent OS integration with centralized standards
- Zero context loss between sessions
- Event-driven architecture with async patterns
- Multi-level validation (MCP hooks, Git pre-commit, PRP loops)

## Your Task

Review and implement the enhancement plan located at:
- Main Plan: `/docs/roadmap/SYSTEM_ENHANCEMENT_PLAN_2025.md`
- Technical Guide: `/docs/roadmap/TECHNICAL_IMPLEMENTATION_GUIDE.md`

## Critical Review Points

### 1. Architecture Compatibility
- Verify all proposed features integrate with existing hook system (review `.claude/hooks/`)
- Ensure new commands follow existing patterns (review `.claude/commands/`)
- Check that storage locations don't conflict with current structure
- Validate that new hooks follow official Claude Code format (snake_case, proper returns)

### 2. Priority Assessment
Question whether the priorities are correct:
- Is snapshot/rollback truly the #1 need? 
- Should TypeScript feedback be integrated differently?
- Are there hidden dependencies between features?

### 3. Implementation Risks
- Will snapshots bloat the project? (Consider `.gitignore` patterns)
- Will TypeScript checking slow down the development flow?
- Could parallel orchestration cause race conditions with existing hooks?

### 4. Missing Considerations
Look for gaps:
- How do snapshots interact with Git branches?
- What happens to snapshots during `/sync-main`?
- How does TypeScript validator handle monorepos?
- Should snapshots be encrypted for sensitive projects?

## Implementation Approach

### Phase 1: Prototype Core Features

1. **Start with Snapshot System**
   ```bash
   # Create command stub
   Create: .claude/commands/snapshot.md
   
   # Create hook
   Create: .claude/hooks/pre-tool-use/00a-snapshot-manager.py
   
   # Test with existing hooks
   Verify: Doesn't break 00-auto-approve-safe-ops.py flow
   ```

2. **Add TypeScript Validator**
   ```bash
   # Create as post-tool-use hook
   Create: .claude/hooks/post-tool-use/07-typescript-validator.py
   
   # Integrate with existing metrics
   Update: .claude/hooks/post-tool-use/02-metrics.py
   ```

### Phase 2: Integration Testing

Test with real scenarios:
1. Create a component with type errors → Should get immediate feedback
2. Make 10+ file changes → Should auto-snapshot
3. Rollback after error → Should restore perfectly
4. Run parallel tasks → Should see speed improvement

### Phase 3: Edge Cases

Consider:
- What if snapshot fails mid-creation?
- What if TypeScript is not installed?
- What if parallel agents modify same file?
- How to handle binary files in snapshots?

## Specific Questions to Answer

1. **Snapshot Storage**: Should we use Git's object database instead of file copies?
2. **TypeScript Integration**: Should we use TSC API instead of CLI for speed?
3. **Parallel Limits**: What's the optimal number of concurrent agents?
4. **Export Format**: Should we support Windsurf and other new tools?

## Code Quality Requirements

- All Python hooks must handle errors gracefully (see existing patterns)
- All commands must have comprehensive help text
- New features must update:
  - `NEW_CHAT_CONTEXT.md` 
  - `QUICK_REFERENCE.md`
  - `SYSTEM_OVERVIEW.md`

## Testing Checklist

- [ ] Snapshot creation < 100ms for typical changes
- [ ] TypeScript feedback appears within 2 seconds
- [ ] Parallel orchestration shows measurable speedup
- [ ] All existing hooks continue to function
- [ ] No performance degradation for existing workflows
- [ ] Export format works in Cursor and Windsurf

## Alternative Approaches to Consider

1. **Instead of file-based snapshots**: Use Git worktrees for isolation?
2. **Instead of TypeScript hook**: Integrate with Biome for unified checking?
3. **Instead of new orchestration**: Enhance existing `/orchestrate-agents`?

## Success Criteria

The implementation is successful when:
1. Developers can fearlessly experiment (rollback in <5 seconds)
2. Type errors never reach runtime
3. Multi-component refactors are 3x faster
4. Zero breaking changes to existing system
5. Documentation is complete and examples are clear

## Final Integration Steps

1. Update `settings.json` with new hooks (maintaining snake_case format)
2. Add new commands to chains where appropriate
3. Create migration guide for existing users
4. Set up feature flags for gradual rollout
5. Update all system documentation

## Start Here

Begin by reading:
1. The enhancement plan documents
2. Current hook implementations for patterns
3. `CLAUDE.md` for system philosophy

Then create a proof-of-concept for the snapshot system as it's the highest priority and will validate the storage approach for other features.

Remember: The goal is to enhance without adding complexity. Every new feature should feel like a natural extension of the existing system.