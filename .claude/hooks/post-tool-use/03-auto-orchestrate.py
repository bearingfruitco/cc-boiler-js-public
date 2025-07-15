#!/usr/bin/env python3
"""
Auto-Orchestration Hook
Automatically triggers multi-agent orchestration when task complexity warrants it
Analyzes generated tasks and suggests spawning specialized agents
"""

import json
import sys
import re
from pathlib import Path
from collections import defaultdict

def load_personas():
    """Load enhanced persona definitions"""
    personas_file = Path(__file__).parent.parent.parent / 'personas' / 'agent-personas-enhanced.json'
    if not personas_file.exists():
        # Fallback to original
        personas_file = Path(__file__).parent.parent.parent / 'personas' / 'agent-personas.json'
    
    try:
        with open(personas_file) as f:
            return json.load(f)
    except:
        return None

def analyze_task_domains(content):
    """Analyze task content to identify required domains"""
    domains = defaultdict(int)
    
    # Domain keyword patterns
    domain_patterns = {
        'frontend': r'\b(component|ui|ux|form|button|layout|style|responsive|accessibility|react|css|animation)\b',
        'backend': r'\b(api|endpoint|database|server|auth|route|middleware|validation|schema)\b',
        'data': r'\b(migration|schema|table|index|query|database|sql|analytics)\b',
        'security': r'\b(encrypt|pii|phi|audit|compliance|vulnerability|auth|owasp)\b',
        'testing': r'\b(test|spec|e2e|coverage|jest|vitest|cypress|playwright)\b',
        'performance': r'\b(optimize|slow|cache|bottleneck|profile|performance|latency)\b',
        'integration': r'\b(webhook|external|third-party|integration|sync|api)\b',
        'devops': r'\b(deploy|docker|kubernetes|ci|cd|pipeline|monitor)\b',
        'refactor': r'\b(refactor|cleanup|technical debt|simplify|extract)\b'
    }
    
    # Count domain mentions
    for domain, pattern in domain_patterns.items():
        matches = len(re.findall(pattern, content, re.IGNORECASE))
        if matches > 0:
            domains[domain] = matches
    
    return domains

def analyze_task_structure(content):
    """Analyze task structure and complexity"""
    lines = content.split('\n')
    
    # Count tasks
    task_count = 0
    epic_count = 0
    subtask_count = 0
    
    for line in lines:
        if re.match(r'^#{1,3}\s+Task\s+\d+\.\d+', line):
            task_count += 1
        elif re.match(r'^#{1,2}\s+Epic\s+\d+', line):
            epic_count += 1
        elif re.match(r'^\s*[-*]\s+', line) and 'subtask' in line.lower():
            subtask_count += 1
    
    # Look for parallel work indicators
    parallel_indicators = [
        'parallel',
        'simultaneously',
        'at the same time',
        'concurrently',
        'independent'
    ]
    
    has_parallel = any(indicator in content.lower() for indicator in parallel_indicators)
    
    return {
        'task_count': task_count,
        'epic_count': epic_count,
        'subtask_count': subtask_count,
        'has_parallel': has_parallel,
        'total_items': task_count + subtask_count
    }

def determine_orchestration_strategy(domains, structure, personas_config):
    """Determine the best orchestration strategy"""
    if not personas_config:
        return None
    
    strategies = personas_config.get('orchestration_strategies', {})
    
    # Check for bug investigation
    if 'analyzer' in domains and domains['analyzer'] > 2:
        return strategies.get('bug_investigation')
    
    # Check for performance optimization
    if 'performance' in domains and domains['performance'] > 3:
        return strategies.get('performance_optimization')
    
    # Check for security audit
    if 'security' in domains and domains['security'] > 2:
        return strategies.get('security_audit')
    
    # Check for deployment
    if 'devops' in domains and domains['devops'] > 2:
        return strategies.get('deployment')
    
    # Check for refactoring
    if 'refactor' in domains and domains['refactor'] > 2:
        return strategies.get('code_quality')
    
    # Check for data work
    if 'data' in domains and domains['data'] > 3:
        return strategies.get('data_migration')
    
    # Full stack if many domains
    active_domains = [d for d, count in domains.items() if count > 1]
    if len(active_domains) >= 5:
        return strategies.get('full_stack')
    
    # Standard feature if frontend + backend
    if 'frontend' in domains and 'backend' in domains:
        return strategies.get('feature_development')
    
    return None

