#!/usr/bin/env python3
"""
Requirement Drift Detector Hook
Prevents any changes that would violate locked requirements
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

def hook(action: Dict[str, Any]) -> Dict[str, Any]:
    """Detect and prevent requirement drift before any edit."""
    
    # Only check file modifications
    if action['tool_name'] not in ['create_file', 'str_replace', 'write_file', 'edit_file']:
        return {"action": "allow"}
    
    # Load all locked requirements
    locked_requirements = load_locked_requirements()
    if not locked_requirements:
        return {"action": "allow"}
    
    # Get file path and content
    file_path = action['parameters'].get('path', '')
    content = get_content_from_action(action)
    
    # Check each locked requirement
    for component, reqs in locked_requirements.items():
        if should_check_component(component, file_path, content):
            violations = check_requirement_violations(component, reqs, content, file_path)
            
            if violations:
                return {
                    "action": "block",
                    "error": format_violation_error(violations),
                    "suggestion": generate_fix_suggestion(violations)
                }
    
    return {"action": "allow"}

def load_locked_requirements() -> Dict[str, Any]:
    """Load all locked requirements from .claude/requirements/locked/"""
    requirements = {}
    req_dir = Path('.claude/requirements/locked')
    
    if not req_dir.exists():
        return requirements
    
    for req_file in req_dir.glob('*.json'):
        try:
            with open(req_file, 'r') as f:
                data = json.load(f)
                requirements[data['component']] = data
        except Exception as e:
            print(f"Error loading {req_file}: {e}")
    
    return requirements

def should_check_component(component: str, file_path: str, content: str) -> bool:
    """Determine if this edit affects a locked component."""
    component_lower = component.lower()
    file_path_lower = file_path.lower()
    content_lower = content.lower()
    
    # Direct component file
    if component_lower in file_path_lower:
        return True
    
    # Component references in content
    if component in content or component_lower in content_lower:
        return True
    
    # Form-specific patterns
    if 'form' in component_lower and ('form' in file_path_lower or 'form' in content_lower):
        return True
    
    return False

def get_content_from_action(action: Dict[str, Any]) -> str:
    """Extract content from various action types."""
    params = action['parameters']
    
    if action['tool_name'] == 'create_file' or action['tool_name'] == 'write_file':
        return params.get('content', '')
    elif action['tool_name'] == 'str_replace':
        return params.get('new_str', '')
    elif action['tool_name'] == 'edit_file':
        # For edit_file, check the new content in edits
        edits = params.get('edits', [])
        return ' '.join([edit.get('newText', '') for edit in edits])
    
    return ''

def check_requirement_violations(component: str, requirements: Dict[str, Any], 
                               content: str, file_path: str) -> List[Dict[str, Any]]:
    """Check if content violates any locked requirements."""
    violations = []
    reqs = requirements.get('requirements', {})
    
    # Check field count requirements
    if 'fields' in reqs and is_form_component(file_path, content):
        field_violations = check_field_requirements(reqs['fields'], content)
        violations.extend(field_violations)
    
    # Check feature requirements
    if 'features' in reqs:
        feature_violations = check_feature_requirements(reqs['features'], content)
        violations.extend(feature_violations)
    
    # Check constraints
    if 'constraints' in reqs:
        constraint_violations = check_constraints(reqs['constraints'], content)
        violations.extend(constraint_violations)
    
    # Check constants (NEW)
    if 'constants' in reqs:
        constant_violations = check_constants(reqs['constants'], content)
        violations.extend(constant_violations)
    
    return violations

def is_form_component(file_path: str, content: str) -> bool:
    """Check if this is a form-related component."""
    form_indicators = [
        'form', 'input', 'field', 'textfield', 'textarea', 
        'select', 'checkbox', 'radio', 'useform', 'formdata'
    ]
    
    combined = (file_path + content).lower()
    return any(indicator in combined for indicator in form_indicators)

def check_field_requirements(field_reqs: Dict[str, Any], content: str) -> List[Dict[str, Any]]:
    """Check field count and name requirements."""
    violations = []
    
    # Extract field definitions from content
    field_patterns = [
        r'name=["\'](\w+)["\']',  # HTML name attributes
        r'id=["\'](\w+)["\']',     # HTML id attributes
        r'register\(["\'](\w+)["\']',  # React Hook Form
        r'field:\s*["\'](\w+)["\']',   # Object notation
        r'(\w+):\s*z\.string\(\)',     # Zod schema
        r'<Input[^>]*name=["\'](\w+)["\']',  # React components
    ]
    
    found_fields = set()
    for pattern in field_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        found_fields.update(matches)
    
    # Check field count
    expected_count = field_reqs.get('count', 0)
    if expected_count > 0 and len(found_fields) != expected_count:
        violations.append({
            'type': 'field_count',
            'expected': expected_count,
            'actual': len(found_fields),
            'severity': 'critical',
            'message': f"Field count mismatch: expected {expected_count}, found {len(found_fields)}"
        })
    
    # Check required field names
    required_fields = set(field_reqs.get('names', []))
    if required_fields:
        missing_fields = required_fields - found_fields
        if missing_fields:
            violations.append({
                'type': 'missing_fields',
                'expected': list(required_fields),
                'actual': list(found_fields),
                'missing': list(missing_fields),
                'severity': 'critical',
                'message': f"Missing required fields: {', '.join(missing_fields)}"
            })
    
    return violations

def check_feature_requirements(features: List[str], content: str) -> List[Dict[str, Any]]:
    """Check if required features are present."""
    violations = []
    content_lower = content.lower()
    
    for feature in features:
        feature_lower = feature.lower()
        # Simple check - could be enhanced with more sophisticated detection
        if feature_lower not in content_lower:
            violations.append({
                'type': 'missing_feature',
                'feature': feature,
                'severity': 'high',
                'message': f"Required feature not found: {feature}"
            })
    
    return violations

def check_constraints(constraints: List[str], content: str) -> List[Dict[str, Any]]:
    """Check if constraints are violated."""
    violations = []
    
    for constraint in constraints:
        # Parse constraint patterns like "no inline styles", "must use design system"
        if "no inline style" in constraint.lower() and 'style=' in content:
            violations.append({
                'type': 'constraint_violation',
                'constraint': constraint,
                'severity': 'medium',
                'message': f"Constraint violated: {constraint}"
            })
    
    return violations

def check_constants(constants: Dict[str, Any], content: str) -> List[Dict[str, Any]]:
    """Check if code violates locked constants."""
    violations = []
    
    # Check for hardcoded values that should use constants
    for const_name, const_value in constants.items():
        if isinstance(const_value, list):
            # Check for values not in approved list
            violations.extend(check_list_constants(const_name, const_value, content))
        elif isinstance(const_value, dict):
            # Check for dictionary constants (like colors)
            violations.extend(check_dict_constants(const_name, const_value, content))
        elif isinstance(const_value, str):
            # Check for string constants
            violations.extend(check_string_constants(const_name, const_value, content))
    
    return violations

def check_list_constants(name: str, allowed_values: List[Any], content: str) -> List[Dict[str, Any]]:
    """Check list constants like approved brands."""
    violations = []
    
    # Pattern matching for common list usage
    patterns = [
        rf'{name}\s*=\s*\[(.*?)\]',  # Direct assignment
        rf'["\']({"|".join(map(str, allowed_values))})["\']',  # String literals
    ]
    
    # Look for any string literal that might be a brand/value
    import ast
    try:
        # Try to parse as Python/JS to find string literals
        # This is a simplified check - real implementation would be more robust
        string_literals = re.findall(r'["\']([^"\'
]+)["\']', content)
        
        # Check if string looks like it could be a value from this category
        for literal in string_literals:
            if (name.lower() in ['brands', 'approvedbrands'] and 
                literal not in allowed_values and 
                len(literal) > 2 and literal[0].isupper()):
                violations.append({
                    'type': 'constant_violation',
                    'constant': name,
                    'found': literal,
                    'allowed': allowed_values,
                    'severity': 'critical',
                    'message': f"'{literal}' not in approved {name} list"
                })
    except:
        pass
    
    return violations

def check_dict_constants(name: str, const_dict: Dict[str, Any], content: str) -> List[Dict[str, Any]]:
    """Check dictionary constants like color palettes."""
    violations = []
    
    # Flatten nested color values
    color_values = []
    def extract_colors(d, prefix=''):
        for k, v in d.items():
            if isinstance(v, dict):
                extract_colors(v, f"{prefix}{k}.")
            elif isinstance(v, str) and v.startswith('#'):
                color_values.append(v)
    
    extract_colors(const_dict)
    
    # Look for hex colors not in palette
    hex_colors = re.findall(r'#[0-9A-Fa-f]{6}\b', content)
    for color in hex_colors:
        if color.upper() not in [c.upper() for c in color_values]:
            violations.append({
                'type': 'constant_violation',
                'constant': name,
                'found': color,
                'severity': 'high',
                'message': f"Color '{color}' not in approved palette"
            })
    
    return violations

def check_string_constants(name: str, value: str, content: str) -> List[Dict[str, Any]]:
    """Check string constants like API endpoints."""
    violations = []
    
    # Look for URLs that might be API endpoints
    if 'api' in name.lower() or 'endpoint' in name.lower():
        urls = re.findall(r'https?://[^\s"\']+', content)
        for url in urls:
            if value in url:  # Correct usage
                continue
            # Check if it looks like an API URL but different
            if 'api' in url and url != value:
                violations.append({
                    'type': 'constant_violation',
                    'constant': name,
                    'found': url,
                    'expected': value,
                    'severity': 'critical',
                    'message': f"Using '{url}' instead of approved '{value}'"
                })
    
    return violations

def format_violation_error(violations: List[Dict[str, Any]]) -> str:
    """Format violations into a clear error message."""
    lines = ["❌ REQUIREMENT VIOLATIONS DETECTED\n" + "="*40]
    
    for v in violations:
        if v['type'] == 'field_count':
            lines.append(f"\n⚠️  Field Count Violation:")
            lines.append(f"   Expected: {v['expected']} fields")
            lines.append(f"   Found: {v['actual']} fields")
            lines.append(f"   Difference: {v['actual'] - v['expected']}")
        elif v['type'] == 'missing_fields':
            lines.append(f"\n⚠️  Missing Required Fields:")
            for field in v['missing']:
                lines.append(f"   - {field}")
        elif v['type'] == 'missing_feature':
            lines.append(f"\n⚠️  Missing Feature: {v['feature']}")
        elif v['type'] == 'constraint_violation':
            lines.append(f"\n⚠️  Constraint Violated: {v['constraint']}")
        elif v['type'] == 'constant_violation':
            lines.append(f"\n⚠️  Constant Violation:")
            lines.append(f"   Constant: {v['constant']}")
            lines.append(f"   Found: '{v['found']}'")
            if 'expected' in v:
                lines.append(f"   Expected: '{v['expected']}'")
            if 'allowed' in v:
                lines.append(f"   Allowed: {', '.join(map(str, v['allowed'][:5]))}...")
            lines.append(f"   {v['message']}")
    
    lines.append("\n" + "="*40)
    lines.append("These requirements are LOCKED and cannot be changed.")
    
    return '\n'.join(lines)

def generate_fix_suggestion(violations: List[Dict[str, Any]]) -> str:
    """Generate suggestions to fix violations."""
    suggestions = []
    
    for v in violations:
        if v['type'] == 'field_count':
            if v['actual'] < v['expected']:
                suggestions.append(f"Add {v['expected'] - v['actual']} more fields")
            else:
                suggestions.append(f"Remove {v['actual'] - v['expected']} fields")
        elif v['type'] == 'missing_fields':
            suggestions.append(f"Add missing fields: {', '.join(v['missing'])}")
    
    if suggestions:
        return "To fix: " + "; ".join(suggestions)
    else:
        return "Review locked requirements and adjust implementation"

if __name__ == "__main__":
    # Test the hook
    test_action = {
        'tool_name': 'create_file',
        'parameters': {
            'path': 'components/forms/ContactForm.tsx',
            'content': 'const ContactForm = () => { /* only 7 fields */ }'
        }
    }
    
    result = hook(test_action)
    print(json.dumps(result, indent=2))
