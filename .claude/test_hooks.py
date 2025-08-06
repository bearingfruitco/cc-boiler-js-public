#!/usr/bin/env python3
"""Test all hooks for Python syntax errors"""

import os
import py_compile
from pathlib import Path

def test_hooks():
    hooks_dir = Path('/Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks')
    
    results = {
        'passed': [],
        'failed': []
    }
    
    # Test all Python hooks
    for py_file in hooks_dir.rglob('*.py'):
        if '__pycache__' in str(py_file) or py_file.suffix == '.backup':
            continue
        
        try:
            py_compile.compile(str(py_file), doraise=True)
            results['passed'].append(str(py_file.name))
        except py_compile.PyCompileError as e:
            results['failed'].append(f"{py_file.name}: {str(e)}")
    
    # Print results
    print(f"✅ Passed: {len(results['passed'])} hooks")
    print(f"❌ Failed: {len(results['failed'])} hooks")
    
    if results['failed']:
        print("\nFailed hooks:")
        for failure in results['failed']:
            print(f"  - {failure}")
    
    return len(results['failed']) == 0

if __name__ == '__main__':
    success = test_hooks()
    exit(0 if success else 1)
