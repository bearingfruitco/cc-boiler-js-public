#!/usr/bin/env python3
"""
TDD Progress Logger - Post-tool-use hook that logs all TDD activities
Part of v3.1 TDD Automation Enhancement - Issue #4
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
import uuid
import hashlib

def get_session_id():
    """Get or create session ID"""
    session_file = Path(".claude/state/current-session.json")
    
    if session_file.exists():
        try:
            with open(session_file) as f:
                data = json.load(f)
                return data.get('session_id', str(uuid.uuid4()))
        except:
            pass
    
    # Create new session ID
    session_id = str(uuid.uuid4())
    session_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(session_file, 'w') as f:
        json.dump({
            'session_id': session_id,
            'started': datetime.now().isoformat()
        }, f)
    
    return session_id

def detect_tdd_activity(tool_name, tool_input, tool_output):
    """Detect if this is a TDD-related activity"""
    tdd_indicators = {
        'test_generation': [
            'test', '.test.', '.spec.', '__tests__',
            'describe', 'it(', 'test(', 'expect'
        ],
        'implementation': [
            'export function', 'export const', 'export default',
            'implements', 'extends', 'return'
        ],
        'test_run': [
            'PASS', 'FAIL', '✓', '✗', 'passed', 'failed',
            'Test Suites:', 'Tests:'
        ],
        'coverage': [
            'Coverage', '%', 'Uncovered', 'Statements',
            'Branches', 'Functions', 'Lines'
        ]
    }
    
    # Check file path
    file_path = tool_input.get('file_path', '') if isinstance(tool_input, dict) else ''
    content = tool_input.get('content', '') if isinstance(tool_input, dict) else str(tool_input)
    output = str(tool_output) if tool_output else ''
    
    # Determine event type
    for event_type, indicators in tdd_indicators.items():
        if any(ind in file_path + content + output for ind in indicators):
            return event_type
    
    return None

def extract_feature_name(file_path, content=''):
    """Extract feature name from file path or content"""
    path = Path(file_path) if file_path else None
    
    if path:
        # Remove test suffixes
        name = path.stem.replace('.test', '').replace('.spec', '')
        return name
    
    # Try to extract from content
    if 'describe(' in content:
        # Extract from describe block
        import re
        match = re.search(r'describe\([\'"`]([^\'"`]+)', content)
        if match:
            return match.group(1)
    
    return 'unknown'

def parse_test_results(output):
    """Parse test runner output"""
    results = {
        'total_tests': 0,
        'passed': 0,
        'failed': 0,
        'skipped': 0,
        'duration_ms': 0
    }
    
    # Vitest pattern
    import re
    
    # Test count pattern
    test_match = re.search(r'Tests:\s+(\d+)\s+passed(?:,\s+(\d+)\s+failed)?(?:,\s+(\d+)\s+skipped)?', output)
    if test_match:
        results['passed'] = int(test_match.group(1))
        results['failed'] = int(test_match.group(2) or 0)
        results['skipped'] = int(test_match.group(3) or 0)
        results['total_tests'] = sum([results['passed'], results['failed'], results['skipped']])
    
    # Duration pattern
    duration_match = re.search(r'Duration\s+(\d+\.?\d*)\s*m?s', output)
    if duration_match:
        duration = float(duration_match.group(1))
        # Convert to ms if needed
        results['duration_ms'] = int(duration * 1000) if duration < 1000 else int(duration)
    
    return results

def parse_coverage_results(output):
    """Parse coverage output"""
    coverage = {
        'statements': 0,
        'branches': 0,
        'functions': 0,
        'lines': 0
    }
    
    import re
    
    # Coverage patterns
    patterns = {
        'statements': r'Statements\s*:\s*(\d+\.?\d*)%',
        'branches': r'Branches\s*:\s*(\d+\.?\d*)%',
        'functions': r'Functions\s*:\s*(\d+\.?\d*)%',
        'lines': r'Lines\s*:\s*(\d+\.?\d*)%'
    }
    
    for metric, pattern in patterns.items():
        match = re.search(pattern, output)
        if match:
            coverage[metric] = float(match.group(1))
    
    return coverage

def calculate_metrics(event_data):
    """Calculate metrics from event data"""
    metrics = {}
    
    if event_data['event_type'] == 'test_run':
        details = event_data['details']
        if details['total_tests'] > 0:
            metrics['pass_rate'] = (details['passed'] / details['total_tests']) * 100
            metrics['test_velocity'] = details['total_tests'] / (details['duration_ms'] / 1000) if details['duration_ms'] > 0 else 0
    
    elif event_data['event_type'] == 'coverage':
        details = event_data['details']
        # Overall coverage (average of all metrics)
        metrics['overall_coverage'] = sum(details.values()) / len(details) if details else 0
    
    return metrics

def log_event(event_data):
    """Log event to appropriate file"""
    # Determine log file
    date_str = datetime.now().strftime('%Y-%m-%d')
    log_dir = Path(f".claude/logs/progress/daily")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / f"tdd-{date_str}.jsonl"
    
    # Write event
    with open(log_file, 'a') as f:
        f.write(json.dumps(event_data) + '\n')
    
    # Also log to session file
    session_dir = Path(f".claude/logs/progress/sessions")
    session_dir.mkdir(parents=True, exist_ok=True)
    
    session_file = session_dir / f"{event_data['session_id']}.jsonl"
    with open(session_file, 'a') as f:
        f.write(json.dumps(event_data) + '\n')
    
    # Update metrics if applicable
    if 'metrics' in event_data:
        update_metrics(event_data)

def update_metrics(event_data):
    """Update metric files"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    if event_data['event_type'] == 'coverage':
        # Update coverage metrics
        coverage_dir = Path(".claude/logs/metrics/test-coverage")
        coverage_dir.mkdir(parents=True, exist_ok=True)
        
        coverage_file = coverage_dir / f"{date_str}.json"
        
        # Load existing or create new
        if coverage_file.exists():
            with open(coverage_file) as f:
                coverage_data = json.load(f)
        else:
            coverage_data = {'features': {}, 'timestamp': datetime.now().isoformat()}
        
        # Update
        feature = event_data['feature']
        coverage_data['features'][feature] = event_data['details']
        coverage_data['last_updated'] = datetime.now().isoformat()
        
        # Save
        with open(coverage_file, 'w') as f:
            json.dump(coverage_data, f, indent=2)
    
    elif event_data['event_type'] == 'test_run':
        # Update TDD compliance metrics
        compliance_dir = Path(".claude/logs/metrics/tdd-compliance")
        compliance_dir.mkdir(parents=True, exist_ok=True)
        
        compliance_file = compliance_dir / f"{date_str}.json"
        
        # Similar update process...

