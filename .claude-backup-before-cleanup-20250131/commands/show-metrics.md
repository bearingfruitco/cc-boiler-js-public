---
name: show-metrics
description: |
  Display performance metrics and analytics for all agents.
  Shows response times, success rates, token usage, and trends.
  Use PROACTIVELY to monitor system health and optimization opportunities.
argument-hint: [dashboard|report|alerts|agent <name>]
allowed-tools: Bash, Read
aliases: ["metrics", "perf", "performance"]
---

# 📊 Performance Metrics Dashboard

Displaying metrics for: **${ARGUMENTS:-dashboard}**

## Generating Performance Report...

!`python3 .claude/scripts/monitoring/agent-metrics.py ${ARGUMENTS:-dashboard}`

## Additional Analytics Options

Based on your query, here are other metrics you can explore:

### 1. Time-based Analysis
- `/show-metrics report 24` - Last 24 hours
- `/show-metrics report 168` - Last week  
- `/show-metrics report 720` - Last month

### 2. Agent-specific Metrics
- `/show-metrics agent supabase-specialist`
- `/show-metrics agent orm-specialist`
- View any of the 31 agents individually

### 3. Alert Management
- `/show-metrics alerts` - Show all recent alerts
- `/show-metrics alerts critical` - Critical alerts only

### 4. Export Options
View raw data files:
!`ls -la .claude/metrics/*.json | tail -10`

### 5. Real-time Monitoring
Set up continuous monitoring:
```bash
# Watch metrics in real-time (updates every 5 minutes)
watch -n 300 'claude -p "show metrics dashboard"'
```

## Quick Health Check

!`python3 << 'EOF'
import json
from pathlib import Path

# Quick health summary
metrics_file = Path(".claude/metrics/v3-performance.json")
if metrics_file.exists():
    with open(metrics_file) as f:
        metrics = json.load(f)
        
    if metrics:
        recent = [m for m in metrics[-100:]]  # Last 100 executions
        success_rate = sum(1 for m in recent if m['success']) / len(recent) * 100
        avg_time = sum(m['execution_time'] for m in recent) / len(recent)
        
        print("\n🏥 Quick Health Summary:")
        print(f"• Recent Success Rate: {success_rate:.1f}%")
        print(f"• Average Response Time: {avg_time:.2f}s")
        print(f"• Status: {'🟢 Healthy' if success_rate > 95 and avg_time < 2 else '🟡 Needs Attention'}")
EOF`

## Performance Optimization Tips

1. **For Slow Agents**: Consider caching common queries
2. **For High Token Usage**: Optimize prompts and limit response length
3. **For Low Success Rates**: Review error patterns and improve error handling
4. **For Workflow Optimization**: Use context sharing to reduce redundant work

## Set Up Automated Reporting

Create a daily performance report:
```bash
# Add to crontab for daily reports at 9 AM
echo "0 9 * * * cd $(pwd) && python3 .claude/scripts/monitoring/agent-metrics.py report > .claude/metrics/daily-report-\$(date +\%Y\%m\%d).txt" | crontab -
```

Metrics data is continuously collected. Use this command regularly to monitor system health!
