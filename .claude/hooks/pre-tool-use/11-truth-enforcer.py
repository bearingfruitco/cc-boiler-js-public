#!/usr/bin/env python3
"""
Truth Enforcer Hook - Prevent changing established project facts
Compliant with official Claude Code hooks documentation
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def get_truths_file():
    """Get the project truths file location"""
    return Path('.claude/project-truths.json')

def load_project_truths():
    """Load established project facts"""
    truths_file = get_truths_file()
    
    if not truths_file.exists():
        return {
            'api_endpoints': {},
            'database_tables': {},
            'component_names': {},
            'feature_flags': {},
            'constants': {},
            'components': {}
        }
    
    try:
        with open(truths_file) as f:
            return json.load(f)
    except:
        return {}

def is_intentional_change():
    """Check if this is an intentional refactor"""
    override_file = Path('.claude/truth-override.json')
    if override_file.exists():
        try:
            with open(override_file) as f:
                override = json.load(f)
                timestamp = datetime.fromisoformat(override['timestamp'])
                if (datetime.now() - timestamp).seconds < 3600:
                    return True, override.get('reason', 'Manual override')
        except:
            pass
    
    return False, None

def check_truth_violations(tool_input, truths, tool_name=''):
    """Check if changes violate established truths"""
    violations = []
    
    file_path = tool_input.get('file_path', '')
    new_content = tool_input.get('content', '')
    
    # For Edit/MultiEdit, content is in new_str
    if new_content == '' and tool_name in ['Edit', 'MultiEdit']:
        new_content = tool_input.get('new_str', '')
    old_content = tool_input.get('old_str', '')
    
    if not new_content:
        return violations
    
    # Check API endpoints
    for endpoint, details in truths.get('api_endpoints', {}).items():
        if endpoint in old_content and endpoint not in new_content:
            violations.append({
                'type': 'api_endpoint_change',
                'message': f"Changing established API endpoint: {endpoint}",
                'established': endpoint,
                'source': details.get('file', 'unknown'),
                'severity': 'high'
            })
    
    # Check component names
    for comp_name, details in truths.get('component_names', {}).items():
        if comp_name in old_content and comp_name not in new_content:
            violations.append({
                'type': 'component_name_change',
                'message': f"Changing established component name: {comp_name}",
                'established': comp_name,
                'source': details.get('file', 'unknown'),
                'severity': 'high'
            })
    
    # Check database tables
    for table_name, details in truths.get('database_tables', {}).items():
        if table_name in old_content and table_name not in new_content:
            violations.append({
                'type': 'database_table_change',
                'message': f"Changing established table name: {table_name}",
                'established': table_name,
                'source': details.get('file', 'unknown'),
                'severity': 'high'
            })
    
    return violations

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        try:
            input_data = json.loads(sys.stdin.read())
        except (json.JSONDecodeError, ValueError):
            # No valid JSON on stdin (e.g., when run directly for testing)
            sys.exit(0)
        
        # Extract tool name from input data
        tool_name = input_data.get('tool_name', '')
        
        # Only check write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            # Not a write operation - continue normally
            sys.exit(0)
        
        # Extract tool input
        tool_input = input_data.get('tool_input', {})
        
        # Check if this is an intentional change
        is_intentional, reason = is_intentional_change()
        
        # Load current truths
        truths = load_project_truths()
        
        # Check for violations
        violations = check_truth_violations(tool_input, truths, tool_name)
        
        if violations:
            high_severity = any(v['severity'] == 'high' for v in violations)
            
            # Format error message
            error_msg = "🚫 Truth Enforcement: Cannot change established facts\n\n"
            
            for v in violations:
                emoji = "🔴" if v['severity'] == 'high' else "⚠️"
                error_msg += f"{emoji} {v['message']}\n"
                error_msg += f"   Established in: {v['source']}\n"
                error_msg += f"   Value: {v['established']}\n\n"
            
            error_msg += "These are established project facts.\n\n"
            error_msg += "To make intentional changes:\n"
            error_msg += "1. Add 'refactor' or 'update api' to your task description\n"
            error_msg += "2. Create override file: .claude/truth-override.json\n"
            error_msg += "3. Update ALL references across the codebase\n"
            error_msg += "4. Run /facts to see all established values"
            
            if is_intentional:
                # If intentional, just output warning to stderr but continue
                warning_msg = "⚠️ Truth Override: Changing established values\n\n"
                warning_msg += f"Reason: {reason}\n\n"
                
                for v in violations:
                    warning_msg += f"📝 {v['message']}\n"
                    warning_msg += f"   Current: {v['established']}\n"
                    warning_msg += f"   Location: {v['source']}\n\n"
                
                warning_msg += "✅ Proceeding with intentional change.\n"
                warning_msg += "Remember to update all references!"
                
                # Output warning to stderr and continue normally
                print(warning_msg, file=sys.stderr)
                sys.exit(0)
            
            elif high_severity:
                # Block the operation using official format
                print(error_msg, file=sys.stderr)
                sys.exit(2)  # Block operation
            else:
                # Non-blocking - output warning to stderr and continue
                print(error_msg, file=sys.stderr)
                sys.exit(0)
        
        # No violations - continue normally
        sys.exit(0)
            
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"Truth enforcer error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
