# PRP: Auto Documentation Updater Hook

## Overview
Create an intelligent hook system that automatically updates documentation when code changes, ensuring docs stay perfectly synchronized with implementation.

## Goals
1. **Automatic Documentation Updates**: Detect code changes and update relevant docs
2. **Preserve Manual Content**: Keep human-written sections while updating generated parts
3. **Multi-Format Support**: Handle markdown, JSDoc, and type definitions
4. **Agent Integration**: Use specialized documentation-writer agent for quality

## Background Context

### Current State
- Documentation lives in multiple places (docs/, component READMEs, JSDoc)
- Manual updates required when code changes
- Documentation drift is common
- No automatic synchronization

### Desired State
- Code changes trigger automatic doc updates
- Documentation always matches implementation
- Manual sections preserved and respected
- Clear tracking of what was auto-updated

## Technical Context

### Documentation Locations
```
docs/
├── components/          # Component documentation
├── api/                # API endpoint docs
├── architecture/       # System design docs
└── guides/            # User guides

components/
└── */README.md        # Component-specific docs

app/api/
└── */route.ts        # JSDoc API documentation
```

### Update Triggers
- Component file changes → Update component docs
- API route changes → Update API docs
- Type definition changes → Update type docs
- Database schema changes → Update schema docs

## Implementation Blueprint

### Phase 1: Hook Infrastructure (2 hours)

#### 1.1 Create Documentation Analyzer
```python
# lib/documentation/doc_analyzer.py
import ast
import re
from pathlib import Path
from typing import Dict, List, Optional

class DocumentationAnalyzer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.doc_mappings = self.load_doc_mappings()
        
    def analyze_code_change(self, file_path: str, change_type: str) -> Dict:
        """Analyze what documentation needs updating"""
        analysis = {
            "file": file_path,
            "type": self.determine_file_type(file_path),
            "docs_to_update": [],
            "update_strategy": "incremental"
        }
        
        # Find related documentation
        if self.is_component(file_path):
            analysis["docs_to_update"].extend(
                self.find_component_docs(file_path)
            )
        
        if self.is_api_route(file_path):
            analysis["docs_to_update"].extend(
                self.find_api_docs(file_path)
            )
            
        if self.is_type_definition(file_path):
            analysis["docs_to_update"].extend(
                self.find_type_docs(file_path)
            )
            
        return analysis
    
    def extract_documentation_sections(self, doc_path: str) -> Dict:
        """Extract manual vs generated sections"""
        with open(doc_path, 'r') as f:
            content = f.read()
            
        sections = {
            "manual": [],
            "generated": [],
            "metadata": {}
        }
        
        # Parse markdown sections
        current_section = None
        for line in content.split('\n'):
            if line.startswith('<!-- GENERATED:'):
                current_section = 'generated'
            elif line.startswith('<!-- MANUAL:'):
                current_section = 'manual'
            elif line.startswith('<!-- END'):
                current_section = None
            elif current_section:
                sections[current_section].append(line)
                
        return sections
```

#### 1.2 Create Documentation Updater
```python
# lib/documentation/doc_updater.py
import subprocess
import json
from datetime import datetime

class DocumentationUpdater:
    def __init__(self):
        self.doc_agent = "documentation-writer"
        
    def update_component_docs(self, component_path: str, doc_path: str):
        """Update component documentation using doc agent"""
        # Extract component information
        component_info = self.analyze_component(component_path)
        
        # Prepare prompt for documentation agent
        prompt = self.create_update_prompt(
            component_info=component_info,
            doc_path=doc_path,
            update_type="component"
        )
        
        # Use documentation-writer agent
        updated_content = self.invoke_doc_agent(prompt)
        
        # Merge with existing manual content
        return self.merge_documentation(doc_path, updated_content)
    
    def create_update_prompt(self, **kwargs) -> str:
        """Create prompt for documentation agent"""
        if kwargs['update_type'] == 'component':
            return f"""
Update the documentation for {kwargs['component_info']['name']} component.

Component Details:
- Props: {json.dumps(kwargs['component_info']['props'], indent=2)}
- Methods: {json.dumps(kwargs['component_info']['methods'], indent=2)}
- Hooks: {kwargs['component_info']['hooks']}

Current Documentation: {kwargs['doc_path']}

Requirements:
1. Update the API section with current props/methods
2. Keep all sections marked with <!-- MANUAL: -->
3. Update code examples to match new API
4. Add deprecation notices if needed
5. Update the "Last Updated" timestamp

Return the complete updated documentation.
"""
    
    def invoke_doc_agent(self, prompt: str) -> str:
        """Invoke documentation-writer agent"""
        # This would integrate with the actual agent system
        # For now, showing the pattern
        result = subprocess.run(
            ["claude", "spawn", "doc", prompt],
            capture_output=True,
            text=True
        )
        return result.stdout
```

