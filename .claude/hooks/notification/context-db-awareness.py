#!/usr/bin/env python3
"""
Context Database Awareness Hook
Automatically suggests relevant context files based on current work
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List

def hook(event: Dict[str, Any]) -> Dict[str, Any]:
    """Suggest relevant context files based on current activity."""
    
    # Get the current command or activity
    command = event.get('command', '')
    context = event.get('context', '')
    
    # Don't suggest if already working with context
    if 'context-db' in command or 'pin-requirements' in command:
        return {"notify": False}
    
    # Look for keywords that might need context
    keywords = extract_keywords(command + ' ' + context)
    if not keywords:
        return {"notify": False}
    
    # Search for relevant context files
    relevant_files = find_relevant_context(keywords)
    if not relevant_files:
        return {"notify": False}
    
    # Format suggestion
    return {
        "notify": True,
        "message": format_context_suggestion(relevant_files, keywords),
        "severity": "info",
        "suggested_commands": [
            f"/context-db load {file['name']}" for file in relevant_files[:3]
        ]
    }

def extract_keywords(text: str) -> List[str]:
    """Extract keywords that might need context."""
    keywords = []
    text_lower = text.lower()
    
    # Domain-specific keywords
    triggers = {
        'brand': ['brand', 'nike', 'adidas', 'puma'],
        'database': ['database', 'schema', 'table', 'field', 'column'],
        'api': ['api', 'endpoint', 'route', 'auth'],
        'color': ['color', 'palette', 'theme', 'design'],
        'product': ['product', 'catalog', 'sku', 'inventory'],
        'company': ['company', 'business', 'organization']
    }
    
    for category, words in triggers.items():
        if any(word in text_lower for word in words):
            keywords.append(category)
    
    return keywords

def find_relevant_context(keywords: List[str]) -> List[Dict[str, Any]]:
    """Find context files relevant to keywords."""
    relevant = []
    
    # Check locked requirements
    req_dir = Path('.claude/requirements/locked')
    if req_dir.exists():
        for file in req_dir.glob('*.json'):
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    content_lower = content.lower()
                    
                    # Check if file contains relevant keywords
                    relevance_score = sum(
                        1 for keyword in keywords 
                        if keyword in content_lower or keyword in file.name.lower()
                    )
                    
                    if relevance_score > 0:
                        # Get preview
                        data = json.loads(content)
                        preview = get_preview(data)
                        
                        relevant.append({
                            'name': file.stem,
                            'path': str(file),
                            'score': relevance_score,
                            'preview': preview,
                            'size': len(content)
                        })
            except:
                pass
    
    # Sort by relevance
    relevant.sort(key=lambda x: x['score'], reverse=True)
    return relevant[:5]  # Top 5 most relevant

def get_preview(data: Dict[str, Any]) -> str:
    """Get a preview of the context file."""
    if '_metadata' in data and 'description' in data['_metadata']:
        return data['_metadata']['description']
    
    # Try to summarize content
    if 'requirements' in data:
        reqs = data['requirements']
        if 'constants' in reqs:
            const_keys = list(reqs['constants'].keys())[:3]
            return f"Constants: {', '.join(const_keys)}"
        elif 'fields' in reqs:
            return f"Fields: {reqs['fields'].get('count', 'unknown')} defined"
    
    # Generic summary
    keys = list(data.keys())[:3]
    return f"Contains: {', '.join(keys)}"

def format_context_suggestion(files: List[Dict[str, Any]], keywords: List[str]) -> str:
    """Format context suggestion message."""
    lines = [
        "💡 RELEVANT CONTEXT FOUND",
        f"Keywords detected: {', '.join(keywords)}",
        "",
        "Available context files:"
    ]
    
    for file in files:
        lines.append(f"\n📄 {file['name']}")
        lines.append(f"   {file['preview']}")
        lines.append(f"   Size: {file['size']} bytes")
    
    lines.extend([
        "",
        "Load relevant context with:",
        f"  /context-db load {files[0]['name']}",
        "",
        "Or search for more:",
        f"  /context-db search {keywords[0]}"
    ])
    
    return '\n'.join(lines)

if __name__ == "__main__":
    # Test the hook
    test_event = {
        "command": "/cc BrandSelector",
        "context": "Creating a component to select Nike or Adidas products"
    }
    
    result = hook(test_event)
    if result.get("notify"):
        print(result["message"])
