#!/usr/bin/env python3
"""
Requirement Context Preserver
Ensures locked requirements and anchors survive conversation compaction
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def preserve_requirements():
    """Preserve requirement context before compaction"""
    preserved_data = {
        "timestamp": datetime.now().isoformat(),
        "requirements": [],
        "anchors": [],
        "locked_specs": []
    }
    
    # Check for PRD files
    prd_files = []
    
    # Project PRD
    project_prd = Path("docs/project/PROJECT_PRD.md")
    if project_prd.exists():
        prd_files.append(project_prd)
    
    # Feature PRDs
    features_dir = Path("docs/project/features")
    if features_dir.exists():
        prd_files.extend(features_dir.glob("*-PRD.md"))
    
    # Extract requirements from PRDs
    for prd_file in prd_files:
        try:
            content = prd_file.read_text()
            
            # Look for requirement sections
            if "## Requirements" in content or "## Functional Requirements" in content:
                preserved_data["requirements"].append({
                    "source": str(prd_file),
                    "timestamp": datetime.fromtimestamp(prd_file.stat().st_mtime).isoformat()
                })
            
            # Look for locked specifications
            if "[LOCKED]" in content or "⚡ LOCKED" in content:
                preserved_data["locked_specs"].append(str(prd_file))
        except:
            pass
    
    # Check for requirement anchors
    anchor_file = Path(".claude/requirements/anchors.json")
    if anchor_file.exists():
        try:
            with open(anchor_file, 'r') as f:
                anchors = json.load(f)
                preserved_data["anchors"] = anchors.get("anchors", [])
        except:
            pass
    
    # Save preservation record
    preservation_dir = Path(".claude/preservation")
    preservation_dir.mkdir(parents=True, exist_ok=True)
    
    preservation_file = preservation_dir / "requirements-context.json"
    with open(preservation_file, 'w') as f:
        json.dump(preserved_data, f, indent=2)
    
    return preserved_data

def main():
    """Main hook logic"""
    try:
        # Read input if provided
        input_data = {}
        if not sys.stdin.isatty():
            try:
                input_data = json.loads(sys.stdin.read())
            except:
                pass
        
        # Preserve requirements
        preserved = preserve_requirements()
        
        # Log preservation info
        if preserved["requirements"] or preserved["locked_specs"]:
            message = f"📋 Preserved {len(preserved['requirements'])} requirement sources\n"
            if preserved["locked_specs"]:
                message += f"🔒 {len(preserved['locked_specs'])} locked specifications\n"
            if preserved["anchors"]:
                message += f"⚓ {len(preserved['anchors'])} requirement anchors\n"
            
            print(message, file=sys.stderr)
        
        # PreCompact hooks just exit with code 0
        sys.exit(1)
        
    except Exception as e:
        # Log error to stderr and exit
        print(f"Requirement context preserver error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
