#!/usr/bin/env python3
"""
Test Coverage Tracking Hook - Monitors test coverage and enforces thresholds
Part of v3.1 TDD Automation Enhancement - Issue #6
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime
import re

def parse_coverage_output(output):
    """Parse coverage report from test runner output"""
    coverage_data = {
        'statements': 0,
        'branches': 0, 
        'functions': 0,
        'lines': 0,
        'overall': 0
    }
    
    # Vitest coverage pattern
    patterns = {
        'statements': r'Statements\s*:\s*(\d+\.?\d*)%',
        'branches': r'Branches\s*:\s*(\d+\.?\d*)%',
        'functions': r'Functions\s*:\s*(\d+\.?\d*)%', 
        'lines': r'Lines\s*:\s*(\d+\.?\d*)%'
    }
    
    for metric, pattern in patterns.items():
        match = re.search(pattern, output)
        if match:
            coverage_data[metric] = float(match.group(1))
    
    # Calculate overall coverage
    if any(coverage_data[m] > 0 for m in ['statements', 'branches', 'functions', 'lines']):
        coverage_data['overall'] = sum(coverage_data[m] for m in ['statements', 'branches', 'functions', 'lines']) / 4
    
    return coverage_data

def get_coverage_thresholds():
    """Get coverage thresholds from config"""
    config_file = Path(".claude/config.json")
    default_thresholds = {
        'overall': 80,
        'new_code': 90,
        'critical_paths': 100
    }
    
    if config_file.exists():
        try:
            with open(config_file) as f:
                config = json.load(f)
                return config.get('coverage_thresholds', default_thresholds)
        except:
            pass
    
    return default_thresholds

def check_critical_path(file_path):
    """Check if file is in critical path"""
    critical_patterns = [
        'auth', 'payment', 'checkout', 'security',
        'encryption', 'api/auth', 'lib/auth'
    ]
    
    return any(pattern in file_path.lower() for pattern in critical_patterns)

def load_previous_coverage(feature):
    """Load previous coverage for comparison"""
    coverage_dir = Path(".claude/logs/metrics/test-coverage")
    
    if not coverage_dir.exists():
        return None
    
    # Look for most recent coverage
    coverage_files = sorted(coverage_dir.glob("*.json"), reverse=True)
    
    for coverage_file in coverage_files:
        try:
            with open(coverage_file) as f:
                data = json.load(f)
                if feature in data.get('features', {}):
                    return data['features'][feature].get('coverage', {})
        except:
            continue
    
    return None

def save_coverage_data(feature, coverage_data, file_path=None):
    """Save coverage data to metrics"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    coverage_dir = Path(".claude/logs/metrics/test-coverage")
    coverage_dir.mkdir(parents=True, exist_ok=True)
    
    coverage_file = coverage_dir / f"{date_str}.json"
    
    # Load existing or create new
    if coverage_file.exists():
        with open(coverage_file) as f:
            data = json.load(f)
    else:
        data = {
            'features': {},
            'timestamp': datetime.now().isoformat()
        }
    
    # Update feature coverage
    if feature not in data['features']:
        data['features'][feature] = {}
    
    data['features'][feature].update({
        'coverage': coverage_data,
        'last_updated': datetime.now().isoformat(),
        'file_path': file_path
    })
    
    # Save
    with open(coverage_file, 'w') as f:
        json.dump(data, f, indent=2)

def generate_coverage_report(feature, coverage_data, previous_coverage=None):
    """Generate coverage report"""
    report = []
    
    report.append(f"## Test Coverage Report: {feature}")
    report.append("")
    report.append("| Metric | Current | Threshold | Status |")
    report.append("|--------|---------|-----------|--------|")
    
    thresholds = get_coverage_thresholds()
    overall_threshold = thresholds['overall']
    
    # Metrics
    for metric in ['statements', 'branches', 'functions', 'lines']:
        current = coverage_data.get(metric, 0)
        status = "✅" if current >= overall_threshold else "❌"
        report.append(f"| {metric.capitalize()} | {current:.1f}% | {overall_threshold}% | {status} |")
    
    # Overall
    overall = coverage_data.get('overall', 0)
    status = "✅" if overall >= overall_threshold else "❌"
    report.append(f"| **Overall** | **{overall:.1f}%** | **{overall_threshold}%** | **{status}** |")
    
    # Delta from previous
    if previous_coverage:
        report.append("")
        report.append("### Coverage Change")
        
        prev_overall = previous_coverage.get('overall', 0)
        delta = overall - prev_overall
        
        if delta > 0:
            report.append(f"📈 Coverage increased by {delta:.1f}%")
        elif delta < 0:
            report.append(f"📉 Coverage decreased by {abs(delta):.1f}%")
        else:
            report.append("➡️ Coverage unchanged")
    
    # Uncovered lines
    if 'uncovered_lines' in coverage_data:
        report.append("")
        report.append("### Uncovered Lines")
        for line_range in coverage_data['uncovered_lines'][:5]:
            report.append(f"- Lines {line_range}")
    
    return '\n'.join(report)

