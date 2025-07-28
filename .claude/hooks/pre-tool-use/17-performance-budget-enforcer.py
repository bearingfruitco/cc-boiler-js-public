#!/usr/bin/env python3
"""
Performance Budget Enforcer
Real-time performance monitoring with budget enforcement
"""

import sys
import json
import re
from pathlib import Path

class PerformanceMonitor:
    def __init__(self):
        self.config_path = Path('.claude/performance-budgets.json')
        self.metrics_path = Path('.claude/metrics/performance.json')
        self.load_config()
        
    def load_config(self):
        """Load performance budgets from config"""
        default_config = {
            "budgets": {
                "bundle": {
                    "max_size_kb": 500,
                    "warning_size_kb": 400
                },
                "component_render": {
                    "max_ms": 50,
                    "warning_ms": 30
                },
                "api_response": {
                    "max_ms": 200,
                    "warning_ms": 100
                },
                "page_load": {
                    "max_ms": 3000,
                    "warning_ms": 2000
                }
            },
            "alerts": {
                "enabled": True,
                "slack_webhook": "",
                "email": ""
            }
        }
        
        if self.config_path.exists():
            with open(self.config_path) as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
    
    def check_component_size(self, content, path):
        """Check if component is within size budget"""
        size_kb = len(content.encode('utf-8')) / 1024
        budget = self.config['budgets']['bundle']
        
        if size_kb > budget['max_size_kb']:
            return {
                'status': 'error',
                'message': f"Component exceeds size budget: {size_kb:.1f}KB > {budget['max_size_kb']}KB",
                'suggestions': [
                    "Split into smaller components",
                    "Move styles to CSS modules",
                    "Lazy load heavy dependencies",
                    "Use dynamic imports"
                ]
            }
        elif size_kb > budget['warning_size_kb']:
            return {
                'status': 'warning',
                'message': f"Component approaching size limit: {size_kb:.1f}KB",
                'suggestions': ["Consider refactoring for better code splitting"]
            }
        
        return {'status': 'ok', 'size_kb': size_kb}
    
    def analyze_render_performance(self, content):
        """Analyze potential render performance issues"""
        issues = []
        
        # Check for performance anti-patterns
        patterns = {
            r'\.map\([^)]+\)\.map\(': "Nested .map() calls can be inefficient",
            r'useEffect\([^}]+\[\]\)': "Empty dependency array might cause memory leaks",
            r'JSON\.parse\(JSON\.stringify': "Inefficient deep cloning detected",
            r'forEach.*setState': "Multiple setState calls in loop",
            r'render.*\(\).*{[\s\S]*?render': "Nested render methods detected"
        }
        
        for pattern, message in patterns.items():
            if re.search(pattern, content):
                issues.append(message)
        
        return issues

def check_performance_impact(input_data):
    """Check if changes will impact performance"""
    tool_name = input_data.get('tool_name', '')
    if tool_name not in ['Write', 'Edit', 'MultiEdit']:
        return
    
    tool_input = input_data.get('tool_input', {})
    path = tool_input.get('path', '') or tool_input.get('file_path', '')
    
    # Skip non-component files
    if not (path.endswith('.tsx') or path.endswith('.ts')):
        return
    
    # Get content based on tool
    if tool_name == 'Write':
        content = tool_input.get('content', '')
    else:
        content = tool_input.get('new_str', '')
    
    if not content:
        return
    
    monitor = PerformanceMonitor()
    
    # Check component size
    size_check = monitor.check_component_size(content, path)
    if size_check['status'] == 'error':
        # Block with feedback
        print(json.dumps({
            "decision": "block",
            "message": f"""🚨 PERFORMANCE BUDGET EXCEEDED

{size_check['message']}

💡 Suggestions:
{chr(10).join(f'• {suggestion}' for suggestion in size_check['suggestions'])}

Please optimize the component before proceeding."""
        }))
        sys.exit(0)
    elif size_check['status'] == 'warning':
        print(f"⚠️  Performance Warning: {size_check['message']}", file=sys.stderr)
    
    # Analyze render performance
    issues = monitor.analyze_render_performance(content)
    if issues:
        print("\n⚡ Performance Issues Detected:", file=sys.stderr)
        for issue in issues:
            print(f"   - {issue}", file=sys.stderr)
        print("\n💡 Consider refactoring to improve performance.", file=sys.stderr)

def main():
    """Main hook logic"""
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        check_performance_impact(input_data)
        
    except Exception as e:
        # Log error to stderr and continue
        print(f"Performance budget hook error: {str(e)}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