def format_orchestration_suggestion(domains, structure, strategy, feature_name):
    """Format the orchestration suggestion message"""
    active_domains = sorted([(d, count) for d, count in domains.items() if count > 1], 
                           key=lambda x: x[1], reverse=True)
    
    message = "🤖 AUTO-ORCHESTRATION ANALYSIS\n\n"
    
    # Task complexity
    message += f"📊 Task Complexity:\n"
    message += f"- Total tasks: {structure['task_count']}\n"
    message += f"- Epics: {structure['epic_count']}\n"
    message += f"- Complexity: {structure['total_items']} work items\n"
    
    if structure['has_parallel']:
        message += f"- ⚡ Parallel work detected\n"
    
    message += f"\n🎯 Domain Analysis:\n"
    for domain, count in active_domains[:5]:
        message += f"- {domain}: {count} references\n"
    
    if strategy:
        message += f"\n📋 Suggested Strategy: **{strategy.get('description', 'Custom')}**\n"
        message += f"Agents: {' → '.join(strategy.get('agents', []))}\n"
        message += f"Flow: {strategy.get('flow', 'Sequential')}\n"
    
    message += f"\n✅ Recommended Action:\n"
    
    if len(active_domains) >= 3 or structure['total_items'] > 15:
        message += f"```bash\n"
        message += f"/orch {feature_name} --agents={len(active_domains)}\n"
        
        if strategy:
            strategy_map = {
                'bug_investigation': 'debug',
                'performance_optimization': 'performance', 
                'security_audit': 'security',
                'deployment': 'deploy',
                'code_quality': 'refactor',
                'data_migration': 'data',
                'full_stack': 'full'
            }
            
            strategy_key = None
            for key, val in strategy_map.items():
                if strategy.get('description', '').lower().find(key.replace('_', ' ')) != -1:
                    strategy_key = val
                    break
            
            if strategy_key:
                message += f"# Or use specific strategy:\n"
                message += f"/orch {feature_name} --strategy={strategy_key}\n"
        
        message += f"```\n\n"
        message += f"This will spawn {len(active_domains)} specialized agents working in parallel.\n"
    else:
        message += f"Single agent can handle this work efficiently.\n"
        message += f"Use: `/pt {feature_name}` to process tasks sequentially.\n"
    
    return message

def main():
    """Main hook logic"""
    input_data = json.loads(sys.stdin.read())
    
    # Only analyze after task generation
    if input_data.get('tool') != 'write_file':
        print(json.dumps({"action": "continue"}))
        return
        
    file_path = input_data.get('path', '')
    
    # Check if this is a tasks file
    if not re.search(r'-tasks\.md$', file_path):
        print(json.dumps({"action": "continue"}))
        return
    
    content = input_data.get('content', '')
    if not content:
        print(json.dumps({"action": "continue"}))
        return
    
    # Extract feature name
    feature_name = Path(file_path).stem.replace('-tasks', '')
    
    # Load personas config
    personas_config = load_personas()
    
    # Analyze the tasks
    domains = analyze_task_domains(content)
    structure = analyze_task_structure(content)
    
    # Determine orchestration strategy
    strategy = determine_orchestration_strategy(domains, structure, personas_config)
    
    # Decide if orchestration is warranted
    active_domains = [d for d, count in domains.items() if count > 1]
    auto_rules = personas_config.get('auto_orchestration_rules', {}) if personas_config else {}
    
    min_domains = auto_rules.get('min_domains_for_orchestration', 3)
    complexity_threshold = auto_rules.get('task_complexity_threshold', 15)
    
    should_orchestrate = (
        len(active_domains) >= min_domains or 
        structure['total_items'] > complexity_threshold or
        structure['has_parallel']
    )
    
    if should_orchestrate and active_domains:
        message = format_orchestration_suggestion(domains, structure, strategy, feature_name)
        
        # Prepare auto command
        auto_command = f"/orch {feature_name}"
        if len(active_domains) > 0:
            auto_command += f" --agents={min(len(active_domains), 5)}"
        
        print(json.dumps({
            "action": "suggest",
            "message": message,
            "auto_command": auto_command,
            "metadata": {
                "domains": list(domains.keys()),
                "domain_counts": dict(domains),
                "task_count": structure['task_count'],
                "feature": feature_name,
                "strategy": strategy.get('description') if strategy else None
            }
        }))
    else:
        # Single agent is fine
        if active_domains:
            primary_domain = max(domains.items(), key=lambda x: x[1])[0]
            
            print(json.dumps({
                "action": "info",
                "message": f"ℹ️ Task Analysis: Primary domain is '{primary_domain}' ({domains[primary_domain]} references). "
                          f"Single agent can handle this efficiently.\n"
                          f"Continue with: `/pt {feature_name}`",
                "metadata": {
                    "primary_domain": primary_domain,
                    "complexity": "low",
                    "recommendation": "single-agent"
                }
            }))
        else:
            print(json.dumps({"action": "continue"}))

if __name__ == "__main__":
    main()
