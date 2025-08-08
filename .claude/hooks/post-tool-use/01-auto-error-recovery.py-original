#!/usr/bin/env python3
"""
Automated Error Recovery System
Intelligent error detection and auto-fix with learning capabilities
Part of v4.0 automation plan - Issue #26
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class ErrorKnowledgeBase:
    def __init__(self):
        self.kb_path = Path('.claude/error-knowledge-base.json')
        self.patterns_path = Path('.claude/error-patterns.json')
        self.load_knowledge_base()
        
    def load_knowledge_base(self):
        """Load error patterns and solutions"""
        default_patterns = {
            "typescript": {
                "TS2304": {
                    "pattern": "Cannot find name '(\\w+)'",
                    "description": "TypeScript cannot find a name/identifier",
                    "solutions": [
                        {
                            "condition": "React component",
                            "fix": "import {{ {name} }} from 'react';",
                            "confidence": 0.9
                        },
                        {
                            "condition": "Custom hook",
                            "fix": "import {{ {name} }} from '@/hooks/{name}';",
                            "confidence": 0.8
                        }
                    ]
                }
            }
        }
        
        if self.kb_path.exists():
            with open(self.kb_path) as f:
                self.patterns = json.load(f)
        else:
            self.patterns = default_patterns
            self.kb_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.kb_path, 'w') as f:
                json.dump(default_patterns, f, indent=2)

class AutoErrorFixer:
    def __init__(self):
        self.kb = ErrorKnowledgeBase()
        
    def analyze_error(self, error_message: str, context: str, line_number: int) -> Dict:
        """Analyze error and suggest fixes"""
        analysis = {
            'error': error_message,
            'context': context,
            'line': line_number,
            'can_auto_fix': False,
            'solution': None,
            'alternatives': []
        }
        
        # Check TypeScript errors
        ts_match = re.search(r'TS(\d+):', error_message)
        if ts_match:
            error_code = f"TS{ts_match.group(1)}"
            if error_code in self.kb.patterns.get('typescript', {}):
                pattern_info = self.kb.patterns['typescript'][error_code]
                analysis['solution'] = pattern_info['solutions'][0] if pattern_info['solutions'] else None
                analysis['can_auto_fix'] = analysis['solution'] is not None
        
        return analysis

def detect_error_in_output(output: str) -> List[Dict]:
    """Detect various types of errors in command output"""
    errors = []
    
    # TypeScript errors
    ts_pattern = r'(TS\d+):\s+(.+?)(?:\n|$)'
    for match in re.finditer(ts_pattern, output):
        errors.append({
            'type': 'typescript',
            'code': match.group(1),
            'message': match.group(2)
        })
    
    # ESLint errors
    eslint_pattern = r'(\d+:\d+)\s+error\s+(.+?)\s+(.+?)(?:\n|$)'
    for match in re.finditer(eslint_pattern, output):
        errors.append({
            'type': 'eslint',
            'location': match.group(1),
            'message': match.group(2),
            'rule': match.group(3)
        })
    
    # Build errors
    if 'Module not found' in output:
        module_pattern = r"Module not found: Can't resolve '(.+?)'"
        for match in re.finditer(module_pattern, output):
            errors.append({
                'type': 'build',
                'message': f"Module not found: Can't resolve '{match.group(1)}'",
                'module': match.group(1)
            })
    
    # Runtime errors
    if 'Error:' in output or 'TypeError:' in output:
        error_pattern = r'((?:Type)?Error):\s+(.+?)(?:\n|$)'
        for match in re.finditer(error_pattern, output):
            errors.append({
                'type': 'runtime',
                'message': f"{match.group(1)}: {match.group(2)}"
            })
    
    return errors

def main():
    """Main error recovery logic"""
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        tool_name = input_data.get('tool_name', '')
        # This hook only processes Bash tool results
        if tool_name != 'Bash':
            sys.exit(0)
        
        tool_output = input_data.get('tool_output', {})
        output = tool_output.get('stdout', '') + tool_output.get('stderr', '')
        
        if not output:
            sys.exit(0)
        
        # Detect errors
        errors = detect_error_in_output(output)
        if not errors:
            sys.exit(0)
        
        print("\n🚨 ERRORS DETECTED - INITIATING AUTO-RECOVERY", file=sys.stderr)
        
        fixer = AutoErrorFixer()
        fixable_errors = []
        
        for error in errors:
            analysis = fixer.analyze_error(
                error.get('message', ''),
                input_data.get('working_directory', ''),
                0
            )
            
            if analysis['can_auto_fix']:
                fixable_errors.append(analysis)
            
            print(f"\n❌ Error: {error.get('message', 'Unknown error')}", file=sys.stderr)
            if analysis['solution']:
                print(f"   Solution ({analysis['solution']['confidence']*100:.0f}% confidence):", file=sys.stderr)
                print(f"   {analysis['solution']['fix']}", file=sys.stderr)
        
        # Suggest fixes
        if fixable_errors:
            print(f"\n🤖 Found {len(fixable_errors)} auto-fixable errors", file=sys.stderr)
            print("   Run: /error-recovery to apply fixes", file=sys.stderr)
        
        # Suggest manual fixes for others
        manual_fixes = [e for e in errors if e not in fixable_errors]
        if manual_fixes:
            print(f"\n📝 {len(manual_fixes)} errors require manual intervention", file=sys.stderr)
            print("   Run: /spawn-agent senior-engineer fix-errors", file=sys.stderr)
        
        # PostToolUse hooks exit with 0 for success
        sys.exit(0)
        
    except Exception as e:
        # Non-blocking error - show to user but continue
        print(f"Auto error recovery hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Non-blocking error

if __name__ == "__main__":
    main()
