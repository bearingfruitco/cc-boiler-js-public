#!/usr/bin/env python3
"""
Architecture Change Tracker Hook
Tracks changes to architecture documents and maintains changelog
"""

import sys
import json
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.environ.get('CLAUDE_PROJECT_DIR', '/Users/shawnsmith/dev/bfc/boilerplate'))

from lib.architecture.change_detector import ArchitectureChangeDetector
from lib.architecture.change_logger import ArchitectureChangeLogger
from lib.architecture.adr_generator import ADRGenerator


def main():
    """Main hook entry point"""
    try:
        # Get hook input
        input_data = json.loads(sys.stdin.read())
        
        # Check if this is a file edit tool
        tool_name = input_data.get('tool_name')
        if tool_name not in ['Edit', 'Write', 'MultiEdit']:
            return 0
            
        # Get file path
        tool_input = input_data.get('tool_input', {})
        file_path = tool_input.get('file_path', '')
        
        # Only track architecture files
        if not file_path.startswith('docs/architecture/'):
            return 0
            
        # Skip the changelog and ADR files themselves
        if 'CHANGELOG.md' in file_path or '/decisions/' in file_path:
            return 0
            
        # Skip state files
        if file_path.endswith('.json'):
            return 0
        
        # Detect changes
        project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '/Users/shawnsmith/dev/bfc/boilerplate')
        detector = ArchitectureChangeDetector(project_dir)
        changes = detector.detect_changes(Path(project_dir) / file_path)
        
        if not changes:
            # No significant changes detected
            return 0
        
        # Extract metadata from tool input
        metadata = {
            "author": os.environ.get('USER', 'system'),
            "rationale": extract_rationale(tool_input),
            "related_prp": extract_related_prp(),
            "related_issue": extract_related_issue(),
            "tags": extract_tags(changes)
        }
        
        # Create change record
        logger = ArchitectureChangeLogger(base_path=project_dir)
        change_record = logger.create_change_record(
            file_path=file_path,
            changes=changes,
            metadata=metadata
        )
        
        # Log the change
        logger.log_change(change_record)
        
        # Generate ADR if needed
        adr_gen = ADRGenerator(project_dir)
        adr_path = None
        if adr_gen.should_generate_adr(change_record):
            adr_path = adr_gen.generate_adr(change_record)
            adr_gen.generate_adr_index()
        
        # Provide feedback
        output = create_output(change_record, adr_path)
        print(json.dumps(output))
        
    except Exception as e:
        # Log error but don't block
        print(f"Architecture tracking error: {e}", file=sys.stderr)
        return 1
    
    return 0


def extract_rationale(tool_input: dict) -> str:
    """Extract rationale from edit description"""
    # Look for description in tool input
    description = tool_input.get('description', '')
    
    # Common patterns for rationale
    if 'to support' in description.lower():
        return description
    elif 'for' in description.lower():
        return description
    elif 'because' in description.lower():
        return description
    
    return ""


def extract_related_prp() -> str:
    """Extract related PRP from context"""
    # Check if we're in a PRP workflow
    prp_file = os.environ.get('CLAUDE_ACTIVE_PRP', '')
    if prp_file:
        return Path(prp_file).stem
    
    # Check for PRP in current directory context
    cwd = os.getcwd()
    if '/PRPs/active/' in cwd:
        return Path(cwd).name
        
    return ""


def extract_related_issue() -> str:
    """Extract related issue number from context"""
    # Check environment for active issue
    issue = os.environ.get('CLAUDE_ACTIVE_ISSUE', '')
    if issue:
        return issue
        
    # Could also check git branch name for issue numbers
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True,
            timeout=2
        )
        branch = result.stdout.strip()
        
        # Extract issue number from branch (e.g., feature/123-add-cache)
        import re
        match = re.search(r'(\d+)', branch)
        if match:
            return match.group(1)
    except:
        pass
        
    return ""


def extract_tags(changes: dict) -> list:
    """Extract relevant tags based on changes"""
    tags = []
    
    # Add tags based on change type
    change_type = changes.get('type', '')
    if 'component' in change_type:
        tags.append('component_change')
    if 'api' in change_type:
        tags.append('api_change')
    if 'schema' in change_type:
        tags.append('database_change')
    if 'security' in change_type:
        tags.append('security_change')
    
    # Add impact tags
    impact = changes.get('impact', {})
    if impact.get('breaking_change'):
        tags.append('breaking_change')
    if impact.get('requires_migration'):
        tags.append('migration_required')
        
    return tags


def create_output(change_record: dict, adr_path: str = None) -> dict:
    """Create structured output for the hook"""
    # Format feedback message
    feedback_lines = [
        f"📝 Architecture change tracked: {change_record['description']}"
    ]
    
    # Add impact information
    impact = change_record['impact']
    if impact['severity'] in ['high', 'critical']:
        feedback_lines.append(f"⚠️  Impact: {impact['severity'].upper()}")
        
    if impact.get('breaking_change'):
        feedback_lines.append("🚨 This is a BREAKING CHANGE")
        
    if impact.get('components_affected'):
        feedback_lines.append(f"🔧 Components affected: {', '.join(impact['components_affected'])}")
    
    # Add ADR information
    if adr_path:
        feedback_lines.append(f"📋 ADR generated: {adr_path}")
    
    feedback = "\n".join(feedback_lines)
    
    # Suggest next actions
    suggestions = []
    
    # If high impact, suggest validation
    if impact['severity'] in ['high', 'critical']:
        suggestions.append({
            "command": "/validate-architecture",
            "description": "Validate architecture completeness and consistency"
        })
    
    # If components affected, suggest PRP sync
    if impact.get('components_affected'):
        suggestions.append({
            "command": "/prp-sync --preview",
            "description": f"Check if PRPs need updating ({len(impact['components_affected'])} components affected)"
        })
    
    # If breaking change, suggest migration planning
    if impact.get('breaking_change'):
        suggestions.append({
            "command": "/create-prp migration-plan",
            "description": "Create migration plan for breaking changes"
        })
    
    # Always suggest viewing the changelog
    suggestions.append({
        "command": "cat docs/architecture/CHANGELOG.md",
        "description": "View architecture changelog"
    })
    
    return {
        "continue": True,
        "feedback": feedback,
        "nextSuggestions": suggestions,
        "metadata": {
            "change_id": change_record['id'],
            "severity": impact['severity'],
            "breaking": impact.get('breaking_change', False)
        }
    }


if __name__ == "__main__":
    sys.exit(main())
