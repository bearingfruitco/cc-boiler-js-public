#!/usr/bin/env python3
"""
Pattern Learning Hook - Learn from successful code patterns
Builds a library of working solutions over time
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime
import hashlib

def extract_patterns(content, file_path):
    """Extract reusable patterns from code"""
    patterns = []
    
    # Extract React hooks usage
    if file_path.endswith(('.tsx', '.jsx')):
        # Custom hooks
        custom_hooks = re.findall(r'const.*=\s*use[A-Z]\w+\([^)]*\)', content)
        for hook in custom_hooks:
            patterns.append({
                'type': 'custom-hook',
                'pattern': hook,
                'category': 'react'
            })
        
        # Component patterns
        if 'export function' in content or 'export const' in content:
            # Extract component structure
            component_match = re.search(
                r'export\s+(?:function|const)\s+(\w+).*?{(.*?)}(?:\s*$|\s*export)',
                content,
                re.DOTALL
            )
            if component_match:
                name = component_match.group(1)
                body = component_match.group(2)
                
                # Identify pattern type
                pattern_type = identify_component_pattern(body)
                if pattern_type:
                    patterns.append({
                        'type': 'component-pattern',
                        'pattern': pattern_type,
                        'name': name,
                        'category': 'react'
                    })
    
    # Extract API patterns
    if '/api/' in file_path:
        # Request handling patterns
        if 'Request' in content and 'Response' in content:
            has_validation = 'zod' in content or '.parse(' in content
            has_error_handling = 'try' in content and 'catch' in content
            
            api_pattern = {
                'type': 'api-pattern',
                'features': [],
                'category': 'api'
            }
            
            if has_validation:
                api_pattern['features'].append('validation')
            if has_error_handling:
                api_pattern['features'].append('error-handling')
            
            if api_pattern['features']:
                patterns.append(api_pattern)
    
    # Extract utility functions
    util_functions = re.findall(
        r'export\s+(?:async\s+)?function\s+(\w+)\s*\([^)]*\)\s*{',
        content
    )
    for func in util_functions:
        if func.startswith('use'):
            continue  # Skip hooks
        
        patterns.append({
            'type': 'utility-function',
            'name': func,
            'category': 'utility'
        })
    
    return patterns

def identify_component_pattern(component_body):
    """Identify common component patterns"""
    patterns = []
    
    if 'useState' in component_body:
        patterns.append('stateful')
    if 'useEffect' in component_body:
        patterns.append('side-effects')
    if 'onSubmit' in component_body or 'handleSubmit' in component_body:
        patterns.append('form')
    if 'map(' in component_body:
        patterns.append('list-render')
    if 'loading' in component_body:
        patterns.append('loading-state')
    if 'error' in component_body:
        patterns.append('error-handling')
    
    return '-'.join(patterns) if patterns else None

def load_pattern_library():
    """Load existing pattern library"""
    library_path = Path(__file__).parent.parent.parent / 'team' / 'pattern-library.json'
    
    if library_path.exists():
        with open(library_path) as f:
            return json.load(f)
    
    return {
        'patterns': {},
        'success_count': {},
        'last_updated': None
    }

def save_pattern_library(library):
    """Save pattern library"""
    library_path = Path(__file__).parent.parent.parent / 'team' / 'pattern-library.json'
    library['last_updated'] = datetime.now().isoformat()
    
    with open(library_path, 'w') as f:
        json.dump(library, f, indent=2)

def update_pattern_success(patterns, library):
    """Update success count for patterns"""
    for pattern in patterns:
        # Create pattern key
        pattern_key = f"{pattern['type']}:{pattern.get('pattern', pattern.get('name', 'unknown'))}"
        
        # Initialize if new
        if pattern_key not in library['patterns']:
            library['patterns'][pattern_key] = {
                'first_seen': datetime.now().isoformat(),
                'details': pattern,
                'usage_count': 0
            }
        
        # Increment usage
        library['patterns'][pattern_key]['usage_count'] += 1
        library['patterns'][pattern_key]['last_used'] = datetime.now().isoformat()

def get_similar_patterns(current_patterns, library):
    """Find similar successful patterns"""
    suggestions = []
    
    for pattern in current_patterns:
        pattern_type = pattern['type']
        
        # Find successful patterns of same type
        for key, data in library['patterns'].items():
            if data['details']['type'] == pattern_type and data['usage_count'] > 3:
                suggestions.append({
                    'pattern': data['details'],
                    'usage_count': data['usage_count'],
                    'relevance': 'high' if data['usage_count'] > 10 else 'medium'
                })
    
    return suggestions[:3]  # Top 3 suggestions

def generate_pattern_insights(library):
    """Generate insights from pattern library"""
    insights = []
    
    # Most used patterns
    sorted_patterns = sorted(
        library['patterns'].items(),
        key=lambda x: x[1]['usage_count'],
        reverse=True
    )
    
    if sorted_patterns:
        top_pattern = sorted_patterns[0]
        insights.append(
            f"Most used pattern: {top_pattern[0]} "
            f"({top_pattern[1]['usage_count']} times)"
        )
    
    # Recent trends
    recent_patterns = [
        p for p in library['patterns'].values()
        if p.get('last_used', '').startswith(datetime.now().strftime('%Y-%m-%d'))
    ]
    
    if recent_patterns:
        insights.append(f"Patterns used today: {len(recent_patterns)}")
    
    return insights

def main():
    """Main hook logic"""
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Only process on successful writes
    if input_data.get('tool') not in ['write_file', 'edit_file']:
        print(json.dumps({"action": "continue"}))
        return
    
    file_path = input_data.get('path', '')
    content = input_data.get('content', '')
    
    # Skip non-code files
    if not any(file_path.endswith(ext) for ext in ['.ts', '.tsx', '.js', '.jsx']):
        print(json.dumps({"action": "continue"}))
        return
    
    # Extract patterns
    patterns = extract_patterns(content, file_path)
    
    if patterns:
        # Load library
        library = load_pattern_library()
        
        # Update success metrics
        update_pattern_success(patterns, library)
        
        # Find similar successful patterns
        suggestions = get_similar_patterns(patterns, library)
        
        # Save updated library
        save_pattern_library(library)
        
        # Generate insights
        insights = generate_pattern_insights(library)
        
        # Log pattern learning
        response = {
            "action": "log",
            "message": f"📚 Learned {len(patterns)} patterns from {Path(file_path).name}",
            "patterns_learned": len(patterns),
            "total_patterns": len(library['patterns'])
        }
        
        if insights:
            response["insights"] = insights
        
        if suggestions:
            response["similar_patterns"] = f"Found {len(suggestions)} similar successful patterns"
        
        print(json.dumps(response))
    else:
        print(json.dumps({"action": "continue"}))

if __name__ == "__main__":
    main()
