#!/usr/bin/env python3
"""
AI Docs Check Hook - Ensures AI documentation is referenced appropriately
Suggests relevant AI docs based on code patterns
"""

import json
import sys
import re
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def get_ai_docs_mapping():
    """Define mappings between code patterns and relevant AI docs"""
    return {
        'nextjs_patterns': {
            'patterns': [
                r'use client',
                r'export\s+default\s+async\s+function',
                r'generateMetadata',
                r'loading\.tsx',
                r'error\.tsx',
                r'app/.*page\.tsx',
                r'cookies\(\)',
                r'headers\(\)'
            ],
            'doc': 'nextjs_15_patterns.md',
            'reason': 'Uses Next.js 15 patterns'
        },
        'supabase_patterns': {
            'patterns': [
                r'createClient',
                r'supabase\.',
                r'from\([\'"`]\w+[\'"`]\)',
                r'\.auth\.',
                r'\.storage\.',
                r'realtime',
                r'row level security',
                r'RLS'
            ],
            'doc': 'supabase_patterns.md',
            'reason': 'Implements Supabase functionality'
        },
        'typescript_gotchas': {
            'patterns': [
                r'as\s+any',
                r'@ts-ignore',
                r'@ts-expect-error',
                r'satisfies',
                r'extends\s+.*\?',
                r'infer\s+',
                r'keyof\s+',
                r'typeof\s+'
            ],
            'doc': 'typescript_gotchas.md',
            'reason': 'Uses advanced TypeScript features'
        },
        'design_system': {
            'patterns': [
                r'className=',
                r'text-size-\d',
                r'font-(?:regular|semibold)',
                r'(?:p|m|gap)-\d+',
                r'h-(?:11|12)',
                r'rounded-xl'
            ],
            'doc': 'design_system_rules.md',
            'reason': 'Implements UI components'
        },
        'security_patterns': {
            'patterns': [
                r'encrypt',
                r'decrypt',
                r'hash',
                r'sanitize',
                r'validate',
                r'auth(?:enticate|orize)',
                r'pii|phi',
                r'sensitive'
            ],
            'doc': 'security_requirements.md',
            'reason': 'Handles sensitive data or authentication'
        },
        'async_patterns': {
            'patterns': [
                r'Promise\.all',
                r'async\s+function',
                r'await\s+',
                r'eventQueue',
                r'setTimeout',
                r'setInterval',
                r'loading\s*:\s*true',
                r'isLoading'
            ],
            'doc': 'async_patterns.md',
            'reason': 'Uses asynchronous operations'
        },
        'testing_strategies': {
            'patterns': [
                r'describe\(',
                r'test\(',
                r'it\(',
                r'expect\(',
                r'\.toEqual',
                r'\.toBe',
                r'mock',
                r'spy',
                r'render\('
            ],
            'doc': 'testing_strategies.md',
            'reason': 'Implements tests'
        }
    }

def check_ai_docs_usage(content, file_path):
    """Check if relevant AI docs are referenced"""
    recommendations = []
    ai_docs_mapping = get_ai_docs_mapping()
    
    # Determine file type
    file_type = 'other'
    if '/components/' in file_path:
        file_type = 'component'
    elif '/app/api/' in file_path or '/pages/api/' in file_path:
        file_type = 'api'
    elif 'PRPs/' in file_path and file_path.endswith('.md'):
        file_type = 'prp'
    elif file_path.endswith('.test.tsx') or file_path.endswith('.test.ts'):
        file_type = 'test'
    
    # Check each pattern category
    for category, config in ai_docs_mapping.items():
        # Check if any patterns match
        matches = False
        for pattern in config['patterns']:
            if re.search(pattern, content, re.IGNORECASE):
                matches = True
                break
        
        if matches:
            # Check if the doc is already referenced
            doc_name = config['doc']
            if f'ai_docs/{doc_name}' not in content and doc_name not in content:
                recommendations.append({
                    'doc': doc_name,
                    'reason': config['reason'],
                    'category': category
                })
    
    # Special checks for PRPs
    if file_type == 'prp':
        # PRPs should reference relevant docs in their context section
        if not re.search(r'ai_docs/', content):
            # Check what the PRP is about
            if 'component' in content.lower() or 'ui' in content.lower():
                if not any(r['doc'] == 'design_system_rules.md' for r in recommendations):
                    recommendations.append({
                        'doc': 'design_system_rules.md',
                        'reason': 'PRP involves UI components',
                        'category': 'design_system'
                    })
            
            if 'auth' in content.lower() or 'user' in content.lower():
                if not any(r['doc'] == 'security_requirements.md' for r in recommendations):
                    recommendations.append({
                        'doc': 'security_requirements.md',
                        'reason': 'PRP involves authentication/users',
                        'category': 'security'
                    })
    
    return recommendations

