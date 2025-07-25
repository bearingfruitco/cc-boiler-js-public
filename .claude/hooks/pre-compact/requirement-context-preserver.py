#!/usr/bin/env python3
"""
Requirement Context Preserver
Ensures locked requirements and anchors survive conversation compaction
"""

import json
from pathlib import Path
from typing import Dict, Any, List

def hook() -> Dict[str, Any]:
    """Preserve requirement context during conversation compaction."""
    
    # Load all critical context
    locked_requirements = load_all_locked_requirements()
    context_anchors = load_context_anchors()
    active_issues = load_active_issues()
    
    # Build preservation package
    preservation_context = {
        "locked_requirements": locked_requirements,
        "context_anchors": context_anchors,
        "active_issues": active_issues,
        "critical_facts": build_critical_facts(locked_requirements)
    }
    
    # Format for inclusion
    formatted_context = format_preservation_context(preservation_context)
    
    return {
        "additional_context": formatted_context,
        "priority": "critical",
        "position": "start"  # Ensure this appears at the beginning
    }

def load_all_locked_requirements() -> Dict[str, Any]:
    """Load all locked requirements."""
    requirements = {}
    req_dir = Path('.claude/requirements/locked')
    
    if req_dir.exists():
        for req_file in req_dir.glob('*.json'):
            try:
                with open(req_file, 'r') as f:
                    data = json.load(f)
                    requirements[data['component']] = data
            except Exception as e:
                print(f"Error loading {req_file}: {e}")
    
    return requirements

def load_context_anchors() -> List[Dict[str, Any]]:
    """Load all context anchors."""
    anchors = []
    anchor_dir = Path('.claude/context/anchors')
    
    if anchor_dir.exists():
        for anchor_file in anchor_dir.glob('*.json'):
            try:
                with open(anchor_file, 'r') as f:
                    anchors.append(json.load(f))
            except Exception as e:
                print(f"Error loading {anchor_file}: {e}")
    
    # Sort by priority
    priority_order = {'critical': 0, 'high': 1, 'normal': 2}
    anchors.sort(key=lambda x: priority_order.get(x.get('priority', 'normal'), 2))
    
    return anchors

def load_active_issues() -> List[str]:
    """Load currently active GitHub issues."""
    active_issues = []
    
    # Check for active feature workflow
    fw_file = Path('.claude/context/active-workflow.json')
    if fw_file.exists():
        try:
            with open(fw_file, 'r') as f:
                workflow = json.load(f)
                if 'issue' in workflow:
                    active_issues.append(f"Issue #{workflow['issue']}")
        except:
            pass
    
    return active_issues

def build_critical_facts(requirements: Dict[str, Any]) -> List[str]:
    """Build list of critical facts from requirements."""
    facts = []
    
    for component, req_data in requirements.items():
        reqs = req_data.get('requirements', {})
        source = req_data.get('source', {})
        
        # Add field count facts
        if 'fields' in reqs and 'count' in reqs['fields']:
            count = reqs['fields']['count']
            ref = source.get('reference', 'Unknown')
            facts.append(f"{component} must have exactly {count} fields (Issue #{ref})")
        
        # Add required features
        if 'features' in reqs:
            for feature in reqs['features']:
                facts.append(f"{component} must include: {feature}")
    
    return facts

def format_preservation_context(context: Dict[str, Any]) -> str:
    """Format context for preservation."""
    lines = [
        "===== PRESERVED REQUIREMENT CONTEXT =====",
        "This context is CRITICAL and must be maintained:",
        ""
    ]
    
    # Add locked requirements summary
    if context['locked_requirements']:
        lines.append("🔒 LOCKED REQUIREMENTS:")
        for component, req_data in context['locked_requirements'].items():
            source = req_data.get('source', {})
            reqs = req_data.get('requirements', {})
            lines.append(f"\n{component} (Issue #{source.get('reference', 'Unknown')}):")
            
            if 'fields' in reqs:
                lines.append(f"  - Must have {reqs['fields']['count']} fields")
                if 'names' in reqs['fields']:
                    lines.append(f"  - Fields: {', '.join(reqs['fields']['names'][:5])}...")
            
            if 'features' in reqs:
                lines.append(f"  - Required features: {len(reqs['features'])}")
        lines.append("")
    
    # Add context anchors
    if context['context_anchors']:
        lines.append("📌 IMMUTABLE CONTEXT ANCHORS:")
        for anchor in context['context_anchors']:
            if anchor.get('priority') == 'critical':
                lines.append(f"  🔴 {anchor['text']}")
            elif anchor.get('priority') == 'high':
                lines.append(f"  🟡 {anchor['text']}")
            else:
                lines.append(f"  ⚪ {anchor['text']}")
        lines.append("")
    
    # Add critical facts
    if context['critical_facts']:
        lines.append("⚠️  CRITICAL FACTS:")
        for fact in context['critical_facts']:
            lines.append(f"  - {fact}")
        lines.append("")
    
    # Add active issues
    if context['active_issues']:
        lines.append("📋 ACTIVE ISSUES:")
        for issue in context['active_issues']:
            lines.append(f"  - {issue}")
        lines.append("")
    
    lines.append("===== END PRESERVED CONTEXT =====")
    
    return '\n'.join(lines)

if __name__ == "__main__":
    # Test the hook
    result = hook()
    print(result['additional_context'])
