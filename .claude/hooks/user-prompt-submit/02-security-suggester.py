#!/usr/bin/env python3
"""
Security Suggester - User Prompt Submit Hook
Suggests security-related commands based on user input
"""

import json
import sys
import os
from pathlib import Path

def analyze_security_intent(prompt):
    """Analyze if user prompt relates to security"""
    security_keywords = [
        'security', 'secure', 'auth', 'authentication', 'authorization',
        'password', 'encrypt', 'decrypt', 'token', 'jwt', 'oauth',
        'vulnerability', 'exploit', 'injection', 'xss', 'csrf',
        'rate limit', 'dos', 'ddos', 'brute force',
        'audit', 'compliance', 'gdpr', 'pci', 'hipaa',
        'api key', 'secret', 'credential', 'certificate',
        'firewall', 'cors', 'csp', 'hsts', 'ssl', 'tls',
        'pentest', 'penetration', 'scan', 'scanner'
    ]
    
    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in security_keywords)

def get_security_suggestions(prompt):
    """Get relevant security command suggestions"""
    suggestions = []
    prompt_lower = prompt.lower()
    
    # API security
    if any(word in prompt_lower for word in ['api', 'endpoint', 'route']):
        suggestions.append({
            'command': '/create-secure-api',
            'description': 'Create API with built-in security features'
        })
        suggestions.append({
            'command': '/security-check api',
            'description': 'Audit API routes for security issues'
        })
    
    # Form security
    if any(word in prompt_lower for word in ['form', 'input', 'submission']):
        suggestions.append({
            'command': '/create-secure-form',
            'description': 'Create form with security best practices'
        })
        suggestions.append({
            'command': '/audit-form-security',
            'description': 'Check forms for security vulnerabilities'
        })
    
    # General security audit
    if any(word in prompt_lower for word in ['audit', 'check', 'scan', 'vulnerability']):
        suggestions.append({
            'command': '/security-audit',
            'description': 'Run comprehensive security audit'
        })
        suggestions.append({
            'command': '/dependency-scan',
            'description': 'Scan dependencies for vulnerabilities'
        })
    
    # Authentication
    if any(word in prompt_lower for word in ['auth', 'login', 'session']):
        suggestions.append({
            'command': '/enhance-security auth',
            'description': 'Add authentication security features'
        })
    
    # RLS / Database security
    if any(word in prompt_lower for word in ['database', 'rls', 'policy', 'supabase']):
        suggestions.append({
            'command': '/generate-rls',
            'description': 'Generate Row Level Security policies'
        })
    
    return suggestions

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
        
        # Get user prompt
        prompt = input_data.get('prompt', '')
        
        if not prompt:
            # No prompt to analyze
            sys.exit(0)
        
        # Check if prompt relates to security
        if analyze_security_intent(prompt):
            suggestions = get_security_suggestions(prompt)
            
            if suggestions:
                # Format suggestions message
                message = "🔒 Security Command Suggestions:\n\n"
                
                for i, suggestion in enumerate(suggestions[:3], 1):  # Max 3 suggestions
                    message += f"{i}. {suggestion['command']}\n"
                    message += f"   {suggestion['description']}\n\n"
                
                message += "💡 Tip: Security is built into many commands with --secure flag"
                
                # Output suggestions to stderr
                print(message, file=sys.stderr)
        
        # UserPromptSubmit hooks just exit normally
        sys.exit(0)
        
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"Security suggester error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
