#!/usr/bin/env python3
"""
Agent performance monitoring for Claude Code Boilerplate v3.0
Tracks execution metrics, success rates, and performance trends
"""

import json
import time
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import defaultdict

class AgentMetrics:
    def __init__(self):
        self.metrics_dir = Path(".claude/metrics")
        self.metrics_dir.mkdir(exist_ok=True)
        self.metrics_file = self.metrics_dir / "v3-performance.json"
        self.summary_file = self.metrics_dir / "v3-performance-summary.json"
        
    def track_agent_execution(self, 
                            agent_name: str, 
                            task: str, 
                            execution_time: float, 
                            success: bool, 
                            tokens_used: Optional[int] = None,
                            error_message: Optional[str] = None):
        """Track individual agent execution metrics"""
        metric = {
            'agent': agent_name,
            'task': task[:200],  # First 200 chars of task
            'execution_time': round(execution_time, 3),
            'success': success,
            'tokens_used': tokens_used,
            'error_message': error_message,
            'timestamp': datetime.now().isoformat(),
            'version': 'v3.0'
        }
        
        # Append to metrics file
        metrics = self._load_metrics()
        metrics.append(metric)
        self._save_metrics(metrics)
        
        # Check performance thresholds
        if execution_time > 2.0:
            print(f"⚠️  Performance warning: {agent_name} took {execution_time:.2f}s")
        
        # Update summary
        self._update_summary(agent_name, execution_time, success)
            
    def generate_report(self, days: int = 7) -> Dict[str, Any]:
        """Generate performance report for the last N days"""
        metrics = self._load_metrics()
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Filter recent metrics
        recent_metrics = [
            m for m in metrics 
            if datetime.fromisoformat(m['timestamp']) > cutoff_date
        ]
        
        # Calculate stats per agent
        agent_stats = defaultdict(lambda: {
            'count': 0,
            'total_time': 0,
            'success_count': 0,
            'error_count': 0,
            'errors': [],
            'p50_time': 0,
            'p95_time': 0,
            'p99_time': 0,
            'avg_time': 0,
            'max_time': 0,
            'min_time': float('inf')
        })
        
        # Collect execution times per agent
        agent_times = defaultdict(list)
        
        for metric in recent_metrics:
            agent = metric['agent']
            stats = agent_stats[agent]
            exec_time = metric['execution_time']
            
            stats['count'] += 1
            stats['total_time'] += exec_time
            agent_times[agent].append(exec_time)
            
            if metric['success']:
                stats['success_count'] += 1
            else:
                stats['error_count'] += 1
                if metric.get('error_message'):
                    stats['errors'].append({
                        'task': metric['task'][:50],
                        'error': metric['error_message'][:100],
                        'timestamp': metric['timestamp']
                    })
            
            stats['max_time'] = max(stats['max_time'], exec_time)
            stats['min_time'] = min(stats['min_time'], exec_time)
        
        # Calculate percentiles and averages
        for agent, times in agent_times.items():
            if not times:
                continue
                
            stats = agent_stats[agent]
            times_sorted = sorted(times)
            n = len(times_sorted)
            
            stats['avg_time'] = round(stats['total_time'] / stats['count'], 3)
            stats['success_rate'] = round((stats['success_count'] / stats['count']) * 100, 1)
            
            # Calculate percentiles
            stats['p50_time'] = round(times_sorted[int(n * 0.5)], 3)
            stats['p95_time'] = round(times_sorted[int(n * 0.95)], 3)
            stats['p99_time'] = round(times_sorted[int(n * 0.99)], 3)
            
            # Clean up errors list (keep last 5)
            stats['errors'] = stats['errors'][-5:]
            
        return {
            'report_date': datetime.now().isoformat(),
            'period_days': days,
            'total_executions': len(recent_metrics),
            'agent_stats': dict(agent_stats),
            'performance_summary': self._get_performance_summary(agent_stats)
        }
    
    def _get_performance_summary(self, agent_stats: Dict) -> Dict[str, Any]:
        """Generate overall performance summary"""
        all_agents = list(agent_stats.keys())
        
        if not all_agents:
            return {'status': 'no_data'}
        
        # Find best and worst performers
        by_avg_time = sorted(all_agents, key=lambda a: agent_stats[a]['avg_time'])
        by_success_rate = sorted(all_agents, 
                                key=lambda a: agent_stats[a]['success_rate'], 
                                reverse=True)
        
        # Identify issues
        slow_agents = [
            a for a in all_agents 
            if agent_stats[a]['p95_time'] > 2.0
        ]
        
        unreliable_agents = [
            a for a in all_agents 
            if agent_stats[a]['success_rate'] < 90 and agent_stats[a]['count'] > 5
        ]
        
        return {
            'fastest_agents': by_avg_time[:3],
            'slowest_agents': by_avg_time[-3:] if len(by_avg_time) > 3 else [],
            'most_reliable': by_success_rate[:3],
            'least_reliable': by_success_rate[-3:] if len(by_success_rate) > 3 else [],
            'performance_warnings': slow_agents,
            'reliability_warnings': unreliable_agents,
            'health_status': self._calculate_health_status(agent_stats)
        }
    
    def _calculate_health_status(self, agent_stats: Dict) -> str:
        """Calculate overall system health status"""
        if not agent_stats:
            return 'no_data'
        
        # Calculate overall metrics
        total_count = sum(s['count'] for s in agent_stats.values())
        total_success = sum(s['success_count'] for s in agent_stats.values())
        avg_success_rate = (total_success / total_count * 100) if total_count > 0 else 0
        
        # Check performance
        avg_p95_times = [
            s['p95_time'] for s in agent_stats.values() 
            if s['count'] > 0
        ]
        overall_p95 = sum(avg_p95_times) / len(avg_p95_times) if avg_p95_times else 0
        
        # Determine status
        if avg_success_rate >= 95 and overall_p95 < 1.5:
            return 'excellent'
        elif avg_success_rate >= 90 and overall_p95 < 2.0:
            return 'good'
        elif avg_success_rate >= 80 and overall_p95 < 3.0:
            return 'fair'
        else:
            return 'needs_attention'
    
    def print_report(self, report: Dict[str, Any]):
        """Print formatted performance report"""
        print("\n📊 V3.0 Agent Performance Report")
        print("=" * 60)
        print(f"Period: Last {report['period_days']} days")
        print(f"Total Executions: {report['total_executions']}")
        print(f"Report Date: {report['report_date'][:19]}")
        
        summary = report['performance_summary']
        print(f"\nHealth Status: {summary['health_status'].upper()}")
        
        print("\n🏆 Top Performers (by speed):")
        for agent in summary['fastest_agents'][:3]:
            stats = report['agent_stats'][agent]
            print(f"  • {agent}: {stats['avg_time']}s avg")
        
        print("\n✅ Most Reliable (by success rate):")
        for agent in summary['most_reliable'][:3]:
            stats = report['agent_stats'][agent]
            print(f"  • {agent}: {stats['success_rate']}% success")
        
        if summary['performance_warnings']:
            print("\n⚠️  Performance Warnings (p95 > 2s):")
            for agent in summary['performance_warnings']:
                stats = report['agent_stats'][agent]
                print(f"  • {agent}: p95={stats['p95_time']}s")
        
        if summary['reliability_warnings']:
            print("\n❌ Reliability Warnings (success < 90%):")
            for agent in summary['reliability_warnings']:
                stats = report['agent_stats'][agent]
                print(f"  • {agent}: {stats['success_rate']}% success rate")
        
        print("\n📈 Detailed Agent Statistics:")
        print("-" * 60)
        print(f"{'Agent':<25} {'Count':>6} {'Avg':>6} {'P95':>6} {'Success':>8}")
        print("-" * 60)
        
        for agent, stats in sorted(report['agent_stats'].items()):
            if stats['count'] > 0:
                print(f"{agent:<25} {stats['count']:>6} "
                      f"{stats['avg_time']:>6.2f}s {stats['p95_time']:>6.2f}s "
                      f"{stats['success_rate']:>7.1f}%")
        
        # Save detailed report
        report_file = self.metrics_dir / f"performance-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📁 Full report saved to: {report_file}")
    
    def _load_metrics(self) -> List[Dict]:
        """Load metrics from file"""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file) as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("⚠️  Warning: Corrupted metrics file, starting fresh")
                return []
        return []
    
    def _save_metrics(self, metrics: List[Dict]):
        """Save metrics to file"""
        # Keep only last 10,000 entries to prevent file bloat
        if len(metrics) > 10000:
            metrics = metrics[-10000:]
            
        with open(self.metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)
    
    def _update_summary(self, agent_name: str, execution_time: float, success: bool):
        """Update running summary statistics"""
        summary = {}
        if self.summary_file.exists():
            try:
                with open(self.summary_file) as f:
                    summary = json.load(f)
            except:
                summary = {}
        
        if agent_name not in summary:
            summary[agent_name] = {
                'total_executions': 0,
                'total_time': 0,
                'success_count': 0,
                'last_execution': None,
                'last_success': None
            }
        
        agent_summary = summary[agent_name]
        agent_summary['total_executions'] += 1
        agent_summary['total_time'] += execution_time
        agent_summary['last_execution'] = datetime.now().isoformat()
        
        if success:
            agent_summary['success_count'] += 1
            agent_summary['last_success'] = datetime.now().isoformat()
        
        with open(self.summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

def main():
    """Main entry point for CLI usage"""
    metrics = AgentMetrics()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'track' and len(sys.argv) >= 5:
            # Track a new metric
            agent = sys.argv[2]
            task = sys.argv[3]
            exec_time = float(sys.argv[4])
            success = sys.argv[5].lower() == 'true' if len(sys.argv) > 5 else True
            tokens = int(sys.argv[6]) if len(sys.argv) > 6 else None
            
            metrics.track_agent_execution(agent, task, exec_time, success, tokens)
            print(f"✅ Tracked: {agent} - {exec_time}s - {'Success' if success else 'Failed'}")
            
        elif command == 'report':
            # Generate report
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            report = metrics.generate_report(days)
            metrics.print_report(report)
            
        else:
            print("Usage:")
            print("  Track: python agent-metrics.py track <agent> <task> <time> [success] [tokens]")
            print("  Report: python agent-metrics.py report [days]")
    else:
        # Default: generate 7-day report
        report = metrics.generate_report(7)
        metrics.print_report(report)

if __name__ == "__main__":
    main()
