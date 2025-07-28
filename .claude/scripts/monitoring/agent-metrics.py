#!/usr/bin/env python3
"""
Agent Performance Monitoring System for v3.0
Tracks execution metrics, success rates, and generates reports
"""

import json
import time
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import statistics

class AgentMetrics:
    def __init__(self, base_path: str = ".claude"):
        self.base_path = Path(base_path)
        self.metrics_dir = self.base_path / "metrics"
        self.metrics_dir.mkdir(exist_ok=True)
        self.metrics_file = self.metrics_dir / "v3-performance.json"
        self.alerts_file = self.metrics_dir / "performance-alerts.json"
        
        # Performance thresholds
        self.thresholds = {
            'response_time_warning': 2.0,  # seconds
            'response_time_critical': 3.0,
            'success_rate_warning': 0.90,  # 90%
            'success_rate_critical': 0.80,  # 80%
            'token_usage_warning': 2000,
            'token_usage_critical': 4000
        }
        
    def track_agent_execution(self, 
                            agent_name: str, 
                            task: str, 
                            execution_time: float, 
                            success: bool, 
                            tokens_used: Optional[int] = None,
                            error_message: Optional[str] = None) -> Dict:
        """Track individual agent execution metrics"""
        metric = {
            'agent': agent_name,
            'task': task[:200],  # First 200 chars of task
            'execution_time': round(execution_time, 3),
            'success': success,
            'tokens_used': tokens_used,
            'error_message': error_message,
            'timestamp': datetime.now().isoformat(),
            'session_id': os.getenv('CLAUDE_SESSION_ID', 'unknown')
        }
        
        # Append to metrics file
        metrics = self._load_metrics()
        metrics.append(metric)
        self._save_metrics(metrics)
        
        # Check thresholds and create alerts
        self._check_thresholds(agent_name, execution_time, success, tokens_used)
        
        return metric
        
    def _check_thresholds(self, agent_name: str, execution_time: float, 
                         success: bool, tokens_used: Optional[int]) -> None:
        """Check performance thresholds and create alerts"""
        alerts = []
        
        # Response time alerts
        if execution_time > self.thresholds['response_time_critical']:
            alerts.append({
                'type': 'critical',
                'metric': 'response_time',
                'agent': agent_name,
                'value': execution_time,
                'threshold': self.thresholds['response_time_critical'],
                'message': f'{agent_name} response time critically high: {execution_time:.2f}s'
            })
        elif execution_time > self.thresholds['response_time_warning']:
            alerts.append({
                'type': 'warning',
                'metric': 'response_time',
                'agent': agent_name,
                'value': execution_time,
                'threshold': self.thresholds['response_time_warning'],
                'message': f'{agent_name} response time warning: {execution_time:.2f}s'
            })
            
        # Token usage alerts
        if tokens_used:
            if tokens_used > self.thresholds['token_usage_critical']:
                alerts.append({
                    'type': 'critical',
                    'metric': 'token_usage',
                    'agent': agent_name,
                    'value': tokens_used,
                    'threshold': self.thresholds['token_usage_critical'],
                    'message': f'{agent_name} token usage critically high: {tokens_used}'
                })
            elif tokens_used > self.thresholds['token_usage_warning']:
                alerts.append({
                    'type': 'warning',
                    'metric': 'token_usage',
                    'agent': agent_name,
                    'value': tokens_used,
                    'threshold': self.thresholds['token_usage_warning'],
                    'message': f'{agent_name} token usage warning: {tokens_used}'
                })
        
        # Save alerts if any
        if alerts:
            existing_alerts = self._load_alerts()
            for alert in alerts:
                alert['timestamp'] = datetime.now().isoformat()
                existing_alerts.append(alert)
            self._save_alerts(existing_alerts)
            
    def generate_report(self, time_window_hours: int = 24) -> Dict:
        """Generate comprehensive performance report"""
        metrics = self._load_metrics()
        
        # Filter by time window
        cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
        recent_metrics = [
            m for m in metrics 
            if datetime.fromisoformat(m['timestamp']) > cutoff_time
        ]
        
        if not recent_metrics:
            return {'error': 'No metrics found in time window'}
        
        # Calculate stats per agent
        agent_stats = self._calculate_agent_stats(recent_metrics)
        
        # Calculate workflow stats
        workflow_stats = self._calculate_workflow_stats(recent_metrics)
        
        # Overall system stats
        system_stats = self._calculate_system_stats(recent_metrics)
        
        # Get recent alerts
        alerts = self._get_recent_alerts(time_window_hours)
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'time_window_hours': time_window_hours,
            'total_executions': len(recent_metrics),
            'agent_stats': agent_stats,
            'workflow_stats': workflow_stats,
            'system_stats': system_stats,
            'recent_alerts': alerts,
            'recommendations': self._generate_recommendations(agent_stats, system_stats)
        }
        
        # Save report
        report_file = self.metrics_dir / f"performance-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        return report
        
    def _calculate_agent_stats(self, metrics: List[Dict]) -> Dict:
        """Calculate statistics per agent"""
        agent_stats = {}
        
        # Group by agent
        for metric in metrics:
            agent = metric['agent']
            if agent not in agent_stats:
                agent_stats[agent] = {
                    'count': 0,
                    'success_count': 0,
                    'total_time': 0,
                    'execution_times': [],
                    'token_usage': []
                }
            
            stats = agent_stats[agent]
            stats['count'] += 1
            stats['total_time'] += metric['execution_time']
            stats['execution_times'].append(metric['execution_time'])
            
            if metric['success']:
                stats['success_count'] += 1
                
            if metric.get('tokens_used'):
                stats['token_usage'].append(metric['tokens_used'])
                
        # Calculate derived metrics
        for agent, stats in agent_stats.items():
            times = stats['execution_times']
            stats['avg_time'] = round(statistics.mean(times), 3)
            stats['median_time'] = round(statistics.median(times), 3)
            stats['p95_time'] = round(statistics.quantiles(times, n=20)[18], 3) if len(times) > 1 else stats['avg_time']
            stats['p99_time'] = round(statistics.quantiles(times, n=100)[98], 3) if len(times) > 5 else stats['p95_time']
            stats['success_rate'] = round(stats['success_count'] / stats['count'], 3)
            
            if stats['token_usage']:
                stats['avg_tokens'] = round(statistics.mean(stats['token_usage']), 0)
                stats['total_tokens'] = sum(stats['token_usage'])
            else:
                stats['avg_tokens'] = 0
                stats['total_tokens'] = 0
                
            # Remove raw lists for cleaner output
            del stats['execution_times']
            del stats['token_usage']
            del stats['total_time']
            del stats['success_count']
            
        return agent_stats
        
    def _calculate_workflow_stats(self, metrics: List[Dict]) -> Dict:
        """Calculate workflow-level statistics"""
        # Group by session to identify workflows
        sessions = {}
        for metric in metrics:
            session = metric.get('session_id', 'unknown')
            if session not in sessions:
                sessions[session] = []
            sessions[session].append(metric)
            
        workflow_stats = {
            'total_workflows': len(sessions),
            'avg_agents_per_workflow': round(
                statistics.mean([len(s) for s in sessions.values()]), 1
            ) if sessions else 0,
            'workflow_success_rate': round(
                sum(1 for s in sessions.values() if all(m['success'] for m in s)) / len(sessions), 3
            ) if sessions else 0
        }
        
        return workflow_stats
        
    def _calculate_system_stats(self, metrics: List[Dict]) -> Dict:
        """Calculate overall system statistics"""
        all_times = [m['execution_time'] for m in metrics]
        all_tokens = [m['tokens_used'] for m in metrics if m.get('tokens_used')]
        
        return {
            'total_executions': len(metrics),
            'overall_success_rate': round(
                sum(1 for m in metrics if m['success']) / len(metrics), 3
            ),
            'avg_response_time': round(statistics.mean(all_times), 3),
            'p95_response_time': round(statistics.quantiles(all_times, n=20)[18], 3) if len(all_times) > 1 else 0,
            'p99_response_time': round(statistics.quantiles(all_times, n=100)[98], 3) if len(all_times) > 5 else 0,
            'total_tokens_used': sum(all_tokens),
            'unique_agents_used': len(set(m['agent'] for m in metrics))
        }
        
    def _get_recent_alerts(self, hours: int) -> List[Dict]:
        """Get recent performance alerts"""
        alerts = self._load_alerts()
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_alerts = [
            a for a in alerts
            if datetime.fromisoformat(a['timestamp']) > cutoff_time
        ]
        
        # Sort by timestamp descending
        recent_alerts.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return recent_alerts[:10]  # Return top 10 most recent
        
    def _generate_recommendations(self, agent_stats: Dict, system_stats: Dict) -> List[str]:
        """Generate actionable recommendations based on metrics"""
        recommendations = []
        
        # Check for slow agents
        slow_agents = [
            agent for agent, stats in agent_stats.items()
            if stats['avg_time'] > self.thresholds['response_time_warning']
        ]
        if slow_agents:
            recommendations.append(
                f"Optimize these slow agents: {', '.join(slow_agents)}. "
                f"Consider caching or simplifying prompts."
            )
            
        # Check for low success rates
        failing_agents = [
            agent for agent, stats in agent_stats.items()
            if stats['success_rate'] < self.thresholds['success_rate_warning']
        ]
        if failing_agents:
            recommendations.append(
                f"Investigate failures in: {', '.join(failing_agents)}. "
                f"Review error logs and improve error handling."
            )
            
        # Check token usage
        high_token_agents = [
            agent for agent, stats in agent_stats.items()
            if stats.get('avg_tokens', 0) > self.thresholds['token_usage_warning']
        ]
        if high_token_agents:
            recommendations.append(
                f"High token usage in: {', '.join(high_token_agents)}. "
                f"Consider more concise prompts or response limits."
            )
            
        # System-level recommendations
        if system_stats['p99_response_time'] > 3.0:
            recommendations.append(
                "System p99 response time is high. Consider implementing "
                "request queuing or scaling strategies."
            )
            
        if not recommendations:
            recommendations.append("All metrics within acceptable ranges. System performing well!")
            
        return recommendations
        
    def _load_metrics(self) -> List[Dict]:
        """Load metrics from file"""
        if self.metrics_file.exists():
            with open(self.metrics_file) as f:
                return json.load(f)
        return []
        
    def _save_metrics(self, metrics: List[Dict]) -> None:
        """Save metrics to file"""
        with open(self.metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)
            
    def _load_alerts(self) -> List[Dict]:
        """Load alerts from file"""
        if self.alerts_file.exists():
            with open(self.alerts_file) as f:
                return json.load(f)
        return []
        
    def _save_alerts(self, alerts: List[Dict]) -> None:
        """Save alerts to file"""
        with open(self.alerts_file, 'w') as f:
            json.dump(alerts, f, indent=2)
            
    def display_dashboard(self) -> None:
        """Display a simple text dashboard of current metrics"""
        report = self.generate_report(time_window_hours=24)
        
        print("\n" + "="*60)
        print("📊 Claude Code v3.0 Performance Dashboard")
        print("="*60)
        print(f"Generated: {report['generated_at']}")
        print(f"Time Window: Last {report['time_window_hours']} hours")
        print(f"Total Executions: {report['total_executions']}")
        
        print("\n🤖 Agent Performance:")
        print("-"*60)
        print(f"{'Agent':<30} {'Calls':<8} {'Avg(s)':<8} {'P95(s)':<8} {'Success':<8}")
        print("-"*60)
        
        for agent, stats in sorted(report['agent_stats'].items(), 
                                  key=lambda x: x[1]['count'], reverse=True):
            print(f"{agent:<30} {stats['count']:<8} "
                  f"{stats['avg_time']:<8.2f} {stats['p95_time']:<8.2f} "
                  f"{stats['success_rate']*100:<8.1f}%")
                  
        print("\n📈 System Stats:")
        print("-"*60)
        sys_stats = report['system_stats']
        print(f"Overall Success Rate: {sys_stats['overall_success_rate']*100:.1f}%")
        print(f"Average Response Time: {sys_stats['avg_response_time']:.2f}s")
        print(f"P95 Response Time: {sys_stats['p95_response_time']:.2f}s")
        print(f"P99 Response Time: {sys_stats['p99_response_time']:.2f}s")
        print(f"Total Tokens Used: {sys_stats['total_tokens_used']:,}")
        
        if report['recent_alerts']:
            print("\n⚠️  Recent Alerts:")
            print("-"*60)
            for alert in report['recent_alerts'][:5]:
                icon = "🔴" if alert['type'] == 'critical' else "🟡"
                print(f"{icon} {alert['message']}")
                
        print("\n💡 Recommendations:")
        print("-"*60)
        for rec in report['recommendations']:
            print(f"• {rec}")
            
        print("\n" + "="*60)


def main():
    """Main entry point for command line usage"""
    metrics = AgentMetrics()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'track':
            # Example: python agent-metrics.py track agent_name task_desc 1.5 true 500
            if len(sys.argv) >= 6:
                agent = sys.argv[2]
                task = sys.argv[3]
                exec_time = float(sys.argv[4])
                success = sys.argv[5].lower() == 'true'
                tokens = int(sys.argv[6]) if len(sys.argv) > 6 else None
                
                metric = metrics.track_agent_execution(agent, task, exec_time, success, tokens)
                print(f"Tracked: {json.dumps(metric, indent=2)}")
            else:
                print("Usage: python agent-metrics.py track <agent> <task> <time> <success> [tokens]")
                
        elif command == 'report':
            hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
            report = metrics.generate_report(hours)
            print(json.dumps(report, indent=2))
            
        elif command == 'dashboard':
            metrics.display_dashboard()
            
        else:
            print(f"Unknown command: {command}")
            print("Available commands: track, report, dashboard")
    else:
        # Default to dashboard
        metrics.display_dashboard()


if __name__ == "__main__":
    main()
