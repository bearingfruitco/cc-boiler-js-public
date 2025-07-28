#!/usr/bin/env python3
"""
Documentation-First Enforcer
Makes documentation generation mandatory for all components and APIs
Part of v4.0 automation plan - Issue #20
"""

import os
import json
import re
import sys
from pathlib import Path
from datetime import datetime

class DocumentationGenerator:
    def __init__(self):
        self.templates_dir = Path('.claude/templates/docs')
        self.docs_dir = Path('docs/components')
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure documentation directories exist"""
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.docs_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_component_info(self, content, path):
        """Extract component information from code"""
        info = {
            'name': Path(path).stem,
            'props': {},
            'hooks': [],
            'dependencies': [],
            'description': '',
            'isAsync': 'async' in content,
            'hasState': 'useState' in content or 'useReducer' in content,
            'hasEffects': 'useEffect' in content
        }
        
        # Extract component name
        component_match = re.search(r'(?:export\s+)?(?:default\s+)?function\s+(\w+)', content)
        if component_match:
            info['name'] = component_match.group(1)
        
        # Extract props
        props_match = re.search(r'interface\s+\w*Props\s*{([^}]+)}', content, re.DOTALL)
        if props_match:
            props_content = props_match.group(1)
            prop_pattern = r'(\w+)(\?)?:\s*([^;]+);?'
            for match in re.finditer(prop_pattern, props_content):
                prop_name = match.group(1)
                optional = match.group(2) == '?'
                prop_type = match.group(3).strip()
                info['props'][prop_name] = {
                    'type': prop_type,
                    'optional': optional,
                    'description': f"{prop_name} property"
                }
        
        # Extract hooks
        hook_pattern = r'use(\w+)\('
        for match in re.finditer(hook_pattern, content):
            hook_name = f"use{match.group(1)}"
            if hook_name not in info['hooks']:
                info['hooks'].append(hook_name)
        
        # Extract imports
        import_pattern = r'import\s+.*?\s+from\s+[\'"]([^\'"\s]+)[\'"]'
        for match in re.finditer(import_pattern, content):
            dep = match.group(1)
            if not dep.startswith('.'):
                info['dependencies'].append(dep)
        
        return info
    
    def generate_component_docs(self, info, content):
        """Generate comprehensive documentation for a component"""
        props_table = self._generate_props_table(info['props'])
        examples = self._generate_usage_examples(info)
        a11y_notes = self._generate_accessibility_notes(info, content)
        perf_notes = self._generate_performance_notes(info)
        
        return f"""# Component: {info['name']}

## Overview
{info['description'] or f"React component that implements {info['name']} functionality."}

## Import
```typescript
import {{ {info['name']} }} from '@/components/{info['name']}';
```

## Props
{props_table}

## Usage Examples

### Basic Usage
{examples['basic']}

### Advanced Usage
{examples['advanced']}

### With Error Handling
{examples['error']}

## Features
- {'✅' if info['hasState'] else '❌'} Stateful component
- {'✅' if info['isAsync'] else '❌'} Async operations
- {'✅' if info['hasEffects'] else '❌'} Side effects
- {'✅' if info['hooks'] else '❌'} Custom hooks

## Hooks Used
{chr(10).join(f"- `{hook}`" for hook in info['hooks']) if info['hooks'] else "No hooks used"}

## Accessibility
{a11y_notes}

## Performance Considerations
{perf_notes}

## Dependencies
{chr(10).join(f"- `{dep}`" for dep in info['dependencies']) if info['dependencies'] else "No external dependencies"}

## Testing
```typescript
import {{ render, screen }} from '@testing-library/react';
import {{ {info['name']} }} from './{info['name']}';

describe('{info['name']}', () => {{
  it('renders without crashing', () => {{
    render(<{info['name']} />);
  }});
  
  // Add more tests here
}});
```

## Storybook
```typescript
import type {{ Meta, StoryObj }} from '@storybook/react';
import {{ {info['name']} }} from './{info['name']}';

const meta: Meta<typeof {info['name']}> = {{
  title: 'Components/{info['name']}',
  component: {info['name']},
  parameters: {{
    layout: 'centered',
  }},
  tags: ['autodocs'],
}};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {{
  args: {{
    // Add default props here
  }},
}};
```

