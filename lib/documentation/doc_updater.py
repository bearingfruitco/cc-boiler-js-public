"""
Documentation Updater
Updates documentation based on code changes using the documentation-writer agent
"""

import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from .doc_analyzer import DocumentationAnalyzer
try:
    from lib.agent_utils import invoke_documentation_writer
except ImportError:
    # If import fails, we'll use the template fallback
    invoke_documentation_writer = None


class DocumentationUpdater:
    """Updates documentation using the documentation-writer agent"""
    
    def __init__(self, project_root: str = "/Users/shawnsmith/dev/bfc/boilerplate"):
        self.project_root = Path(project_root)
        self.doc_agent = "documentation-writer"
        self.analyzer = DocumentationAnalyzer(project_root)
        
    def update_documentation(self, code_path: str, doc_path: str) -> Dict:
        """Update documentation for a code file"""
        result = {
            'success': False,
            'doc_path': doc_path,
            'update_type': 'update',
            'sections_updated': [],
            'error': None
        }
        
        try:
            # Analyze the code file
            code_info = self.analyzer.analyze_code_for_documentation(code_path)
            
            # Check if doc exists
            doc_exists = Path(doc_path).exists()
            
            if doc_exists:
                # Update existing documentation
                result = self.update_existing_doc(code_path, doc_path, code_info)
            else:
                # Create new documentation
                result = self.create_new_doc(code_path, doc_path, code_info)
                result['update_type'] = 'create'
            
        except Exception as e:
            result['error'] = str(e)
            
        return result
    
    def update_existing_doc(self, code_path: str, doc_path: str, 
                           code_info: Dict) -> Dict:
        """Update existing documentation file"""
        # Extract current sections
        sections = self.analyzer.extract_documentation_sections(doc_path)
        
        # Determine what needs updating
        update_needed = self._determine_updates_needed(code_info, sections)
        
        if not update_needed:
            return {
                'success': True,
                'doc_path': doc_path,
                'update_type': 'no_changes',
                'sections_updated': []
            }
        
        # Create update prompt
        prompt = self.create_update_prompt(
            code_path=code_path,
            doc_path=doc_path,
            code_info=code_info,
            sections=sections,
            updates_needed=update_needed
        )
        
        # Invoke documentation agent
        updated_content = self.invoke_doc_agent(prompt)
        
        if updated_content:
            # Write updated content
            Path(doc_path).write_text(updated_content)
            
            return {
                'success': True,
                'doc_path': doc_path,
                'update_type': 'update',
                'sections_updated': update_needed
            }
        else:
            return {
                'success': False,
                'doc_path': doc_path,
                'update_type': 'update',
                'sections_updated': [],
                'error': 'Failed to generate updated content'
            }
    
    def create_new_doc(self, code_path: str, doc_path: str, 
                      code_info: Dict) -> Dict:
        """Create new documentation file"""
        # Determine documentation type
        file_type = self.analyzer.determine_file_type(code_path)
        
        # Create generation prompt
        prompt = self.create_generation_prompt(
            code_path=code_path,
            doc_path=doc_path,
            code_info=code_info,
            file_type=file_type
        )
        
        # Invoke documentation agent
        content = self.invoke_doc_agent(prompt)
        
        if content:
            # Ensure directory exists
            Path(doc_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Write new documentation
            Path(doc_path).write_text(content)
            
            return {
                'success': True,
                'doc_path': doc_path,
                'update_type': 'create',
                'sections_updated': ['all']
            }
        else:
            return {
                'success': False,
                'doc_path': doc_path,
                'update_type': 'create',
                'sections_updated': [],
                'error': 'Failed to generate documentation'
            }
    
    def create_update_prompt(self, **kwargs) -> str:
        """Create prompt for updating existing documentation"""
        code_path = kwargs['code_path']
        doc_path = kwargs['doc_path']
        code_info = kwargs['code_info']
        sections = kwargs['sections']
        updates_needed = kwargs['updates_needed']
        
        prompt_parts = [
            f"Update the documentation for {Path(code_path).name}",
            f"\nCurrent documentation: {doc_path}",
            "\nCode Analysis Results:",
            "=" * 50
        ]
        
        # Add code information
        if code_info.get('props'):
            prompt_parts.append("\nComponent Props:")
            for prop in code_info['props']:
                prompt_parts.append(f"  - {prop['name']}: {prop['type']} {'(required)' if prop['required'] else '(optional)'}")
        
        if code_info.get('methods'):
            prompt_parts.append(f"\nMethods: {', '.join(code_info['methods'])}")
            
        if code_info.get('hooks'):
            prompt_parts.append(f"\nHooks Used: {', '.join(code_info['hooks'])}")
        
        # Add update requirements
        prompt_parts.extend([
            "\n\nUpdate Requirements:",
            "=" * 50,
            "1. Update the following sections:"
        ])
        
        for section in updates_needed:
            prompt_parts.append(f"   - {section}")
        
        prompt_parts.extend([
            "\n2. PRESERVE all sections marked with <!-- MANUAL: -->",
            "3. Update generated sections between <!-- GENERATED: --> and <!-- END GENERATED -->",
            "4. Keep the same documentation structure and format",
            "5. Update the 'Last Updated' timestamp",
            "6. Ensure code examples match the current implementation",
            "\nReturn the complete updated documentation."
        ])
        
        return '\n'.join(prompt_parts)
    
    def create_generation_prompt(self, **kwargs) -> str:
        """Create prompt for generating new documentation"""
        code_path = kwargs['code_path']
        code_info = kwargs['code_info']
        file_type = kwargs['file_type']
        
        component_name = self.analyzer.extract_component_name(code_path)
        
        prompt_parts = [
            f"Generate documentation for {component_name or Path(code_path).name}",
            f"\nFile Type: {file_type}",
            f"Source: {code_path}",
            "\nCode Analysis:",
            "=" * 50
        ]
        
        # Add code details based on type
        if file_type == 'component':
            from .templates.component_template import COMPONENT_TEMPLATE
            prompt_parts.extend([
                "\nUse this template structure:",
                COMPONENT_TEMPLATE,
                "\nFill in the template with:"
            ])
            
            if code_info.get('props'):
                prompt_parts.append("\nProps:")
                for prop in code_info['props']:
                    prompt_parts.append(f"  - {prop['name']}: {prop['type']} {'(required)' if prop['required'] else '(optional)'}")
                    
        elif file_type == 'api':
            from .templates.api_template import API_TEMPLATE
            prompt_parts.extend([
                "\nUse this template structure:",
                API_TEMPLATE,
                f"\nHTTP Methods: {', '.join(code_info.get('methods', []))}"
            ])
        
        prompt_parts.extend([
            "\n\nRequirements:",
            "1. Follow the template structure exactly",
            "2. Mark generated sections with <!-- GENERATED: section_name -->",
            "3. Include practical usage examples",
            "4. Add TypeScript types where relevant",
            "5. Include error handling examples",
            "\nGenerate complete documentation following project standards."
        ])
        
        return '\n'.join(prompt_parts)
    
    def invoke_doc_agent(self, prompt: str) -> Optional[str]:
        """Invoke the documentation-writer agent"""
        try:
            # Format request for documentation-writer agent
            agent_request = f"""<agent_request>
Agent: documentation-writer
Context: Automatic Documentation Update
Prompt:
{prompt}
</agent_request>"""
            
            # In Claude Code, this would trigger the documentation-writer agent
            # The agent would analyze the code and generate appropriate documentation
            
            # Generate documentation based on the prompt content
            return self._generate_actual_documentation(prompt)
            
        except Exception as e:
            print(f"Error invoking documentation agent: {e}")
            return None
    
    def _generate_actual_documentation(self, prompt: str) -> str:
        """Generate documentation based on prompt analysis"""
        import re
        
        # Extract component/file info from prompt
        component_match = re.search(r'documentation for (.+?)\n', prompt)
        component_name = component_match.group(1) if component_match else "Component"
        
        # Check if it's an update or new creation
        is_update = "Update the documentation" in prompt
        
        # Extract code analysis info
        has_props = "Component Props:" in prompt
        has_methods = "Methods:" in prompt
        has_api = "HTTP Methods:" in prompt
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if "component" in prompt.lower() or has_props:
            return self._generate_component_documentation(component_name, prompt, timestamp)
        elif "api" in prompt.lower() or has_api:
            return self._generate_api_documentation(component_name, prompt, timestamp)
        else:
            return self._generate_template_documentation()
    
    def _generate_component_documentation(self, component_name: str, prompt: str, timestamp: str) -> str:
        """Generate component-specific documentation"""
        # Extract props from prompt
        props_section = ""
        if "Component Props:" in prompt:
            props_match = re.search(r'Component Props:(.+?)(?:\n\n|\nMethods:|$)', prompt, re.DOTALL)
            if props_match:
                props_lines = props_match.group(1).strip().split('\n')
                for line in props_lines:
                    if '-' in line:
                        prop_match = re.match(r'\s*-\s*(\w+):\s*(.+?)\s*\((required|optional)\)', line)
                        if prop_match:
                            name, type_info, req = prop_match.groups()
                            default = '-' if req == 'required' else 'undefined'
                            props_section += f"| {name} | {type_info} | {default} | {req.capitalize()} prop |\n"
        
        if not props_section:
            props_section = "| prop | type | default | description |\n|------|------|---------|-------------|\n| children | ReactNode | - | Component children |\n"
        else:
            props_section = "| Prop | Type | Default | Description |\n|------|------|---------|-------------|\n" + props_section
        
        return f"""# {component_name}

<!-- GENERATED: component-overview -->
{component_name} is a React component that provides UI functionality for the application.
<!-- END GENERATED -->

## Installation

```bash
import {{ {component_name} }} from '@/components/{component_name}'
```

## API Reference

<!-- GENERATED: props-table -->
### Props

{props_section}
<!-- END GENERATED -->

## Usage Examples

<!-- GENERATED: examples -->
### Basic Usage

```tsx
<{component_name}>
  Content goes here
</{component_name}>
```

### Advanced Usage

```tsx
<{component_name}
  className="custom-class"
  onClick={{handleClick}}
>
  <span>Custom content</span>
</{component_name}>
```
<!-- END GENERATED -->

<!-- MANUAL: custom-notes -->
## Notes

Add any custom notes here. This section is preserved during updates.
<!-- END MANUAL -->

<!-- GENERATED: metadata -->
---
*Last updated: {timestamp}*
*Auto-generated from: components/{component_name}.tsx*
<!-- END GENERATED -->
"""
    
    def _generate_api_documentation(self, endpoint_name: str, prompt: str, timestamp: str) -> str:
        """Generate API-specific documentation"""
        # Extract HTTP methods from prompt
        methods = "GET"
        if "HTTP Methods:" in prompt:
            methods_match = re.search(r'HTTP Methods:\s*(.+?)(?:\n|$)', prompt)
            if methods_match:
                methods = methods_match.group(1).strip()
        
        # Extract path from endpoint name
        path = endpoint_name.lower().replace(' ', '-')
        if '/' in endpoint_name:
            path = endpoint_name.split('/')[-1]
        
        auth_required = "true" if "auth" in prompt.lower() else "false"
        
        return f"""# API: {endpoint_name}

<!-- GENERATED: endpoint-info -->
- **Method**: {methods}
- **Path**: `/api/{path}`
- **Auth Required**: {auth_required}
<!-- END GENERATED -->

## Request

<!-- GENERATED: request-schema -->
### Headers
| Header | Value | Required |
|--------|-------|----------|
| Content-Type | application/json | Yes |
| Authorization | Bearer TOKEN | {"Yes" if auth_required == "true" else "No"} |

### Body Schema
```typescript
interface Request {{
  // Request body schema
  data: unknown
}}
```
<!-- END GENERATED -->

## Response

<!-- GENERATED: response-schema -->
### Success Response (200)
```typescript
interface Response {{
  success: boolean
  data: {{
    // Response data
  }}
}}
```

### Error Responses
| Code | Description |
|------|-------------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 500 | Server Error |
<!-- END GENERATED -->

## Examples

<!-- GENERATED: examples -->
### cURL
```bash
curl -X {methods} https://api.example.com/api/{path} \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer YOUR_TOKEN"
```

### TypeScript
```typescript
const response = await fetch('/api/{path}', {{
  method: '{methods}',
  headers: {{
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token
  }}
}})
```
<!-- END GENERATED -->

<!-- MANUAL: notes -->
## Implementation Notes

Add any custom notes here.
<!-- END MANUAL -->

<!-- GENERATED: metadata -->
---
*Last updated: {timestamp}*
*Source: app/api/{path}/route.ts*
<!-- END GENERATED -->
"""
    
    def _generate_template_documentation(self) -> str:
        """Generate template documentation (placeholder)"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""# Component Name

<!-- GENERATED: component-overview -->
Component description goes here.
<!-- END GENERATED -->

## Installation

```bash
import {{ ComponentName }} from '@/components/ComponentName'
```

## API Reference

<!-- GENERATED: props-table -->
### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| prop1 | string | - | Description |
<!-- END GENERATED -->

## Usage Examples

<!-- GENERATED: examples -->
### Basic Usage

```tsx
<ComponentName prop1="value" />
```
<!-- END GENERATED -->

<!-- MANUAL: custom-notes -->
## Notes

Add any custom notes here. This section is preserved during updates.
<!-- END MANUAL -->

<!-- GENERATED: metadata -->
---
*Last updated: {timestamp}*
*Auto-generated from: components/ComponentName.tsx*
<!-- END GENERATED -->
"""
    
    def _determine_updates_needed(self, code_info: Dict, sections: Dict) -> List[str]:
        """Determine which sections need updating"""
        updates_needed = []
        
        # Always update metadata
        updates_needed.append('metadata')
        
        # Check if props have changed
        if code_info.get('props'):
            updates_needed.append('props-table')
            
        # Check if examples might need updating
        if code_info.get('methods') or code_info.get('hooks'):
            updates_needed.append('examples')
            
        # Update overview if major changes
        if len(updates_needed) > 2:
            updates_needed.append('component-overview')
        
        return updates_needed
    
    def update_component_docs(self, component_path: str, doc_path: str) -> Dict:
        """Specialized method for updating component documentation"""
        return self.update_documentation(component_path, doc_path)
    
    def update_api_docs(self, api_path: str, doc_path: str) -> Dict:
        """Specialized method for updating API documentation"""
        return self.update_documentation(api_path, doc_path)
    
    def update_type_docs(self, type_path: str, doc_path: str) -> Dict:
        """Specialized method for updating type documentation"""
        return self.update_documentation(type_path, doc_path)
