#!/usr/bin/env python3
"""
Database Environment Check Hook - Prevents cross-environment database access
Validates connection strings and blocks production data exports
"""

import json
import sys
import os
import re
from urllib.parse import urlparse

def parse_database_url(url):
    """Parse database URL to extract components"""
    try:
        parsed = urlparse(url)
        return {
            'scheme': parsed.scheme,
            'host': parsed.hostname,
            'port': parsed.port,
            'database': parsed.path.lstrip('/'),
            'user': parsed.username,
        }
    except:
        return None

def get_env_database_patterns():
    """Get expected database patterns for each environment"""
    return {
        'development': [
            'localhost',
            '127.0.0.1',
            'docker.internal',
            '_dev',
            '_development',
        ],
        'staging': [
            'staging',
            '_staging',
            'stage',
            '_stg',
        ],
        'production': [
            'prod',
            'production',
            '_prod',
            'live',
        ],
    }

def check_database_environment_match(command, current_env):
    """Check if database operations match the current environment"""
    patterns = get_env_database_patterns()
    
    # Extract database references from command
    db_pattern = r'(?:DATABASE_URL|postgresql://|mysql://|mongodb://)[^\s\'\"]+|(?:FROM|INTO|UPDATE|DELETE FROM)\s+(\w+)'
    matches = re.findall(db_pattern, command, re.IGNORECASE)
    
    if not matches:
        return True  # No database operations found
    
    # Check each match
    for match in matches:
        match_lower = match.lower()
        
        # Check for cross-environment access
        for env, env_patterns in patterns.items():
            if env != current_env:
                for pattern in env_patterns:
                    if pattern in match_lower:
                        return False  # Cross-environment access detected
    
    return True

def is_data_export_command(command):
    """Check if command is attempting to export data"""
    export_patterns = [
        r'pg_dump',
        r'mysqldump',
        r'mongodump',
        r'SELECT.*INTO OUTFILE',
        r'COPY.*TO',
        r'\.dump',
        r'--export',
        r'backup',
    ]
    
    for pattern in export_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    
    return False

def is_migration_command(command):
    """Check if this is a migration command"""
    migration_patterns = [
        'migrate',
        'migration',
        'db:push',
        'db:migrate',
        'prisma migrate',
        'drizzle',
    ]
    
    return any(pattern in command.lower() for pattern in migration_patterns)

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Only check Bash commands for database operations
        if tool_name != 'Bash':
            sys.exit(0)
        
        command = tool_input.get('command', '')
        current_env = os.environ.get('NODE_ENV', 'development')
        
        # Check for cross-environment database access
        if not check_database_environment_match(command, current_env):
            error_msg = {
                "action": "block",
                "message": f"🚫 Cross-environment database access detected!\n\n"
                          f"Current environment: {current_env.upper()}\n"
                          f"Command appears to access a different environment's database.\n\n"
                          "This is blocked to prevent:\n"
                          "• Accidental data corruption\n"
                          "• Security breaches\n"
                          "• Data inconsistencies\n\n"
                          "Please use the correct database URL for your environment."
            }
            print(json.dumps(error_msg))
            sys.exit(1)
        
        # Check for data exports in production
        if current_env == 'production' and is_data_export_command(command):
            error_msg = {
                "action": "block",
                "message": "🚫 PRODUCTION: Data export blocked!\n\n"
                          "Exporting production data is restricted for security.\n\n"
                          "If you need production data:\n"
                          "1. Use read-only queries\n"
                          "2. Request anonymized dumps\n"
                          "3. Use staging environment with sanitized data\n"
                          "4. Contact security team for approved exports"
            }
            print(json.dumps(error_msg))
            sys.exit(1)
        
        # Check for migrations in production
        if current_env == 'production' and is_migration_command(command):
            warning_msg = {
                "action": "warn",
                "message": "⚠️  PRODUCTION MIGRATION DETECTED!\n\n"
                          "You're about to run a migration in production.\n\n"
                          "Checklist:\n"
                          "✓ Backup completed?\n"
                          "✓ Migration tested in staging?\n"
                          "✓ Rollback plan ready?\n"
                          "✓ Maintenance window scheduled?\n\n"
                          "Type 'yes' to confirm you've completed the checklist."
            }
            print(json.dumps(warning_msg))
            sys.exit(0)
        
        # Allow operation to proceed
        sys.exit(0)
        
    except Exception as e:
        # In case of any error, log but allow operation
        error_output = {
            "action": "allow",
            "message": f"Database environment check error: {str(e)}"
        }
        print(json.dumps(error_output))
        sys.exit(0)

if __name__ == '__main__':
    main()
