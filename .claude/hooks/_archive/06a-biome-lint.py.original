#!/usr/bin/env python3
"""
Biome Linting Hook - Run Biome checks before file changes
Ensures code quality with Biome's fast linting and formatting
"""

import json
import sys
import subprocess
from pathlib import Path
import tempfile
import os

def run_biome_check(file_path):
    """Run Biome linter on the file"""
    try:
        # Run Biome check on the specific file
        result = subprocess.run(
            ["pnpm", "biome", "check", file_path],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'errors': result.stderr
        }
    except Exception as e:
        return {
            'success': False,
            'output': '',
            'errors': str(e)
        }

def run_biome_format_check(file_path):
    """Check if file needs formatting"""
    try:
        # Check format without applying
        result = subprocess.run(
            ["pnpm", "biome", "format", file_path],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        return {
            'needs_format': result.returncode != 0,
            'output': result.stdout
        }
    except:
        return {'needs_format': False, 'output': ''}

def auto_fix_with_biome(file_path):
    """Attempt to auto-fix issues with Biome"""
    try:
        # Run Biome with --apply flag
        result = subprocess.run(
            ["pnpm", "biome", "check", "--apply", file_path],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            # Read the fixed content
            with open(file_path, 'r') as f:
                fixed_content = f.read()
            return {'success': True, 'content': fixed_content}
        
        return {'success': False, 'content': None}
    except:
        return {'success': False, 'content': None}

def parse_biome_output(output):
    """Parse Biome output for specific issues"""
    issues = []
    
    if "error" in output.lower() or "warning" in output.lower():
        # Extract error messages
        lines = output.split('\n')
        for line in lines:
            if '⚠' in line or '✖' in line or 'error' in line.lower():
                issues.append(line.strip())
    
    return issues

def should_check_file(file_path):
    """Determine if file should be checked by Biome"""
    # Check file extensions
    checkable_extensions = ['.js', '.jsx', '.ts', '.tsx', '.json', '.jsonc']
    
    # Skip ignored paths
    ignore_paths = ['node_modules', '.next', 'dist', 'build', '.turbo']
    
    path = Path(file_path)
    
    # Check if extension is supported
    if not any(str(path).endswith(ext) for ext in checkable_extensions):
        return False
    
    # Check if in ignored directory
    if any(ignored in str(path) for ignored in ignore_paths):
        return False
    
    return True

def format_biome_report(check_result, format_result, file_path):
    """Format Biome results into readable report"""
    report = f"🔍 Biome Check: {Path(file_path).name}\n"
    
    if not check_result['success']:
        report += "\n❌ Linting Issues Found:\n"
        issues = parse_biome_output(check_result['output'] + check_result['errors'])
        for issue in issues[:5]:  # Show first 5 issues
            report += f"  {issue}\n"
        
        if len(issues) > 5:
            report += f"\n  ... and {len(issues) - 5} more issues\n"
    
    if format_result.get('needs_format'):
        report += "\n📐 Formatting Required\n"
        report += "  File needs formatting according to Biome rules\n"
    
    report += "\n💡 To fix automatically, run:\n"
    report += f"  pnpm biome check --apply {file_path}\n"
    report += f"  pnpm format\n"
    
    return report

def main():
    """Main hook logic"""
    try:
        # Read input
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name - handle multiple formats
        tool_name = input_data.get('tool_name', '')
        if not tool_name and 'tool_use' in input_data:
            tool_name = input_data['tool_use'].get('name', '')
        if not tool_name:
            tool_name = input_data.get('tool', '')
        
        # Only check on write operations
        if tool_name not in ['Write', 'Edit', 'str_replace']:
            sys.exit(0)
            return
        
        # Extract parameters
        tool_input = input_data.get('tool_input', {})
        if not tool_input and 'tool_use' in input_data:
            tool_input = input_data['tool_use'].get('parameters', {})
        
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        # Check if file should be linted
        if not should_check_file(file_path):
            sys.exit(0)
            return
        
        # Create temp file for checking
        with tempfile.NamedTemporaryFile(mode='w', suffix=Path(file_path).suffix, delete=False) as temp:
            temp.write(content)
            temp_path = temp.name
        
        try:
            # Run Biome checks
            check_result = run_biome_check(temp_path)
            format_result = run_biome_format_check(temp_path)
            
            # If there are issues
            if not check_result['success'] or format_result.get('needs_format'):
                # Try auto-fix
                fix_result = auto_fix_with_biome(temp_path)
                
                if fix_result['success'] and fix_result['content'] != content:
                    # Suggest the fixed version
                    message = format_biome_report(check_result, format_result, file_path)
                    message += f"\n✨ Auto-fixed version available with corrections applied."
                    
                    print(message)  # Warning
            sys.exit(0)
                else:
                    # Just warn about issues
                    print(format_biome_report(check_result, format_result, file_path),
                        "continue": True
                    , file=sys.stderr)
            sys.exit(1)
            else:
                # No issues, continue
                sys.exit(0)
                
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        
    except Exception as e:
        # On error, log but don't block
        print(json.dumps({
            sys.exit(0)

if __name__ == "__main__":
    main()
