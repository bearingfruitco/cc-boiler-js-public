#!/usr/bin/env python3
"""
Quick Boilerplate Update Checker
Shows what commands/features to update in projects
"""

import json
from pathlib import Path
from datetime import datetime

# Recent boilerplate updates
RECENT_UPDATES = {
    "2024-01-15": {
        "name": "Architecture-Driven Development",
        "commands": [
            "/create-architecture",
            "/validate-architecture", 
            "/architecture-viz",
            "/generate-component-prps"
        ],
        "agents": ["prp-writer"],
        "files": [
            ".claude/commands/create-architecture.md",
            ".claude/commands/validate-architecture.md",
            ".claude/commands/architecture-viz.md",
            ".claude/commands/generate-component-prps.md",
            ".claude/agents/prp-writer.md",
            "scripts/validate-architecture.py",
            "scripts/visualize-architecture.py",
            "scripts/generate-component-prps.py"
        ],
        "impact": "Major - adds complete architecture workflow"
    }
}

def check_project_status(project_path="."):
    """Check which updates a project needs"""
    project = Path(project_path)
    missing_updates = []
    
    print(f"Checking project: {project.absolute()}")
    print("-" * 50)
    
    for date, update in RECENT_UPDATES.items():
        print(f"\n📦 Update: {update['name']} ({date})")
        print(f"Impact: {update['impact']}")
        
        missing_files = []
        for file in update['files']:
            if not (project / file).exists():
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ Missing {len(missing_files)} files:")
            for f in missing_files[:5]:  # Show first 5
                print(f"   - {f}")
            if len(missing_files) > 5:
                print(f"   ... and {len(missing_files) - 5} more")
                
            missing_updates.append(update)
        else:
            print("✅ Already updated")
    
    if missing_updates:
        print("\n🔧 To update your project:")
        print("1. In boilerplate directory, run:")
        print("   git log --oneline -10")
        print("\n2. In your project, cherry-pick relevant commits:")
        print("   git cherry-pick [commit-hash]")
        print("\n3. Or use selective copy:")
        for update in missing_updates:
            print(f"\n   # For {update['name']}:")
            print("   cp -r ../boilerplate/.claude/commands/[new-commands] .claude/commands/")
    else:
        print("\n✅ Your project is up to date!")

if __name__ == "__main__":
    import sys
    project_path = sys.argv[1] if len(sys.argv) > 1 else "."
    check_project_status(project_path)
