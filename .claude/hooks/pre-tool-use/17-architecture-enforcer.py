#!/usr/bin/env python3
"""
Architecture Enforcement Hook - Ensures architecture is designed before issue generation
Prevents jumping directly from PRD to implementation without proper technical design
"""

import json
import sys
import os
from pathlib import Path

def check_architecture_exists():
    """Check if architecture documentation exists"""
    arch_dir = Path('docs/architecture')
    required_files = [
        'SYSTEM_DESIGN.md',
        'DATABASE_SCHEMA.md',
        'API_SPECIFICATION.md',
        'FRONTEND_ARCHITECTURE.md',
        'SECURITY_DESIGN.md',
        'TECHNICAL_ROADMAP.md'
    ]
    
    if not arch_dir.exists():
        return False, []
    
    existing_files = []
    for file in required_files:
        if (arch_dir / file).exists():
            existing_files.append(file)
    
    # Need at least 4 out of 6 files to consider architecture "done"
    return len(existing_files) >= 4, existing_files

def check_prd_exists():
    """Check if PRD exists"""
    prd_locations = [
        'docs/project/PROJECT_PRD.md',
        'PROJECT_PRD.md',
        'docs/PROJECT_PRD.md'
    ]
    
    for location in prd_locations:
        if Path(location).exists():
            return True
    return False

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract command information
        tool_name = input_data.get('tool_name', '')
        
        # Only check for specific commands
        if tool_name == 'execute_command':
            parameters = input_data.get('parameters', {})
            command = parameters.get('command', '')
            
            # Check if trying to generate issues without architecture
            if command.startswith('/gi ') or command == '/gi PROJECT' or command.startswith('/generate-issues'):
                has_arch, existing_files = check_architecture_exists()
                
                if not has_arch:
                    has_prd = check_prd_exists()
                    
                    if has_prd:
                        # PRD exists but no architecture - this is the gap we're fixing
                        error_msg = """🚫 Architecture Design Required

You have a PRD but haven't designed the system architecture yet. This is a critical step that:
- Defines technical implementation details
- Prevents costly refactoring later
- Enables parallel development
- Ensures scalability and security

Please design your architecture first:

Option 1: Use the architecture chain (recommended)
```bash
/chain architecture-design
# or shortcut:
/ad
```

Option 2: Use the architecture command
```bash
/create-architecture
# or shortcut:
/arch
```

Option 3: Manual approach (if needed)
```bash
/ultrathink system architecture for this project
/create-prp database design
/create-prp api design
/create-prp frontend architecture
```

The architecture phase will:
1. Analyze your PRD for technical requirements
2. Design system components and data flow
3. Create database schema
4. Define API structure
5. Plan security measures
6. Generate component PRPs
7. Create technical roadmap

This ensures thoughtful system design before jumping into code!"""
                        
                        print(json.dumps({
                            "action": "block",
                            "message": error_msg
                        }))
                        sys.exit(0)
                    else:
                        # No PRD either - different error
                        error_msg = """❌ No PRD Found

You need to create a PRD before generating issues:
```bash
/prd [feature name]
```

Then design the architecture:
```bash
/arch
```

Finally, generate issues:
```bash
/gi PROJECT
```"""
                        
                        print(json.dumps({
                            "action": "block",
                            "message": error_msg
                        }))
                        sys.exit(0)
                else:
                    # Architecture exists - provide helpful info
                    info_msg = f"""✅ Architecture found! ({len(existing_files)}/6 documents)

Existing architecture docs:
{chr(10).join('• ' + f for f in existing_files)}

Proceeding with issue generation..."""
                    
                    # Log but don't block
                    print(json.dumps({
                        "action": "log",
                        "message": info_msg
                    }), file=sys.stderr)
        
        # For all other cases, continue normally
        sys.exit(0)
        
    except Exception as e:
        # On error, log but don't block
        print(json.dumps({
            "action": "log",
            "message": f"Architecture hook error: {str(e)}"
        }), file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
