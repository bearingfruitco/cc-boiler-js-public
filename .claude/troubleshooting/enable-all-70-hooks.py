#!/usr/bin/env python3
"""Create complete configuration with ALL 70+ hooks"""

import json
from pathlib import Path

CLAUDE_DIR = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude")

# Complete list of ALL hooks based on directory listings
ALL_HOOKS = {
    "PreToolUse": [
        "00-auto-approve-safe-ops.py",
        "00a-dangerous-commands.py",
        "00a-snapshot-manager.py",
        "01-collab-sync.py",
        "02-design-check.py",
        "03-conflict-check.py",
        "04-actually-works.py",
        "05-code-quality.py",
        "05a-auto-context-inclusion.py",
        "05b-prp-context-loader.py",
        "06-requirement-drift-detector.py",
        "06a-biome-lint.py",
        "07-pii-protection.py",
        "08-evidence-language.py",
        "08a-async-patterns.py",
        "09-auto-persona.py",
        "10-hydration-guard.py",
        "11-truth-enforcer.py",
        "12-deletion-guard.py",
        "13-import-validator.py",
        "14-prd-clarity.py",
        "14a-creation-guard.py",
        "15-implementation-guide.py",
        "15a-dependency-tracker.py",
        "16-tcpa-compliance.py",
        "16a-prp-validator.py",
        "17-ai-docs-check.py",
        "17-test-generation-enforcer.py",
        "18-auto-parallel-agents.py",
        "19-tdd-enforcer.py",
        "20-feature-awareness.py",
        "20-feature-state-guardian.py",
        "21-branch-controller.py",
        "21-security-command-enhancer.py",
        "22-security-validator.py"
    ],
    "PostToolUse": [
        "01-state-save.py",
        "01a-action-logger.py",
        "02-metrics.py",
        "03-pattern-learning.py",
        "03a-auto-orchestrate.py",
        "03b-command-logger.py",
        "03c-response-capture.py",
        "04-next-command-suggester.py",
        "04-research-capture.py",
        "04a-prp-metrics.py",
        "05-multi-review-suggester.py",
        "05-test-runner.py",
        "06-test-auto-runner.py",
        "10-prp-progress-tracker.py",
        "14-completion-verifier.py",
        "15b-task-ledger-updater.py",
        "16-security-analyzer.py"
    ],
    "Notification": [
        "01-precompact-handler.py",
        "02-pr-feedback-monitor.py",
        "branch-health.py",
        "context-db-awareness.py",
        "continuous-requirement-validator.py",
        "security-alerts.py",
        "smart-suggest.py",
        "team-aware.py",
        "worktree-awareness.py"
    ],
    "Stop": [
        "01-save-transcript.py",
        "02-state-save.py",
        "03-handoff-prep.py",
        "04-task-summary.py",
        "05-security-summary.py"
    ],
    "SubagentStop": [
        "01-track-completion.py"
    ]
}

def create_complete_config():
    """Create configuration with all hooks"""
    # Load current permissions
    with open(CLAUDE_DIR / "settings.json") as f:
        current = json.load(f)
    
    config = {
        "permissions": current.get("permissions", {
            "file_system": {"read": True, "write": True},
            "shell": {"execute": True}
        }),
        "hooks": {}
    }
    
    # Add all hooks
    total = 0
    for event_type, hook_files in ALL_HOOKS.items():
        if hook_files:
            # Map directory names
            dir_map = {
                "PreToolUse": "pre-tool-use",
                "PostToolUse": "post-tool-use", 
                "Notification": "notification",
                "Stop": "stop",
                "SubagentStop": "sub-agent-stop"
            }
            
            dir_name = dir_map.get(event_type, event_type.lower())
            
            config["hooks"][event_type] = [{
                "matcher": "",
                "hooks": [
                    {
                        "type": "command",
                        "command": f"python3 .claude/hooks/{dir_name}/{hook_file}"
                    }
                    for hook_file in hook_files
                ]
            }]
            total += len(hook_files)
    
    return config, total

def main():
    config, total = create_complete_config()
    
    print("✅ Creating configuration with ALL hooks...")
    print(f"📊 Total hooks to enable: {total}")
    
    # Save it
    output_path = CLAUDE_DIR / "settings-all-70-hooks.json"
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Saved to: {output_path}")
    print("\n📈 Hook counts:")
    for event_type, hooks in ALL_HOOKS.items():
        print(f"  • {event_type}: {len(hooks)} hooks")
    
    print(f"\n🚀 To enable ALL {total} hooks:")
    print(f"   cp {output_path} .claude/settings.json")
    print("   claude doctor")

if __name__ == "__main__":
    main()
