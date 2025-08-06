#!/usr/bin/env python3
"""
Comprehensive hook review - check ALL hooks for official compliance.
"""

import os
import json
from pathlib import Path
from collections import defaultdict

def check_hook_compliance(file_path):
    """Check if a hook follows official Claude Code format."""
    
    compliance = {
        "file": file_path.name,
        "path": str(file_path),
        "issues": []
    }
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check Python syntax first
        try:
            compile(content, file_path, 'exec')
            compliance["syntax_valid"] = True
        except SyntaxError as e:
            compliance["syntax_valid"] = False
            compliance["issues"].append(f"Syntax error at line {e.lineno}: {e.msg}")
            return compliance
        
        # Check for official format indicators
        
        # 1. Should read from stdin
        if 'sys.stdin.read()' in content:
            compliance["reads_stdin"] = True
        else:
            compliance["reads_stdin"] = False
            compliance["issues"].append("Does not read from sys.stdin")
        
        # 2. Should parse JSON
        if 'json.loads' in content:
            compliance["parses_json"] = True
        else:
            compliance["parses_json"] = False
            compliance["issues"].append("Does not parse JSON")
        
        # 3. Should use official field names
        if 'tool_name' in content:
            compliance["has_tool_name"] = True
        else:
            compliance["has_tool_name"] = False
            compliance["issues"].append("Missing 'tool_name' field")
            
        if 'tool_input' in content:
            compliance["has_tool_input"] = True
        else:
            compliance["has_tool_input"] = False
            compliance["issues"].append("Missing 'tool_input' field")
        
        # 4. Should NOT use old format
        if '"decision"' in content and '"block"' in content:
            compliance["uses_old_format"] = True
            compliance["issues"].append("Uses old {\"decision\": \"block\"} format instead of exit codes")
        else:
            compliance["uses_old_format"] = False
        
        # 5. Should use proper exit codes
        has_exit_0 = 'sys.exit(0)' in content
        has_exit_1 = 'sys.exit(1)' in content
        has_exit_2 = 'sys.exit(2)' in content
        
        if not any([has_exit_0, has_exit_1, has_exit_2]):
            compliance["issues"].append("No proper exit codes (should use 0, 1, or 2)")
        else:
            compliance["exit_codes"] = {
                "0": has_exit_0,
                "1": has_exit_1,
                "2": has_exit_2
            }
        
        # 6. Check tool name format
        if 'write_file' in content or 'edit_file' in content:
            compliance["issues"].append("Uses old tool names (write_file) instead of official (Write, Edit)")
        
        # Calculate compliance score
        compliance["score"] = sum([
            compliance.get("reads_stdin", False),
            compliance.get("parses_json", False),
            compliance.get("has_tool_name", False),
            compliance.get("has_tool_input", False),
            not compliance.get("uses_old_format", False),
            any([has_exit_0, has_exit_1, has_exit_2])
        ])
        
        compliance["compliant"] = len(compliance["issues"]) == 0
        
    except Exception as e:
        compliance["error"] = str(e)
        compliance["compliant"] = False
    
    return compliance

def review_all_hooks():
    """Review all hooks in the system."""
    
    base_dir = Path(".claude/hooks")
    
    hook_dirs = {
        "pre-tool-use": "PreToolUse - Can block operations",
        "post-tool-use": "PostToolUse - After operations",
        "user-prompt-submit": "UserPromptSubmit - When user submits",
        "session-start": "SessionStart - New/resumed session",
        "notification": "Notification - Awaiting input",
        "stop": "Stop - When Claude finishes",
        "sub-agent-stop": "SubAgentStop - When subagent finishes",
        "pre-compact": "PreCompact - Before compaction"
    }
    
    all_results = {}
    
    for dir_name, description in hook_dirs.items():
        dir_path = base_dir / dir_name
        if not dir_path.exists():
            continue
            
        print(f"\n{'=' * 80}")
        print(f"{dir_name.upper()} - {description}")
        print(f"{'=' * 80}")
        
        # Get all Python files (excluding backups)
        py_files = [f for f in dir_path.glob("*.py") 
                   if not any(ext in f.name for ext in ['.original', '.broken', '.backup', '.old', '.prefixbatch', '-FIXED', '-OFFICIAL'])]
        
        compliant_count = 0
        non_compliant = []
        
        for py_file in sorted(py_files):
            result = check_hook_compliance(py_file)
            
            if result.get("compliant"):
                compliant_count += 1
                print(f"✅ {py_file.name} - COMPLIANT")
            else:
                non_compliant.append(result)
                print(f"❌ {py_file.name} - NOT COMPLIANT (score: {result.get('score', 0)}/6)")
                if result.get("issues"):
                    for issue in result["issues"][:2]:  # Show first 2 issues
                        print(f"   - {issue}")
        
        print(f"\nSummary: {compliant_count}/{len(py_files)} compliant")
        
        all_results[dir_name] = {
            "total": len(py_files),
            "compliant": compliant_count,
            "non_compliant": non_compliant
        }
    
    # Overall summary
    print("\n" + "=" * 80)
    print("OVERALL COMPLIANCE SUMMARY")
    print("=" * 80)
    
    total_hooks = sum(r["total"] for r in all_results.values())
    total_compliant = sum(r["compliant"] for r in all_results.values())
    
    print(f"\nTotal hooks: {total_hooks}")
    print(f"Compliant: {total_compliant}")
    print(f"Non-compliant: {total_hooks - total_compliant}")
    print(f"Compliance rate: {total_compliant/total_hooks*100:.1f}%")
    
    print("\n🚨 CRITICAL ISSUES:")
    print("1. Most hooks use OLD format with {\"decision\": \"block\"} instead of exit codes")
    print("2. Most hooks check for 'write_file' instead of 'Write'")
    print("3. Many hooks don't read from stdin properly")
    print("4. Exit code usage is inconsistent")
    
    return all_results

if __name__ == "__main__":
    review_all_hooks()
