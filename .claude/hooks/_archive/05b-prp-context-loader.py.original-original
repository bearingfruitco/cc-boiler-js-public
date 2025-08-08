#!/usr/bin/env python3
"""
Automatically load relevant PRP context based on current work
"""

import json
import sys
import os
from pathlib import Path

def hook_pre_tool_use(params, state):
    """Load PRP context when relevant"""
    
    # Check if we should load PRP context
    if not should_load_prp_context(params):
        return
    
    # Find relevant PRPs
    relevant_prps = find_relevant_prps(params)
    
    if not relevant_prps:
        return
    
    # Load PRP context into state
    for prp_name in relevant_prps:
        load_prp_context(prp_name, state)
    
    print(f"📚 Loaded PRP context: {', '.join(relevant_prps)}")

def should_load_prp_context(params):
    """Determine if PRP context is needed"""
    
    tool = params.get('tool', '')
    
    # Always load for certain tools
    if tool in ['EditTool', 'CreateTool', 'BashCommand']:
        return True
    
    # Load if command references PRPs
    if tool == 'ReadTool':
        path = params.get('path', '')
        if 'PRPs/' in path or any(marker in path for marker in [
            'validation', 'blueprint', 'implementation'
        ]):
            return True
    
    return False

def find_relevant_prps(params):
    """Find PRPs relevant to current action"""
    
    relevant = []
    
    # Get current file/command
    current_context = extract_context(params)
    
    # Check each active PRP
    active_prps = list(Path('PRPs/active/').glob('*.md'))
    
    for prp_path in active_prps:
        prp_name = prp_path.stem
        
        # Read PRP to check relevance
        with open(prp_path) as f:
            prp_content = f.read()
        
        # Check if current work relates to this PRP
        if is_prp_relevant(prp_name, prp_content, current_context):
            relevant.append(prp_name)
    
    return relevant[:2]  # Limit to 2 most relevant

def extract_context(params):
    """Extract context from current action"""
    
    context = {
        'tool': params.get('tool', ''),
        'path': params.get('path', ''),
        'command': params.get('command', ''),
        'content': params.get('content', '')[:500]  # First 500 chars
    }
    
    return context

def is_prp_relevant(prp_name, prp_content, context):
    """Check if PRP is relevant to current context"""
    
    # Check direct name match
    if prp_name in context['path'] or prp_name in context['command']:
        return True
    
    # Check feature name variants
    feature_variants = [
        prp_name,
        prp_name.replace('-', '_'),
        prp_name.replace('-', ''),
    ]
    
    for variant in feature_variants:
        if variant in context['path'] or variant in context['content']:
            return True
    
    # Check if files mentioned in PRP
    if context['path']:
        if context['path'] in prp_content:
            return True
    
    return False

def load_prp_context(prp_name, state):
    """Load PRP context into state"""
    
    prp_path = Path(f'PRPs/active/{prp_name}.md')
    if not prp_path.exists():
        return
    
    # Extract key sections
    with open(prp_path) as f:
        content = f.read()
    
    # Parse important sections
    sections = parse_prp_sections(content)
    
    # Add to state context
    if 'prp_context' not in state:
        state['prp_context'] = {}
    
    state['prp_context'][prp_name] = {
        'gotchas': sections.get('gotchas', []),
        'patterns': sections.get('patterns', []),
        'validation': sections.get('validation', {}),
        'context_files': sections.get('context_files', [])
    }

def parse_prp_sections(content):
    """Parse PRP content into sections"""
    
    sections = {
        'gotchas': [],
        'patterns': [],
        'validation': {},
        'context_files': []
    }
    
    # Extract gotchas
    import re
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

# Ensure we always output valid JSON
sys.exit(0)
