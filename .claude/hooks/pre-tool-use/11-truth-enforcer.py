#!/usr/bin/env python3
"""
Truth Enforcer Hook - Prevent changing established project facts
Protects values like API endpoints, component names, established patterns
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
    # Check for override file
    override_file = Path('.claude/truth-override.json')
    if override_file.exists():
        try:
            with open(override_file) as f:
                override = json.load(f)
                # Check if override is recent (within 1 hour)
                timestamp = datetime.fromisoformat(override['timestamp'])
                if (datetime.now() - timestamp).seconds < 3600:
                    return True, override.get('reason', 'Manual override')
        except:
            pass
    
    return False, None

def check_truth_violations(tool_input, truths):
    """Check if changes violate established truths"""
    violations = []
    
    # Get file path and content
    file_path = tool_input.get('file_path', tool_input.get('path', ''))
    new_content = tool_input.get('content', tool_input.get('new_str', ''))
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
        # Read input
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name - handle multiple formats
        tool_name = input_data.get('tool_name', '')
        if not tool_name and 'tool_use' in input_data:
            tool_name = input_data['tool_use'].get('name', '')
        
        # Only check write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            sys.exit(0)
            return
        
        # Extract parameters
        tool_input = input_data.get('tool_input', {})
        if not tool_input and 'tool_use' in input_data:
            tool_input = input_data['tool_use'].get('parameters', {})
        
        # Check if this is an intentional change
        is_intentional, reason = is_intentional_change()
        
        # Load current truths
        truths = load_project_truths()
        
        # Check for violations
        violations = check_truth_violations(tool_input, truths)
        
        if violations:
            # If intentional, just warn
            if is_intentional:
                warning_msg = "⚠️ Truth Override: Changing established values\n\n"
                warning_msg += f"Reason: {reason}\n\n"
                
                for v in violations:
                    warning_msg += f"📝 {v['message']}\n"
                    warning_msg += f"   Current: {v['established']}\n"
                    warning_msg += f"   Location: {v['source']}\n\n"
                
                warning_msg += "✅ Proceeding with intentional change.\n"
                warning_msg += "Remember to update all references!"
                
                print(warning_msg)  # Warning shown in transcript
        sys.exit(0)
            else:
                # Not intentional - format error message
                error_msg = "🚫 Truth Enforcement: Cannot change established facts\n\n"
                
                # Check severity
                high_severity = any(v['severity'] == 'high' for v in violations)
                
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
                
                # Only block for high severity violations
                if high_severity:
                    print(error_msg
                    , file=sys.stderr)
        sys.exit(2)
                else:
                    # Warn for low severity
                    print(error_msg)  # Warning shown in transcript
        sys.exit(0)
        else:
            sys.exit(0)
            
    except Exception as e:
        print(json.dumps({
            sys.exit(0)

if __name__ == "__main__":
    main()
    sys.exit(0)
