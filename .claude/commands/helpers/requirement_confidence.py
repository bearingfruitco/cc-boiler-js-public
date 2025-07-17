#!/usr/bin/env python3
"""
Requirement-aware confidence scoring helper
Used by generate-prd and grade commands
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple

def assess_requirement_confidence(component_name: str, 
                                proposed_implementation: str) -> Dict[str, Any]:
    """Assess confidence with requirement awareness."""
    
    # Load locked requirements
    locked_reqs = load_locked_requirements(component_name)
    
    if not locked_reqs:
        return standard_confidence_assessment(proposed_implementation)
    
    # Initialize scores
    scores = {
        "requirement_clarity": 0,
        "implementation_match": 0,
        "deviation_risk": 0,
        "completeness": 0,
        "complexity": 0
    }
    
    warnings = []
    
    # Check field requirements
    if 'fields' in locked_reqs.get('requirements', {}):
        field_score, field_warnings = check_field_alignment(
            locked_reqs['requirements']['fields'],
            proposed_implementation
        )
        scores['implementation_match'] = field_score
        if field_score < 8:
            scores['deviation_risk'] = 10 - field_score
        warnings.extend(field_warnings)
    
    # Check feature requirements
    if 'features' in locked_reqs.get('requirements', {}):
        feature_score, feature_warnings = check_feature_alignment(
            locked_reqs['requirements']['features'],
            proposed_implementation
        )
        scores['completeness'] = feature_score
        warnings.extend(feature_warnings)
    
    # Check requirement clarity
    scores['requirement_clarity'] = assess_requirement_clarity(locked_reqs)
    
    # Calculate overall score
    overall = calculate_weighted_score(scores)
    
    return {
        "score": overall,
        "breakdown": scores,
        "warnings": warnings,
        "recommendation": get_recommendation(overall, warnings),
        "source_requirements": locked_reqs.get('source', {})
    }

def load_locked_requirements(component_name: str) -> Dict[str, Any]:
    """Load locked requirements for a component."""
    req_file = Path(f'.claude/requirements/locked/{component_name}.json')
    
    if req_file.exists():
        try:
            with open(req_file, 'r') as f:
                return json.load(f)
        except:
            pass
    
    return {}

def standard_confidence_assessment(implementation: str) -> Dict[str, Any]:
    """Standard assessment when no locked requirements exist."""
    # Simplified assessment based on implementation complexity
    lines = implementation.split('\n')
    complexity = len(lines) / 100  # Rough complexity measure
    
    return {
        "score": max(3, min(9, 10 - complexity)),
        "breakdown": {
            "requirement_clarity": 5,
            "implementation_match": 5,
            "deviation_risk": 5,
            "completeness": 5,
            "complexity": 5
        },
        "warnings": ["No locked requirements found - using standard assessment"],
        "recommendation": "Consider pinning requirements with /pin-requirements"
    }

def check_field_alignment(field_reqs: Dict[str, Any], 
                         implementation: str) -> Tuple[int, List[str]]:
    """Check if implementation aligns with field requirements."""
    warnings = []
    score = 10
    
    # Extract proposed fields from implementation
    field_patterns = [
        r'fields?:\s*\[(.*?)\]',
        r'(\w+)Field',
        r'name=["\'](\w+)["\']',
        r'register\(["\'](\w+)["\']'
    ]
    
    proposed_fields = set()
    for pattern in field_patterns:
        matches = re.findall(pattern, implementation, re.IGNORECASE | re.DOTALL)
        for match in matches:
            if isinstance(match, str):
                # Clean up field names
                fields = match.replace('"', '').replace("'", '').split(',')
                proposed_fields.update(f.strip() for f in fields if f.strip())
    
    # Check field count
    expected_count = field_reqs.get('count', 0)
    if expected_count > 0:
        if len(proposed_fields) != expected_count:
            diff = len(proposed_fields) - expected_count
            score -= min(5, abs(diff))
            warnings.append(
                f"Field count mismatch: planning {len(proposed_fields)} "
                f"but requirement specifies {expected_count}"
            )
    
    # Check required fields
    required_fields = set(field_reqs.get('names', []))
    if required_fields:
        missing = required_fields - proposed_fields
        if missing:
            score -= min(5, len(missing))
            warnings.append(
                f"Missing required fields: {', '.join(missing)}"
            )
    
    return max(0, score), warnings

def check_feature_alignment(features: List[str], 
                           implementation: str) -> Tuple[int, List[str]]:
    """Check if implementation includes required features."""
    warnings = []
    score = 10
    impl_lower = implementation.lower()
    
    missing_features = []
    for feature in features:
        # Simple keyword search - could be enhanced
        if feature.lower() not in impl_lower:
            missing_features.append(feature)
    
    if missing_features:
        score -= min(5, len(missing_features) * 2)
        warnings.append(
            f"Missing features: {', '.join(missing_features)}"
        )
    
    return max(0, score), warnings

def assess_requirement_clarity(locked_reqs: Dict[str, Any]) -> int:
    """Assess how clear and complete the requirements are."""
    score = 10
    reqs = locked_reqs.get('requirements', {})
    
    # Deduct for missing information
    if 'fields' not in reqs:
        score -= 2
    elif 'names' not in reqs.get('fields', {}):
        score -= 1
    
    if 'features' not in reqs:
        score -= 2
    
    if 'constraints' not in reqs:
        score -= 1
    
    return max(0, score)

def calculate_weighted_score(scores: Dict[str, int]) -> int:
    """Calculate weighted overall score."""
    weights = {
        "requirement_clarity": 0.15,
        "implementation_match": 0.35,  # Most important
        "deviation_risk": 0.25,
        "completeness": 0.15,
        "complexity": 0.10
    }
    
    total = sum(scores[key] * weights[key] for key in scores)
    return round(total)

def get_recommendation(score: int, warnings: List[str]) -> str:
    """Get recommendation based on score and warnings."""
    if score >= 8:
        return "High confidence - proceed with implementation"
    elif score >= 6:
        return "Moderate confidence - review warnings before proceeding"
    elif score >= 4:
        return "Low confidence - address warnings and clarify requirements"
    else:
        return "Very low confidence - do not proceed without clarification"

if __name__ == "__main__":
    # Test the assessment
    test_implementation = """
    Create ContactForm with the following fields:
    - firstName
    - lastName  
    - email
    - phone
    - company
    - message
    - consent
    
    Total: 7 fields
    """
    
    result = assess_requirement_confidence("ContactForm", test_implementation)
    print(json.dumps(result, indent=2))
