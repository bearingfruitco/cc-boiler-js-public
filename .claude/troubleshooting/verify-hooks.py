#!/usr/bin/env python3
"""
Verify Claude Code hook configuration and provide detailed diagnostics
"""

import json
import subprocess
import sys
from pathlib import Path

CLAUDE_DIR = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude")

def check_claude_doctor():
    """Run claude doctor and analyze output"""
    try:
        result = subprocess.run(
            ["claude", "doctor"],
            cwd=CLAUDE_DIR.parent,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Check for specific errors
        has_error = False
        error_type = None
        
        if "Cannot assign to read only property" in result.stderr:
            has_error = True
            error_type = "read_only_property"
        elif "Found invalid settings files" in result.stderr:
            has_error = True
            error_type = "invalid_settings"
        elif result.returncode != 0:
            has_error = True
            error_type = "unknown_error"
            
        return {
            "success": not has_error,
            "error_type": error_type,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {
            "success": False,
            "error_type": "exception",
            "error": str(e)
        }

def verify_hook_files():
    """Verify all hook files exist and are executable"""
    settings_path = CLAUDE_DIR / "settings.json"
    if not settings_path.exists():
        return {"error": "settings.json not found"}
    
    settings = json.loads(settings_path.read_text())
    
    missing_files = []
    non_executable = []
    
    if "hooks" in settings:
        for event_type, hooks in settings["hooks"].items():
            for hook in hooks:
                command = hook.get("command", "")
                # Extract file path from command
                if command.startswith("python3 "):
                    file_path = command.replace("python3 ", "").strip()
                    full_path = CLAUDE_DIR.parent / file_path
                    
                    if not full_path.exists():
                        missing_files.append(file_path)
                    elif not full_path.stat().st_mode & 0o111:
                        non_executable.append(file_path)
    
    return {
        "total_hooks": sum(len(hooks) for hooks in settings.get("hooks", {}).values()),
        "missing_files": missing_files,
        "non_executable": non_executable
    }

def main():
    """Run verification"""
    print("🔍 Claude Code Hook Configuration Verification")
    print("=" * 60)
    
    # Check current settings
    settings_path = CLAUDE_DIR / "settings.json"
    if settings_path.exists():
        settings = json.loads(settings_path.read_text())
        hook_count = sum(len(hooks) for hooks in settings.get("hooks", {}).values())
        print(f"📋 Current configuration has {hook_count} hooks")
    else:
        print("❌ No settings.json found")
        sys.exit(1)
    
    # Verify hook files
    print("\n📁 Verifying hook files...")
    file_check = verify_hook_files()
    print(f"   Total hooks: {file_check['total_hooks']}")
    
    if file_check["missing_files"]:
        print(f"   ❌ Missing files: {len(file_check['missing_files'])}")
        for f in file_check["missing_files"][:5]:
            print(f"      - {f}")
    else:
        print("   ✅ All hook files exist")
    
    if file_check["non_executable"]:
        print(f"   ⚠️  Non-executable files: {len(file_check['non_executable'])}")
    
    # Check Claude doctor
    print("\n🏥 Running claude doctor...")
    doctor_result = check_claude_doctor()
    
    if doctor_result["success"]:
        print("   ✅ SUCCESS! No configuration errors detected")
        print("   Claude Code accepts the hook configuration")
    else:
        print(f"   ❌ FAILED: {doctor_result.get('error_type', 'Unknown error')}")
        if doctor_result.get("stderr"):
            print(f"   Error: {doctor_result['stderr'][:200]}")
    
    # Provide recommendations
    print("\n💡 Recommendations:")
    if doctor_result["success"]:
        print("   1. Configuration is working! You can now gradually add more hooks")
        print("   2. Test with: cp .claude/settings-migrated-gradual.json .claude/settings.json")
        print("   3. Monitor for any runtime errors when hooks execute")
    else:
        if doctor_result.get("error_type") == "read_only_property":
            print("   1. The hook format is still incorrect")
            print("   2. Try the minimal configuration first")
            print("   3. Check if hooks should be strings instead of objects")
        elif doctor_result.get("error_type") == "invalid_settings":
            print("   1. The settings.json has invalid JSON structure")
            print("   2. Validate with: jq . .claude/settings.json")
            print("   3. Check for trailing commas or syntax errors")
    
    # Save detailed report
    report = {
        "timestamp": Path("/bin/date").read_text().strip() if Path("/bin/date").exists() else "now",
        "settings_valid": settings_path.exists(),
        "hook_count": hook_count if 'hook_count' in locals() else 0,
        "file_check": file_check,
        "doctor_result": {
            "success": doctor_result["success"],
            "error_type": doctor_result.get("error_type"),
            "returncode": doctor_result.get("returncode")
        }
    }
    
    report_path = CLAUDE_DIR / "hook-verification-report.json"
    report_path.write_text(json.dumps(report, indent=2))
    print(f"\n📊 Detailed report saved to: {report_path}")

if __name__ == "__main__":
    main()