def main():
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        # Extract fields
        session_id = get_session_id()
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        tool_output = input_data.get('tool_output', '')
        
        # Detect TDD activity
        event_type = detect_tdd_activity(tool_name, tool_input, tool_output)
        
        if not event_type:
            # Not TDD related
            sys.exit(1)
        
        # Extract feature name
        file_path = tool_input.get('file_path', '') if isinstance(tool_input, dict) else ''
        content = tool_input.get('content', '') if isinstance(tool_input, dict) else ''
        feature_name = extract_feature_name(file_path, content)
        
        # Build event data
        event_data = {
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'feature': feature_name,
            'event_type': event_type,
            'status': 'completed',  # Post-tool-use means it completed
            'details': {},
            'metadata': {
                'tool': tool_name,
                'file_path': file_path
            }
        }
        
        # Parse type-specific details
        if event_type == 'test_run' and tool_output:
            test_results = parse_test_results(str(tool_output))
            event_data['details'] = test_results
            event_data['metadata']['test_count'] = test_results['total_tests']
        
        elif event_type == 'coverage' and tool_output:
            coverage_results = parse_coverage_results(str(tool_output))
            event_data['details'] = coverage_results
            event_data['metadata']['coverage_percentage'] = coverage_results.get('lines', 0)
        
        elif event_type == 'test_generation':
            # Count generated tests
            if content:
                test_count = content.count('test(') + content.count('it(')
                event_data['metadata']['test_count'] = test_count
                event_data['details']['generated_tests'] = test_count
        
        # Calculate metrics
        metrics = calculate_metrics(event_data)
        if metrics:
            event_data['metrics'] = metrics
        
        # Log the event
        log_event(event_data)
        
        # Update dashboard data
        dashboard_file = Path(".claude/logs/dashboards/current.json")
        dashboard_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Simple dashboard update (last 10 events)
        if dashboard_file.exists():
            with open(dashboard_file) as f:
                dashboard = json.load(f)
        else:
            dashboard = {'events': [], 'updated': datetime.now().isoformat()}
        
        # Add event summary
        dashboard['events'].insert(0, {
            'timestamp': event_data['timestamp'],
            'feature': feature_name,
            'type': event_type,
            'status': event_data['status']
        })
        
        # Keep only last 10
        dashboard['events'] = dashboard['events'][:10]
        dashboard['updated'] = datetime.now().isoformat()
        
        with open(dashboard_file, 'w') as f:
            json.dump(dashboard, f, indent=2)
        
        # Exit successfully
        sys.exit(0)
        
    except Exception as e:
        # Log error but don't block
        error_log = Path(".claude/logs/errors.log")
        error_log.parent.mkdir(parents=True, exist_ok=True)
        
        with open(error_log, 'a') as f:
            f.write(f"{datetime.now()}: TDD progress logger error - {str(e)}\n")
        
        sys.exit(1)

if __name__ == "__main__":
    main()
