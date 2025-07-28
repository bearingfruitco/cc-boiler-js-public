---
name: agent-stats
description: View performance metrics for persona agents
argument-hint: <agent-name> [--last-7d | --last-30d | --all]
allowed-tools: Read, Bash
aliases: ["stats", "metrics", "agent-metrics"]
---

# 📊 Agent Performance Statistics

Analyzing agent metrics: **$ARGUMENTS**

## Loading Performance Data

!`python3 << 'PYTHON'
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Parse arguments
args = """$ARGUMENTS""".strip().split()
agent_name = args[0] if args else "all"
time_range = args[1] if len(args) > 1 else "--last-7d"

# Metrics directory
metrics_dir = Path(".claude/metrics/agents")

def calculate_success_rate(metrics):
    """Calculate success rate from metrics"""
    total = metrics.get('total_tasks', 0)
    if total == 0:
        return 0
    # For now, estimate success rate based on task completion
    # This will be improved when we add success tracking
    return 0.85  # Placeholder

def get_time_filtered_history(history, days):
    """Filter history by time range"""
    cutoff = datetime.now() - timedelta(days=days)
    filtered = []
    for entry in history:
        try:
            entry_time = datetime.fromisoformat(entry['timestamp'])
            if entry_time >= cutoff:
                filtered.append(entry)
        except:
            continue
    return filtered

def format_duration(seconds):
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"

# Load metrics
if agent_name == "all":
    # Show summary for all agents
    print("# 📊 All Agents Performance Summary\n")
    
    agent_files = list(metrics_dir.glob("*.json"))
    if not agent_files:
        print("ℹ️ No agent metrics found yet. Metrics will be collected as agents are used.")
        sys.exit(0)
    
    print("| Agent | Total Tasks | Success Rate | Most Common Task | Last Active |")
    print("|-------|------------|--------------|------------------|-------------|")
    
    for agent_file in sorted(agent_files):
        with open(agent_file, 'r') as f:
            metrics = json.load(f)
        
        agent = metrics['agent']
        total_tasks = metrics['total_tasks']
        success_rate = calculate_success_rate(metrics)
        
        # Find most common task type
        task_types = metrics.get('task_types', {})
        most_common = max(task_types.items(), key=lambda x: x[1]['count'])[0] if task_types else "N/A"
        
        last_updated = metrics.get('last_updated', 'Never')
        if last_updated != 'Never':
            last_updated = datetime.fromisoformat(last_updated).strftime('%Y-%m-%d %H:%M')
        
        print(f"| {agent} | {total_tasks} | {success_rate:.1%} | {most_common} | {last_updated} |")
    
else:
    # Show detailed stats for specific agent
    agent_file = metrics_dir / f"{agent_name}.json"
    
    if not agent_file.exists():
        print(f"ℹ️ No metrics found for agent '{agent_name}'")
        print("\nAvailable agents:")
        for f in metrics_dir.glob("*.json"):
            print(f"  - {f.stem}")
        sys.exit(0)
    
    with open(agent_file, 'r') as f:
        metrics = json.load(f)
    
    print(f"# 📊 {agent_name.title()} Agent Performance\n")
    
    # Time filtering
    days_map = {
        '--last-7d': 7,
        '--last-30d': 30,
        '--all': None
    }
    
    filter_days = days_map.get(time_range, 7)
    
    # Basic stats
    print("## Overview")
    print(f"- **Total Tasks**: {metrics['total_tasks']}")
    print(f"- **Success Rate**: {calculate_success_rate(metrics):.1%}")
    print(f"- **Last Active**: {metrics.get('last_updated', 'Never')}")
    
    # Task type breakdown
    print("\n## Task Type Performance")
    task_types = metrics.get('task_types', {})
    if task_types:
        print("| Task Type | Count | % of Total |")
        print("|-----------|-------|------------|")
        
        total = sum(t['count'] for t in task_types.values())
        for task_type, data in sorted(task_types.items(), key=lambda x: x[1]['count'], reverse=True):
            percentage = (data['count'] / total * 100) if total > 0 else 0
            print(f"| {task_type.replace('_', ' ').title()} | {data['count']} | {percentage:.1f}% |")
    
    # Recent history
    print("\n## Recent Activity")
    history = metrics.get('performance_history', [])
    
    if filter_days:
        history = get_time_filtered_history(history, filter_days)
        print(f"*Showing last {filter_days} days*\n")
    
    if history:
        # Show last 10 entries
        for entry in history[-10:]:
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%m/%d %H:%M')
            task_type = entry['task_type'].replace('_', ' ').title()
            prompt = entry['prompt_preview']
            print(f"- **{timestamp}** [{task_type}]: {prompt}")
    else:
        print("No recent activity in selected time range")
    
    # Recommendations
    print("\n## 💡 Performance Insights")
    
    if metrics['total_tasks'] > 10:
        # Find best performing task types
        best_task = max(task_types.items(), key=lambda x: x[1]['count'])[0] if task_types else None
        if best_task:
            print(f"- ✅ {agent_name} excels at **{best_task.replace('_', ' ')}** tasks")
        
        # Suggest optimizations
        if metrics['total_tasks'] > 50:
            print(f"- 📈 High usage agent - consider creating specialized sub-agents for common patterns")
        
        # Activity patterns
        if history:
            recent_types = [h['task_type'] for h in history[-20:]]
            most_recent_common = max(set(recent_types), key=recent_types.count)
            print(f"- 🔄 Recent trend: Increasing **{most_recent_common.replace('_', ' ')}** tasks")
    else:
        print(f"- ℹ️ Need more data (only {metrics['total_tasks']} tasks recorded)")

PYTHON`

## Next Steps

- View specific agent: `/agent-stats frontend`
- Compare agents: `/agent-report --compare`
- Real-time monitoring: `/agent-monitor`
- Export metrics: `/agent-export`
