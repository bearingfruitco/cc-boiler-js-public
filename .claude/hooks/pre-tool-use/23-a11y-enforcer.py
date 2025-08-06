#!/usr/bin/env python3
"""
Accessibility-First Enforcer
Makes accessibility testing mandatory for all UI components
Part of v4.0 automation plan - Issue #23
"""

import sys
import json
import re
from pathlib import Path

class AccessibilityAnalyzer:
    def __init__(self):
        self.a11y_config_path = Path('.claude/a11y-config.json')
        self.load_config()
        
    def load_config(self):
        """Load accessibility configuration"""
        default_config = {
            "wcag_level": "AA",
            "required_tests": [
                "keyboard_navigation",
                "screen_reader",
                "color_contrast",
                "focus_management"
            ],
            "aria_requirements": {
                "interactive_elements": ["button", "a", "input", "select", "textarea"],
                "landmark_roles": ["main", "navigation", "complementary", "contentinfo"],
                "required_attributes": {
                    "img": ["alt"],
                    "input": ["label", "aria-label", "aria-labelledby"],
                    "button": ["aria-label", "text-content"]
                }
            },
            "minimum_scores": {
                "overall": 95,
                "keyboard": 100,
                "screen_reader": 95,
                "color_contrast": 90
            }
        }
        
        if self.a11y_config_path.exists():
            with open(self.a11y_config_path) as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.a11y_config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.a11y_config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
    
    def analyze_component(self, content, component_name):
        """Analyze component for accessibility issues"""
        issues = []
        suggestions = []
        score = 100
        
        # Check for interactive elements without proper ARIA
        interactive_issues = self._check_interactive_elements(content)
        issues.extend(interactive_issues['issues'])
        suggestions.extend(interactive_issues['suggestions'])
        score -= len(interactive_issues['issues']) * 5
        
        # Check for keyboard navigation
        keyboard_issues = self._check_keyboard_navigation(content)
        issues.extend(keyboard_issues['issues'])
        suggestions.extend(keyboard_issues['suggestions'])
        score -= len(keyboard_issues['issues']) * 10
        
        # Check for focus management
        focus_issues = self._check_focus_management(content)
        issues.extend(focus_issues['issues'])
        suggestions.extend(focus_issues['suggestions'])
        score -= len(focus_issues['issues']) * 5
        
        # Check for color contrast
        contrast_issues = self._check_color_contrast(content)
        issues.extend(contrast_issues['issues'])
        suggestions.extend(contrast_issues['suggestions'])
        score -= len(contrast_issues['issues']) * 3
        
        # Check for screen reader support
        sr_issues = self._check_screen_reader_support(content)
        issues.extend(sr_issues['issues'])
        suggestions.extend(sr_issues['suggestions'])
        score -= len(sr_issues['issues']) * 5
        
        return {
            'score': max(0, score),
            'issues': issues,
            'suggestions': suggestions,
            'passing': score >= self.config['minimum_scores']['overall']
        }
    
    def _check_interactive_elements(self, content):
        """Check interactive elements for proper ARIA attributes"""
        issues = []
        suggestions = []
        
        # Check buttons
        button_pattern = r'<button[^>]*>'
        buttons = re.findall(button_pattern, content)
        for button in buttons:
            if 'aria-label' not in button and not re.search(r'>\s*\w+', button):
                issues.append("Button without accessible label")
                suggestions.append("Add aria-label or text content to button")
        
        # Check links
        link_pattern = r'<a[^>]*>'
        links = re.findall(link_pattern, content)
        for link in links:
            if 'href' in link and 'aria-label' not in link:
                if not re.search(r'>\s*\w+', link):
                    issues.append("Link without accessible text")
                    suggestions.append("Add aria-label or text content to link")
        
        # Check images
        img_pattern = r'<img[^>]*>'
        images = re.findall(img_pattern, content)
        for img in images:
            if 'alt' not in img:
                issues.append("Image without alt text")
                suggestions.append("Add alt attribute to all images")
        
        # Check form inputs
        input_pattern = r'<input[^>]*>'
        inputs = re.findall(input_pattern, content)
        for input_tag in inputs:
            if 'aria-label' not in input_tag and 'aria-labelledby' not in input_tag:
                if 'id' not in input_tag:
                    issues.append("Input without accessible label")
                    suggestions.append("Add label with htmlFor or aria-label to input")
        
        return {'issues': issues, 'suggestions': suggestions}
    
    def _check_keyboard_navigation(self, content):
        """Check for keyboard navigation support"""
        issues = []
        suggestions = []
        
        # Check for onClick without keyboard handlers
        if 'onClick' in content:
            onclick_count = content.count('onClick')
            onkeydown_count = content.count('onKeyDown') + content.count('onKeyPress')
            
            if onclick_count > onkeydown_count:
                issues.append("Click handlers without keyboard support")
                suggestions.append("Add onKeyDown handlers for keyboard navigation")
        
        # Check for proper tab order
        if 'tabIndex' in content:
            # Check for positive tabIndex (bad practice)
            if re.search(r'tabIndex=["\']?[1-9]', content):
                issues.append("Positive tabIndex values detected")
                suggestions.append("Use tabIndex={0} or {-1}, avoid positive values")
        
        # Check for focus traps
        if 'focus' in content.lower() and 'blur' not in content:
            suggestions.append("Ensure focus can move freely (no focus traps)")
        
        return {'issues': issues, 'suggestions': suggestions}
    
    def _check_focus_management(self, content):
        """Check for proper focus management"""
        issues = []
        suggestions = []
        
        # Check for focus styles
        if 'focus:' not in content and 'focusVisible' not in content:
            issues.append("No focus styles detected")
            suggestions.append("Add focus:ring or focus:outline styles for keyboard users")
        
        # Check for focus restoration
        if 'Modal' in content or 'Dialog' in content:
            if 'focus' not in content.lower():
                issues.append("Modal/Dialog without focus management")
                suggestions.append("Implement focus trap and restoration for modals")
        
        return {'issues': issues, 'suggestions': suggestions}
    
    def _check_color_contrast(self, content):
        """Check for potential color contrast issues"""
        issues = []
        suggestions = []
        
        # Look for low contrast color combinations
        low_contrast_patterns = [
            (r'text-gray-[3-4]00.*bg-white', "Light gray text on white background"),
            (r'text-white.*bg-gray-[1-3]00', "White text on light background"),
            (r'text-yellow.*bg-white', "Yellow text on white background")
        ]
        
        for pattern, issue in low_contrast_patterns:
            if re.search(pattern, content):
                issues.append(f"Potential low contrast: {issue}")
                suggestions.append("Ensure 4.5:1 contrast ratio for normal text, 3:1 for large text")
        
        return {'issues': issues, 'suggestions': suggestions}
    
    def _check_screen_reader_support(self, content):
        """Check for screen reader support"""
        issues = []
        suggestions = []
        
        # Check for aria-live regions for dynamic content
        if 'setState' in content or 'useState' in content:
            if 'aria-live' not in content:
                suggestions.append("Consider aria-live regions for dynamic content updates")
        
        # Check for proper heading hierarchy
        heading_pattern = r'<h(\d)'
        headings = re.findall(heading_pattern, content)
        if headings:
            heading_levels = sorted([int(h) for h in headings])
            if heading_levels and heading_levels[0] != 1:
                issues.append("Heading hierarchy doesn't start with h1")
            
            # Check for skipped levels
            for i in range(1, len(heading_levels)):
                if heading_levels[i] - heading_levels[i-1] > 1:
                    issues.append("Skipped heading levels detected")
                    break
        
        # Check for landmark roles
        if len(content) > 500:  # Only for substantial components
            has_landmarks = any(role in content for role in ['role="main"', 'role="navigation"', '<main', '<nav'])
            if not has_landmarks:
                suggestions.append("Consider using landmark roles for better navigation")
        
        return {'issues': issues, 'suggestions': suggestions}
    
    def generate_a11y_tests(self, component_name):
        """Generate accessibility tests for component"""
        return f"""import {{ render, screen }} from '@testing-library/react';
import {{ axe, toHaveNoViolations }} from 'jest-axe';
import userEvent from '@testing-library/user-event';
import {{ {component_name} }} from './{component_name}';

expect.extend(toHaveNoViolations);

describe('{component_name} Accessibility', () => {{
  it('should not have any accessibility violations', async () => {{
    const {{ container }} = render(<{component_name} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  }});
  
  it('should be keyboard navigable', async () => {{
    const user = userEvent.setup();
    render(<{component_name} />);
    
    // Tab through interactive elements
    await user.tab();
    // Add specific keyboard navigation tests
  }});
  
  it('should have proper ARIA labels', () => {{
    render(<{component_name} />);
    
    // Check for accessible names
    const buttons = screen.getAllByRole('button');
    buttons.forEach(button => {{
      expect(button).toHaveAccessibleName();
    }});
  }});
  
  it('should manage focus properly', async () => {{
    const user = userEvent.setup();
    render(<{component_name} />);
    
    // Test focus management
    const firstElement = screen.getByRole('button');
    await user.click(firstElement);
    expect(firstElement).toHaveFocus();
  }});
  
  it('should support screen readers', () => {{
    render(<{component_name} />);
    
    // Check for proper heading hierarchy
    const headings = screen.getAllByRole('heading');
    // Add heading hierarchy tests
  }});
  
  it('should have sufficient color contrast', () => {{
    // This would typically be checked by axe
    // Add any specific contrast tests if needed
  }});
}});
"""

