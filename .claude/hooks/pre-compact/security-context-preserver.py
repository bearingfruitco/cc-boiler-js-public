#!/usr/bin/env python3
"""
Security Context Preserver - PreCompact Hook
Preserves security requirements and status during context compaction
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def extract_security_context():
    """Extract security-related context to preserve"""
    security_context = {
        'active_vulnerabilities': [],
        'security_policies': [],
        'pending_audits': [],
        'security_requirements': []
    }
    
    # Check for active vulnerabilities
    vuln_file = Path('.claude/security/vulnerabilities.json')
    if vuln_file.exists():
        try:
            with open(vuln_file, 'r') as f:
                vulns = json.load(f)
                security_context['active_vulnerabilities'] = [
                    {
                        'id': v.get('id'),
                        'severity': v.get('severity'),
                        'description': v.get('description', '')[:100]  # Truncate for compaction
                    }
                    for v in vulns.get('active', [])
                ]
        except:
            pass
    
    # Check for security policies
    policy_file = Path('.claude/security/policies.json')
    if policy_file.exists():
        try:
            with open(policy_file, 'r') as f:
                policies = json.load(f)
                security_context['security_policies'] = policies.get('active_policies', [])
        except:
            pass
    
    # Check for pending audits
    audit_file = Path('.claude/security/pending-audits.json')
    if audit_file.exists():
        try:
            with open(audit_file, 'r') as f:
                audits = json.load(f)
                security_context['pending_audits'] = audits
        except:
            pass
    
    # Check for security requirements from PRD
    prd_locations = [
        Path('PRD.md'),
        Path('.claude/PRD.md'),
        Path('docs/project/PROJECT_PRD.md')
    ]
    
    for prd_path in prd_locations:
        if prd_path.exists():
            try:
                content = prd_path.read_text()
                # Extract security section
                if 'Security Requirements' in content:
                    start = content.find('Security Requirements')
                    end = content.find('\n#', start)
                    if end == -1:
                        end = len(content)
                    security_section = content[start:end].strip()[:500]  # Limit size
                    security_context['security_requirements'].append({
                        'source': str(prd_path),
                        'content': security_section
                    })
            except:
                pass
    
    return security_context

def save_security_context(context):
    """Save security context for preservation"""
    context_dir = Path('.claude/context/preserved')
    context_dir.mkdir(parents=True, exist_ok=True)
    
    context_file = context_dir / 'security-context.json'
    
    # Add metadata
    context['preserved_at'] = datetime.now().isoformat()
    context['version'] = '1.0'
    
    with open(context_file, 'w') as f:
        json.dump(context, f, indent=2)
    
    return context_file

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = {}
        if not sys.stdin.isatty():
            try:
                input_data = json.loads(sys.stdin.read())
            except:
                pass
        
        # Extract security context
        security_context = extract_security_context()
        
        # Check if there's important security context to preserve
        has_important_context = (
            security_context['active_vulnerabilities'] or
            security_context['security_policies'] or
            security_context['pending_audits'] or
            security_context['security_requirements']
        )
        
        if has_important_context:
            # Save security context
            context_file = save_security_context(security_context)
            
            # Create preservation notice
            notice = "🔒 Security Context Preserved\n\n"
            
            if security_context['active_vulnerabilities']:
                notice += f"• {len(security_context['active_vulnerabilities'])} active vulnerabilities\n"
            
            if security_context['security_policies']:
                notice += f"• {len(security_context['security_policies'])} security policies\n"
            
            if security_context['pending_audits']:
                notice += f"• {len(security_context['pending_audits'])} pending audits\n"
            
            if security_context['security_requirements']:
                notice += f"• Security requirements from {len(security_context['security_requirements'])} sources\n"
            
            notice += f"\nPreserved to: {context_file}"
            
            # Output notice to stderr
            print(notice, file=sys.stderr)
        
        # PreCompact hooks just exit normally
        sys.exit(0)
        
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"Security context preserver error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
