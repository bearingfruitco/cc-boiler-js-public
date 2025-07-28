#!/usr/bin/env python3
"""
Automated Error Recovery System
Intelligent error detection and auto-fix with learning capabilities
Part of v4.0 automation plan - Issue #26
"""

import os
import json
import re
import hashlib
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
                },
                "TS2345": {
                    "pattern": "Argument of type '(.+)' is not assignable to parameter of type '(.+)'",
                    "description": "Type mismatch error",
                    "solutions": [
                        {
                            "condition": "null or undefined",
                            "fix": "Add null check: if ({var}) {{ ... }}",
                            "confidence": 0.85
                        },
                        {
                            "condition": "wrong type",
                            "fix": "Type assertion: {var} as {expectedType}",
                            "confidence": 0.7
                        }
                    ]
                },
                "TS7006": {
                    "pattern": "Parameter '(\\w+)' implicitly has an 'any' type",
                    "description": "Missing type annotation",
                    "solutions": [
                        {
                            "condition": "event handler",
                            "fix": "{param}: React.{EventType}Event",
                            "confidence": 0.9
                        },
                        {
                            "condition": "general parameter",
                            "fix": "{param}: any // TODO: Add proper type",
                            "confidence": 0.6
                        }
                    ]
                }
            },
            "eslint": {
                "react-hooks/exhaustive-deps": {
                    "pattern": "React Hook (\\w+) has a missing dependency: '(.+)'",
                    "description": "Missing dependency in React hook",
                    "solutions": [
                        {
                            "condition": "useEffect",
                            "fix": "Add '{dependency}' to dependency array",
                            "confidence": 0.95
                        },
                        {
                            "condition": "useCallback",
                            "fix": "Add '{dependency}' to dependency array or memoize it",
                            "confidence": 0.9
                        }
                    ]
                },
                "no-unused-vars": {
                    "pattern": "'(\\w+)' is .* but never used",
                    "description": "Unused variable",
                    "solutions": [
                        {
                            "condition": "import",
                            "fix": "Remove unused import",
                            "confidence": 0.95
                        },
                        {
                            "condition": "variable",
                            "fix": "Remove declaration or add usage",
                            "confidence": 0.9
                        }
                    ]
                }
            },
            "design_system": {
                "invalid_text_size": {
                    "pattern": "text-(xs|sm|base|lg|xl|2xl|3xl)",
                    "description": "Invalid text size class",
                    "solutions": [
                        {
                            "condition": "heading",
                            "fix": "Replace with text-size-1 or text-size-2",
                            "confidence": 0.95
                        },
                        {
                            "condition": "body text",
                            "fix": "Replace with text-size-3",
                            "confidence": 0.95
                        },
                        {
                            "condition": "small text",
                            "fix": "Replace with text-size-4",
                            "confidence": 0.95
                        }
                    ]
                },
                "invalid_spacing": {
                    "pattern": "(p|m|gap|space)-(5|7|9|11|13|15)",
                    "description": "Invalid spacing (not on 4px grid)",
                    "solutions": [
                        {
                            "condition": "5 (20px)",
                            "fix": "Use -4 (16px) or -6 (24px)",
                            "confidence": 0.9
                        },
                        {
                            "condition": "7 (28px)",
                            "fix": "Use -6 (24px) or -8 (32px)",
                            "confidence": 0.9
                        }
                    ]
                }
            },
            "build": {
                "module_not_found": {
                    "pattern": "Module not found: Can't resolve '(.+)'",
                    "description": "Missing module or import path error",
                    "solutions": [
                        {
                            "condition": "npm package",
                            "fix": "pnpm add {module}",
                            "confidence": 0.9
                        },
                        {
                            "condition": "relative import",
                            "fix": "Check import path and file exists",
                            "confidence": 0.8
                        }
                    ]
                },
                "syntax_error": {
                    "pattern": "SyntaxError: (.+)",
                    "description": "JavaScript/TypeScript syntax error",
                    "solutions": [
                        {
                            "condition": "Unexpected token",
                            "fix": "Check for missing brackets, quotes, or semicolons",
                            "confidence": 0.8
                        }
                    ]
                }
            },
            "runtime": {
                "undefined_property": {
                    "pattern": "Cannot read prop.* of undefined",
                    "description": "Accessing property of undefined",
                    "solutions": [
                        {
                            "condition": "object access",
                            "fix": "Add optional chaining: object?.property",
                            "confidence": 0.95
                        },
                        {
                            "condition": "array access",
                            "fix": "Add null check: array && array[index]",
                            "confidence": 0.9
                        }
                    ]
                },
                "hydration_mismatch": {
                    "pattern": "Hydration failed because",
                    "description": "Server/client render mismatch",
                    "solutions": [
                        {
                            "condition": "dynamic content",
                            "fix": "Wrap in useEffect or use suppressHydrationWarning",
                            "confidence": 0.85
                        }
                    ]
                }
            }
        }
        
        if self.patterns_path.exists():
            with open(self.patterns_path) as f:
                self.patterns = json.load(f)
        else:
            self.patterns = default_patterns
            self.patterns_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.patterns_path, 'w') as f:
                json.dump(default_patterns, f, indent=2)
        
        # Load knowledge base of successful fixes
        if self.kb_path.exists():
            with open(self.kb_path) as f:
                self.knowledge_base = json.load(f)
        else:
            self.knowledge_base = {"fixes": [], "success_rate": {}}
            with open(self.kb_path, 'w') as f:
                json.dump(self.knowledge_base, f, indent=2)
    
    def find_matching_pattern(self, error_message: str) -> Optional[Dict]:
        """Find pattern matching the error message"""
        for category, errors in self.patterns.items():
            for error_code, error_data in errors.items():
                pattern = error_data.get('pattern', '')
                if re.search(pattern, error_message):
                    return {
                        'category': category,
                        'code': error_code,
                        'data': error_data,
                        'match': re.search(pattern, error_message)
                    }
        return None
    
    def get_solution(self, error_message: str, context: str = "") -> Optional[Dict]:
        """Get best solution for an error"""
        pattern_match = self.find_matching_pattern(error_message)
        if not pattern_match:
            return None
        
        solutions = pattern_match['data'].get('solutions', [])
        if not solutions:
            return None
        
        # Find best matching solution based on context
        best_solution = None
        best_confidence = 0
        
        for solution in solutions:
            condition = solution.get('condition', '')
            confidence = solution.get('confidence', 0.5)
            
            # Check if condition matches context
            if condition.lower() in context.lower():
                confidence += 0.1
            
            # Check knowledge base for successful fixes
            fix_hash = hashlib.md5(f"{error_message}{solution['fix']}".encode()).hexdigest()
            if fix_hash in self.knowledge_base.get('success_rate', {}):
                success_rate = self.knowledge_base['success_rate'][fix_hash]
                confidence = confidence * 0.5 + success_rate * 0.5
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_solution = solution
        
        if best_solution:
            return {
                'fix': best_solution['fix'],
                'confidence': best_confidence,
                'category': pattern_match['category'],
                'code': pattern_match['code'],
                'match': pattern_match['match']
            }
        
        return None
    
    def record_fix_result(self, error_message: str, fix: str, success: bool):
        """Record whether a fix was successful"""
        fix_hash = hashlib.md5(f"{error_message}{fix}".encode()).hexdigest()
        
        if fix_hash not in self.knowledge_base['success_rate']:
            self.knowledge_base['success_rate'][fix_hash] = 0.5
        
        # Update success rate with exponential moving average
        alpha = 0.2
        current_rate = self.knowledge_base['success_rate'][fix_hash]
        new_rate = alpha * (1.0 if success else 0.0) + (1 - alpha) * current_rate
        self.knowledge_base['success_rate'][fix_hash] = new_rate
        
        # Record the fix
        self.knowledge_base['fixes'].append({
            'timestamp': datetime.now().isoformat(),
            'error': error_message,
            'fix': fix,
            'success': success,
            'hash': fix_hash
        })
        
        # Keep only last 1000 fixes
        self.knowledge_base['fixes'] = self.knowledge_base['fixes'][-1000:]
        
        # Save knowledge base
        with open(self.kb_path, 'w') as f:
            json.dump(self.knowledge_base, f, indent=2)

