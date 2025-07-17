#!/usr/bin/env python3
"""
Continuous Requirement Validator
Runs validation checks every N commands to detect drift early
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import subprocess

def hook(event: Dict[str, Any]) -> Dict[str, Any]:
    """Run requirement validation periodically."""
    
    # Check if we should run validation
    command_count = event.get('command_count', 0)
    validation_frequency = get_validation_frequency()
    
    if command_count % validation_frequency != 0:
        return {"notify": False}
    
    # Run validation checks
    validation_results = run_requirement_validation()
    
    if not validation_results['violations']:
        return {"notify": False}
    
    # Format notification
    return {
        "notify": True,
        "message": format_violation_notification(validation_results),
        "severity": "warning",
        "action_required": True,
        "suggested_commands": get_suggested_fixes(validation_results)
    }

def get_validation_frequency() -> int:
    """Get validation frequency from config."""
    config_file = Path('.claude/config.json')
    
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config.get('requirement_enforcement', {}).get('validation_frequency', 10)
        except:
            pass
    
    return 10  # Default to every 10 commands

def run_requirement_validation() -> Dict[str, Any]:
    """Run comprehensive requirement validation."""
    violations = []
    
    # Get all locked requirements
    req_dir = Path('.claude/requirements/locked')
    if not req_dir.exists():
        return {"violations": []}
    
    for req_file in req_dir.glob('*.json'):
        try:
            with open(req_file, 'r') as f:
                requirement = json.load(f)
                component_violations = validate_component(requirement)
                violations.extend(component_violations)
        except Exception as e:
            print(f"Error validating {req_file}: {e}")
    
    return {
        "violations": violations,
        "total_components": len(list(req_dir.glob('*.json'))),
        "failed_components": len(set(v['component'] for v in violations))
    }

def validate_component(requirement: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Validate a single component against its requirements."""
    violations = []
    component = requirement['component']
    reqs = requirement.get('requirements', {})
    
    # Find component files
    component_files = find_component_files(component)
    if not component_files:
        violations.append({
            'component': component,
            'type': 'missing_component',
            'message': f"Component {component} not found",
            'severity': 'critical'
        })
        return violations
    
    # Read component content
    content = ""
    for file_path in component_files:
        try:
            with open(file_path, 'r') as f:
                content += f.read() + "\n"
        except:
            pass
    
    # Validate fields
    if 'fields' in reqs:
        field_violations = validate_fields(component, reqs['fields'], content)
        violations.extend(field_violations)
    
    # Validate features
    if 'features' in reqs:
        feature_violations = validate_features(component, reqs['features'], content)
        violations.extend(feature_violations)
    
    # Run tests if they exist
    test_violations = validate_tests(component)
    violations.extend(test_violations)
    
    return violations

def find_component_files(component: str) -> List[Path]:
    """Find all files related to a component."""
    files = []
    search_dirs = [
        Path('components'),
        Path('app'),
        Path('src/components'),
        Path('pages')
    ]
    
    for search_dir in search_dirs:
        if search_dir.exists():
            # Look for exact matches and partial matches
            patterns = [
                f"**/{component}.tsx",
                f"**/{component}.ts",
                f"**/{component}.jsx",
                f"**/{component}.js",
                f"**/{component}/*.tsx",
                f"**/{component}/*.ts"
            ]
            
            for pattern in patterns:
                files.extend(search_dir.glob(pattern))
    
    return files

def validate_fields(component: str, field_reqs: Dict[str, Any], 
                   content: str) -> List[Dict[str, Any]]:
    """Validate field requirements."""
    import re
    violations = []
    
    # Count fields in content
    field_patterns = [
        r'name=["\'](\w+)["\']',
        r'register\(["\'](\w+)["\']',
        r'(\w+):\s*z\.string\(\)',
        r'<Input[^>]*name=["\'](\w+)["\']'
    ]
    
    found_fields = set()
    for pattern in field_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        found_fields.update(matches)
    
    expected_count = field_reqs.get('count', 0)
    if expected_count > 0 and len(found_fields) != expected_count:
        violations.append({
            'component': component,
            'type': 'field_count_mismatch',
            'expected': expected_count,
            'actual': len(found_fields),
            'message': f"{component}: Expected {expected_count} fields, found {len(found_fields)}",
            'severity': 'critical'
        })
    
    # Check required fields
    required_fields = set(field_reqs.get('names', []))
    if required_fields:
        missing = required_fields - found_fields
        if missing:
            violations.append({
                'component': component,
                'type': 'missing_required_fields',
                'missing': list(missing),
                'message': f"{component}: Missing fields: {', '.join(missing)}",
                'severity': 'critical'
            })
    
    return violations

def validate_features(component: str, features: List[str], 
                     content: str) -> List[Dict[str, Any]]:
    """Validate required features are present."""
    violations = []
    content_lower = content.lower()
    
    for feature in features:
        if feature.lower() not in content_lower:
            violations.append({
                'component': component,
                'type': 'missing_feature',
                'feature': feature,
                'message': f"{component}: Missing feature '{feature}'",
                'severity': 'high'
            })
    
    return violations

def validate_tests(component: str) -> List[Dict[str, Any]]:
    """Check if requirement tests exist and pass."""
    violations = []
    
    # Look for requirement test file
    test_patterns = [
        f"**/{component}.requirements.test.*",
        f"**/{component}.test.*",
        f"**/test/{component}.*"
    ]
    
    test_files = []
    for pattern in test_patterns:
        test_files.extend(Path('.').glob(pattern))
    
    if not test_files:
        violations.append({
            'component': component,
            'type': 'missing_tests',
            'message': f"{component}: No requirement tests found",
            'severity': 'medium'
        })
    
    return violations

def format_violation_notification(results: Dict[str, Any]) -> str:
    """Format violations into a notification message."""
    violations = results['violations']
    
    if not violations:
        return ""
    
    lines = [
        "⚠️  REQUIREMENT DRIFT DETECTED",
        "=" * 40,
        f"Components checked: {results['total_components']}",
        f"Components with violations: {results['failed_components']}",
        "",
        "VIOLATIONS:"
    ]
    
    # Group by component
    by_component = {}
    for v in violations:
        component = v['component']
        if component not in by_component:
            by_component[component] = []
        by_component[component].append(v)
    
    for component, component_violations in by_component.items():
        lines.append(f"\n{component}:")
        for v in component_violations:
            if v['type'] == 'field_count_mismatch':
                lines.append(f"  ❌ Field count: expected {v['expected']}, found {v['actual']}")
            elif v['type'] == 'missing_required_fields':
                lines.append(f"  ❌ Missing fields: {', '.join(v['missing'])}")
            elif v['type'] == 'missing_feature':
                lines.append(f"  ❌ Missing feature: {v['feature']}")
            elif v['type'] == 'missing_tests':
                lines.append(f"  ⚠️  No requirement tests")
    
    lines.append("\n" + "=" * 40)
    lines.append("Run /review-requirements to see full report")
    
    return '\n'.join(lines)

def get_suggested_fixes(results: Dict[str, Any]) -> List[str]:
    """Suggest commands to fix violations."""
    suggestions = ["/review-requirements --all"]
    
    # Get unique components with violations
    components = list(set(v['component'] for v in results['violations']))
    
    for component in components[:3]:  # Limit to first 3
        suggestions.append(f"/review-requirements {component}")
    
    return suggestions

if __name__ == "__main__":
    # Test the hook
    test_event = {"command_count": 10}
    result = hook(test_event)
    if result.get("notify"):
        print(result["message"])