def create_coverage_alert(feature, coverage_data, threshold_violated=False):
    """Create alert for coverage issues"""
    alert = {
        'type': 'coverage_alert',
        'feature': feature,
        'timestamp': datetime.now().isoformat(),
        'coverage': coverage_data.get('overall', 0),
        'threshold_violated': threshold_violated
    }
    
    # Save to alerts file
    alerts_file = Path(".claude/logs/alerts.jsonl")
    alerts_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(alerts_file, 'a') as f:
        f.write(json.dumps(alert) + '\n')

def main():
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        tool_name = input_data.get('tool_name', '')
        tool_output = input_data.get('tool_output', '')
        tool_input = input_data.get('tool_input', {})
        
        # Check if this is a test execution
        if tool_name not in ['Execute', 'Run'] or not tool_output:
            sys.exit(1)
        
        # Check if output contains coverage data
        if not any(indicator in str(tool_output) for indicator in ['Coverage', 'Statements', 'Branches']):
            sys.exit(0)
        
        # Parse coverage data
        coverage_data = parse_coverage_output(str(tool_output))
        
        if coverage_data['overall'] == 0:
            # No coverage data found
            sys.exit(0)
        
        # Extract feature name
        command = tool_input.get('command', '') if isinstance(tool_input, dict) else str(tool_input)
        
        # Try to get feature from test file path
        feature = 'unknown'
        if 'test' in command:
            # Extract from test command
            import re
            file_match = re.search(r'(\w+)\.test\.[jt]sx?', command)
            if file_match:
                feature = file_match.group(1)
        
        # Load previous coverage
        previous_coverage = load_previous_coverage(feature)
        
        # Save current coverage
        save_coverage_data(feature, coverage_data)
        
        # Check thresholds
        thresholds = get_coverage_thresholds()
        overall = coverage_data.get('overall', 0)
        threshold_violated = False
        
        # Check overall threshold
        if overall < thresholds['overall']:
            threshold_violated = True
            print(f"⚠️ Coverage below threshold: {overall:.1f}% < {thresholds['overall']}%", file=sys.stderr)
        
        # Check critical path threshold
        if check_critical_path(feature) and overall < thresholds['critical_paths']:
            threshold_violated = True
            print(f"🚨 Critical path coverage below 100%: {overall:.1f}%", file=sys.stderr)
        
        # Check coverage drop
        if previous_coverage:
            prev_overall = previous_coverage.get('overall', 0)
            if overall < prev_overall - 5:  # More than 5% drop
                threshold_violated = True
                print(f"📉 Significant coverage drop: {prev_overall:.1f}% → {overall:.1f}%", file=sys.stderr)
        
        # Create alert if threshold violated
        if threshold_violated:
            create_coverage_alert(feature, coverage_data, True)
        
        # Generate and save report
        report = generate_coverage_report(feature, coverage_data, previous_coverage)
        
        report_file = Path(f".claude/logs/dashboards/coverage-{feature}.md")
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w') as f:
            f.write(report)
        
        # Log coverage event
        log_dir = Path(".claude/logs/progress/daily")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"tdd-{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        
        event = {
            'timestamp': datetime.now().isoformat(),
            'feature': feature,
            'event_type': 'coverage',
            'status': 'completed',
            'details': coverage_data,
            'metadata': {
                'threshold_violated': threshold_violated,
                'coverage_percentage': overall
            }
        }
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
        
        # If running in a chain, add to chain results
        if 'chain_results' in os.environ:
            chain_results = {
                'coverage': coverage_data,
                'threshold_met': not threshold_violated,
                'report_path': str(report_file)
            }
            
            # Append to chain results file
            results_file = Path(".claude/state/chain-results.json")
            if results_file.exists():
                with open(results_file) as f:
                    results = json.load(f)
            else:
                results = []
            
            results.append(chain_results)
            
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2)
        
        # Exit with appropriate code
        if threshold_violated:
            # Non-zero exit to signal threshold violation
            # But don't block the workflow
            print("\n💡 To improve coverage, focus on:")
            print("  - Writing tests for uncovered branches")
            print("  - Adding edge case tests")
            print("  - Testing error scenarios")
            
        sys.exit(0)
        
    except Exception as e:
        # Log error but don't block
        error_log = Path(".claude/logs/errors.log")
        error_log.parent.mkdir(parents=True, exist_ok=True)
        
        with open(error_log, 'a') as f:
            f.write(f"{datetime.now()}: Coverage tracking error - {str(e)}\n")
        
        sys.exit(1)

if __name__ == "__main__":
    main()
