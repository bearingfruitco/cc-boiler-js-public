#!/usr/bin/env python3
"""
Security Alerts - Monitors for security issues and provides notifications
Checks for vulnerabilities, exposed secrets, and security best practices
"""

import json
import sys
import os
import re
from pathlib import Path
from datetime import datetime, timedelta

def check_for_secrets(recent_files):
    """Check if any recent files might contain secrets"""
    secret_patterns = [
        (r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?[a-zA-Z0-9]{20,}', 'API key'),
        (r'(?i)(secret|password|passwd|pwd)\s*[:=]\s*["\']?[^\s"\']{8,}', 'Password/Secret'),
        (r'(?i)bearer\s+[a-zA-Z0-9\-._~+/]+={0,2}', 'Bearer token'),
        (r'(?i)(aws[_-]?access[_-]?key[_-]?id|aws[_-]?secret)\s*[:=]\s*["\']?[A-Z0-9]{16,}', 'AWS credentials'),
        (r'(?i)private[_-]?key\s*[:=]\s*["\']?-----BEGIN', 'Private key'),
        (r'postgresql://[^:]+:[^@]+@[^/]+', 'Database URL with password'),
    ]
    
    found_secrets = []
    
    for file_path in recent_files:
        if Path(file_path).exists() and Path(file_path).suffix in ['.js', '.ts', '.py', '.env', '.json', '.yml', '.yaml']:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                    for pattern, secret_type in secret_patterns:
                        if re.search(pattern, content):
                            found_secrets.append({
                                'file': file_path,
                                'type': secret_type
                            })
                            break  # One secret per file is enough for notification
            except:
                pass
    
    return found_secrets

def check_dependency_vulnerabilities():
    """Check for known vulnerabilities in dependencies"""
    vulnerabilities = []
    
    # Check if package.json was recently modified
    package_json = Path('package.json')
    if package_json.exists():
        # Check if modified in last hour
        if (datetime.now() - datetime.fromtimestamp(package_json.stat().st_mtime)) < timedelta(hours=1):
            vulnerabilities.append({
                'type': 'dependencies-updated',
                'message': 'Dependencies were recently updated'
            })
    
    # Check for audit markers
    audit_marker = Path('.claude/security/last-audit.json')
    if audit_marker.exists():
        try:
            with open(audit_marker, 'r') as f:
                audit_data = json.load(f)
                if audit_data.get('vulnerabilities', 0) > 0:
                    vulnerabilities.append({
                        'type': 'known-vulnerabilities',
                        'count': audit_data['vulnerabilities'],
                        'critical': audit_data.get('critical', 0)
                    })
        except:
            pass
    
    return vulnerabilities

def check_security_practices():
    """Check for security best practices"""
    issues = []
    
    # Check if .env is in git
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'ls-files', '.env'],
            capture_output=True,
            text=True,
            stderr=subprocess.DEVNULL
        )
        if result.stdout.strip():
            issues.append({
                'type': 'env-in-git',
                'severity': 'critical',
                'message': '.env file is tracked in git'
            })
    except:
        pass
    
    # Check for missing security headers in API routes
    api_dir = Path('app/api')
    if api_dir.exists():
        routes_without_auth = []
        for route_file in api_dir.rglob('route.ts'):
            try:
                with open(route_file, 'r') as f:
                    content = f.read()
                    # Simple check for auth
                    if 'export async function' in content and not any(auth in content for auth in ['authenticate', 'getServerSession', 'requireAuth', 'verifyToken']):
                        routes_without_auth.append(str(route_file))
            except:
                pass
        
        if routes_without_auth:
            issues.append({
                'type': 'unprotected-routes',
                'count': len(routes_without_auth),
                'severity': 'high'
            })
    
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
        
        # Check if we should run security checks (throttled)
        check_marker = Path('.claude/state/last-security-check.json')
        should_check = True
        
        if check_marker.exists():
            try:
                with open(check_marker, 'r') as f:
                    last_check = json.load(f)
                    last_time = datetime.fromisoformat(last_check.get('timestamp'))
                    # Check every hour
                    if (datetime.now() - last_time).seconds < 3600:
                        should_check = False
            except:
                pass
        
        if should_check:
            alerts = []
            
            # Get recent files
            recent_files = []
            recent_files_path = Path('.claude/state/recent-files.txt')
            if recent_files_path.exists():
                try:
                    with open(recent_files_path, 'r') as f:
                        recent_files = [line.strip() for line in f.readlines()[-50:]]
                except:
                    pass
            
            # Check for exposed secrets
            secrets = check_for_secrets(recent_files)
            if secrets:
                alerts.append({
                    'type': 'exposed-secrets',
                    'severity': 'critical',
                    'count': len(secrets),
                    'files': [s['file'] for s in secrets[:3]]  # Show max 3
                })
            
            # Check for vulnerabilities
            vulns = check_dependency_vulnerabilities()
            if vulns:
                for vuln in vulns:
                    if vuln.get('critical', 0) > 0:
                        alerts.append(vuln)
            
            # Check security practices
            practices = check_security_practices()
            for issue in practices:
                if issue.get('severity') in ['critical', 'high']:
                    alerts.append(issue)
            
            if alerts:
                # Create notification
                message = "🔒 Security Alert\n"
                
                critical_count = sum(1 for a in alerts if a.get('severity') == 'critical')
                if critical_count > 0:
                    message += f"⚠️ {critical_count} CRITICAL issues found\n\n"
                
                for alert in alerts[:3]:  # Show max 3 alerts
                    if alert['type'] == 'exposed-secrets':
                        message += f"🔑 Potential secrets exposed in {alert['count']} files\n"
                    elif alert['type'] == 'env-in-git':
                        message += "📁 .env file is tracked in git (CRITICAL)\n"
                    elif alert['type'] == 'unprotected-routes':
                        message += f"🛡️ {alert['count']} API routes without authentication\n"
                    elif alert['type'] == 'known-vulnerabilities':
                        message += f"⚠️ {alert['count']} vulnerabilities ({alert.get('critical', 0)} critical)\n"
                
                message += "\nRun /security-check for details"
                
                # Update check marker
                check_marker.parent.mkdir(parents=True, exist_ok=True)
                with open(check_marker, 'w') as f:
                    json.dump({
                        'timestamp': datetime.now().isoformat(),
                        'alerts': len(alerts)
                    }, f)
                
                # Output notification to stderr
                print(message, file=sys.stderr)
        
        # Notification hooks just exit normally
        sys.exit(1)
        
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"Security alerts error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