### Phase 2: Hook Implementation (1.5 hours)

#### 2.1 Post-Tool-Use Hook
```python
#!/usr/bin/env python3
# .claude/hooks/post-tool-use/25-doc-updater.py

import sys
import json
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.environ.get('CLAUDE_PROJECT_DIR', '/Users/shawnsmith/dev/bfc/boilerplate'))

from lib.documentation.doc_analyzer import DocumentationAnalyzer
from lib.documentation.doc_updater import DocumentationUpdater
from lib.documentation.doc_tracker import DocumentationTracker

def main():
    # Get hook input
    input_data = json.loads(sys.stdin.read())
    
    # Check if this is a code file edit
    tool_name = input_data.get('tool_name')
    if tool_name not in ['Edit', 'Write', 'MultiEdit']:
        return 0
        
    file_path = input_data.get('tool_input', {}).get('file_path', '')
    
    # Skip non-code files
    if not is_code_file(file_path):
        return 0
    
    # Skip documentation files themselves
    if is_documentation_file(file_path):
        return 0
    
    try:
        # Analyze what needs updating
        analyzer = DocumentationAnalyzer(os.environ['CLAUDE_PROJECT_DIR'])
        analysis = analyzer.analyze_code_change(file_path, tool_name)
        
        if not analysis['docs_to_update']:
            return 0
        
        # Update documentation
        updater = DocumentationUpdater()
        tracker = DocumentationTracker()
        
        updates_made = []
        for doc_path in analysis['docs_to_update']:
            # Check if doc exists
            if not Path(doc_path).exists():
                # Create new documentation
                result = updater.create_documentation(file_path, doc_path)
            else:
                # Update existing documentation
                result = updater.update_documentation(file_path, doc_path)
            
            if result['success']:
                updates_made.append({
                    'doc': doc_path,
                    'type': result['update_type'],
                    'sections': result['sections_updated']
                })
                
                # Track the update
                tracker.log_update(file_path, doc_path, result)
        
        # Provide feedback
        if updates_made:
            print(json.dumps({
                "continue": True,
                "feedback": format_update_feedback(updates_made),
                "nextSuggestions": suggest_next_actions(updates_made)
            }))
            
    except Exception as e:
        # Log error but don't block
        print(f"Documentation update error: {e}", file=sys.stderr)
        return 1
    
    return 0

def is_code_file(path: str) -> bool:
    """Check if file is a code file that might need docs"""
    code_extensions = {'.ts', '.tsx', '.js', '.jsx', '.py', '.sql'}
    return any(path.endswith(ext) for ext in code_extensions)

def is_documentation_file(path: str) -> bool:
    """Check if file is documentation"""
    return (
        path.endswith('.md') or
        path.startswith('docs/') or
        'README' in path
    )

def format_update_feedback(updates: list) -> str:
    """Format feedback about documentation updates"""
    feedback = "📚 Documentation updated:\n"
    for update in updates:
        emoji = "📝" if update['type'] == 'update' else "📄"
        feedback += f"{emoji} {update['doc']}\n"
        if update['sections']:
            feedback += f"   Sections: {', '.join(update['sections'])}\n"
    return feedback

def suggest_next_actions(updates: list) -> list:
    """Suggest next actions after doc updates"""
    suggestions = []
    
    # If component docs updated, suggest reviewing
    if any('components/' in u['doc'] for u in updates):
        suggestions.append({
            "command": "/review-docs components",
            "description": "Review updated component documentation"
        })
    
    # If API docs updated, suggest testing
    if any('api/' in u['doc'] for u in updates):
        suggestions.append({
            "command": "/test-api",
            "description": "Test API endpoints match documentation"
        })
    
    return suggestions

if __name__ == "__main__":
    sys.exit(main())
```

### Phase 3: Documentation Templates (1 hour)

