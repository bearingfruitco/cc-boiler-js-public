#!/usr/bin/env python3
"""
Completion Verifier Hook - Enhances TDD workflow by verifying completion claims
Works with existing test-auto-runner and TDD enforcer
Follows official Claude Code PostToolUse hook format
"""

import json
import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime

# Completion claim patterns
COMPLETION_PHRASES = [
    "implementation complete",
    "feature is now complete", 
    "successfully implemented",
    "done implementing",
    "finished implementing",
    "✅ completed",
    "task completed",
    "finished the task",
    "all done",
    "implementation is complete"
]

def main():
    try:
        # Read input from stdin as per official docs
        input_data = json.loads(sys.stdin.read())
        
        # Extract fields for PostToolUse
        session_id = input_data.get('session_id')
        tool_name = input_data.get('tool_name')
        tool_input = input_data.get('tool_input', {})
        tool_response = input_data.get('tool_result', {})
        
        # Only check Write and Edit operations that might contain completion claims
        # There is no 'Respond' tool in the official spec
        # We should check the actual content being written/edited instead
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            sys.exit(0)
        
        # Get the content being written/edited
        # This would contain completion claims in comments or documentation
        response_text = tool_input.get('content', tool_input.get('new_str', ''))
        
        # Check if this is a completion claim
        if not detect_completion_claim(response_text):
            sys.exit(0)
        
        # Extract context about what was claimed complete
        context = extract_completion_context(response_text, session_id)
        
        # Load verification manifest
        manifest = load_verification_manifest()
        
        # Run TDD-focused verification
        verification_result = run_tdd_verification(context, manifest)
        
        # Update manifest
        update_verification_manifest(manifest, context, verification_result)
        
        if not verification_result['passed']:
            # Use info message to guide TDD workflow
            message = format_tdd_guidance(verification_result, context)
            
            # Print to stdout for transcript visibility
            print(message)
            
        else:
            # Log successful verification
            success_msg = f"✅ TDD Verification Complete: {context['feature']}\n"
            success_msg += f"   • Tests: {verification_result['test_count']} passing\n"
            success_msg += f"   • Coverage: {verification_result.get('coverage', 'N/A')}\n"
            print(success_msg)
            
        # PostToolUse hooks just exit normally
        sys.exit(0)
        
    except Exception as e:
        # Non-blocking error - use exit code 1
        print(f"Completion verifier error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Non-blocking error

def detect_completion_claim(text):
    """Check if the text contains a completion claim."""
    if not text:
        return False
    
    text_lower = text.lower()
    return any(phrase in text_lower for phrase in COMPLETION_PHRASES)

def extract_completion_context(text, session_id):
    """Extract what feature/task was claimed complete."""
    
    # Try to extract feature name from text
    feature_patterns = [
        r"(?:feature|task|implementation of|implemented)\s+['\"]?([a-zA-Z0-9-_]+)['\"]?",
        r"([a-zA-Z0-9-_]+)\s+(?:is now complete|has been implemented)",
        r"✅\s+([a-zA-Z0-9-_]+)",
        r"Task\s+(\d+\.\d+)",  # Task numbers like 2.3
    ]
    
    feature = None
    task_number = None
    
    for pattern in feature_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if 'Task' in pattern:
                task_number = match.group(1)
            else:
                feature = match.group(1)
            break
    
    # If no feature found, try to get from current file
    if not feature:
        try:
            # Check recently modified files
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD~1..HEAD'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout:
                files = result.stdout.strip().split('\n')
                for file in files:
                    if 'components/' in file or 'lib/' in file:
                        feature = Path(file).stem
                        break
        except:
            pass
    
    return {
        'feature': feature or 'unknown',
        'task_number': task_number,
        'session_id': session_id,
        'timestamp': datetime.now().isoformat(),
        'claim_text': text[:200]  # First 200 chars
    }

def load_verification_manifest():
    """Load the verification manifest."""
    manifest_path = Path('.claude/verification-manifest.json')
    
    if manifest_path.exists():
        with open(manifest_path) as f:
            return json.load(f)
    
    # Create default manifest
    return {
        "verification_rules": {
            "require_tests": True,
            "require_passing_tests": True,
            "require_typescript_check": True
        },
        "feature_verifications": {},
        "task_verifications": {},
        "tdd_metrics": {
            "tests_written_first": 0,
            "tests_written_after": 0,
            "completion_claims_verified": 0,
            "completion_claims_failed": 0
        }
    }

def run_tdd_verification(context, manifest):
    """Run TDD-focused verification checks."""
    
    feature = context['feature']
    results = {
        'feature': feature,
        'passed': True,
        'checks': [],
        'test_count': 0,
        'coverage': None
    }
    
    # Check 1: Do tests exist? (TDD requires tests first)
    test_check = check_tests_exist(feature)
    results['checks'].append(test_check)
    if not test_check['passed']:
        results['passed'] = False
        return results  # No point continuing without tests
    
    # Check 2: Run the tests
    test_run = run_feature_tests(feature, test_check['files'])
    results['checks'].append(test_run)
    results['test_count'] = test_run.get('test_count', 0)
    if not test_run['passed']:
        results['passed'] = False
    
    # Check 3: Quick TypeScript check
    ts_check = check_typescript_for_feature(feature)
    results['checks'].append(ts_check)
    if not ts_check['passed']:
        results['passed'] = False
    
    # Check 4: Test coverage if available
    coverage_check = check_test_coverage(feature)
    if coverage_check:
        results['checks'].append(coverage_check)
        results['coverage'] = coverage_check.get('coverage_percent')
    
    return results

def check_tests_exist(feature):
    """Check if test files exist for the feature."""
    
    test_patterns = [
        f"**/*{feature}*.test.tsx",
        f"**/*{feature}*.test.ts",
        f"**/*{feature}*.spec.tsx",
        f"**/*{feature}*.spec.ts",
        f"**/__tests__/*{feature}*"
    ]
    
    test_files = []
    for pattern in test_patterns:
        test_files.extend(Path(".").glob(pattern))
    
    # Check if tests were written before implementation (TDD)
    tests_first = False
    if test_files:
        # Simple heuristic: check if test file is older than implementation
        impl_files = list(Path(".").glob(f"**/{feature}.tsx")) + \
                    list(Path(".").glob(f"**/{feature}.ts"))
        
        if impl_files and test_files:
            test_mtime = min(f.stat().st_mtime for f in test_files)
            impl_mtime = min(f.stat().st_mtime for f in impl_files)
            tests_first = test_mtime < impl_mtime
    
    return {
        'name': 'Test Files',
        'passed': len(test_files) > 0,
        'message': f"Found {len(test_files)} test files" if test_files else "No test files found",
        'files': [str(f) for f in test_files[:3]],
        'tdd_compliant': tests_first
    }

def run_feature_tests(feature, test_files):
    """Run tests for the feature."""
    if not test_files:
        return {
            'name': 'Test Execution',
            'passed': False,
            'message': 'No tests to run'
        }
    
    try:
        # Run tests for this feature
        test_file = test_files[0]  # Use first test file
        
        result = subprocess.run(
            ['npm', 'test', str(test_file), '--', '--run'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        passed = result.returncode == 0
        
        # Extract test count
        test_count = 0
        if passed:
            # Look for test count in output
            count_match = re.search(r'(\d+)\s+pass(?:ing|ed)', result.stdout)
            if count_match:
                test_count = int(count_match.group(1))
        
        return {
            'name': 'Test Execution',
            'passed': passed,
            'message': f"{test_count} tests passed" if passed else "Tests failed",
            'test_count': test_count,
            'output': result.stdout[:500] if not passed else None
        }
    except Exception as e:
        return {
            'name': 'Test Execution',
            'passed': False,
            'message': f"Test execution error: {str(e)}"
        }

def check_typescript_for_feature(feature):
    """Run TypeScript check for files related to feature."""
    try:
        # Find implementation files
        impl_files = list(Path(".").glob(f"**/{feature}.tsx")) + \
                    list(Path(".").glob(f"**/{feature}.ts"))
        
        if not impl_files:
            return {
                'name': 'TypeScript',
                'passed': True,
                'message': 'No TypeScript files to check'
            }
        
        # Run tsc on specific files
        result = subprocess.run(
            ['npx', 'tsc', '--noEmit'] + [str(f) for f in impl_files],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        passed = result.returncode == 0
        
        return {
            'name': 'TypeScript',
            'passed': passed,
            'message': 'No TypeScript errors' if passed else 'TypeScript errors found'
        }
    except:
        # TypeScript check is non-critical
        return {
            'name': 'TypeScript',
            'passed': True,
            'message': 'TypeScript check skipped'
        }

def check_test_coverage(feature):
    """Check test coverage if available."""
    try:
        # Look for recent coverage report
        coverage_file = Path('coverage/coverage-summary.json')
        if not coverage_file.exists():
            return None
        
        # Check if file is recent (within last hour)
        if (datetime.now().timestamp() - coverage_file.stat().st_mtime) > 3600:
            return None
        
        with open(coverage_file) as f:
            coverage_data = json.load(f)
        
        # Find coverage for this feature
        for file_path, data in coverage_data.items():
            if feature in file_path:
                coverage_percent = data.get('lines', {}).get('pct', 0)
                return {
                    'name': 'Test Coverage',
                    'passed': coverage_percent >= 70,  # 70% threshold
                    'message': f"Coverage: {coverage_percent}%",
                    'coverage_percent': coverage_percent
                }
        
        return None
    except:
        return None

def update_verification_manifest(manifest, context, result):
    """Update the verification manifest with results."""
    feature = context['feature']
    
    # Update feature verifications
    if feature != 'unknown':
        manifest['feature_verifications'][feature] = {
            'last_verified': context['timestamp'],
            'verification_result': result['passed'],
            'test_count': result['test_count'],
            'coverage': result.get('coverage'),
            'checks': result['checks']
        }
    
    # Update task verifications if task number present
    if context.get('task_number'):
        manifest['task_verifications'][context['task_number']] = {
            'verified': result['passed'],
            'timestamp': context['timestamp'],
            'feature': feature
        }
    
    # Update TDD metrics
    metrics = manifest.get('tdd_metrics', {})
    metrics['completion_claims_verified'] = metrics.get('completion_claims_verified', 0) + (1 if result['passed'] else 0)
    metrics['completion_claims_failed'] = metrics.get('completion_claims_failed', 0) + (0 if result['passed'] else 1)
    
    # Check if tests were written first
    for check in result['checks']:
        if check['name'] == 'Test Files' and check.get('tdd_compliant'):
            metrics['tests_written_first'] = metrics.get('tests_written_first', 0) + 1
    
    manifest['tdd_metrics'] = metrics
    
    # Save manifest
    manifest_path = Path('.claude/verification-manifest.json')
    manifest_path.parent.mkdir(exist_ok=True)
    
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

def format_tdd_guidance(result, context):
    """Format TDD-focused guidance for failed verification."""
    
    feature = context['feature']
    task = context.get('task_number', '')
    
    message = f"\n📋 TDD Verification Check for {feature}"
    if task:
        message += f" (Task {task})"
    message += "\n\n"
    
    # Check which step failed
    no_tests = False
    tests_failed = False
    ts_errors = False
    
    for check in result['checks']:
        if check['name'] == 'Test Files' and not check['passed']:
            no_tests = True
        elif check['name'] == 'Test Execution' and not check['passed']:
            tests_failed = True
        elif check['name'] == 'TypeScript' and not check['passed']:
            ts_errors = True
    
    if no_tests:
        message += "❌ No tests found - TDD requires tests first!\n\n"
        message += "Follow the TDD workflow:\n"
        message += f"1. Create test: /test {feature}\n"
        message += "2. Write failing tests\n"
        message += "3. Run tests to see them fail\n"
        message += "4. Implement to make tests pass\n"
        message += f"5. Run: /verify {feature}\n"
    
    elif tests_failed:
        message += "⚠️  Tests are failing - implementation incomplete\n\n"
        message += "TDD workflow status:\n"
        message += "✅ Tests exist (good!)\n"
        message += "❌ Tests not passing\n\n"
        message += "Next steps:\n"
        message += f"1. Run tests: npm test {feature}.test\n"
        message += "2. Fix failing tests\n"
        message += "3. Ensure all tests green\n"
        message += f"4. Run: /verify {feature}\n"
        
        if result['checks'][1].get('output'):
            message += "\nTest output:\n"
            message += result['checks'][1]['output'][:300] + "...\n"
    
    elif ts_errors:
        message += "⚠️  TypeScript errors detected\n\n"
        message += "Fix TypeScript errors:\n"
        message += f"1. Run: npm run typecheck\n"
        message += "2. Fix type errors\n"
        message += f"3. Run: /verify {feature}\n"
    
    else:
        message += "✅ Basic checks passed\n"
        message += f"   • Tests: {result.get('test_count', 0)} passing\n"
        if result.get('coverage'):
            message += f"   • Coverage: {result['coverage']}%\n"
    
    # Add TDD best practice reminder
    message += "\n💡 TDD Best Practice: Write tests first, then implement!\n"
    
    return message

if __name__ == "__main__":
    main()