def get_ai_doc_snippet(doc_name):
    """Get a helpful snippet about what the AI doc contains"""
    snippets = {
        'nextjs_15_patterns.md': 'Server components, async patterns, app router, form actions',
        'supabase_patterns.md': 'Auth flows, RLS policies, real-time subscriptions, storage',
        'typescript_gotchas.md': 'Type safety, common errors, advanced patterns, strict mode',
        'design_system_rules.md': '4 sizes, 2 weights, 4px grid, component patterns',
        'security_requirements.md': 'PII/PHI handling, encryption, audit logging, TCPA/GDPR',
        'async_patterns.md': 'Event queue, parallel operations, loading states, error handling',
        'testing_strategies.md': 'Unit tests, integration tests, mocking, best practices'
    }
    return snippets.get(doc_name, 'Patterns and best practices')

def main():
    """Main hook logic"""
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    # Only process file write/edit operations
    if input_data['tool'] not in ['write_file', 'edit_file', 'str_replace']:
        print(json.dumps({"action": "continue"}))
        return
    
    file_path = input_data.get('path', '')
    content = input_data.get('content', '')
    
    # Skip if it's an AI doc itself
    if 'ai_docs/' in file_path:
        print(json.dumps({"action": "continue"}))
        return
    
    # Check for AI docs usage
    recommendations = check_ai_docs_usage(content, file_path)
    
    if recommendations:
        # For PRPs, be more insistent
        is_prp = 'PRPs/' in file_path and file_path.endswith('.md')
        
        message = "💡 AI DOCS RECOMMENDATIONS\n\n"
        
        if is_prp:
            message += "PRPs should reference relevant AI docs for patterns:\n\n"
        else:
            message += "Consider referencing these AI docs:\n\n"
        
        # Group by importance
        high_priority = []
        normal_priority = []
        
        for rec in recommendations:
            if rec['category'] in ['security_patterns', 'design_system']:
                high_priority.append(rec)
            else:
                normal_priority.append(rec)
        
        # Show high priority first
        if high_priority:
            message += "🔴 High Priority:\n"
            for rec in high_priority:
                snippet = get_ai_doc_snippet(rec['doc'])
                message += f"  • {rec['doc']}\n"
                message += f"    {rec['reason']}\n"
                message += f"    Contains: {snippet}\n\n"
        
        # Then normal priority
        if normal_priority:
            if high_priority:
                message += "🟡 Suggested:\n"
            for rec in normal_priority:
                snippet = get_ai_doc_snippet(rec['doc'])
                message += f"  • {rec['doc']}\n"
                message += f"    {rec['reason']}\n"
                message += f"    Contains: {snippet}\n\n"
        
        # Add usage example for PRPs
        if is_prp:
            message += "📝 Add to your PRP's Required Context section:\n"
            message += "```yaml\n"
            for rec in recommendations[:2]:  # Show max 2 examples
                message += f"- doc: PRPs/ai_docs/{rec['doc']}\n"
                message += f"  why: {rec['reason']}\n"
                message += f"  critical: Key patterns to follow\n\n"
            message += "```\n"
        
        # Add location info
        message += f"\n📁 AI docs location: PRPs/ai_docs/"
        
        # Determine action based on file type and priority
        action = "warn"
        if is_prp and high_priority:
            # For PRPs with security/design concerns, consider blocking
            # But let's be helpful and just warn strongly
            message = "⚠️ IMPORTANT: " + message
        
        print(json.dumps({
            "action": action,
            "message": message,
            "recommendations": [r['doc'] for r in recommendations],
            "file_type": 'prp' if is_prp else 'code'
        }))
    else:
        # Check if this is a good example of AI docs usage
        if 'ai_docs/' in content:
            doc_refs = re.findall(r'ai_docs/(\w+\.md)', content)
            if doc_refs:
                # Positive reinforcement
                print(json.dumps({
                    "action": "continue",
                    "message": f"✅ Good AI docs usage: {', '.join(set(doc_refs))}",
                    "ai_docs_referenced": list(set(doc_refs))
                }))
            else:
                print(json.dumps({"action": "continue"}))
        else:
            print(json.dumps({"action": "continue"}))

if __name__ == "__main__":
    main()