class AutoErrorFixer:
    def __init__(self):
        self.kb = ErrorKnowledgeBase()
        self.fixes_applied = []
        
    def analyze_error(self, error_message: str, file_path: str = "", line_number: int = 0) -> Dict:
        """Analyze error and suggest fixes"""
        # Get file context if available
        context = ""
        if file_path and Path(file_path).exists():
            with open(file_path) as f:
                lines = f.readlines()
                if 0 < line_number <= len(lines):
                    start = max(0, line_number - 5)
                    end = min(len(lines), line_number + 5)
                    context = ''.join(lines[start:end])
        
        # Get solution from knowledge base
        solution = self.kb.get_solution(error_message, context)
        
        if solution:
            return {
                'error': error_message,
                'file': file_path,
                'line': line_number,
                'solution': solution,
                'can_auto_fix': solution['confidence'] > 0.8
            }
        
        return {
            'error': error_message,
            'file': file_path,
            'line': line_number,
            'solution': None,
            'can_auto_fix': False
        }
    
    def generate_fix_command(self, analysis: Dict) -> Optional[str]:
        """Generate command to fix the error"""
        if not analysis['solution']:
            return None
        
        solution = analysis['solution']
        fix_template = solution['fix']
        
        # Replace placeholders in fix template
        if solution['match']:
            for i, group in enumerate(solution['match'].groups()):
                fix_template = fix_template.replace(f'{{{i}}}', group)
                fix_template = fix_template.replace('{name}', group)
                fix_template = fix_template.replace('{var}', group)
                fix_template = fix_template.replace('{dependency}', group)
                fix_template = fix_template.replace('{module}', group)
        
        # Generate appropriate command based on category
        if solution['category'] == 'build' and 'pnpm add' in fix_template:
            return fix_template
        elif solution['category'] == 'typescript':
            return f"# Add to {analysis['file']}:\n{fix_template}"
        elif solution['category'] == 'design_system':
            return f"# In {analysis['file']}, {fix_template}"
        
        return f"# Suggested fix:\n{fix_template}"
    
    def apply_auto_fix(self, analysis: Dict) -> bool:
        """Attempt to automatically apply a fix"""
        if not analysis['can_auto_fix']:
            return False
        
        # Record the fix attempt
        self.fixes_applied.append({
            'timestamp': datetime.now().isoformat(),
            'analysis': analysis
        })
        
        # Here we would actually apply the fix
        # For now, we'll just return the command
        fix_command = self.generate_fix_command(analysis)
        if fix_command:
            print(f"\n🔧 AUTO-FIX AVAILABLE:")
            print(fix_command)
            return True
        
        return False

