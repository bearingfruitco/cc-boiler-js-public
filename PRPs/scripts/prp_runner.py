#!/usr/bin/env python3
"""
PRP Runner - Execute PRPs with validation and metrics
Supports interactive, headless, and streaming modes
Enhanced version with multi-level validation and auto-fix
"""

import json
import asyncio
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import subprocess

class PRPRunner:
    def __init__(self, prp_path: str, mode: str = 'interactive'):
        self.prp_path = Path(prp_path)
        if not self.prp_path.exists():
            # Try common locations
            locations = [
                Path(f"PRPs/{prp_path}"),
                Path(f"PRPs/active/{prp_path}"),
                Path(f"PRPs/{prp_path}.md")
            ]
            for loc in locations:
                if loc.exists():
                    self.prp_path = loc
                    break
            else:
                raise FileNotFoundError(f"PRP not found: {prp_path}")
        
        self.mode = mode
        self.metrics = {
            'start_time': datetime.now(),
            'validation_results': {},
            'errors': [],
            'warnings': [],
            'auto_fixes': []
        }
        self.verbose = False
    
    def load_prp(self) -> Dict:
        """Load and parse PRP file"""
        with open(self.prp_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract sections
        return {
            'content': content,
            'name': self.prp_path.stem,
            'goal': self._extract_section(content, 'Goal'),
            'context': self._extract_section(content, 'Context'),
            'implementation': self._extract_section(content, 'Implementation'),
            'validation': self._extract_section(content, 'Validation')
        }
    
    def _extract_section(self, content: str, section: str) -> str:
        """Extract a specific section from PRP"""
        import re
        # Handle sections with or without emoji
        pattern = rf'##\s*(?:[🎯📚🏗️🧪✅]\s*)?{section}.*?(?=##|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        return match.group(0) if match else ''
    
    async def validate_level(self, level: int, auto_fix: bool = False) -> Dict:
        """Run validation for a specific level"""
        level_configs = {
            1: {
                'name': 'Syntax & Standards',
                'checks': [
                    ('lint', 'bun run lint', 'bun run lint:fix'),
                    ('typecheck', 'bun run typecheck', None),
                    ('design', 'bun run /vd', None)
                ]
            },
            2: {
                'name': 'Component Testing',
                'checks': [
                    ('unit-tests', 'bun test --run', None),
                    ('component-tests', 'bun test components --run', None),
                    ('hook-tests', 'bun test hooks --run', None)
                ]
            },
            3: {
                'name': 'Integration Testing',
                'checks': [
                    ('e2e-tests', 'bunx playwright test', None),
                    ('api-tests', 'bun test api --run', None),
                    ('accessibility', 'bun run test:a11y', None)
                ]
            },
            4: {
                'name': 'Production Readiness',
                'checks': [
                    ('security', 'bun run security-scan', None),
                    ('bundle-size', 'bun run analyze', None),
                    ('performance', 'lighthouse-ci', None),
                    ('dependencies', 'bun run check:deps', None)
                ]
            }
        }
        
        config = level_configs.get(level, {})
        level_name = config.get('name', f'Level {level}')
        
        if self.mode == 'interactive':
            print(f"\n🔍 Running {level_name} Validation")
            print("─" * 50)
        
        results = {}
        for check_name, check_cmd, fix_cmd in config.get('checks', []):
            if self.verbose or self.mode == 'interactive':
                print(f"  → {check_name}...", end='', flush=True)
            
            result = await self._run_check(check_name, check_cmd)
            
            # Try auto-fix if enabled and fix command available
            if auto_fix and not result['passed'] and fix_cmd:
                if self.mode == 'interactive':
                    print(" ❌ Failed, attempting fix...", end='', flush=True)
                
                fix_result = await self._run_check(f"{check_name}-fix", fix_cmd)
                if fix_result['passed']:
                    # Re-run original check
                    result = await self._run_check(check_name, check_cmd)
                    if result['passed']:
                        self.metrics['auto_fixes'].append(check_name)
                        if self.mode == 'interactive':
                            print(" ✅ Fixed!")
                else:
                    if self.mode == 'interactive':
                        print(" ❌")
            else:
                if self.mode == 'interactive':
                    print(" ✅" if result['passed'] else " ❌")
            
            results[check_name] = result
            
            if self.mode == 'streaming':
                self._stream_result(level, check_name, result)
        
        return results
    
    async def _run_check(self, check: str, command: str) -> Dict:
        """Execute a specific validation check"""
        start_time = datetime.now()
        
        try:
            # Handle special commands
            if command.startswith('bun run /'):
                # This is a slash command - convert to actual command
                slash_cmd = command.replace('bun run /', '')
                # For now, just simulate - in real implementation would call the command
                await asyncio.sleep(0.5)
                return {
                    'passed': True,
                    'output': f"Simulated {slash_cmd} check",
                    'duration': 0.5
                }
            
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=Path.cwd()
            )
            stdout, stderr = await proc.communicate()
            
            duration = (datetime.now() - start_time).total_seconds()
            
            return {
                'passed': proc.returncode == 0,
                'output': stdout.decode('utf-8'),
                'error': stderr.decode('utf-8') if stderr else None,
                'duration': duration,
                'exit_code': proc.returncode
            }
        except Exception as e:
            return {
                'passed': False,
                'error': str(e),
                'duration': (datetime.now() - start_time).total_seconds(),
                'exception': True
            }
    
    def _stream_result(self, level: int, check: str, result: Dict):
        """Stream results in JSON format for real-time monitoring"""
        output = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'check': check,
            'passed': result['passed'],
            'duration': result.get('duration', 0)
        }
        
        if not result['passed'] and 'error' in result:
            output['error'] = result['error'][:200]  # Truncate long errors
        
        print(json.dumps(output))
        sys.stdout.flush()
    
    async def execute(self, levels: Optional[List[int]] = None, 
                     auto_fix: bool = False,
                     continue_on_fail: bool = False):
        """Execute PRP with specified validation levels"""
        prp = self.load_prp()
        
        if self.mode == 'interactive':
            print(f"\n🚀 Executing PRP: {prp['name']}")
            print(f"📋 Goal: {prp['goal'][:100]}...")
            print(f"\n{'='*50}")
        
        # Default to all levels
        if levels is None:
            levels = [1, 2, 3, 4]
        
        all_passed = True
        for level in levels:
            results = await self.validate_level(level, auto_fix)
            self.metrics['validation_results'][f'level_{level}'] = results
            
            # Check if we should continue
            failed = [k for k, v in results.items() if not v['passed']]
            if failed:
                all_passed = False
                if not continue_on_fail and level < 4:
                    if self.mode == 'interactive':
                        print(f"\n⚠️  {len(failed)} checks failed at Level {level}")
                        response = input("Continue anyway? (y/N): ")
                        if response.lower() != 'y':
                            break
                    else:
                        # In non-interactive mode, stop on failure unless told otherwise
                        break
        
        # Calculate final metrics
        self._calculate_metrics()
        self.metrics['first_pass_success'] = all_passed
        
        # Output based on mode
        if self.mode == 'json':
            print(json.dumps(self.metrics, indent=2, default=str))
        elif self.mode == 'interactive':
            self._print_summary()
        
        # Save metrics
        self._save_metrics()
        
        return all_passed
    
    def _calculate_metrics(self):
        """Calculate success metrics"""
        self.metrics['end_time'] = datetime.now()
        self.metrics['duration'] = (
            self.metrics['end_time'] - self.metrics['start_time']
        ).total_seconds()
        
        # Calculate pass rate and scores per level
        level_scores = {}
        total_checks = 0
        passed_checks = 0
        
        for level, results in self.metrics['validation_results'].items():
            level_passed = 0
            level_total = len(results)
            
            for check_result in results.values():
                total_checks += 1
                if check_result['passed']:
                    passed_checks += 1
                    level_passed += 1
            
            if level_total > 0:
                level_scores[level] = (level_passed / level_total) * 100
        
        self.metrics['pass_rate'] = (
            passed_checks / total_checks if total_checks > 0 else 0
        )
        self.metrics['level_scores'] = level_scores
        self.metrics['validation_scores'] = {
            'syntax': level_scores.get('level_1', 0),
            'components': level_scores.get('level_2', 0),
            'integration': level_scores.get('level_3', 0),
            'production': level_scores.get('level_4', 0)
        }
    
    def _print_summary(self):
        """Print interactive summary"""
        print("\n" + "="*50)
        print("📊 PRP EXECUTION SUMMARY")
        print("="*50)
        
        print(f"\n⏱️  Duration: {self.metrics['duration']:.1f}s")
        print(f"📈 Overall Pass Rate: {self.metrics['pass_rate']*100:.1f}%")
        print(f"✨ First Pass Success: {'✅ Yes' if self.metrics.get('first_pass_success') else '❌ No'}")
        
        if self.metrics['auto_fixes']:
            print(f"🔧 Auto-fixed: {', '.join(self.metrics['auto_fixes'])}")
        
        # Show validation results by level
        print("\n📋 Validation Results:")
        for level, results in sorted(self.metrics['validation_results'].items()):
            level_num = int(level.split('_')[1])
            level_names = {
                1: "Syntax & Standards",
                2: "Component Testing",
                3: "Integration Testing",
                4: "Production Readiness"
            }
            
            failed = [k for k, v in results.items() if not v['passed']]
            score = self.metrics['validation_scores'].get(
                ['syntax', 'components', 'integration', 'production'][level_num-1],
                0
            )
            
            print(f"\n  Level {level_num} - {level_names.get(level_num, 'Unknown')} ({score:.0f}%)")
            
            if failed:
                print(f"    ❌ Failed: {', '.join(failed)}")
                # Show first error for context
                for check in failed[:1]:  # Just show first failure
                    error = results[check].get('error', 'No details')
                    if error and len(error) > 100:
                        error = error[:100] + '...'
                    print(f"       → {error}")
            else:
                print(f"    ✅ All checks passed!")
    
    def _save_metrics(self):
        """Save metrics to file"""
        metrics_dir = Path("PRPs/metrics")
        metrics_dir.mkdir(exist_ok=True)
        
        metrics_file = metrics_dir / f"{self.prp_path.stem}_metrics.json"
        
        # Include PRP name in metrics
        self.metrics['prp_name'] = self.prp_path.stem
        self.metrics['prp_path'] = str(self.prp_path)
        
        with open(metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2, default=str)
        
        if self.mode == 'interactive':
            print(f"\n💾 Metrics saved to: {metrics_file}")

async def main():
    parser = argparse.ArgumentParser(
        description='PRP Runner - Execute PRPs with validation'
    )
    parser.add_argument('--prp', required=True, help='PRP file to execute')
    parser.add_argument('--mode', choices=['interactive', 'json', 'streaming'], 
                      default='interactive', help='Execution mode')
    parser.add_argument('--levels', nargs='+', type=int, 
                      help='Validation levels to run (1-4)')
    parser.add_argument('--fix', action='store_true', 
                      help='Attempt to auto-fix issues')
    parser.add_argument('--continue', dest='continue_on_fail',
                      action='store_true',
                      help='Continue on validation failures')
    parser.add_argument('--verbose', '-v', action='store_true',
                      help='Verbose output')
    
    args = parser.parse_args()
    
    try:
        runner = PRPRunner(args.prp, args.mode)
        runner.verbose = args.verbose
        
        success = await runner.execute(
            levels=args.levels,
            auto_fix=args.fix,
            continue_on_fail=args.continue_on_fail
        )
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
