#!/bin/bash
# Clean up excessive aliases

echo "🧹 Cleaning up excessive aliases..."

cd /Users/shawnsmith/dev/bfc/boilerplate/.claude

# Backup current aliases
cp aliases.json aliases.backup.json

# Create new clean aliases
cat > aliases-recommended.json << 'EOF'
{
  "sr": "smart-resume",
  "cc": "create-component",
  "vd": "validate-design",
  "prd": "create-prd",
  "fw": "feature-workflow",
  "cp": "checkpoint",
  "gt": "generate-tasks",
  "orch": "orchestrate",
  "grade": "stage-validate-grade",
  "tb": "task-board",
  "ts": "task-status",
  "tc": "task-checkpoint",
  "pt": "process-tasks",
  "at": "analyze-task",
  "mt": "micro-task",
  "gi": "generate-issues",
  "cti": "capture-to-issue",
  "gs": "git-status",
  "sync": "sync-main",
  "wt": "worktree",
  "tr": "test-runner",
  "tdd": "tdd-workflow",
  "lint": "lint-check",
  "specs": "spec-patterns",
  "sc": "security-check",
  "rls": "generate-rls",
  "ctf": "create-tracked-form",
  "sca": "create-secure-api",
  "scf": "create-secure-form",
  "audit": "security-audit",
  "spawn": "spawn-agent",
  "pm": "use product-manager-orchestrator subagent to",
  "fe": "use frontend-ux-specialist subagent to",
  "be": "use backend-reliability-engineer subagent to",
  "sec": "use security-threat-analyst subagent to",
  "db": "use database-architect subagent to",
  "ui": "use ui-systems subagent to",
  "qa": "use qa-test-engineer subagent to",
  "prp": "create-prp",
  "prp-exec": "prp-execute",
  "ut": "ultra-think",
  "vp": "visual-plan",
  "tt": "think-through",
  "compress": "compress-context",
  "h": "help",
  "?": "help",
  "ws": "work-status",
  "td": "todo",
  "ctx": "share-context",
  "deps": "dependency-check",
  "pin": "pin-requirements",
  "metrics": "show-metrics",
  "init": "init-project",
  "bug": "bug-track",
  "research": "research",
  "onboard": "onboard",
  "persona": "persona",
  "er": "error-recovery",
  "vt": "verify-task",
  "dm": "design-mode",
  "bs": "branch-status",
  "fs": "feature-status",
  "bc": "branch-clean",
  "bsw": "branch-switch",
  "ff": "feature-flags",
  "report": "agent-report",
  "health": "agent-health",
  "stats": "agent-stats",
  "doc": "use documentation-writer subagent to",
  "perf": "use performance-optimizer subagent to",
  "arch": "use systems-architect subagent to",
  "sup": "use supabase-specialist subagent to",
  "orm": "use orm-specialist subagent to",
  "tdd-dash": "tdd-dashboard",
  "test": "test-runner-bun",
  "prd-tests": "prd-generate-tests",
  "pin-config": "pin-config",
  "truth": "facts",
  "check": "exists",
  "fg": "field-generate",
  "afs": "audit-form-security",
  "gft": "generate-field-types",
  "ss": "security-status",
  "es": "enhance-security",
  "ds": "dependency-scan",
  "pr-feedback": "pr-feedback",
  "analyze": "analyze-existing",
  "snapshot": "snapshot",
  "share": "share-context",
  "todo": "todo"
}
EOF

echo "✅ Created recommended aliases (reduced from 283 to ~90)"

# Count reduction
original=$(cat aliases.json | jq 'length')
new=$(cat aliases-recommended.json | jq 'length')

echo ""
echo "📊 Alias Reduction:"
echo "  Original: $original aliases"
echo "  Recommended: $new aliases"
echo "  Reduction: $(( original - new )) aliases removed"
echo ""
echo "🎯 Benefits:"
echo "  - Each command has 1-2 aliases max"
echo "  - Easier to remember"
echo "  - Less confusion"
echo "  - Clearer documentation"
echo ""
echo "📝 Next steps:"
echo "1. Review aliases-recommended.json"
echo "2. If happy, replace aliases.json"
echo "3. Remove excess alias command files"
echo "4. Update documentation"