## API Reference
See the [API documentation](/api/components/{info['name'].lower()}) for detailed prop descriptions and types.

---
Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    def _generate_props_table(self, props):
        """Generate markdown table for props"""
        if not props:
            return "This component accepts no props."
        
        table = "| Prop | Type | Required | Description |\n"
        table += "|------|------|----------|-------------|\n"
        
        for name, details in props.items():
            required = "No" if details['optional'] else "Yes"
            table += f"| `{name}` | `{details['type']}` | {required} | {details['description']} |\n"
        
        return table
    
    def _generate_usage_examples(self, info):
        """Generate usage examples"""
        component_name = info['name']
        props_str = ""
        
        if info['props']:
            # Generate props for examples
            required_props = {k: v for k, v in info['props'].items() if not v['optional']}
            if required_props:
                props_examples = []
                for prop, details in required_props.items():
                    if 'string' in details['type']:
                        props_examples.append(f'{prop}="example"')
                    elif 'number' in details['type']:
                        props_examples.append(f'{prop}={{42}}')
                    elif 'boolean' in details['type']:
                        props_examples.append(f'{prop}')
                    else:
                        props_examples.append(f'{prop}={{/* value */}}')
                props_str = " " + " ".join(props_examples)
        
        return {
            'basic': f"""```tsx
<{component_name}{props_str} />
```""",
            'advanced': f"""```tsx
function MyComponent() {{
  const [state, setState] = useState();
  
  return (
    <{component_name}
      {props_str.strip()}
      onEvent={{handleEvent}}
    />
  );
}}
```""",
            'error': f"""```tsx
<ErrorBoundary>
  <{component_name}{props_str} />
</ErrorBoundary>
```"""
        }
    
    def _generate_accessibility_notes(self, info, content):
        """Generate accessibility notes based on component analysis"""
        notes = []
        
        # Check for ARIA attributes
        if 'aria-' in content:
            notes.append("✅ ARIA attributes detected")
        else:
            notes.append("⚠️ Consider adding ARIA attributes for better screen reader support")
        
        # Check for keyboard navigation
        if 'onKeyDown' in content or 'onKeyPress' in content:
            notes.append("✅ Keyboard event handlers present")
        elif 'button' in content.lower() or 'onClick' in content:
            notes.append("⚠️ Ensure keyboard navigation is supported for interactive elements")
        
        # Check for focus management
        if 'focus' in content.lower():
            notes.append("✅ Focus management detected")
        
        # Check for alt text
        if '<img' in content and 'alt=' not in content:
            notes.append("❌ Images detected without alt text")
        
        return "\n".join(notes) if notes else "No specific accessibility concerns detected. Follow WCAG 2.1 guidelines."
    
    def _generate_performance_notes(self, info):
        """Generate performance considerations"""
        notes = []
        
        if info['hasState']:
            notes.append("- Component maintains internal state. Consider memoization if used in lists.")
        
        if info['hasEffects']:
            notes.append("- Uses side effects. Ensure proper cleanup and dependency arrays.")
        
        if 'map' in str(info):
            notes.append("- May render lists. Consider virtualization for large datasets.")
        
        if len(info['dependencies']) > 5:
            notes.append("- Multiple dependencies. Monitor bundle size impact.")
        
        return "\n".join(notes) if notes else "No specific performance concerns identified."
    
    def generate_storybook_story(self, info):
        """Generate Storybook story file"""
        return f"""import type {{ Meta, StoryObj }} from '@storybook/react';
import {{ {info['name']} }} from './{info['name']}';

const meta: Meta<typeof {info['name']}> = {{
  title: 'Components/{info['name']}',
  component: {info['name']},
  parameters: {{
    layout: 'centered',
    docs: {{
      description: {{
        component: '{info['description'] or "Component description"}'
      }}
    }}
  }},
  tags: ['autodocs'],
  argTypes: {{
    {self._generate_arg_types(info['props'])}
  }},
}};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {{
  args: {{
    {self._generate_default_args(info['props'])}
  }},
}};

export const Playground: Story = {{
  args: {{
    {self._generate_default_args(info['props'])}
  }},
  render: (args) => <{info['name']} {{...args}} />,
}};
"""
    
    def _generate_arg_types(self, props):
        """Generate Storybook argTypes"""
        if not props:
            return ""
        
        arg_types = []
        for name, details in props.items():
            arg_type = f"    {name}: {{\n"
            arg_type += f"      description: '{details['description']}',\n"
            
            if 'boolean' in details['type']:
                arg_type += "      control: 'boolean',\n"
            elif 'number' in details['type']:
                arg_type += "      control: 'number',\n"
            elif 'string' in details['type']:
                arg_type += "      control: 'text',\n"
            
            arg_type += "    },"
            arg_types.append(arg_type)
        
        return "\n".join(arg_types)
    
    def _generate_default_args(self, props):
        """Generate default args for Storybook"""
        if not props:
            return ""
        
        args = []
        for name, details in props.items():
            if not details['optional']:
                if 'string' in details['type']:
                    args.append(f"    {name}: 'Example {name}',")
                elif 'number' in details['type']:
                    args.append(f"    {name}: 42,")
                elif 'boolean' in details['type']:
                    args.append(f"    {name}: true,")
        
        return "\n".join(args)

