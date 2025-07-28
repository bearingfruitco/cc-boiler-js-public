#!/usr/bin/env python3
"""
Performance Budget Enforcer
Real-time performance monitoring with budget enforcement
"""

import os
import json
import time
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
    
    def generate_performance_overlay(self, metrics):
        """Generate performance overlay UI"""
        return f"""
// Add this performance overlay to your app
import {{ useEffect, useState }} from 'react';

export function PerformanceOverlay() {{
  const [metrics, setMetrics] = useState({json.dumps(metrics, indent=2)});
  const [show, setShow] = useState(true);
  
  useEffect(() => {{
    // Real-time performance monitoring
    const observer = new PerformanceObserver((list) => {{
      const entries = list.getEntries();
      entries.forEach((entry) => {{
        if (entry.entryType === 'measure') {{
          setMetrics(prev => ({{
            ...prev,
            [entry.name]: {{
              duration: entry.duration,
              alert: entry.duration > {self.config['budgets']['component_render']['warning_ms']}
            }}
          }}));
        }}
      }});
    }});
    
    observer.observe({{ entryTypes: ['measure'] }});
    return () => observer.disconnect();
  }}, []);
  
  if (!show) return null;
  
  return (
    <div className="fixed bottom-4 right-4 bg-black/90 text-white p-4 rounded-lg text-xs font-mono max-w-sm">
      <div className="flex justify-between items-center mb-2">
        <h3 className="font-bold">Performance Monitor</h3>
        <button onClick={{() => setShow(false)}} className="text-gray-400 hover:text-white">×</button>
      </div>
      <table className="w-full">
        <thead>
          <tr className="text-left">
            <th>Component</th>
            <th>Render</th>
            <th>Alert</th>
          </tr>
        </thead>
        <tbody>
          {{Object.entries(metrics).map(([name, data]) => (
            <tr key={{name}}>
              <td className="pr-2">{{name}}</td>
              <td className="pr-2">{{data.duration?.toFixed(1)}}ms</td>
              <td>{{data.alert ? '⚠️' : '✅'}}</td>
            </tr>
          ))}}
        </tbody>
      </table>
      <div className="mt-2 pt-2 border-t border-gray-700">
        <div>Bundle Size: {metrics.bundleSize || '---'}KB</div>
      </div>
    </div>
  );
}}
"""

def check_performance_impact(tool_use):
    """Check if changes will impact performance"""
    if tool_use.tool != 'str_replace_editor':
        return
    
    # Skip non-component files
    path = tool_use.path or ''
    if not (path.endswith('.tsx') or path.endswith('.ts')):
        return
    
    content = getattr(tool_use, 'new_str', '') or getattr(tool_use, 'content', '')
    if not content:
        return
    
    monitor = PerformanceMonitor()
    
    # Check component size
    size_check = monitor.check_component_size(content, path)
    if size_check['status'] == 'error':
        print(f"\n🚨 PERFORMANCE BUDGET EXCEEDED")
        print(f"   {size_check['message']}")
        print("\n💡 Suggestions:")
        for suggestion in size_check['suggestions']:
            print(f"   - {suggestion}")
        print("\n❌ Operation blocked. Please optimize before proceeding.")
        sys.exit(1)
    elif size_check['status'] == 'warning':
        print(f"\n⚠️  Performance Warning: {size_check['message']}")
    
    # Analyze render performance
    issues = monitor.analyze_render_performance(content)
    if issues:
        print("\n⚡ Performance Issues Detected:")
        for issue in issues:
            print(f"   - {issue}")
        print("\n💡 Consider refactoring to improve performance.")
    
    # Generate performance tracking code if needed
    if 'Component' in content and 'export' in content:
        print("\n📊 Adding performance tracking...")
        overlay_code = monitor.generate_performance_overlay({})
        
        # Save overlay component
        overlay_path = Path('components/dev/PerformanceOverlay.tsx')
        overlay_path.parent.mkdir(parents=True, exist_ok=True)
        with open(overlay_path, 'w') as f:
            f.write(overlay_code)
        
        print(f"✅ Performance overlay created: {overlay_path}")
        print("   Import and add <PerformanceOverlay /> to your app")

def main(tool_use):
    check_performance_impact(tool_use)

if __name__ == "__main__":
    import sys
    tool_use_data = json.loads(os.environ.get('TOOL_USE', '{}'))
    
    class ToolUse:
        def __init__(self, data):
            for key, value in data.items():
                setattr(self, key, value)
    
    tool_use = ToolUse(tool_use_data)
    main(tool_use)