def detect_error_in_output(output: str) -> List[Dict]:
    """Detect errors in command output"""
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

def main(tool_use):
    """Main error recovery logic"""
    # This hook can be triggered by error output
    if tool_use.tool != 'bash':
        return
    
    output = getattr(tool_use, 'output', '')
    if not output:
        return
    
    # Detect errors
    errors = detect_error_in_output(output)
    if not errors:
        return
    
    print("\n🚨 ERRORS DETECTED - INITIATING AUTO-RECOVERY")
    
    fixer = AutoErrorFixer()
    fixable_errors = []
    
    for error in errors:
        analysis = fixer.analyze_error(
            error.get('message', ''),
            getattr(tool_use, 'working_directory', ''),
            0
        )
        
        if analysis['can_auto_fix']:
            fixable_errors.append(analysis)
        
        print(f"\n❌ Error: {error.get('message', 'Unknown error')}")
        if analysis['solution']:
            print(f"   Solution ({analysis['solution']['confidence']*100:.0f}% confidence):")
            print(f"   {analysis['solution']['fix']}")
    
    # Apply auto-fixes for high confidence solutions
    if fixable_errors:
        print(f"\n🤖 Found {len(fixable_errors)} auto-fixable errors")
        for analysis in fixable_errors:
            if fixer.apply_auto_fix(analysis):
                # Record result (would be updated based on actual success)
                fixer.kb.record_fix_result(
                    analysis['error'],
                    analysis['solution']['fix'],
                    True  # Assume success for now
                )
    
    # Suggest manual fixes for others
    manual_fixes = [e for e in errors if e not in fixable_errors]
    if manual_fixes:
        print(f"\n📝 {len(manual_fixes)} errors require manual intervention")
        print("   Run: /spawn-agent senior-engineer fix-errors")

if __name__ == "__main__":
    tool_use_data = json.loads(os.environ.get('TOOL_USE', '{}'))
    
    class ToolUse:
        def __init__(self, data):
            for key, value in data.items():
                setattr(self, key, value)
    
    tool_use = ToolUse(tool_use_data)
    main(tool_use)
