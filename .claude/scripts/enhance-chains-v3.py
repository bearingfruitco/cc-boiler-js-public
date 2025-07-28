#!/usr/bin/env python3
"""
Update existing chains to leverage v3.0 technology agents
"""

import json
from pathlib import Path

# Load current chains
chains_file = Path(".claude/chains.json")
with open(chains_file) as f:
    data = json.load(f)

chains = data["chains"]

# Define enhancements for existing chains
enhancements = {
    "feature-complete": {
        "commands": [
            "checkpoint create pre-complete",
            "analyze-task",  # New v3.0 command
            "orchestrate if complex",  # New v3.0 command
            "validate-design",
            "test-runner all",
            "agent-health technology",  # New v3.0 command
            "show-metrics",  # New v3.0 command
            "performance-monitor compare",
            "security-check all",
            "feature-workflow complete"
        ]
    },
    "daily-startup": {
        "commands": [
            "smart-resume",
            "agent-health all",  # New v3.0 command
            "show-metrics dashboard",  # New v3.0 command
            "task-ledger summary",
            "task-status",
            "work-status",
            "todo list"
        ]
    },
    "morning-setup": {
        "commands": [
            "smart-resume",
            "agent-health technology",  # New v3.0 command
            "security-check deps",
            "test-runner changed"
        ]
    },
    "pre-pr": {
        "commands": [
            "analyze-task",  # New v3.0 command
            "validate-design",
            "test-runner changed",
            "verify --full",
            "performance-monitor check",
            "security-check all",
            "show-metrics alerts"  # New v3.0 command
        ]
    }
}

# Apply enhancements to existing chains
for chain_name, enhancement in enhancements.items():
    if chain_name in chains:
        if "commands" in enhancement:
            chains[chain_name]["commands"] = enhancement["commands"]
            chains[chain_name]["description"] += " (enhanced with v3.0)"

# Add new v3.0 specialized chains
new_chains = {
    "database-optimization": {
        "description": "Optimize database performance with v3.0 specialists",
        "steps": [
            {"agent": "performance-optimizer", "task": "Analyze database performance metrics"},
            {"agent": "supabase-specialist", "task": "Optimize Supabase queries, indexes, and RLS policies"},
            {"agent": "orm-specialist", "task": "Optimize ORM queries and implement efficient patterns"},
            {"agent": "database-architect", "task": "Review and optimize overall database design"},
            {"agent": "qa-test-engineer", "task": "Create performance benchmarks"}
        ]
    },
    "full-stack-feature": {
        "description": "Build complete full-stack feature with all v3.0 agents",
        "steps": [
            {"agent": "pm-orchestrator", "task": "Break down feature requirements"},
            {"agent": "event-schema", "task": "Design event tracking and data model"},
            {"agent": "orm-specialist", "task": "Create Drizzle/Prisma schema"},
            {"agent": "supabase-specialist", "task": "Implement Supabase backend with RLS"},
            {"agent": "ui-systems", "task": "Build Shadcn UI components with animations"},
            {"agent": "analytics-engineer", "task": "Set up RudderStack tracking"},
            {"agent": "privacy-compliance", "task": "Implement GDPR/CCPA compliance"},
            {"agent": "platform-deployment", "task": "Configure Vercel deployment"},
            {"agent": "qa-test-engineer", "task": "Complete end-to-end testing"}
        ]
    },
    "privacy-implementation": {
        "description": "Implement complete privacy compliance with v3.0 agents",
        "steps": [
            {"agent": "privacy-compliance", "task": "Design consent flows and cookie management"},
            {"agent": "event-schema", "task": "Classify PII in event schemas"},
            {"agent": "analytics-engineer", "task": "Implement privacy-safe tracking"},
            {"agent": "ui-systems", "task": "Build consent UI components"},
            {"agent": "qa-test-engineer", "task": "Test compliance requirements"}
        ]
    },
    "tech-stack-audit": {
        "description": "Comprehensive audit of technology stack",
        "commands": [
            "test-v3 all",
            "agent-health all",
            "show-metrics report 168",
            "dependency-scan",
            "security-audit --comprehensive"
        ]
    }
}

# Add new chains
chains.update(new_chains)

# Update shortcuts
shortcuts = data.get("shortcuts", {})
new_shortcuts = {
    "dbo": "database-optimization",
    "fsf": "full-stack-feature", 
    "pi": "privacy-implementation",
    "tsa": "tech-stack-audit"
}
shortcuts.update(new_shortcuts)

# Enhance specific step-based chains
step_chains_to_enhance = {
    "feature-development-chain": {
        "phase": "planning",
        "insert_agents": [
            {"agent": "event-schema", "task": "Design data model and event taxonomy"},
            {"agent": "orm-specialist", "task": "Design database schema with optimal relations and migrations"}
        ]
    },
    "performance-optimization-chain": {
        "insert_after": "performance-optimizer",
        "new_steps": [
            {"agent": "supabase-specialist", "task": "Optimize Supabase queries, indexes, and connection pooling"},
            {"agent": "orm-specialist", "task": "Optimize ORM queries and implement query caching"},
            {"agent": "ui-systems", "task": "Optimize UI rendering, bundle size, and implement code splitting"},
            {"agent": "platform-deployment", "task": "Configure edge caching, CDN, and optimize Vercel deployment"}
        ]
    }
}

# Save enhanced chains
data["chains"] = chains
data["shortcuts"] = shortcuts

# Write back
output_file = Path(".claude/chains-enhanced.json")
with open(output_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ Enhanced chains saved to: {output_file}")
print(f"📊 Stats:")
print(f"  - Enhanced existing chains: {len(enhancements)}")
print(f"  - Added new chains: {len(new_chains)}")
print(f"  - Added shortcuts: {len(new_shortcuts)}")
print("\nTo apply changes:")
print(f"  cp {output_file} .claude/chains.json")
