#!/usr/bin/env python3
"""
PRP Context Loader Hook
Automatically loads relevant PRP context based on current work
"""

import json
import sys
import os
import re
from pathlib import Path

def should_load_prp_context(tool_name, tool_input):
    """Determine if PRP context is needed"""
    
    # Always load for file modification tools
    if tool_name in ['Write', 'Edit', 'MultiEdit']:
        return True
    
    # Load if reading PRP-related files
    if tool_name == 'Read':
        path = tool_input.get('path', '')
        if 'PRPs/' in path or any(marker in path for marker in [
            'validation', 'blueprint', 'implementation'
        ]):
            return True
    
    return False

def find_relevant_prps(tool_input):
    """Find PRPs relevant to current action"""
    relevant = []
    
    # Get current file/command context
    current_path = tool_input.get('file_path', tool_input.get('path', ''))
    current_content = tool_input.get('content', tool_input.get('new_str', ''))[:500]
    
    # Check each active PRP
    prp_dir = Path('PRPs')
    if not prp_dir.exists():
        return relevant
    
    active_prps = list(prp_dir.glob('*-PRP.md'))
    
    for prp_path in active_prps:
        prp_name = prp_path.stem
        
        # Read PRP to check relevance
        try:
            with open(prp_path) as f:
                prp_content = f.read()
            
            # Check if current work relates to this PRP
            if is_prp_relevant(prp_name, prp_content, current_path, current_content):
                relevant.append({
                    'name': prp_name,
                    'path': str(prp_path),
                    'content': prp_content
                })
        except:
            pass
    
    return relevant[:2]  # Limit to 2 most relevant

def is_prp_relevant(prp_name, prp_content, current_path, current_content):
    """Check if PRP is relevant to current context"""
    
    # Check direct name match
    if prp_name in current_path:
        return True
    
    # Check feature name variants
    feature_name = prp_name.replace('-PRP', '')
    feature_variants = [
        feature_name,
        feature_name.replace('-', '_'),
        feature_name.replace('-', ''),
    ]
    
    for variant in feature_variants:
        if variant in current_path or variant in current_content:
            return True
    
    # Check if current file is mentioned in PRP
    if current_path and current_path in prp_content:
        return True
    
    return False

def parse_prp_sections(content):
    """Parse PRP content into sections"""
    sections = {
        'gotchas': [],
        'patterns': [],
        'validation': {},
        'context_files': []
    }
    
    # Extract gotchas
    gotcha_pattern = r'(?:GOTCHA|WARNING|CRITICAL):\s*(.+?)(?:\n|$)'
    sections['gotchas'] = re.findall(gotcha_pattern, content)
    
    # Extract file references
    file_pattern = r'file:\s*([^\s]+)'
    sections['context_files'] = re.findall(file_pattern, content)
    
    # Extract validation commands
    if 'Level 1:' in content:
        level1_match = re.search(r'Level 1:.*?```(?:bash)?\n(.+?)```', content, re.DOTALL)
        if level1_match:
            sections['validation']['level1'] = level1_match.group(1).strip()
    
    return sections

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name and input
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Check if we should load PRP context
        if not should_load_prp_context(tool_name, tool_input):
            # Not relevant - continue normally
            sys.exit(0)
        
        # Find relevant PRPs
        relevant_prps = find_relevant_prps(tool_input)
        
        if not relevant_prps:
            # No relevant PRPs - continue normally
            sys.exit(0)
        
        # Build context message
        message = "📚 PRP CONTEXT LOADED\n\n"
        
        for prp in relevant_prps:
            message += f"Loading context from: {prp['name']}\n"
            
            # Parse important sections
            sections = parse_prp_sections(prp['content'])
            
            if sections['gotchas']:
                message += "\n⚠️ GOTCHAS:\n"
                for gotcha in sections['gotchas'][:3]:  # Max 3
                    message += f"  • {gotcha}\n"
            
            if sections['validation']:
                message += "\n✅ Validation available:\n"
                if 'level1' in sections['validation']:
                    message += f"  • Level 1: {sections['validation']['level1'][:50]}...\n"
            
            if sections['context_files']:
                message += f"\n📁 Related files: {', '.join(sections['context_files'][:3])}\n"
        
        message += f"\nRefer to PRPs for full implementation details."
        
        # Output context message to stderr
        print(message, file=sys.stderr)
        
        # Continue normally
        sys.exit(0)
        
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"PRP context loader error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