#### 3.1 Component Documentation Template
```python
# lib/documentation/templates/component_template.py

COMPONENT_TEMPLATE = """# {component_name}

<!-- GENERATED: component-overview -->
{overview}
<!-- END GENERATED -->

## Installation

```bash
import {{ {component_name} }} from '@/components/{component_path}'
```

## API Reference

<!-- GENERATED: props-table -->
### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
{props_table}
<!-- END GENERATED -->

<!-- GENERATED: methods-table -->
### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
{methods_table}
<!-- END GENERATED -->

## Usage Examples

<!-- GENERATED: examples -->
### Basic Usage

```tsx
{basic_example}
```

### Advanced Usage

```tsx
{advanced_example}
```
<!-- END GENERATED -->

<!-- MANUAL: custom-notes -->
## Notes

Add any custom notes here. This section is preserved during updates.
<!-- END MANUAL -->

<!-- GENERATED: metadata -->
---
*Last updated: {timestamp}*
*Auto-generated from: {source_file}*
<!-- END GENERATED -->
"""

API_TEMPLATE = """# API: {endpoint_name}

<!-- GENERATED: endpoint-info -->
- **Method**: {method}
- **Path**: `/api/{path}`
- **Auth Required**: {auth_required}
<!-- END GENERATED -->

## Request

<!-- GENERATED: request-schema -->
### Headers
{headers_table}

### Body Schema
```typescript
{request_schema}
```

### Query Parameters
{query_params_table}
<!-- END GENERATED -->

## Response

<!-- GENERATED: response-schema -->
### Success Response (200)
```typescript
{success_response}
```

### Error Responses
{error_responses}
<!-- END GENERATED -->

## Examples

<!-- GENERATED: examples -->
### cURL
```bash
{curl_example}
```

### TypeScript
```typescript
{typescript_example}
```
<!-- END GENERATED -->

<!-- MANUAL: notes -->
## Implementation Notes

Add any custom notes here.
<!-- END MANUAL -->

<!-- GENERATED: metadata -->
---
*Last updated: {timestamp}*
*Source: {source_file}*
<!-- END GENERATED -->
"""
```

### Phase 4: Integration & Testing (1.5 hours)

#### 4.1 Integration with Existing Systems
```python
# lib/documentation/doc_integration.py

class DocumentationIntegration:
    def __init__(self):
        self.config = self.load_config()
        
    def integrate_with_commands(self):
        """Add documentation commands"""
        commands = {
            "/update-docs": "Force documentation update for current files",
            "/doc-status": "Show documentation sync status",
            "/doc-preview": "Preview documentation changes"
        }
        
        # Register commands
        for cmd, desc in commands.items():
            self.register_command(cmd, desc)
    
    def integrate_with_agents(self):
        """Configure agent integration"""
        agent_config = {
            "documentation-writer": {
                "prompts": {
                    "component": self.load_prompt("component_doc"),
                    "api": self.load_prompt("api_doc"),
                    "type": self.load_prompt("type_doc")
                },
                "constraints": [
                    "Preserve MANUAL sections",
                    "Use project voice and tone",
                    "Include practical examples",
                    "Follow documentation standards"
                ]
            }
        }
        
        return agent_config
```

## Validation Loops

### 🔴 Level 1: Syntax & Standards (Every Change)
```bash
# Automatic on every doc update
- Markdown linting
- Link validation  
- Code example syntax check
- Template compliance
```

### 🟡 Level 2: Content Quality (Periodic)
```bash
# Run with /doc-validate
- Completeness check
- Example compilation
- Cross-reference validation
- Manual section preservation
```

### 🟢 Level 3: Integration Testing (Pre-PR)
```bash
# Run with /doc-test
- Documentation site build
- API doc accuracy
- Component playground test
- Search index update
```

### 🔵 Level 4: Production Readiness (Release)
```bash
# Run with /doc-audit
- Full documentation coverage
- Broken link scan
- Version consistency
- Accessibility check
```

## Success Criteria

- [ ] Code changes trigger automatic doc updates within 5 seconds
- [ ] Manual documentation sections always preserved
- [ ] Documentation-writer agent used for quality content
- [ ] Support for markdown, JSDoc, and type definitions
- [ ] Clear marking of auto-generated vs manual content
- [ ] Integration with existing documentation workflow
- [ ] Tracking of all documentation updates
- [ ] Rollback capability for doc changes

## Common Pitfalls & Solutions

### Pitfall 1: Over-updating
**Problem**: Every tiny change triggers doc updates
**Solution**: Batch updates with debouncing, significance threshold

### Pitfall 2: Losing Manual Content  
**Problem**: Auto-updates overwrite carefully written docs
**Solution**: Clear section markers, strict preservation rules

### Pitfall 3: Circular Updates
**Problem**: Doc updates trigger code formatting which triggers doc updates
**Solution**: Skip documentation files in hook, update tracking

### Pitfall 4: Agent Latency
**Problem**: Doc agent takes time, slows development
**Solution**: Async updates, queue system, caching

## Testing Strategy

1. **Unit Tests**: Doc analyzer, section parser, template system
2. **Integration Tests**: Hook triggers, agent communication
3. **End-to-End Tests**: Full update flow from code change to doc
4. **Manual Testing**: Verify quality of generated documentation

## Rollout Plan

1. **Phase 1**: Deploy hook without agent integration (template-based)
2. **Phase 2**: Add documentation-writer agent for quality
3. **Phase 3**: Expand to all documentation types
4. **Phase 4**: Add advanced features (versioning, diffs)

This PRP ensures documentation stays perfectly synchronized with code through intelligent automation while preserving the human touch in manually written sections.
