#!/bin/bash
# Auto-generated hook fix script
# Generated: 2025-08-05 12:01:28

# Create backup
cp -r .claude/hooks .claude/hooks.backup.$(date +%Y%m%d_%H%M%S)

# Fix missing hooks
cp .claude/hooks/pre-tool-use/07-pii-protection.py.original .claude/hooks/pre-tool-use/07-pii-protection.py
cp .claude/hooks/pre-tool-use/16-tcpa-compliance.py.original .claude/hooks/pre-tool-use/16-tcpa-compliance.py
cp .claude/hooks/pre-tool-use/22-security-validator.py.original .claude/hooks/pre-tool-use/22-security-validator.py
# Archive: .claude/hooks/pre-tool-use/08-evidence-language.py.original
# Archive: .claude/hooks/pre-tool-use/16a-prp-validator.py.original
# Archive: .claude/hooks/pre-tool-use/06a-biome-lint.py.original
# Archive: .claude/hooks/pre-tool-use/00a-snapshot-manager.py.original
# Archive: .claude/hooks/pre-tool-use/13-import-validator.py.old
# Archive: .claude/hooks/pre-tool-use/13-import-validator.py.original
# Archive: .claude/hooks/pre-tool-use/14a-creation-guard.py.original
# Archive: .claude/hooks/pre-tool-use/11-truth-enforcer.py.old
# Archive: .claude/hooks/pre-tool-use/11-truth-enforcer.py.original
# Archive: .claude/hooks/pre-tool-use/20-feature-state-guardian.py.original
# Archive: .claude/hooks/pre-tool-use/15a-dependency-tracker.py.original
# Archive: .claude/hooks/pre-tool-use/15a-dependency-tracker.py.old
# Archive: .claude/hooks/pre-tool-use/20-feature-awareness.py.original
# Archive: .claude/hooks/pre-tool-use/19-tdd-enforcer.py.backup
# Archive: .claude/hooks/pre-tool-use/19-tdd-enforcer.py.original
# Archive: .claude/hooks/pre-tool-use/05-code-quality.py.original
# Archive: .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py.original
# Archive: .claude/hooks/pre-tool-use/17-ai-docs-check.py.original
# Archive: .claude/hooks/pre-tool-use/10-hydration-guard.py.original
# Archive: .claude/hooks/pre-tool-use/18-auto-parallel-agents.py.original
# Archive: .claude/hooks/pre-tool-use/21-branch-controller.py.original
# Archive: .claude/hooks/pre-tool-use/17-test-generation-enforcer.py.original
# Archive: .claude/hooks/pre-tool-use/02-design-check.py.original
# Archive: .claude/hooks/pre-tool-use/01-collab-sync.py.original
# Archive: .claude/hooks/pre-tool-use/08a-async-patterns.py.original
# Archive: .claude/hooks/pre-tool-use/04-actually-works.py.original
# Archive: .claude/hooks/pre-tool-use/14-prd-clarity.py.original
# Archive: .claude/hooks/pre-tool-use/00a-dangerous-commands.py.original
# Archive: .claude/hooks/pre-tool-use/09-auto-persona.py.original
# Archive: .claude/hooks/pre-tool-use/12-deletion-guard.py.original
# Archive: .claude/hooks/pre-tool-use/05a-auto-context-inclusion.py.original
# Archive: .claude/hooks/pre-tool-use/03-conflict-check.py.original
# Archive: .claude/hooks/pre-tool-use/06-requirement-drift-detector.py.original
# Archive: .claude/hooks/pre-tool-use/05b-prp-context-loader.py.original
# Archive: .claude/hooks/pre-tool-use/21-security-command-enhancer.py.original
# Archive: .claude/hooks/post-tool-use/05-test-runner.py.original
# Archive: .claude/hooks/post-tool-use/04-next-command-suggester.py.original
# Archive: .claude/hooks/post-tool-use/05-multi-review-suggester.py.original
# Archive: .claude/hooks/post-tool-use/06-test-auto-runner.py.original
# Archive: .claude/hooks/post-tool-use/03c-response-capture.py.original
# Archive: .claude/hooks/post-tool-use/02-metrics.py.original
# Archive: .claude/hooks/post-tool-use/10-prp-progress-tracker.py.original
# Archive: .claude/hooks/post-tool-use/03-pattern-learning.py.original
# Archive: .claude/hooks/post-tool-use/03a-auto-orchestrate.py.original
# Archive: .claude/hooks/post-tool-use/14-completion-verifier.py.original
# Archive: .claude/hooks/post-tool-use/03b-command-logger.py.original
# Archive: .claude/hooks/post-tool-use/04-research-capture.py.original
# Archive: .claude/hooks/post-tool-use/15b-task-ledger-updater.py.original
# Archive: .claude/hooks/post-tool-use/04a-prp-metrics.py.original
# Archive: .claude/hooks/post-tool-use/01-state-save.py.original
# Archive: .claude/hooks/post-tool-use/01a-action-logger.py.original
# Archive: .claude/hooks/post-tool-use/16-security-analyzer.py.original
# Archive: .claude/hooks/pre-compact/security-context-preserver.py.original
# Archive: .claude/hooks/pre-compact/security-context-preserver.py.prefixbatch
# Archive: .claude/hooks/pre-compact/requirement-context-preserver.py
# Archive: .claude/hooks/pre-compact/requirement-context-preserver.py.original
# Archive: .claude/hooks/user-prompt-submit/01-tdd-suggester.py.original
# Archive: .claude/hooks/user-prompt-submit/02-security-suggester.py.original
# Archive: .claude/hooks/user-prompt-submit/02-security-suggester.py
# Archive: .claude/hooks/stop/01-save-transcript.py.original
# Archive: .claude/hooks/stop/01-save-transcript.py.prefixbatch
# Archive: .claude/hooks/stop/security-summary.py.prefixbatch
# Archive: .claude/hooks/stop/security-summary.py.original
# Archive: .claude/hooks/stop/handoff-prep.py.original
# Archive: .claude/hooks/stop/handoff-prep.py.prefixbatch
# Archive: .claude/hooks/stop/knowledge-share.py.original
# Archive: .claude/hooks/stop/knowledge-share.py.prefixbatch
# Archive: .claude/hooks/stop/save-state.py
# Archive: .claude/hooks/stop/save-state.py.original
# Archive: .claude/hooks/sub-agent-stop/security-report.py.original
# Archive: .claude/hooks/sub-agent-stop/security-report.py.prefixbatch
# Archive: .claude/hooks/sub-agent-stop/01-track-completion.py.original
# Archive: .claude/hooks/sub-agent-stop/01-track-completion.py.prefixbatch
# Archive: .claude/hooks/sub-agent-stop/coordinate.py.prefixbatch
# Archive: .claude/hooks/sub-agent-stop/coordinate.py.original
# Archive: .claude/hooks/notification/context-db-awareness.py.original
# Archive: .claude/hooks/notification/context-db-awareness.py
# Archive: .claude/hooks/notification/continuous-requirement-validator.py.original
# Archive: .claude/hooks/notification/continuous-requirement-validator.py
# Archive: .claude/hooks/notification/02-pr-feedback-monitor.py.prefixbatch
# Archive: .claude/hooks/notification/02-pr-feedback-monitor.py.original
# Archive: .claude/hooks/notification/security-alerts.py.original
# Archive: .claude/hooks/notification/security-alerts.py
# Archive: .claude/hooks/notification/01-precompact-handler.py.original
# Archive: .claude/hooks/notification/01-precompact-handler.py.prefixbatch
# Archive: .claude/hooks/notification/smart-suggest.py.prefixbatch
# Archive: .claude/hooks/notification/smart-suggest.py.original
# Archive: .claude/hooks/notification/branch-health.py
# Archive: .claude/hooks/notification/branch-health.py.original
# Archive: .claude/hooks/notification/team-aware.py.original
# Archive: .claude/hooks/notification/team-aware.py
# Archive: .claude/hooks/notification/worktree-awareness.py.original

# Archive old versions
mkdir -p .claude/hooks/_archive/$(date +%Y%m%d)
find .claude/hooks -name '*.original' -o -name '*.broken' -o -name '*.backup' -o -name '*.old' | while read f; do
  mv "$f" .claude/hooks/_archive/$(date +%Y%m%d)/
done

echo 'Hook fixes applied!'
