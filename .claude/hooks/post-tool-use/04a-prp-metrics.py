#!/usr/bin/env python3
"""
PRP Metrics Collection Hook - Track PRP execution success
Collects metrics after PRP-related operations
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def get_metrics_path():
    """Get path to metrics storage"""
    return Path("PRPs/metrics")

def extract_prp_name(file_path):
    """Extract PRP name from file path"""
    if 'PRPs/' in file_path and file_path.endswith('.md'):
        # Get filename without extension
        return Path(file_path).stem
    return None

def load_existing_metrics(prp_name):
    """Load existing metrics for a PRP if they exist"""
    metrics_path = get_metrics_path() / f"{prp_name}_metrics.json"
    if metrics_path.exists():
        with open(metrics_path) as f:
            return json.load(f)
    return None

def save_metrics(prp_name, metrics):
    """Save metrics for a PRP"""
    metrics_path = get_metrics_path()
    metrics_path.mkdir(exist_ok=True)
    
    metrics_file = metrics_path / f"{prp_name}_metrics.json"
    
    # Add timestamp
    metrics['last_updated'] = datetime.now().isoformat()
    
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2, default=str)

def extract_validation_results(content):
    """Extract validation results from PRP execution output"""
    results = {
        'syntax': None,
        'components': None,
        'integration': None,
        'production': None
    }
    
    # Look for validation level results
    patterns = {
        'syntax': r'Level 1.*?(\d+)%|Syntax.*?(\d+)%',
        'components': r'Level 2.*?(\d+)%|Component.*?(\d+)%',
        'integration': r'Level 3.*?(\d+)%|Integration.*?(\d+)%',
        'production': r'Level 4.*?(\d+)%|Production.*?(\d+)%'
    }
    
    for level, pattern in patterns.items():
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            score = match.group(1) or match.group(2)
            if score:
                results[level] = int(score)
    
    return results

def update_prp_with_metrics(file_path, metrics):
    """Update PRP file with metrics section"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check if metrics section exists
        if '## 📊 Success Metrics' in content or '## Success Metrics' in content:
            # Update existing metrics
            metrics_yaml = format_metrics_yaml(metrics)
            
            # Replace metrics section
            pattern = r'(##\s*(?:📊\s*)?Success Metrics.*?```yaml)(.*?)(```)'
            replacement = f'\\1\n{metrics_yaml}\n\\3'
            
            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        else:
            # Add metrics section at the end
            metrics_section = f"\n\n## 📊 Success Metrics\n```yaml\n{format_metrics_yaml(metrics)}\n```\n"
            new_content = content.rstrip() + metrics_section
        
        # Write back
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print(f"Error updating PRP with metrics: {e}", file=sys.stderr)
        return False

def format_metrics_yaml(metrics):
    """Format metrics as YAML for PRP"""
    yaml_lines = []
    
    if 'first_pass_success' in metrics:
        yaml_lines.append(f"first_pass_success: {str(metrics['first_pass_success']).lower()}")
    
    if 'validation_scores' in metrics:
        yaml_lines.append("validation_scores:")
        for level, score in metrics['validation_scores'].items():
            if score is not None:
                yaml_lines.append(f"  {level}: {score}%")
    
    if 'duration' in metrics:
        # Convert seconds to human readable
        duration_sec = metrics['duration']
        hours = int(duration_sec // 3600)
        minutes = int((duration_sec % 3600) // 60)
        if hours > 0:
            yaml_lines.append(f"time_to_complete: \"{hours}h {minutes}m\"")
        else:
            yaml_lines.append(f"time_to_complete: \"{minutes}m\"")
    
    # Add other metrics
    for key in ['bugs_found_after', 'test_coverage', 'bundle_impact']:
        if key in metrics:
            yaml_lines.append(f"{key}: {metrics[key]}")
    
    return '\n'.join(yaml_lines)

def analyze_prp_completion(file_path):
    """Analyze if PRP is being moved to completed"""
    if '/active/' in file_path and '/completed/' in file_path:
        return True
    return False

def main():
    """Main hook logic"""
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    # Get file path and operation
    file_path = input_data.get('path', '')
    tool = input_data.get('tool', '')
    
    # Track different types of operations
    if tool in ['write_file', 'edit_file', 'str_replace']:
        content = input_data.get('content', '')
        
        # Check if this is a PRP file
        prp_name = extract_prp_name(file_path)
        if prp_name:
            # Initialize or load metrics
            metrics = load_existing_metrics(prp_name) or {
                'created_at': datetime.now().isoformat(),
                'updates': 0,
                'validation_scores': {}
            }
            
            # Increment update counter
            metrics['updates'] += 1
            
            # Check for validation results in content
            validation_results = extract_validation_results(content)
            if any(v is not None for v in validation_results.values()):
                metrics['validation_scores'].update({
                    k: v for k, v in validation_results.items() if v is not None
                })
                
                # Check if all validations passed
                all_passed = all(
                    v >= 90 for v in validation_results.values() 
                    if v is not None
                )
                metrics['first_pass_success'] = all_passed
            
            # Check if PRP is being completed
            if analyze_prp_completion(file_path):
                metrics['completed_at'] = datetime.now().isoformat()
                
                # Calculate duration if we have start time
                if 'created_at' in metrics:
                    start = datetime.fromisoformat(metrics['created_at'])
                    end = datetime.now()
                    metrics['duration'] = (end - start).total_seconds()
            
            # Save metrics
            save_metrics(prp_name, metrics)
            
            # If PRP is completed, update the file with metrics
            if 'completed_at' in metrics:
                update_prp_with_metrics(file_path, metrics)
    
    # Check for test results that might indicate bugs
    elif tool == 'run_command':
        command = input_data.get('command', '')
        if 'test' in command or 'vitest' in command or 'playwright' in command:
            # Look for test failures in output
            output = input_data.get('output', '')
            if 'FAIL' in output or 'failed' in output.lower():
                # Try to associate with active PRP
                # This is a simple heuristic - could be improved
                active_prps = list(Path("PRPs/active").glob("*.md"))
                if active_prps:
                    # Update the most recent PRP
                    most_recent = max(active_prps, key=lambda p: p.stat().st_mtime)
                    prp_name = most_recent.stem
                    
                    metrics = load_existing_metrics(prp_name) or {}
                    metrics['test_failures'] = metrics.get('test_failures', 0) + 1
                    save_metrics(prp_name, metrics)
    
    # Always continue - this is a post-hook for collection only
    print(json.dumps({"action": "continue"}))

if __name__ == "__main__":
    main()
