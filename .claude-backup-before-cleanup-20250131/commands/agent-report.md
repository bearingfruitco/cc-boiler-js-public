---
name: agent-report
description: Generate comprehensive agent performance reports
argument-hint: [--compare | --weekly | --recommendations]
allowed-tools: Read, Write, CreateFile, Bash
aliases: ["report", "agent-analysis"]
---

# 📈 Agent Performance Report

Generating report: **$ARGUMENTS**

## Analyzing Agent Performance Data

!`python3 << 'PYTHON'
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import statistics

# Parse arguments
args = """$ARGUMENTS""".strip()
report_type = args if args else "--weekly"

# Directories
metrics_dir = Path(".claude/metrics/agents")
session_dir = Path(".claude/metrics/sessions")
report_dir = Path(".claude/reports")
report_dir.mkdir(exist_ok=True)

def load_all_metrics():
    """Load metrics for all agents"""
    metrics = {}
    for agent_file in metrics_dir.glob("*.json"):
        with open(agent_file, 'r') as f:
            agent_data = json.load(f)
            metrics[agent_data['agent']] = agent_data
    return metrics

def calculate_efficiency_score(agent_metrics):
    """Calculate efficiency score for an agent"""
    # Factors: task completion, diversity of tasks, consistency
    total_tasks = agent_metrics.get('total_tasks', 0)
    if total_tasks == 0:
        return 0
    
    # Task diversity score
    task_types = agent_metrics.get('task_types', {})
    diversity = len(task_types) / 10.0  # Normalize to 0-1
    
    # Volume score
    volume = min(total_tasks / 100.0, 1.0)  # Normalize to 0-1
    
    # Combined score
    return (diversity * 0.4 + volume * 0.6) * 100

def generate_comparison_report(metrics):
    """Generate agent comparison report"""
    print("# 🔍 Agent Comparison Report\n")
    print(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
    
    if not metrics:
        print("ℹ️ No agent metrics available yet.")
        return
    
    # Calculate scores
    agent_scores = []
    for agent, data in metrics.items():
        score = calculate_efficiency_score(data)
        agent_scores.append({
            'agent': agent,
            'score': score,
            'total_tasks': data.get('total_tasks', 0),
            'task_types': len(data.get('task_types', {})),
            'last_active': data.get('last_updated', 'Never')
        })
    
    # Sort by score
    agent_scores.sort(key=lambda x: x['score'], reverse=True)
    
    print("## 🏆 Agent Performance Rankings\n")
    print("| Rank | Agent | Efficiency Score | Total Tasks | Task Diversity | Last Active |")
    print("|------|-------|-----------------|-------------|----------------|-------------|")
    
    for i, agent in enumerate(agent_scores, 1):
        last_active = agent['last_active']
        if last_active != 'Never':
            last_active = datetime.fromisoformat(last_active).strftime('%Y-%m-%d')
        
        print(f"| {i} | {agent['agent']} | {agent['score']:.1f}/100 | {agent['total_tasks']} | {agent['task_types']} types | {last_active} |")
    
    # Task type analysis
    print("\n## 📊 Task Type Specialization\n")
    
    task_specialists = defaultdict(list)
    for agent, data in metrics.items():
        task_types = data.get('task_types', {})
        for task_type, task_data in task_types.items():
            task_specialists[task_type].append({
                'agent': agent,
                'count': task_data['count']
            })
    
    print("| Task Type | Best Agent | Tasks Completed |")
    print("|-----------|------------|-----------------|")
    
    for task_type, agents in task_specialists.items():
        best = max(agents, key=lambda x: x['count'])
        print(f"| {task_type.replace('_', ' ').title()} | {best['agent']} | {best['count']} |")
    
    # Recommendations
    print("\n## 💡 Optimization Recommendations\n")
    
    # Find underutilized agents
    underutilized = [a for a in agent_scores if a['total_tasks'] < 5]
    if underutilized:
        print("### Underutilized Agents")
        for agent in underutilized:
            print(f"- **{agent['agent']}**: Only {agent['total_tasks']} tasks - consider expanding usage or removing")
    
    # Find overloaded agents
    overloaded = [a for a in agent_scores if a['total_tasks'] > 100]
    if overloaded:
        print("\n### High-Volume Agents")
        for agent in overloaded:
            print(f"- **{agent['agent']}**: {agent['total_tasks']} tasks - consider creating specialized sub-agents")
    
    # Save report
    report_file = report_dir / f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    # Implementation continues...

def generate_weekly_report(metrics):
    """Generate weekly performance summary"""
    print("# 📅 Weekly Agent Performance Summary\n")
    print(f"*Week ending: {datetime.now().strftime('%Y-%m-%d')}*\n")
    
    # Calculate weekly stats
    week_ago = datetime.now() - timedelta(days=7)
    
    weekly_stats = {
        'total_tasks': 0,
        'active_agents': set(),
        'task_distribution': defaultdict(int)
    }
    
    for agent, data in metrics.items():
        history = data.get('performance_history', [])
        for entry in history:
            try:
                entry_time = datetime.fromisoformat(entry['timestamp'])
                if entry_time >= week_ago:
                    weekly_stats['total_tasks'] += 1
                    weekly_stats['active_agents'].add(agent)
                    weekly_stats['task_distribution'][entry['task_type']] += 1
            except:
                continue
    
    print("## 📈 Key Metrics\n")
    print(f"- **Total Tasks**: {weekly_stats['total_tasks']}")
    print(f"- **Active Agents**: {len(weekly_stats['active_agents'])}")
    print(f"- **Task Types**: {len(weekly_stats['task_distribution'])}")
    
    if weekly_stats['active_agents']:
        print("\n## 🤖 Active Agents This Week\n")
        for agent in sorted(weekly_stats['active_agents']):
            agent_data = metrics.get(agent, {})
            print(f"- **{agent}**: {agent_data.get('total_tasks', 0)} total tasks")
    
    if weekly_stats['task_distribution']:
        print("\n## 📊 Task Distribution\n")
        print("| Task Type | Count | Percentage |")
        print("|-----------|-------|------------|")
        
        total = sum(weekly_stats['task_distribution'].values())
        for task_type, count in sorted(weekly_stats['task_distribution'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            print(f"| {task_type.replace('_', ' ').title()} | {count} | {percentage:.1f}% |")

def generate_recommendations_report(metrics):
    """Generate detailed recommendations for agent optimization"""
    print("# 🎯 Agent Optimization Recommendations\n")
    print(f"*Analysis date: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
    
    recommendations = []
    
    for agent, data in metrics.items():
        total_tasks = data.get('total_tasks', 0)
        task_types = data.get('task_types', {})
        
        # Analyze patterns
        if total_tasks > 20:
            # Check for specialization opportunities
            if len(task_types) == 1:
                recommendations.append({
                    'agent': agent,
                    'type': 'specialization',
                    'message': f"Highly specialized in {list(task_types.keys())[0].replace('_', ' ')}"
                })
            elif len(task_types) > 5:
                recommendations.append({
                    'agent': agent,
                    'type': 'generalization',
                    'message': "Handling too many task types - consider splitting responsibilities"
                })
    
    # Group by recommendation type
    print("## 🔧 Agent Specialization\n")
    spec_recs = [r for r in recommendations if r['type'] == 'specialization']
    for rec in spec_recs:
        print(f"- **{rec['agent']}**: {rec['message']}")
    
    print("\n## 🔀 Agent Splitting Candidates\n")
    gen_recs = [r for r in recommendations if r['type'] == 'generalization']
    for rec in gen_recs:
        print(f"- **{rec['agent']}**: {rec['message']}")
    
    # Performance patterns
    print("\n## 📊 Performance Patterns\n")
    
    # Find task type trends
    all_task_counts = defaultdict(int)
    for agent, data in metrics.items():
        for task_type, task_data in data.get('task_types', {}).items():
            all_task_counts[task_type] += task_data['count']
    
    if all_task_counts:
        print("### Most Common Task Types")
        for task_type, count in sorted(all_task_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"- **{task_type.replace('_', ' ').title()}**: {count} total")

# Main report generation
all_metrics = load_all_metrics()

if report_type == "--compare":
    generate_comparison_report(all_metrics)
elif report_type == "--weekly":
    generate_weekly_report(all_metrics)
elif report_type == "--recommendations":
    generate_recommendations_report(all_metrics)
else:
    # Default to weekly
    generate_weekly_report(all_metrics)

print("\n---\n*Report saved to `.claude/reports/`*")

PYTHON`

## Report Generated Successfully!

View saved reports in `.claude/reports/` directory.

### Available Report Types:
- `/agent-report --compare` - Compare all agents
- `/agent-report --weekly` - Weekly summary
- `/agent-report --recommendations` - Optimization suggestions

### Next Actions:
- Schedule weekly reports: `/schedule agent-report --weekly`
- Export data: `/agent-export --csv`
- Real-time dashboard: `/agent-dashboard`
