#!/usr/bin/env python3
"""
Manual hook-by-hook review tool.
Goes through each hook group and helps make decisions.
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

def test_hook_with_official_format(hook_path):
    """Test if a hook handles the official JSON format correctly."""
    test_cases = [
        {
            "name": "Write operation",
            "input": {
                "tool_name": "Write",
                "tool_input": {
                    "file_path": "test.ts",
                    "content": "console.log('test');"
                }
            }
        },
        {
            "name": "Edit operation",
            "input": {
                "tool_name": "Edit",
                "tool_input": {
                    "file_path": "test.ts",
                    "old_str": "old",
                    "new_str": "new"
                }
            }
        }
    ]
    
    results = []
    for test in test_cases:
        try:
            import subprocess
            import tempfile
            
            # Write test input to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(test["input"], f)
                temp_file = f.name
            
            # Run hook with test input
            result = subprocess.run(
                ['python3', str(hook_path)],
                stdin=open(temp_file),
                capture_output=True,
                text=True,
                timeout=5
            )
            
            os.unlink(temp_file)
            
            results.append({
                "test": test["name"],
                "exit_code": result.returncode,
                "stdout": result.stdout[:100] if result.stdout else "",
                "stderr": result.stderr[:100] if result.stderr else "",
                "success": result.returncode in [0, 1, 2]  # Valid exit codes
            })
            
        except Exception as e:
            results.append({
                "test": test["name"],
                "error": str(e),
                "success": False
            })
    
    return results

def analyze_single_hook_group(base_name, files, dir_path):
    """Analyze a single hook group in detail."""
    
    print(f"\n{'=' * 80}")
    print(f"HOOK: {base_name}")
    print(f"{'=' * 80}")
    
    # Check each file version
    file_analysis = []
    for file in files:
        file_path = dir_path / file
        
        analysis = {
            "file": file,
            "path": file_path,
            "exists": file_path.exists()
        }
        
        if file_path.exists():
            stat = os.stat(file_path)
            analysis["size"] = stat.st_size
            analysis["modified"] = datetime.fromtimestamp(stat.st_mtime)
            
            # Check Python syntax
            try:
                with open(file_path, 'r') as f:
                    code = f.read()
                compile(code, file_path, 'exec')
                analysis["syntax_valid"] = True
                
                # Check for official format indicators
                analysis["has_stdin_read"] = 'sys.stdin.read()' in code
                analysis["has_json_loads"] = 'json.loads' in code
                analysis["has_tool_name"] = 'tool_name' in code
                analysis["has_tool_input"] = 'tool_input' in code
                analysis["has_exit_codes"] = 'sys.exit(' in code
                
                # Count exit codes used
                analysis["exit_0"] = 'sys.exit(0)' in code
                analysis["exit_1"] = 'sys.exit(1)' in code
                analysis["exit_2"] = 'sys.exit(2)' in code
                
            except SyntaxError as e:
                analysis["syntax_valid"] = False
                analysis["syntax_error"] = f"Line {e.lineno}: {e.msg}"
        
        file_analysis.append(analysis)
    
    # Display analysis
    print("\n📊 File Analysis:")
    print("-" * 80)
    
    for analysis in file_analysis:
        if not analysis["exists"]:
            print(f"\n❌ {analysis['file']} - DOES NOT EXIST")
            continue
            
        print(f"\n📄 {analysis['file']}")
        print(f"   Size: {analysis['size']} bytes")
        print(f"   Modified: {analysis['modified'].strftime('%Y-%m-%d %H:%M')}")
        
        if not analysis["syntax_valid"]:
            print(f"   ❌ SYNTAX ERROR: {analysis.get('syntax_error', 'Unknown')}")
        else:
            print(f"   ✅ Valid Python syntax")
            
            # Check for official format compliance
            compliance_score = 0
            print("   Official format indicators:")
            
            if analysis.get("has_stdin_read"):
                print("     ✅ Reads from stdin")
                compliance_score += 1
            else:
                print("     ❌ No stdin.read()")
                
            if analysis.get("has_json_loads"):
                print("     ✅ Parses JSON")
                compliance_score += 1
            else:
                print("     ❌ No JSON parsing")
                
            if analysis.get("has_tool_name"):
                print("     ✅ Checks tool_name")
                compliance_score += 1
            else:
                print("     ❌ No tool_name check")
                
            if analysis.get("has_tool_input"):
                print("     ✅ Uses tool_input")
                compliance_score += 1
            else:
                print("     ❌ No tool_input")
                
            # Check exit codes
            print("   Exit codes used:")
            if analysis.get("exit_0"):
                print("     ✅ exit(0) - Success")
            if analysis.get("exit_1"):
                print("     ✅ exit(1) - Non-blocking error")
            if analysis.get("exit_2"):
                print("     ✅ exit(2) - Blocking error")
            if not any([analysis.get("exit_0"), analysis.get("exit_1"), analysis.get("exit_2")]):
                print("     ❌ No proper exit codes")
            else:
                compliance_score += 1
            
            print(f"   📊 Compliance score: {compliance_score}/5")
    
    # Make recommendation
    print("\n🎯 RECOMMENDATION:")
    
    # Find best candidate
    valid_files = [a for a in file_analysis if a.get("syntax_valid", False)]
    
    if not valid_files:
        print("   ❌ NO VALID FILES - Need to create new hook from scratch")
        return "CREATE_NEW"
    
    # Sort by compliance score
    valid_files.sort(key=lambda x: (
        x.get("has_stdin_read", 0) + 
        x.get("has_json_loads", 0) + 
        x.get("has_tool_name", 0) + 
        x.get("has_tool_input", 0) +
        any([x.get("exit_0"), x.get("exit_1"), x.get("exit_2")])
    ), reverse=True)
    
    best = valid_files[0]
    
    # Check if main version exists and is valid
    main_version = None
    for a in file_analysis:
        if a["file"] == base_name and a.get("syntax_valid"):
            main_version = a
            break
    
    if main_version and main_version == best:
        print(f"   ✅ KEEP CURRENT: {base_name} is already the best version")
        return "KEEP_CURRENT"
    elif best["file"] != base_name:
        print(f"   🔄 REPLACE: Use {best['file']} instead of current")
        print(f"      Reason: Better compliance with official format")
        return f"REPLACE_WITH:{best['file']}"
    else:
        print(f"   ✅ KEEP: {best['file']} is the best version")
        return f"KEEP:{best['file']}"

def main():
    """Manual hook review process."""
    
    print("=" * 80)
    print("MANUAL HOOK-BY-HOOK REVIEW")
    print("=" * 80)
    print("\nThis tool will help you review each hook group individually")
    print("and decide which version to keep based on official compliance.\n")
    
    # Start with critical hooks
    critical_hooks = [
        ("07-pii-protection.py", ["07-pii-protection.py.original", "07-pii-protection.py.broken"]),
        ("16-tcpa-compliance.py", ["16-tcpa-compliance.py.original"]),
        ("22-security-validator.py", ["22-security-validator.py.original"]),
    ]
    
    print("\n🚨 CRITICAL HOOKS (Blocking Operations)")
    print("-" * 40)
    
    decisions = []
    
    for base_name, extra_files in critical_hooks:
        # Check if main file exists
        main_path = Path(".claude/hooks/pre-tool-use") / base_name
        all_files = [base_name] if main_path.exists() else []
        all_files.extend(extra_files)
        
        decision = analyze_single_hook_group(
            base_name, 
            all_files,
            Path(".claude/hooks/pre-tool-use")
        )
        
        decisions.append({
            "hook": base_name,
            "decision": decision,
            "files": all_files
        })
    
    # Generate action plan
    print("\n" + "=" * 80)
    print("ACTION PLAN")
    print("=" * 80)
    
    for d in decisions:
        print(f"\n{d['hook']}:")
        
        if d["decision"] == "CREATE_NEW":
            print(f"  ❌ Create new official-compliant version")
            print(f"  Archive: {', '.join(d['files'])}")
            
        elif d["decision"] == "KEEP_CURRENT":
            print(f"  ✅ Keep current version")
            if len(d['files']) > 1:
                print(f"  Archive: {', '.join([f for f in d['files'] if f != d['hook']])}")
                
        elif d["decision"].startswith("REPLACE_WITH:"):
            source = d["decision"].split(":")[1]
            print(f"  🔄 Replace with {source}")
            print(f"  Commands:")
            print(f"    cp .claude/hooks/pre-tool-use/{source} .claude/hooks/pre-tool-use/{d['hook']}")
            print(f"  Archive: {', '.join([f for f in d['files'] if f != d['hook']])}")
    
    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("""
1. For hooks marked "CREATE_NEW":
   - Use the official-compliant versions created earlier
   - Or create new ones following the official format

2. For hooks marked "REPLACE_WITH":
   - Run the cp commands shown above
   - Test with official JSON format

3. For hooks marked "KEEP_CURRENT":
   - Test to ensure they handle official format
   - May need minor updates for full compliance

4. Archive old versions:
   mkdir -p .claude/hooks/_archive/$(date +%Y%m%d)
   # Move files listed under "Archive:" to the archive directory
""")

if __name__ == "__main__":
    main()
