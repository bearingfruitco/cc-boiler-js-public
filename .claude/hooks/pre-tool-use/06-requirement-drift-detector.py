#!/usr/bin/env python3
"""
Requirement Drift Detector - Prevents drift from locked specifications
Monitors changes to ensure they align with approved requirements
"""

import json
import sys
import re
from pathlib import Path

def load_locked_requirements():
    """Load locked requirements from PRDs"""
    locked_reqs = []
    
    # Check project PRD
    project_prd = Path("docs/project/PROJECT_PRD.md")
    if project_prd.exists():
        try:
            content = project_prd.read_text()
            # Look for locked sections
            locked_matches = re.findall(r'\[LOCKED\](.*?)(?=\n#|\n\[|$)', content, re.DOTALL)
            for match in locked_matches:
                locked_reqs.append({
                    'source': 'PROJECT_PRD.md',
                    'content': match.strip(),
                    'type': 'project'
                })
        except:
            pass
    
    # Check feature PRDs
    features_dir = Path("docs/project/features")
    if features_dir.exists():
        for prd_file in features_dir.glob("*-PRD.md"):
            try:
                content = prd_file.read_text()
                locked_matches = re.findall(r'\[LOCKED\](.*?)(?=\n#|\n\[|$)', content, re.DOTALL)
                for match in locked_matches:
                    locked_reqs.append({
                        'source': prd_file.name,
                        'content': match.strip(),
                        'type': 'feature'
                    })
            except:
                pass
    
    return locked_reqs

def check_for_violations(content, file_path, locked_reqs):
    """Check if changes violate locked requirements"""
    violations = []
    
    # Check for common violation patterns
    violation_patterns = [
        # Trying to change core functionality
        (r'remove.*authentication', 'Attempting to remove authentication'),
        (r'disable.*security', 'Attempting to disable security features'),
        (r'skip.*validation', 'Attempting to skip validation'),
        
        # Changing locked UI elements
        (r'change.*layout', 'Attempting to change locked layout'),
        (r'modify.*design.*system', 'Attempting to modify design system'),
        
        # Data structure changes
        (r'alter.*schema', 'Attempting to alter locked schema'),
        (r'change.*model', 'Attempting to change data model')
    ]
    
    content_lower = content.lower()
    
    for pattern, message in violation_patterns:
        if re.search(pattern, content_lower):
            # Check if this relates to a locked requirement
            for req in locked_reqs:
                if any(keyword in req['content'].lower() for keyword in pattern.split('.*')):
                    violations.append({
                        'pattern': pattern,
                        'message': message,
                        'locked_req': req
                    })
    
    return violations

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name
        tool_name = input_data.get('tool_name', '')
        
        # Only check write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            # Not a write operation - continue
            sys.exit(0)
        
        # Extract parameters
        tool_input = input_data.get('tool_input', {})
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        if not content:
            sys.exit(0)
        
        # Load locked requirements
        locked_reqs = load_locked_requirements()
        
        if not locked_reqs:
            # No locked requirements - continue
            sys.exit(0)
        
        # Check for violations
        violations = check_for_violations(content, file_path, locked_reqs)
        
        if violations:
            # Build violation message
            message = "🔒 REQUIREMENT DRIFT DETECTED\n\n"
            message += "Your changes may violate locked requirements:\n\n"
            
            for v in violations:
                message += f"❌ {v['message']}\n"
                message += f"   Locked in: {v['locked_req']['source']}\n"
                message += f"   Requirement: {v['locked_req']['content'][:100]}...\n\n"
            
            message += "Locked requirements cannot be changed without approval.\n"
            message += "If this change is necessary, please:\n"
            message += "1. Document the reason for change\n"
            message += "2. Get approval from the project owner\n"
            message += "3. Update the PRD with [UPDATED] marker"
            
            # Block the change
            print(json.dumps({
                "decision": "block",
                "message": message
            }))
            sys.exit(0)
        
        # No violations - continue
        sys.exit(0)
        
    except Exception as e:
        # On error, log to stderr and exit with non-zero
        print(f"Requirement drift detector error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
