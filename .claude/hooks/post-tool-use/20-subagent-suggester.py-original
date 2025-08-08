#!/usr/bin/env python3
"""
Subagent Suggestion Hook - Suggests relevant sub-agents based on file operations
"""

import sys
import json
import os
import re

def get_hook_input():
    """Get and parse hook input from stdin"""
    try:
        return json.loads(sys.stdin.read())
    except:
        return {}

def suggest_agents_for_file(filepath):
    """Suggest relevant sub-agents based on file type and content"""
    suggestions = []
    
    # Extract file extension and path components
    ext = os.path.splitext(filepath)[1].lower()
    path_lower = filepath.lower()
    
    # Frontend files
    if ext in ['.tsx', '.jsx', '.css', '.scss'] or 'components/' in path_lower:
        suggestions.append({
            'agent': 'frontend-ux-specialist',
            'reason': 'UI component - ensure design system compliance',
            'command': 'use frontend-ux-specialist subagent to review and enhance UI'
        })
    
    # Backend/API files
    if '/api/' in path_lower or ext in ['.py', '.go', '.java'] or 'server' in path_lower:
        suggestions.append({
            'agent': 'backend-reliability-engineer',
            'reason': 'Backend code - ensure reliability and error handling',
            'command': 'use backend-reliability-engineer subagent to review API patterns'
        })
    
    # Test files
    if 'test' in path_lower or ext in ['.test.ts', '.spec.ts', '.test.tsx']:
        suggestions.append({
            'agent': 'qa-test-engineer',
            'reason': 'Test file - ensure comprehensive coverage',
            'command': 'use qa-test-engineer subagent to enhance test coverage'
        })
        suggestions.append({
            'agent': 'tdd-engineer',
            'reason': 'Follow TDD principles for test implementation',
            'command': 'use tdd-engineer subagent to implement test-first approach'
        })
    
    # Authentication/Security files
    security_patterns = ['auth', 'login', 'password', 'token', 'secret', 'security', 'permission']
    if any(pattern in path_lower for pattern in security_patterns):
        suggestions.append({
            'agent': 'security-threat-analyst',
            'reason': 'Security-sensitive code detected',
            'command': 'use security-threat-analyst subagent to audit security'
        })
    
    # Database files
    if 'schema' in path_lower or 'migration' in path_lower or ext in ['.sql', '.prisma']:
        suggestions.append({
            'agent': 'database-architect',
            'reason': 'Database changes - ensure proper design',
            'command': 'use database-architect subagent to review schema design'
        })
    
    # Documentation files
    if ext in ['.md', '.mdx'] or 'docs/' in path_lower or 'README' in filepath:
        suggestions.append({
            'agent': 'documentation-writer',
            'reason': 'Documentation file - ensure clarity and completeness',
            'command': 'use documentation-writer subagent to enhance documentation'
        })
    
    # Performance-critical files
    perf_patterns = ['optimize', 'performance', 'cache', 'worker', 'queue']
    if any(pattern in path_lower for pattern in perf_patterns):
        suggestions.append({
            'agent': 'performance-optimizer',
            'reason': 'Performance-critical code',
            'command': 'use performance-optimizer subagent to analyze performance'
        })
    
    # Form-related files
    if 'form' in path_lower or 'input' in path_lower:
        suggestions.append({
            'agent': 'smart-form-builder',
            'reason': 'Form component detected',
            'command': 'use smart-form-builder subagent to enhance form UX'
        })
    
    return suggestions

def main():
    # Get hook input
    hook_data = get_hook_input()
    
    # Only process Write, Edit, and MultiEdit operations
    tool_name = hook_data.get('tool_use', {}).get('tool_name', '')
    if tool_name not in ['Write', 'Edit', 'MultiEdit']:
        return
    
    # Get file path
    parameters = hook_data.get('tool_use', {}).get('parameters', {})
    filepath = parameters.get('path', parameters.get('paths', [''])[0] if 'paths' in parameters else '')
    
    if not filepath:
        return
    
    # Get suggestions for this file
    suggestions = suggest_agents_for_file(filepath)
    
    if suggestions:
        print("\n💡 **Sub-Agent Suggestions**")
        print(f"Based on your work with `{os.path.basename(filepath)}`, consider using:\n")
        
        for suggestion in suggestions:
            print(f"• **{suggestion['agent']}** - {suggestion['reason']}")
            print(f"  ```")
            print(f"  {suggestion['command']}")
            print(f"  ```")
        
        print("\n💬 Quick aliases available: `fe` (frontend), `be` (backend), `qa` (QA), `sec` (security)")

if __name__ == "__main__":
    main()
