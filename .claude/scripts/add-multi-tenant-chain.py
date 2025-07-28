#!/usr/bin/env python3
"""
Add multi-tenant-setup chain to chains.json
"""

import json

# Load chains
with open('.claude/chains.json', 'r') as f:
    data = json.load(f)

# Add multi-tenant-setup chain
new_chain = {
    "multi-tenant-setup": {
        "description": "Complete multi-tenant SaaS setup with isolation and security",
        "steps": [
            {"agent": "pm-orchestrator", "task": "Define tenant isolation requirements"},
            {"agent": "supabase-specialist", "task": "Design RLS policies for tenant isolation"},
            {"agent": "orm-specialist", "task": "Create multi-tenant schema with tenant_id"},
            {"agent": "event-schema", "task": "Design tenant-aware event tracking"},
            {"agent": "backend", "task": "Implement tenant context middleware"},
            {"agent": "privacy-compliance", "task": "Ensure tenant data privacy compliance"},
            {"agent": "ui-systems", "task": "Build tenant switcher UI components"},
            {"agent": "platform-deployment", "task": "Configure per-tenant edge routing"},
            {"agent": "qa", "task": "Test tenant isolation thoroughly"},
            {"agent": "documentation-writer", "task": "Document multi-tenant architecture"}
        ]
    }
}

# Add to chains
data['chains'].update(new_chain)

# Add shortcut
data['shortcuts']['mts'] = 'multi-tenant-setup'

# Save
with open('.claude/chains.json', 'w') as f:
    json.dump(data, f, indent=2)

print("✅ Added multi-tenant-setup chain")
print("✅ Added shortcut 'mts'")
