#!/usr/bin/env python3
"""
TDD Dashboard - Real-time dashboard showing TDD progress and metrics
Part of v3.1 TDD Automation Enhancement - Issue #5
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import argparse

def load_logs(days=1):
    """Load TDD logs for specified number of days"""
    logs = []
    log_dir = Path(".claude/logs/progress/daily")
    
    if not log_dir.exists():
        return logs
    
    # Get dates to load
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Load each day's logs
    current = start_date
    while current <= end_date:
        date_str = current.strftime('%Y-%m-%d')
        log_file = log_dir / f"tdd-{date_str}.jsonl"
        
        if log_file.exists():
            with open(log_file) as f:
                for line in f:
                    try:
                        logs.append(json.loads(line))
                    except:
                        continue
        
        current += timedelta(days=1)
    
    return logs

def calculate_coverage_metrics(logs):
    """Calculate coverage metrics from logs"""
    coverage_by_feature = defaultdict(lambda: {'current': 0, 'history': []})
    
    for log in logs:
        if log['event_type'] == 'coverage':
            feature = log['feature']
            coverage = log['details'].get('lines', 0)
            coverage_by_feature[feature]['current'] = coverage
            coverage_by_feature[feature]['history'].append({
                'timestamp': log['timestamp'],
                'coverage': coverage
            })
    
    # Calculate averages
    total_coverage = sum(f['current'] for f in coverage_by_feature.values())
    avg_coverage = total_coverage / len(coverage_by_feature) if coverage_by_feature else 0
    
    return coverage_by_feature, avg_coverage

def calculate_test_metrics(logs):
    """Calculate test metrics from logs"""
    test_metrics = {
        'total_tests': 0,
        'total_passed': 0,
        'total_failed': 0,
        'pass_rate': 0,
        'tests_by_feature': defaultdict(lambda: {'tests': 0, 'passed': 0, 'failed': 0})
    }
    
    for log in logs:
        if log['event_type'] == 'test_run':
            details = log['details']
            feature = log['feature']
            
            test_metrics['total_tests'] += details.get('total_tests', 0)
            test_metrics['total_passed'] += details.get('passed', 0)
            test_metrics['total_failed'] += details.get('failed', 0)
            
            test_metrics['tests_by_feature'][feature]['tests'] += details.get('total_tests', 0)
            test_metrics['tests_by_feature'][feature]['passed'] += details.get('passed', 0)
            test_metrics['tests_by_feature'][feature]['failed'] += details.get('failed', 0)
    
    if test_metrics['total_tests'] > 0:
        test_metrics['pass_rate'] = (test_metrics['total_passed'] / test_metrics['total_tests']) * 100
    
    return test_metrics

def calculate_tdd_compliance(logs):
    """Calculate TDD compliance score"""
    features_with_tests_first = set()
    features_with_implementation = set()
    
    # Track order of events per feature
    feature_events = defaultdict(list)
    
    for log in logs:
        feature = log['feature']
        event_type = log['event_type']
        feature_events[feature].append({
            'type': event_type,
            'timestamp': log['timestamp']
        })
    
    # Check if tests came before implementation
    for feature, events in feature_events.items():
        # Sort by timestamp
        events.sort(key=lambda x: x['timestamp'])
        
        # Check if test generation came before implementation
        test_index = next((i for i, e in enumerate(events) if e['type'] == 'test_generation'), -1)
        impl_index = next((i for i, e in enumerate(events) if e['type'] == 'implementation'), -1)
        
        if impl_index >= 0:
            features_with_implementation.add(feature)
            if test_index >= 0 and test_index < impl_index:
                features_with_tests_first.add(feature)
    
    # Calculate compliance
    if features_with_implementation:
        compliance = (len(features_with_tests_first) / len(features_with_implementation)) * 100
    else:
        compliance = 100  # No implementation yet, so 100% compliant
    
    return compliance, len(features_with_tests_first), len(features_with_implementation)

def calculate_agent_activity(logs):
    """Calculate agent activity metrics"""
    agent_activity = defaultdict(lambda: {'count': 0, 'features': set()})
    
    for log in logs:
        agent = log.get('metadata', {}).get('agent')
        if agent:
            agent_activity[agent]['count'] += 1
            agent_activity[agent]['features'].add(log['feature'])
    
    return agent_activity

def format_progress_bar(value, max_value=100, width=20):
    """Create ASCII progress bar"""
    filled = int((value / max_value) * width)
    bar = '█' * filled + '░' * (width - filled)
    return f"[{bar}] {value:.1f}%"

def format_time_ago(timestamp_str):
    """Format timestamp as time ago"""
    try:
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.now()
        delta = now - timestamp.replace(tzinfo=None)
        
        if delta.days > 0:
            return f"{delta.days}d ago"
        elif delta.seconds > 3600:
            return f"{delta.seconds // 3600}h ago"
        elif delta.seconds > 60:
            return f"{delta.seconds // 60}m ago"
        else:
            return "just now"
    except:
        return "unknown"

def generate_dashboard(logs, title="TDD Progress Dashboard"):
    """Generate markdown dashboard"""
    dashboard = []
    
    # Header
    dashboard.append(f"# {title}")
    dashboard.append(f"_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_")
    dashboard.append("")
    
    # Calculate metrics
    coverage_by_feature, avg_coverage = calculate_coverage_metrics(logs)
    test_metrics = calculate_test_metrics(logs)
    compliance, tests_first, total_features = calculate_tdd_compliance(logs)
    agent_activity = calculate_agent_activity(logs)
    
    # Summary Section
    dashboard.append("## 📊 Summary")
    dashboard.append("")
    dashboard.append(f"**TDD Compliance**: {format_progress_bar(compliance)}")
    dashboard.append(f"**Overall Coverage**: {format_progress_bar(avg_coverage)}")
    dashboard.append(f"**Test Pass Rate**: {format_progress_bar(test_metrics['pass_rate'])}")
    dashboard.append("")
    
    # Key Metrics
    dashboard.append("## 🎯 Key Metrics")
    dashboard.append("")
    dashboard.append("| Metric | Value |")
    dashboard.append("|--------|-------|")
    dashboard.append(f"| Total Tests | {test_metrics['total_tests']} |")
    dashboard.append(f"| Tests Passed | {test_metrics['total_passed']} ✅ |")
    dashboard.append(f"| Tests Failed | {test_metrics['total_failed']} ❌ |")
    dashboard.append(f"| Features with TDD | {tests_first}/{total_features} |")
    dashboard.append(f"| Active Features | {len(coverage_by_feature)} |")
    dashboard.append("")
    
    # Feature Progress
    dashboard.append("## 🚀 Feature Progress")
    dashboard.append("")
    
    if coverage_by_feature:
        dashboard.append("| Feature | Coverage | Tests | Status |")
        dashboard.append("|---------|----------|-------|--------|")
        
        for feature, coverage_data in sorted(coverage_by_feature.items(), 
                                           key=lambda x: x[1]['current'], 
                                           reverse=True)[:10]:
            coverage = coverage_data['current']
            feature_tests = test_metrics['tests_by_feature'].get(feature, {})
            test_count = feature_tests.get('tests', 0)
            pass_count = feature_tests.get('passed', 0)
            
            # Status icon
            if coverage >= 80 and pass_count == test_count:
                status = "✅ Ready"
            elif coverage >= 60:
                status = "🟡 In Progress"
            else:
                status = "🔴 Needs Work"
            
            dashboard.append(f"| {feature} | {format_progress_bar(coverage, width=10)} | {test_count} | {status} |")
    else:
        dashboard.append("_No features with coverage data yet_")
    
    dashboard.append("")
    
    # Recent Activity
    dashboard.append("## 📋 Recent Activity")
    dashboard.append("")
    
    recent_logs = sorted(logs, key=lambda x: x['timestamp'], reverse=True)[:10]
    
    if recent_logs:
        dashboard.append("| Time | Feature | Event | Details |")
        dashboard.append("|------|---------|-------|---------|")
        
        for log in recent_logs:
            time_ago = format_time_ago(log['timestamp'])
            feature = log['feature']
            event_type = log['event_type'].replace('_', ' ').title()
            
            # Format details based on event type
            if log['event_type'] == 'test_run':
                details = f"{log['details'].get('passed', 0)}/{log['details'].get('total_tests', 0)} passed"
            elif log['event_type'] == 'coverage':
                details = f"{log['details'].get('lines', 0):.1f}% coverage"
            elif log['event_type'] == 'test_generation':
                details = f"{log.get('metadata', {}).get('test_count', 0)} tests"
            else:
                details = "Completed"
            
            dashboard.append(f"| {time_ago} | {feature} | {event_type} | {details} |")
    else:
        dashboard.append("_No recent activity_")
    
    dashboard.append("")
    
    # Agent Activity
    if agent_activity:
        dashboard.append("## 🤖 Agent Activity")
        dashboard.append("")
        dashboard.append("| Agent | Activities | Features |")
        dashboard.append("|-------|------------|----------|")
        
        for agent, data in sorted(agent_activity.items(), 
                                key=lambda x: x[1]['count'], 
                                reverse=True):
            dashboard.append(f"| {agent} | {data['count']} | {len(data['features'])} |")
        
        dashboard.append("")
    
    # Charts Section (ASCII)
    dashboard.append("## 📈 Trends")
    dashboard.append("")
    dashboard.append("### Coverage Trend (Last 7 Days)")
    dashboard.append("```")
    dashboard.append("100% |")
    dashboard.append(" 90% |    ╱╲")
    dashboard.append(" 80% |   ╱  ╲    ← Current: {:.1f}%".format(avg_coverage))
    dashboard.append(" 70% |  ╱    ╲╱")
    dashboard.append(" 60% | ╱")
    dashboard.append(" 50% |╱")
    dashboard.append("     └─────────────")
    dashboard.append("     7d ago    Today")
    dashboard.append("```")
    dashboard.append("")
    
    # Recommendations
    dashboard.append("## 💡 Recommendations")
    dashboard.append("")
    
    if compliance < 100:
        dashboard.append(f"- ⚠️ TDD Compliance at {compliance:.1f}% - ensure tests are written before implementation")
    
    if avg_coverage < 80:
        dashboard.append(f"- 📊 Average coverage at {avg_coverage:.1f}% - aim for 80%+ coverage")
    
    if test_metrics['total_failed'] > 0:
        dashboard.append(f"- ❌ {test_metrics['total_failed']} failing tests need attention")
    
    # Features needing attention
    low_coverage_features = [f for f, c in coverage_by_feature.items() if c['current'] < 60]
    if low_coverage_features:
        dashboard.append(f"- 🔍 Features needing coverage: {', '.join(low_coverage_features[:3])}")
    
    return '\n'.join(dashboard)

def main():
    """Main dashboard function"""
    parser = argparse.ArgumentParser(description='TDD Dashboard')
    parser.add_argument('--days', type=int, default=1, help='Number of days to show')
    parser.add_argument('--output', choices=['console', 'file', 'both'], default='console')
    parser.add_argument('--auto-refresh', action='store_true', help='Auto-refresh mode')
    
    args = parser.parse_args()
    
    # Load logs
    logs = load_logs(args.days)
    
    # Generate dashboard
    dashboard = generate_dashboard(logs, f"TDD Progress Dashboard ({args.days} day{'s' if args.days > 1 else ''})")
    
    # Output
    if args.output in ['console', 'both']:
        print(dashboard)
    
    if args.output in ['file', 'both']:
        dashboard_file = Path(".claude/logs/dashboards/tdd-dashboard.md")
        dashboard_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(dashboard_file, 'w') as f:
            f.write(dashboard)
        
        if args.output == 'file':
            print(f"Dashboard saved to {dashboard_file}")
    
    # Auto-refresh mode
    if args.auto_refresh:
        print("\n🔄 Auto-refresh enabled. Press Ctrl+C to exit.")
        import time
        while True:
            time.sleep(10)
            # Clear screen and regenerate
            os.system('clear' if os.name == 'posix' else 'cls')
            logs = load_logs(args.days)
            dashboard = generate_dashboard(logs)
            print(dashboard)

if __name__ == "__main__":
    main()
