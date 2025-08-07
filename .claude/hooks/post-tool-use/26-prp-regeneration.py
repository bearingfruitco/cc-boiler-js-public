#!/usr/bin/env python3
"""
PRP Regeneration Hook - Ensures PRPs use all available documentation
Monitors PRP generation and suggests missing context
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

def check_documentation_sources():
    """Check what documentation sources are available"""
    sources = {
        'prd': False,
        'agent_os': False,
        'architecture': False,
        'roadmap': False,
        'improvements': False,
        'tech_stack': False
    }
    
    # Check for PRD
    if Path('docs/project/PROJECT_PRD.md').exists():
        sources['prd'] = True
    
    # Check for agent-os analysis
    if Path('.agent-os').exists():
        if Path('.agent-os/product/roadmap.md').exists():
            sources['roadmap'] = True
        if Path('.agent-os/product/tech-stack.md').exists():
            sources['tech_stack'] = True
        sources['agent_os'] = True
    
    # Check for architecture docs
    if Path('docs/architecture').exists():
        arch_files = list(Path('docs/architecture').glob('*.md'))
        if arch_files:
            sources['architecture'] = True
    
    # Check for improvements doc
    improvement_files = list(Path('.').glob('*IMPROVEMENTS.md'))
    if improvement_files:
        sources['improvements'] = True
    
    return sources

def analyze_prp_generation_context(response):
    """Check if PRP generation used all available docs"""
    missing_context = []
    sources = check_documentation_sources()
    
    # Check if response references key documentation
    response_lower = response.lower() if response else ""
    
    if sources['roadmap'] and 'roadmap' not in response_lower and 'phase' not in response_lower:
        missing_context.append({
            'source': '.agent-os/product/roadmap.md',
            'reason': 'Contains phased development plan (Phase 1-4)',
            'impact': 'PRPs may not align with planned phases'
        })
    
    if sources['architecture'] and 'architecture' not in response_lower:
        missing_context.append({
            'source': 'docs/architecture/',
            'reason': 'Contains architectural analysis and debt',
            'impact': 'PRPs may miss critical refactoring needs'
        })
    
    if sources['improvements'] and 'improvement' not in response_lower and 'p0' not in response_lower:
        missing_context.append({
            'source': '*IMPROVEMENTS.md',
            'reason': 'Contains prioritized improvement list',
            'impact': 'PRPs may not address P0 critical issues'
        })
    
    if sources['tech_stack'] and 'tech' not in response_lower and 'stack' not in response_lower:
        missing_context.append({
            'source': '.agent-os/product/tech-stack.md',
            'reason': 'Contains technology decisions and constraints',
            'impact': 'PRPs may suggest incompatible solutions'
        })
    
    return missing_context

def suggest_prp_improvements(missing_context):
    """Generate suggestions for better PRP generation"""
    if not missing_context:
        return None
    
    suggestions = []
    suggestions.append("\n🔍 **PRP Generation Enhancement Suggested**\n")
    suggestions.append("The following documentation should be incorporated:\n")
    
    for context in missing_context:
        suggestions.append(f"\n📄 **{context['source']}**")
        suggestions.append(f"   Why: {context['reason']}")
        suggestions.append(f"   Impact: {context['impact']}")
    
    suggestions.append("\n💡 **Recommended Action:**")
    suggestions.append("Re-run with explicit context:")
    suggestions.append("```")
    suggestions.append("/prd-to-prp")
    suggestions.append("")
    suggestions.append("Please incorporate:")
    
    for context in missing_context:
        suggestions.append(f"- {context['source']}")
    
    suggestions.append("```")
    
    return "\n".join(suggestions)

def check_for_architectural_debt():
    """Look for known architectural issues that should be addressed"""
    debt_items = []
    
    # Check for monolithic components
    large_files = []
    for ext in ['*.tsx', '*.ts', '*.jsx', '*.js']:
        for file_path in Path('src').rglob(ext):
            if file_path.is_file():
                lines = len(file_path.read_text().splitlines())
                if lines > 1000:
                    large_files.append({
                        'file': str(file_path),
                        'lines': lines
                    })
    
    if large_files:
        debt_items.append({
            'type': 'Monolithic Components',
            'items': large_files,
            'prp_needed': 'refactor-monolith-prp.md'
        })
    
    # Check for test coverage
    if not Path('src').rglob('*.test.*') and not Path('src').rglob('*.spec.*'):
        debt_items.append({
            'type': 'Missing Tests',
            'items': ['No test files found'],
            'prp_needed': 'test-infrastructure-prp.md'
        })
    
    return debt_items

def main(response=None):
    """Main hook execution"""
    # Only run for PRP-related commands
    if response and any(cmd in response for cmd in ['/prd-to-prp', '/prp create', '/prp-generate']):
        # Check if all documentation was used
        missing = analyze_prp_generation_context(response)
        
        if missing:
            suggestion = suggest_prp_improvements(missing)
            if suggestion:
                print(suggestion)
        
        # Check for architectural debt
        debt = check_for_architectural_debt()
        if debt:
            print("\n⚠️ **Architectural Debt Detected**")
            for item in debt:
                print(f"\n{item['type']}:")
                if isinstance(item['items'], list):
                    for file_item in item['items'][:3]:  # Show top 3
                        if isinstance(file_item, dict):
                            print(f"  - {file_item['file']}: {file_item['lines']} lines")
                        else:
                            print(f"  - {file_item}")
                print(f"  → Suggested PRP: {item['prp_needed']}")
        
        # Log PRP generation event
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'command': 'prd-to-prp',
            'documentation_available': check_documentation_sources(),
            'missing_context': len(missing) if missing else 0,
            'debt_found': len(debt) if debt else 0
        }
        
        log_file = Path('.claude/logs/prp-generation.jsonl')
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        # If significant issues found, suggest comprehensive review
        if (missing and len(missing) > 2) or (debt and len(debt) > 1):
            print("\n🎯 **Comprehensive PRP Strategy Recommended**")
            print("Multiple issues detected. Consider running:")
            print("```")
            print("/analyze-existing full  # Update analysis")
            print("/architecture           # Update architecture docs")
            print("/prd-from-existing      # Regenerate PRD")
            print("/prd-to-prp            # Generate comprehensive PRPs")
            print("```")

if __name__ == "__main__":
    # For testing or when called directly
    import sys
    response = sys.stdin.read() if not sys.stdin.isatty() else None
    main(response)
