#!/usr/bin/env python3
"""
Auto Context Inclusion Hook
Automatically includes relevant context files based on current work
NOTE: Works in conjunction with 05b-prp-context-loader.py for PRP-specific context
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, Any, List, Set

def hook(action: Dict[str, Any]) -> Dict[str, Any]:
    """Automatically include relevant context before file operations."""
    
    # Skip if working with PRP files (handled by 05b)
    file_path = action['parameters'].get('path', '')
    if 'PRPs/' in file_path or any(marker in file_path for marker in ['prp', 'validation', 'blueprint']):
        sys.exit(0)
    
    # Extract context clues
    clues = extract_context_clues(file_path, content)
    if not clues:
        sys.exit(0)
    if not relevant_contexts:
        sys.exit(0)
    
    return {
        sys.exit(0)
    
    # From file path
    path_lower = file_path.lower()
    
    # Component type clues
    if 'brand' in path_lower:
        clues.add('brand')
    if 'product' in path_lower:
        clues.add('product')
    if 'order' in path_lower:
        clues.add('order')
    if any(db_term in path_lower for db_term in ['model', 'schema', 'entity', 'repository']):
        clues.add('database')
    if any(api_term in path_lower for api_term in ['api', 'endpoint', 'route', 'controller']):
        clues.add('api')
    
    # Content analysis
    content_lower = content.lower()
    
    # Look for brand mentions
    brands = ['nike', 'adidas', 'puma', 'new balance', 'under armour']
    if any(brand in content_lower for brand in brands):
        clues.add('brand')
    
    # Look for database operations
    db_keywords = ['select', 'insert', 'update', 'delete', 'create table', 
                   'products', 'orders', 'customers', 'prisma', 'drizzle']
    if any(keyword in content_lower for keyword in db_keywords):
        clues.add('database')
    
    # Look for API patterns
    api_patterns = ['fetch(', 'axios', 'api/', '/api', 'endpoint', 'apikey', 'oauth']
    if any(pattern in content_lower for pattern in api_patterns):
        clues.add('api')
        
    # Look for color/design references
    if re.search(r'#[0-9a-fA-F]{6}', content) or 'color' in content_lower:
        clues.add('design')
    
    # Look for specific field names that match our schemas
    schema_fields = ['brand', 'sku', 'price', 'category', 'tier', 'minimumordervalue']
    if any(field in content_lower for field in schema_fields):
        clues.add('database')
        clues.add('brand')
    
    return clues

def find_relevant_contexts(clues: Set[str]) -> List[Dict[str, Any]]:
    """Find context files relevant to the clues."""
    relevant = []
    
    # Map clues to likely context files
    context_map = {
        'brand': ['BrandDatabase.json', 'BrandConfig.json', 'BrandGuidelines.json'],
        'database': ['DatabaseSchema.json', 'DataModel.json', 'Migrations.json'],
        'product': ['ProductCatalog.json', 'ProductSchema.json', 'BrandDatabase.json'],
        'api': ['APIEndpoints.json', 'APIConfig.json', 'BrandDatabase.json'],
        'design': ['ColorPalette.json', 'DesignSystem.json', 'BrandDatabase.json'],
        'order': ['DatabaseSchema.json', 'OrderFlow.json', 'BusinessRules.json']
    }
    
    # Collect all potentially relevant files
    potential_files = set()
    for clue in clues:
        if clue in context_map:
            potential_files.update(context_map[clue])
    
    # Check which files actually exist
    req_dir = Path('.claude/requirements/locked')
    if req_dir.exists():
        for filename in potential_files:
            file_path = req_dir / filename
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        content = json.load(f)
                        
                    relevant.append({
                        'name': filename,
                        'path': str(file_path),
                        'content': content,
                        'description': content.get('_metadata', {}).get('description', ''),
                        'clues': list(clues)
                    })
                except:
                        return relevant

def inject_context_awareness(action: Dict[str, Any], contexts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Inject context awareness into the action."""
    
    # Build context injection comment
    context_comment = build_context_comment(contexts)
    
    # Modify the action to include context
    if action['tool_name'] in ['create_file', 'Write']:
        # Prepend context comment to file content
        original_content = action['parameters'].get('content', '')
        action['parameters']['content'] = context_comment + '\n\n' + original_content
        
    elif action['tool_name'] == 'str_replace':
        # Add context awareness to replacements
        action['parameters']['context_files'] = [c['name'] for c in contexts]
        
    # Add metadata about included context
    action['included_context'] = {
        'files': [c['name'] for c in contexts],
        'auto_included': True,
        'reason': 'Automatic context detection'
    }
    
    return action

def build_context_comment(contexts: List[Dict[str, Any]]) -> str:
    """Build a comment explaining the included context."""
    
    lines = [
        "/**",
        " * AUTO-INCLUDED CONTEXT FILES:",
        " * These files contain locked requirements and must be followed:"
    ]
    
    for ctx in contexts:
        lines.append(f" * - {ctx['name']}: {ctx['description']}")
        
        # Add specific constraints from the context
        if 'brands' in ctx['content']:
            brands = list(ctx['content']['brands'].keys())
            lines.append(f" *   Approved brands: {', '.join(brands)}")
            
        if 'tables' in ctx['content']:
            tables = list(ctx['content']['tables'].keys())
            lines.append(f" *   Database tables: {', '.join(tables)}")
            
        if 'colors' in ctx['content']:
            lines.append(f" *   Color palette defined - use only approved colors")
    
    lines.extend([
        " *",
        " * IMPORTANT: Any deviation from these requirements will be blocked.",
        " * Reference: .claude/requirements/locked/",
        " */"
    ])
    
    return '\n'.join(lines)

def get_content_from_action(action: Dict[str, Any]) -> str:
    """Extract content from various action types."""
    params = action['parameters']
    
    if action['tool_name'] in ['create_file', 'Write']:
        return params.get('content', '')
    elif action['tool_name'] == 'str_replace':
        return params.get('new_str', '')
    elif action['tool_name'] == 'Edit':
        edits = params.get('edits', [])
        return ' '.join([edit.get('newText', '') for edit in edits])
    
    return ''

# Additional helper for active issue context
def get_active_issue_context() -> Dict[str, Any]:
    """Get context from currently active GitHub issue."""
    try:
        workflow_file = Path('.claude/context/active-workflow.json')
        if workflow_file.exists():
            with open(workflow_file, 'r') as f:
                workflow = json.load(f)
                
            if 'issue' in workflow:
                # Look for issue-specific requirements
                issue_num = workflow['issue']
                issue_req_file = Path(f'.claude/requirements/locked/Issue_{issue_num}.json')
                
                if issue_req_file.exists():
                    with open(issue_req_file, 'r') as f:
                        return json.load(f)
    except:
    
 Test the hook
    test_action = {
        'tool_name': 'create_file',
        'parameters': {
            'path': 'components/BrandSelector.tsx',
            'content': 'const BrandSelector = () => { const brands = ["Nike", "Reebok"]; }'
        }
    }
    
    result = hook(test_action)
    print(json.dumps(result, indent=2))
