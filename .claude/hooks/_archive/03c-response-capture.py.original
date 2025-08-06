#!/usr/bin/env python3
"""
Response Capture Hook - Capture Claude's responses for potential issue creation
Stores summaries, plans, and implementation details
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
import hashlib

def get_config():
    """Load hook configuration"""
    config_path = Path(__file__).parent.parent / 'config.json'
    with open(config_path) as f:
        return json.load(f)

def get_claude_context():
    """Get Claude's last response from context"""
    context_path = Path(__file__).parent.parent / 'context' / 'last_response.json'
    
    if context_path.exists():
        with open(context_path) as f:
            return json.load(f)
    
    return None

def extract_sections(content):
    """Extract structured sections from Claude's response"""
    sections = {
        'summary': None,
        'plan': None,
        'implementation': None,
        'tasks': [],
        'components': [],
        'dependencies': []
    }
    
    # Extract summary
    summary_patterns = [
        r'## Summary\n(.*?)(?=\n##|\Z)',
        r'### Summary\n(.*?)(?=\n###|\Z)',
        r'Summary:\s*(.*?)(?=\n\n|\Z)'
    ]
    
    for pattern in summary_patterns:
        import re
        match = re.search(pattern, content, re.DOTALL)
        if match:
            sections['summary'] = match.group(1).strip()
            break
    
    # Extract plan/implementation
    plan_patterns = [
        r'## (?:Implementation )?Plan\n(.*?)(?=\n##|\Z)',
        r'### (?:Implementation )?Plan\n(.*?)(?=\n###|\Z)',
        r'Implementation steps:\s*(.*?)(?=\n\n|\Z)'
    ]
    
    for pattern in plan_patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            sections['plan'] = match.group(1).strip()
            break
    
    # Extract tasks (numbered lists)
    task_pattern = r'^\d+\.\s+(.+)$'
    tasks = re.findall(task_pattern, content, re.MULTILINE)
    sections['tasks'] = tasks[:10]  # Max 10 tasks
    
    # Extract component mentions
    component_pattern = r'(?:component|Component)\s+`?(\w+)`?'
    components = re.findall(component_pattern, content)
    sections['components'] = list(set(components))[:10]
    
    # Extract dependency mentions
    dep_patterns = [
        r'depends on\s+`?(\w+)`?',
        r'uses\s+`?(\w+)`?',
        r'requires\s+`?(\w+)`?'
    ]
    
    dependencies = []
    for pattern in dep_patterns:
        deps = re.findall(pattern, content, re.IGNORECASE)
        dependencies.extend(deps)
    
    sections['dependencies'] = list(set(dependencies))[:10]
    
    return sections

def should_capture_response(content):
    """Determine if this response should be captured"""
    # Keywords that indicate a plan/summary worth capturing
    capture_keywords = [
        'implementation plan',
        'here\'s how',
        'summary',
        'approach',
        'strategy',
        'we\'ll implement',
        'steps:',
        'to implement',
        'architecture',
        'solution'
    ]
    
    content_lower = content.lower()
    return any(keyword in content_lower for keyword in capture_keywords)

def save_captured_response(content, sections, metadata):
    """Save captured response for later use"""
    captures_dir = Path(__file__).parent.parent / 'captures'
    captures_dir.mkdir(exist_ok=True)
    
    # Generate unique ID
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
    capture_id = f"capture_{timestamp}_{content_hash}"
    
    capture_data = {
        'id': capture_id,
        'timestamp': datetime.now().isoformat(),
        'content': content,
        'sections': sections,
        'metadata': metadata,
        'converted_to_issue': False
    }
    
    # Save to file
    capture_file = captures_dir / f"{capture_id}.json"
    with open(capture_file, 'w') as f:
        json.dump(capture_data, f, indent=2)
    
    # Update index
    update_capture_index(capture_id, sections.get('summary', 'No summary'))
    
    return capture_id

def update_capture_index(capture_id, summary):
    """Update capture index for easy retrieval"""
    index_path = Path(__file__).parent.parent / 'captures' / 'index.json'
    
    if index_path.exists():
        with open(index_path) as f:
            index = json.load(f)
    else:
        index = {'captures': []}
    
    # Add new capture
    index['captures'].insert(0, {
        'id': capture_id,
        'timestamp': datetime.now().isoformat(),
        'summary': summary[:100] + '...' if len(summary) > 100 else summary
    })
    
    # Keep only last 50 captures
    index['captures'] = index['captures'][:50]
    
    with open(index_path, 'w') as f:
        json.dump(index, f, indent=2)

def get_current_context():
    """Get current work context"""
    return {
        'branch': get_git_branch(),
        'issue': extract_issue_number(),
        'modified_files': get_modified_files()
    }

def get_git_branch():
    """Get current git branch"""
    try:
        import subprocess
        result = subprocess.run(
            "git branch --show-current",
            shell=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except:
        return 'unknown'

def extract_issue_number():
    """Extract issue number from branch name"""
    branch = get_git_branch()
    if '/' in branch:
        parts = branch.split('/')[-1].split('-')
        if parts[0].isdigit():
            return parts[0]
    return None

def get_modified_files():
    """Get list of recently modified files"""
    try:
        import subprocess
        result = subprocess.run(
            "git status --porcelain | head -10",
            shell=True,
            capture_output=True,
            text=True
        )
        
        files = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                files.append(line[3:])
        return files
    except:
        return []

def main():
    try:
        """Main hook logic"""
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
    
        # This is a post-tool-use hook, so we capture after responses
        # Get Claude's last response (this would need integration with Claude Code)
        # For now, we'll check if there's a response to capture
    
        config = get_config()
    
        # Check if response capture is enabled
        if not config.get('capture', {}).get('auto_capture', True):
                    return
    
        # In a real implementation, we'd get Claude's actual response
        # For this example, we'll check if the tool operation suggests a response was given
        if input_data.get('tool') == 'assistant_response':
            content = input_data.get('content', '')
        
            if should_capture_response(content):
                sections = extract_sections(content)
                metadata = get_current_context()
            
                if sections['summary'] or sections['plan']:
                    capture_id = save_captured_response(content, sections, metadata)
                
                    print(json.dumps({
                        sys.exit(0)
                    return
    
        sys.exit(0)

    except Exception as e:
if __name__ == "__main__":
    main()
