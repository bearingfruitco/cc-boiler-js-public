#!/usr/bin/env python3
"""
Continuous Requirement Validator - Monitors adherence to project requirements
Checks if current work aligns with PRD and active requirements
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

def load_active_requirements():
    """Load current project requirements"""
    requirements = {
        'prd': None,
        'prps': [],
        'features': [],
        'constraints': []
    }
    
    # Check for main PRD
    prd_locations = [
        Path('PRD.md'),
        Path('.claude/PRD.md'),
        Path('docs/project/PROJECT_PRD.md')
    ]
    
    for prd_path in prd_locations:
        if prd_path.exists():
            requirements['prd'] = str(prd_path)
            break
    
    # Check for active PRPs
    prp_dir = Path('PRPs')
    if prp_dir.exists():
        for prp_file in prp_dir.glob('*-PRP.md'):
            # Check if it's active (modified in last 7 days)
            if (datetime.now() - datetime.fromtimestamp(prp_file.stat().st_mtime)) < timedelta(days=7):
                requirements['prps'].append({
                    'name': prp_file.stem,
                    'path': str(prp_file),
                    'modified': datetime.fromtimestamp(prp_file.stat().st_mtime).isoformat()
                })
    
    # Check for feature requirements
    features_dir = Path('docs/project/features')
    if features_dir.exists():
        for feature_file in features_dir.glob('*-PRD.md'):
            requirements['features'].append(str(feature_file))
    
    # Check for constraints file
    constraints_path = Path('.claude/requirements/constraints.json')
    if constraints_path.exists():
        try:
            with open(constraints_path, 'r') as f:
                requirements['constraints'] = json.load(f)
        except:
            pass
    
    return requirements

def check_requirement_drift():
    """Check if recent work might be drifting from requirements"""
    drift_indicators = []
    
    # Check recent files against known requirements
    recent_files_path = Path('.claude/state/recent-files.txt')
    if recent_files_path.exists():
        try:
            with open(recent_files_path, 'r') as f:
                recent_files = [line.strip() for line in f.readlines()[-20:]]
                
                # Look for new directories/features not in requirements
                known_features = set()
                features_dir = Path('docs/project/features')
                if features_dir.exists():
                    known_features = {f.stem.split('-')[0] for f in features_dir.glob('*-PRD.md')}
                
                for file_path in recent_files:
                    parts = Path(file_path).parts
                    # Check if working on undocumented feature
                    if 'features' in parts or 'components' in parts:
                        feature_name = None
                        for part in parts:
                            if part not in ['features', 'components', 'src', 'app']:
                                feature_name = part.split('-')[0]
                                break
                        
                        if feature_name and feature_name not in known_features:
                            drift_indicators.append(f"undocumented-feature: {feature_name}")
        except:
            pass
    
    # Check if working without active PRP
    active_prp_path = Path('.claude/state/active-prp.json')
    if not active_prp_path.exists():
        # Check if doing significant work
        if recent_files_path.exists():
            try:
                with open(recent_files_path, 'r') as f:
                    if len(f.readlines()) > 10:
                        drift_indicators.append("no-active-prp")
            except:
                pass
    
    return drift_indicators

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
        
        # Check for requirement drift periodically
        check_marker = Path('.claude/state/last-requirement-check.json')
        should_check = True
        
        if check_marker.exists():
            try:
                with open(check_marker, 'r') as f:
                    last_check = json.load(f)
                    last_time = datetime.fromisoformat(last_check.get('timestamp'))
                    # Check every 30 minutes
                    if (datetime.now() - last_time).seconds < 1800:
                        should_check = False
            except:
                pass
        
        if should_check:
            # Load requirements
            requirements = load_active_requirements()
            drift_indicators = check_requirement_drift()
            
            if drift_indicators:
                # Create notification
                message = "⚠️ Requirement Validation Alert\n"
                
                if "no-active-prp" in drift_indicators:
                    message += "• Working without an active PRP\n"
                
                undocumented = [d for d in drift_indicators if d.startswith("undocumented-feature")]
                if undocumented:
                    message += f"• Found {len(undocumented)} undocumented features\n"
                
                message += "\nRecommended actions:\n"
                if "no-active-prp" in drift_indicators:
                    message += "• Run /create-prp to document current work\n"
                if undocumented:
                    message += "• Run /create-prd for new features\n"
                
                message += "• Run /verify --requirements to check alignment"
                
                # Update check marker
                check_marker.parent.mkdir(parents=True, exist_ok=True)
                with open(check_marker, 'w') as f:
                    json.dump({'timestamp': datetime.now().isoformat()}, f)
                
                # Output notification to stderr
                print(message, file=sys.stderr)
        
        # Notification hooks just exit normally
        sys.exit(1)
        
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"Requirement validator error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