def check_for_component_creation(tool_use):
    """Check if creating a React component"""
    if tool_use.tool != 'str_replace_editor':
        return False
    
    path = tool_use.path or ''
    content = getattr(tool_use, 'new_str', '') or getattr(tool_use, 'content', '')
    
    # Check if it's a component file
    if not (path.endswith('.tsx') or path.endswith('.jsx')):
        return False
    
    # Check for component patterns
    component_patterns = [
        r'export\s+(?:default\s+)?function\s+\w+',
        r'export\s+const\s+\w+\s*=\s*\(',
        r'const\s+\w+\s*=\s*\([^)]*\)\s*=>\s*[{(]',
        r'React\.FC',
        r'React\.Component'
    ]
    
    for pattern in component_patterns:
        if re.search(pattern, content):
            return True
    
    return False

def check_for_existing_docs(component_name):
    """Check if documentation already exists"""
    docs_locations = [
        f'docs/components/{component_name}.md',
        f'components/{component_name}/README.md',
        f'stories/{component_name}.stories.tsx'
    ]
    
    for doc_path in docs_locations:
        if Path(doc_path).exists():
            return True
    
    return False

def main(tool_use):
    if not check_for_component_creation(tool_use):
        return
    
    path = tool_use.path
    content = getattr(tool_use, 'new_str', '') or getattr(tool_use, 'content', '')
    
    # Skip if documentation already exists
    component_name = Path(path).stem
    if check_for_existing_docs(component_name):
        return
    
    # Check for opt-out
    if '--no-docs' in content or '@no-docs' in content:
        print("📝 Documentation skipped (--no-docs flag)")
        return
    
    print(f"\n📚 DOCUMENTATION-FIRST DEVELOPMENT ENFORCED")
    print(f"   Component detected: {component_name}")
    
    # Generate documentation
    generator = DocumentationGenerator()
    info = generator.extract_component_info(content, path)
    
    # Generate component documentation
    docs_content = generator.generate_component_docs(info, content)
    docs_path = Path(f'docs/components/{component_name}.md')
    docs_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(docs_path, 'w') as f:
        f.write(docs_content)
    
    print(f"✅ Generated documentation: {docs_path}")
    
    # Generate Storybook story
    story_content = generator.generate_storybook_story(info)
    story_path = Path(f'stories/{component_name}.stories.tsx')
    story_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(story_path, 'w') as f:
        f.write(story_content)
    
    print(f"✅ Generated Storybook story: {story_path}")
    
    print("\n📝 Next steps:")
    print(f"1. Review and enhance the documentation")
    print(f"2. Add specific examples to Storybook")
    print(f"3. Run: pnpm storybook")
    
    # Suggest documentation improvements
    if not info['props']:
        print("\n⚠️  No props detected. Consider adding TypeScript interfaces.")
    
    if not info['description']:
        print("⚠️  Add a description comment above the component.")

if __name__ == "__main__":
    tool_use_data = json.loads(os.environ.get('TOOL_USE', '{}'))
    
    class ToolUse:
        def __init__(self, data):
            for key, value in data.items():
                setattr(self, key, value)
    
    tool_use = ToolUse(tool_use_data)
    main(tool_use)