def check_for_ui_component(input_data):
    """Check if creating a UI component"""
    tool_name = input_data.get('tool_name', '')
    if tool_name not in ['Write', 'Edit', 'MultiEdit']:
        return False
    
    tool_input = input_data.get('tool_input', {})
    path = tool_input.get('path', '') or tool_input.get('file_path', '')
    
    # Check for React component patterns
    if not (path.endswith('.tsx') or path.endswith('.jsx')):
        return False
    
    # Get content based on tool
    if tool_name == 'Write':
        content = tool_input.get('content', '')
    else:
        content = tool_input.get('new_str', '')
    
    # Check for UI elements
    ui_patterns = ['<button', '<input', '<select', '<form', '<a ', 'onClick', 'className=']
    return any(pattern in content for pattern in ui_patterns)

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code via stdin
        input_data = json.loads(sys.stdin.read())
        
        if not check_for_ui_component(input_data):
            sys.exit(0)
        
        tool_input = input_data.get('tool_input', {})
        tool_name = input_data.get('tool_name', '')
        path = tool_input.get('path', '') or tool_input.get('file_path', '')
        
        # Get content based on tool type
        if tool_name == 'Write':
            content = tool_input.get('content', '')
        else:
            content = tool_input.get('new_str', '')
        
        component_name = Path(path).stem
        
        # Skip if opted out
        if '--no-a11y' in content:
            print("♿ Accessibility checks skipped (--no-a11y flag)", file=sys.stderr)
            sys.exit(0)
        
        print(f"\n♿ ACCESSIBILITY-FIRST DEVELOPMENT ENFORCED", file=sys.stderr)
        print(f"   Component: {component_name}", file=sys.stderr)
        
        analyzer = AccessibilityAnalyzer()
        
        # Analyze component
        analysis = analyzer.analyze_component(content, component_name)
        
        print(f"\n📊 Accessibility Score: {analysis['score']}/100", file=sys.stderr)
        
        if analysis['issues']:
            print("\n❌ Accessibility Issues Found:", file=sys.stderr)
            for issue in analysis['issues']:
                print(f"   - {issue}", file=sys.stderr)
        
        if analysis['suggestions']:
            print("\n💡 Suggestions:", file=sys.stderr)
            for suggestion in analysis['suggestions']:
                print(f"   - {suggestion}", file=sys.stderr)
        
        # Generate requirements
        requirements_content = f"""# Accessibility Requirements: {component_name}

## WCAG 2.1 Level {analyzer.config['wcag_level']} Compliance

### Issues Found
{chr(10).join(f'- {issue}' for issue in analysis['issues']) if analysis['issues'] else 'None'}

### Suggestions
{chr(10).join(f'- {suggestion}' for suggestion in analysis['suggestions']) if analysis['suggestions'] else 'None'}

### Score: {analysis['score']}/100
"""
        
        req_path = Path(f'.claude/a11y-requirements/{component_name}.md')
        req_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(req_path, 'w') as f:
            f.write(requirements_content)
        
        print(f"\n✅ Generated requirements: {req_path}", file=sys.stderr)
        
        # Generate tests
        tests = analyzer.generate_a11y_tests(component_name)
        test_path = Path(f'tests/a11y/{component_name}.a11y.test.tsx')
        test_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(test_path, 'w') as f:
            f.write(tests)
        
        print(f"✅ Generated tests: {test_path}", file=sys.stderr)
        
        # Block if score too low
        if not analysis['passing']:
            # Block the component creation with feedback using official format
            message = f"""♿ Accessibility Requirements Not Met

Component '{component_name}' needs accessibility improvements:

Score: {analysis['score']}/100 (minimum required: {analyzer.config['minimum_scores']['overall']})

Issues found:
{chr(10).join(f'• {issue}' for issue in analysis['issues'])}

Suggestions:
{chr(10).join(f'• {suggestion}' for suggestion in analysis['suggestions'])}

Would you like me to add the necessary accessibility features?"""
            print(message, file=sys.stderr)
            sys.exit(2)  # Block operation
        
        print("\n✅ Accessibility check passed! Component can be created.", file=sys.stderr)
        
    except Exception as e:
        # Log error to stderr and continue
        print(f"A11y enforcer hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
