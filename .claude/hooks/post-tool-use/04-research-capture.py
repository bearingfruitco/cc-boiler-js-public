#!/usr/bin/env python3
"""
Research Capture Hook - Captures research data from tool use
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        tool_result = input_data.get('tool_result', {})
        
        # Only capture research-related tools
        research_tools = ['Read', 'SearchFiles', 'Grep', 'web_search']
        if tool_name not in research_tools:
            sys.exit(0)
        
        # Create research entry
        research_entry = {
            'timestamp': datetime.now().isoformat(),
            'tool': tool_name,
            'query': extract_query(tool_name, tool_input),
            'findings': extract_findings(tool_name, tool_result)
        }
        
        # Save to research log
        save_research(research_entry)
        
        # Exit successfully
        sys.exit(0)
        
    except Exception as e:
        # Log error to stderr and exit
        print(f"Research capture error: {str(e)}", file=sys.stderr)
        sys.exit(0)

def extract_query(tool_name, tool_input):
    """Extract the query/search term from tool input"""
    if tool_name == 'SearchFiles':
        return tool_input.get('pattern', '')
    elif tool_name == 'Grep':
        return tool_input.get('pattern', '')
    elif tool_name == 'web_search':
        return tool_input.get('query', '')
    elif tool_name == 'Read':
        return tool_input.get('path', tool_input.get('file_path', ''))
    return ''

def extract_findings(tool_name, tool_result):
    """Extract key findings from tool result"""
    if not tool_result:
        return None
        
    if tool_name == 'SearchFiles':
        matches = tool_result.get('matches', [])
        return f"Found {len(matches)} matches"
    elif tool_name == 'web_search':
        results = tool_result.get('results', [])
        return f"Found {len(results)} web results"
    elif tool_name == 'Read':
        content = tool_result.get('content', '')
        return f"Read {len(content)} characters"
    
    return None

def save_research(entry):
    """Save research entry to log"""
    research_dir = Path('.claude/research')
    research_dir.mkdir(parents=True, exist_ok=True)
    
    # Daily research log
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = research_dir / f'{today}-research.jsonl'
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')

if __name__ == '__main__':
    main()
