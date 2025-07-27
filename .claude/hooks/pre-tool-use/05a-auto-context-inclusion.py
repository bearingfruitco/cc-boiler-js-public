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

def extract_context_clues(file_path, content):
    """Extract clues about what context might be relevant"""
    clues = set()
    
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

def find_relevant_contexts(clues):
    """Find context files relevant to the clues"""
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
                    pass
                    
    return relevant

def build_context_comment(contexts):
    """Build a comment explaining the included context"""
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
            lines.append(f" *   Approved brands: {', '.join(brands[:3])}...")
            
        if 'tables' in ctx['content']:
            tables = list(ctx['content']['tables'].keys())
            lines.append(f" *   Database tables: {', '.join(tables[:3])}...")
            
        if 'colors' in ctx['content']:
            lines.append(f" *   Color palette defined - use only approved colors")
    
    lines.extend([
        " *",
        " * IMPORTANT: Any deviation from these requirements will be blocked.",
        " * Reference: .claude/requirements/locked/",
        " */"
    ])
    
    return '\n'.join(lines)

def main():
    """Main hook logic"""
    try:
        # Read input
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name
        tool_name = input_data.get('tool_name', '')
        if not tool_name and 'tool_use' in input_data:
            tool_name = input_data['tool_use'].get('name', '')
        
        # Only process write operations
        if tool_name not in ['Write', 'Edit', 'str_replace']:
            sys.exit(0)
        
        # Extract parameters
        tool_input = input_data.get('tool_input', {})
        if not tool_input and 'tool_use' in input_data:
            tool_input = input_data['tool_use'].get('parameters', {})
        
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        # Skip if working with PRP files (handled by 05b)
        if 'PRPs/' in file_path or any(marker in file_path for marker in ['prp', 'validation', 'blueprint']):
            sys.exit(0)
        
        # Extract context clues
        clues = extract_context_clues(file_path, content)
        if not clues:
            sys.exit(0)
        
        # Find relevant contexts
        relevant_contexts = find_relevant_contexts(clues)
        if not relevant_contexts:
            sys.exit(0)
        
        # Build context message
        context_comment = build_context_comment(relevant_contexts)
        
        # Show context awareness in stderr (informational)
        message = f"📚 AUTO-CONTEXT INCLUSION\n\n"
        message += f"Detected context clues: {', '.join(clues)}\n"
        message += f"Including {len(relevant_contexts)} context files:\n"
        for ctx in relevant_contexts:
            message += f"  • {ctx['name']}\n"
        message += f"\nThese locked requirements will be enforced."
        
        print(message, file=sys.stderr)
        
        # For now, just inform - don't modify content
        # In a full implementation, we could prepend the context comment
        sys.exit(0)
        
    except Exception as e:
        # On error, exit with non-zero code and error in stderr
        print(f"Auto context inclusion hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
