#!/usr/bin/env python3
"""
Auto Documentation Updater Hook
Automatically updates documentation when code changes
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.environ.get('CLAUDE_PROJECT_DIR', '/Users/shawnsmith/dev/bfc/boilerplate'))

from lib.documentation.doc_analyzer import DocumentationAnalyzer
from lib.documentation.doc_updater import DocumentationUpdater
from lib.documentation.doc_tracker import DocumentationTracker


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
        
        # Skip non-code files
        if not is_code_file(file_path):
            return 0
            
        # Skip test files
        if is_test_file(file_path):
            return 0
            
        # Skip documentation files
        if is_documentation_file(file_path):
            return 0
        
        project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '/Users/shawnsmith/dev/bfc/boilerplate')
        
        # Analyze what documentation needs updating
        analyzer = DocumentationAnalyzer(project_dir)
        analysis = analyzer.analyze_code_change(file_path, tool_name)
        
        if not analysis['docs_to_update']:
            # No documentation needs updating
            return 0
        
        # Skip if update strategy is 'skip'
        if analysis['update_strategy'] == 'skip':
            return 0
        
        # Update documentation
        updater = DocumentationUpdater(project_dir)
        tracker = DocumentationTracker(project_root=project_dir)
        
        updates_made = []
        errors = []
        
        for doc_path in analysis['docs_to_update']:
            try:
                # Check if update is needed based on timing
                source_mtime = datetime.fromtimestamp(
                    Path(project_dir, file_path).stat().st_mtime
                )
                
                if not tracker.should_update_doc(doc_path, source_mtime):
                    continue
                
                # Update documentation
                result = updater.update_documentation(file_path, doc_path)
                
                if result['success']:
                    updates_made.append(result)
                    
                    # Track the update
                    tracker.log_update(file_path, doc_path, result)
                else:
                    errors.append(result)
                    
            except Exception as e:
                errors.append({
                    'doc': doc_path,
                    'error': str(e)
                })
        
        # Generate output
        if updates_made or errors:
            output = create_output(updates_made, errors, analysis)
            print(json.dumps(output))
        
    except Exception as e:
        print(f"Documentation updater error: {e}", file=sys.stderr)
        return 1
    
    return 0


def is_code_file(path: str) -> bool:
    """Check if file is a code file that might need docs"""
    code_extensions = {'.ts', '.tsx', '.js', '.jsx', '.py', '.sql'}
    return any(path.endswith(ext) for ext in code_extensions)


def is_test_file(path: str) -> bool:
    """Check if file is a test file"""
    test_patterns = ['.test.', '.spec.', '__tests__/', 'tests/']
    return any(pattern in path for pattern in test_patterns)


def is_documentation_file(path: str) -> bool:
    """Check if file is documentation"""
    return (
        path.endswith('.md') or
        path.startswith('docs/') or
        'README' in path or
        path.endswith('.mdx')
    )


def create_output(updates_made: list, errors: list, analysis: dict) -> dict:
    """Create structured output for the hook"""
    feedback_lines = []
    
    if updates_made:
        feedback_lines.append(f"📚 Documentation updated for {analysis['file']}:")
        
        for update in updates_made:
            emoji = "📄" if update['update_type'] == 'create' else "📝"
            doc_name = Path(update['doc_path']).name
            feedback_lines.append(f"{emoji} {doc_name}")
            
            if update['sections_updated'] and update['sections_updated'] != ['all']:
                sections = ', '.join(update['sections_updated'])
                feedback_lines.append(f"   Updated: {sections}")
    
    if errors:
        feedback_lines.append("\n❌ Documentation update errors:")
        for error in errors:
            doc_name = Path(error.get('doc', 'unknown')).name
            feedback_lines.append(f"   - {doc_name}: {error.get('error', 'Unknown error')}")
    
    # Suggest next actions
    suggestions = []
    
    # If component docs updated, suggest reviewing
    if any('components/' in u['doc_path'] for u in updates_made):
        suggestions.append({
            "command": "/review-docs components",
            "description": "Review updated component documentation"
        })
    
    # If API docs updated, suggest validating
    if any('api/' in u['doc_path'] for u in updates_made):
        suggestions.append({
            "command": "/validate-api-docs",
            "description": "Validate API documentation accuracy"
        })
    
    # Always suggest viewing the docs
    if updates_made:
        first_doc = updates_made[0]['doc_path']
        suggestions.append({
            "command": f"cat {first_doc}",
            "description": "View updated documentation"
        })
    
    # If there were errors, suggest manual update
    if errors:
        suggestions.append({
            "command": "/update-docs --manual",
            "description": "Manually update failed documentation"
        })
    
    return {
        "continue": True,
        "feedback": "\n".join(feedback_lines),
        "nextSuggestions": suggestions,
        "metadata": {
            "updates_count": len(updates_made),
            "errors_count": len(errors),
            "components_affected": analysis.get('components_affected', [])
        }
    }


if __name__ == "__main__":
    sys.exit(main())
