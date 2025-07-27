#!/usr/bin/env python3
"""
Pattern Learning Hook - Learns from code patterns to improve suggestions
Tracks common patterns and anti-patterns for better assistance
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
import re

def extract_patterns(content, file_type):
    """Extract patterns from code content"""
    patterns = {
        'components': [],
        'imports': [],
        'hooks': [],
        'api_calls': [],
        'design_tokens': []
    }
    
    if file_type in ['.tsx', '.jsx']:
        # Extract component definitions
        component_matches = re.findall(r'(?:export\s+)?(?:const|function)\s+(\w+).*?(?:React\.FC|=>)', content)
        patterns['components'] = component_matches[:5]  # Limit to 5
        
        # Extract imports
        import_matches = re.findall(r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]", content)
        patterns['imports'] = [imp for imp in import_matches if not imp.startswith('.')][:10]
        
        # Extract hooks usage
        hook_matches = re.findall(r'\b(use[A-Z]\w+)\(', content)
        patterns['hooks'] = list(set(hook_matches))[:10]
        
        # Extract API calls
        api_matches = re.findall(r'(?:fetch|apiClient|api\.)\s*\([\'"`]([^\'"`]+)', content)
        patterns['api_calls'] = api_matches[:5]
        
        # Extract design tokens
        design_matches = re.findall(r'\b(text-size-\d|font-(?:regular|semibold)|rounded-\w+|bg-\w+-\d+)\b', content)
        patterns['design_tokens'] = list(set(design_matches))[:20]
    
    return patterns

def update_pattern_database(patterns, file_path):
    """Update the pattern database with new observations"""
    db_file = Path('.claude/analytics/pattern-database.json')
    db_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing database
    database = {}
    if db_file.exists():
        try:
            with open(db_file, 'r') as f:
                database = json.load(f)
        except:
            database = {}
    
    # Initialize if needed
    if 'patterns' not in database:
        database['patterns'] = {
            'components': {},
            'imports': {},
            'hooks': {},
            'api_calls': {},
            'design_tokens': {}
        }
    
    if 'statistics' not in database:
        database['statistics'] = {
            'total_files': 0,
            'last_updated': None
        }
    
    # Update patterns
    for category, items in patterns.items():
        for item in items:
            if item not in database['patterns'][category]:
                database['patterns'][category][item] = {
                    'count': 0,
                    'first_seen': datetime.now().isoformat(),
                    'last_seen': None,
                    'files': []
                }
            
            database['patterns'][category][item]['count'] += 1
            database['patterns'][category][item]['last_seen'] = datetime.now().isoformat()
            
            # Track files (limit to last 5)
            if file_path not in database['patterns'][category][item]['files']:
                database['patterns'][category][item]['files'].append(file_path)
                database['patterns'][category][item]['files'] = database['patterns'][category][item]['files'][-5:]
    
    # Update statistics
    database['statistics']['total_files'] += 1
    database['statistics']['last_updated'] = datetime.now().isoformat()
    
    # Save database
    with open(db_file, 'w') as f:
        json.dump(database, f, indent=2)
    
    return database

def generate_insights(database):
    """Generate insights from pattern database"""
    insights = []
    
    # Most used hooks
    if database['patterns']['hooks']:
        top_hooks = sorted(database['patterns']['hooks'].items(), 
                          key=lambda x: x[1]['count'], 
                          reverse=True)[:3]
        if top_hooks:
            hooks_list = ', '.join([h[0] for h in top_hooks])
            insights.append(f"Popular hooks: {hooks_list}")
    
    # Common imports
    if database['patterns']['imports']:
        top_imports = sorted(database['patterns']['imports'].items(), 
                           key=lambda x: x[1]['count'], 
                           reverse=True)[:3]
        if top_imports:
            imports_list = ', '.join([i[0].split('/')[-1] for i in top_imports])
            insights.append(f"Common imports: {imports_list}")
    
    # Design token usage
    if database['patterns']['design_tokens']:
        token_count = sum(item['count'] for item in database['patterns']['design_tokens'].values())
        insights.append(f"Design tokens used: {len(database['patterns']['design_tokens'])} unique")
    
    return insights

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        tool_result = input_data.get('tool_result', {})
        
        # Only process write operations on code files
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            sys.exit(0)
        
        # Get file info
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        if not file_path or not content:
            sys.exit(0)
        
        # Determine file type
        file_ext = Path(file_path).suffix
        
        # Only process code files
        if file_ext not in ['.tsx', '.jsx', '.ts', '.js']:
            sys.exit(0)
        
        # Extract patterns
        patterns = extract_patterns(content, file_ext)
        
        # Update database
        database = update_pattern_database(patterns, file_path)
        
        # Generate insights periodically
        if database['statistics']['total_files'] % 20 == 0:
            insights = generate_insights(database)
            if insights:
                message = "🧠 Pattern Learning Insights:\n"
                for insight in insights:
                    message += f"  • {insight}\n"
                
                # PostToolUse hooks output to stdout for transcript mode
                print(message)
        
        # Exit successfully
        sys.exit(0)
        
    except Exception as e:
        # Log error to stderr and exit
        print(f"Pattern learning error: {str(e)}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
