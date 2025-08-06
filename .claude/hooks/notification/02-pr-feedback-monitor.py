#!/usr/bin/env python3
"""
PR Feedback Monitor - Checks for CodeRabbit and other PR feedback
Provides notifications when reviews are ready
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def get_current_pr():
    """Get PR number for current branch"""
    try:
        # Get current branch
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
        
        # Check if gh CLI is available
        result = subprocess.check_output(
            ["gh", "pr", "list", "--head", branch, "--json", "number"],
            text=True,
            stderr=subprocess.DEVNULL
        )
        
        prs = json.loads(result)
        if prs:
            return prs[0]['number']
    except:
        pass
    
    return None

def check_coderabbit_review(pr_number):
    """Check if CodeRabbit has reviewed"""
    try:
        # Get PR comments
        result = subprocess.check_output(
            ["gh", "api", f"repos/:owner/:repo/pulls/{pr_number}/comments"],
            text=True,
            stderr=subprocess.DEVNULL
        )
        
        comments = json.loads(result)
        
        # Look for CodeRabbit
        for comment in comments:
            if comment.get('user', {}).get('login') == 'coderabbitai':
                return parse_coderabbit_comment(comment['body'])
    except:
        pass
    
    return None

def parse_coderabbit_comment(body):
    """Extract key info from CodeRabbit comment"""
    issues = {
        'design_violations': [],
        'errors': [],
        'warnings': [],
        'suggestions': []
    }
    
    # Look for design system violations
    if 'text-size-' in body or 'font-regular' in body:
        issues['design_violations'].append("Design token violations found")
    
    # Look for errors
    if '🔴' in body or 'Error:' in body:
        issues['errors'].append("Critical issues found")
    
    # Look for warnings
    if '⚠️' in body or 'Warning:' in body:
        issues['warnings'].append("Warnings to address")
    
    return issues

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = {}
        if not sys.stdin.isatty():
            try:
                input_data = json.loads(sys.stdin.read())
            except:
                pass
        
        # This is a notification hook - it runs periodically
        # Check for PR feedback
        pr_number = get_current_pr()
        
        if pr_number:
            # Check for new feedback
            feedback = check_coderabbit_review(pr_number)
            
            if feedback:
                # Check if we've already notified
                notified_file = Path(f".claude/notifications/pr-{pr_number}-notified.json")
                
                if not notified_file.exists():
                    # First time seeing this feedback
                    notified_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Count total issues
                    total_issues = (
                        len(feedback.get('errors', [])) +
                        len(feedback.get('warnings', [])) +
                        len(feedback.get('design_violations', []))
                    )
                    
                    if total_issues > 0:
                        # Create notification message
                        message = f"🐰 CodeRabbit Review Ready for PR #{pr_number}\n"
                        message += f"Found {total_issues} issue(s) to address:\n"
                        
                        if feedback.get('errors'):
                            message += f"  - {len(feedback['errors'])} errors\n"
                        if feedback.get('warnings'):
                            message += f"  - {len(feedback['warnings'])} warnings\n"
                        if feedback.get('design_violations'):
                            message += f"  - {len(feedback['design_violations'])} design violations\n"
                        
                        message += f"\nRun: /pr-feedback {pr_number}"
                        
                        # Mark as notified
                        with open(notified_file, 'w') as f:
                            json.dump({
                                'notified_at': datetime.now().isoformat(),
                                'issues': feedback
                            }, f, indent=2)
                        
                        # Output notification message to stderr
                        print(message, file=sys.stderr)
        
        # Notification hooks just exit normally
        sys.exit(1)
        
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"PR feedback monitor error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
